# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Coffee shop barista agent implementation."""

import logging
import os
import uuid
import json
from datetime import datetime, timedelta, timezone
from typing import Any, override

import httpx
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from ap2.types.mandate import CART_MANDATE_DATA_KEY, CartContents, CartMandate
from ap2.types.payment_request import PaymentRequest
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from x402_a2a import FacilitatorClient, get_extension_declaration
from x402_a2a.types import (
    EIP3009Authorization,
    ExactPaymentPayload,
    PaymentPayload,
    PaymentRequirements,
)

from .base_agent import BaseAgent
from .menu import (
    BEANS,
    DEFAULT_BEAN,
    DEFAULT_SIZE,
    MENU,
    SIZES,
    calculate_price,
    format_price_usd,
    get_menu_display,
    get_order_description,
    validate_order,
)

logger = logging.getLogger(__name__)

load_dotenv()


class CoffeeShopAgent(BaseAgent):
    """
    Coffee shop barista agent that handles orders and payments.
    
    This agent can:
    - Show the menu with prices and options
    - Create orders with customizable size and bean options
    - Process payments via x402/AP2 protocol
    """

    def __init__(self):
        self._wallet_address = os.getenv("MERCHANT_WALLET_ADDRESS")
        if not self._wallet_address:
            raise ValueError("MERCHANT_WALLET_ADDRESS environment variable not set.")
        self._facilitator = FacilitatorClient()
        self._current_payment_requirements: PaymentRequirements | None = None

    def get_menu(self) -> dict[str, Any]:
        """
        Returns the coffee shop menu with all available drinks, sizes, and bean options.
        This is a free operation that doesn't require payment.
        """
        menu_data = get_menu_display()
        return {
            "message": "☕ 커피숍 메뉴입니다! Here's our menu!",
            **menu_data,
        }

    async def create_order(
        self,
        drink: str,
        size: str = DEFAULT_SIZE,
        bean: str = DEFAULT_BEAN,
    ) -> dict[str, Any]:
        """
        Creates an order for a drink with the specified options.
        Returns a CartMandate with x402 payment requirements.
        
        Args:
            drink: Name of the drink (e.g., "아메리카노", "카페라떼")
            size: Size option (Short/Tall/Grande/Venti), defaults to Tall
            bean: Bean option (일반/디카페인/하프디카페인), defaults to 일반
        """
        # Validate the order
        is_valid, error_msg = validate_order(drink, size, bean)
        if not is_valid:
            return {"error": error_msg}

        # Calculate price
        total_price = calculate_price(drink, size, bean)
        price_usd = format_price_usd(total_price)
        order_description = get_order_description(drink, size, bean)

        # Create PaymentRequirements
        requirements = PaymentRequirements(
            scheme="exact",
            network="base-sepolia",
            asset="0x036CbD53842c5426634e7929541eC2318f3dCF7e",  # USDC on Base Sepolia
            pay_to=self._wallet_address,
            max_amount_required=str(total_price),
            description=f"☕ {order_description} 주문",
            resource=f"/order/{drink}/{size}/{bean}",
            mime_type="application/json",
            max_timeout_seconds=1200,
            extra={
                "name": order_description,
                "description": f"Your order: {order_description}",
                "order_details": {
                    "drink": drink,
                    "size": size,
                    "bean": bean,
                    "drink_description": MENU[drink]["description"],
                    "size_volume": SIZES[size]["volume"],
                    "bean_description": BEANS[bean]["description"],
                },
            },
        )

        # Create x402 Payment Required structure
        x402_payment_required = {
            "x402.payment.required": {
                "x402Version": 1,
                "accepts": [
                    {
                        "scheme": requirements.scheme,
                        "network": requirements.network,
                        "asset": requirements.asset,
                        "payTo": requirements.pay_to,
                        "maxAmountRequired": requirements.max_amount_required,
                    }
                ],
            }
        }

        # Create AP2 PaymentRequest
        order_id = f"order_{drink.lower()}_{uuid.uuid4()}"
        payment_request = PaymentRequest(
            method_data=[
                {
                    "supported_methods": "https://www.x402.org/",
                    "data": x402_payment_required,
                }
            ],
            details={
                "id": order_id,
                "display_items": [
                    {
                        "label": order_description,
                        "amount": {"currency": "USD", "value": price_usd.replace("$", "")},
                    }
                ],
                "total": {
                    "label": "Total",
                    "amount": {"currency": "USD", "value": price_usd.replace("$", "")},
                },
            },
        )

        # Create CartContents
        cart_contents = CartContents(
            id=f"cart_{uuid.uuid4()}",
            user_cart_confirmation_required=True,
            payment_request=payment_request,
            cart_expiry=(
                datetime.now(timezone.utc) + timedelta(minutes=15)
            ).isoformat(),
            merchant_name="☕ AI Coffee Shop",
        )

        # Sign the cart contents
        try:
            payload_to_sign = cart_contents.model_dump_json()
            wallet_url = os.getenv("LOCAL_WALLET_URL", "http://localhost:5001")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{wallet_url}/sign",
                    json={"payload": payload_to_sign},
                )
                response.raise_for_status()
                signature_data = response.json()
                merchant_signature = signature_data.get("signature")
        except httpx.RequestError as e:
            return {"error": f"Failed to contact signing service: {e}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred during signing: {e}"}

        # Create CartMandate
        cart_mandate = CartMandate(
            contents=cart_contents,
            merchant_authorization=merchant_signature,
        )

        # Return artifact and context to save
        cart_mandate_data = {
            CART_MANDATE_DATA_KEY: cart_mandate.model_dump(by_alias=True)
        }

        logger.info(f"Created order: {order_description} for {price_usd}")

        return {
            "artifact": {
                "artifactId": f"cart-mandate-{uuid.uuid4()}",
                "name": "AP2 CartMandate",
                "parts": [
                    {
                        "kind": "data",
                        "data": cart_mandate_data,
                    }
                ],
                "extensions": [
                    "https://github.com/google-agentic-commerce/ap2/tree/v0.1",
                    "https://github.com/google-agentic-commerce/a2a-x402/blob/main/spec/v0.2",
                ],
            },
            "context_to_save": {"payment_requirements": requirements.model_dump()},
        }

    async def process_payment(self, payment_mandate: dict[str, Any]) -> dict[str, Any]:
        """
        Processes the payment mandate received from the client.
        Verifies the payment using the x402 facilitator and settles it.
        """
        try:
            logger.info("📨 Received payment mandate")
            
            # Extract payment payload from the mandate
            # Expected structure from Client Agent:
            # { "payment_mandate_contents": { "payment_response": { "details": ... } } }
            payment_payload_dict = (
                payment_mandate.get("payment_mandate_contents", {})
                .get("payment_response", {})
                .get("details")
            )
            
            if not payment_payload_dict:
                # Fallback for simpler structures
                payment_payload_dict = payment_mandate.get("payment_response", {}).get("details")

            if not payment_payload_dict:
                return {"error": "Invalid payment mandate structure. Could not find payment details."}

            logger.info("✅ extracted payment_payload_dict")

            # Construct PaymentPayload object
            auth_raw = payment_payload_dict["payload"]["authorization"]
            # Ensure numeric fields are strings for EIP3009Authorization
            auth_dict = {
                "from": auth_raw.get("from"),
                "to": auth_raw.get("to"),
                "value": str(auth_raw.get("value")),
                "validAfter": str(auth_raw.get("validAfter")),
                "validBefore": str(auth_raw.get("validBefore")),
                "nonce": auth_raw.get("nonce"),
            }
            payment_payload = PaymentPayload(
                x402_version=payment_payload_dict.get("x402_version", 1),
                scheme=payment_payload_dict.get("scheme", "exact"),
                network=payment_payload_dict.get("network"),
                payload=ExactPaymentPayload(
                    authorization=EIP3009Authorization(
                        from_=auth_dict.get("from"),
                        to=auth_dict.get("to"),
                        value=str(auth_dict.get("value")),
                        valid_after=str(auth_dict.get("validAfter")),
                        valid_before=str(auth_dict.get("validBefore")),
                        nonce=auth_dict.get("nonce"),
                    ),
                    signature=payment_payload_dict["payload"]["signature"],
                ),
            )

            # Reconstruct PaymentRequirements from the payment payload if not loaded from session
            # This handles the case where the payment comes in a different session/context
            payment_requirements = self._current_payment_requirements
            if payment_requirements is None:
                logger.info("Reconstructing payment requirements from payment payload...")
                payment_requirements = PaymentRequirements(
                    scheme=payment_payload_dict.get("scheme", "exact"),
                    network=payment_payload_dict.get("network", "base-sepolia"),
                    asset="0x036CbD53842c5426634e7929541eC2318f3dCF7e",  # USDC on Base Sepolia
                    pay_to=auth_dict.get("to"),
                    max_amount_required=str(auth_dict.get("value")),
                    description="Coffee order payment",
                    # CRITICAL FIX: Must use absolute URL for resource
                    resource="http://localhost:10000/order",
                    mime_type="application/json",
                    max_timeout_seconds=1200,
                )
            
            # Verify Payment
            logger.info("Verifying payment with Facilitator...")
            verify_response = await self._facilitator.verify(
                payment=payment_payload,
                payment_requirements=payment_requirements
            )

            if not verify_response.is_valid:
                logger.error(f"Payment verification failed: {verify_response.invalid_reason}")
                return {"error": f"Payment verification failed: {verify_response.invalid_reason}"}

            logger.info("Payment verified successfully!")

            # Settle Payment
            logger.info("Settling payment...")
            settle_response = await self._facilitator.settle(
                payment=payment_payload,
                payment_requirements=payment_requirements
            )
            
            if not settle_response.success:
                 logger.error(f"Payment settlement failed: {settle_response.error_reason}")
                 return {"error": f"Payment settlement failed: {settle_response.error_reason}"}

            logger.info(f"Payment settled! Transaction: {settle_response.transaction}")

            return {
                "status": "SUCCESS",
                "message": "☕ 결제가 완료되었습니다! 음료를 준비하겠습니다.",
                "transaction": settle_response.transaction,
            }

        except Exception as e:
            logger.error(f"An error occurred during payment processing: {e}", exc_info=True)
            return {"error": f"An unexpected error occurred: {e}"}

    def before_agent_callback(self, callback_context: CallbackContext):
        """
        Callback executed before the agent is invoked.
        Loads payment requirements from session state and handles payment verification.
        """
        if callback_context.state:
            # Load payment requirements if they exist
            requirements_dict = callback_context.state.get("payment_requirements")
            if requirements_dict:
                self._current_payment_requirements = PaymentRequirements(**requirements_dict)
                logger.info("Loaded payment requirements from session state.")
            else:
                self._current_payment_requirements = None

            # Check if payment was verified
            payment_data = callback_context.state.get("payment_verified_data")
            if payment_data:
                # Consume the data so it's not used again
                del callback_context.state["payment_verified_data"]

                # Create a virtual tool response for the LLM
                tool_response = types.Part(
                    function_response=types.FunctionResponse(
                        name="check_payment_status",
                        response=payment_data,
                    )
                )
                callback_context.new_user_message = types.Content(parts=[tool_response])

    @override
    def create_agent(self) -> LlmAgent:
        """Creates the LlmAgent instance for the coffee shop."""
        return LlmAgent(
            model="gemini-2.5-flash",
            name="coffee_shop_agent",
            description="A friendly coffee shop barista agent that takes orders and processes payments.",
            instruction="""당신은 친절한 커피숍 바리스타 AI입니다. You are a friendly coffee shop barista AI.

## 역할 (Your Role)
1. **메뉴 안내**: 고객이 메뉴를 물어보면 `get_menu` 도구를 사용하세요.
2. **주문 접수**: 고객이 음료를 주문하면 `create_order` 도구를 사용하세요.
   - 음료 이름, 사이즈(Short/Tall/Grande/Venti), 원두(일반/디카페인/하프디카페인)를 확인하세요.
   - 사이즈나 원두를 지정하지 않으면 기본값(Tall, 일반)을 사용하세요.
3. **결제 처리**: PaymentMandate를 받으면 `process_payment` 도구를 사용하세요.

## 중요: 메시지 유형 식별 방법

### IntentMandate 식별
메시지에 다음 키가 포함되어 있으면 IntentMandate입니다:
- `natural_language_description`
- `intent_expiry`
→ 주문 내용을 파악하고 `create_order`를 호출하세요.

### PaymentMandate 식별 (매우 중요!)
메시지에 다음 키가 포함되어 있으면 PaymentMandate입니다:
- `payment_mandate_contents`
- `payment_response`
- `user_authorization`
→ **반드시** `process_payment` 도구를 호출하세요! 전체 JSON 객체를 `payment_mandate` 인자로 전달하세요.

## 주문 흐름 (Order Flow)
1. IntentMandate를 받으면 주문 내용을 파악하고 `create_order`를 호출합니다.
2. `create_order`로 CartMandate를 생성하여 반환합니다.
3. PaymentMandate를 받으면 **반드시** `process_payment`를 호출합니다.
4. 결제 성공 시 주문 완료를 알리고 음료 준비를 시작합니다.

## 가격 정보 (Pricing)
- 모든 가격은 Tall 사이즈 기준입니다.
- Short: -$0.005 / Grande: +$0.005 / Venti: +$0.010
- 디카페인/하프디카페인: +$0.003

항상 친절하고 밝은 톤으로 응대하세요! ☕
""",
            tools=[self.get_menu, self.create_order, self.process_payment],
            before_agent_callback=self.before_agent_callback,
        )

    @override
    async def create_agent_card(self, url: str) -> AgentCard:
        """Creates the AgentCard for this agent."""
        from google.adk.a2a.utils.agent_card_builder import AgentCardBuilder

        capabilities = AgentCapabilities(
            streaming=False,
            extensions=[
                get_extension_declaration(
                    description="Supports payments using the x402 protocol for USDC on Base Sepolia.",
                    required=True,
                )
            ],
        )

        builder = AgentCardBuilder(
            agent=self.create_agent(),
            rpc_url=url,
            capabilities=capabilities,
            agent_version="1.0.0",
        )
        card = await builder.build()

        # Override with custom values
        card.name = "☕ AI Coffee Shop"
        card.description = (
            "A friendly coffee shop barista that takes your order and processes "
            "payment via x402 protocol. Supports customizable sizes and bean options."
        )
        card.skills = [
            AgentSkill(
                id="menu",
                name="View Menu",
                description="Shows the coffee shop menu with all drinks, sizes, and bean options.",
                tags=["menu", "coffee", "drinks"],
                examples=[
                    "메뉴 보여줘",
                    "What's on the menu?",
                    "커피 종류가 뭐가 있어요?",
                ],
            ),
            AgentSkill(
                id="order",
                name="Place Order",
                description="Takes a coffee order with customizable size and bean options.",
                tags=["order", "coffee", "payment", "x402"],
                examples=[
                    "아메리카노 한 잔 주세요",
                    "Grande 디카페인 라떼 주문할게요",
                    "I'd like a Venti vanilla latte",
                ],
            ),
        ]
        card.default_input_modes = ["text", "text/plain"]
        card.default_output_modes = ["text", "text/plain"]

        return card


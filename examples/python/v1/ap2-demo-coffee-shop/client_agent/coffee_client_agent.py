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
"""Coffee shop client agent for ordering drinks with customization options."""

import datetime
import json
import logging
import os
import uuid
from typing import Any, Optional

import httpx
from ap2.types.mandate import IntentMandate, PaymentMandate, PaymentMandateContents
from ap2.types.payment_request import PaymentResponse
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.agents import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools import AgentTool
from google.adk.tools.tool_context import ToolContext
from web3 import Web3

from x402_a2a.core.utils import x402Utils
from x402_a2a.core.wallet import get_transfer_with_auth_typed_data

logger = logging.getLogger(__name__)

load_dotenv()

# ABI for USDC contract functions
USDC_ABI = json.loads(
    """
[
    {
      "inputs": [],
      "name": "name",
      "outputs": [{"name": "", "type": "string"}],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "version",
      "outputs": [{"name": "", "type": "string"}],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [{"name": "owner", "type": "address"}],
      "name": "nonces",
      "outputs": [{"name": "", "type": "uint256"}],
      "stateMutability": "view",
      "type": "function"
    }
]
"""
)


class CoffeeClientAgent:
    """
    Client agent specialized for ordering coffee with customization options.
    
    This agent helps users:
    - Browse the coffee menu
    - Customize their order (size, bean type)
    - Complete payment via x402/AP2 protocol
    """

    def __init__(
        self,
        remote_agents: list[BaseAgent],
        http_client: httpx.AsyncClient,
    ):
        """Initialize the CoffeeClientAgent."""
        self.httpx_client = http_client
        self.remote_agents = remote_agents
        agent_list = [
            {"name": agent.name, "description": agent.description}
            for agent in self.remote_agents
        ]
        self.agents_info_str = json.dumps(agent_list, indent=2)
        self.x402 = x402Utils()
        self._wallet_address: Optional[str] = None

    def create_agent(self) -> Agent:
        """Creates the ADK Agent instance."""
        all_tools: list[Any] = [
            self.create_intent_mandate,
            self.sign_intent_mandate,
            self.save_cart_and_inform_user,
            self.pay_for_cart,
            self.sign_payment_request,
            self.create_payment_mandate,
            self.sign_payment_mandate,
            self.forward_signed_payment_mandate,
        ]
        # Add remote agents as tools
        all_tools.extend([AgentTool(agent=agent) for agent in self.remote_agents])

        return Agent(
            model="gemini-2.5-flash",
            name="coffee_client_agent",
            instruction=self.root_instruction,
            before_agent_callback=self.before_agent_callback,
            description="A friendly AI assistant that helps you order coffee with customization options.",
            tools=all_tools,
        )

    async def before_agent_callback(self, callback_context: CallbackContext):
        """Initialize wallet connection before first interaction."""
        if self._wallet_address:
            return

        try:
            wallet_url = os.getenv("LOCAL_WALLET_URL", "http://localhost:5001")
            response = await self.httpx_client.get(f"{wallet_url}/address")
            response.raise_for_status()
            self._wallet_address = response.json().get("address")
            logger.info(f"Connected to wallet: {self._wallet_address[:10]}...")
        except httpx.RequestError as e:
            logger.error(f"Could not connect to wallet: {e}")

    def save_cart_and_inform_user(
        self, cart_mandate_str: str, tool_context: ToolContext
    ) -> str:
        """
        Parses the cart mandate and informs the user about the order details.
        """
        try:
            cart_mandate = json.loads(cart_mandate_str)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode cart_mandate_str: {cart_mandate_str}")
            return "☕ 주문 정보를 이해하지 못했습니다. 다시 시도해주세요."

        # Unwrap the mandate data
        unwrapped_mandate = cart_mandate.get("data", cart_mandate)
        cart_data = unwrapped_mandate.get("ap2.mandates.CartMandate", unwrapped_mandate)
        tool_context.state["cart_mandate"] = cart_data

        # Extract order details
        try:
            contents = cart_data.get("contents", {})
            payment_request = contents.get("payment_request", {})
            details = payment_request.get("details", {})
            
            # Get display items (order items)
            display_items = details.get("display_items", [])
            items_str = "\n".join(
                f"  - {item.get('label')}: ${item.get('amount', {}).get('value')}"
                for item in display_items
            )
            
            # Get total
            total = details.get("total", {}).get("amount", {})
            total_amount = total.get("value", "?")
            total_currency = total.get("currency", "USD")
            
            # Get merchant name
            merchant_name = contents.get("merchant_name", "커피숍")

        except Exception as e:
            logger.error(f"Error parsing cart details: {e}")
            return "주문 정보를 파싱하는 중 오류가 발생했습니다."

        user_message = f"""
☕ **{merchant_name}에서 주문을 준비했습니다!**

📋 **주문 내역:**
{items_str}

💰 **총 금액: ${total_amount} {total_currency}**

결제를 진행하시려면 '결제할게요' 또는 'pay for the cart'라고 말씀해주세요.
"""
        return user_message

    def pay_for_cart(self, tool_context: ToolContext) -> dict[str, str]:
        """Initiates payment for the cart."""
        logger.info("Initiating payment for cart...")
        cart_mandate = tool_context.state.get("cart_mandate")
        
        if not cart_mandate:
            return {"user_message": "☕ 장바구니가 비어있습니다. 먼저 음료를 주문해주세요."}
        
        if not self._wallet_address:
            return {"user_message": "💳 지갑이 연결되지 않았습니다. 설정을 확인해주세요."}

        try:
            # Extract x402 payment requirements
            method_data = (
                cart_mandate.get("contents", {})
                .get("payment_request", {})
                .get("method_data", [])
            )
            
            x402_data = None
            for method in method_data:
                if method.get("supported_methods") == "https://www.x402.org/":
                    x402_data = method.get("data", {}).get("x402.payment.required")
                    break

            if not x402_data:
                raise ValueError("x402 결제 정보를 찾을 수 없습니다.")

            requirements = x402_data
            if not requirements.get("accepts"):
                raise ValueError("결제 옵션을 찾을 수 없습니다.")

            selected_requirement = requirements["accepts"][0]

            # Get EIP-712 domain info from USDC contract
            rpc_url = os.getenv("RPC_URL", "https://sepolia.base.org")
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            usdc_contract = w3.eth.contract(
                address=selected_requirement["asset"], abi=USDC_ABI
            )
            token_name = usdc_contract.functions.name().call()
            token_version = usdc_contract.functions.version().call()

            # Prepare EIP-712 typed data
            chain_id = int(w3.eth.chain_id)
            value = int(selected_requirement["maxAmountRequired"])
            valid_after = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            valid_before = int(
                (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).timestamp()
            )

            typed_data = get_transfer_with_auth_typed_data(
                from_=self._wallet_address,
                to=selected_requirement["payTo"],
                value=value,
                valid_after=valid_after,
                valid_before=valid_before,
                nonce="0x" + os.urandom(32).hex(),
                chain_id=chain_id,
                contract_address=selected_requirement["asset"],
                token_name=token_name,
                token_version=token_version,
            )

            # Store purchase details for later
            tool_context.state["purchase_details"] = {
                "payment_details_id": cart_mandate.get("contents", {})
                    .get("payment_request", {})
                    .get("details", {})
                    .get("id"),
                "payment_details_total": cart_mandate.get("contents", {})
                    .get("payment_request", {})
                    .get("details", {})
                    .get("total"),
                "merchant_agent": cart_mandate.get("contents", {}).get("merchant_name"),
                "request_id": cart_mandate.get("contents", {})
                    .get("payment_request", {})
                    .get("details", {})
                    .get("id"),
                "x402_version": x402_data.get("x402Version"),
                "scheme": selected_requirement.get("scheme"),
                "network": selected_requirement.get("network"),
            }
            tool_context.state["payment_request_to_sign"] = typed_data

            # Format amount for display
            amount_usd = value / 1_000_000

            return {
                "user_message": f"💳 ${amount_usd:.2f} USDC 결제를 준비했습니다.\n\n"
                               f"결제를 승인하려면 'sign payment request' 또는 '결제 승인'이라고 말씀해주세요."
            }

        except Exception as e:
            logger.error(f"Payment preparation failed: {e}", exc_info=True)
            return {"user_message": f"결제 준비 중 오류가 발생했습니다: {e}"}

    async def sign_payment_request(self, tool_context: ToolContext) -> dict[str, str]:
        """Signs the payment request with the wallet."""
        logger.info("Signing payment request...")
        request_to_sign = tool_context.state.get("payment_request_to_sign")
        
        if not request_to_sign:
            return {"user_message": "서명할 결제 요청이 없습니다."}

        try:
            wallet_url = os.getenv("LOCAL_WALLET_URL", "http://localhost:5001")
            response = await self.httpx_client.post(
                f"{wallet_url}/sign",
                json=request_to_sign,
            )
            response.raise_for_status()
            signature_data = response.json()

            purchase_details = tool_context.state.get("purchase_details")
            if not purchase_details:
                raise ValueError("구매 정보가 없습니다.")

            final_payload = {
                "x402_version": purchase_details.get("x402_version", 1),
                "scheme": purchase_details.get("scheme"),
                "network": purchase_details.get("network"),
                "payload": {
                    "signature": signature_data["signature"],
                    "authorization": request_to_sign["message"],
                },
            }

            tool_context.state["signed_payment_payload"] = final_payload
            tool_context.state["payment_request_to_sign"] = None
            logger.info("Payment request signed successfully.")

            return self.create_payment_mandate(tool_context)

        except httpx.RequestError as e:
            logger.error(f"Wallet connection error: {e}")
            return {"user_message": "지갑 연결에 실패했습니다."}
        except Exception as e:
            logger.error(f"Signing error: {e}", exc_info=True)
            return {"user_message": f"서명 중 오류가 발생했습니다: {e}"}

    def create_payment_mandate(self, tool_context: ToolContext) -> dict[str, str]:
        """Creates a payment mandate from the signed payload."""
        logger.info("Creating payment mandate...")
        signed_payload = tool_context.state.get("signed_payment_payload")
        purchase_details = tool_context.state.get("purchase_details")

        if not signed_payload or not purchase_details:
            raise ValueError("결제 정보가 누락되었습니다.")

        payment_response = PaymentResponse(
            request_id=purchase_details["request_id"],
            method_name="https://www.x402.org/",
            details=signed_payload,
        )

        payment_mandate_contents = PaymentMandateContents(
            payment_mandate_id=str(uuid.uuid4()),
            payment_details_id=purchase_details["payment_details_id"],
            payment_details_total=purchase_details["payment_details_total"],
            payment_response=payment_response,
            merchant_agent=purchase_details["merchant_agent"],
        )

        payment_mandate = PaymentMandate(
            payment_mandate_contents=payment_mandate_contents
        )

        tool_context.state["payment_mandate_to_sign"] = payment_mandate.model_dump(by_alias=True)
        tool_context.state["purchase_details"] = None

        return {
            "user_message": "✅ 결제 승인서를 생성했습니다.\n\n"
                           "최종 승인을 위해 'sign payment mandate' 또는 '최종 승인'이라고 말씀해주세요."
        }

    async def sign_payment_mandate(self, tool_context: ToolContext) -> dict[str, Any]:
        """Signs the payment mandate and prepares it for the merchant."""
        logger.info("Signing payment mandate...")
        mandate_to_sign = tool_context.state.get("payment_mandate_to_sign")

        if not mandate_to_sign:
            return {"user_message": "서명할 결제 승인서가 없습니다."}

        try:
            wallet_url = os.getenv("LOCAL_WALLET_URL", "http://localhost:5001")
            payload_to_sign = json.dumps(mandate_to_sign)

            response = await self.httpx_client.post(
                f"{wallet_url}/sign",
                json={"payload": payload_to_sign},
            )
            response.raise_for_status()
            signature_data = response.json()

            # AP2 표준: payment_mandate_contents 루트 래핑 + user_authorization
            mandate_contents = mandate_to_sign.get(
                "payment_mandate_contents", mandate_to_sign
            )
            signed_mandate = {
                "payment_mandate_contents": mandate_contents,
                "user_authorization": signature_data["signature"],
            }

            # Store for downstream forwarding
            tool_context.state["signed_payment_mandate"] = signed_mandate
            tool_context.state["payment_mandate_to_sign"] = None

            logger.info("Payment mandate signed successfully.")

            # Align 반환 형태 with base ap2-demo: include user_message + signed_payment_mandate key
            return {
                "user_message": "✅ 결제 승인서에 서명했습니다. 커피숍 에이전트로 전달합니다.",
                "signed_payment_mandate": signed_mandate,
            }
        except Exception as e:
            logger.error(f"Signing error: {e}", exc_info=True)
            return {"user_message": f"서명 중 오류가 발생했습니다: {e}"}
        except httpx.RequestError as e:
            logger.error(f"Wallet connection error: {e}")
            return {"user_message": "지갑 연결에 실패했습니다."}

    def forward_signed_payment_mandate(
        self, tool_context: ToolContext, agent_name: str = "coffee_shop_agent"
    ) -> dict[str, Any]:
        """
        Ensures the signed mandate is forwarded in the correct AP2 structure.
        Returns the JSON string ready to send to the merchant agent.
        """
        signed_mandate = tool_context.state.get("signed_payment_mandate")
        if not signed_mandate:
            return {
                "user_message": "서명된 결제 승인서가 없습니다. 먼저 'sign payment mandate'를 진행해주세요."
            }

        try:
            message = json.dumps(signed_mandate)
        except Exception as e:
            logger.error(f"Failed to serialize signed_payment_mandate: {e}")
            return {"user_message": "승인서 직렬화에 실패했습니다."}

        return {
            "user_message": "서명된 결제 승인서를 커피숍 에이전트로 전달하세요.",
            "agent_name": agent_name,
            "message": message,
        }

    def create_intent_mandate(
        self,
        natural_language_description: str,
        tool_context: ToolContext,
        merchants: Optional[list[str]] = None,
        skus: Optional[list[str]] = None,
        requires_refundability: bool = False,
    ) -> dict[str, str]:
        """Creates an intent mandate for the coffee order."""
        mandate = IntentMandate(
            natural_language_description=natural_language_description,
            merchants=merchants,
            skus=skus,
            requires_refundability=requires_refundability,
            intent_expiry=(
                datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
            ).isoformat(),
        )
        tool_context.state["intent_mandate_to_sign"] = mandate.model_dump(by_alias=True)

        return {
            "user_message": f"☕ 주문 의향서를 생성했습니다:\n\n"
                           f"📝 \"{mandate.natural_language_description}\"\n\n"
                           f"주문을 확정하려면 'sign intent mandate' 또는 '주문 확정'이라고 말씀해주세요."
        }

    async def sign_intent_mandate(self, tool_context: ToolContext) -> dict[str, Any]:
        """Signs the intent mandate."""
        logger.info("Signing intent mandate...")
        mandate_to_sign = tool_context.state.get("intent_mandate_to_sign")

        if not mandate_to_sign:
            return {"user_message": "서명할 주문 의향서가 없습니다. 먼저 주문 내용을 알려주세요."}

        try:
            wallet_url = os.getenv("LOCAL_WALLET_URL", "http://localhost:5001")
            payload_to_sign = json.dumps(mandate_to_sign)

            response = await self.httpx_client.post(
                f"{wallet_url}/sign",
                json={"payload": payload_to_sign},
            )
            response.raise_for_status()
            signature_data = response.json()

            signed_mandate = mandate_to_sign.copy()
            signed_mandate["signature"] = {
                "signature": signature_data["signature"],
                "signer_address": signature_data["address"],
            }

            tool_context.state["signed_intent_mandate"] = {
                "signed_intent_mandate": signed_mandate
            }
            tool_context.state["intent_mandate_to_sign"] = None

            logger.info("Intent mandate signed successfully.")

            return {
                "user_message": "✅ 주문 의향서에 서명했습니다. 커피숍에 전달하겠습니다!",
                "signed_intent_mandate": signed_mandate,
            }

        except httpx.RequestError as e:
            logger.error(f"Wallet connection error: {e}")
            return {"user_message": "지갑 연결에 실패했습니다."}
        except Exception as e:
            logger.error(f"Signing error: {e}", exc_info=True)
            return {"user_message": f"서명 중 오류가 발생했습니다: {e}"}

    def root_instruction(self, context: ReadonlyContext) -> str:
        """Provides instructions for the coffee ordering agent."""
        return f"""
당신은 친절한 커피 주문 도우미 AI입니다. ☕

## 역할
사용자가 커피를 주문하고 결제하는 과정을 도와줍니다.

## 주문 흐름

### 1단계: 주문 정보 수집
사용자가 커피를 주문하려고 할 때:
- 먼저 `coffee_shop_agent` 도구에 "메뉴 보여줘" 메시지를 보내 최신 메뉴/가격을 받아 사용자에게 그대로 보여줍니다.
- 음료 종류를 확인합니다 (아메리카노, 카페라떼, 카푸치노, 바닐라라떼, 카라멜마끼아또, 모카)
- 사이즈를 확인합니다 (Short, Tall, Grande, Venti) - 기본값: Tall
- 원두를 확인합니다 (일반, 디카페인, 하프디카페인) - 기본값: 일반

**중요**: 사용자가 사이즈나 원두를 지정하지 않으면 기본값을 사용한다고 안내하고 확인을 받으세요.

예시 대화:
- 사용자: "아메리카노 주세요"
- AI: "아메리카노 주문이시네요! ☕ 사이즈는 어떻게 할까요? (Short/Tall/Grande/Venti, 기본: Tall)"
- 사용자: "그란데로요"
- AI: "원두는 일반, 디카페인, 하프디카페인 중에서 선택해주세요. (기본: 일반)"
- 사용자: "일반으로요"
- AI: "Grande 아메리카노 (일반 원두)로 주문하시겠습니까?"

### 2단계: 주문 의향서 생성
사용자가 주문을 확정하면:
1. `create_intent_mandate` 도구를 사용하여 상세한 주문 설명을 포함한 의향서를 생성합니다.
   - natural_language_description에는 "Grande 아메리카노 1잔 (일반 원두)" 형식으로 작성합니다.
2. 사용자에게 서명 요청을 안내합니다.

### 3단계: 의향서 서명 및 전달
사용자가 '주문 확정' 또는 'sign intent mandate'라고 하면:
1. `sign_intent_mandate` 도구를 호출합니다.
2. 서명된 의향서를 `coffee_shop_agent` 도구에 JSON 문자열로 전달합니다.

### 4단계: 장바구니 확인
커피숍에서 CartMandate를 받으면:
1. `save_cart_and_inform_user` 도구를 사용하여 주문 내역과 가격을 사용자에게 보여줍니다.
2. 결제 진행 여부를 확인합니다.

### 5단계: 결제 진행
사용자가 '결제할게요' 또는 'pay for the cart'라고 하면:
1. `pay_for_cart` 도구를 호출합니다.
2. 결제 승인을 안내합니다.

### 6단계: 결제 서명
'결제 승인' 또는 'sign payment request'라고 하면:
1. `sign_payment_request` 도구를 호출합니다.

### 7단계: 최종 승인 및 전달
'최종 승인' 또는 'sign payment mandate'라고 하면:
1. `sign_payment_mandate` 도구를 호출합니다.
2. `forward_signed_payment_mandate` 도구를 호출해 반환된 `message`를 그대로 `coffee_shop_agent`에 JSON 문자열로 전달합니다.

### 8단계: 완료
결제가 완료되면 사용자에게 주문 완료를 알립니다.

## 사용 가능한 에이전트
{self.agents_info_str}

## 주의사항
- 항상 친절하고 밝은 톤으로 응대하세요.
- 한국어와 영어 모두 지원합니다.
- 가격 정보는 커피숍 에이전트에서 받습니다.
- 결제는 USDC 스테이블코인으로 진행됩니다.
"""


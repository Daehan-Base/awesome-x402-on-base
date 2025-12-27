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
"""x402 Executor for the coffee shop using Coinbase Facilitator."""

from typing import override

from a2a.server.agent_execution import AgentExecutor

from x402_a2a import FacilitatorClient, FacilitatorConfig, x402ExtensionConfig
from x402_a2a.executors import x402ServerExecutor
from x402_a2a.types import (
    PaymentPayload,
    PaymentRequirements,
    SettleResponse,
    VerifyResponse,
)


class CoffeeShopExecutor(x402ServerExecutor):
    """
    x402 Server Executor for the coffee shop.
    
    Uses the Coinbase Facilitator (https://x402.org/facilitator) to verify
    and settle payments on Base Sepolia testnet.
    """

    def __init__(
        self,
        delegate: AgentExecutor,
        facilitator_config: FacilitatorConfig | None = None,
    ):
        """
        Initialize the executor.
        
        Args:
            delegate: The underlying agent executor
            facilitator_config: Optional facilitator configuration.
                              Defaults to Coinbase facilitator at https://x402.org/facilitator
        """
        super().__init__(delegate, x402ExtensionConfig())

        # Use Coinbase's default facilitator if no config provided
        if facilitator_config:
            self._facilitator = FacilitatorClient(facilitator_config)
        else:
            # Default to Coinbase facilitator
            self._facilitator = FacilitatorClient()
            print("☕ Using Coinbase Facilitator: https://x402.org/facilitator")

    @override
    async def verify_payment(
        self, payload: PaymentPayload, requirements: PaymentRequirements
    ) -> VerifyResponse:
        """
        Verifies the payment signature and requirements with the facilitator.
        
        This is an off-chain operation that checks:
        - Signature validity
        - Amount matches requirements
        - Payment hasn't expired
        - Nonce hasn't been used
        """
        print(f"🔍 Verifying payment...")
        print(f"   Network: {payload.network}")
        print(f"   Scheme: {payload.scheme}")
        print(f"   Amount: {requirements.max_amount_required} micro USDC")
        
        # Log the actual payload being sent to facilitator
        print(f"📤 Sending to facilitator:")
        print(f"   Payload: {payload.model_dump()}")
        print(f"   Requirements: {requirements.model_dump()}")

        response = await self._facilitator.verify(payload, requirements)
        
        # Log facilitator response
        print(f"📥 Facilitator verification response:")
        print(f"   Valid: {response.is_valid}")
        print(f"   Reason: {getattr(response, 'invalid_reason', 'N/A')}")

        if response.is_valid:
            print("✅ Payment verified successfully!")
        else:
            print(f"⛔ Payment verification failed: {response.invalid_reason}")

        return response

    @override
    async def settle_payment(
        self, payload: PaymentPayload, requirements: PaymentRequirements
    ) -> SettleResponse:
        """
        Settles the payment on-chain via the facilitator.
        
        This triggers the actual USDC transfer on Base Sepolia:
        - Facilitator calls transferWithAuthorization on USDC contract
        - Funds are transferred from customer to merchant wallet
        - Transaction hash is returned
        """
        print(f"💰 Settling payment on-chain...")
        print(f"   To: {requirements.pay_to}")
        
        # Log the actual payload being sent to facilitator
        print(f"📤 Sending to facilitator:")
        print(f"   Payload: {payload.model_dump()}")
        print(f"   Requirements: {requirements.model_dump()}")

        response = await self._facilitator.settle(payload, requirements)
        
        # Log facilitator response
        print(f"📥 Facilitator settlement response:")
        print(f"   Success: {response.success}")
        print(f"   TX Hash: {getattr(response, 'transaction', 'N/A')}")
        print(f"   Network: {getattr(response, 'network', 'N/A')}")
        print(f"   Error: {getattr(response, 'error_reason', 'N/A')}")

        if response.success:
            print(f"✅ Payment settled!")
            print(f"   TX Hash: {response.transaction}")
            print(f"   Network: {response.network}")
        else:
            print(f"⛔ Settlement failed: {response.error_reason}")

        return response


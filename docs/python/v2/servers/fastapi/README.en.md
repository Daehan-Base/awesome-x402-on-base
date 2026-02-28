[한국어](./README.md) | [English](./README.en.md)

# x402 FastAPI Server Example (v2)

> **v2 Documentation (Latest)**
>
> This documentation covers x402 **v2 SDK (v2.2.0+)**.
> For v1 Legacy documentation, see [v1 FastAPI Server](../../../v1/servers/fastapi/README.en.md).
>
> **v2 Example Path**:
> - 📂 Local: [`external/x402/examples/python/servers/fastapi/`](../../../../../external/x402/examples/python/servers/fastapi/)
> - 🔗 Origin: [coinbase/x402/.../servers/fastapi/](https://github.com/coinbase/x402/tree/main/examples/python/servers/fastapi)
>
> **Created**: February 28, 2026
> **Last Verified**: Against `external/x402/examples/python/servers/fastapi/main.py`

---

This guide demonstrates how to implement paid API endpoints using the x402 v2 SDK's FastAPI middleware.

**Web2 Analogy**: Just like SaaS APIs restrict access and charge fees using API keys, x402 middleware automatically verifies payments on every HTTP request. With a single line of middleware, you can monetize endpoints without any separate authentication system or subscription management.

## v1 → v2 Changes

| Item | v1 (Legacy) | v2 |
|------|------------|-----|
| Middleware | `paywall_middleware()` | `PaymentMiddlewareASGI` |
| Pricing | USD string or `TokenAmount` object | `"$0.01"` or `AssetAmount` object |
| Route config | `{"/path": "$0.01"}` | `{"/path": RouteConfig(...)}` |
| Multi-chain | Base only | EVM + Solana simultaneously |
| Network format | `base-sepolia` | `eip155:84532` (CAIP-2) |
| Payment verification | Built-in | Facilitator service |
| Environment variables | `ADDRESS` | `EVM_ADDRESS` + `SVM_ADDRESS` |

## Prerequisites

- Python 3.10 or higher
- Valid Ethereum address to receive payments (EVM)
- Solana address (SVM, required in this example code)

## Setup and Usage

1. Copy the `.env-local` file to `.env` and add your addresses.

```bash
cd external/x402/examples/python/servers/fastapi
cp .env-local .env
```

`.env` file contents:
```bash
EVM_ADDRESS=0xYourEthereumAddress
SVM_ADDRESS=YourSolanaAddress
FACILITATOR_URL=https://x402.org/facilitator
```

> **Note**: The server **receives** payments, so only addresses (public keys) are needed. Private keys are not required.

2. Install dependencies:
```bash
uv sync
```

3. Run the server:
```bash
uv run python main.py
```

The server starts at `http://0.0.0.0:4021`.

## Code Analysis (main.py)

### 1. Network and Configuration

```python
from x402.schemas import AssetAmount, Network

EVM_NETWORK: Network = "eip155:84532"   # Base Sepolia
SVM_NETWORK: Network = "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1"  # Solana Devnet
FACILITATOR_URL = os.getenv("FACILITATOR_URL", "https://x402.org/facilitator")
```

v2 uses CAIP-2 standard network identifiers.

### 2. x402 Resource Server Setup

```python
from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.mechanisms.svm.exact import ExactSvmServerScheme
from x402.server import x402ResourceServer

# Create Facilitator client
facilitator = HTTPFacilitatorClient(FacilitatorConfig(url=FACILITATOR_URL))

# Create resource server and register payment schemes
server = x402ResourceServer(facilitator)
server.register(EVM_NETWORK, ExactEvmServerScheme())
server.register(SVM_NETWORK, ExactSvmServerScheme())
```

Unlike v1, v2 uses a Facilitator service to verify payments.

### 3. Route Configuration

```python
routes = {
    # String price: "$0.01"
    "GET /weather": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=EVM_ADDRESS,
                price="$0.01",
                network=EVM_NETWORK,
            ),
            PaymentOption(
                scheme="exact",
                pay_to=SVM_ADDRESS,
                price="$0.01",
                network=SVM_NETWORK,
            ),
        ],
        mime_type="application/json",
        description="Weather report",
    ),
    # AssetAmount price: Direct USDC token specification
    "GET /premium/*": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=EVM_ADDRESS,
                price=AssetAmount(
                    amount="10000",  # $0.01 USDC (6 decimals)
                    asset="0x036CbD53842c5426634e7929541eC2318f3dCF7e",
                    extra={"name": "USDC", "version": "2"},
                ),
                network=EVM_NETWORK,
            ),
            PaymentOption(
                scheme="exact",
                pay_to=SVM_ADDRESS,
                price="$0.01",
                network=SVM_NETWORK,
            ),
        ],
        mime_type="application/json",
        description="Premium content",
    ),
}
```

**Pricing methods:**
- `"$0.01"` — Dollar-based string (simple)
- `AssetAmount(...)` — Direct token amount specification (precise control)

### 4. Middleware Registration

```python
app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)
```

A single line adds payment verification to all paid endpoints.

### 5. Endpoint Definitions

```python
@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/weather")
async def get_weather() -> WeatherResponse:
    return WeatherResponse(report=WeatherReport(weather="sunny", temperature=70))

@app.get("/premium/content")
async def get_premium_content() -> PremiumContentResponse:
    return PremiumContentResponse(content="This is premium content")
```

- `/health` — Free endpoint (not in route config)
- `/weather` — Paid ($0.01, string price)
- `/premium/content` — Paid ($0.01 USDC, AssetAmount)

## Testing the Server

### 1. Test Free Endpoint

```bash
curl http://localhost:4021/health
# {"status":"ok"}
```

### 2. Test Paid Endpoint (Without Payment)

```bash
curl -i http://localhost:4021/weather
# HTTP/1.1 402 Payment Required
# Response headers contain payment option information
```

### 3. Test with x402 Client

Use the requests or httpx client examples to test automatic payments:

```bash
cd external/x402/examples/python/clients/requests
uv sync && uv run python main.py
```

## Example Code Location

```
external/x402/examples/python/servers/fastapi/
├── main.py           # FastAPI server example
├── .env-local        # Environment variable template
└── pyproject.toml    # Project dependencies (x402[fastapi,evm,svm])
```

## Key Concepts

### x402ResourceServer
- Core async server class in v2
- Registers payment schemes per network
- Payment verification via Facilitator
- Sync variant: `x402ResourceServerSync` (used with Flask)

### PaymentMiddlewareASGI
- FastAPI/Starlette ASGI middleware
- Intercepts requests to paid routes for payment verification
- Returns 402 response + payment options if no payment provided

### RouteConfig
- Defines payment configuration per route
- `accepts`: List of accepted payment options
- `mime_type`: Response MIME type
- `description`: Endpoint description

### PaymentOption
- Defines an individual payment option
- `scheme`: Payment scheme ("exact")
- `pay_to`: Recipient address
- `price`: Price (string or AssetAmount)
- `network`: Network identifier (CAIP-2)

### Facilitator
- External service that performs payment verification
- Default: `https://x402.org/facilitator`
- Handles payment signature verification and settlement

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `EVM_ADDRESS` | Yes | EVM address to receive payments |
| `SVM_ADDRESS` | Yes | Solana address to receive payments |
| `FACILITATOR_URL` | No | Facilitator URL (default: `https://x402.org/facilitator`) |

## Next Steps

- [Flask Server Example](../flask/README.en.md) - Build a sync Flask-based server
- [requests Client Example](../../clients/requests/README.en.md) - Test server with sync client
- [httpx Client Example](../../clients/httpx/README.en.md) - Test server with async client

## Additional Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- x402 Protocol Specification: [📂 Local](../../../../../external/x402/) | [🔗 Origin](https://github.com/coinbase/x402)
- [Base Network Documentation](https://docs.base.org/)

---

[← Back to v2 Documentation](../../README.en.md) | [View v1 Legacy →](../../../v1/servers/fastapi/README.en.md)

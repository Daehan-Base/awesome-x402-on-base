[한국어](./README.md) | [English](./README.en.md)

# x402 Flask Server Example (v2)

> **v2 Documentation (Latest)**
>
> This documentation covers x402 **v2 SDK (v2.2.0+)**.
> Flask support is newly added in v2 (v1 only supported FastAPI).
>
> **v2 Example Path**:
> - 📂 Local: [`external/x402/examples/python/servers/flask/`](../../../../../external/x402/examples/python/servers/flask/)
> - 🔗 Origin: [coinbase/x402/.../servers/flask/](https://github.com/coinbase/x402/tree/main/examples/python/servers/flask)
>
> **Created**: February 28, 2026
> **Last Verified**: Against `external/x402/examples/python/servers/flask/main.py`

---

This guide demonstrates how to implement paid API endpoints using the x402 v2 SDK's Flask middleware.

**Web2 Analogy**: Just like requiring authentication with `@login_required` decorator in Flask, x402 middleware requires payment for specific routes. Adding a single line of middleware to your existing Flask app monetizes your endpoints.

## Comparison with FastAPI

Flask support is new in v2 and was not available in v1. Key differences from FastAPI (async):

| Item | FastAPI (async) | Flask (sync) |
|------|-----------------|-------------|
| Server type | ASGI | WSGI |
| Resource server | `x402ResourceServer` | `x402ResourceServerSync` |
| Facilitator client | `HTTPFacilitatorClient` | `HTTPFacilitatorClientSync` |
| Middleware registration | `app.add_middleware(PaymentMiddlewareASGI, ...)` | `payment_middleware(app, ...)` |
| Response model | Pydantic `BaseModel` | `jsonify()` dicts |
| Server runner | `uvicorn.run(app, ...)` | `app.run(host=..., port=...)` |

## Prerequisites

- Python 3.10 or higher
- Valid Ethereum address to receive payments (EVM)
- Solana address (SVM, required in this example code)

## Setup and Usage

1. Copy the `.env-local` file to `.env` and add your addresses.

```bash
cd external/x402/examples/python/servers/flask
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

Uses the same CAIP-2 standard network identifiers as the FastAPI example.

### 2. x402 Resource Server Setup (Sync)

```python
from x402.http import FacilitatorConfig, HTTPFacilitatorClientSync, PaymentOption
from x402.http.middleware.flask import payment_middleware
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.mechanisms.svm.exact import ExactSvmServerScheme
from x402.server import x402ResourceServerSync

# Create sync Facilitator client
facilitator = HTTPFacilitatorClientSync(FacilitatorConfig(url=FACILITATOR_URL))

# Create sync resource server and register payment schemes
server = x402ResourceServerSync(facilitator)
server.register(EVM_NETWORK, ExactEvmServerScheme())
server.register(SVM_NETWORK, ExactSvmServerScheme())
```

Since Flask is a WSGI-based synchronous framework, it uses `x402ResourceServerSync` and `HTTPFacilitatorClientSync`.

### 3. Route Configuration

```python
routes = {
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

Route configuration uses the exact same `RouteConfig` structure as the FastAPI example.

### 4. Middleware Registration

```python
payment_middleware(app, routes=routes, server=server)
```

In Flask, middleware is registered via a function call (unlike FastAPI's `app.add_middleware()`).

### 5. Endpoint Definitions

```python
@app.route("/health")
def health_check():
    return jsonify({"status": "ok"})

@app.route("/weather")
def get_weather():
    return jsonify({"report": {"weather": "sunny", "temperature": 70}})

@app.route("/premium/content")
def get_premium_content():
    return jsonify({"content": "This is premium content"})
```

Standard Flask patterns for endpoint definitions, using `jsonify()` for JSON responses.

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

```bash
cd external/x402/examples/python/clients/requests
uv sync && uv run python main.py
```

## Example Code Location

```
external/x402/examples/python/servers/flask/
├── main.py           # Flask server example
├── .env-local        # Environment variable template
└── pyproject.toml    # Project dependencies (x402[flask,evm,svm])
```

## Key Concepts

### x402ResourceServerSync
- Synchronous server class in v2 (for Flask/WSGI)
- Async variant: `x402ResourceServer` (used with FastAPI)
- Same payment scheme registration API

### payment_middleware (Flask)
- Function that adds payment verification middleware to a Flask app
- Same functionality as FastAPI's `PaymentMiddlewareASGI`
- `payment_middleware(app, routes=routes, server=server)`

### HTTPFacilitatorClientSync
- Synchronous HTTP Facilitator client
- Used in Flask/WSGI environments
- Async variant: `HTTPFacilitatorClient`

### Flask vs FastAPI Selection Criteria

| Criteria | Flask | FastAPI |
|----------|-------|---------|
| Existing code | Already have a Flask app | New project |
| Async needed | No | Yes |
| Performance requirements | Moderate | High |
| API docs | Manual | Automatic (OpenAPI) |
| Type hints | Optional | Required |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `EVM_ADDRESS` | Yes | EVM address to receive payments |
| `SVM_ADDRESS` | Yes | Solana address to receive payments |
| `FACILITATOR_URL` | No | Facilitator URL (default: `https://x402.org/facilitator`) |

## Next Steps

- [FastAPI Server Example](../fastapi/README.en.md) - Build an async FastAPI server
- [requests Client Example](../../clients/requests/README.en.md) - Test server with sync client
- [httpx Client Example](../../clients/httpx/README.en.md) - Test server with async client

## Additional Resources

- [Flask Official Documentation](https://flask.palletsprojects.com/)
- x402 Protocol Specification: [📂 Local](../../../../../external/x402/) | [🔗 Origin](https://github.com/coinbase/x402)
- [Base Network Documentation](https://docs.base.org/)

---

[← Back to v2 Documentation](../../README.en.md) | [View FastAPI Server →](../fastapi/README.en.md)

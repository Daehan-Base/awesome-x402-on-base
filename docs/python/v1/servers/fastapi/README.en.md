[한국어](./README.md) | [English](./README.en.md)

# x402 FastAPI Server Example (v1 Legacy)

> **Legacy Documentation (v1)**
>
> This documentation covers x402 **v1 SDK**.
> For the latest v2 spec, see [x402-v2-specification.md](../../../../x402-v2-specification.md).
>
> **v1 Example Path**:
> - 📂 Local: [`external/x402/examples/python/legacy/servers/fastapi/`](../../../../../external/x402/examples/python/legacy/servers/fastapi/)
> - 🔗 Origin: [coinbase/x402/.../servers/fastapi/](https://github.com/coinbase/x402/tree/main/examples/python/legacy/servers/fastapi)

---

This guide introduces how to implement paid API endpoints using x402 FastAPI middleware. This example demonstrates how to add paywall functionality to your API to monetize endpoint access.

## Prerequisites

- Python 3.10 or higher
- A valid Ethereum address to receive payments

## Setup and Usage

1. Copy the `.env-local` file to `.env` and add your Ethereum address to receive payments:

```bash
cd external/x402/examples/python/legacy/servers/fastapi
cp .env-local .env
```

`.env` file contents:
```bash
ADDRESS=0xYourEthereumAddress
```

2. Install dependencies:
```bash
uv sync
```

3. Run the server:
```bash
uv run python main.py
```

The server will start at http://localhost:4021.

## How x402 FastAPI Middleware Works

The x402 FastAPI middleware requires payment for specific paths. When a client tries to access a protected endpoint:

1. **First Request**: Middleware intercepts requests without payment information
2. **402 Response**: Server returns a 402 Payment Required response with payment requirements
3. **Client Payment**: Client generates and signs payment information
4. **Retry Request**: Client retries the request with payment headers
5. **Verification and Response**: Middleware verifies payment and executes the actual endpoint handler

## Basic Example Code Analysis

```python
import os
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from x402.fastapi.middleware import require_payment
from x402.types import EIP712Domain, TokenAmount, TokenAsset

# Load environment variables
load_dotenv()

# Get configuration from environment variables
ADDRESS = os.getenv("ADDRESS")

if not ADDRESS:
    raise ValueError("Missing required environment variables")

app = FastAPI()

# Apply payment middleware to a specific path - using USD pricing
app.middleware("http")(
    require_payment(
        path="/weather",           # Endpoint path to protect
        price="$0.001",            # USD price (automatically converted to tokens)
        pay_to_address=ADDRESS,    # Address to receive payments
        network="base-sepolia",    # Network (base-sepolia, base, etc.)
    )
)

# Define endpoint
@app.get("/weather")
async def get_weather() -> Dict[str, Any]:
    return {
        "report": {
            "weather": "sunny",
            "temperature": 70,
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4021)
```

## Advanced Configuration: Token Payments

You can also receive payments in specific tokens instead of USD pricing:

```python
# Apply USDC token payment middleware to premium path
app.middleware("http")(
    require_payment(
        path="/premium/*",         # Protect multiple paths with wildcard
        price=TokenAmount(
            amount="10000",        # Token amount (in smallest units)
            asset=TokenAsset(
                address="0x036CbD53842c5426634e7929541eC2318f3dCF7e",  # USDC token address
                decimals=6,        # Token decimal places
                eip712=EIP712Domain(
                    name="USDC",   # Token name for EIP-712 signing
                    version="2"    # EIP-712 signing version
                ),
            ),
        ),
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

@app.get("/premium/content")
async def get_premium_content() -> Dict[str, Any]:
    return {
        "content": "This is premium content",
    }
```

### Understanding TokenAmount Configuration

- **amount**: Amount expressed in the token's smallest units (e.g., USDC has 6 decimals, so 10000 = 0.01 USDC)
- **asset.address**: Token contract address
- **asset.decimals**: Token decimal places (USDC is 6, DAI is 18)
- **asset.eip712**: Domain information for EIP-712 signing standard

## Adding Paid Endpoints

Follow these patterns to add new paid endpoints:

### 1. Simple USD Price Endpoint

```python
# Middleware configuration
app.middleware("http")(
    require_payment(
        path="/api/data",
        price="$0.05",              # 5 cents
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

# Endpoint definition
@app.get("/api/data")
async def get_data():
    return {
        "data": "Your valuable data here"
    }
```

### 2. Protecting Multiple Endpoints with Path Patterns

```python
# Protect all endpoints under /api/v2/*
app.middleware("http")(
    require_payment(
        path="/api/v2/*",
        price="$0.10",
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

@app.get("/api/v2/users")
async def get_users():
    return {"users": []}

@app.get("/api/v2/posts")
async def get_posts():
    return {"posts": []}
```

### 3. Multiple Endpoints with Different Price Tiers

```python
# Low-price endpoint
app.middleware("http")(
    require_payment(
        path="/basic/*",
        price="$0.01",
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

# High-price endpoint
app.middleware("http")(
    require_payment(
        path="/premium/*",
        price="$1.00",
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

@app.get("/basic/info")
async def basic_info():
    return {"info": "Basic information"}

@app.get("/premium/analytics")
async def premium_analytics():
    return {"analytics": "Detailed analytics data"}
```

### 4. Protecting POST Requests

```python
app.middleware("http")(
    require_payment(
        path="/api/process",
        price="$0.50",
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

@app.post("/api/process")
async def process_data(data: dict):
    # Data processing logic
    return {"result": "processed", "data": data}
```

## Middleware Configuration Options

### require_payment Parameters

- **path** (str): Path to protect (supports wildcard `*`)
- **price** (str | TokenAmount):
  - String: USD price (e.g., `"$0.10"`)
  - TokenAmount: Specific token amount
- **pay_to_address** (str): Ethereum address to receive payments
- **network** (str): Blockchain network (`"base"`, `"base-sepolia"`, etc.)

### Path Pattern Rules

```python
# Exact path matching
path="/weather"              # Matches only /weather

# Prefix matching
path="/api/*"                # All paths starting with /api/

# Nested paths
path="/api/v1/premium/*"     # All paths starting with /api/v1/premium/
```

## Testing the Server

### 1. Test Free Endpoints

Your server may have default endpoints that don't require payment:

```bash
curl http://localhost:4021/
# or
curl http://localhost:4021/health
```

### 2. Test Paid Endpoints (Without Payment)

Requesting without payment will return a 402 response:

```bash
curl -v http://localhost:4021/weather
```

Response:
```
< HTTP/1.1 402 Payment Required
< x-accept-402: 1.0
< x-acceptpayment-address: 0xYourAddress
< x-acceptpayment-amount: 1000
< x-acceptpayment-asset: 0x036CbD53842c5426634e7929541eC2318f3dCF7e
...
```

### 3. Test with x402 Client

Using an x402 client will automatically handle payments:

```python
# Using requests
from x402.clients import x402_requests
from eth_account import Account

account = Account.from_key("your_private_key")
session = x402_requests(account)
response = session.get("http://localhost:4021/weather")
print(response.json())
```

```python
# Using httpx (async)
from x402.clients import x402HttpxClient
from eth_account import Account

account = Account.from_key("your_private_key")

async with x402HttpxClient(
    account=account,
    base_url="http://localhost:4021"
) as client:
    response = await client.get("/weather")
    print(response.json())
```

### 4. Test with Manual Payment Headers

Advanced users can manually generate payment headers:

```bash
curl http://localhost:4021/weather \
  -H "x-payment-address: 0xYourAddress" \
  -H "x-payment-amount: 1000" \
  -H "x-payment-asset: 0x036CbD53842c5426634e7929541eC2318f3dCF7e" \
  -H "x-payment-signature: 0x..."
```

## Example Code Location

```
external/x402/examples/python/legacy/servers/fastapi/
├── main.py           # FastAPI server example
├── .env-local        # Environment variable template
└── pyproject.toml    # Project dependencies
```

## Key Concepts

### FastAPI Middleware

- **HTTP Middleware**: Intercepts and processes all HTTP requests
- **Path-based Filtering**: Apply payment requirements to specific paths only
- **Automatic 402 Response**: Automatically returns 402 response for requests without payment
- **Payment Verification**: Automatically verifies and processes payment signatures

### Pricing Options

#### USD Pricing (Recommended)
```python
price="$0.10"  # Simple and intuitive
```

- Automatically converts to appropriate tokens
- Protection from price volatility
- User-friendly

#### Token Amount
```python
price=TokenAmount(
    amount="10000",
    asset=TokenAsset(...)
)
```

- Receive payment in specific tokens
- Precise amount control
- Custom token support

### Network Configuration

- **base**: Base Mainnet (production)
- **base-sepolia**: Base Sepolia Testnet (development/testing)

### Security Considerations

1. **Environment Variables**: Store sensitive information in `.env` file and exclude from version control
2. **Address Verification**: Ensure ADDRESS environment variable is set
3. **Network Matching**: Ensure client and server use the same network
4. **HTTPS**: Recommend using HTTPS in production environments

## Practical Use Cases

### AI API Service

```python
app.middleware("http")(
    require_payment(
        path="/ai/*",
        price="$0.02",  # 2 cents per request
        pay_to_address=ADDRESS,
        network="base",
    )
)

@app.post("/ai/chat")
async def ai_chat(prompt: str):
    # Call AI model
    response = await call_ai_model(prompt)
    return {"response": response}

@app.post("/ai/image")
async def ai_image(description: str):
    # Generate image
    image_url = await generate_image(description)
    return {"image_url": image_url}
```

### Data API Service

```python
# Free tier
@app.get("/data/sample")
async def sample_data():
    return {"data": "Limited sample data"}

# Paid tier
app.middleware("http")(
    require_payment(
        path="/data/full",
        price="$0.50",
        pay_to_address=ADDRESS,
        network="base",
    )
)

@app.get("/data/full")
async def full_data():
    return {"data": "Complete dataset"}
```

### Tiered Pricing

```python
# Basic tier - $0.01
app.middleware("http")(
    require_payment(
        path="/tier/basic/*",
        price="$0.01",
        pay_to_address=ADDRESS,
        network="base",
    )
)

# Pro tier - $0.10
app.middleware("http")(
    require_payment(
        path="/tier/pro/*",
        price="$0.10",
        pay_to_address=ADDRESS,
        network="base",
    )
)

# Enterprise tier - $1.00
app.middleware("http")(
    require_payment(
        path="/tier/enterprise/*",
        price="$1.00",
        pay_to_address=ADDRESS,
        network="base",
    )
)
```

## Troubleshooting

### Environment Variable Error
```
ValueError: Missing required environment variables
```
**Solution**: Ensure ADDRESS is set in your `.env` file

### Port Conflict
```
OSError: [Errno 48] Address already in use
```
**Solution**: Use a different port
```python
uvicorn.run(app, host="0.0.0.0", port=4022)
```

### Client Connection Failure
**Check**:
1. Verify the server is running
2. Check firewall settings
3. Use the correct URL (`http://localhost:4021`)

### Payment Verification Failure
**Check**:
1. Ensure client and server use the same network
2. Verify the token address is correct
3. Verify the payment amount is correct

## Next Steps

- [requests Client Example](../../clients/requests/README.en.md) - Test server with sync client
- [httpx Client Example](../../clients/httpx/README.en.md) - Test server with async client
- [Discovery Example](../../discovery/README.en.md) - x402 service discovery

## Additional Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [x402 Protocol Specification](https://github.com/coinbase/x402)
- [Base Network Documentation](https://docs.base.org/)

---

[← Back to v1 Documentation](../../README.en.md) | [View v2 Spec →](../../../../x402-v2-specification.md)

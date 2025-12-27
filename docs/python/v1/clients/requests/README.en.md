[한국어](./README.md) | [English](./README.en.md)

# x402 requests Client Example (v1 Legacy)

> **Legacy Documentation (v1)**
>
> This documentation covers x402 **v1 SDK**.
> For the latest v2 spec, see [x402-v2-specification.md](../../../../x402-v2-specification.md).
>
> **v1 Example Path**: [python/legacy/clients/requests](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/requests)

---

This guide introduces two methods of using the x402 package with requests to make requests to 402-protected endpoints.

## Setup and Usage

1. Copy the `.env-local` file to `.env` and add your private key.

```bash
cd external/x402/examples/python/legacy/clients/requests
cp .env-local .env
```

2. Install dependencies:
```bash
uv sync
```

3. Run the examples:
```bash
# Simple approach
python main.py

# Extensible approach
python extensible.py
```

## Two Integration Approaches

### Simple Approach (main.py)

The simple approach uses `x402_requests`, which returns a pre-configured session that handles payments automatically:

```python
from x402.clients import x402_requests

session = x402_requests(account)
response = session.get(url)
```

**Advantages:**
- Quick and easy setup
- Create an x402-enabled session in one line
- Ideal for beginners

### Extensible Approach (extensible.py)

The extensible approach uses `x402_http_adapter` with a custom requests session:

```python
from x402.clients import x402_http_adapter
import requests

session = requests.Session()
adapter = x402_http_adapter(account)
session.mount("http://", adapter)
session.mount("https://", adapter)
response = session.get(url)
```

**Advantages:**
- Full control over the session
- Easy integration with existing requests code
- Add custom settings and middleware

## How It Works

Both examples work as follows:

1. Initialize an eth_account.Account instance from a private key
2. Configure a requests session with x402 payment handling
3. Make a request to the protected endpoint
4. Automatically handle 402 Payment Required responses
5. Output the final response

## Example Code Location

```
external/x402/examples/python/legacy/clients/requests/
├── main.py           # Simple approach example
├── extensible.py     # Extensible approach example
├── .env-local        # Environment variable template
└── pyproject.toml    # Project dependencies
```

## Key Concepts

### x402_requests
- Helper function that returns a fully configured session object
- Uses `x402_http_adapter` internally
- Ideal for quick prototyping

### x402_http_adapter
- Extends requests HTTPAdapter
- Intercepts 402 responses and handles payments
- Can be integrated into existing requests workflows

## Next Steps

- [httpx Client Example](../httpx/README.en.md) - Async client implementation
- [FastAPI Server Example](../../servers/fastapi/README.en.md) - Build a 402-protected server
- [Discovery Example](../../discovery/README.en.md) - x402 service discovery

---

[← Back to v1 Documentation](../../README.en.md) | [View v2 Spec →](../../../../x402-v2-specification.md)

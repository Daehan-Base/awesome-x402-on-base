[한국어](./README.md) | [English](./README.en.md)

# x402 httpx Client Example (v1 Legacy)

> **Legacy Documentation (v1)**
>
> This documentation covers x402 **v1 SDK**.
> For the latest v2 spec, see [x402-v2-specification.md](../../../../x402-v2-specification.md).
>
> **v1 Example Path**: [python/legacy/clients/httpx](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/httpx)

---

This guide introduces two methods of using the x402 package with httpx to make async requests to 402-protected endpoints.

## Setup and Usage

1. Copy the `.env-local` file to `.env` and add your private key.

```bash
cd external/x402/examples/python/legacy/clients/httpx
cp .env-local .env
```

2. Install dependencies:
```bash
uv sync
```

3. Run the examples:
```bash
# Simple approach
uv run python main.py

# Extensible approach
uv run python extensible.py
```

## Two Integration Approaches

### Simple Approach (main.py)

The simple approach uses `x402HttpxClient`, a pre-configured client that handles payments automatically:

```python
from x402.clients import x402HttpxClient

async with x402HttpxClient(account=account, base_url=base_url) as client:
    response = await client.get(endpoint_path)
```

**Advantages:**
- Async context manager support
- Automatic resource management
- Ready to use with minimal code
- Ideal for beginners and quick prototyping

### Extensible Approach (extensible.py)

The extensible approach uses `x402_payment_hooks` with a custom httpx client:

```python
from x402.clients import x402_payment_hooks
import httpx

async with httpx.AsyncClient(base_url=base_url) as client:
    client.event_hooks = x402_payment_hooks(account)
    response = await client.get(endpoint_path)
```

**Advantages:**
- Full control over client configuration
- Easy integration with existing httpx code
- Add custom timeouts, headers, and interceptors
- Suitable for production environments

## How It Works

Both examples work as follows:

1. Initialize an eth_account.Account instance from a private key
2. Configure an httpx client with x402 payment handling
3. Make an async request to the protected endpoint
4. Automatically handle 402 Payment Required responses
5. Output the final response

## httpx vs requests

### When to choose httpx:
- When async I/O is needed (async/await)
- When high concurrency is required
- When HTTP/2 support is needed
- When leveraging modern Python features

### When to choose requests:
- Simple synchronous scripts
- Legacy codebase integration
- When async is not necessary

## Example Code Location

```
external/x402/examples/python/legacy/clients/httpx/
├── main.py           # Simple approach example
├── extensible.py     # Extensible approach example
├── .env-local        # Environment variable template
└── pyproject.toml    # Project dependencies
```

## Key Concepts

### x402HttpxClient
- Pre-configured client extending httpx.AsyncClient
- Built-in automatic payment handling
- Safe resource management via context manager

### x402_payment_hooks
- Utilizes httpx's event hook system
- Intercepts 402 responses and handles payments
- Easy integration into existing httpx workflows

### Async Programming
```python
# Process multiple requests concurrently
import asyncio

async def fetch_multiple():
    async with x402HttpxClient(account=account, base_url=base_url) as client:
        tasks = [
            client.get("/endpoint1"),
            client.get("/endpoint2"),
            client.get("/endpoint3"),
        ]
        responses = await asyncio.gather(*tasks)
        return responses
```

## Next Steps

- [requests Client Example](../requests/README.en.md) - Sync client implementation
- [FastAPI Server Example](../../servers/fastapi/README.en.md) - Build a 402-protected server
- [Discovery Example](../../discovery/README.en.md) - x402 service discovery

---

[← Back to v1 Documentation](../../README.en.md) | [View v2 Spec →](../../../../x402-v2-specification.md)

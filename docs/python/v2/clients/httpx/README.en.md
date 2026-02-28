[한국어](./README.md) | [English](./README.en.md)

# x402 httpx Client Example (v2)

> **v2 Documentation (Latest)**
>
> This documentation covers x402 **v2 SDK (v2.2.0+)**.
> For v1 Legacy documentation, see [v1 httpx Client](../../../v1/clients/httpx/README.en.md).
>
> **v2 Example Path**:
> - 📂 Local: [`external/x402/examples/python/clients/httpx/`](../../../../../external/x402/examples/python/clients/httpx/)
> - 🔗 Origin: [coinbase/x402/.../clients/httpx/](https://github.com/coinbase/x402/tree/main/examples/python/clients/httpx)
>
> **Created**: February 28, 2026
> **Last Verified**: Against `external/x402/examples/python/clients/httpx/main.py`

---

This guide demonstrates how to use the x402 v2 SDK with httpx to send async payment requests to 402-protected endpoints.

**Web2 Analogy**: Just like calling APIs with async HTTP clients (httpx, aiohttp), the x402 httpx client handles payments using the `async/await` pattern. You can efficiently process large volumes of paid API calls asynchronously.

## v1 → v2 Changes

| Item | v1 (Legacy) | v2 |
|------|------------|-----|
| Client | `x402_httpx(account)` | `x402HttpxClient(x402Client())` |
| Signer | Direct `eth_account.Account` | `EthAccountSigner` wrapper |
| Multi-chain | EVM only | EVM + Solana simultaneously |
| Network format | `base-sepolia` | `eip155:84532` (CAIP-2) |
| Environment variable | `PRIVATE_KEY` | `EVM_PRIVATE_KEY` |
| Scheme registration | Automatic (single) | Explicit `register_exact_evm_client()` |
| Payment response | None | `get_payment_settle_response()` support |

## Setup and Usage

1. Copy the `.env-local` file to `.env` and add your private key.

```bash
cd external/x402/examples/python/clients/httpx
cp .env-local .env
```

`.env` file contents:
```bash
EVM_PRIVATE_KEY=0xYourPrivateKey
SVM_PRIVATE_KEY=              # For Solana use (optional)
RESOURCE_SERVER_URL=http://localhost:4021
ENDPOINT_PATH=/weather
```

> **Security Warning**: Never commit your private keys. `.env` is included in `.gitignore`.

2. Install dependencies:
```bash
uv sync
```

3. Start the server (separate terminal):
```bash
# Start a FastAPI or Flask server first
cd ../../../servers/fastapi
uv sync && uv run python main.py
```

4. Run the client:
```bash
cd external/x402/examples/python/clients/httpx
uv run python main.py
```

## Code Analysis (main.py)

### 1. Initialization

```python
from eth_account import Account

from x402 import x402Client
from x402.http import x402HTTPClient
from x402.http.clients import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client
from x402.mechanisms.svm import KeypairSigner
from x402.mechanisms.svm.exact.register import register_exact_svm_client

# Create x402 client (async variant)
client = x402Client()
```

Since httpx is an async client, it uses `x402Client` (the async variant), as opposed to `x402ClientSync` used with requests.

### 2. Payment Scheme Registration

```python
# Register EVM payment scheme
if evm_private_key:
    account = Account.from_key(evm_private_key)
    register_exact_evm_client(client, EthAccountSigner(account))

# Register SVM (Solana) payment scheme (optional)
if svm_private_key:
    svm_signer = KeypairSigner.from_base58(svm_private_key)
    register_exact_svm_client(client, svm_signer)
```

Same registration pattern as the requests example. The same signers work regardless of sync/async.

### 3. Async Request and Payment

```python
# Create HTTP client helper (for payment response extraction)
http_client = x402HTTPClient(client)

async with x402HttpxClient(client) as http:
    response = await http.get(url)
    await response.aread()  # httpx-specific: explicitly read response body

    if response.is_success:  # httpx uses .is_success (requests uses .ok)
        settle_response = http_client.get_payment_settle_response(
            lambda name: response.headers.get(name)
        )
```

**httpx-specific notes:**
- Uses `async with` for async context manager
- `await response.aread()` is required to explicitly read the response body
- Uses `response.is_success` (equivalent to requests' `response.ok`)

### 4. Main Function

```python
if __name__ == "__main__":
    asyncio.run(main())
```

Uses Python's `asyncio.run()` to execute the async main function.

## Example Code Location

```
external/x402/examples/python/clients/httpx/
├── main.py           # Async httpx client example
├── .env-local        # Environment variable template
└── pyproject.toml    # Project dependencies (x402[httpx,evm,svm])
```

## Key Concepts

### x402Client vs x402ClientSync
- `x402Client` — Async client (for httpx)
- `x402ClientSync` — Sync client (for requests)
- Both classes use the same payment scheme registration API

### x402HttpxClient
- Wraps httpx `AsyncClient` with x402 payment capabilities
- Used as an `async with` context manager
- Internally: detect 402 → create payment → retry request

### x402HTTPClient
- HTTP helper class for extracting payment responses
- Use `get_payment_settle_response()` to check payment settlement results
- Sync variant: `x402HTTPClientSync`

### requests vs httpx Comparison

| Item | requests (sync) | httpx (async) |
|------|----------------|---------------|
| x402 client | `x402ClientSync` | `x402Client` |
| HTTP wrapper | `x402_requests(client)` | `x402HttpxClient(client)` |
| Context manager | `with` | `async with` |
| Response check | `response.ok` | `response.is_success` |
| Response read | Automatic | `await response.aread()` |
| Dependencies | `x402[requests,evm,svm]` | `x402[httpx,evm,svm]` |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `EVM_PRIVATE_KEY` | One of EVM or SVM | EVM wallet private key (Base Sepolia) |
| `SVM_PRIVATE_KEY` | One of EVM or SVM | Solana wallet private key (Devnet) |
| `RESOURCE_SERVER_URL` | Yes | Server URL (default: `http://localhost:4021`) |
| `ENDPOINT_PATH` | Yes | Request path (default: `/weather`) |

## Next Steps

- [requests Client Example](../requests/README.en.md) - Sync client implementation
- [FastAPI Server Example](../../servers/fastapi/README.en.md) - Build a 402-protected server
- [Flask Server Example](../../servers/flask/README.en.md) - Build a Flask-based server

---

[← Back to v2 Documentation](../../README.en.md) | [View v1 Legacy →](../../../v1/clients/httpx/README.en.md)

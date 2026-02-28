[한국어](./README.md) | [English](./README.en.md)

# x402 requests Client Example (v2)

> **v2 Documentation (Latest)**
>
> This documentation covers x402 **v2 SDK (v2.2.0+)**.
> For v1 Legacy documentation, see [v1 requests Client](../../../v1/clients/requests/README.en.md).
>
> **v2 Example Path**:
> - 📂 Local: [`external/x402/examples/python/clients/requests/`](../../../../../external/x402/examples/python/clients/requests/)
> - 🔗 Origin: [coinbase/x402/.../clients/requests/](https://github.com/coinbase/x402/tree/main/examples/python/clients/requests)
>
> **Created**: February 28, 2026
> **Last Verified**: Against `external/x402/examples/python/clients/requests/main.py`

---

This guide demonstrates how to use the x402 v2 SDK with requests to send payment requests to 402-protected endpoints.

**Web2 Analogy**: Just like adding an API key to headers when calling a paid API, x402 automatically adds payment signatures to HTTP headers to access paid endpoints. Instead of an API key, cryptocurrency payments become the authentication method.

## v1 → v2 Changes

| Item | v1 (Legacy) | v2 |
|------|------------|-----|
| Client | `x402_requests(account)` | `x402_requests(x402ClientSync())` |
| Signer | Direct `eth_account.Account` | `EthAccountSigner` wrapper |
| Multi-chain | EVM only | EVM + Solana simultaneously |
| Network format | `base-sepolia` | `eip155:84532` (CAIP-2) |
| Environment variable | `PRIVATE_KEY` | `EVM_PRIVATE_KEY` |
| Scheme registration | Automatic (single) | Explicit `register_exact_evm_client()` |
| Payment response | None | `get_payment_settle_response()` support |

## Setup and Usage

1. Copy the `.env-local` file to `.env` and add your private key.

```bash
cd external/x402/examples/python/clients/requests
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
cd external/x402/examples/python/clients/requests
uv run python main.py
```

## Code Analysis (main.py)

### 1. Initialization

```python
from eth_account import Account

from x402 import x402ClientSync
from x402.http import x402HTTPClientSync
from x402.http.clients import x402_requests
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client
from x402.mechanisms.svm import KeypairSigner
from x402.mechanisms.svm.exact.register import register_exact_svm_client

# Create x402 client (sync variant)
client = x402ClientSync()
```

In v2, you first create an `x402ClientSync` then register payment schemes — a modular architecture.

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

Unlike v1, you can register multiple chain payment schemes on a single client.

### 3. Request and Payment

```python
# Create HTTP client helper (for payment response extraction)
http_client = x402HTTPClientSync(client)

# Create session with context manager
with x402_requests(client) as session:
    response = session.get(url)

    # Extract payment response
    if response.ok:
        settle_response = http_client.get_payment_settle_response(
            lambda name: response.headers.get(name)
        )
```

`x402_requests` automatically detects 402 responses and handles payments.

## Example Code Location

```
external/x402/examples/python/clients/requests/
├── main.py           # Sync requests client example
├── .env-local        # Environment variable template
└── pyproject.toml    # Project dependencies (x402[requests,evm,svm])
```

## Key Concepts

### x402ClientSync
- Core synchronous client class in v2
- Register payment schemes like plugins
- Async variant: `x402Client` (used with httpx)

### EthAccountSigner
- Signer wrapper around `eth_account.Account`
- Generates payment signatures for EVM chains (Base, Ethereum, etc.)
- v1 passed Account directly; v2 uses an abstracted signer interface

### register_exact_evm_client
- Registers the "exact" payment scheme on the client
- Pays the exact amount specified (extensible to streaming and other schemes)
- Solana variant: `register_exact_svm_client`

### x402_requests
- Wraps a requests session with x402 payment capabilities
- Used as a context manager (`with` statement)
- Internally: detect 402 → create payment → retry request

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `EVM_PRIVATE_KEY` | One of EVM or SVM | EVM wallet private key (Base Sepolia) |
| `SVM_PRIVATE_KEY` | One of EVM or SVM | Solana wallet private key (Devnet) |
| `RESOURCE_SERVER_URL` | Yes | Server URL (default: `http://localhost:4021`) |
| `ENDPOINT_PATH` | Yes | Request path (default: `/weather`) |

## Next Steps

- [httpx Client Example](../httpx/README.en.md) - Async client implementation
- [FastAPI Server Example](../../servers/fastapi/README.en.md) - Build a 402-protected server
- [Flask Server Example](../../servers/flask/README.en.md) - Build a Flask-based server

---

[← Back to v2 Documentation](../../README.en.md) | [View v1 Legacy →](../../../v1/clients/requests/README.en.md)

[한국어](./README.md) | [English](./README.en.md)

# x402 Python v2 Documentation

> Documentation for **x402 v2 SDK**.
> v2 was released on December 11, 2025.
>
> 📚 **Migrating from v1**: [Migration Guide](https://docs.cdp.coinbase.com/x402/migration-guide)

---

## v2 Specification Document

- [x402-v2-specification.md](../../x402-v2-specification.md) - Complete v2 protocol specification

---

## Python v2 Example Guides

### Client Examples

| Example | Local Code | Origin Repo | Guide |
|---------|----------|----------|-------|
| **requests** (sync) | [→ Local](../../../external/x402/examples/python/clients/requests/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/clients/requests) | [→ Guide](./clients/requests/README.en.md) |
| **httpx** (async) | [→ Local](../../../external/x402/examples/python/clients/httpx/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/clients/httpx) | [→ Guide](./clients/httpx/README.en.md) |

### Server Examples

| Example | Local Code | Origin Repo | Guide |
|---------|----------|----------|-------|
| **FastAPI** (async) | [→ Local](../../../external/x402/examples/python/servers/fastapi/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/servers/fastapi) | [→ Guide](./servers/fastapi/README.en.md) |
| **Flask** (sync) | [→ Local](../../../external/x402/examples/python/servers/flask/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/servers/flask) | [→ Guide](./servers/flask/README.en.md) |

### Additional Examples (Documentation Coming Soon)

| Example | Local Code | Origin Repo | Guide |
|---------|----------|----------|-------|
| **Facilitator** | [→ Local](../../../external/x402/examples/python/facilitator/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/facilitator) | Coming soon |
| **MCP** (AI agents) | — | Coming soon | Coming soon |
| **Extensions** | — | Coming soon | Coming soon |

---

## Learning Path

### Beginners (New to x402)

1. [requests Client](./clients/requests/README.en.md) — Start with sync HTTP client
2. [FastAPI Server](./servers/fastapi/README.en.md) — Build a paid API server

### Async Developers

1. [httpx Client](./clients/httpx/README.en.md) — async/await pattern
2. [FastAPI Server](./servers/fastapi/README.en.md) — ASGI-based server

### Flask Users

1. [requests Client](./clients/requests/README.en.md) — Sync client
2. [Flask Server](./servers/flask/README.en.md) — WSGI-based server

---

## v2 New Features

1. **Multi-chain Support** - Base, Solana, EVM-compatible chains (CAIP standard)
2. **Multi-Transport** - HTTP, MCP (AI agents), A2A (agent-to-agent)
3. **Enhanced Security** - ERC1271, ERC6492 support
4. **Session Management** - Wallet-based reusable access
5. **Plugin Architecture** - Independent chain/payment method extensions
6. **Dynamic Routing** - Per-request `payTo` recipient specification
7. **Automatic API Discovery** - Bazaar/Discovery API

---

## TypeScript Examples

| Example | Local Code | Origin Repo |
|---------|----------|----------|
| Clients | [→ Local](../../../external/x402/examples/typescript/clients/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/) |
| Servers | [→ Local](../../../external/x402/examples/typescript/servers/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/) |
| Facilitator | [→ Local](../../../external/x402/examples/typescript/facilitator/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/facilitator/) |

---

[← Back to Python Documentation](../README.en.md) | [View v1 Legacy →](../v1/README.en.md)

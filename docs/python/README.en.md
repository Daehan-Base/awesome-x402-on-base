[한국어](./README.md) | [English](./README.en.md)

# x402 Python Documentation

> Guide for implementing x402 payment protocol on Base chain with Python

---

## Documentation by Version

### v2 (Latest)

> Released December 2025, modular SDK based

- [v2/](v2/) - Python v2 Documentation
  - [requests Client](v2/clients/requests/README.en.md) - Sync HTTP client
  - [httpx Client](v2/clients/httpx/README.en.md) - Async HTTP client
  - [FastAPI Server](v2/servers/fastapi/README.en.md) - ASGI server
  - [Flask Server](v2/servers/flask/README.en.md) - WSGI server

### v1 (Legacy)

> Single `x402` package based

- [v1/](v1/) - Python v1 Legacy Documentation (clients/, servers/, discovery/)

---

## v1 vs v2 Key Differences

| Item | v1 (Legacy) | v2 |
|------|------------|-----|
| HTTP Header | `X-PAYMENT` | `PAYMENT-SIGNATURE` |
| Network Format | `base-sepolia` | `eip155:84532` (CAIP Standard) |
| Version Field | `x402Version: 1` | `x402Version: 2` |
| Example Path | `examples/python/legacy/` | `examples/python/clients/`, `servers/` |

---

[← Back to Documentation Home](../README.en.md)

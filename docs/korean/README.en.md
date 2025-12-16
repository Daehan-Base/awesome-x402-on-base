[한국어](./README.md) | [English](./README.en.md)

# x402 Korean Documentation

> Korean guide for using the x402 payment protocol on Base chain

---

## Getting Started

- [getting_started.ko.md](getting_started.ko.md) - Environment setup and getting started guide

---

## Documentation by Version

### v2 (Latest)

> Released on December 11, 2025

- [x402-v2-specification.ko.md](x402-v2-specification.ko.md) - **Complete v2 Protocol Specification**
- [v2/](v2/) - v2 related documentation

### v1 (Legacy)

> Python SDK-based example documentation

- [v1/](v1/) - v1 Legacy documentation
  - [python-requests-client.ko.md](v1/examples/python-requests-client.ko.md)
  - [python-httpx-client.ko.md](v1/examples/python-httpx-client.ko.md)
  - [python-fastapi-server.ko.md](v1/examples/python-fastapi-server.ko.md)
  - [python-discovery.ko.md](v1/examples/python-discovery.ko.md)

---

## Quick Comparison: v1 vs v2

| Item | v1 (Legacy) | v2 (Latest) |
|------|------------|-----------|
| HTTP Headers | `X-PAYMENT` | `PAYMENT-SIGNATURE`, `PAYMENT-REQUIRED` |
| Network Format | `base-sepolia` | `eip155:84532` (CAIP Standard) |
| Transport | HTTP only | HTTP, MCP, A2A |
| Chain Support | Single EVM | Multi-chain EVM + Solana |

---

[← Back to Main README](../../README.md)

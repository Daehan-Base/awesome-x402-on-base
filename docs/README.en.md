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
- [python/v2/](python/v2/) - Python v2 related documentation

### v1 (Legacy)

> Python SDK-based example documentation

- [python/v1/](python/v1/) - Python v1 Legacy documentation
  - [requests-client.ko.md](python/v1/examples/requests-client.ko.md)
  - [httpx-client.ko.md](python/v1/examples/httpx-client.ko.md)
  - [fastapi-server.ko.md](python/v1/examples/fastapi-server.ko.md)
  - [discovery.ko.md](python/v1/examples/discovery.ko.md)

---

## TypeScript Example Documentation

### v2 (Latest)

> Modular `@x402/*` packages based

- [typescript/v2/](typescript/v2/) - TypeScript v2 Example Documentation
  - [clients/](typescript/v2/clients/) - Client Examples (axios, fetch, custom, advanced, mcp)
  - [servers/](typescript/v2/servers/) - Server Examples (express, hono, advanced, custom)
  - [facilitator/](typescript/v2/facilitator/) - Facilitator Examples
  - [fullstack/](typescript/v2/fullstack/) - Fullstack Examples (next, miniapp)

### v1 (Legacy)

- [typescript/v1/](typescript/v1/) - TypeScript v1 Legacy Documentation (Coming Soon)

---

## Quick Comparison: v1 vs v2

| Item | v1 (Legacy) | v2 (Latest) |
|------|------------|-----------|
| HTTP Headers | `X-PAYMENT` | `PAYMENT-SIGNATURE`, `PAYMENT-REQUIRED` |
| Network Format | `base-sepolia` | `eip155:84532` (CAIP Standard) |
| Transport | HTTP only | HTTP, MCP, A2A |
| Chain Support | Single EVM | Multi-chain EVM + Solana |

---

[← Back to Main README](../README.md)

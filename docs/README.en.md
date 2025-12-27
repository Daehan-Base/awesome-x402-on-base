[한국어](./README.md) | [English](./README.en.md)

# x402 Korean Documentation

> Korean guide for using the x402 payment protocol on Base chain

---

## Getting Started

- [getting_started.md](getting_started.md) - Environment setup and getting started guide

---

## Documentation by Version

### v2 (Latest)

> Released on December 11, 2025

- [x402-v2-specification.md](x402-v2-specification.md) - **Complete v2 Protocol Specification**
- [python/v2/](python/v2/) - Python v2 related documentation

### v1 (Legacy)

> Python SDK-based example documentation

- [python/v1/](python/v1/) - Python v1 Legacy documentation
  - [requests Client](python/v1/clients/requests/README.md)
  - [httpx Client](python/v1/clients/httpx/README.md)
  - [FastAPI Server](python/v1/servers/fastapi/README.md)
  - [Discovery](python/v1/discovery/README.md)

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

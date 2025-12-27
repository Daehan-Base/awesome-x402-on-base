[한국어](./README.md) | [English](./README.en.md)

# x402 TypeScript Documentation

> Guide for implementing x402 payment protocol with TypeScript on Base chain

---

## Documentation by Version

### v2 (Latest)

> Released December 11, 2025, modular `@x402/*` packages

- [v2/](v2/) - TypeScript v2 Example Documentation
  - [clients/](v2/clients/) - Client Examples (axios, fetch, custom, advanced, mcp)
  - [servers/](v2/servers/) - Server Examples (express, hono, advanced, custom)
  - [facilitator/](v2/facilitator/) - Facilitator Examples
  - [fullstack/](v2/fullstack/) - Fullstack Examples (next, miniapp)

### v1 (Legacy)

> Single `x402` package based

- [v1/](v1/) - TypeScript v1 Legacy Documentation (Coming Soon)

---

## Key Differences: v1 vs v2

| Item | v1 (Legacy) | v2 |
|------|------------|-----|
| HTTP Header | `X-PAYMENT` | `PAYMENT-SIGNATURE` |
| Network Format | `base-sepolia` | `eip155:84532` (CAIP standard) |
| Version Field | `x402Version: 1` | `x402Version: 2` |
| SDK Structure | Single `x402` package | Modular `@x402/*` packages |
| Chain Support | EVM only | EVM + Solana multi-chain |

---

[← Back to Documentation Home](../README.md)

[한국어](./README.md) | [English](./README.en.md)

# x402 Python Documentation

> Guide for implementing x402 payment protocol on Base chain with Python

---

## Documentation by Version

### v2 (Latest)

> Released December 2025, modular SDK based

- [v2/](v2/) - Python v2 Documentation (Coming Soon)

### v1 (Legacy)

> Single `x402` package based

- [v1/](v1/) - Python v1 Legacy Documentation
  - [examples/](v1/examples/) - Example Guides (requests, httpx, fastapi, discovery)

---

## v1 vs v2 Key Differences

| Item | v1 (Legacy) | v2 |
|------|------------|-----|
| HTTP Header | `X-PAYMENT` | `PAYMENT-SIGNATURE` |
| Network Format | `base-sepolia` | `eip155:84532` (CAIP Standard) |
| Version Field | `x402Version: 1` | `x402Version: 2` |
| Example Path | `examples/python/legacy/` | (Coming Soon) |

---

[← Back to Documentation Home](../README.md)

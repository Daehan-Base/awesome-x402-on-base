[한국어](./README.md) | [English](./README.en.md)

# x402 v1 (Legacy) Korean Documentation

> This is legacy documentation covering **x402 v1 SDK**.
> For the latest v2 specification, see [x402-v2-specification.md](../../x402-v2-specification.md).
>
> 📚 **v1 → v2 Migration**: [Migration Guide](https://docs.cdp.coinbase.com/x402/migration-guide)

---

## Python Example Documentation

| Document | Description | Local Code | Origin Repo |
|------|------|----------|----------|
| [requests Client](clients/requests/README.md) | Synchronous HTTP client | [→ Local](../../../external/x402/examples/python/legacy/clients/requests/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/requests) |
| [httpx Client](clients/httpx/README.md) | Asynchronous HTTP client | [→ Local](../../../external/x402/examples/python/legacy/clients/httpx/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/httpx) |
| [FastAPI Server](servers/fastapi/README.md) | FastAPI server | [→ Local](../../../external/x402/examples/python/legacy/servers/fastapi/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/legacy/servers/fastapi) |
| [Discovery](discovery/README.md) | Resource discovery | [→ Local](../../../external/x402/examples/python/legacy/discovery/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/legacy/discovery) |

---

## Key Differences: v1 vs v2

| Item | v1 (Legacy) | v2 |
|------|------------|-----|
| HTTP Headers | `X-PAYMENT` | `PAYMENT-SIGNATURE` |
| Network Format | `base-sepolia` | `eip155:84532` (CAIP Standard) |
| Version Field | `x402Version: 1` | `x402Version: 2` |
| SDK Structure | Single `x402` package | Modular `@x402/*` packages |

---

## Learning Path

```
Step 1: ../../getting_started.md (Environment setup)
    ↓
Step 2: clients/requests/README.md (Synchronous client)
    ↓
Step 3: clients/httpx/README.md (Asynchronous client)
    ↓
Step 4: servers/fastapi/README.md (Server implementation)
    ↓
Step 5: discovery/README.md (Advanced features)
```

---

[← Back to Korean Documentation](../../README.md) | [View v2 Spec →](../../x402-v2-specification.md)

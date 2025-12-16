[한국어](./README.md) | [English](./README.en.md)

# x402 v1 (Legacy) Korean Documentation

> This is legacy documentation covering **x402 v1 SDK**.
> For the latest v2 specification, see [x402-v2-specification.ko.md](../x402-v2-specification.ko.md).
>
> 📚 **v1 → v2 Migration**: [Migration Guide](https://docs.cdp.coinbase.com/x402/migration-guide)

---

## Python Example Documentation

| Document | Description | Official Example Path |
|------|------|----------------|
| [python-requests-client.ko.md](examples/python-requests-client.ko.md) | Synchronous HTTP client | `external/x402/examples/python/legacy/clients/requests` |
| [python-httpx-client.ko.md](examples/python-httpx-client.ko.md) | Asynchronous HTTP client | `external/x402/examples/python/legacy/clients/httpx` |
| [python-fastapi-server.ko.md](examples/python-fastapi-server.ko.md) | FastAPI server | `external/x402/examples/python/legacy/servers/fastapi` |
| [python-discovery.ko.md](examples/python-discovery.ko.md) | Resource discovery | `external/x402/examples/python/legacy/discovery` |

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
Step 1: ../getting_started.ko.md (Environment setup)
    ↓
Step 2: python-requests-client.ko.md (Synchronous client)
    ↓
Step 3: python-httpx-client.ko.md (Asynchronous client)
    ↓
Step 4: python-fastapi-server.ko.md (Server implementation)
    ↓
Step 5: python-discovery.ko.md (Advanced features)
```

---

[← Back to Korean Documentation](../README.md) | [View v2 Spec →](../x402-v2-specification.ko.md)

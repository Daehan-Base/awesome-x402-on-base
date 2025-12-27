[한국어](./README.md) | [English](./README.en.md)

# x402 v2 Korean Documentation

> Documentation for **x402 v2 SDK**.
> v2 was released on December 11, 2025.
>
> 📚 **Migrating from v1**: [Migration Guide](https://docs.cdp.coinbase.com/x402/migration-guide)

---

## v2 Specification Document

- [x402-v2-specification.md](../../x402-v2-specification.md) - Complete v2 protocol specification

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

## v2 Examples (In Progress)

> 🚧 **Python v2 SDK In Progress**: [PR #841](https://github.com/coinbase/x402/pull/841)
>
> TypeScript examples:
> - 📂 Local: [`external/x402/examples/typescript/`](../../../external/x402/examples/typescript/)
> - 🔗 Origin: [coinbase/x402/.../examples/typescript/](https://github.com/coinbase/x402/tree/main/examples/typescript)

### TypeScript Examples

| Example | Local Code | Origin Repo |
|---------|----------|----------|
| Clients | [→ Local](../../../external/x402/examples/typescript/clients/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/) |
| Servers | [→ Local](../../../external/x402/examples/typescript/servers/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/) |
| Facilitator | [→ Local](../../../external/x402/examples/typescript/facilitator/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/facilitator/) |

---

[← Back to Korean Documentation](../README.md) | [View v1 Legacy →](../v1/README.md)

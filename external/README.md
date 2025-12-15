# External Resources

## 📝 TL;DR

**What**: Git submodule linking to official [coinbase/x402](https://github.com/coinbase/x402) repository  
**Why**: Avoid code duplication, always reference latest official examples  
**Usage**: Read-only - use Korean guides in `docs/korean/` to follow along  
**Update**: `git submodule update --remote external/x402`  

---

This directory contains Git submodules for external repositories.

## x402 Official Repository

**Submodule**: `external/x402/`
**Source**: https://github.com/coinbase/x402

### What's Included

The official x402 repository includes:
- Python SDK implementation
- Python examples (clients, servers, discovery)
- TypeScript examples
- Go implementation
- Java implementation
- Protocol specifications

### Accessing Examples

⚠️ **Note**: The submodule needs to be initialized first:
```bash
git submodule update --init --recursive
```

Then navigate to Python examples:
```bash
cd external/x402/examples/python/legacy

# Available examples:
# - clients/requests/  - Python requests client example
# - clients/httpx/     - Python httpx client example
# - servers/           - Python server examples
# - discovery/         - x402 discovery example
```

### Korean Guides

For each official example, we provide Korean documentation:

| Example | Code | Korean Guide |
|---------|------|--------------|
| requests Client | `./x402/examples/python/legacy/clients/requests` | [→ Guide](../docs/korean/examples/python-requests-client.ko.md) |
| httpx Client | `./x402/examples/python/legacy/clients/httpx` | [→ Guide](../docs/korean/examples/python-httpx-client.ko.md) |
| Python Servers | `./x402/examples/python/legacy/servers` | [→ Guide](../docs/korean/examples/python-fastapi-server.ko.md) |
| Discovery | `./x402/examples/python/legacy/discovery` | [→ Guide](../docs/korean/examples/python-discovery.ko.md) |

### Updating the Submodule

To get the latest changes from the official repository:

```bash
git submodule update --remote external/x402
```

### Important Note

⚠️ **Do not modify files in this directory directly**. This is a read-only reference to the official repository. Any modifications should be made in the `examples/` directory at the root level.

---

[← Back to main README](../README.md)

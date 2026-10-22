[한국어](./README.md) | [English](./README.en.md)

# Awesome x402 on Base 🚀

> A curated collection of resources, tools, and knowledge for using the x402 protocol on Base chain - Maintained by Base Korea Developer Ambassador.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Base Chain](https://img.shields.io/badge/Chain-Base-blue.svg)](https://base.org)
[![x402 Protocol](https://img.shields.io/badge/Protocol-x402-green.svg)](https://www.x402.org)

## 📝 TL;DR

**What**: Korean guide for x402 payment protocol on Base chain
**Why**: Official examples already use Base - adding detailed Korean tutorials
**How**: Link official code (`external/`) via Git submodule + Korean guides (`docs/`)
**Target**: Korean developers & global builders interested in Base-specific x402 implementations

**Quick Start**: [Official Documentation](https://docs.cdp.coinbase.com/x402/welcome) | [Korean Guide](./docs/getting_started.md)

---

## 📖 About This Repository

This repository provides **Korean guides and documentation** for using the **x402 protocol** on Base chain. Since official x402 examples already use Base chain by default, we focus on providing detailed Korean tutorials for each example and community resources.

**What's Included:**
- 🔗 **Official Examples** (Git submodule in `external/`) - Direct access to Coinbase's x402 examples
- 📝 **Korean Guides** (`docs/`) - Step-by-step Korean tutorials for each example
- 🔵 **Base-Specific Content** (`examples/`) - Base chain optimizations and use cases
- 🇰🇷 **Korean Community** - Resources for Korean developers

> **Note**: This repository complements the [official x402 repository](https://github.com/coinbase/x402) by providing Korean documentation and Base-centric content.

## 🔍 What is x402?

**x402** is an open-source payment protocol developed by Coinbase that revolutionizes internet-native payments by modernizing the HTTP 402 status code that has been unused for 26 years.

### Key Features

- ⚡ **Fast Speed** - Payment processing in ~2 seconds
- 💰 **Ultra-Low Cost** - Transaction fees < $0.0001, minimum $0.001 payments possible
- 🤖 **Machine-to-Machine Payments** - Autonomous resource payments for AI agents and IoT devices
- 🔗 **Chain Agnostic** - Supports Base, Solana, Polygon, Ethereum, and more
- 🌐 **HTTP Native** - Built on top of HTTP for seamless web integration

### How It Works

x402 leverages the HTTP 402 "Payment Required" status code to create a standardized payment layer for the internet. When a service requires payment, it returns a 402 response with payment instructions. Clients (including AI agents) can automatically handle payments using stablecoins like USDC without accounts, sessions, or complex authentication.

## 🎯 Why Base Chain?

**Base** is the optimal network for x402 protocol adoption:

- 🚀 **High Performance** - Fast finality and low latency
- 💵 **Minimal Fees** - Gas fees for x402 transactions < $0.0001
- 🔐 **Ethereum Security** - Strong security of L2 built on Ethereum
- 🌊 **Native Support** - First-class support for Base Sepolia and Base Mainnet
- 💎 **USDC Integration** - Native USDC as the default payment currency

Base provides the perfect infrastructure to enable x402's micropayments and AI agent transactions at scale.

## 🌟 x402 Ecosystem

The x402 ecosystem is rapidly growing with support from major tech companies:

- **Coinbase** - Protocol creator and primary maintainer
- **Cloudflare** - x402 Foundation co-founder
- **Google** - Infrastructure integration
- **Visa** - Payment network partnership
- **AWS** - Cloud infrastructure support
- **Circle** - USDC stablecoin provider
- **Anthropic** - AI integration
- **base-oracle** - Trading-intelligence API on Base mainnet: 6 computed x402-paid endpoints (wallet report, token-safety risk flags, cross-DEX arb scan, momentum signals, Hyperliquid funding/OI, portfolio composition). $0.05 USDC per call, verified directly on-chain — no facilitator, no API keys. ([live](https://arturo-epiphytical-torrie.ngrok-free.dev) | [openapi](https://arturo-epiphytical-torrie.ngrok-free.dev/openapi.json))



## 📁 Repository Structure

```
awesome-x402-on-base/
├── external/x402/              # 🔗 Git Submodule (Official x402 repository, read-only)
│
├── examples/                   # 📝 Base-specific examples and demos
│   └── python/                 # Python examples
│       ├── v1/                 # v1 Legacy SDK examples
│       └── v2/                 # v2 SDK examples
│
├── docs/                       # 🇰🇷 Korean documentation
│   ├── getting_started.md   # Getting started guide
│   ├── x402-v2-specification.md  # v2 protocol specification
│   ├── python/                 # Python documentation
│   │   ├── v1/                 # v1 Legacy docs
│   │   │   ├── clients/        # Clients (requests, httpx)
│   │   │   ├── servers/        # Servers (FastAPI)
│   │   │   └── discovery/      # Discovery
│   │   └── v2/                 # v2 documentation (clients/, servers/)
│   └── typescript/             # TypeScript documentation
│       ├── v1/                 # v1 Legacy docs (coming soon)
│       └── v2/                 # v2 example guides
│
├── ROADMAP.md                  # 🗺️ Development roadmap
└── LICENSE                     # 📄 MIT License
```

**Clear Separation:**
- **`external/`** = Official x402 examples (submodule, do not modify)
- **`examples/`** = Base-specific x402 examples
- **`docs/`** = Korean guides and tutorials (language → version structure)

## 🚀 Quick Start

### For English Speakers
→ Start with the [Official x402 Documentation](https://docs.cdp.coinbase.com/x402/welcome)

### For Korean Developers 🇰🇷
→ Start with the [Korean Quick Start Guide](./docs/getting_started.md)

## 💡 Examples & Korean Guides

### Python v2 Examples (Latest)

| Example | Local Code | Origin Repo | Guide |
|---------|----------|----------|-------|
| **requests client** (sync) | [→ Local](./external/x402/examples/python/clients/requests/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/clients/requests) | [→ Guide](./docs/python/v2/clients/requests/README.en.md) |
| **httpx client** (async) | [→ Local](./external/x402/examples/python/clients/httpx/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/clients/httpx) | [→ Guide](./docs/python/v2/clients/httpx/README.en.md) |
| **FastAPI server** (async) | [→ Local](./external/x402/examples/python/servers/fastapi/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/servers/fastapi) | [→ Guide](./docs/python/v2/servers/fastapi/README.en.md) |
| **Flask server** (sync) | [→ Local](./external/x402/examples/python/servers/flask/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/servers/flask) | [→ Guide](./docs/python/v2/servers/flask/README.en.md) |

### Python v1 Examples (Legacy)

| Example | Local Code | Origin Repo | Guide |
|---------|----------|----------|-------|
| **requests client** | [→ Local](./external/x402/examples/python/legacy/clients/requests/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/requests) | [→ Guide](./docs/python/v1/clients/requests/README.en.md) |
| **httpx client** | [→ Local](./external/x402/examples/python/legacy/clients/httpx/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/httpx) | [→ Guide](./docs/python/v1/clients/httpx/README.en.md) |
| **FastAPI server** | [→ Local](./external/x402/examples/python/legacy/servers/fastapi/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/legacy/servers/fastapi) | [→ Guide](./docs/python/v1/servers/fastapi/README.en.md) |
| **Discovery** | [→ Local](./external/x402/examples/python/legacy/discovery/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/legacy/discovery) | [→ Guide](./docs/python/v1/discovery/README.en.md) |

### TypeScript Examples (v2 Latest)

| Example | Local Code | Origin Repo | Korean Guide |
|---------|----------|----------|--------------|
| **Axios Client** | [→ Local](./external/x402/examples/typescript/clients/axios/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/axios) | [→ Guide](./docs/typescript/v2/clients/axios/) |
| **Fetch Client** | [→ Local](./external/x402/examples/typescript/clients/fetch/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/fetch) | [→ Guide](./docs/typescript/v2/clients/fetch/) |
| **Express Server** | [→ Local](./external/x402/examples/typescript/servers/express/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/express) | [→ Guide](./docs/typescript/v2/servers/express/) |
| **Hono Server** | [→ Local](./external/x402/examples/typescript/servers/hono/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/hono) | [→ Guide](./docs/typescript/v2/servers/hono/) |
| **Next.js Fullstack** | [→ Local](./external/x402/examples/typescript/fullstack/next/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/fullstack/next) | [→ Guide](./docs/typescript/v2/fullstack/next/) |
| **Farcaster Mini App** | [→ Local](./external/x402/examples/typescript/fullstack/miniapp/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/fullstack/miniapp) | [→ Guide](./docs/typescript/v2/fullstack/miniapp/) |
| **MCP Client** | [→ Local](./external/x402/examples/typescript/clients/mcp/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/mcp) | [→ Guide](./docs/typescript/v2/clients/mcp/) |

### Using the Submodule

⚠️ **Important**: `external/x402` is a Git submodule. Initialization is required.

Initial setup:
```bash
# Clone this repository with submodule
git clone --recursive https://github.com/Daehan-Base/awesome-x402-on-base.git

# Or if already cloned
git submodule update --init --recursive
```

Access official examples:
```bash
# First, verify submodule initialization
ls external/x402/examples/python  # If empty, run the commands above

cd external/x402/examples/python
# Follow Korean guides in docs/python/v1/
```

## 🗺️ Roadmap

For detailed development plans, see [ROADMAP.md](./ROADMAP.md).

## 🤝 Contributing

Contributions are welcome! For detailed guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md).

### How to Contribute

- 📝 **Documentation** - Write Korean tutorials and guides
- 💻 **Example Code** - Add Base-specific examples
- 🐛 **Bug Reports** - Submit issues
- 💡 **Feature Requests** - Share new ideas

[View Contributing Guide →](./CONTRIBUTING.md)

## 📚 Resources

### Official x402 Resources
- 📖 [Official Documentation](https://docs.cdp.coinbase.com/x402/welcome)
- 💻 x402 GitHub: [📂 Local](./external/x402/) | [🔗 Origin](https://github.com/coinbase/x402)
- 📄 [x402 Whitepaper](https://www.x402.org/x402-whitepaper.pdf)
- 🌐 [x402 Website](https://www.x402.org)

### x402 SDKs & Examples

| SDK/Example | Local Code | Origin Repo |
|-------------|----------|----------|
| Python SDK | [→ Local](./external/x402/python/x402/) | [→ Origin](https://github.com/coinbase/x402/tree/main/python/x402) |
| Python v2 Examples | [→ Local](./external/x402/examples/python/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python) |
| Python v1 Examples | [→ Local](./external/x402/examples/python/legacy/) | [→ Origin](https://github.com/coinbase/x402/tree/main/examples/python/legacy) |
| TypeScript SDK | [→ Local](./external/x402/typescript/) | [→ Origin](https://github.com/coinbase/x402/tree/main/typescript) |
| Go Implementation | [→ Local](./external/x402/go/) | [→ Origin](https://github.com/coinbase/x402/tree/main/go) |

### Base Chain Resources
- [Base Official Website](https://base.org)
- [Base Documentation](https://docs.base.org)
- [Base Sepolia Faucet](https://faucet.quicknode.com/base/sepolia)
- [Circle USDC Faucet](https://faucet.circle.com/)

## 📬 Contact

- **Issues & Questions** - Open an issue in this repository
- **Discussions** - Share opinions in GitHub Discussions

## 📄 License

This repository is licensed under the [MIT License](LICENSE).

---

**Maintained with care by Logan (Base Korea Developer Ambassador)**

*Building the future of internet-native payments, one commit at a time.*

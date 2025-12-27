# Coding Guidelines for AI Coding Agents

This file provides guidance to AI coding agents when working with code in this repository.


## Project Overview

Read `README.md` for overall architecture and purpose of this project.

Consult component READMEs for detailed information:
- `docs/README.md` - Korean documentation structure
- `docs/python/v1/README.md` - Python v1 Legacy examples guide
- `examples/README.md` - Base-specific examples


## Directory Structure

```
awesome-x402-on-base/
├── external/x402/       # Git submodule - official x402 repository (READ-ONLY)
├── examples/            # Base chain-specific examples
│   └── python/          # Python examples
│       ├── v1/          # v1 Legacy SDK examples (ap2-demo-coffee-shop)
│       └── v2/          # v2 SDK examples (in progress)
├── docs/                # Korean documentation
│   └── python/          # Python documentation
│       ├── v1/          # v1 Legacy docs (clients/, servers/, discovery/)
│       └── v2/          # v2 documentation (in progress)
├── README.md            # Project introduction
├── ROADMAP.md           # Development roadmap
└── CLAUDE.md            # This file
```

### Directory Descriptions

**`external/x402/`** - Official x402 repository (READ-ONLY)
- Git submodule linking to [coinbase/x402](https://github.com/coinbase/x402)
- Contains official SDKs (Python, TypeScript, Go, Java) and examples
- Never modify directly; update via `git submodule update --remote`

**`examples/`** - Base chain-specific examples
- `python/v1/`: Python examples using x402 v1 Legacy SDK (e.g., ap2-demo-coffee-shop)
- `python/v2/`: Python examples using x402 v2 SDK (in progress)
- Community contributions welcome

**`docs/`** - Korean documentation for x402 on Base
- `getting_started.md`: Environment setup guide
- `x402-v2-specification.md`: v2 protocol specification
- `python/v1/`: v1 Legacy tutorials (clients/, servers/, discovery/)
- `python/v2/`: Python v2 documentation (in progress)


## README-First Development

**Always read the component README before making changes.**

Update README when:
- Adding new documentation or examples
- Changing directory structure
- Adding new v1/v2 content


## General

### Critical Security Rules (MUST READ)

**NEVER do the following:**

1. **Commit Private Keys or `.env` files**
   - `.env` files are gitignored - never commit them
   - Never hardcode Private Keys in source code
   - Never output Private Keys to console: `print(private_key)`, `console.log(privateKey)`
   - Never share Private Keys in public channels (Slack, Discord, etc.)
   - Never expose Private Keys in screenshots or screen sharing

2. **Modify `external/x402/` directory**
   - This is a read-only Git submodule
   - All customizations go in root `examples/` or `docs/`

3. **Use mainnet keys for development**
   - Always use Base Sepolia (testnet) for development
   - Keep development wallets separate from production wallets
   - Mainnet Private Keys are for production deployment only

**Required security practices:**
- Store secrets in `.env` file (gitignored)
- Use password managers (1Password, Bitwarden) for key storage
- Separate development wallet (small amounts only) from asset wallet
- Always develop on Base Sepolia testnet

**Emergency response for key exposure:**
1. Create new wallet immediately
2. Transfer remaining assets to new wallet
3. Stop using compromised wallet permanently
4. Rotate all related API keys

**Environment variables (`.env`):**
```bash
# CDP Platform
CDP_API_KEY_ID=
CDP_API_KEY_SECRET=
CDP_WALLET_SECRET=

# Development wallet (Base Sepolia only)
PRIVATE_KEY=

# Network
NETWORK=base-sepolia
```

**Security patterns in `.gitignore`:**
```gitignore
.env
.env.local
.env.*.local
*.pem
*.key
credentials.json
secrets.json
```

### Code Quality

- Follow existing patterns in the codebase
- Keep Korean documentation consistent with official x402 examples
- Use Web2 analogies when explaining Web3 concepts
- Include timestamps in Korean docs (작성 시점, 최종 검증)
- Always include security warnings in documentation

### Python Specifics

- **Version**: Python 3.10+
- **Package Manager**: `uv` (recommended)
- **Type Hints**: Use type annotations
- **Async**: Use `async/await` with FastAPI/httpx
- **Environment**: Load config from `.env` files, never hardcode

### TypeScript Specifics

- **Node.js**: ≥18.0.0
- **Package Manager**: `pnpm` (≥10.7.0, required)
- **Mode**: ESM (ECMAScript Modules)
- **Strict Mode**: Enable TypeScript strict mode


## Development Commands

### Project Setup

```bash
# Clone with submodule
git clone --recursive https://github.com/Daehan-Base/awesome-x402-on-base.git

# Or initialize submodule after clone
git submodule update --init --recursive
```

### Git Submodule Management

```bash
# Update to latest official x402
git submodule update --remote external/x402
```

### Running Python Examples

```bash
cd external/x402/examples/python/legacy/clients/requests
cp .env-local .env
# Edit .env to add PRIVATE_KEY
uv sync && uv run python main.py
```

### Test Token Faucets

- **ETH (gas)**: https://faucet.quicknode.com/base/sepolia
- **USDC**: https://faucet.circle.com/


## Quick Reference

**Forbidden:**
- ❌ Modify `external/x402/`
- ❌ Commit Private Keys or `.env`
- ❌ Use mainnet keys for development
- ❌ Hardcode secrets in source code
- ❌ Output Private Keys to console

**Required:**
- ✅ Use Base Sepolia for development
- ✅ Store secrets in `.env` (gitignored)
- ✅ Read component README before changes
- ✅ Follow existing patterns
- ✅ Separate dev/prod wallets

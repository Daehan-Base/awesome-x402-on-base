[한국어](./README.md) | [English](./README.en.md)

# {{Title}}

<!-- Include the block below for v1 Legacy -->
<!--
> ⚠️ **Legacy Documentation (v1)**
>
> This document covers the x402 **v1 SDK**.
> For the latest v2 specification, see [x402-v2-specification.md]({{v2SpecPath}}).
>
> **Example paths**:
> - 📂 Local: [`{{localPath}}`]({{localRelativePath}})
> - 🔗 Original: [{{repoPath}}]({{githubUrl}})
-->

> **Created**: {{YYYY-MM-DD}}

## Overview

{{Write a brief description}}

## Code Location

| Type | Path |
|------|------|
| 📂 Local | [`{{localPath}}`]({{localRelativePath}}) |
| 🔗 Original | [{{repoPath}}]({{githubUrl}}) |

## Prerequisites

- Python 3.10+ / Node.js 18+
- uv / pnpm
- Base Sepolia testnet ETH and USDC

## Setup and Run

### 1. Environment Setup

```bash
cd {{path}}
cp .env-local .env
# Add PRIVATE_KEY to .env file
```

### 2. Install Dependencies

```bash
uv sync  # Python
# or
pnpm install  # TypeScript
```

### 3. Run

```bash
uv run python main.py  # Python
# or
pnpm dev  # TypeScript
```

## Key Concepts

### {{Concept 1}}

{{Description}}

### {{Concept 2}}

{{Description}}

## Next Steps

- [{{Related Doc 1}}](link)
- [{{Related Doc 2}}](link)

---

[← Parent](../README.md) | [Next →]({{nextPath}})

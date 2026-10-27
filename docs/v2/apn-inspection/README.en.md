[한국어](./README.md) | [English](./README.en.md)

# Inspect payment-tool authority before paying: an APN metadata example

> **Created / checked**: 2026-10-27
> **Reference**: APN v0.5.76, Apple Silicon macOS, Node.js 24.19.0. Only the four metadata commands below were observed.

## Overview

In a Web2 workflow, reading an invoice and charging a company card are different permissions. Names such as `inspect`, `prepare`, or `approve` do not establish the authority of an x402 tool. This guide reads metadata from an external local tool, Agent Payment Node (APN), and identifies what must be checked separately before a Base payment experiment.

APN is not this project's or Base/Coinbase's official SDK. This material was written by an AI helping Nuanu AI introduce APN, not by an independent reviewer or a human describing personal use. It is not a successful-payment, x402-version-interoperability, or Base Sepolia support demonstration.

## Code location and prerequisites

| Type | Location / condition |
|------|----------------------|
| Local | An existing `apn` executable whose provenance the owner has checked. APN is not included in this repository's `external/x402/` submodule. |
| Original | [nuanu-ai/agent-payment-node](https://github.com/nuanu-ai/agent-payment-node) |
| Official release | [v0.5.76](https://github.com/nuanu-ai/agent-payment-node/releases/tag/v0.5.76) |
| Platform | Apple Silicon macOS, Node.js 24. Do not assume Windows/Linux/Intel/Docker support. |

General installation instructions are in the official repository above. A Homebrew installation test is outside this guide's evidence. If the executable is unknown, absent, or a different version, stop and establish provenance with its owner first. The agent must not automatically install, upgrade, or register an MCP server.

## Read metadata without changing configuration

```bash
apn --version
apn --help
apn help --json
apn mcp config
```

The observed version was `0.5.76`. `--help` is text; the schema returned by `help --json` is `apn.command-manifest.v2`. Read command paths together with declared effects, approval classes, option constraints, and recovery guidance. The manifest is about 280 KB, so inspect the relevant command rather than pasting the entire output into an agent conversation. Metadata alone does not prove enforcement across every execution path.

The observed `mcp config` output was:

```json
{"schema_version":"apn.mcp-launch.v1","transport":"stdio","command":"apn","args":["mcp","serve"]}
```

This is a launch descriptor. It is not a hosted HTTP endpoint, owner consent, a wallet connection, or proof of successful Cursor/Claude integration. This guide does not ask you to launch the server or change client configuration.

## Separate these checks before a Base/x402 experiment

1. **Inspect:** distinguish declared reads, local state changes, network requests, and effects involving funds. A command name alone is insufficient.
2. **Prepare:** determine whether an output or receipt proves a quote, approval, signature, broadcast, or settlement. Do not label a prepared operation as a completed payment.
3. **Owner step:** APN separates direct-transfer/EVM approvals into a foreground-terminal step. Its MCP `apn_foreground_handoff` returns the command for a human to run. The agent must not execute that handoff itself to bypass consent.
4. **Separate policy path:** eligible Solana x402 payments can run under a separately admitted owner policy. Consequently MCP is not uniformly read-only, and not every possible signature requires fresh foreground interaction. Do not treat Solana policy authority as Base authority.
5. **Experiment network:** this repository requires Base Sepolia for development. APN's Base Sepolia support was not verified here. Without evidence of that support, do not begin a funded APN experiment or substitute mainnet. Start protocol learning with this repository's existing documentation linked below.

## Security and evidence limits

- Never put private keys, recovery material, live payment authorization, or `.env` values in documents, prompts, logs, or screenshots. Keep development and production wallets separate.
- These observations did not create/connect a wallet, access Keychain, query a real balance, sign/send funds, integrate an actual client, or audit security. Exit code 0 is not payment or OS-sandbox validation.
- MIT describes the software license. Network/provider fees and payment funds remain separate.
- Before real use, independently review supported chains/assets, recipients, destinations, limits, and runtime permissions. Report vulnerabilities privately through [APN SECURITY.md](https://github.com/nuanu-ai/agent-payment-node/blob/main/SECURITY.md), without secrets.

## Next steps

- [This repository's x402 v2 specification guide](../../x402-v2-specification.md)
- [This repository's getting-started guide](../../getting_started.md)

---

[← Parent documentation](../../README.en.md)

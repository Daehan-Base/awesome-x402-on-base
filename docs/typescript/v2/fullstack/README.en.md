[한국어](./README.md) | [English](./README.en.md)

# x402 Fullstack Examples

This directory contains fullstack examples that integrate the x402 payment protocol on both frontend and backend.

## Directory Structure

| Directory | Description |
| --------- | ----------- |
| [`next/`](./next/) | Next.js x402 integration example (`@x402/next`, `@x402/fetch`) |
| [`miniapp/`](./miniapp/) | Farcaster Mini App + x402 payment integration example |

## Example Descriptions

### Next.js (`next/`)

Demonstrates how to protect Next.js routes with payments using `@x402/next` middleware.

- `paymentProxy` - Page route protection
- `withX402` - API route protection
- EVM + SVM multi-network support
- Custom Paywall UI configuration

### Farcaster Mini App (`miniapp/`)

Shows how to combine Farcaster Mini App SDK with x402 to handle payments within social apps.

- OnchainKit wallet connection
- Mini App manifest configuration
- x402 protected API endpoints

## Getting Started

1. Choose your desired example directory.
2. Follow the README in that directory to set up the environment.
3. Run the development server to test.

---

[← Back to v2 Documentation](../README.md)

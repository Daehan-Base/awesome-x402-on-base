[한국어](./README.md) | [English](./README.en.md)

# ☕ AI Coffee Shop - AP2 & x402 Demo

A demo where an AI agent orders coffee and pays with cryptocurrency using AP2 (Agent Payment Protocol) and x402 payment protocol.

## Overview

This demo showcases:

- **A2A (Agent-to-Agent) Communication**: Standardized communication between client agent and coffee shop agent
- **AP2 Protocol**: IntentMandate → CartMandate → PaymentMandate flow
- **x402 Payment**: USDC payment via EIP-712 signatures (Base Sepolia testnet)
- **Customization**: Size (Short/Tall/Grande/Venti) and bean (Regular/Decaf) options

## Components

```
ap2-demo-coffee-shop/
├── client_agent/          # Customer AI agent (ADK Web UI)
│   ├── agent.py           # Root agent configuration
│   └── coffee_client_agent.py  # Order assistant agent
├── server/                # Coffee shop server
│   ├── __main__.py        # Server entry point
│   └── agents/
│       ├── coffee_shop_agent.py  # Barista agent
│       ├── x402_executor.py      # x402 payment processor
│       ├── menu.py               # Menu and pricing
│       └── routes.py             # A2A routing
└── local_wallet.py        # Local wallet service
```

## Menu

### Beverages (Tall size base)

| Item | Price | Description |
|------|-------|-------------|
| Americano | $0.045 | Bold espresso |
| Cafe Latte | $0.050 | Smooth milk and espresso |
| Cappuccino | $0.055 | Rich foam |
| Vanilla Latte | $0.060 | Sweet vanilla aroma |
| Caramel Macchiato | $0.065 | Sweet caramel drizzle |
| Mocha | $0.060 | Chocolate and espresso harmony |

### Size Options

| Size | Volume | Price Difference |
|------|--------|------------------|
| Short | 237ml | -$0.005 |
| Tall | 355ml | Base |
| Grande | 473ml | +$0.005 |
| Venti | 591ml | +$0.010 |

### Bean Options

| Bean | Price Difference | Description |
|------|------------------|-------------|
| Regular | $0 | House blend |
| Decaf | +$0.003 | Caffeine removed |
| Half-Decaf | +$0.003 | 50% decaf |

## Prerequisites

- **Python 3.13+**: Check with `python --version`
- **uv package manager**: Install with `pip install uv`

## Installation

```bash
cd examples/ap2-demo-coffee-shop

# Check prerequisites
python --version  # Requires Python 3.13+
uv --version      # Requires uv package manager

# Set up environment variables
cp .env.example .env
# Edit .env file to set required values

# Install dependencies
uv sync
```

## Running

You need 3 terminals:

### Terminal 1: Local Wallet

```bash
cd examples/ap2-demo-coffee-shop
uv run python local_wallet.py
```

The wallet service will run at `http://localhost:5001`.

### Terminal 2: Coffee Shop Server

```bash
cd examples/ap2-demo-coffee-shop
uv run server
```

The coffee shop server will run at `http://localhost:10000`.

### Terminal 3: Client Agent (ADK Web UI)

```bash
cd examples/ap2-demo-coffee-shop
uv run adk web
```

Open `http://localhost:8000` in your browser to chat with the AI.

## Usage Example

```
User: I'd like an Americano please

AI: One Americano! ☕ What size would you like?
    (Short/Tall/Grande/Venti, default: Tall)

User: Grande

AI: Please choose from Regular, Decaf, or Half-Decaf beans. (default: Regular)

User: Decaf

AI: Would you like to order a Grande Decaf Americano?

User: Yes

AI: ☕ Intent mandate created:
    📝 "1 Grande Decaf Americano"
    Say 'confirm order' to finalize your order.

User: confirm order

AI: ✅ Signed the intent mandate. Sending to coffee shop!

(Coffee shop receives CartMandate)

AI: ☕ AI Coffee Shop prepared your order!
    📋 Order details:
      - Grande Decaf Americano: $0.053
    💰 Total: $0.053 USD
    Say 'proceed with payment' to continue.

User: proceed with payment

AI: 💳 Prepared $0.053 USDC payment.
    Say 'approve payment' to authorize.

User: approve payment

AI: ✅ Payment mandate generated.
    Say 'final approval' for final confirmation.

User: final approval

AI: ✅ Payment completed!
    ☕ Preparing your drink. Please wait!
```

## Payment Flow

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  Client Agent   │         │  Coffee Shop    │         │  Facilitator    │
│  (Customer AI)  │         │  Agent (Barista)│         │  (x402.org)     │
└────────┬────────┘         └────────┬────────┘         └────────┬────────┘
         │                           │                           │
         │  1. IntentMandate         │                           │
         │  (Order intent)           │                           │
         │ ────────────────────────► │                           │
         │                           │                           │
         │  2. CartMandate           │                           │
         │  (Cart + price)           │                           │
         │ ◄──────────────────────── │                           │
         │                           │                           │
         │  3. PaymentMandate        │                           │
         │  (EIP-712 signature)      │                           │
         │ ────────────────────────► │                           │
         │                           │                           │
         │                           │  4. verify()              │
         │                           │ ────────────────────────► │
         │                           │                           │
         │                           │  5. settle()              │
         │                           │ ────────────────────────► │
         │                           │                           │
         │                           │  (USDC transfer on-chain) │
         │                           │ ◄──────────────────────── │
         │                           │                           │
         │  6. Order complete        │                           │
         │ ◄──────────────────────── │                           │
         │                           │                           │
```

## Test Preparation

### 1. Create Test Wallet

Create a test wallet and set the Private Key in `.env`.

### 2. Get Base Sepolia ETH

Get test ETH from [Coinbase Faucet](https://www.coinbase.com/faucets/base-ethereum-sepolia-faucet).

### 3. Get Test USDC

Get Base Sepolia USDC from [Circle Faucet](https://faucet.circle.com/).


## Tech Stack

- **Python 3.13+**
- **uv**: Modern Python package manager
- **Google ADK**: AI agent framework
- **A2A Protocol**: Agent-to-agent communication standard
- **AP2**: Agent Payment Protocol
- **x402**: HTTP 402-based payment protocol
- **Base Sepolia**: Ethereum L2 testnet
- **USDC**: Stablecoin payment

## License

Apache License 2.0

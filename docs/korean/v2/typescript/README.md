# X402 타입스크립트 예제

이 디렉토리는 다양한 시나리오에서 X402 프로토콜을 사용하는 방법을 보여주는 TypeScript 예제들을 포함하고 있습니다. 예제들은 X402 npm 패키지와 함께 사용하도록 설계되었으며, 주요 X402 패키지와 동일한 워크스페이스를 공유합니다.

## 설치

예제를 진행하기 전에 먼저 필요한 의존성 패키지를 설치하고 빌드해야 합니다.

```bash
# examples/typescript 디렉토리에서 실행
pnpm install
pnpm build
```

## 예제 구조

예제는 다음과 같은 카테고리들로 구성되어 있습니다.

### Clients

X402 서비스와 상호작용하기 위한 다양한 클라이언트 구현 예제입니다.

- `clients/axios/` - `x402-axios`에서 제공된 x402 결제 인터셉터를 사용하는 axios 클라이언트
- `clients/fetch/` - 네이티브 fetch API를 래핑한 `x402-fetch`를 사용하는 클라이언트
- `clients/cdp-sdk/` - CDP Server Wallets를 서명자(signer)로 두고 `x402-axios`를 사용하는 클라이언트
- `clients/chainlink-vrf-nft/` - [Chainlink](docs.chain.link)를 사용해 랜덤 NFT를 민팅하는 예제([Opensea](https://testnets.opensea.io/collection/vrfnft-1)에서 확인 가능)입니다. `x402-axios`를 사용해 검증 및 정산(verify/settle) 플로우를 구현합니다.

### Agents

- `agent/` - `x402-fetch`를 사용하여 Go 프록시를 통해 결제하는 Anthropic 에이전트
- `dynamic_agent/` - 동적으로 도구를 탐색하고 요청 단위(per-request)로 x402 결제를 수행하는 에이전트

### Discovery

- `discovery/` - Facilitator를 통해 x402로 보호된 사용 가능한 리소스 목록(Bazaar)을 조회하는 예제

### MCP

- `mcp/` - `x402-axios`를 통해 유료 API 요청을 수행하는 MCP 서버 (Claude 데스크탑 앱과 호환)
- `mcp-embedded-wallet/` - 임베디드 월렛을 포함한 일렉트론(Electron) 기반 MCP 서버로 IPC를 통해 요청에 서명합니다.

### Facilitator

- `facilitator/` - `/verify`, `/settle` 엔드포인트를 노출하는 x402 결제 중개자(facilitator) 예제 구현

### Fullstack

- `fullstack/next/` - `x402-next` 미들웨어를 사용해 라우트 보호(route protection)를 구현한 Next.js 앱입니다.
- `fullstack/mainnet/` - 코인베이스 호스팅 Facilitator를 사용하고 Base 메인넷에 맞게 구성된 Next.js 앱입니다.
- `fullstack/next-advanced/` - [WIP] 검증/정산 이후 페이월(paywall) + 세션 쿠키(session cookie)를 시용하는 심화된 Next.js 통합 예제
- `fullstack/browser-wallet-example/` - 브라우저 지갑 템플릿: 세션 및 일회성 결제를 지원하는 Hono 서버 + React 클라이언트
- `fullstack/farcaster-miniapp/` - [MiniKit](https://www.base.org/build/mini-apps)을 사용해 x402로 보호된 API를 제공하는 Farcaster Mini App 템플릿
- `fullstack/auth_based_pricing/` - SIWE + JWT를 활용한 조건부 가격 정책 예제 (JWT 포함 시 $0.01, 미포함 시 $0.10)

### Servers

다양한 서버 구현 예제입니다.

- `servers/express/` - `x402-express` 미들웨어를 사용하는 Express 서버
- `servers/hono/` - `x402-hono` 미들웨어를 사용하는 Hono 서버
- `servers/advanced/` - 미들웨어를 사용하지 않는 Express 서버 예제: 지연 결제(settlement), 동적 가격 책정, 복수 요구 조건 처리
- `servers/mainnet/` - 코인베이스 호스팅 Facilitator를 사용하여 Base 메인넷에서 실제 USDC 결제를 수락하는 서버 예제

## 예제 실행

각 예제 디렉토리에는 실행하기 위한 구체적인 지침이 포함된 자체 README가 있습니다. 원하는 예제로 이동한 후, 해당 README에 안내된 절차를 따라 실행하세요.

## 개발 환경

이 워크스페이스는 다음 도구들을 사용합니다.

- pnpm: 패키지 관리
- Turborepo: 모노레포(monorepo) 관리
- TypeScript: 타입 안정성 보장

예제들은 메인 X402 패키지와 함께 동작하도록 설계되어 있으므로 예제를 실행하기 전에는 반드시 패키지를 먼저 빌드해야 합니다.

## 개인키(private keys) 관련 주의사항

이 예제들은 메세지 서명을 위해 개인키(private key)를 사용하는 경우가 많습니다. **메인넷 자금이 포함된 개인키를 절대 .env 파일에 저장하지 마세요**. 이로 인해 키가 코드베이스에 포함되어 유출되거나 자금을 도난당할 수 있습니다.

개발 전용으로 사용할 키페어(keypair)를 생성하는 방법은 여러가지가 있습니다. 그중 하나는 Foundry를 사용하는 것입니다.

```
# Foundry 설치
curl -L https://foundry.paradigm.xyz | bash

# 새 지갑 생성
cast w new
```

생성된 지갑은 대부분의 네트워크에서 테스트넷 [CDP Faucet](https://portal.cdp.coinbase.com/products/faucet)을 통해 자금을 받을 수 있습니다. cast 명령으로 생성한 주소를 입력하면 됩니다.

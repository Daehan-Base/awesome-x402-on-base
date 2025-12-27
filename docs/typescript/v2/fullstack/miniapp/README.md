[한국어](./README.md) | [English](./README.en.md)

# x402 Farcaster Mini App 예제 (v2 SDK)

이 프로젝트는 [Next.js](https://nextjs.org) 기반으로 `@x402/next`, `@x402/fetch`, `@x402/evm` 패키지를 사용해 x402 결제 보호 API 엔드포인트를 포함한 [Farcaster Mini App](https://miniapps.farcaster.xyz/)을 구축하는 방법을 시연합니다.

## 사전 준비 사항

- Node.js 22 이상
- pnpm v10 (설치: [pnpm.io/installation](https://pnpm.io/installation))
- Base Sepolia 테스트넷의 USDC

## 시작하기

1. 타입스크립트 예제 루트에서 전체 패키지 설치 및 빌드

```bash
cd ../../
pnpm install && pnpm build
cd fullstack/miniapp
```

2. 다음 환경 변수를 설정합니다.

```bash
cp .env-local .env
```

3. 환경 변수 설정 (아래 "환경 변수 설정 방법" 참고)

4. 개발 서버 실행

```bash
pnpm dev
```

5. 브라우저에서 [http://localhost:3000](http://localhost:3000) 접속

## 환경 변수 설정 방법

`.env` 파일에서 다음 환경 변수들을 설정하세요.

### 필요한 변수

```bash
# x402 결제 설정 (필수)
FACILITATOR_URL=https://x402.org/facilitator
EVM_ADDRESS=0xYourWalletAddress

# OnchainKit 설정
NEXT_PUBLIC_ONCHAINKIT_API_KEY=your_onchainkit_api_key_here
NEXT_PUBLIC_ONCHAINKIT_PROJECT_NAME=x402 Mini App

# 앱 URL과 이미지
NEXT_PUBLIC_URL=http://localhost:3000
NEXT_PUBLIC_APP_HERO_IMAGE=https://example.com/app-logo.png
NEXT_PUBLIC_SPLASH_IMAGE=https://example.com/app-logo-200x200.png
NEXT_PUBLIC_SPLASH_BACKGROUND_COLOR=#3b82f6
NEXT_PUBLIC_ICON_URL=https://example.com/app-logo.png
```

### API 가져오기

1. **OnchainKit API Key**: [OnchainKit](https://onchainkit.xyz)에서 발급
2. **EVM Address**: 결제 받을 지갑 주소
3. **Facilitator URL**: 공개 facilitator를 사용하거나 직접 운영

## 동작 방식

### 서버 사이드 결제 보호

`/api/protected` 엔드포인트는 `withX402` 래퍼를 사용하여 결제 보호를 적용합니다.

```typescript
// app/api/protected/route.ts
import { withX402 } from "@x402/next";
import { x402ResourceServer, HTTPFacilitatorClient } from "@x402/core/server";
import { registerExactEvmScheme } from "@x402/evm/exact/server";

const facilitatorClient = new HTTPFacilitatorClient({
  url: process.env.FACILITATOR_URL,
});
const server = new x402ResourceServer(facilitatorClient);
registerExactEvmScheme(server);

export const GET = withX402(
  handler,
  {
    accepts: [
      {
        scheme: "exact",
        price: "$0.01",
        network: "eip155:84532", // base-sepolia
        payTo: process.env.EVM_ADDRESS,
      },
    ],
    description: "Access to protected Mini App API",
    mimeType: "application/json",
  },
  server,
);
```

### 클라이언트 사이드 결제 처리

프론트엔드는 `@x402/fetch`를 사용해 결제를 처리합니다.

```typescript
import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";

// 클라이언트 생성 및 EVM 스키마 등록
const client = new x402Client();
registerExactEvmScheme(client, { signer: wagmiToClientSigner(walletClient) });

// 결제 처리가 포함된 fetch 래핑
const fetchWithPayment = wrapFetchWithPayment(fetch, client);

// 요청 수행 - 결제는 자동 처리됨
const response = await fetchWithPayment("/api/protected");
```

### Farcaster Mini App 통합

Farcaster Mini App SDK를 사용하여 Mini App 컨텍스트 여부를 감지합니다.

```typescript
import { sdk } from "@farcaster/miniapp-sdk";

await sdk.actions.ready();
const isInMiniApp = await sdk.isInMiniApp();
```

### Manifest 설정

이 앱은 Farcaster 및 Base 앱에 Mini App을 퍼블리시하기 위해 필요한 manifest를 `/.well-known/farcaster.json` 경로에서 제공합니다. `minikit.config.ts`에서 앱 설정을 구성합니다.

```typescript
// minikit.config.ts
export const minikitConfig = {
  // Generate at https://warpcast.com/~/developers/mini-apps/manifest
  accountAssociation: {
    header: "your-signed-header",
    payload: "your-signed-payload",
    signature: "your-signature",
  },
  baseBuilder: {
    ownerAddress: "0xYourWalletAddress",
  },
  miniapp: {
    version: "1",
    name: "x402 Mini App",
    // ... other config
  },
};
```

**배포하기 전에**, 반드시 해야하는 것들

1. [Base Dev Mini App Tools](https://www.base.dev/preview?tab=account) 또는 [Farcaster Manifest Tool](https://farcaster.xyz/~/developers/mini-apps/manifest)애서 `accountAssociation` 생성
2. `baseBuilder.ownerAddress`를 본인 지갑 주소로 설정
3. `NEXT_PUBLIC_URL`를 프로덕션 도메인으로 변경
4. 이미지가 요구 조건을 만족하는지 확인
   - `iconUrl`: 1024x1024px PNG, 알파 채널 없음
   - `splashImageUrl`: 200x200px
   - `heroImageUrl`: 1200x630px (1.91:1 비율)

## 응답 포맷

### Payment Required (402)

```
HTTP/1.1 402 Payment Required
Content-Type: application/json
PAYMENT-REQUIRED: <base64-encoded JSON>
```

`PAYMENT-REQUIRED` 헤더에는 결제 요구사항이 포함됩니다.

```json
{
  "x402Version": 2,
  "error": "Payment required",
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:84532",
      "amount": "10000",
      "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
      "payTo": "0x...",
      "maxTimeoutSeconds": 300,
      "extra": { "name": "USDC", "version": "2" }
    }
  ]
}
```

### 성공 응답

```json
{
  "success": true,
  "message": "Protected action completed successfully",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "secretMessage": "This content was paid for with x402!",
    "accessedAt": 1704067200000
  }
}
```

## 예제 확장하기

### 보호 라우트 추가

새 라우트 파일(예: `app/api/premium/route.ts`)를 만들고 `withX402` 레퍼를 적용합니다.

```typescript
// app/api/premium/route.ts
import { NextRequest, NextResponse } from "next/server";
import { withX402 } from "@x402/next";
import { x402ResourceServer, HTTPFacilitatorClient } from "@x402/core/server";
import { registerExactEvmScheme } from "@x402/evm/exact/server";

const facilitatorClient = new HTTPFacilitatorClient({
  url: process.env.FACILITATOR_URL,
});
const server = new x402ResourceServer(facilitatorClient);
registerExactEvmScheme(server);

const handler = async (_: NextRequest) => {
  return NextResponse.json({ message: "Premium content!" });
};

export const GET = withX402(
  handler,
  {
    accepts: [
      {
        scheme: "exact",
        price: "$0.10",
        network: "eip155:84532",
        payTo: process.env.EVM_ADDRESS,
      },
    ],
    description: "Premium content access",
    mimeType: "application/json",
  },
  server,
);
```

### 네트워크 식별자

네트워크 식별자는 [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md) 형식을 사용합니다.

- `eip155:84532` - Base Sepolia
- `eip155:8453` - Base Mainnet

## Resources

- [Farcaster Mini Apps 문서](https://miniapps.farcaster.xyz/)
- [x402 Protocol 문서](https://x402.org)
- [OnchainKit 문서](https://onchainkit.xyz)
- [MiniKit 문서](https://docs.base.org/builderkits/minikit/overview)
- [Next.js 문서](https://nextjs.org/docs)
- [Tailwind CSS v4 문서](https://tailwindcss.com/docs)

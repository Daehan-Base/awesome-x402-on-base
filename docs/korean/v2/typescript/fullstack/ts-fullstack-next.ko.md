# x402-next 예제 앱

`@x402/next` 미들웨어를 사용하여 페이월(paywall)로 라우트를 보호하는 방법을 보여주는 Next.js 애플리케이션 예제입니다.

## 사전 준비 사항

- Node.js v20 이상 (설치: [nvm](https://github.com/nvm-sh/nvm))
- pnpm v10 (설치: [pnpm.io/installation](https://pnpm.io/installation))
- 결제 받기 위한 유효한 EVM 및 SVM 주소
- 원하는 결제 네트워크를 지원하는 Facilitator URL, 참고: [facilitator 목록](https://www.x402.org/ecosystem?category=facilitators)

## Setup

1. `.env-local`파일을 `.env`로 복사

```bash
cp .env-local .env
```

다음 환경 변수를 설정합니다.

- `FACILITATOR_URL` - Facilitator 엔드포인트 URL
- `EVM_ADDRESS` - 결제 받을 이더리움 주소
- `SVM_ADDRESS` - 결제 받을 솔라나 주소

2. 타입스크립트 예제 루트에서 전체 패키지 설치 및 빌드
```bash
cd ../../
pnpm install && pnpm build
cd fullstack/next
```

3. 서버 실행
```bash
pnpm dev
```

## 예제 라우트

이 앱에는 접근 시 결제가 필요한 보호 라우트(protected routes)가 포함되어 있습니다.

### 보호된 페이지 라우트

`/protected` 라우트는 `paymentProxy`를 사용해 보호됩니다. 페이지 라우트는 다음 방식으로 보호됩니다.

```typescript
// proxy.ts
import { paymentProxy } from "@x402/next";
import { x402ResourceServer, HTTPFacilitatorClient } from "@x402/core/server";
import { registerExactEvmScheme } from "@x402/evm/exact/server";
import { registerExactSvmScheme } from "@x402/svm/exact/server";
import { createPaywall } from "@x402/paywall";
import { evmPaywall } from "@x402/paywall/evm";
import { svmPaywall } from "@x402/paywall/svm";

const facilitatorClient = new HTTPFacilitatorClient({ url: facilitatorUrl });
const server = new x402ResourceServer(facilitatorClient);

// 스키마 등록
registerExactEvmScheme(server);
registerExactSvmScheme(server);

// 빌드 패턴으로 paywall 구성
const paywall = createPaywall()
  .withNetwork(evmPaywall)
  .withNetwork(svmPaywall)
  .withConfig({
    appName: "Next x402 Demo",
    appLogo: "/x402-icon-blue.png",
    testnet: true,
  })
  .build();

export const proxy = paymentProxy(
  {
    "/protected": {
      accepts: [
        {
          scheme: "exact",
          price: "$0.001",
          network: "eip155:84532",
          payTo: evmAddress,
        },
        {
          scheme: "exact",
          price: "$0.001",
          network: "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1",
          payTo: svmAddress,
        },
      ],
      description: "Premium music: x402 Remix",
      mimeType: "text/html",
    },
  },
  server,
  undefined, // paywallConfig (대신 커스텀 paywall 사용)
  paywall,   // 커스텀 paywall provider
);

export const config = {
  matcher: ["/protected/:path*"],
};
```

### Weather API 라우트 (withX402 사용)

`/api/weather` 라우트는 개별 API 라우트를 보호하기 위해 `withX402` 래퍼를 사용합니다.

```typescript
// app/api/weather/route.ts
import { NextRequest, NextResponse } from "next/server";
import { withX402 } from "@x402/next";
import { server, paywall, evmAddress, svmAddress } from "../../../proxy";

const handler = async (_: NextRequest) => {
  return NextResponse.json({
    report: {
      weather: "sunny",
      temperature: 72,
    },
  });
};

export const GET = withX402(
  handler,
  {
    accepts: [
      {
        scheme: "exact",
        price: "$0.001",
        network: "eip155:84532",
        payTo: evmAddress,
      },
      {
        scheme: "exact",
        price: "$0.001",
        network: "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1",
        payTo: svmAddress,
      },
    ],
    description: "Access to weather API",
    mimeType: "application/json",
  },
  server,
  undefined, // paywallConfig (proxy.ts의 커스텀 paywall 사용)
  paywall,
);
```

## 응답 포맷

### Payment Required (402)

```
HTTP/1.1 402 Payment Required
Content-Type: application/json; charset=utf-8
PAYMENT-REQUIRED: <base64-encoded JSON>

{}
```

`PAYMENT-REQUIRED` 헤더에는 결제 요구 사항을 담은 base64 인코딩 JSON이 포함됩니다.
참고: `amount`는 최소 단위(atomic units)로 표현됩니다. (예: USDC는 소수점 6자리이므로 1000 = 0.001 USDC)

```json
{
  "x402Version": 2,
  "error": "Payment required",
  "resource": {
    "url": "http://localhost:3000/api/weather",
    "description": "Access to weather API",
    "mimeType": "application/json"
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:84532",
      "amount": "1000",
      "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
      "payTo": "0x...",
      "maxTimeoutSeconds": 300,
      "extra": {
        "name": "USDC",
        "version": "2",
        "resourceUrl": "http://localhost:4021/weather"
      }   
    }
  ]
}
```

### 성공 응답

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
PAYMENT-RESPONSE: <base64-encoded JSON>

{"report":{"weather":"sunny","temperature":72}}
```

`PAYMENT-RESPONSE` 헤더에는 정산(settlement) 상세 정보를 담은 base64 인코딩 JSON이 포함됩니다.

```json
{
  "success": true,
  "transaction": "0x...",
  "network": "eip155:84532",
  "payer": "0x...",
  "requirements": {
    "scheme": "exact",
    "network": "eip155:84532",
    "amount": "1000",
    "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
    "payTo": "0x...",
    "maxTimeoutSeconds": 300,
    "extra": {
      "name": "USDC",
      "version": "2",
      "resourceUrl": "http://localhost:4021/weather"
    }
  }
}
```

## paymentProxy vs withX402

`paymentProxy`는 페이지 라우트를 보호할 때 사용하는 방식입니다. API 라우트도 보호할 수는 있지만, API가 실패한 응답(에러 응답)인 경우에도 과금될 수 있는 문제가 있습니다.

`withX402`는 API 라우트 핸들러를 감싸는 방식이며, API 응답이 성공(status < 400)한 뒤에만 정산(settlement)이 이뤄지도록 보장하므로 API 보호에는 이 방식을 권장합니다.

| 방식           | 유스케이스                                                      |
| -------------- | --------------------------------------------------------------- |
| `paymentProxy` | 페이지 라우트 보호, 또는 여러 라우트를 하나의 설정으로 보호     |
| `withX402`     | 개별 API 라우트 보호(정산 타이밍을 정밀하게 제어해야 하는 경우) |

## 예제 확장하기

보호 라우트를 추가하기 위해서는 proxy 설정을 확장해야 합니다.

```typescript
export const proxy = paymentProxy(
  {
    "/protected": {
      accepts: {
        scheme: "exact",
        price: "$0.001",
        network: "eip155:84532",
        payTo: evmAddress,
      },
      description: "Access to protected content",
    },
    "/premium": {
      accepts: {
        scheme: "exact",
        price: "$0.10",
        network: "eip155:84532",
        payTo: evmAddress,
      },
      description: "Premium content access",
    },
  },
  server,
  undefined,
  paywall,
);

export const config = {
  matcher: ["/protected/:path*", "/premium/:path*"],
};
```

**네트워크 식별자**는 [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md) 형식을 사용합니다. 예:
- `eip155:84532` — Base Sepolia
- `eip155:8453` — Base Mainnet
- `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` — Solana Devnet
- `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` — Solana Mainnet

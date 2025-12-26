[한국어](./README.md) | [English](./README.en.md)

# @x402/hono 서버 예제

`@x402/hono` 미들웨어를 사용해 페이월(paywall)로 API 엔드포인트를 보호하는 방법을 보여주는 Hono 서버 예제입니다.

```typescript
import { Hono } from "hono";
import { paymentMiddleware, x402ResourceServer } from "@x402/hono";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";

const app = new Hono();

app.use(
  paymentMiddleware(
    {
      "GET /weather": {
        accepts: { scheme: "exact", price: "$0.001", network: "eip155:84532", payTo: evmAddress },
        description: "Weather data",
        mimeType: "application/json",
      },
    },
    new x402ResourceServer(new HTTPFacilitatorClient({ url: facilitatorUrl }))
      .register("eip155:84532", new ExactEvmScheme()),
  ),
);

app.get("/weather", c => c.json({ weather: "sunny", temperature: 70 }));
```

## 사전 준비 사항

- Node.js v20 이상 (설치: [nvm](https://github.com/nvm-sh/nvm))
- pnpm v10 (설치: [pnpm.io/installation](https://pnpm.io/installation))
- 결제 받기 위한 유효한 EVM 및 SVM 주소
- 원하는 결제 네트워크를 지원하는 Facilitator URL (참고: [facilitator 목록](https://www.x402.org/ecosystem?category=facilitators))

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
cd servers/hono
```

3. 서버 실행

```bash
pnpm dev
```

## 서버 테스트 방법

예제 클라이언트 중 하나를 사용하여 서버를 테스트할 수 있습니다.

### Fetch 클라이언트 사용

```bash
cd ../clients/fetch
# .env 설정이 되어 있는지 확인
pnpm dev
```

### Axios 클라이언트 사용

```bash
cd ../clients/axios
# .env 설정이 되어 있는지 확인
pnpm dev
```

이 클라이언트들은 다음 과정을 시연합니다.

1. 최초 요청을 보내 결제 요구 사항을 수신
2. 결제 요구 사항을 처리
3. 결제 토큰(결제 헤더)을 포함하여 두 번째 요청 수행

## 예제 엔드포인트

서버에는 `/weather` 단일 예제 엔드포인트가 포함되어 있으며, 접근을 위해 Base Sepolia 또는 Solana Devnet에서 0.001 USDC 결제가 필요합니다. 응답은 간단한 날씨 리포트를 반환합니다.

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
    "url": "http://localhost:4021/weather",
    "description": "Weather data",
    "mimeType": "application/json"
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:84532",
      "amount": "1000",
      "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
      "payTo": "0x1c47E9C085c2B7458F5b6C16cCBD65A65255a9f6",
      "maxTimeoutSeconds": 300,
      "extra": {
        "name": "USDC",
        "version": "2",
        "resourceUrl": "http://localhost:4021/weather"
      }
    },
    {
      "scheme": "exact",
      "network": "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1",
      "amount": "1000",
      "asset": "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU",
      "payTo": "FV6JPj6Fy12HG8SYStyHdcecXYmV1oeWERAokrh4GQ1n",
      "maxTimeoutSeconds": 300,
      "extra": {
        "feePayer": "...",
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

{"report":{"weather":"sunny","temperature":70}}
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

## 예제 확장하기

유료 엔드포인트를 추가하려면 아래 패턴을 따릅니다.

```typescript
// 먼저 결제 미들웨어에 라우트 구성 추가
app.use(
  paymentMiddleware(
    {
      "GET /your-endpoint": {
        accepts: {
          scheme: "exact",
          price: "$0.10",
          network: "eip155:84532",
          payTo: evmAddress,
        },
        description: "Your endpoint description",
        mimeType: "application/json",
      },
    },
    resourceServer,
  ),
);

// 라우트는 평소처럼 정의
app.get("/your-endpoint", (c) => {
  return c.json({
    // 응답 데이터
  });
});
```

**네트워크 식별자**는 [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md) 형식을 사용합니다. 예:

- `eip155:84532` — Base Sepolia
- `eip155:8453` — Base Mainnet
- `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` — Solana Devnet
- `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` — Solana Mainnet

## x402ResourceServer 설정

`x402ResourceServer`는 빌더 패턴으로 결제 스키마를 등록하며, 각 네트워크에서 결제를 어떻게 처리할지 선언합니다.

```typescript
const resourceServer = new x402ResourceServer(facilitatorClient)
  .register("eip155:*", new ExactEvmScheme()) // 모든 EVM 체인
  .register("solana:*", new ExactSvmScheme()); // 모든 SVM 체인
```

## Facilitator 설정

`HTTPFacilitatorClient`는 온체인에서 결제를 검증 및 정산하는 Facilitator 서비스에 연결합니다.

```typescript
const facilitatorClient = new HTTPFacilitatorClient({ url: facilitatorUrl });

// 또는 이중화(레던던시)를 위해 여러 Facilitator 사용
const facilitatorClient = [
  new HTTPFacilitatorClient({ url: primaryFacilitatorUrl }),
  new HTTPFacilitatorClient({ url: backupFacilitatorUrl }),
];
```

## 다음 단계

[Advanced 예제](/external/x402/examples/typescript/servers/advanced/)에서 아래 항목을 확인할 수 있습니다.

- **Bazaar Discovery** — API를 발견 가능하게 노출
- **Dynamic pricing** — 요청 컨텍스트 기반 가격 산정
- **Dynamic payTo** — 요청별 결제 수신자 라우팅
- **Lifecycle hooks** — verify/settle에 사용자 정의 로직 추가
- **Custom tokens** — 커스텀 토큰 결제 수락


# @x402/express 고급 예제

고급 x402 패턴을 사용하는 Express.js 서버 예제입니다. 동적 가격 책정, 결제 라우팅(payTo), 라이프사이클 훅, API 디스커버리(발견 가능성) 등을 시연합니다.

```typescript
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";

const resourceServer = new x402ResourceServer(new HTTPFacilitatorClient({ url: facilitatorUrl }))
  .register("eip155:84532", new ExactEvmScheme())
  .onBeforeVerify(async ctx => console.log("Verifying payment..."))
  .onAfterSettle(async ctx => console.log("Settled:", ctx.result.transaction));

app.use(
  paymentMiddleware(
    {
      "GET /weather": {
        accepts: {
          scheme: "exact",
          price: ctx => (ctx.adapter.getQueryParam?.("tier") === "premium" ? "$0.01" : "$0.001"),
          network: "eip155:84532",
          payTo: evmAddress,
        },
      },
    },
    resourceServer,
  ),
);
```

## 사전 준비 사항

- Node.js v20 이상 (설치: [nvm](https://github.com/nvm-sh/nvm))
- pnpm v10 (설치: [pnpm.io/installation](https://pnpm.io/installation))
- 결제 받기 위한 유효한 EVM 주소
- 원하는 결제 네트워크를 지원하는 Facilitator URL (참고: [facilitator 목록](https://www.x402.org/ecosystem?category=facilitators))

## 설정 방법

1. `.env-local`파일을 `.env`로 복사

```bash
cp .env-local .env
```

다음 환경 변수를 설정합니다.

- `FACILITATOR_URL` - Facilitator 엔드포인트 URL
- `EVM_ADDRESS` - 결제 받을 이더리움 주소

2. 타입스크립트 예제 루트에서 전체 패키지 설치 및 빌드

```bash
cd ../../
pnpm install && pnpm build
cd servers/advanced
```

3. 서버 실행

```bash
pnpm dev
```

## 사용 가능한 예제

각 예제는 특정 고급 패턴 하나에 집중합니다.

| 예제                      | 실행 명령                          | 설명                                 |
| ------------------------- | ---------------------------------- | ------------------------------------ |
| `bazaar`                  | `pnpm dev:bazaar`                  | 바자르(Bazaar)를 통한 API 디스커버리 |
| `hooks`                   | `pnpm dev:hooks`                   | 결제 라이프사이클 훅                 |
| `dynamic-price`           | `pnpm dev:dynamic-price`           | 요청 컨텍스트 기반 가격 책정         |
| `dynamic-pay-to`          | `pnpm dev:dynamic-pay-to`          | 요청별 결제 수신자 라우팅            |
| `custom-money-definition` | `pnpm dev:custom-money-definition` | 대체 토큰 결제 수락                  |

## 서버 테스트 방법

예제 클라이언트 중 하나를 사용하여 서버를 테스트할 수 있습니다.

### Fetch 클라이언트 사용

```bash
cd ../../clients/fetch
# .env 설정이 되어 있는지 확인
pnpm dev
```

### Axios 클라이언트 사용

```bash
cd ../clients/axios
# .env 설정이 되어 있는지 확인
pnpm dev
```

## 예제: 바자르(Bazaar) 디스커버리

디스커버리 확장(extension)을 추가하여 API를 발견 가능(discoverable)하게 만듭니다.

```typescript
import { declareDiscoveryExtension } from "@x402/extensions/bazaar";

app.use(
  paymentMiddleware(
    {
      "GET /weather": {
        accepts: {
          scheme: "exact",
          price: "$0.001",
          network: "eip155:84532",
          payTo: evmAddress,
        },
        description: "Weather data",
        mimeType: "application/json",
        extensions: {
          ...declareDiscoveryExtension({
            input: { city: "San Francisco" },
            inputSchema: {
              properties: { city: { type: "string" } },
              required: ["city"],
            },
            output: {
              example: { city: "San Francisco", weather: "foggy", temperature: 60 },
            },
          }),
        },
      },
    },
    resourceServer,
  ),
);
```

**유스케이스:** 클라이언트 및 AI 에이전트가 서비스를 더 쉽게 탐색/발견할 수 있음

## 예제: 동적 가격(Dynamic Pricing)

요청 컨텍스트에 따라 런타임에 가격을 산정합니다.

```typescript
app.use(
  paymentMiddleware(
    {
      "GET /weather": {
        accepts: {
          scheme: "exact",
          price: context => {
            const tier = context.adapter.getQueryParam?.("tier") ?? "standard";
            return tier === "premium" ? "$0.005" : "$0.001";
          },
          network: "eip155:84532",
          payTo: evmAddress,
        },
      },
    },
    resourceServer,
  ),
);
```

**유스케이스:** 티어별 과금, 사용자별 과금, 콘텐츠 기반 과금 등 요청에 따라 가격이 달라지는 모든 시나리오

## 예제: 동적 PayTo

요청 컨텍스트에 따라 결제 수신자(payTo)를 다르게 라우팅합니다.

```typescript
const addressLookup: Record<string, `0x${string}`> = {
  US: "0x...",
  UK: "0x...",
};

app.use(
  paymentMiddleware(
    {
      "GET /weather": {
        accepts: {
          scheme: "exact",
          price: "$0.001",
          network: "eip155:84532",
          payTo: context => {
            const country = context.adapter.getQueryParam?.("country") ?? "US";
            return addressLookup[country];
          },
        },
      },
    },
    resourceServer,
  ),
);
```

**유스케이스:** 마켓플레이스처럼 리소스/판매자/크리에이터에 따라 수신자가 달라져야 하는 경우

## 예제: 라이프사이클 훅(Lifecycle Hooks)

검증(verify) 및 정산(settle) 전후에 사용자 정의 로직을 실행합니다.

```typescript
const resourceServer = new x402ResourceServer(facilitatorClient)
  .register("eip155:84532", new ExactEvmScheme())
  .onBeforeVerify(async context => {
    console.log("Before verify hook", context);
    // { abort: true, reason: string }을 반환하면 검증을 중단할 수 있습니다.
  })
  .onAfterSettle(async context => {
    await logPaymentToDatabase(context);
  })
  .onSettleFailure(async context => {
    // recovered=true를 가진 결과를 반환하면 실패에서 복구할 수 있습니다.
    // return { recovered: true, result: { success: true, transaction: "0x123..." } };
  });
```

사용 가능한 훅:

- `onBeforeVerify` — 검증 전 실행(중단 가능)
- `onAfterVerify` — 검증 성공 후 실행
- `onVerifyFailure` — 검증 실패 시 실행(복구 가능)
- `onBeforeSettle` — 정산 전 실행(중단 가능)
- `onAfterSettle` — 정산 성공 후 실행
- `onSettleFailure` — 정산 실패 시 실행(복구 가능)

**유스케이스:**

- 결제 이벤트를 DB/모니터링 시스템에 기록
- 결제 처리 전 사용자 정의 검증 수행
- 실패한 결제에 대한 재시도/복구 로직 구현
- 결제 성공 후 알림/DB 업데이트 등의 부수 효과(side effect) 트리거

## 예제: 커스텀 토큰(Custom Tokens)

커스텀 토큰 결제를 허용합니다. 스키마에 money parser를 등록해, 특정 네트워크에서 대체 토큰을 지원할 수 있습니다.

```typescript
import { ExactEvmScheme } from "@x402/evm/exact/server";

const resourceServer = new x402ResourceServer(facilitatorClient).register(
  "eip155:84532",
  new ExactEvmScheme().registerMoneyParser(async (amount, network) => {
    // Gnosis Chain에서 Wrapped XDAI 사용
    if (network === "eip155:100") {
      return {
        amount: BigInt(Math.round(amount * 1e18)).toString(),
        asset: "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d",
        extra: { token: "Wrapped XDAI" },
      };
    }
    return null; // 기본 파서로 fallback
  }),
);

// 결제 요구 사항에서 사용
"GET /weather": {
  accepts: {
    scheme: "exact",
    price: "$0.001",
    network: "eip155:100",
    payTo: evmAddress,
  },
},
```

**유스케이스:** USDC 이외 토큰을 받거나, 조건에 따라 네트워크별로 다른 토큰을 받고 싶은 경우

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

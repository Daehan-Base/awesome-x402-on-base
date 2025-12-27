[한국어](./README.md) | [English](./README.en.md)

# @x402/core 커스텀 서버

`@x402/express`, `@x402/hono` 같은 사전 구축된 미들웨어 패키지를 사용하지 않고, x402 결제 처리를 수동으로 구현하는 방법을 시연합니다.

```typescript
import { x402ResourceServer, HTTPFacilitatorClient } from "@x402/core/server";
import { ExactEvmScheme } from "@x402/evm/exact/server";

const resourceServer = new x402ResourceServer(
  new HTTPFacilitatorClient({ url: facilitatorUrl }),
).register("eip155:84532", new ExactEvmScheme());

// 요청 핸들러 내부:
if (!paymentHeader) {
  const paymentRequired = resourceServer.createPaymentRequiredResponse([requirements], resource);
  res.status(402).set("PAYMENT-REQUIRED", encode(paymentRequired)).json({});
  return;
}

const paymentPayload = decode(paymentHeader);
const verifyResult = await resourceServer.verifyPayment(paymentPayload, requirements);
if (!verifyResult.isValid) return res.status(402).json({ error: verifyResult.invalidReason });

// 핸들러 실행 후 정산
const settleResult = await resourceServer.settlePayment(paymentPayload, requirements);
res.set("PAYMENT-RESPONSE", encode(settleResult));
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
cd servers/custom
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

## HTTP 헤더

### 요청 헤더

결제를 제출할 때 아래 헤더 중 하나를 포함합니다. (하위 호환을 위해 둘 다 지원)

| 헤더                | 프로토콜 | 설명                               |
| ------------------- | -------- | ---------------------------------- |
| `PAYMENT-SIGNATURE` | v2       | Base64 인코딩된 JSON 결제 페이로드 |
| `X-PAYMENT`         | v1       | Base64 인코딩된 JSON 결제 페이로드 |

결제 포함 요청 예시:

```
GET /weather HTTP/1.1
Host: localhost:4021
PAYMENT-SIGNATURE: eyJwYXltZW50IjoiLi4uIn0=
```

### 응답 헤더

| 헤더               | 상태코드 | 설명                                                 |
| ------------------ | -------- | ---------------------------------------------------- |
| `PAYMENT-REQUIRED` | 402      | 결제 요구 사항을 담은 Base64 인코딩 JSON             |
| `PAYMENT-RESPONSE` | 200      | 정산(settlement) 상세 정보를 담은 Base64 인코딩 JSON |

## 응답 포맷

### Payment Required (402)

```
HTTP/1.1 402 Payment Required
Content-Type: application/json; charset=utf-8
PAYMENT-REQUIRED: <base64-encoded JSON>

{"error":"Payment Required","message":"This endpoint requires payment"}
```

`PAYMENT-REQUIRED` 헤더에는 결제 요구 사항을 담은 base64 인코딩 JSON이 포함됩니다.

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

### 성공 응답(결제 포함)

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
PAYMENT-RESPONSE: <base64-encoded JSON>

{"city":"San Francisco","weather":"foggy","temperature":60,"timestamp":"2024-01-01T12:00:00.000Z"}
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

## 결제 플로우

커스텀 구현은 x402 결제 플로우의 각 단계를 명시적으로 보여줍니다.

1. **요청 도착** — 미들웨어가 모든 요청을 가로챔
2. **라우트 확인** — 라우트가 결제를 요구하는지 판단
3. **결제 확인** — `PAYMENT-SIGNATURE` 또는 `X-PAYMENT` 헤더 존재 여부 확인
4. **분기 처리**:
   - **결제 없음**: `PAYMENT-REQUIRED` 헤더에 요구 사항을 담아 402 반환
   - **결제 있음**: Facilitator를 통해 결제 검증
5. **검증(Verification)** — 결제 서명 및 유효성 확인
6. **핸들러 실행** — 보호된 엔드포인트 로직 실행
7. **정산(Settlement)** — 2xx 응답에 대해 온체인 정산 수행
8. **응답 반환** — `PAYMENT-RESPONSE` 헤더에 정산 결과 포함

## 주요 구현 상세

### 결제 요구 사항 정의

```typescript
const routeConfigs: Record<string, RoutePaymentConfig> = {
  "GET /weather": {
    scheme: "exact",
    price: "$0.001",
    network: "eip155:84532",
    payTo: evmAddress,
    description: "Weather data",
    mimeType: "application/json",
  },
};
```

### 결제 여부 확인

```typescript
const paymentHeader = (req.headers["payment-signature"] || req.headers["x-payment"]) as
  | string
  | undefined;

if (!paymentHeader) {
  const paymentRequired = resourceServer.createPaymentRequiredResponse([requirements], {
    url: `${req.protocol}://${req.get("host")}${req.originalUrl}`,
    description: routeConfig.description,
    mimeType: routeConfig.mimeType,
  });
  const requirementsHeader = Buffer.from(JSON.stringify(paymentRequired)).toString("base64");

  res.status(402);
  res.set("PAYMENT-REQUIRED", requirementsHeader);
  res.json({
    error: "Payment Required",
    message: "This endpoint requires payment",
  });
  return;
}
```

### 결제 검증

```typescript
const paymentPayload = JSON.parse(Buffer.from(paymentHeader, "base64").toString("utf-8"));
const verifyResult = await resourceServer.verifyPayment(paymentPayload, requirements);

if (!verifyResult.isValid) {
  res.status(402).json({
    error: "Invalid Payment",
    reason: verifyResult.invalidReason,
  });
  return;
}
```

### 결제 정산

```typescript
const settleResult = await resourceServer.settlePayment(paymentPayload, requirements);
const settlementHeader = Buffer.from(JSON.stringify(settleResult)).toString("base64");
res.set("PAYMENT-RESPONSE", settlementHeader);
```

## 미들웨어 vs 커스텀 구현 비교

| 항목        | 미들웨어 사용(@x402/express) | 커스텀 구현   |
| ----------- | ---------------------------- | ------------- |
| 코드 복잡도 | 약 10줄                      | 약 150줄      |
| 자동 검증   | ✅ 지원                       | ❌ 직접 구현   |
| 자동 정산   | ✅ 지원                       | ❌ 직접 구현   |
| 헤더 처리   | ✅ 자동                       | ❌ 직접 구현   |
| 유연성      | 제한적                       | ✅ 완전한 제어 |
| 에러 처리   | ✅ 내장                       | ❌ 직접 구현   |
| 유지보수    | x402 팀                      | 직접 유지보수 |

## 어떤 방식을 선택할까?

**미들웨어(@x402/express, @x402/hono)를 권장하는 경우**

- 일반적인 형태의 앱을 구축하는 경우
- 빠르게 통합하고 싶은 경우
- 결제 처리를 자동화하고 싶은 경우
- 지원되는 프레임워크(Express, Hono)를 사용하는 경우

**커스텀 구현을 권장하는 경우**

- 지원되지 않는 프레임워크(Koa, Fastify 등)를 사용하는 경우
- 결제 플로우를 완전히 제어해야 하는 경우
- 커스텀 에러 처리 요구가 있는 경우
- 내부 동작을 이해하고 싶은 경우
- 자체 추상화/프레임워크 통합 레이어를 만들고 싶은 경우

## 다른 프레임워크로의 적용

이 패턴을 다른 프레임워크에 적용하려면 다음 순서로 구현합니다.

1. 해당 프레임워크용 미들웨어 함수 작성
2. 라우트별 결제 요구 사항 확인
3. `x402ResourceServer`로 결제 verify/settle 수행
4. 응답을 가로채 정산 헤더를 추가

`index.ts`의 패턴은 어떤 Node.js 웹 프레임워크에도 그대로 응용할 수 있습니다.

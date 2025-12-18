# Custom x402 클라이언트 구현

이 예제는 `@x402/fetch`, `@x402/axios` 같은 편의 래퍼 없이, 코어 패키지만 사용해서 x402 결제 처리를 수동으로 구현하는 방법을 보여줍니다.


```typescript
import { x402Client } from "@x402/core/client";
import { decodePaymentRequiredHeader, encodePaymentSignatureHeader } from "@x402/core/http";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const client = new x402Client().register(
  "eip155:*",
  new ExactEvmScheme(privateKeyToAccount(evmPrivateKey)),
);

// 1. 최초 요청
let response = await fetch(url);

// 2. 402 Payment Required 처리
if (response.status === 402) {
  const paymentRequired = decodePaymentRequiredHeader(response.headers.get("PAYMENT-REQUIRED"));
  const paymentPayload = await client.createPaymentPayload(paymentRequired);

  // 3. 결제 헤더를 포함해 재요청
  response = await fetch(url, {
    headers: { "PAYMENT-SIGNATURE": encodePaymentSignatureHeader(paymentPayload) },
  });
}

console.log(await response.json());
```

## 사전 준비 사항

- Node.js v20 이상 (설치: [nvm](https://github.com/nvm-sh/nvm))
- pnpm v10 (설치: [pnpm.io/installation](https://pnpm.io/installation))
- V결제를 수행하기 위한 유효한 EVM 또는 SVM 개인키
- 실행 중인 x402 서버 (참고: [express 서버 예제](/external/x402/examples/typescript/servers/express/))

## 설정 방법

1. `.env-local`파일을 `.env`로 복사

```bash
cp .env-local .env
```

다음 환경 변수를 설정합니다.

- `EVM_PRIVATE_KEY` - EVM 결제를 위한 이더리움 개인키
- `SVM_PRIVATE_KEY` - SVM 결제를 위한 솔라나 개인키

2. 타입스크립트 예제 루트에서 전체 패키지 설치 및 빌드

```bash
cd ../../
pnpm install && pnpm build
cd clients/custom
```

3. 예제 실행

```bash
pnpm dev
```

## 예제 테스트 방법

먼저 서버를 실행합니다.

```bash
cd ../../servers/express
pnpm dev
```

그다음 커스텀 클라이언트를 실행합니다.

```bash
cd ../../clients/custom
pnpm dev
```

## HTTP 헤더 (v2 프로토콜)

| 헤더(Header)        | 방향(Direction) | 설명                                           |
| ------------------- | --------------- | ---------------------------------------------- |
| `PAYMENT-REQUIRED`  | Server → Client | 402 응답과 함께 전달되는 결제 요구 사항        |
| `PAYMENT-SIGNATURE` | Client → Server | 결제 페이로드를 포함해 재시도하는 요청 헤더    |
| `PAYMENT-RESPONSE`  | Server → Client | 200 응답과 함께 전달되는 정산(settlement) 정보 |

## 결제 흐름

1. **초기 요청** — 보호된 엔드포인트로 HTTP 요청 전송
2. **402 응답** — 서버가 `PAYMENT-REQUIRED` 헤더에 요구 사항을 담아 응답
3. **요구사항 파싱** — `decodePaymentRequiredHeader()`로 요구 사항 디코딩
4. **결제 생성** — `x402Client.createPaymentPayload()`로 결제 페이로드 생성
5. **결제 인코딩** — `encodePaymentSignatureHeader()`로 헤더 값 생성
6. **결제 포함 재시도** — `PAYMENT-SIGNATURE` 헤더를 붙여 재요청
7. **성공** — `PAYMENT-RESPONSE` 헤더에 정산 정보가 포함된 200 응답 수신

## 핵심 구현 포인트

### 1. 클라이언트 설정

```typescript
import { x402Client } from "@x402/core/client";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { ExactSvmScheme } from "@x402/svm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const evmSigner = privateKeyToAccount(evmPrivateKey);
const svmSigner = await createKeyPairSignerFromBytes(base58.decode(svmPrivateKey));

// 선택 사항: 어떤 결제 옵션을 사용할지 선택하는 커스텀 셀렉터
const selectPayment = (_version: number, requirements: PaymentRequirements[]) => {
  return requirements[1]; // 두 번째 옵션 선택 (예: 솔라나)
};

const client = new x402Client(selectPayment)
  .register("eip155:*", new ExactEvmScheme(evmSigner))
  .register("solana:*", new ExactSvmScheme(svmSigner));
```

### 2. Payment Required 감지

```typescript
import { decodePaymentRequiredHeader } from "@x402/core/http";

if (response.status === 402) {
  const paymentRequiredHeader = response.headers.get("PAYMENT-REQUIRED");
  const paymentRequired = decodePaymentRequiredHeader(paymentRequiredHeader);
  // paymentRequired.accepts에 결제 옵션들이 포함됩니다.
}
```

### 3. 결제 페이로드 생성

```typescript
import { encodePaymentSignatureHeader } from "@x402/core/http";

const paymentPayload = await client.createPaymentPayload(paymentRequired);
const paymentHeader = encodePaymentSignatureHeader(paymentPayload);
```

### 4. 결제 포함 재요청

```typescript
const response = await fetch(url, {
  headers: {
    "PAYMENT-SIGNATURE": paymentHeader,
  },
});
```

### 5. 정산(Settlement) 정보 추출

```typescript
import { decodePaymentResponseHeader } from "@x402/core/http";

const settlementHeader = response.headers.get("PAYMENT-RESPONSE");
const settlement = decodePaymentResponseHeader(settlementHeader);
// settlement.transaction, settlement.network, settlement.payer
```

## 래퍼 사용 vs 커스텀 구현 비교

| 항목        | 레퍼 사용 (@x402/fetch) | 커스텀 구현        |
| ----------- | ----------------------- | ------------------ |
| 코드 복잡도 | 약 10줄                 | 약 100줄           |
| 자동 재시도 | ✅ 지원                  | ❌ 직접 구현        |
| 에러 처리   | ✅ 내장                  | ❌ 직접 구현        |
| 헤더 관리   | ✅ 자동                  | ❌ 직접 구현        |
| 유연성      | 제한적                  | ✅ 완전한 제어 가능 |

## 커스텀 구현을 사용해야 하는 경우

- 결제 플로우의 모든 단계를 완전히 제어해야 하는 경우
- 표준적이지 않은 HTTP 라이브러리와 통합해야 하는 경우
- 커스텀 재시도/에러 처리 로직을 구현해야 하는 경우
- x402가 내부적으로 어떻게 동작하는지 학습하고 싶은 경우

## 다른 HTTP 클라이언트로 확장하기

이 패턴을 다른 HTTP 클라이언트(axios, got 등)에 적용하려면 다음 순서를 따르면 됩니다.

1. 402 상태 코드를 감지
2. `PAYMENT-REQUIRED` 헤더에서 요구 사항 추출
3. `decodePaymentRequiredHeader()`로 파싱
4. `x402Client.createPaymentPayload()`로 페이로드 생성
5. `encodePaymentSignatureHeader()`로 헤더 값 인코딩
6. `PAYMENT-SIGNATURE` 헤더를 추가해 요청 재시도
7. `PAYMENT-RESPONSE` 헤더에서 정산 정보 추출

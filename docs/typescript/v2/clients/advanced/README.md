[한국어](./README.md) | [English](./README.en.md)

# 고급 x402 클라이언트 예제

빌더 패턴 기반 등록, 결제 라이프사이클 훅, 네트워크 선호도 설정과 같은 x402 타입스크립트 클라이언트의 고급 기능들을 구현하는 예제입니다.

```typescript
import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const client = new x402Client()
  .register("eip155:*", new ExactEvmScheme(privateKeyToAccount(evmPrivateKey)))
  .onBeforePaymentCreation(async ctx => {
    console.log("Creating payment for:", ctx.selectedRequirements.network);
  })
  .onAfterPaymentCreation(async ctx => {
    console.log("Payment created:", ctx.paymentPayload.x402Version);
  });

const fetchWithPayment = wrapFetchWithPayment(fetch, client);
const response = await fetchWithPayment("http://localhost:4021/weather");
```

## 사전 준비 사항

- Node.js v20 이상 (설치: [nvm](https://github.com/nvm-sh/nvm))
- pnpm v10 (설치: [pnpm.io/installation](https://pnpm.io/installation))
- 결제를 수행하기 위한 유효한 EVM 또는 SVM 개인키
- 실행 중인 x402 서버 (참고: express 서버 예제 [📂 로컬](../../../../external/x402/examples/typescript/servers/express/) | [🔗 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/express))
- [기본 fetch 클라이언트](./ts-clients-fetch.ko.md) 예제에 대한 이해

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
cd clients/advanced
```

3. 예제 실행

```bash
pnpm dev
```

## 사용 가능한 예제

각 예제는 특정 고급 패턴을 중심으로 구성되어 있습니다.

| 예제                | 실행 명령                    | 설명                          |
| ------------------- | ---------------------------- | ----------------------------- |
| `builder-pattern`   | `pnpm dev:builder-pattern`   | SVM 결제를 위한 솔라나 개인키 |
| `hooks`             | `pnpm dev:hooks`             | 결제 라이프사이클 훅          |
| `preferred-network` | `pnpm dev:preferred-network` | 클라이언트 측 네트워크 선호도 |

## 예제 테스트 방법

먼저 서버를 실행합니다.

```bash
cd ../../servers/express
pnpm dev
```

그런 다음 예제를 실행합니다.

```bash
cd ../../clients/advanced
pnpm dev:builder-pattern
```

## 예제: 빌더 패턴 기반 등록

빌더 패턴을 사용하면 어떤 네트워크를 지원할지, 어떤 서명자를 사용할지를 세밀하게 제어할 수 있습니다.

```typescript
import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { ExactSvmScheme } from "@x402/svm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const evmSigner = privateKeyToAccount(evmPrivateKey);
const mainnetSigner = privateKeyToAccount(mainnetPrivateKey);

// 더 구체적인 패턴이 와일드카드보다 먼저 적용됩니다.
const client = new x402Client()
  .register("eip155:*", new ExactEvmScheme(evmSigner)) // 모든 EVM 네트워크
  .register("eip155:1", new ExactEvmScheme(mainnetSigner)) // 이더리움 메인넷 오버라이드
  .register("solana:*", new ExactSvmScheme(svmSigner)); // 모든 솔라나 네트워크

const fetchWithPayment = wrapFetchWithPayment(fetch, client);
const response = await fetchWithPayment("http://localhost:4021/weather");
```

**유스케이스**

- 메인넷과 테스트넷에 서로 다른 서명자(signer) 사용
- 네트워크별 키 분리
- 지원 네트워크에 대한 명시적 제어

## 결제: 결제 라이프사이클 훅

결제 단계별로 사용자 정의 로직을 등록하여 관측성(observability) 및 제어 기능을 강화할 수 있습니다.

```typescript
import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const signer = privateKeyToAccount(process.env.EVM_PRIVATE_KEY);

const client = new x402Client()
  .register("eip155:*", new ExactEvmScheme(signer))
  .onBeforePaymentCreation(async context => {
    console.log("Creating payment for:", context.selectedRequirements);
    // 결제를 중단하려면: { abort: true, reason: "Not allowed" }
  })
  .onAfterPaymentCreation(async context => {
    console.log("Payment created:", context.paymentPayload.x402Version);
    // 분석 시스템, DB 등으로 전송 가능
  })
  .onPaymentCreationFailure(async context => {
    console.error("Payment failed:", context.error);
    // 복구 시: { recovered: true, payload: alternativePayload }
  });

const fetchWithPayment = wrapFetchWithPayment(fetch, client);
const response = await fetchWithPayment("http://localhost:4021/weather");
```

사용 가능한 훅:

- `onBeforePaymentCreation` — 결제 생성 전 실행 (중단 가능)
- `onAfterPaymentCreation` — 결제 성공 후 실행
- `onPaymentCreationFailure` — 결제 실패 시 실행 (복구 가능)

**유스케이스**

- 결제 이벤트 로깅 및 모니터링
- 결제 허용 전 사용자 정의 검증
- 실패한 결제에 대한 재시도 및 복구 로직
- 매트릭(Metrics) 및 분석 데이터 수집

## 예제: 선호 네트워크 선택

자동화된 폴백(fallback)과 함께 클라이언트 측에서 네트워크 선호도를 설정할 수 있습니다.

```typescript
import { x402Client, wrapFetchWithPayment, type PaymentRequirements } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { ExactSvmScheme } from "@x402/svm/exact/client";

// 네트워크 선호 순서 (우선순위가 높은 순)
const networkPreferences = ["solana:", "eip155:"];

const preferredNetworkSelector = (
  _x402Version: number,
  options: PaymentRequirements[],
): PaymentRequirements => {
  // 정렬된 각 선호도를 시도
  for (const preference of networkPreferences) {
    const match = options.find(opt => opt.network.startsWith(preference));
    if (match) return match;
  }
  // 공통적으로 지원되는 첫번째 옵션으로 fallback
  return options[0];
};

const client = new x402Client(preferredNetworkSelector)
  .register("eip155:*", new ExactEvmScheme(evmSigner))
  .register("solana:*", new ExactSvmScheme(svmSigner));

const fetchWithPayment = wrapFetchWithPayment(fetch, client);
const response = await fetchWithPayment("http://localhost:4021/weather");
```

**유스케이스**

- 특정 체인을 우선적으로 사용하고 싶은 경우
- 지갑 UI에서 사용자 선호 네트워크 설정 반영

## 훅(hooks) 사용 시 권장 사항

1. **훅은 빠르게 실행** — 블로킹(blocking) 작업은 피할 것
2. **에러는 우아하게(graceful)하게 처리** — 훅 내부에서 예외를 throw 하지 말 것
3. **적절한 로그 남기기** — 구조화된 로그 사용
4. **before 훅에서 사이드 이펙트 최소화** — 검증 용도로만 사용

---

[← 클라이언트 목록](../README.md) | [v2 문서 →](../../README.md)

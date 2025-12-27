[한국어](./README.md) | [English](./README.en.md)

# x402 Facilitator 예제

x402 프로토콜에서 온체인 결제의 검증(verify)과 정산(settle) 을 수행하는 Express.js 기반 Facilitator 서비스 예제입니다.

## 사전 준비 사항

- Node.js v20 이상 (설치: [nvm](https://github.com/nvm-sh/nvm))
- pnpm v10 (설치: [pnpm.io/installation](https://pnpm.io/installation))
- 트랜잭션 수수료를 위한 Base Sepolia ETH를 보유한 EVM 개인 키
- 트랜잭션 수수료를 위한 Solana Devnet SOL을 보유한 SVM 개인 키

## 설정 방법

1. `.env-local`파일을 `.env`로 복사

```bash
cp .env-local .env
```

다음 환경 변수를 설정합니다.

- `EVM_PRIVATE_KEY` - EVM 결제를 위한 이더리움 개인키
- `SVM_PRIVATE_KEY` - SVM 결제를 위한 솔라나 개인키
- `PORT` - 서버 포트(port) (선택적, 기본 값은 4022)

2. 타입스크립트 예제 루트에서 전체 패키지 설치 및 빌드

```bash
cd ../../
pnpm install && pnpm build
cd facilitator
```

3. 서버 실행

```bash
pnpm dev
```

## API 엔드포인트

### GET /supported

이 Facilitator가 지원하는 결제 스키마(scheme) 및 네트워크(network) 목록을 반환합니다.

```json
{
  "kinds": [
    {
      "x402Version": 2,
      "scheme": "exact",
      "network": "eip155:84532"
    },
    {
      "x402Version": 2,
      "scheme": "exact",
      "network": "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1",
      "extra": {
        "feePayer": "..."
      }
    }
  ],
  "extensions": [],
  "signers": {
    "eip155": ["0x..."],
    "solana": ["..."]
  }
}
```

### POST /verify

정산(settlement) 수행 전에, 결제 페이로드가 요구 조건을 충족하는지 사전 검증합니다.

요청(Request):

```json
{
  "paymentPayload": {
    "x402Version": 2,
    "resource": {
      "url": "http://localhost:4021/weather",
      "description": "Weather data",
      "mimeType": "application/json"
    },
    "accepted": {
      "scheme": "exact",
      "network": "eip155:84532",
      "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
      "amount": "1000",
      "payTo": "0x...",
      "maxTimeoutSeconds": 300,
      "extra": {
        "name": "USDC",
        "version": "2"
      }
    },
    "payload": {
      "signature": "0x...",
      "authorization": {}
    }
  },
  "paymentRequirements": {
    "scheme": "exact",
    "network": "eip155:84532",
    "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
    "amount": "1000",
    "payTo": "0x...",
    "maxTimeoutSeconds": 300,
    "extra": {
      "name": "USDC",
      "version": "2"
    }
  }
}
```

응답(Response) - 성공:

```json
{
  "isValid": true,
  "payer": "0x..."
}
```

응답(Response) — 실패:

```json
{
  "isValid": false,
  "invalidReason": "invalid_signature"
}
```

### POST /settle

검증된 결제를 실제로 온체인에 브로드캐스트하여 정산(settlement)을 수행합니다.

요청 바디(body)는 `/verify`와 동일합니다.

응답(Response) — 성공:

```json
{
  "success": true,
  "transaction": "0x...",
  "network": "eip155:84532",
  "payer": "0x..."
}
```

응답(Response) — 실패:

```json
{
  "success": false,
  "errorReason": "insufficient_balance",
  "transaction": "",
  "network": "eip155:84532"
}
```

## 예제 확장하기

### 네트워크 추가

다른 네트워크에 대한 스키마를 추가로 등록할 수 있습니다.

```typescript
import { registerExactEvmScheme } from "@x402/evm/exact/facilitator";
import { registerExactSvmScheme } from "@x402/svm/exact/facilitator";

const facilitator = new x402Facilitator();

registerExactEvmScheme(facilitator, {
  signer: evmSigner,
  networks: "eip155:84532",
});

registerExactSvmScheme(facilitator, {
  signer: svmSigner,
  networks: "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1",
});
```

### 라이프사이클 훅

verify/settle 전후에 커스텀 로직을 추가할 수 있습니다.

```typescript
const facilitator = new x402Facilitator()
  .onBeforeVerify(async (context) => {
    // 검증 전 로깅 또는 검증 로직
  })
  .onAfterVerify(async (context) => {
    // 검증된 결제 추적
  })
  .onVerifyFailure(async (context) => {
    // 검증 실패 처리
  })
  .onBeforeSettle(async (context) => {
    // 정산 전 검증 로직
    // { abort: true, reason: "..." }를 반환하면 취소 가능
  })
  .onAfterSettle(async (context) => {
    // 성공한 결제 추적
  })
  .onSettleFailure(async (context) => {
    // 정산 실패 처리
  });
```

## 네트워크 식별자

네트워크는 [CAIP-2](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md) 형식을 사용합니다.

- `eip155:84532` — Base Sepolia
- `eip155:8453` — Base Mainnet
- `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` — Solana Devnet
- `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` — Solana Mainnet

---

[← v2 문서로 돌아가기](../README.md)

[한국어](./README.md) | [English](./README.en.md)

# @x402/axios 클라이언트 예제

이 예제는 x402 결제 프로토콜로 보호된 엔드포인트에 HTTP 요청을 보내기 위해 `@x402/axios`를 사용하는 방법을 보여주는 클라이언트 예제입니다.

```typescript
import { x402Client, wrapAxiosWithPayment } from "@x402/axios";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";
import axios from "axios";

const client = new x402Client();
registerExactEvmScheme(client, { signer: privateKeyToAccount(process.env.EVM_PRIVATE_KEY) });

const api = wrapAxiosWithPayment(axios.create(), client);

const response = await api.get("http://localhost:4021/weather");
console.log(response.data);
```

## 사전 준비 사항

- Node.js v20 이상 (설치: [nvm](https://github.com/nvm-sh/nvm))
- pnpm v10 (설치: [pnpm.io/installation](https://pnpm.io/installation))
- 실행 중인 x402 서버 (참고: [express 서버 예제](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/express))
- 결제를 수행하기 위한 유효한 EVM 또는 SVM 개인키

## 설정 방법

1. 타입스크립트 예제 루트 경로에서 전체 패키지 설치 및 빌드

```bash
cd ../../
pnpm install && pnpm build
cd clients/axios
```

2. `.env-local`파일을 `.env`로 복사하고 개인키 추가

```bash
cp .env-local .env
```

필수적인 환경 변수는 다음과 같습니다.

- `EVM_PRIVATE_KEY` - EVM 결제를 위한 이더리움 개인키
- `SVM_PRIVATE_KEY` - SVM 결제를 위한 솔라나 개인키

3. 클라이언트 실행

```bash
pnpm start
```

## 다음 단계

빌더 패턴 기반 등록, 결제 라이프사이클 훅, 네트워크 선호도 설정에 대해서는 [고급 예제](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/advanced)를 참고하세요.

---

[← 클라이언트 목록](../README.md) | [v2 문서 →](../../README.md)

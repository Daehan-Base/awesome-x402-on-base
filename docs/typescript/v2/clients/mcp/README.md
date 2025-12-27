[한국어](./README.md) | [English](./README.en.md)

# x402 MCP 클라이언트 예제

이 예제는 Model Context Protocol(MCP) 과 x402 결제 프로토콜(v2) 을 함께 사용하여, MCP 서버를 통해 유료 API 요청을 수행하는 방법을 보여주는 클라이언트 예제입니다.

## 사전 준비 사항

- Node.js v20 이상 (설치: [nvm](https://github.com/nvm-sh/nvm))
- pnpm v10 (설치: [pnpm.io/installation](https://pnpm.io/installation))
- 실행 중인 x402서버 (`examples/typescript/servers/express` 예제 서버를 사용할 수 있음)
- 결제를 수행하기 위한 유효한 이더리움 및 솔라나 개인 키
- MCP를 지원하는 Claude 데스크탑 앱

## 설정 방법

1. 타입스크립트 예제 루트 경로에서 전체 패키지 설치 및 빌드
```bash
cd ../../
pnpm install
pnpm build
cd clients/mcp
```

2. Claude 데스크탑의 MCP 설정 구성
```json
{
  "mcpServers": {
    "demo": {
      "command": "pnpm",
      "args": [
        "--silent",
        "-C",
        "<absolute path to this repo>/examples/typescript/clients/mcp",
        "dev"
      ],
      "env": {
        "EVM_PRIVATE_KEY": "<Base Sepolia에서 USDC를 보유한 지갑의 private key>",
        "SVM_PRIVATE_KEY": "<Devnet에서 USDC를 보유한 Solana 지갑의 base58 인코딩 private key>",
        "RESOURCE_SERVER_URL": "http://localhost:4021",
        "ENDPOINT_PATH": "/weather"
      }
    }
  }
}
```

3. `RESOURCE_SERVER_URL`에 지정한 주소에서 x402 서버가 실행 중인지 확인 (예: express 서버 예시 `examples/typescript/servers/express`)

4. 새로운 MCP 서버로 Claude 데스크탑 재시작 

5. Claude에게 `get-data-from-resource-server` 도구(tool) 사용 요청

## 동작 방식

이 예제는 다음을 시연합니다.
1. EVM과 SVM 스키마를 지원하는 x402 클라이언트 생성
2. `@x402/evm`과 `@x402/svm`를 사용하여 결제 스키마 등록
3. x402 결제 처리를 포함한 MCP 서버 구성
4. 유료 API 요청을 수행하는 도구 생성
5. MCP 프로토콜을 통해 응답 및 오류 처리

## 예제 코드

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import axios from "axios";
import { x402Client, wrapAxiosWithPayment } from "@x402/axios";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { registerExactSvmScheme } from "@x402/svm/exact/client";
import { privateKeyToAccount } from "viem/accounts";
import { createKeyPairSignerFromBytes } from "@solana/kit";
import { base58 } from "@scure/base";

// 결제 스키마를 포함한 x402 클라이언트 생성
const client = new x402Client();

// EVM 결제 스키마 등록
const evmSigner = privateKeyToAccount(EVM_PRIVATE_KEY);
registerExactEvmScheme(client, { signer: evmSigner });

// SVM 결제 스키마 등록
const svmSigner = await createKeyPairSignerFromBytes(base58.decode(SVM_PRIVATE_KEY));
registerExactSvmScheme(client, { signer: svmSigner });

// 결제 처리가 포함된 Axios 인스턴스 생성
const api = wrapAxiosWithPayment(axios.create({ baseURL: RESOURCE_SERVER_URL }), client);

// MCP 서버 생성
const server = new McpServer({
  name: "x402 MCP Client Demo",
  version: "2.0.0",
});

// 유료 요청을 수행하는 도구 추가
server.tool(
  "get-data-from-resource-server",
  "Get data from the resource server (in this example, the weather)",
  {},
  async () => {
    const res = await api.get(ENDPOINT_PATH);
    return {
      content: [{ type: "text", text: JSON.stringify(res.data) }],
    };
  },
);

// MCP transport 연결
const transport = new StdioServerTransport();
await server.connect(transport);
```

## 응답 처리

### Payment Required (402)
결제가 필요한 경우 x402는 다음 과정을 자동으로 수행합니다.
1. 402 응답 수신
2. 결제 요구사항 파싱
3. 적절한 스키마(EVM 또는 SVM)를 사용해 결제 헤더 생성 및 서명
4. 결제 헤더를 포함하여 요청 자동 재시도

### 성공 응답
결제가 처리되면, MCP 서버는 MCP 프로토콜을 통해 응답 데이터를 반환합니다.
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"report\":{\"weather\":\"sunny\",\"temperature\":70}}"
    }
  ]
}
```
## Claude 데스크탑과 통합

이 예제는 Claude 데스크탑의 MCP 지원과 함께 동작하도록 설계되었습니다. MCP 서버는 다음을 수행합니다.
1. Claude로부터 도구(tool) 요청을 수신
2. x402 v2 프로토콜을 사용해 결제 과정을 자동 처리
3. MCP 프로토콜을 통해 응답 데이터를 반환
4. Claude가 결과를 처리하고 표시할 수 있도록 지원

---

[← 클라이언트 목록](../README.md) | [v2 문서 →](../../README.md)

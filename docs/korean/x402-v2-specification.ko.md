# x402 v2 프로토콜 명세서

> **작성 시점**: 2025년 12월 16일
> **버전**: x402 v2 (2025년 12월 11일 출시)
>
> 이 문서는 x402 v2 프로토콜의 핵심 기능과 변경사항을 한국어로 요약한 것입니다. 전체 명세서는 [공식 x402 저장소](https://github.com/coinbase/x402/tree/main/specs)를 참고하세요.
>
> **v2 출시 발표**: [x402-v2-launch](https://x402.org/writing/x402-v2-launch)

---

## 📋 목차

- [v2 주요 변경사항](#v2-주요-변경사항)
- [HTTP v2 트랜스포트](#http-v2-트랜스포트)
- [MCP 트랜스포트 (AI 에이전트)](#mcp-트랜스포트-ai-에이전트)
- [A2A 트랜스포트 (에이전트간)](#a2a-트랜스포트-에이전트간)
- [결제 방식 (Schemes)](#결제-방식-schemes)
- [Facilitator API](#facilitator-api)
- [Discovery API (Bazaar)](#discovery-api-bazaar)
- [다중 체인 지원](#다중-체인-지원)
- [보안 강화](#보안-강화)
- [세션 관리](#세션-관리)
- [에러 처리](#에러-처리)
- [v1 Legacy 문서](#v1-legacy-문서)
- [향상된 예제](#향상된-예제)

---

## v2 주요 변경사항

### 🔄 핵심 아키텍처 변경

**v1 → v2 주요 차이점:**

| 구분 | v1 | v2 |
|------|-----|-----|
| **HTTP 헤더** | `X-PAYMENT`, `X-PAYMENT-RESPONSE` | `PAYMENT-SIGNATURE`, `PAYMENT-RESPONSE`, `PAYMENT-REQUIRED` |
| **데이터 형식** | Base64 인코딩 | Base64 인코딩 (동일) |
| **체인 지원** | 단일 체인 | 다중 체인 (CAIP 표준) |
| **플러그인** | 단일 SDK | 모듈형 플러그인 아키텍처 |
| **세션** | 없음 | 지갑 기반 세션 지원 |
| **확장성** | 제한적 | 완전 확장 가능 |

### 🌟 v2 신기능

1. **다중 체인 지원** - Base, Solana, EVM 호환 체인 (CAIP 표준)
2. **다중 Transport** - HTTP, MCP (AI 에이전트), A2A (에이전트간)
3. **향상된 보안** - ERC1271, ERC6492 지원
4. **세션 관리** - 지갑 기반 재사용 액세스 (`@x402/paywall`)
5. **플러그인 아키텍처** - 독립적인 체인/결제 방식 확장
6. **동적 라우팅** - 요청별 `payTo` 수신자 지정
7. **자동 API 발견** - Bazaar/Discovery API

---

## HTTP v2 트랜스포트

### 결제 요구 신호

서버는 HTTP 402 상태 코드와 `PAYMENT-REQUIRED` 헤더로 결제를 요구합니다.

**형식**: Base64로 인코딩된 `PaymentRequired` 객체

**예시:**
```http
HTTP/1.1 402 Payment Required
Content-Type: application/json
PAYMENT-REQUIRED: eyJ4NDAyVmVyc2lvbiI6MiwiZXJyb3IiOiJQQVlNRU5ULVNJR05BVFVSRSBoZWFkZXIgaXMgcmVxdWlyZWQiLCJyZXNvdXJjZSI6eyJ1cmwiOiJodHRwczovL2FwaS5leGFtcGxlLmNvbS9wcmVtaXVtLWRhdGEiLCJkZXNjcmlwdGlvbiI6IkFjY2VzcyB0byBwcmVtaXVtIG1hcmtldCBkYXRhIiwibWltZVR5cGUiOiJhcHBsaWNhdGlvbi9qc29uIn0sImFjY2VwdHMiOlt7InNjaGVtZSI6ImV4YWN0IiwibmV0d29yayI6ImVpcDE1NTo4NDUzMiIsImFtb3VudCI6IjEwMDAwIiwiYXNzZXQiOiIweDAzNkNiRDUzODQyYzU0MjY2MzRlNzkyOTU0MWVDMjMxOGYzZENGN2UiLCJwYXlUbyI6IjB4MjA5NjkzQmM2YWZjMEM1MzI4YkEzNkZhRjAzQzUxNEVGMzEyMjg3QyIsIm1heFRpbWVvdXRTZWNvbmRzIjo2MCwiZXh0cmEiOnsibmFtZSI6IlVTREMIsInZlcnNpb24iOiIyIn19XX0=

{
  "error": "Payment required"
}
```

**디코딩된 내용:**
```json
{
  "x402Version": 2,
  "error": "PAYMENT-SIGNATURE header is required",
  "resource": {
    "url": "https://api.example.com/premium-data",
    "description": "Access to premium market data",
    "mimeType": "application/json"
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:84532",
      "amount": "10000",
      "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
      "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
      "maxTimeoutSeconds": 60,
      "extra": {
        "name": "USDC",
        "version": "2"
      }
    }
  ]
}
```

### 결제 페이로드 전송

클라이언트는 `PAYMENT-SIGNATURE` 헤더로 결제 데이터를 전송합니다.

**형식**: Base64로 인코딩된 `PaymentPayload` 객체

**예시:**
```http
POST /premium-data HTTP/1.1
Host: api.example.com
PAYMENT-SIGNATURE: eyJ4NDAyVmVyc2lvbiI6MiwicmVzb3VyY2UiOnsidXJsIjoiaHR0cHM6Ly9hcGkuZXhhbXBsZS5jb20vcHJlbWl1bS1kYXRhIiwiZGVzY3JpcHRpb24iOiJBY2Nlc3MgdG8gcHJlbWl1bSBtYXJrZXQgZGF0YSIsIm1pbWVUeXBlIjoiYXBwbGljYXRpb24vanNvbiJ9LCJhY2NlcHRlZCI6eyJzY2hlbWUiOiJleGFjdCIsIm5ldHdvcmsiOiJlaXAxNTU6ODQ1MzIiLCJhbW91bnQiOiIxMDAwMCIsImFzc2V0IjoiMHgwMzZDYkQ1Mzg0MmM1NDI2NjM0ZTc5Mjk1NDFlQzIzMThmM2RDRjdlIiwicGF5VG8iOiIweDIwOTY5M0JjNmFmYzBDNTMyOGJBMzZGYUYwM0M1MTRFRjMxMjI4N0MiLCJtYXhUaW1lb3V0U2Vjb25kcyI6NjAsImV4dHJhIjp7Im5hbWUiOiJVU0RDIiwidmVyc2lvbiI6IjIifX0sInBheWxvYWQiOnsic2lnbmF0dXJlIjoiMHgyZDZhNzU4OGQ2YWNjYTUwNWNiZjBkOWE0YTIyN2UwYzUyYzZjMzQwMDhjOGU4OTg2YTEyODMyNTk3NjQxNzM2MDhhMmNlNjQ5NjY0MmUzNzdkNmRhOGRiYmY1ODM2ZTliZDE1MDkyZjllY2FiMDVkZWQzZDYyOTNhZjE0OGI1NzFjIiwiYXV0aG9yaXphdGlvbiI6eyJmcm9tIjoiMHg4NTdiMDY1MTlFOTFlM0E1NDUzODc5MWJEYmIwRTIyMzczZTM2YjY2IiwidG8iOiIweDIwOTY5M0JjNmFmYzBDNTMyOGJBMzZGYUYwM0M1MTRFRjMxMjI4N0MiLCJ2YWx1ZSI6IjEwMDAwIiwidmFsaWRBZnRlciI6IjE3NDA2NzIwODkiLCJ2YWxpZEJlZm9yZSI6IjE3NDA2NzIxNTQiLCJub25jZSI6IjB4ZjM3NDY2MTNjMmQ5MjBiNWZkYWJjMDg1NmYyYWViMmQ0Zjg4ZWU2MDM3YjhjYzVkMDRhNzFhNDQ2MmYxMzQ4MCJ9fX0=
Content-Type: application/json

{
  "query": "latest market data"
}
```

**디코딩된 내용:**
```json
{
  "x402Version": 2,
  "resource": {
    "url": "https://api.example.com/premium-data",
    "description": "Access to premium market data",
    "mimeType": "application/json"
  },
  "accepted": {
    "scheme": "exact",
    "network": "eip155:84532",
    "amount": "10000",
    "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
    "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
    "maxTimeoutSeconds": 60,
    "extra": {
      "name": "USDC",
      "version": "2"
    }
  },
  "payload": {
    "signature": "0x2d6a7588d6acca505cbf0d9a4a227e0c52c6c34008c8e8986a1283259764173608a2ce6496642e377d6da8dbbf5836e9bd15092f9ecab05ded3d6293af148b571c",
    "authorization": {
      "from": "0x857b06519E91e3A54538791bDbb0E22373e36b66",
      "to": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
      "value": "10000",
      "validAfter": "1740672089",
      "validBefore": "1740672154",
      "nonce": "0xf3746613c2d920b5fdabc0856f2aeb2d4f88ee6037b8cc5d04a71a4462f13480"
    }
  }
}
```

#### 주요 필드 설명

| 필드 | 설명 |
|------|------|
| `from` | 결제자 지갑 주소 (클라이언트) |
| `to` | 결제 수신자 주소 (서버) |
| `value` | 결제 금액 (토큰 최소 단위, USDC의 경우 10000 = $0.01) |
| `validAfter` | 결제 유효 시작 시간 (Unix 타임스탬프) |
| `validBefore` | 결제 만료 시간 (Unix 타임스탬프) |
| `nonce` | 리플레이 방지용 고유 식별자 (한 번만 사용 가능) |
| `signature` | EIP-3009 서명 (transferWithAuthorization용) |

> **EIP-3009**: `transferWithAuthorization`을 통해 토큰 소유자가 직접 트랜잭션을 보내지 않고, 서명만으로 토큰 전송을 승인할 수 있는 표준입니다. 이를 통해 가스리스(gasless) 결제가 가능합니다.

### 정산 응답 전송

서버는 `PAYMENT-RESPONSE` 헤더로 결제 정산 결과를 전달합니다.

**성공 예시:**
```http
HTTP/1.1 200 OK
Content-Type: application/json
PAYMENT-RESPONSE: eyJzdWNjZXNzIjp0cnVlLCJ0cmFuc2FjdGlvbiI6IjB4MTIzNDU2Nzg5MGFiY2RlZjEyMzQ1Njc4OTBhYmNkZWYxMjM0NTY3ODkwYWJjZGVmMTIzNDU2Nzg5MGFiY2RlZiIsIm5ldHdvcmsiOiJlaXAxNTU6ODQ1MzIiLCJwYXllciI6IjB4ODU3YjA2NTE5RTkxZTNBNTQ1Mzg3OTFiRGJiMEUyMjM3M2UzNmI2NiJ9

{
  "data": "premium market data response",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**실패 예시:**
```http
HTTP/1.1 402 Payment Required
Content-Type: application/json
PAYMENT-RESPONSE: eyJzdWNjZXNzIjpmYWxzZSwiZXJyb3JSZWFzb24iOiJpbnN1ZmZpY2llbnRfZnVuZHMiLCJ0cmFuc2FjdGlvbiI6IiIsIm5ldHdvcmsiOiJlaXAxNTU6ODQ1MzIiLCJwYXllciI6IjB4ODU3YjA2NTE5RTkxZTNBNTQ1Mzg3OTFiRGJiMEUyMjM3M2UzNmI2NiJ9

{
  "x402Version": 2,
  "error": "Payment failed: insufficient funds",
  "accepts": [...]
}
```

---

## MCP 트랜스포트 (AI 에이전트)

MCP (Model Context Protocol) 트랜스포트는 AI 에이전트와 MCP 클라이언트가 도구 및 리소스에 대해 결제할 수 있도록 합니다.

### 결제 요구 신호

서버는 JSON-RPC 에러 응답으로 결제를 요구합니다.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": 402,
    "message": "Payment required",
    "data": {
      "x402Version": 2,
      "error": "Payment required to access this resource",
      "accepts": [
        {
          "scheme": "exact",
          "network": "eip155:84532",
          "amount": "10000",
          "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
          "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
          "resource": "mcp://tool/financial_analysis",
          "description": "Advanced financial analysis tool"
        }
      ]
    }
  }
}
```

### 결제 페이로드 전송

클라이언트는 `_meta["x402/payment"]` 필드로 결제 데이터를 전송합니다.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "financial_analysis",
    "arguments": { "ticker": "AAPL" },
    "_meta": {
      "x402/payment": {
        "x402Version": 2,
        "scheme": "exact",
        "network": "eip155:84532",
        "payload": {
          "signature": "0x...",
          "authorization": {
            "from": "0x...",
            "to": "0x...",
            "value": "10000",
            "validAfter": "1740672089",
            "validBefore": "1740672154",
            "nonce": "0x..."
          }
        }
      }
    }
  }
}
```

### 정산 응답

서버는 `_meta["x402/payment-response"]` 필드로 결과를 반환합니다.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{ "type": "text", "text": "Analysis result..." }],
    "_meta": {
      "x402/payment-response": {
        "success": true,
        "transaction": "0x1234...",
        "network": "eip155:84532",
        "payer": "0x857b..."
      }
    }
  }
}
```

---

## A2A 트랜스포트 (에이전트간)

A2A (Agent-to-Agent) 트랜스포트는 에이전트간 직접 결제를 가능하게 합니다.

### 결제 상태 라이프사이클

```
payment-required → payment-submitted → payment-verified → payment-completed
                                    ↘ payment-failed
```

| 상태 | 설명 |
|------|------|
| `payment-required` | 결제 필요 |
| `payment-rejected` | 결제 거부됨 |
| `payment-submitted` | 결제 제출됨 |
| `payment-verified` | 결제 검증됨 |
| `payment-completed` | 결제 완료 |
| `payment-failed` | 결제 실패 |

### 메타데이터 필드

```json
{
  "x402.payment.status": "payment-required",
  "x402.payment.required": {
    "x402Version": 2,
    "accepts": [...]
  },
  "x402.payment.payload": { ... },
  "x402.payment.receipts": [
    {
      "success": true,
      "transaction": "0x...",
      "network": "eip155:84532"
    }
  ]
}
```

### AgentCard 확장 선언

에이전트는 x402 기능을 AgentCard에 선언해야 합니다:

```json
{
  "name": "PaidAgent",
  "extensions": {
    "x402": {
      "version": 2,
      "networks": ["eip155:84532", "eip155:8453"]
    }
  }
}
```

---

## 결제 방식 (Schemes)

### 1. Exact 방식 (현재)

- **설명**: 정확한 금액 지불 (예: $1로 기사 읽기)
- **특징**: 즉시 정산, 정확한 금액
- **사용 사례**: 콘텐츠 액세스, API 호출

**요청 형식:**
```json
{
  "scheme": "exact",
  "network": "eip155:84532",
  "amount": "10000",
  "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
  "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
  "maxTimeoutSeconds": 60
}
```

### 2. 예정된 방식 (추가 예정)

#### Upto 방식
- **설명**: 최대 금액까지 사용량 기반 지불 (예: LLM 토큰 생성)
- **특징**: 사용량에 따른 동적 청구
- **사용 사례**: AI 모델 추론, 데이터 처리

#### Defer 방식
- **설명**: 서비스 완료 후 사용량 기반 지불
- **특징**: 후결제, 사용 기반 청구
- **사용 사례**: 배치 작업, 장기 실행 서비스

#### Subscription 방식
- **설명**: 정기 구독 모델 자동 갱신
- **특징**: 반복 액세스, 자동 결제
- **사용 사례**: API 구독, 프리미엄 서비스

---

## Facilitator API

Facilitator는 결제 검증 및 블록체인 정산을 처리하는 서비스입니다.

### POST /verify

결제 인증을 검증합니다 (트랜잭션 미실행).

**요청:**
```json
{
  "paymentPayload": {
    "x402Version": 2,
    "scheme": "exact",
    "network": "eip155:84532",
    "payload": { ... }
  },
  "paymentRequirements": {
    "scheme": "exact",
    "network": "eip155:84532",
    "amount": "10000",
    "payTo": "0x..."
  }
}
```

**응답 (성공):**
```json
{
  "isValid": true,
  "payer": "0x857b06519E91e3A54538791bDbb0E22373e36b66"
}
```

**응답 (실패):**
```json
{
  "isValid": false,
  "invalidReason": "insufficient_funds",
  "payer": "0x857b06519E91e3A54538791bDbb0E22373e36b66"
}
```

### POST /settle

검증된 결제를 블록체인에 정산합니다.

**응답 (성공):**
```json
{
  "success": true,
  "payer": "0x857b...",
  "transaction": "0x1234567890abcdef...",
  "network": "eip155:84532"
}
```

### GET /supported

Facilitator가 지원하는 scheme/network 조합을 반환합니다.

```json
{
  "kinds": [
    { "x402Version": 2, "scheme": "exact", "network": "eip155:84532" },
    { "x402Version": 2, "scheme": "exact", "network": "eip155:8453" }
  ]
}
```

---

## Discovery API (Bazaar)

x402 리소스를 자동으로 검색할 수 있는 API입니다.

### GET /discovery/resources

```bash
GET /discovery/resources?type=http&limit=10
```

**응답:**
```json
{
  "x402Version": 2,
  "items": [
    {
      "resource": "https://api.example.com/premium-data",
      "type": "http",
      "x402Version": 2,
      "accepts": [
        {
          "scheme": "exact",
          "network": "eip155:84532",
          "amount": "10000",
          "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
          "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
          "description": "Premium market data"
        }
      ],
      "lastUpdated": 1703123456,
      "metadata": {
        "category": "finance",
        "provider": "Example Corp"
      }
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "total": 1
  }
}
```

---

## 다중 체인 지원

### CAIP 표준 준수

v2는 **Chain Agnostic Improvement Proposal (CAIP)** 표준을 준수합니다:

```javascript
// EVM 체인 예시 (Base Sepolia)
network: "eip155:84532"

// Solana 체인 예시
network: "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"

// 기타 EVM 호환 체인
network: "eip155:1"     // Ethereum Mainnet
network: "eip155:137"   // Polygon
network: "eip155:56"    // BSC
```

### 체인별 특화

| 체인 | 네트워크 ID | 주요 특징 | 가스비 |
|------|-------------|------------|--------|
| **Base** | `eip155:84532` (Sepolia) / `eip155:8453` (Mainnet) | L2, 빠른 최종성 | 매우 낮음 |
| **Solana** | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | 고성능, 저비용 | 낮음 |
| **Ethereum** | `eip155:11155111` (Sepolia) / `eip155:1` (Mainnet) | L1, 높은 보안 | 높음 |
| **Polygon** | `eip155:80001` (Mumbai) / `eip155:137` (Mainnet) | L2, 중간 비용 | 중간 |

### 애셋 식별

CAIP-20 표준을 사용하여 애셋 식별:

```javascript
// USDC (Base Sepolia)
asset: "eip155:84532/erc20:0x036CbD53842c5426634e7929541eC2318f3dCF7e"

// SOL (Solana Devnet)
asset: "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp/So11111111111111111111111111111111111111112"

// ETH (Ethereum Mainnet)
asset: "eip155:1/slip44:60"
```

---

## 보안 강화

### ERC1271 지원

스마트 컨트랙트 지갑의 서명 검증 지원:

```javascript
// ERC1271 서명 확인
const isValidSignature = await contract.isValidSignature(
  messageHash,
  signature
);
```

### ERC6492 지원

생성된 스마트 컨트랙트 지갑 지원:

```javascript
// ERC6492 미배포 계정 서명 확인
const isCounterfactual = await verifyERC6492Signature(
  address,
  messageHash,
  signature
);
```

### 가스리스 트랜잭션

클라이언트가 가스가 없이도 트랜잭션 가능:

- **Meta-Transactions**: 서버가 가스를 대납
- **Relayer Networks**: 외부 릴레이어 사용
- **EIP-3074**: 계정 추상화 활용

### 리플레이 방지

- **Nonce**: 고유한 트랜잭션 식별자
- **타임스탬프**: `validAfter`, `validBefore`로 유효기간 설정
- **체인별 Nonce**: 각 체인에서 독립적인 논스 관리

---

## 세션 관리

### Sign-In-With-X (SIWx)

지갑 기반 인증 시스템 (개발 중):

```javascript
// 세션 생성
const session = await signInWithX({
  wallet: provider,
  domain: "api.example.com",
  uri: "https://api.example.com",
  statement: "Sign in with your wallet",
  resources: ["premium-data"]
});

// 세션 재사용
const response = await fetch('/premium-data', {
  headers: {
    'Authorization': `Bearer ${session.token}`,
    'X-Session': session.id
  }
});
```

### 세션 특징

- **유효기간**: 설정 가능한 세션 만료 시간
- **리소스 제한**: 특정 리소스에 대한 액세스 제어
- **재사용**: 반복 요청 시 재인증 불필요
- **보안**: 지갑 서명 기반 강력한 인증

---

## 에러 처리

x402 v2는 표준화된 에러 코드를 정의합니다.

### 에러 코드 목록

| 에러 코드 | 설명 |
|-----------|------|
| `insufficient_funds` | 잔액 부족 |
| `invalid_exact_evm_payload_authorization_valid_after` | 인증 시작 시간 미도래 |
| `invalid_exact_evm_payload_authorization_valid_before` | 인증 만료됨 |
| `invalid_exact_evm_payload_authorization_value` | 결제 금액 불일치 |
| `invalid_exact_evm_payload_signature` | 서명 검증 실패 |
| `invalid_exact_evm_payload_recipient_mismatch` | 수신자 주소 불일치 |
| `invalid_network` | 지원하지 않는 네트워크 |
| `invalid_payload` | 잘못된 페이로드 형식 |
| `invalid_payment_requirements` | 잘못된 결제 요구사항 |
| `invalid_scheme` | 지원하지 않는 결제 방식 |
| `unsupported_scheme` | Facilitator에서 지원하지 않는 결제 방식 |
| `invalid_x402_version` | 지원하지 않는 프로토콜 버전 |
| `unexpected_verify_error` | 검증 중 예상치 못한 오류 |
| `unexpected_settle_error` | 정산 중 예상치 못한 오류 |

### HTTP 에러 매핑

| x402 에러 | HTTP 상태 | 설명 |
|-----------|-----------|------|
| Payment Required | 402 | 결제 필요 |
| Invalid Payment | 400 | 잘못된 결제 데이터 |
| Payment Failed | 402 | 결제 실패 |
| Server Error | 500 | 서버 오류 |
| Success | 200 | 성공 |

---

## v1 Legacy 문서

v1 SDK를 사용하는 기존 Python 예제 문서입니다.

> ⚠️ **Legacy 문서**: 아래 문서들은 x402 v1 SDK를 다룹니다.
> 새 프로젝트는 v2 스펙을 따르는 것을 권장합니다.

### v1 예제 문서 목록

| 문서 | 설명 | 경로 |
|------|------|------|
| [python-requests-client.ko.md](v1/examples/python-requests-client.ko.md) | 동기 HTTP 클라이언트 | `legacy/clients/requests` |
| [python-httpx-client.ko.md](v1/examples/python-httpx-client.ko.md) | 비동기 HTTP 클라이언트 | `legacy/clients/httpx` |
| [python-fastapi-server.ko.md](v1/examples/python-fastapi-server.ko.md) | FastAPI 서버 | `legacy/servers/fastapi` |
| [python-discovery.ko.md](v1/examples/python-discovery.ko.md) | 리소스 검색 | `legacy/` |

### v1 vs v2 주요 차이점 요약

| 항목 | v1 (Legacy) | v2 |
|------|------------|-----|
| HTTP 헤더 | `X-PAYMENT` | `PAYMENT-SIGNATURE` |
| 네트워크 형식 | `base-sepolia` | `eip155:84532` |
| 버전 필드 | `x402Version: 1` | `x402Version: 2` |
| 예제 경로 | `examples/python/legacy/` | (준비 중) |

---

## 향상된 예제

### TypeScript/JavaScript v2

```javascript
import { withX402 } from '@x402/fetch';

// 클라이언트 예제
const response = await withX402('https://api.example.com/premium-data', {
  method: 'POST',
  body: JSON.stringify({ query: 'latest data' })
});
```

```javascript
import { x402Middleware } from '@x402/express';
import express from 'express';

// 서버 예제
const app = express();

app.use('/premium', x402Middleware({
  facilitatorUrl: 'https://facilitator.example.com',
  defaultNetwork: 'eip155:84532',
  defaultAsset: 'eip155:84532/erc20:0x036CbD53842c5426634e7929541eC2318f3dCF7e'
}));
```

### Python v2

```python
from x402 import X402Client

# 클라이언트 예제
client = X402Client(
    facilitator_url="https://facilitator.example.com",
    network="eip155:84532"
)

response = client.post(
    "https://api.example.com/premium-data",
    json={"query": "latest data"}
)
```

```python
from x402 import X402Middleware
from fastapi import FastAPI

# 서버 예제
app = FastAPI()

app.add_middleware(
    X402Middleware,
    facilitator_url="https://facilitator.example.com",
    default_network="eip155:84532"
)
```

### Go v2

```go
import "github.com/coinbase/x402/go"

// 클라이언트 예제
client := x402.NewClient(
    x402.WithFacilitator("https://facilitator.example.com"),
    x402.WithNetwork("eip155:84532"),
)

resp, err := client.Post(
    "https://api.example.com/premium-data",
    map[string]interface{}{"query": "latest data"},
)
```

---

## 📚 추가 리소스

### 공식 문서
- [x402 v2 명세서](https://github.com/coinbase/x402/tree/main/specs)
- [HTTP v2 트랜스포트](https://github.com/coinbase/x402/blob/main/specs/transports-v2/http.md)
- [CAIP 표준](https://chainagnostic.org/)

### SDK 설치
```bash
# TypeScript/JavaScript
npm install @x402/core @x402/evm @x402/svm
npm install @x402/fetch @x402/express @x402/next

# Python
pip install x402

# Go
go get github.com/coinbase/x402/go
```

### 예제 저장소
- [x402 v2 예제](https://github.com/coinbase/x402/tree/main/examples)
- [TypeScript 예제](https://github.com/coinbase/x402/tree/main/examples/typescript)
- [Python 예제](https://github.com/coinbase/x402/tree/main/examples/python)
- [Go 예제](https://github.com/coinbase/x402/tree/main/go/examples)

---

## 🤝 기여하기

이 명세서에 오류나 누락된 내용이 있다면 기여해주세요:

- 🐛 [이슈 생성](https://github.com/Daehan-Base/awesome-x402-on-base/issues/new)
- 📝 [Pull Request](https://github.com/Daehan-Base/awesome-x402-on-base/pulls)
- 💬 [토론 참여](https://github.com/Daehan-Base/awesome-x402-on-base/discussions)

---

## 📄 라이선스

이 문서는 [MIT License](../../LICENSE)에 따라 제공됩니다.

---

**작성**: Logan (Base Korea Developer Ambassador)
**마지막 업데이트**: 2025년 12월 16일
**다음 검토 예정**: 2026년 1월

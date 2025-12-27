[한국어](./README.md) | [English](./README.en.md)

# x402 한국어 문서

> Base 체인에서 x402 결제 프로토콜을 사용하기 위한 한국어 가이드

---

## 시작하기

- [getting_started.md](getting_started.md) - 환경 설정 및 시작 가이드

---

## 버전별 문서

### v2 (최신)

> 2025년 12월 11일 출시

- [x402-v2-specification.md](x402-v2-specification.md) - **v2 프로토콜 전체 명세서**
- [python/v2/](python/v2/) - Python v2 관련 문서

### v1 (Legacy)

> Python SDK 기반 예제 문서

- [python/v1/](python/v1/) - Python v1 Legacy 문서
  - [requests 클라이언트](python/v1/clients/requests/README.md)
  - [httpx 클라이언트](python/v1/clients/httpx/README.md)
  - [FastAPI 서버](python/v1/servers/fastapi/README.md)
  - [Discovery](python/v1/discovery/README.md)

---

## TypeScript 예제 문서

### v2 (최신)

> 모듈형 `@x402/*` 패키지 기반

- [typescript/v2/](typescript/v2/) - TypeScript v2 예제 문서
  - [clients/](typescript/v2/clients/) - 클라이언트 예제 (axios, fetch, custom, advanced, mcp)
  - [servers/](typescript/v2/servers/) - 서버 예제 (express, hono, advanced, custom)
  - [facilitator/](typescript/v2/facilitator/) - Facilitator 예제
  - [fullstack/](typescript/v2/fullstack/) - Fullstack 예제 (next, miniapp)

### v1 (Legacy)

- [typescript/v1/](typescript/v1/) - TypeScript v1 Legacy 문서 (예정)

---

## 빠른 비교: v1 vs v2

| 항목 | v1 (Legacy) | v2 (최신) |
|------|------------|-----------|
| HTTP 헤더 | `X-PAYMENT` | `PAYMENT-SIGNATURE`, `PAYMENT-REQUIRED` |
| 네트워크 형식 | `base-sepolia` | `eip155:84532` (CAIP 표준) |
| Transport | HTTP만 | HTTP, MCP, A2A |
| 체인 지원 | EVM 단일 | EVM + Solana 다중 체인 |

---

[← 메인 README로 돌아가기](../README.md)

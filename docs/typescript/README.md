[한국어](./README.md) | [English](./README.en.md)

# x402 TypeScript 문서

> Base 체인에서 x402 결제 프로토콜을 TypeScript로 구현하기 위한 가이드

---

## 버전별 문서

### v2 (최신)

> 2025년 12월 11일 출시, 모듈형 `@x402/*` 패키지 기반

- [v2/](v2/) - TypeScript v2 예제 문서
  - [clients/](v2/clients/) - 클라이언트 예제 (axios, fetch, custom, advanced, mcp)
  - [servers/](v2/servers/) - 서버 예제 (express, hono, advanced, custom)
  - [facilitator/](v2/facilitator/) - Facilitator 예제
  - [fullstack/](v2/fullstack/) - Fullstack 예제 (next, miniapp)

### v1 (Legacy)

> 단일 `x402` 패키지 기반

- [v1/](v1/) - TypeScript v1 Legacy 문서 (예정)

---

## v1 vs v2 주요 차이점

| 항목 | v1 (Legacy) | v2 |
|------|------------|-----|
| HTTP 헤더 | `X-PAYMENT` | `PAYMENT-SIGNATURE` |
| 네트워크 형식 | `base-sepolia` | `eip155:84532` (CAIP 표준) |
| 버전 필드 | `x402Version: 1` | `x402Version: 2` |
| SDK 구조 | 단일 `x402` 패키지 | 모듈형 `@x402/*` 패키지 |
| 체인 지원 | EVM 단일 | EVM + Solana 다중 체인 |

---

[← 문서 홈으로 돌아가기](../README.md)

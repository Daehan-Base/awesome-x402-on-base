[한국어](./README.md) | [English](./README.en.md)

# x402 한국어 문서

> Base 체인에서 x402 결제 프로토콜을 사용하기 위한 한국어 가이드

---

## 시작하기

- [getting_started.ko.md](getting_started.ko.md) - 환경 설정 및 시작 가이드

---

## 버전별 문서

### v2 (최신)

> 2025년 12월 11일 출시

- [x402-v2-specification.ko.md](x402-v2-specification.ko.md) - **v2 프로토콜 전체 명세서**
- [v2/](v2/) - v2 관련 문서

### v1 (Legacy)

> Python SDK 기반 예제 문서

- [v1/](v1/) - v1 Legacy 문서
  - [python-requests-client.ko.md](v1/examples/python-requests-client.ko.md)
  - [python-httpx-client.ko.md](v1/examples/python-httpx-client.ko.md)
  - [python-fastapi-server.ko.md](v1/examples/python-fastapi-server.ko.md)
  - [python-discovery.ko.md](v1/examples/python-discovery.ko.md)

---

## 빠른 비교: v1 vs v2

| 항목 | v1 (Legacy) | v2 (최신) |
|------|------------|-----------|
| HTTP 헤더 | `X-PAYMENT` | `PAYMENT-SIGNATURE`, `PAYMENT-REQUIRED` |
| 네트워크 형식 | `base-sepolia` | `eip155:84532` (CAIP 표준) |
| Transport | HTTP만 | HTTP, MCP, A2A |
| 체인 지원 | EVM 단일 | EVM + Solana 다중 체인 |

---

[← 메인 README로 돌아가기](../../README.md)

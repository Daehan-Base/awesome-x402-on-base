[한국어](./README.md) | [English](./README.en.md)

# x402 Python 문서

> Base 체인에서 x402 결제 프로토콜을 Python으로 구현하기 위한 가이드

---

## 버전별 문서

### v2 (최신)

> 2025년 12월 출시, 모듈형 SDK 기반

- [v2/](v2/) - Python v2 문서
  - [requests 클라이언트](v2/clients/requests/README.md) - 동기 HTTP 클라이언트
  - [httpx 클라이언트](v2/clients/httpx/README.md) - 비동기 HTTP 클라이언트
  - [FastAPI 서버](v2/servers/fastapi/README.md) - ASGI 서버
  - [Flask 서버](v2/servers/flask/README.md) - WSGI 서버

### v1 (Legacy)

> 단일 `x402` 패키지 기반

- [v1/](v1/) - Python v1 Legacy 문서 (clients/, servers/, discovery/)

---

## v1 vs v2 주요 차이점

| 항목 | v1 (Legacy) | v2 |
|------|------------|-----|
| HTTP 헤더 | `X-PAYMENT` | `PAYMENT-SIGNATURE` |
| 네트워크 형식 | `base-sepolia` | `eip155:84532` (CAIP 표준) |
| 버전 필드 | `x402Version: 1` | `x402Version: 2` |
| 예제 경로 | `examples/python/legacy/` | `examples/python/clients/`, `servers/` |

---

[← 문서 홈으로 돌아가기](../README.md)

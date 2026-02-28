[한국어](./README.md) | [English](./README.en.md)

# x402 Python v2 문서

> **x402 v2 SDK** 관련 문서입니다.
> v2는 2025년 12월 11일에 출시되었습니다.
>
> 📚 **v1에서 마이그레이션**: [Migration Guide](https://docs.cdp.coinbase.com/x402/migration-guide)

---

## v2 스펙 문서

- [x402-v2-specification.md](../../x402-v2-specification.md) - v2 프로토콜 전체 명세서

---

## Python v2 예제 가이드

### 클라이언트 예제

| 예제 | 로컬 코드 | 원본 레포 | 한글 가이드 |
|------|----------|----------|------------|
| **requests** (동기) | [→ 로컬](../../../external/x402/examples/python/clients/requests/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/clients/requests) | [→ 가이드](./clients/requests/README.md) |
| **httpx** (비동기) | [→ 로컬](../../../external/x402/examples/python/clients/httpx/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/clients/httpx) | [→ 가이드](./clients/httpx/README.md) |

### 서버 예제

| 예제 | 로컬 코드 | 원본 레포 | 한글 가이드 |
|------|----------|----------|------------|
| **FastAPI** (비동기) | [→ 로컬](../../../external/x402/examples/python/servers/fastapi/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/servers/fastapi) | [→ 가이드](./servers/fastapi/README.md) |
| **Flask** (동기) | [→ 로컬](../../../external/x402/examples/python/servers/flask/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/servers/flask) | [→ 가이드](./servers/flask/README.md) |

### 추가 예제 (후속 문서 예정)

| 예제 | 로컬 코드 | 원본 레포 | 한글 가이드 |
|------|----------|----------|------------|
| **Facilitator** | [→ 로컬](../../../external/x402/examples/python/facilitator/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/facilitator) | 예정 |
| **MCP** (AI 에이전트) | — | 예정 | 예정 |
| **Extensions** | — | 예정 | 예정 |

---

## 학습 경로

### 입문자 (x402가 처음이라면)

1. [requests 클라이언트](./clients/requests/README.md) — 동기 HTTP 클라이언트로 시작
2. [FastAPI 서버](./servers/fastapi/README.md) — 유료 API 서버 구축

### 비동기 개발자

1. [httpx 클라이언트](./clients/httpx/README.md) — async/await 패턴
2. [FastAPI 서버](./servers/fastapi/README.md) — ASGI 기반 서버

### Flask 사용자

1. [requests 클라이언트](./clients/requests/README.md) — 동기 클라이언트
2. [Flask 서버](./servers/flask/README.md) — WSGI 기반 서버

---

## v2 신기능

1. **다중 체인 지원** - Base, Solana, EVM 호환 체인 (CAIP 표준)
2. **다중 Transport** - HTTP, MCP (AI 에이전트), A2A (에이전트간)
3. **향상된 보안** - ERC1271, ERC6492 지원
4. **세션 관리** - 지갑 기반 재사용 액세스
5. **플러그인 아키텍처** - 독립적인 체인/결제 방식 확장
6. **동적 라우팅** - 요청별 `payTo` 수신자 지정
7. **자동 API 발견** - Bazaar/Discovery API

---

## TypeScript 예제

| 예제 | 로컬 코드 | 원본 레포 |
|------|----------|----------|
| 클라이언트 | [→ 로컬](../../../external/x402/examples/typescript/clients/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/) |
| 서버 | [→ 로컬](../../../external/x402/examples/typescript/servers/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/) |
| Facilitator | [→ 로컬](../../../external/x402/examples/typescript/facilitator/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/facilitator/) |

---

[← 한국어 문서로 돌아가기](../README.md) | [v1 Legacy 보기 →](../v1/README.md)

[한국어](./README.md) | [English](./README.en.md)

# x402 v1 (Legacy) 한국어 문서

> **x402 v1 SDK**를 다루는 Legacy 문서입니다.
> 최신 v2 스펙은 [x402-v2-specification.ko.md](../../x402-v2-specification.ko.md)를 참조하세요.
>
> 📚 **v1 → v2 마이그레이션**: [Migration Guide](https://docs.cdp.coinbase.com/x402/migration-guide)

---

## Python 예제 문서

| 문서 | 설명 | 공식 예제 |
|------|------|----------|
| [requests-client.ko.md](examples/requests-client.ko.md) | 동기 HTTP 클라이언트 | [clients/requests](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/requests) |
| [httpx-client.ko.md](examples/httpx-client.ko.md) | 비동기 HTTP 클라이언트 | [clients/httpx](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/httpx) |
| [fastapi-server.ko.md](examples/fastapi-server.ko.md) | FastAPI 서버 | [servers/fastapi](https://github.com/coinbase/x402/tree/main/examples/python/legacy/servers/fastapi) |
| [discovery.ko.md](examples/discovery.ko.md) | 리소스 검색 | [discovery](https://github.com/coinbase/x402/tree/main/examples/python/legacy/discovery) |

---

## v1 vs v2 주요 차이점

| 항목 | v1 (Legacy) | v2 |
|------|------------|-----|
| HTTP 헤더 | `X-PAYMENT` | `PAYMENT-SIGNATURE` |
| 네트워크 형식 | `base-sepolia` | `eip155:84532` (CAIP 표준) |
| 버전 필드 | `x402Version: 1` | `x402Version: 2` |
| SDK 구조 | 단일 `x402` 패키지 | 모듈형 `@x402/*` 패키지 |

---

## 학습 경로

```
1단계: ../../getting_started.ko.md (환경 설정)
    ↓
2단계: requests-client.ko.md (동기 클라이언트)
    ↓
3단계: httpx-client.ko.md (비동기 클라이언트)
    ↓
4단계: fastapi-server.ko.md (서버 구현)
    ↓
5단계: discovery.ko.md (고급 기능)
```

---

[← 한국어 문서로 돌아가기](../../README.md) | [v2 스펙 보기 →](../../x402-v2-specification.ko.md)

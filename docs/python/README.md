[한국어](./README.md) | [English](./README.en.md)

# x402 Python 문서

> Base 체인에서 x402 결제 프로토콜을 Python으로 구현하기 위한 가이드

---

## 버전별 문서

### v2 (최신)

> 2025년 12월 출시, 모듈형 SDK 기반

- [v2/](v2/) - Python v2 문서 (준비 중)
- 🚧 **Python v2 SDK 작업 중**: [PR #841](https://github.com/coinbase/x402/pull/841)

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
| 예제 경로 | `examples/python/legacy/` | (준비 중) |

---

[← 문서 홈으로 돌아가기](../README.md)

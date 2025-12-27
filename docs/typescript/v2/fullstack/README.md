[한국어](./README.md) | [English](./README.en.md)

# x402 Fullstack 예제

이 디렉토리는 x402 결제 프로토콜을 프론트엔드와 백엔드 모두에서 통합하는 Fullstack 예제들을 포함하고 있습니다.

## 디렉토리 구조

| 디렉토리 | 설명 |
| -------- | ---- |
| [`next/`](./next/) | Next.js 기반 x402 통합 예제 (`@x402/next`, `@x402/fetch`) |
| [`miniapp/`](./miniapp/) | Farcaster Mini App + x402 결제 통합 예제 |

## 예제 설명

### Next.js (`next/`)

`@x402/next` 미들웨어를 사용하여 Next.js 라우트를 결제로 보호하는 방법을 보여줍니다.

- `paymentProxy` - 페이지 라우트 보호
- `withX402` - API 라우트 보호
- EVM + SVM 다중 네트워크 지원
- 커스텀 Paywall UI 구성

### Farcaster Mini App (`miniapp/`)

Farcaster Mini App SDK와 x402를 결합하여 소셜 앱 내에서 결제를 처리하는 방법을 보여줍니다.

- OnchainKit 지갑 연결
- Mini App manifest 구성
- x402 보호 API 엔드포인트

## 시작하기

1. 원하는 예제 디렉토리를 선택합니다.
2. 해당 디렉토리의 README를 따라 환경을 설정합니다.
3. 개발 서버를 실행하여 테스트합니다.

---

[← v2 문서로 돌아가기](../README.md)

# 예제 (v1 Legacy)

> **x402 v1 SDK** 기반 예제입니다.
> v2 예제는 [examples/v2/](../v2/)를 참조하세요.

## 📝 요약 (TL;DR)

**무엇**: Base 체인 특화 x402 v1 예제 및 고급 사용 사례
**공식 예제**: [`external/x402/examples/python/legacy`](../../external/x402/examples/python/legacy) 사용 (서브모듈)
**이 디렉토리**: Base 최적화, AI 에이전트, 프로덕션 패턴
**한글 가이드**: [`docs/korean/v1/examples/`](../../docs/korean/v1/examples/)에서 확인

---

이 디렉토리는 공식 x402 예제를 보완하는 **Base 특화** 예제와 고급 사용 사례를 포함합니다.

## 디렉토리 구조

```
examples/
├── ap2-demo-coffee-shop/  # AI 커피숍 데모 (AP2 & x402)
└── base-specific/         # Base 체인 최적화 예제 (준비 중)
    ├── quickstart/        # Base 빠른 시작 예제
    ├── ai-agents/         # AI 에이전트 통합 (준비 중)
    └── advanced/          # 고급 최적화 (준비 중)
```

## 공식 예제와의 차이점

[공식 x402 v1 예제](../../external/x402/examples/python/legacy)는 이미 Base 체인을 기본으로 사용합니다. 이 디렉토리는 다음을 제공합니다:

1. **Base 특화 최적화**
   - Base용 가스 최적화 기법
   - USDC 통합 패턴
   - Base Sepolia 테스트넷 구성

2. **고급 사용 사례**
   - AI 에이전트 자율 결제
   - API 수익화 전략
   - 프로덕션 배포 예제

3. **커뮤니티 기여**
   - 실제 구현 사례
   - 커뮤니티 모범 사례
   - 해커톤 프로젝트

## 공식 예제

표준 x402 v1 구현은 다음을 참조하세요:
- [공식 Python 예제](../../external/x402/examples/python/legacy) (서브모듈)
- [공식 예제 한글 가이드](../../docs/korean/v1/examples/)

## Base 특화 예제 (준비 중)

### Quickstart
- [ ] Base Sepolia 빠른 시작
- [ ] USDC 결제 통합
- [ ] 간단한 API 수익화

### AI 에이전트
- [ ] LangChain + x402 통합
- [ ] 자율 AI 에이전트 결제
- [ ] 멀티 에이전트 상거래

### 고급
- [ ] 가스 최적화 전략
- [ ] 프로덕션 배포 가이드
- [ ] 멀티체인 지원

## 기여하기

Base 특화 예제를 공유하고 싶으신가요? 환영합니다!

1. 이 레포지토리를 Fork 하세요
2. 적절한 디렉토리에 예제를 추가하세요
3. 설정 가이드가 포함된 README를 작성하세요
4. Pull Request를 제출하세요

---

[← 예제 목록으로 돌아가기](../README.md) | [v2 예제 보기 →](../v2/README.md)

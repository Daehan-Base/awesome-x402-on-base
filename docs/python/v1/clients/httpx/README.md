[한국어](./README.md) | [English](./README.en.md)

# x402 httpx 클라이언트 예제 (v1 Legacy)

> ⚠️ **Legacy 문서 (v1)**
>
> 이 문서는 x402 **v1 SDK**를 다룹니다.
> 최신 v2 스펙은 [x402-v2-specification.md](../../../../x402-v2-specification.md)를 참조하세요.
>
> **v1 예제 경로**:
> - 📂 로컬: [`external/x402/examples/python/legacy/clients/httpx/`](../../../../../external/x402/examples/python/legacy/clients/httpx/)
> - 🔗 원본: [coinbase/x402/.../clients/httpx/](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/httpx)

---

x402 패키지와 httpx를 함께 사용하여 402로 보호된 엔드포인트에 비동기 요청하는 두 가지 방법을 소개합니다.

## 설정 및 사용법

1. `.env-local` 파일을 `.env`로 복사하고 개인 키를 추가하세요.

```bash
cd external/x402/examples/python/legacy/clients/httpx
cp .env-local .env
```

2. 의존성 설치:
```bash
uv sync
```

3. 예제 실행:
```bash
# 간단한 방식
uv run python main.py

# 확장 가능한 방식
uv run python extensible.py
```

## 두 가지 통합 방식

### 간단한 방식 (main.py)

간단한 방식은 `x402HttpxClient`를 사용하며, 결제를 자동으로 처리하는 사전 구성된 클라이언트입니다:

```python
from x402.clients import x402HttpxClient

async with x402HttpxClient(account=account, base_url=base_url) as client:
    response = await client.get(endpoint_path)
```

**장점:**
- 비동기 컨텍스트 매니저 지원
- 자동 리소스 관리
- 최소한의 코드로 즉시 사용 가능
- 초보자와 빠른 프로토타이핑에 적합

### 확장 가능한 방식 (extensible.py)

확장 가능한 방식은 사용자 정의 httpx 클라이언트와 함께 `x402_payment_hooks`를 사용합니다:

```python
from x402.clients import x402_payment_hooks
import httpx

async with httpx.AsyncClient(base_url=base_url) as client:
    client.event_hooks = x402_payment_hooks(account)
    response = await client.get(endpoint_path)
```

**장점:**
- 클라이언트 설정에 대한 완전한 제어
- 기존 httpx 코드와 쉬운 통합
- 커스텀 타임아웃, 헤더, 인터셉터 추가 가능
- 프로덕션 환경에 적합

## 작동 방식

두 예제 모두 다음과 같이 동작합니다:

1. 개인 키로부터 eth_account.Account 인스턴스 초기화
2. x402 결제 처리로 httpx 클라이언트 구성
3. 보호된 엔드포인트에 비동기 요청
4. 402 Payment Required 응답을 자동으로 처리
5. 최종 응답 출력

## httpx vs requests

### httpx를 선택해야 하는 경우:
- 비동기 I/O가 필요한 경우 (async/await)
- 높은 동시성이 필요한 경우
- HTTP/2 지원이 필요한 경우
- 최신 Python 기능을 활용하고 싶은 경우

### requests를 선택해야 하는 경우:
- 간단한 동기 스크립트
- 레거시 코드베이스 통합
- 비동기가 불필요한 경우

## 예제 코드 위치

```
external/x402/examples/python/legacy/clients/httpx/
├── main.py           # 간단한 방식 예제
├── extensible.py     # 확장 가능한 방식 예제
├── .env-local        # 환경 변수 템플릿
└── pyproject.toml    # 프로젝트 의존성
```

## 주요 개념

### x402HttpxClient
- httpx.AsyncClient를 확장한 사전 구성된 클라이언트
- 자동 결제 처리 기능 내장
- 컨텍스트 매니저로 안전한 리소스 관리

### x402_payment_hooks
- httpx의 이벤트 훅 시스템 활용
- 402 응답을 가로채고 결제 처리
- 기존 httpx 워크플로우에 쉽게 통합

### 비동기 프로그래밍
```python
# 여러 요청을 동시에 처리
import asyncio

async def fetch_multiple():
    async with x402HttpxClient(account=account, base_url=base_url) as client:
        tasks = [
            client.get("/endpoint1"),
            client.get("/endpoint2"),
            client.get("/endpoint3"),
        ]
        responses = await asyncio.gather(*tasks)
        return responses
```

## 다음 단계

- [requests 클라이언트 예제](../requests/README.md) - 동기 클라이언트 구현
- [FastAPI 서버 예제](../../servers/fastapi/README.md) - 402 보호된 서버 구축
- [Discovery 예제](../../discovery/README.md) - x402 서비스 검색

---

[← v1 문서로 돌아가기](../../README.md) | [v2 스펙 보기 →](../../../../x402-v2-specification.md)

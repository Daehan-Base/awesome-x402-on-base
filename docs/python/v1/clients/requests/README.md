[한국어](./README.md) | [English](./README.en.md)

# x402 requests 클라이언트 예제 (v1 Legacy)

> ⚠️ **Legacy 문서 (v1)**
>
> 이 문서는 x402 **v1 SDK**를 다룹니다.
> 최신 v2 스펙은 [x402-v2-specification.md](../../../../x402-v2-specification.md)를 참조하세요.
>
> **v1 예제 경로**: [python/legacy/clients/requests](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/requests)

---

x402 패키지와 requests를 함께 사용하여 402로 보호된 엔드포인트에 요청하는 두 가지 방법을 소개합니다.

## 설정 및 사용법

1. `.env-local` 파일을 `.env`로 복사하고 개인 키를 추가하세요.

```bash
cd external/x402/examples/python/legacy/clients/requests
cp .env-local .env
```

2. 의존성 설치:
```bash
uv sync
```

3. 예제 실행:
```bash
# 간단한 방식
python main.py

# 확장 가능한 방식
python extensible.py
```

## 두 가지 통합 방식

### 간단한 방식 (main.py)

간단한 방식은 `x402_requests`를 사용하며, 결제를 자동으로 처리하는 사전 구성된 세션을 반환합니다:

```python
from x402.clients import x402_requests

session = x402_requests(account)
response = session.get(url)
```

**장점:**
- 설정이 간단하고 빠름
- 한 줄로 x402 기능을 갖춘 세션 생성
- 초보자에게 적합

### 확장 가능한 방식 (extensible.py)

확장 가능한 방식은 사용자 정의 requests 세션과 함께 `x402_http_adapter`를 사용합니다:

```python
from x402.clients import x402_http_adapter
import requests

session = requests.Session()
adapter = x402_http_adapter(account)
session.mount("http://", adapter)
session.mount("https://", adapter)
response = session.get(url)
```

**장점:**
- 세션에 대한 완전한 제어
- 기존 requests 코드와 통합 용이
- 커스텀 설정 및 미들웨어 추가 가능

## 작동 방식

두 예제 모두 다음과 같이 동작합니다:

1. 개인 키로부터 eth_account.Account 인스턴스 초기화
2. x402 결제 처리로 requests 세션 구성
3. 보호된 엔드포인트에 요청
4. 402 Payment Required 응답을 자동으로 처리
5. 최종 응답 출력

## 예제 코드 위치

```
external/x402/examples/python/legacy/clients/requests/
├── main.py           # 간단한 방식 예제
├── extensible.py     # 확장 가능한 방식 예제
├── .env-local        # 환경 변수 템플릿
└── pyproject.toml    # 프로젝트 의존성
```

## 주요 개념

### x402_requests
- 모든 것이 설정된 세션 객체를 반환하는 헬퍼 함수
- 내부적으로 `x402_http_adapter`를 사용
- 빠른 프로토타이핑에 이상적

### x402_http_adapter
- requests의 HTTPAdapter를 확장
- 402 응답을 가로채고 결제를 처리
- 기존 requests 워크플로우에 통합 가능

## 다음 단계

- [httpx 클라이언트 예제](../httpx/README.md) - 비동기 클라이언트 구현
- [FastAPI 서버 예제](../../servers/fastapi/README.md) - 402 보호된 서버 구축
- [Discovery 예제](../../discovery/README.md) - x402 서비스 검색

---

[← v1 문서로 돌아가기](../../README.md) | [v2 스펙 보기 →](../../../../x402-v2-specification.md)

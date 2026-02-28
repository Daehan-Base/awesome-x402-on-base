[한국어](./README.md) | [English](./README.en.md)

# x402 httpx 클라이언트 예제 (v2)

> **v2 문서 (최신)**
>
> 이 문서는 x402 **v2 SDK (v2.2.0+)** 를 다룹니다.
> v1 Legacy 문서는 [v1 httpx 클라이언트](../../../v1/clients/httpx/README.md)를 참조하세요.
>
> **v2 예제 경로**:
> - 📂 로컬: [`external/x402/examples/python/clients/httpx/`](../../../../../external/x402/examples/python/clients/httpx/)
> - 🔗 원본: [coinbase/x402/.../clients/httpx/](https://github.com/coinbase/x402/tree/main/examples/python/clients/httpx)
>
> **작성일**: 2026년 2월 28일
> **최종 검증**: `external/x402/examples/python/clients/httpx/main.py` 기준

---

x402 v2 SDK와 httpx를 사용하여 402로 보호된 엔드포인트에 비동기 결제 요청을 보내는 방법을 소개합니다.

**Web2 비유**: 비동기 HTTP 클라이언트(httpx, aiohttp)로 API를 호출하는 것처럼, x402 httpx 클라이언트는 `async/await` 패턴으로 결제를 처리합니다. 대량의 유료 API 호출을 비동기로 효율적으로 처리할 수 있습니다.

## v1 → v2 변경 사항

| 항목 | v1 (Legacy) | v2 |
|------|------------|-----|
| 클라이언트 | `x402_httpx(account)` | `x402HttpxClient(x402Client())` |
| 서명자 | `eth_account.Account` 직접 전달 | `EthAccountSigner` 래퍼 사용 |
| 다중 체인 | EVM만 지원 | EVM + Solana 동시 지원 |
| 네트워크 형식 | `base-sepolia` | `eip155:84532` (CAIP-2) |
| 환경 변수 | `PRIVATE_KEY` | `EVM_PRIVATE_KEY` |
| 결제 방식 등록 | 자동 (단일) | `register_exact_evm_client()` 명시적 등록 |
| 결제 응답 | 없음 | `get_payment_settle_response()` 지원 |

## 설정 및 사용법

1. `.env-local` 파일을 `.env`로 복사하고 개인 키를 추가하세요.

```bash
cd external/x402/examples/python/clients/httpx
cp .env-local .env
```

`.env` 파일 내용:
```bash
EVM_PRIVATE_KEY=0xYourPrivateKey
SVM_PRIVATE_KEY=              # Solana 사용 시 (선택)
RESOURCE_SERVER_URL=http://localhost:4021
ENDPOINT_PATH=/weather
```

> **보안 주의**: 개인 키를 절대 커밋하지 마세요. `.env`는 `.gitignore`에 포함되어 있습니다.

2. 의존성 설치:
```bash
uv sync
```

3. 서버 실행 (별도 터미널):
```bash
# FastAPI 또는 Flask 서버를 먼저 실행하세요
cd ../../../servers/fastapi
uv sync && uv run python main.py
```

4. 클라이언트 실행:
```bash
cd external/x402/examples/python/clients/httpx
uv run python main.py
```

## 코드 분석 (main.py)

### 1. 초기화

```python
from eth_account import Account

from x402 import x402Client
from x402.http import x402HTTPClient
from x402.http.clients import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client
from x402.mechanisms.svm import KeypairSigner
from x402.mechanisms.svm.exact.register import register_exact_svm_client

# x402 클라이언트 생성 (비동기 버전)
client = x402Client()
```

httpx는 비동기 클라이언트이므로 `x402Client` (비동기 버전)를 사용합니다. requests의 `x402ClientSync`와 구분됩니다.

### 2. 결제 방식 등록

```python
# EVM 결제 방식 등록
if evm_private_key:
    account = Account.from_key(evm_private_key)
    register_exact_evm_client(client, EthAccountSigner(account))

# SVM (Solana) 결제 방식 등록 (선택)
if svm_private_key:
    svm_signer = KeypairSigner.from_base58(svm_private_key)
    register_exact_svm_client(client, svm_signer)
```

requests 예제와 동일한 등록 방식입니다. 비동기/동기에 관계없이 동일한 서명자를 사용합니다.

### 3. 비동기 요청 및 결제

```python
# HTTP 클라이언트 헬퍼 생성 (결제 응답 추출용)
http_client = x402HTTPClient(client)

async with x402HttpxClient(client) as http:
    response = await http.get(url)
    await response.aread()  # httpx 특유: 응답 본문 명시적 읽기

    if response.is_success:  # httpx는 .is_success 사용 (requests는 .ok)
        settle_response = http_client.get_payment_settle_response(
            lambda name: response.headers.get(name)
        )
```

**httpx 특이사항:**
- `async with`로 비동기 컨텍스트 매니저 사용
- `await response.aread()`로 응답 본문을 명시적으로 읽어야 함
- `response.is_success` 사용 (requests의 `response.ok`와 동일)

### 4. 메인 함수

```python
if __name__ == "__main__":
    asyncio.run(main())
```

Python의 `asyncio.run()`으로 비동기 메인 함수를 실행합니다.

## 예제 코드 위치

```
external/x402/examples/python/clients/httpx/
├── main.py           # 비동기 httpx 클라이언트 예제
├── .env-local        # 환경 변수 템플릿
└── pyproject.toml    # 프로젝트 의존성 (x402[httpx,evm,svm])
```

## 주요 개념

### x402Client vs x402ClientSync
- `x402Client` — 비동기 클라이언트 (httpx용)
- `x402ClientSync` — 동기 클라이언트 (requests용)
- 두 클래스 모두 동일한 결제 방식 등록 API 사용

### x402HttpxClient
- httpx의 `AsyncClient`를 x402 결제 기능으로 래핑
- `async with` 컨텍스트 매니저로 사용
- 내부적으로 402 응답 감지 → 결제 생성 → 재요청 처리

### x402HTTPClient
- 결제 응답 추출을 위한 HTTP 헬퍼 클래스
- `get_payment_settle_response()`로 결제 정산 결과 확인
- 동기 버전: `x402HTTPClientSync`

### requests vs httpx 비교

| 항목 | requests (동기) | httpx (비동기) |
|------|----------------|---------------|
| x402 클라이언트 | `x402ClientSync` | `x402Client` |
| HTTP 래퍼 | `x402_requests(client)` | `x402HttpxClient(client)` |
| 컨텍스트 매니저 | `with` | `async with` |
| 응답 확인 | `response.ok` | `response.is_success` |
| 응답 읽기 | 자동 | `await response.aread()` |
| 의존성 | `x402[requests,evm,svm]` | `x402[httpx,evm,svm]` |

## 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `EVM_PRIVATE_KEY` | EVM 또는 SVM 중 하나 | EVM 지갑 개인 키 (Base Sepolia) |
| `SVM_PRIVATE_KEY` | EVM 또는 SVM 중 하나 | Solana 지갑 개인 키 (Devnet) |
| `RESOURCE_SERVER_URL` | 예 | 서버 URL (기본: `http://localhost:4021`) |
| `ENDPOINT_PATH` | 예 | 요청 경로 (기본: `/weather`) |

## 다음 단계

- [requests 클라이언트 예제](../requests/README.md) - 동기 클라이언트 구현
- [FastAPI 서버 예제](../../servers/fastapi/README.md) - 402 보호된 서버 구축
- [Flask 서버 예제](../../servers/flask/README.md) - Flask 기반 서버 구축

---

[← v2 문서로 돌아가기](../../README.md) | [v1 Legacy 보기 →](../../../v1/clients/httpx/README.md)

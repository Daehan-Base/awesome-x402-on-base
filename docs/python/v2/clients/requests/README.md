[한국어](./README.md) | [English](./README.en.md)

# x402 requests 클라이언트 예제 (v2)

> **v2 문서 (최신)**
>
> 이 문서는 x402 **v2 SDK (v2.2.0+)** 를 다룹니다.
> v1 Legacy 문서는 [v1 requests 클라이언트](../../../v1/clients/requests/README.md)를 참조하세요.
>
> **v2 예제 경로**:
> - 📂 로컬: [`external/x402/examples/python/clients/requests/`](../../../../../external/x402/examples/python/clients/requests/)
> - 🔗 원본: [coinbase/x402/.../clients/requests/](https://github.com/coinbase/x402/tree/main/examples/python/clients/requests)
>
> **작성일**: 2026년 2월 28일
> **최종 검증**: `external/x402/examples/python/clients/requests/main.py` 기준

---

x402 v2 SDK와 requests를 사용하여 402로 보호된 엔드포인트에 결제 요청을 보내는 방법을 소개합니다.

**Web2 비유**: 유료 API에 API 키를 헤더에 넣어 요청하는 것처럼, x402는 결제 서명을 HTTP 헤더에 자동으로 추가하여 유료 엔드포인트에 접근합니다. API 키 대신 암호화폐 결제가 인증 수단이 됩니다.

## v1 → v2 변경 사항

| 항목 | v1 (Legacy) | v2 |
|------|------------|-----|
| 클라이언트 | `x402_requests(account)` | `x402_requests(x402ClientSync())` |
| 서명자 | `eth_account.Account` 직접 전달 | `EthAccountSigner` 래퍼 사용 |
| 다중 체인 | EVM만 지원 | EVM + Solana 동시 지원 |
| 네트워크 형식 | `base-sepolia` | `eip155:84532` (CAIP-2) |
| 환경 변수 | `PRIVATE_KEY` | `EVM_PRIVATE_KEY` |
| 결제 방식 등록 | 자동 (단일) | `register_exact_evm_client()` 명시적 등록 |
| 결제 응답 | 없음 | `get_payment_settle_response()` 지원 |

## 설정 및 사용법

1. `.env-local` 파일을 `.env`로 복사하고 개인 키를 추가하세요.

```bash
cd external/x402/examples/python/clients/requests
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
cd external/x402/examples/python/clients/requests
uv run python main.py
```

## 코드 분석 (main.py)

### 1. 초기화

```python
from eth_account import Account

from x402 import x402ClientSync
from x402.http import x402HTTPClientSync
from x402.http.clients import x402_requests
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client
from x402.mechanisms.svm import KeypairSigner
from x402.mechanisms.svm.exact.register import register_exact_svm_client

# x402 클라이언트 생성 (동기 버전)
client = x402ClientSync()
```

v2에서는 `x402ClientSync`를 먼저 생성한 뒤, 결제 방식(scheme)을 등록하는 모듈형 구조입니다.

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

v1과 달리 여러 체인의 결제 방식을 하나의 클라이언트에 등록할 수 있습니다.

### 3. 요청 및 결제

```python
# HTTP 클라이언트 헬퍼 생성 (결제 응답 추출용)
http_client = x402HTTPClientSync(client)

# 컨텍스트 매니저로 세션 생성
with x402_requests(client) as session:
    response = session.get(url)

    # 결제 응답 추출
    if response.ok:
        settle_response = http_client.get_payment_settle_response(
            lambda name: response.headers.get(name)
        )
```

`x402_requests`가 402 응답을 자동으로 감지하고 결제를 처리합니다.

## 예제 코드 위치

```
external/x402/examples/python/clients/requests/
├── main.py           # 동기 requests 클라이언트 예제
├── .env-local        # 환경 변수 템플릿
└── pyproject.toml    # 프로젝트 의존성 (x402[requests,evm,svm])
```

## 주요 개념

### x402ClientSync
- v2의 핵심 동기(sync) 클라이언트 클래스
- 결제 방식(scheme)을 플러그인처럼 등록
- 비동기 버전: `x402Client` (httpx에서 사용)

### EthAccountSigner
- `eth_account.Account`를 감싸는 서명자 래퍼
- EVM 체인(Base, Ethereum 등)용 결제 서명 생성
- v1에서는 Account를 직접 전달했지만, v2는 추상화된 서명자 인터페이스 사용

### register_exact_evm_client
- "exact" 결제 방식을 클라이언트에 등록하는 함수
- 정확한 금액을 지불하는 방식 (향후 스트리밍 등 다른 방식 확장 가능)
- Solana용: `register_exact_svm_client`

### x402_requests
- requests 세션을 x402 결제 기능으로 래핑
- 컨텍스트 매니저 (`with` 문)로 사용
- 내부적으로 402 응답 감지 → 결제 생성 → 재요청 처리

## 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `EVM_PRIVATE_KEY` | EVM 또는 SVM 중 하나 | EVM 지갑 개인 키 (Base Sepolia) |
| `SVM_PRIVATE_KEY` | EVM 또는 SVM 중 하나 | Solana 지갑 개인 키 (Devnet) |
| `RESOURCE_SERVER_URL` | 예 | 서버 URL (기본: `http://localhost:4021`) |
| `ENDPOINT_PATH` | 예 | 요청 경로 (기본: `/weather`) |

## 다음 단계

- [httpx 클라이언트 예제](../httpx/README.md) - 비동기 클라이언트 구현
- [FastAPI 서버 예제](../../servers/fastapi/README.md) - 402 보호된 서버 구축
- [Flask 서버 예제](../../servers/flask/README.md) - Flask 기반 서버 구축

---

[← v2 문서로 돌아가기](../../README.md) | [v1 Legacy 보기 →](../../../v1/clients/requests/README.md)

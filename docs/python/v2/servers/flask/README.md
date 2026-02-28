[한국어](./README.md) | [English](./README.en.md)

# x402 Flask 서버 예제 (v2)

> **v2 문서 (최신)**
>
> 이 문서는 x402 **v2 SDK (v2.2.0+)** 를 다룹니다.
> Flask 지원은 v2에서 새롭게 추가되었습니다 (v1에는 FastAPI만 지원).
>
> **v2 예제 경로**:
> - 📂 로컬: [`external/x402/examples/python/servers/flask/`](../../../../../external/x402/examples/python/servers/flask/)
> - 🔗 원본: [coinbase/x402/.../servers/flask/](https://github.com/coinbase/x402/tree/main/examples/python/servers/flask)
>
> **작성일**: 2026년 2월 28일
> **최종 검증**: `external/x402/examples/python/servers/flask/main.py` 기준

---

x402 v2 SDK의 Flask 미들웨어를 사용하여 유료 API 엔드포인트를 구현하는 방법을 소개합니다.

**Web2 비유**: Flask에서 `@login_required` 데코레이터로 인증을 요구하듯, x402 미들웨어는 특정 라우트에 결제를 요구합니다. 기존 Flask 앱에 미들웨어를 한 줄 추가하면 엔드포인트가 유료화됩니다.

## FastAPI와의 비교

Flask는 v2에서 새로 지원되며, v1에서 제공되지 않았습니다. FastAPI(비동기)와의 주요 차이점:

| 항목 | FastAPI (비동기) | Flask (동기) |
|------|-----------------|-------------|
| 서버 타입 | ASGI | WSGI |
| 리소스 서버 | `x402ResourceServer` | `x402ResourceServerSync` |
| Facilitator 클라이언트 | `HTTPFacilitatorClient` | `HTTPFacilitatorClientSync` |
| 미들웨어 등록 | `app.add_middleware(PaymentMiddlewareASGI, ...)` | `payment_middleware(app, ...)` |
| 응답 모델 | Pydantic `BaseModel` | `jsonify()` 딕셔너리 |
| 서버 실행 | `uvicorn.run(app, ...)` | `app.run(host=..., port=...)` |

## 사전 요구사항

- Python 3.10 이상
- 결제를 받을 유효한 Ethereum 주소 (EVM)
- Solana 주소 (SVM, 이 예제 코드에서는 필수)

## 설정 및 사용법

1. `.env-local` 파일을 `.env`로 복사하고 주소를 추가하세요.

```bash
cd external/x402/examples/python/servers/flask
cp .env-local .env
```

`.env` 파일 내용:
```bash
EVM_ADDRESS=0xYourEthereumAddress
SVM_ADDRESS=YourSolanaAddress
FACILITATOR_URL=https://x402.org/facilitator
```

> **참고**: 서버는 결제를 **받는** 쪽이므로 주소(공개키)만 필요합니다. 개인 키는 필요하지 않습니다.

2. 의존성 설치:
```bash
uv sync
```

3. 서버 실행:
```bash
uv run python main.py
```

서버가 `http://0.0.0.0:4021`에서 시작됩니다.

## 코드 분석 (main.py)

### 1. 네트워크 및 설정

```python
from x402.schemas import AssetAmount, Network

EVM_NETWORK: Network = "eip155:84532"   # Base Sepolia
SVM_NETWORK: Network = "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1"  # Solana Devnet
FACILITATOR_URL = os.getenv("FACILITATOR_URL", "https://x402.org/facilitator")
```

FastAPI 예제와 동일한 CAIP-2 표준 네트워크 식별자를 사용합니다.

### 2. x402 리소스 서버 구성 (동기)

```python
from x402.http import FacilitatorConfig, HTTPFacilitatorClientSync, PaymentOption
from x402.http.middleware.flask import payment_middleware
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.mechanisms.svm.exact import ExactSvmServerScheme
from x402.server import x402ResourceServerSync

# 동기 Facilitator 클라이언트 생성
facilitator = HTTPFacilitatorClientSync(FacilitatorConfig(url=FACILITATOR_URL))

# 동기 리소스 서버 생성 및 결제 방식 등록
server = x402ResourceServerSync(facilitator)
server.register(EVM_NETWORK, ExactEvmServerScheme())
server.register(SVM_NETWORK, ExactSvmServerScheme())
```

Flask는 WSGI 기반 동기 프레임워크이므로, `x402ResourceServerSync`와 `HTTPFacilitatorClientSync`를 사용합니다.

### 3. 라우트 설정

```python
routes = {
    "GET /weather": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=EVM_ADDRESS,
                price="$0.01",
                network=EVM_NETWORK,
            ),
            PaymentOption(
                scheme="exact",
                pay_to=SVM_ADDRESS,
                price="$0.01",
                network=SVM_NETWORK,
            ),
        ],
        mime_type="application/json",
        description="Weather report",
    ),
    "GET /premium/*": RouteConfig(
        accepts=[
            PaymentOption(
                scheme="exact",
                pay_to=EVM_ADDRESS,
                price=AssetAmount(
                    amount="10000",  # $0.01 USDC (6 decimals)
                    asset="0x036CbD53842c5426634e7929541eC2318f3dCF7e",
                    extra={"name": "USDC", "version": "2"},
                ),
                network=EVM_NETWORK,
            ),
            PaymentOption(
                scheme="exact",
                pay_to=SVM_ADDRESS,
                price="$0.01",
                network=SVM_NETWORK,
            ),
        ],
        mime_type="application/json",
        description="Premium content",
    ),
}
```

라우트 설정은 FastAPI 예제와 완전히 동일한 `RouteConfig` 구조를 사용합니다.

### 4. 미들웨어 등록

```python
payment_middleware(app, routes=routes, server=server)
```

Flask에서는 함수 호출로 미들웨어를 등록합니다 (FastAPI의 `app.add_middleware()`와 다름).

### 5. 엔드포인트 정의

```python
@app.route("/health")
def health_check():
    return jsonify({"status": "ok"})

@app.route("/weather")
def get_weather():
    return jsonify({"report": {"weather": "sunny", "temperature": 70}})

@app.route("/premium/content")
def get_premium_content():
    return jsonify({"content": "This is premium content"})
```

Flask 표준 패턴으로 엔드포인트를 정의합니다. `jsonify()`로 JSON 응답을 반환합니다.

## 서버 테스트하기

### 1. 무료 엔드포인트 테스트

```bash
curl http://localhost:4021/health
# {"status":"ok"}
```

### 2. 유료 엔드포인트 테스트 (결제 없이)

```bash
curl -i http://localhost:4021/weather
# HTTP/1.1 402 Payment Required
# 응답 헤더에 결제 옵션 정보 포함
```

### 3. x402 클라이언트로 테스트

```bash
cd external/x402/examples/python/clients/requests
uv sync && uv run python main.py
```

## 예제 코드 위치

```
external/x402/examples/python/servers/flask/
├── main.py           # Flask 서버 예제
├── .env-local        # 환경 변수 템플릿
└── pyproject.toml    # 프로젝트 의존성 (x402[flask,evm,svm])
```

## 주요 개념

### x402ResourceServerSync
- v2의 동기 서버 클래스 (Flask/WSGI용)
- 비동기 버전: `x402ResourceServer` (FastAPI에서 사용)
- 동일한 결제 방식 등록 API

### payment_middleware (Flask)
- Flask 앱에 결제 검증 미들웨어를 추가하는 함수
- FastAPI의 `PaymentMiddlewareASGI`와 동일한 기능
- `payment_middleware(app, routes=routes, server=server)`

### HTTPFacilitatorClientSync
- 동기 HTTP Facilitator 클라이언트
- Flask/WSGI 환경에서 사용
- 비동기 버전: `HTTPFacilitatorClient`

### Flask vs FastAPI 선택 기준

| 선택 기준 | Flask | FastAPI |
|-----------|-------|---------|
| 기존 코드 | Flask 앱이 이미 있음 | 새 프로젝트 |
| 비동기 필요 | 아니오 | 예 |
| 성능 요구 | 보통 | 높음 |
| API 문서 | 수동 | 자동 (OpenAPI) |
| 타입 힌트 | 선택 | 필수 |

## 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `EVM_ADDRESS` | 예 | 결제를 받을 EVM 주소 |
| `SVM_ADDRESS` | 예 | 결제를 받을 Solana 주소 |
| `FACILITATOR_URL` | 아니오 | Facilitator URL (기본: `https://x402.org/facilitator`) |

## 다음 단계

- [FastAPI 서버 예제](../fastapi/README.md) - 비동기 FastAPI 서버 구축
- [requests 클라이언트 예제](../../clients/requests/README.md) - 동기 클라이언트로 서버 테스트
- [httpx 클라이언트 예제](../../clients/httpx/README.md) - 비동기 클라이언트로 서버 테스트

## 추가 리소스

- [Flask 공식 문서](https://flask.palletsprojects.com/)
- x402 프로토콜 사양: [📂 로컬](../../../../../external/x402/) | [🔗 원본](https://github.com/coinbase/x402)
- [Base 네트워크 문서](https://docs.base.org/)

---

[← v2 문서로 돌아가기](../../README.md) | [FastAPI 서버 보기 →](../fastapi/README.md)

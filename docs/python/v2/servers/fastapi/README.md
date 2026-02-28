[한국어](./README.md) | [English](./README.en.md)

# x402 FastAPI 서버 예제 (v2)

> **v2 문서 (최신)**
>
> 이 문서는 x402 **v2 SDK (v2.2.0+)** 를 다룹니다.
> v1 Legacy 문서는 [v1 FastAPI 서버](../../../v1/servers/fastapi/README.md)를 참조하세요.
>
> **v2 예제 경로**:
> - 📂 로컬: [`external/x402/examples/python/servers/fastapi/`](../../../../../external/x402/examples/python/servers/fastapi/)
> - 🔗 원본: [coinbase/x402/.../servers/fastapi/](https://github.com/coinbase/x402/tree/main/examples/python/servers/fastapi)
>
> **작성일**: 2026년 2월 28일
> **최종 검증**: `external/x402/examples/python/servers/fastapi/main.py` 기준

---

x402 v2 SDK의 FastAPI 미들웨어를 사용하여 유료 API 엔드포인트를 구현하는 방법을 소개합니다.

**Web2 비유**: SaaS API에서 API 키로 접근을 제한하고 요금을 부과하는 것처럼, x402 미들웨어는 HTTP 요청마다 자동으로 결제를 검증합니다. 별도의 인증 시스템이나 구독 관리 없이, 미들웨어 한 줄로 엔드포인트를 유료화할 수 있습니다.

## v1 → v2 변경 사항

| 항목 | v1 (Legacy) | v2 |
|------|------------|-----|
| 미들웨어 | `paywall_middleware()` | `PaymentMiddlewareASGI` |
| 가격 설정 | USD 문자열 또는 `TokenAmount` 객체 | `"$0.01"` 또는 `AssetAmount` 객체 |
| 라우트 설정 | `{"/path": "$0.01"}` | `{"/path": RouteConfig(...)}` |
| 다중 체인 | Base만 | EVM + Solana 동시 지원 |
| 네트워크 형식 | `base-sepolia` | `eip155:84532` (CAIP-2) |
| 결제 검증 | 내장 | Facilitator 서비스 사용 |
| 환경 변수 | `ADDRESS` | `EVM_ADDRESS` + `SVM_ADDRESS` |

## 사전 요구사항

- Python 3.10 이상
- 결제를 받을 유효한 Ethereum 주소 (EVM)
- Solana 주소 (SVM, 이 예제 코드에서는 필수)

## 설정 및 사용법

1. `.env-local` 파일을 `.env`로 복사하고 주소를 추가하세요.

```bash
cd external/x402/examples/python/servers/fastapi
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

v2에서는 CAIP-2 표준 네트워크 식별자를 사용합니다.

### 2. x402 리소스 서버 구성

```python
from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.mechanisms.svm.exact import ExactSvmServerScheme
from x402.server import x402ResourceServer

# Facilitator 클라이언트 생성
facilitator = HTTPFacilitatorClient(FacilitatorConfig(url=FACILITATOR_URL))

# 리소스 서버 생성 및 결제 방식 등록
server = x402ResourceServer(facilitator)
server.register(EVM_NETWORK, ExactEvmServerScheme())
server.register(SVM_NETWORK, ExactSvmServerScheme())
```

v1과 달리, v2에서는 Facilitator 서비스를 통해 결제를 검증합니다.

### 3. 라우트 설정

```python
routes = {
    # 문자열 가격: "$0.01"
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
    # AssetAmount 가격: USDC 토큰 직접 지정
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

**가격 설정 방법:**
- `"$0.01"` — 달러 기반 문자열 (간편)
- `AssetAmount(...)` — 토큰 금액 직접 지정 (정밀 제어)

### 4. 미들웨어 등록

```python
app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=server)
```

한 줄로 모든 유료 엔드포인트에 결제 검증을 추가합니다.

### 5. 엔드포인트 정의

```python
@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/weather")
async def get_weather() -> WeatherResponse:
    return WeatherResponse(report=WeatherReport(weather="sunny", temperature=70))

@app.get("/premium/content")
async def get_premium_content() -> PremiumContentResponse:
    return PremiumContentResponse(content="This is premium content")
```

- `/health` — 무료 엔드포인트 (라우트 설정에 없음)
- `/weather` — 유료 ($0.01, 문자열 가격)
- `/premium/content` — 유료 ($0.01 USDC, AssetAmount)

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

requests 또는 httpx 클라이언트 예제를 사용하여 자동 결제를 테스트하세요:

```bash
cd external/x402/examples/python/clients/requests
uv sync && uv run python main.py
```

## 예제 코드 위치

```
external/x402/examples/python/servers/fastapi/
├── main.py           # FastAPI 서버 예제
├── .env-local        # 환경 변수 템플릿
└── pyproject.toml    # 프로젝트 의존성 (x402[fastapi,evm,svm])
```

## 주요 개념

### x402ResourceServer
- v2의 핵심 서버 클래스 (비동기)
- 결제 방식(scheme)을 네트워크별로 등록
- Facilitator를 통한 결제 검증
- 동기 버전: `x402ResourceServerSync` (Flask에서 사용)

### PaymentMiddlewareASGI
- FastAPI/Starlette ASGI 미들웨어
- 유료 라우트에 대한 요청을 가로채서 결제 검증
- 결제 없으면 402 응답 + 결제 옵션 반환

### RouteConfig
- 라우트별 결제 설정을 정의
- `accepts`: 허용하는 결제 옵션 목록
- `mime_type`: 응답 MIME 타입
- `description`: 엔드포인트 설명

### PaymentOption
- 개별 결제 옵션을 정의
- `scheme`: 결제 방식 ("exact")
- `pay_to`: 수신 주소
- `price`: 가격 (문자열 또는 AssetAmount)
- `network`: 네트워크 식별자 (CAIP-2)

### Facilitator
- 결제 검증을 수행하는 외부 서비스
- 기본값: `https://x402.org/facilitator`
- 결제 서명 검증 및 정산 처리

## 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `EVM_ADDRESS` | 예 | 결제를 받을 EVM 주소 |
| `SVM_ADDRESS` | 예 | 결제를 받을 Solana 주소 |
| `FACILITATOR_URL` | 아니오 | Facilitator URL (기본: `https://x402.org/facilitator`) |

## 다음 단계

- [Flask 서버 예제](../flask/README.md) - Flask 기반 동기 서버 구축
- [requests 클라이언트 예제](../../clients/requests/README.md) - 동기 클라이언트로 서버 테스트
- [httpx 클라이언트 예제](../../clients/httpx/README.md) - 비동기 클라이언트로 서버 테스트

## 추가 리소스

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- x402 프로토콜 사양: [📂 로컬](../../../../../external/x402/) | [🔗 원본](https://github.com/coinbase/x402)
- [Base 네트워크 문서](https://docs.base.org/)

---

[← v2 문서로 돌아가기](../../README.md) | [v1 Legacy 보기 →](../../../v1/servers/fastapi/README.md)

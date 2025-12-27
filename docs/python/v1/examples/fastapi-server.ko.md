# x402 FastAPI 서버 예제 (v1 Legacy)

> ⚠️ **Legacy 문서 (v1)**
>
> 이 문서는 x402 **v1 SDK**를 다룹니다.
> 최신 v2 스펙은 [x402-v2-specification.ko.md](../../../x402-v2-specification.ko.md)를 참조하세요.
>
> **v1 예제 경로**: [python/legacy/servers/fastapi](https://github.com/coinbase/x402/tree/main/examples/python/legacy/servers/fastapi)

---

x402 FastAPI 미들웨어를 사용하여 유료 API 엔드포인트를 구현하는 방법을 소개합니다. 이 예제는 API에 페이월 기능을 추가하여 엔드포인트 접근을 수익화하는 방법을 보여줍니다.

## 사전 요구사항

- Python 3.10 이상
- 결제를 받을 유효한 Ethereum 주소

## 설정 및 사용법

1. `.env-local` 파일을 `.env`로 복사하고 결제를 받을 Ethereum 주소를 추가하세요:

```bash
cd external/x402/examples/python/legacy/servers/fastapi
cp .env-local .env
```

`.env` 파일 내용:
```bash
ADDRESS=0xYourEthereumAddress
```

2. 의존성 설치:
```bash
uv sync
```

3. 서버 실행:
```bash
uv run python main.py
```

서버가 http://localhost:4021 에서 시작됩니다.

## x402 FastAPI 미들웨어 작동 방식

x402 FastAPI 미들웨어는 특정 경로에 대해 결제를 요구하는 방식으로 작동합니다. 클라이언트가 보호된 엔드포인트에 접근하려고 하면:

1. **첫 번째 요청**: 미들웨어가 결제 정보가 포함되지 않은 요청을 가로챕니다
2. **402 응답 반환**: 서버가 결제 요구사항이 담긴 402 Payment Required 응답을 반환합니다
3. **클라이언트 결제**: 클라이언트가 결제 정보를 생성하고 서명합니다
4. **재요청**: 클라이언트가 결제 헤더와 함께 다시 요청합니다
5. **검증 및 응답**: 미들웨어가 결제를 검증하고 실제 엔드포인트 핸들러를 실행합니다

## 기본 예제 코드 분석

```python
import os
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from x402.fastapi.middleware import require_payment
from x402.types import EIP712Domain, TokenAmount, TokenAsset

# 환경 변수 로드
load_dotenv()

# 환경 변수에서 설정 가져오기
ADDRESS = os.getenv("ADDRESS")

if not ADDRESS:
    raise ValueError("Missing required environment variables")

app = FastAPI()

# 특정 경로에 결제 미들웨어 적용 - USD 가격 사용
app.middleware("http")(
    require_payment(
        path="/weather",           # 보호할 엔드포인트 경로
        price="$0.001",            # USD 가격 (자동으로 토큰으로 변환)
        pay_to_address=ADDRESS,    # 결제를 받을 주소
        network="base-sepolia",    # 네트워크 (base-sepolia, base 등)
    )
)

# 엔드포인트 정의
@app.get("/weather")
async def get_weather() -> Dict[str, Any]:
    return {
        "report": {
            "weather": "sunny",
            "temperature": 70,
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4021)
```

## 고급 설정: 토큰 결제

USD 가격 대신 특정 토큰으로 직접 결제를 받을 수도 있습니다:

```python
# 프리미엄 경로에 USDC 토큰 결제 미들웨어 적용
app.middleware("http")(
    require_payment(
        path="/premium/*",         # 와일드카드로 여러 경로 보호
        price=TokenAmount(
            amount="10000",        # 토큰 금액 (최소 단위)
            asset=TokenAsset(
                address="0x036CbD53842c5426634e7929541eC2318f3dCF7e",  # USDC 토큰 주소
                decimals=6,        # 토큰 소수점 자릿수
                eip712=EIP712Domain(
                    name="USDC",   # EIP-712 서명을 위한 토큰 이름
                    version="2"    # EIP-712 서명 버전
                ),
            ),
        ),
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

@app.get("/premium/content")
async def get_premium_content() -> Dict[str, Any]:
    return {
        "content": "This is premium content",
    }
```

### TokenAmount 설정 이해하기

- **amount**: 토큰의 최소 단위로 표현된 금액 (예: USDC는 6 decimals이므로 10000 = 0.01 USDC)
- **asset.address**: 토큰 컨트랙트 주소
- **asset.decimals**: 토큰 소수점 자릿수 (USDC는 6, DAI는 18)
- **asset.eip712**: EIP-712 서명 표준을 위한 도메인 정보

## 유료 엔드포인트 추가하기

새로운 유료 엔드포인트를 추가하려면 다음 패턴을 따르세요:

### 1. 간단한 USD 가격 엔드포인트

```python
# 미들웨어 설정
app.middleware("http")(
    require_payment(
        path="/api/data",
        price="$0.05",              # 5센트
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

# 엔드포인트 정의
@app.get("/api/data")
async def get_data():
    return {
        "data": "Your valuable data here"
    }
```

### 2. 경로 패턴을 사용한 여러 엔드포인트 보호

```python
# /api/v2/* 아래의 모든 엔드포인트 보호
app.middleware("http")(
    require_payment(
        path="/api/v2/*",
        price="$0.10",
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

@app.get("/api/v2/users")
async def get_users():
    return {"users": []}

@app.get("/api/v2/posts")
async def get_posts():
    return {"posts": []}
```

### 3. 다른 가격대의 여러 엔드포인트

```python
# 저가 엔드포인트
app.middleware("http")(
    require_payment(
        path="/basic/*",
        price="$0.01",
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

# 고가 엔드포인트
app.middleware("http")(
    require_payment(
        path="/premium/*",
        price="$1.00",
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

@app.get("/basic/info")
async def basic_info():
    return {"info": "Basic information"}

@app.get("/premium/analytics")
async def premium_analytics():
    return {"analytics": "Detailed analytics data"}
```

### 4. POST 요청 보호

```python
app.middleware("http")(
    require_payment(
        path="/api/process",
        price="$0.50",
        pay_to_address=ADDRESS,
        network="base-sepolia",
    )
)

@app.post("/api/process")
async def process_data(data: dict):
    # 데이터 처리 로직
    return {"result": "processed", "data": data}
```

## 미들웨어 설정 옵션

### require_payment 매개변수

- **path** (str): 보호할 경로 (와일드카드 `*` 지원)
- **price** (str | TokenAmount):
  - 문자열: USD 가격 (예: `"$0.10"`)
  - TokenAmount: 특정 토큰 금액
- **pay_to_address** (str): 결제를 받을 Ethereum 주소
- **network** (str): 블록체인 네트워크 (`"base"`, `"base-sepolia"` 등)

### 경로 패턴 규칙

```python
# 정확한 경로 매칭
path="/weather"              # /weather만 매칭

# 접두사 매칭
path="/api/*"                # /api/로 시작하는 모든 경로

# 중첩 경로
path="/api/v1/premium/*"     # /api/v1/premium/로 시작하는 모든 경로
```

## 서버 테스트하기

### 1. 무료 엔드포인트 테스트

서버에는 결제가 필요 없는 기본 엔드포인트가 있을 수 있습니다:

```bash
curl http://localhost:4021/
# 또는
curl http://localhost:4021/health
```

### 2. 유료 엔드포인트 테스트 (결제 없이)

결제 없이 요청하면 402 응답을 받습니다:

```bash
curl -v http://localhost:4021/weather
```

응답:
```
< HTTP/1.1 402 Payment Required
< x-accept-402: 1.0
< x-acceptpayment-address: 0xYourAddress
< x-acceptpayment-amount: 1000
< x-acceptpayment-asset: 0x036CbD53842c5426634e7929541eC2318f3dCF7e
...
```

### 3. x402 클라이언트로 테스트

x402 클라이언트를 사용하면 자동으로 결제가 처리됩니다:

```python
# requests 사용
from x402.clients import x402_requests
from eth_account import Account

account = Account.from_key("your_private_key")
session = x402_requests(account)
response = session.get("http://localhost:4021/weather")
print(response.json())
```

```python
# httpx 사용 (비동기)
from x402.clients import x402HttpxClient
from eth_account import Account

account = Account.from_key("your_private_key")

async with x402HttpxClient(
    account=account,
    base_url="http://localhost:4021"
) as client:
    response = await client.get("/weather")
    print(response.json())
```

### 4. 수동 결제 헤더로 테스트

고급 사용자는 수동으로 결제 헤더를 생성할 수 있습니다:

```bash
curl http://localhost:4021/weather \
  -H "x-payment-address: 0xYourAddress" \
  -H "x-payment-amount: 1000" \
  -H "x-payment-asset: 0x036CbD53842c5426634e7929541eC2318f3dCF7e" \
  -H "x-payment-signature: 0x..."
```

## 예제 코드 위치

```
external/x402/examples/python/legacy/servers/fastapi/
├── main.py           # FastAPI 서버 예제
├── .env-local        # 환경 변수 템플릿
└── pyproject.toml    # 프로젝트 의존성
```

## 주요 개념

### FastAPI 미들웨어

- **HTTP 미들웨어**: 모든 HTTP 요청을 가로채고 처리
- **경로 기반 필터링**: 특정 경로에만 결제 요구사항 적용
- **자동 402 응답**: 결제가 없는 요청에 자동으로 402 응답 반환
- **결제 검증**: 결제 서명을 자동으로 검증하고 처리

### 가격 설정 옵션

#### USD 가격 (권장)
```python
price="$0.10"  # 간단하고 직관적
```

- 자동으로 적절한 토큰으로 변환
- 가격 변동성으로부터 보호
- 사용자 친화적

#### 토큰 금액
```python
price=TokenAmount(
    amount="10000",
    asset=TokenAsset(...)
)
```

- 특정 토큰으로 결제 받기
- 정확한 금액 제어
- 커스텀 토큰 지원

### 네트워크 설정

- **base**: Base 메인넷 (프로덕션)
- **base-sepolia**: Base Sepolia 테스트넷 (개발/테스트)

### 보안 고려사항

1. **환경 변수**: 민감한 정보를 `.env` 파일에 보관하고 버전 관리에서 제외
2. **주소 검증**: ADDRESS 환경 변수가 설정되었는지 확인
3. **네트워크 매칭**: 클라이언트와 서버가 같은 네트워크를 사용하는지 확인
4. **HTTPS**: 프로덕션 환경에서는 HTTPS 사용 권장

## 실전 활용 예제

### AI API 서비스

```python
app.middleware("http")(
    require_payment(
        path="/ai/*",
        price="$0.02",  # 요청당 2센트
        pay_to_address=ADDRESS,
        network="base",
    )
)

@app.post("/ai/chat")
async def ai_chat(prompt: str):
    # AI 모델 호출
    response = await call_ai_model(prompt)
    return {"response": response}

@app.post("/ai/image")
async def ai_image(description: str):
    # 이미지 생성
    image_url = await generate_image(description)
    return {"image_url": image_url}
```

### 데이터 API 서비스

```python
# 무료 티어
@app.get("/data/sample")
async def sample_data():
    return {"data": "Limited sample data"}

# 유료 티어
app.middleware("http")(
    require_payment(
        path="/data/full",
        price="$0.50",
        pay_to_address=ADDRESS,
        network="base",
    )
)

@app.get("/data/full")
async def full_data():
    return {"data": "Complete dataset"}
```

### 계층별 가격 책정

```python
# 기본 티어 - $0.01
app.middleware("http")(
    require_payment(
        path="/tier/basic/*",
        price="$0.01",
        pay_to_address=ADDRESS,
        network="base",
    )
)

# 프로 티어 - $0.10
app.middleware("http")(
    require_payment(
        path="/tier/pro/*",
        price="$0.10",
        pay_to_address=ADDRESS,
        network="base",
    )
)

# 엔터프라이즈 티어 - $1.00
app.middleware("http")(
    require_payment(
        path="/tier/enterprise/*",
        price="$1.00",
        pay_to_address=ADDRESS,
        network="base",
    )
)
```

## 문제 해결

### 환경 변수 오류
```
ValueError: Missing required environment variables
```
**해결방법**: `.env` 파일에 ADDRESS가 설정되어 있는지 확인

### 포트 충돌
```
OSError: [Errno 48] Address already in use
```
**해결방법**: 다른 포트 사용
```python
uvicorn.run(app, host="0.0.0.0", port=4022)
```

### 클라이언트 연결 실패
**확인사항**:
1. 서버가 실행 중인지 확인
2. 방화벽 설정 확인
3. 올바른 URL 사용 (`http://localhost:4021`)

### 결제 검증 실패
**확인사항**:
1. 클라이언트와 서버가 같은 네트워크 사용
2. 토큰 주소가 정확한지 확인
3. 결제 금액이 정확한지 확인

## 다음 단계

- [requests 클라이언트 예제](./requests-client.ko.md) - 동기 클라이언트로 서버 테스트
- [httpx 클라이언트 예제](./httpx-client.ko.md) - 비동기 클라이언트로 서버 테스트
- [Discovery 예제](./discovery.ko.md) - x402 서비스 검색

## 추가 리소스

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [x402 프로토콜 사양](https://github.com/coinbase/x402)
- [Base 네트워크 문서](https://docs.base.org/)

---

[← v1 문서로 돌아가기](../README.md) | [v2 스펙 보기 →](../../../x402-v2-specification.ko.md)

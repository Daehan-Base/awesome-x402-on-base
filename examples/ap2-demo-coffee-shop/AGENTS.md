# AI Coffee Shop - Agent Architecture Guide

이 문서는 AI 에이전트가 Coffee Shop AP2 데모 프로젝트를 이해하고 수정할 때 참고할 수 있는 아키텍처 가이드입니다.

## 프로젝트 개요

**목적**: AP2 (Agent Payment Protocol)와 x402 결제 프로토콜을 사용하여 AI 에이전트가 커피를 주문하고 암호화폐로 결제하는 데모

**핵심 기술**:
- A2A (Agent-to-Agent) Protocol: 에이전트 간 통신 표준
- AP2: IntentMandate → CartMandate → PaymentMandate 흐름
- x402: EIP-712 서명 기반 USDC 결제 (Base Sepolia)
- Google ADK: AI 에이전트 프레임워크

## 디렉토리 구조

```
ap2-demo-coffee-shop/
├── client_agent/                 # 고객 AI 에이전트 (ADK Web UI용)
│   ├── __init__.py
│   ├── agent.py                  # 루트 에이전트 설정 (RemoteA2aAgent 연결)
│   └── coffee_client_agent.py    # 주문 도우미 에이전트 (도구 정의)
├── server/                       # 커피숍 서버 (A2A 엔드포인트)
│   ├── __init__.py
│   ├── __main__.py               # 서버 진입점 (Starlette + Uvicorn)
│   └── agents/
│       ├── __init__.py
│       ├── _adk_agent_executor.py  # ADK 에이전트를 A2A로 실행
│       ├── base_agent.py           # 에이전트 추상 클래스
│       ├── coffee_shop_agent.py    # 바리스타 에이전트 (핵심 로직)
│       ├── menu.py                 # 메뉴, 사이즈, 원두, 가격 계산
│       ├── routes.py               # A2A 라우팅 설정
│       └── x402_executor.py        # x402 결제 처리 (Facilitator 연동)
├── local_wallet.py               # 로컬 지갑 서비스 (EIP-712 서명)
├── pyproject.toml                # 의존성 및 프로젝트 설정
├── .env.example                  # 환경 변수 템플릿
└── README.md                     # 사용자 가이드
```

## 핵심 컴포넌트

### 1. Menu System (`server/agents/menu.py`)

메뉴, 사이즈, 원두 옵션 및 가격 계산 로직을 담당합니다.

```python
# 가격 단위: micro USDC (1 USDC = 1,000,000 micro USDC)
MENU = {
    "아메리카노": {"base_price": 45_000, ...},  # $0.045 (1/100 of $4.50)
    "카페라떼": {"base_price": 50_000, ...},    # $0.050 (1/100 of $5.00)
    ...
}

SIZES = {
    "Short": {"price_diff": -5_000, ...},   # -$0.005 (1/100 of $0.50)
    "Tall": {"price_diff": 0, ...},           # 기준
    "Grande": {"price_diff": 5_000, ...},   # +$0.005 (1/100 of $0.50)
    "Venti": {"price_diff": 10_000, ...},  # +$0.010 (1/100 of $1.00)
}

BEANS = {
    "일반": {"price_diff": 0, ...},
    "디카페인": {"price_diff": 3_000, ...},     # +$0.003 (1/100 of $0.30)
    "하프디카페인": {"price_diff": 3_000, ...}, # +$0.003 (1/100 of $0.30)
}

def calculate_price(drink, size, bean) -> int:
    """총 가격 계산 (micro USDC)"""
    return MENU[drink]["base_price"] + SIZES[size]["price_diff"] + BEANS[bean]["price_diff"]
```

**수정 시 주의사항**:
- 가격은 항상 micro USDC 단위 (정수)
- 새 메뉴 추가 시 `MENU` dict에 `base_price`, `description`, `description_en` 필수
- `validate_order()` 함수가 유효성 검사 담당

### 2. Coffee Shop Agent (`server/agents/coffee_shop_agent.py`)

바리스타 역할을 하는 서버 측 에이전트입니다.

**주요 도구**:
| 도구 | 설명 | 결제 필요 |
|------|------|----------|
| `get_menu()` | 메뉴판 반환 | ❌ |
| `create_order(drink, size, bean)` | CartMandate 생성 | ❌ |
| `process_payment(payment_mandate)` | 결제 처리 | ✅ |

**CartMandate 생성 흐름**:
```python
async def create_order(self, drink, size, bean):
    # 1. 가격 계산
    total_price = calculate_price(drink, size, bean)
    
    # 2. PaymentRequirements 생성 (x402)
    requirements = PaymentRequirements(
        scheme="exact",
        network="base-sepolia",
        asset="0x036CbD53842c5426634e7929541eC2318f3dCF7e",  # USDC
        pay_to=self._wallet_address,
        max_amount_required=str(total_price),
        ...
    )
    
    # 3. CartMandate 생성 및 서명
    cart_mandate = CartMandate(contents=cart_contents, merchant_authorization=signature)
    
    # 4. 세션에 requirements 저장 (나중에 결제 검증용)
    return {"artifact": ..., "context_to_save": {"payment_requirements": ...}}
```

**수정 시 주의사항**:
- `MERCHANT_WALLET_ADDRESS` 환경 변수 필수
- `context_to_save`로 반환된 데이터는 세션 상태에 저장됨
- `before_agent_callback`에서 세션 상태 로드

### 3. x402 Executor (`server/agents/x402_executor.py`)

Coinbase Facilitator를 통한 결제 검증 및 정산을 담당합니다.

```python
class CoffeeShopExecutor(x402ServerExecutor):
    async def verify_payment(self, payload, requirements) -> VerifyResponse:
        """결제 서명 검증 (off-chain)"""
        return await self._facilitator.verify(payload, requirements)
    
    async def settle_payment(self, payload, requirements) -> SettleResponse:
        """결제 정산 (on-chain USDC 전송)"""
        return await self._facilitator.settle(payload, requirements)
```

**Facilitator URL**: `https://x402.org/facilitator` (기본값)

**수정 시 주의사항**:
- `x402ServerExecutor`를 상속하여 `verify_payment`, `settle_payment` 구현
- 실제 결제가 발생하므로 테스트넷(Base Sepolia)에서만 테스트

### 4. Coffee Client Agent (`client_agent/coffee_client_agent.py`)

고객 측 주문 도우미 에이전트입니다.

**주요 도구**:
| 도구 | 설명 |
|------|------|
| `create_intent_mandate()` | 주문 의향서 생성 |
| `sign_intent_mandate()` | 의향서 서명 |
| `save_cart_and_inform_user()` | 장바구니 저장 및 안내 |
| `pay_for_cart()` | EIP-712 결제 요청 생성 |
| `sign_payment_request()` | 결제 요청 서명 |
| `create_payment_mandate()` | 결제 승인서 생성 |
| `sign_payment_mandate()` | 최종 승인 서명 |

**EIP-712 Typed Data 생성**:
```python
typed_data = get_transfer_with_auth_typed_data(
    from_=self._wallet_address,
    to=pay_to_address,
    value=amount_micro_usdc,
    valid_after=timestamp,
    valid_before=timestamp + 1hour,
    nonce=random_hex,
    chain_id=84532,  # Base Sepolia
    contract_address=usdc_address,
    token_name="USD Coin",
    token_version="2",
)
```

### 5. Local Wallet (`local_wallet.py`)

테스트용 로컬 지갑 서비스입니다.

**엔드포인트**:
| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/address` | GET | 지갑 주소 반환 |
| `/sign` | POST | 페이로드 서명 (EIP-712 또는 일반) |

**서명 타입 자동 감지**:
```python
if all(key in payload for key in ["types", "domain", "message", "primaryType"]):
    # EIP-712 서명 (결제용)
    signable_message = encode_typed_data(full_message=payload)
else:
    # 일반 문자열 서명 (mandate용)
    message = encode_defunct(text=payload_str)
```

## AP2 결제 흐름

```
User → Client Agent → Coffee Shop Agent → Facilitator → Blockchain

1. IntentMandate: 사용자 주문 의향
   {"natural_language_description": "Grande 디카페인 아메리카노 1잔", ...}

2. CartMandate: 상점의 주문 확인 + 가격
   {"contents": {"payment_request": {...}, "merchant_name": "..."}, "merchant_authorization": "0x..."}

3. PaymentMandate: 사용자의 결제 승인
   {"payment_mandate_contents": {"payment_response": {"details": {x402_payload}}}, "user_authorization": "0x..."}

4. Settlement: 블록체인에서 USDC 전송
   facilitator.settle() → transferWithAuthorization() on USDC contract
```

## 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `GOOGLE_API_KEY` | ✅ | Gemini API 키 |
| `CLIENT_PRIVATE_KEY` | ✅ | 고객 지갑 Private Key |
| `MERCHANT_WALLET_ADDRESS` | ✅ | 상점 지갑 주소 |
| `LOCAL_WALLET_URL` | ❌ | 지갑 서비스 URL (기본: `http://localhost:5001`) |
| `RPC_URL` | ❌ | Base Sepolia RPC (기본: `https://sepolia.base.org`) |

## 실행 순서

```bash
# 1. 환경 변수 설정
cp .env.example .env
# .env 편집

# 2. 의존성 설치
uv sync

# 3. 지갑 서비스 시작 (Terminal 1)
uv run python local_wallet.py

# 4. 커피숍 서버 시작 (Terminal 2)
uv run server

# 5. 클라이언트 에이전트 시작 (Terminal 3)
uv run adk web
```

## 수정 가이드

### 새 메뉴 추가

`server/agents/menu.py`:
```python
MENU["새메뉴"] = {
    "base_price": 5_500_000,  # $5.50
    "description": "설명 (한국어)",
    "description_en": "Description (English)",
}
```

### 새 옵션 추가

사이즈나 원두 외의 새 옵션(예: 샷 추가)을 추가하려면:

1. `menu.py`에 새 옵션 dict 추가
2. `calculate_price()` 함수 수정
3. `validate_order()` 함수 수정
4. `coffee_shop_agent.py`의 `create_order()` 파라미터 추가
5. `coffee_client_agent.py`의 instruction 업데이트

### 다른 네트워크 지원

`coffee_shop_agent.py`에서 `PaymentRequirements` 수정:
```python
requirements = PaymentRequirements(
    network="base-mainnet",  # 또는 다른 네트워크
    asset="0x...",  # 해당 네트워크의 USDC 주소
    ...
)
```

## 디버깅 팁

1. **서버 로그 확인**: `uv run server` 출력에서 요청/응답 확인
2. **ADK Trace**: `http://127.0.0.1:8000`의 Debug 탭에서 에이전트 실행 추적
3. **지갑 로그**: `local_wallet.py` 출력에서 서명 요청 확인
4. **Facilitator 응답**: `verify_payment`, `settle_payment` 결과 로깅

## 관련 파일

- `/spec/v0.2/spec.md`: x402 프로토콜 스펙
- `/python/x402_a2a/`: x402-a2a 라이브러리 소스
- `/python/examples/ap2-demo/`: 원본 AP2 데모 (참고용)


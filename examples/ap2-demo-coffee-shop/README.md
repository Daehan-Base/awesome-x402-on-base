# ☕ AI Coffee Shop - AP2 & x402 Demo

AI 에이전트가 커피를 주문하고 암호화폐로 결제하는 데모입니다. AP2 (Agent Payment Protocol)와 x402 결제 프로토콜을 사용합니다.

## 개요

이 데모는 다음을 보여줍니다:

- **A2A (Agent-to-Agent) 통신**: 클라이언트 에이전트와 커피숍 에이전트 간의 표준화된 통신
- **AP2 프로토콜**: IntentMandate → CartMandate → PaymentMandate 흐름
- **x402 결제**: EIP-712 서명을 통한 USDC 결제 (Base Sepolia 테스트넷)
- **커스터마이징**: 사이즈(Short/Tall/Grande/Venti)와 원두(일반/디카페인) 옵션

## 구성 요소

```
ap2-demo-coffee-shop/
├── client_agent/          # 고객 AI 에이전트 (ADK Web UI)
│   ├── agent.py           # 루트 에이전트 설정
│   └── coffee_client_agent.py  # 주문 도우미 에이전트
├── server/                # 커피숍 서버
│   ├── __main__.py        # 서버 진입점
│   └── agents/
│       ├── coffee_shop_agent.py  # 바리스타 에이전트
│       ├── x402_executor.py      # x402 결제 처리
│       ├── menu.py               # 메뉴 및 가격
│       └── routes.py             # A2A 라우팅
└── local_wallet.py        # 로컬 지갑 서비스
```

## 메뉴

### 음료 (Tall 기준)

| 메뉴 | 가격 | 설명 |
|------|------|------|
| 아메리카노 | $0.045 | 진한 에스프레소 |
| 카페라떼 | $0.050 | 부드러운 우유와 에스프레소 |
| 카푸치노 | $0.055 | 풍성한 거품 |
| 바닐라라떼 | $0.060 | 달콤한 바닐라 향 |
| 카라멜마끼아또 | $0.065 | 달콤한 카라멜 드리즐 |
| 모카 | $0.060 | 초콜릿과 에스프레소의 조화 |

### 사이즈 옵션

| 사이즈 | 용량 | 가격 차이 |
|--------|------|-----------|
| Short | 237ml | -$0.005 |
| Tall | 355ml | 기준 |
| Grande | 473ml | +$0.005 |
| Venti | 591ml | +$0.010 |

### 원두 옵션

| 원두 | 가격 차이 | 설명 |
|------|-----------|------|
| 일반 | $0 | 하우스 블렌드 |
| 디카페인 | +$0.003 | 카페인 제거 |
| 하프디카페인 | +$0.003 | 50% 디카페인 |

## 사전 요구사항

- **Python 3.13+**: `python --version`으로 확인
- **uv 패키지 매니저**: `pip install uv`로 설치

## 설치

```bash
cd examples/ap2-demo-coffee-shop

# 사전 요구사항 확인
python --version  # Python 3.13+ 필요
uv --version      # uv 패키지 매니저 필요

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 필요한 값을 설정하세요

# 의존성 설치
uv sync
```

## 실행

3개의 터미널이 필요합니다:

### Terminal 1: Local Wallet

```bash
cd examples/ap2-demo-coffee-shop
uv run python local_wallet.py
```

지갑 서비스가 `http://localhost:5001`에서 실행됩니다.

### Terminal 2: Coffee Shop Server

```bash
cd examples/ap2-demo-coffee-shop
uv run server
```

커피숍 서버가 `http://localhost:10000`에서 실행됩니다.

### Terminal 3: Client Agent (ADK Web UI)

```bash
cd examples/ap2-demo-coffee-shop
uv run adk web
```

브라우저에서 `http://localhost:8000`을 열어 AI와 대화하세요.

## 사용 예시

```
사용자: 아메리카노 한 잔 주세요

AI: 아메리카노 주문이시네요! ☕ 사이즈는 어떻게 할까요? 
    (Short/Tall/Grande/Venti, 기본: Tall)

사용자: 그란데로요

AI: 원두는 일반, 디카페인, 하프디카페인 중에서 선택해주세요. (기본: 일반)

사용자: 디카페인으로요

AI: Grande 디카페인 아메리카노로 주문하시겠습니까?

사용자: 네

AI: ☕ 주문 의향서를 생성했습니다:
    📝 "Grande 디카페인 아메리카노 1잔"
    주문을 확정하려면 '주문 확정'이라고 말씀해주세요.

사용자: 주문 확정

AI: ✅ 주문 의향서에 서명했습니다. 커피숍에 전달하겠습니다!

(커피숍에서 CartMandate 수신)

AI: ☕ AI Coffee Shop에서 주문을 준비했습니다!
    📋 주문 내역:
      - Grande 디카페인 아메리카노: $0.053
    💰 총 금액: $0.053 USD
    결제를 진행하시려면 '결제할게요'라고 말씀해주세요.

사용자: 결제할게요

AI: 💳 $0.053 USDC 결제를 준비했습니다.
    결제를 승인하려면 '결제 승인'이라고 말씀해주세요.

사용자: 결제 승인

AI: ✅ 결제 승인서를 생성했습니다.
    최종 승인을 위해 '최종 승인'이라고 말씀해주세요.

사용자: 최종 승인

AI: ✅ 결제가 완료되었습니다! 
    ☕ 음료를 준비하겠습니다. 잠시만 기다려주세요!
```

## 결제 흐름

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  Client Agent   │         │  Coffee Shop    │         │  Facilitator    │
│  (고객 AI)      │         │  Agent (바리스타)│         │  (x402.org)     │
└────────┬────────┘         └────────┬────────┘         └────────┬────────┘
         │                           │                           │
         │  1. IntentMandate         │                           │
         │  (주문 의향)              │                           │
         │ ────────────────────────► │                           │
         │                           │                           │
         │  2. CartMandate           │                           │
         │  (장바구니 + 가격)        │                           │
         │ ◄──────────────────────── │                           │
         │                           │                           │
         │  3. PaymentMandate        │                           │
         │  (EIP-712 서명)           │                           │
         │ ────────────────────────► │                           │
         │                           │                           │
         │                           │  4. verify()              │
         │                           │ ────────────────────────► │
         │                           │                           │
         │                           │  5. settle()              │
         │                           │ ────────────────────────► │
         │                           │                           │
         │                           │  (USDC 전송 on-chain)     │
         │                           │ ◄──────────────────────── │
         │                           │                           │
         │  6. 주문 완료             │                           │
         │ ◄──────────────────────── │                           │
         │                           │                           │
```

## 테스트 준비

### 1. 테스트 지갑 생성

테스트용 지갑을 생성하고 Private Key를 `.env`에 설정하세요.

### 2. Base Sepolia ETH 받기

[Coinbase Faucet](https://www.coinbase.com/faucets/base-ethereum-sepolia-faucet)에서 테스트 ETH를 받으세요.

### 3. 테스트 USDC 받기

[Circle Faucet](https://faucet.circle.com/)에서 Base Sepolia USDC를 받으세요.


## 기술 스택

- **Python 3.13+**
- **uv**: 최신 Python 패키지 매니저
- **Google ADK**: AI 에이전트 프레임워크
- **A2A Protocol**: 에이전트 간 통신 표준
- **AP2**: 에이전트 결제 프로토콜
- **x402**: HTTP 402 기반 결제 프로토콜
- **Base Sepolia**: 이더리움 L2 테스트넷
- **USDC**: 스테이블코인 결제

## 라이선스

Apache License 2.0


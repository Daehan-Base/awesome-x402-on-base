# awesome-x402-on-base

> Base 체인에서 x402 프로토콜을 사용하기 위한 한국어 리소스, 도구, 지식 모음

**관리자**: Logan (Base Korea Developer Ambassador)
**라이선스**: MIT License
**작성일**: 2025-11-09

---

## 📋 프로젝트 개요

### 목적
- **What**: Base 체인에서 x402 결제 프로토콜을 사용하기 위한 한국어 가이드 및 문서
- **Why**: 공식 x402 예제(이미 Base 사용)에 대한 상세한 한글 튜토리얼 제공
- **How**: Git 서브모듈로 공식 코드 연결 + 한글 가이드 작성 + Base 특화 예제
- **Target**: 한국 개발자 & Base 특화 x402 구현에 관심있는 글로벌 빌더

### 핵심 가치
1. **x402 프로토콜**: HTTP 402 "Payment Required" 상태 코드를 활용한 마이크로페이먼트
   - 약 2초 내 빠른 결제 처리
   - 거래 수수료 < $0.0001
   - 최소 $0.001 결제 가능
   - AI 에이전트 및 IoT 기기의 기계간 자율 결제

2. **Base 체인 최적화**
   - 높은 성능: 빠른 최종성과 낮은 지연시간
   - 최소 가스비: x402 거래 비용 < $0.0001
   - 이더리움 L2 보안
   - 네이티브 USDC 결제 통화

3. **한국어 문서화**
   - Web2 개발자를 위한 Web3 교육
   - 단계별 튜토리얼 및 실습 예제
   - 보안 가이드라인 및 Best Practices

---

## 📁 레포지토리 구조

```
awesome-x402-on-base/
├── external/x402/          # 🔗 Git 서브모듈 (공식 x402 레포지토리)
│   ├── python/             # Python SDK
│   ├── typescript/         # TypeScript SDK
│   ├── examples/           # 공식 예제 (Python, TS, Go)
│   └── specs/              # 프로토콜 스펙
│
├── examples/               # 📝 Base 특화 예제
│   ├── README.md           # 예제 허브
│   ├── v1/                 # v1 Legacy 예제
│   │   ├── ap2-demo-coffee-shop/  # AI 커피숍 데모
│   │   └── README.md
│   └── v2/                 # v2 예제 (준비 중)
│       └── README.md
│
├── docs/korean/            # 🇰🇷 한국어 문서
│   ├── README.md                     # 한국어 문서 허브
│   ├── getting_started.ko.md         # 시작 가이드
│   ├── x402-v2-specification.ko.md   # v2 프로토콜 스펙
│   ├── v1/                           # v1 Legacy 문서
│   │   ├── README.md
│   │   └── examples/
│   │       ├── python-requests-client.ko.md
│   │       ├── python-httpx-client.ko.md
│   │       ├── python-fastapi-server.ko.md
│   │       └── python-discovery.ko.md
│   └── v2/                           # v2 문서
│       └── README.md
│
├── README.md               # 프로젝트 소개 (한글/영문)
├── ROADMAP.md              # 개발 로드맵
├── LICENSE                 # MIT 라이선스
├── CLAUDE.md               # Claude Code 컨텍스트 (이 파일)
└── .cursor/rules           # Cursor AI 규칙
```

### 디렉토리 역할

**`external/x402/`** (읽기 전용)
- Coinbase 공식 x402 코드 참조
- Git 서브모듈, 절대 수정 금지
- 업데이트: `git submodule update --remote external/x402`

**`examples/v1/`** (v1 Legacy 예제)
- x402 v1 SDK 기반 예제
- ap2-demo-coffee-shop: AI 커피숍 데모
- 커뮤니티 기여 환영

**`examples/v2/`** (v2 예제 - 준비 중)
- x402 v2 SDK 기반 예제
- 공식 예제는 `external/x402/examples/typescript/`에서 참조

**`docs/korean/`** (활발히 작성 중)
- 한국 개발자를 위한 단계별 가이드
- v1/v2 버전별 문서 분리
- `v1/examples/`: v1 Legacy Python 예제 튜토리얼
- `x402-v2-specification.ko.md`: v2 프로토콜 스펙

---

## 🎯 핵심 개념

### 1. x402 프로토콜
**정의**: HTTP 402 Payment Required 상태 코드를 활용한 암호화폐 결제 프로토콜

**동작 원리**:
1. 클라이언트 → 서버: HTTP 요청
2. 서버 → 클라이언트: 402 응답 (결제 정보 포함)
3. 클라이언트: 결제 서명 생성
4. 클라이언트 → 서버: 결제 헤더와 함께 재요청
5. 서버: 결제 검증 → 리소스 제공

**버전별 차이**:
- **v1 (Legacy)**: `X-PAYMENT` 헤더, `base-sepolia` 네트워크 형식
- **v2 (Current)**: `PAYMENT-SIGNATURE` 헤더, `eip155:84532` CAIP 표준

**특징**:
- Gasless: 클라이언트와 서버는 가스비 부담 없음
- 빠름: ~2초 결제 완료
- 저비용: 거래 수수료 < $0.0001
- 마이크로페이먼트: 최소 $0.001 결제

### 2. Base 체인
**설명**: Coinbase가 Ethereum 위에 구축한 L2 블록체인

**네트워크**:
- `base-sepolia` (84532): 테스트넷, 무료 토큰 획득 가능
- `base` (8453): 메인넷, 실제 USDC 결제

**특징**:
- EVM 호환 (Ethereum Virtual Machine)
- 초저비용 가스비
- 빠른 최종성 (~2초)
- CDP Platform 통합

### 3. CDP Platform (Coinbase Developer Platform)
**구성 요소**:
- **API Key**: CDP API 인증 (ID + Secret)
- **Wallet Secret**: 서버 월렛 제어 (TEE 기반)
- **Server Wallet**: 비수탁형 월렛 서비스
- **Facilitator**: x402 리소스 중앙 레지스트리

### 4. Web3 지갑 (Wallet vs Account)
**Web2 비유**:
```
지갑 (Wallet) = Gmail 앱 (여러 계정 관리 도구)
계정 (Account) = user@gmail.com (개별 이메일 주소)
Recovery Phrase = 마스터 키 (모든 계정 복구)
Private Key = 특정 방 열쇠 (한 계정만 복구)
```

**핵심 차이**:
- 1개 Recovery Phrase → 여러 Private Key 생성 가능
- Recovery Phrase 유출 = 모든 계정 탈취
- Private Key 유출 = 해당 계정만 탈취

### 5. USDC (USD Coin)
**설명**: 1 USDC = 1 USD 고정 스테이블코인

**x402에서의 역할**:
- 기본 결제 통화
- 가격 안정성 (암호화폐 변동성 제거)
- Base 체인 네이티브 지원

### 6. x402 v1 vs v2

| 항목 | v1 (Legacy) | v2 (Current) |
|------|------------|--------------|
| HTTP 헤더 | `X-PAYMENT` | `PAYMENT-SIGNATURE` |
| 네트워크 형식 | `base-sepolia` | `eip155:84532` (CAIP) |
| 버전 필드 | `x402Version: 1` | `x402Version: 2` |
| SDK 구조 | 단일 `x402` 패키지 | 모듈형 `@x402/*` |
| 문서 위치 | `docs/korean/v1/` | `docs/korean/v2/` |
| 예제 위치 | `examples/v1/` | `examples/v2/` |

**v2 주요 특징**:
- 멀티체인 지원 (Base, Solana, EVM 체인)
- MCP/A2A 전송 프로토콜
- ERC-1271, ERC-6492 스마트 컨트랙트 지갑 지원
- CAIP 표준 기반 네트워크/자산 식별

---

## 🛠️ 기술 스택

### Python (3.10+)
**코어 라이브러리**:
- `x402` - x402 프로토콜 Python SDK
- `eth-account` (≥0.13.7) - 지갑 관리 및 서명
- `web3` (≥6.0.0) - 블록체인 상호작용

**웹 프레임워크**:
- `fastapi` (≥0.115.12) - 비동기 API 프레임워크
- `flask` - 경량 웹 프레임워크

**HTTP 클라이언트**:
- `requests` - 동기식 HTTP 클라이언트
- `httpx` - 비동기 HTTP 클라이언트

**개발 도구**:
- `uv` - 패키지 관리자 (권장)
- `pytest` - 테스팅 프레임워크

### TypeScript (Node.js ≥18.0.0)
**코어 라이브러리**:
- `x402` - x402 프로토콜 TypeScript SDK
- `viem` (^2.21.26) - Ethereum 상호작용
- `@coinbase/cdp-sdk` - CDP Platform SDK

**웹 프레임워크 & 미들웨어**:
- `x402-express` - Express.js 통합
- `x402-next` - Next.js 통합
- `x402-hono` - Hono 프레임워크 통합

**개발 도구**:
- `pnpm` (≥10.7.0) - 패키지 관리자 (필수)
- `turbo` - 모노레포 빌드 시스템
- `typescript` (^5.8.3)

### 블록체인
- **Base Sepolia**: 테스트넷 (네트워크 ID: 84532)
- **Base Mainnet**: 프로덕션 (네트워크 ID: 8453)
- **USDC**: 결제 통화

### 버전 관리
- **Git**: 서브모듈 지원 필수
- **GitHub**: 레포지토리 호스팅

---

## 📜 개발 가이드라인

### 🚫 절대 규칙 (MUST NOT)

1. **`external/x402/` 수정 금지**
   - 공식 x402 레포지토리는 읽기 전용
   - Git 서브모듈이므로 직접 수정하면 안 됨
   - 모든 커스터마이징은 루트의 `examples/` 또는 `docs/`에서 수행

2. **Private Key 커밋 금지**
   - `.env` 파일 절대 커밋 금지
   - Private Key를 코드에 하드코딩 금지
   - Git history에 Private Key가 들어가면 영구적 위험

3. **메인넷 키를 개발에 사용 금지**
   - 개발/테스트는 Base Sepolia 사용
   - 메인넷 Private Key는 프로덕션 배포 시에만 사용
   - 개발용 지갑과 실제 자산 지갑 분리

### ✅ 권장 사항 (SHOULD)

1. **한글 가이드 먼저 확인**
   - `docs/korean/getting_started.ko.md`에서 시작
   - v1 예제 튜토리얼: `docs/korean/v1/examples/`
   - v2 스펙 문서: `docs/korean/x402-v2-specification.ko.md`

2. **공식 예제 패턴 따르기**
   - `external/x402/examples/`에서 표준 구현 패턴 학습
   - Base 특화 예제는 `examples/v1/` 또는 `examples/v2/`에 구현

3. **Base Sepolia 테스트넷 사용**
   - 무료 테스트 토큰 획득: [QuickNode Faucet](https://faucet.quicknode.com/base/sepolia)
   - USDC 테스트 토큰: [Circle Faucet](https://faucet.circle.com/)

4. **환경 변수 안전 관리**
   - `.env` 파일 사용 (`.gitignore`에 포함됨)
   - `.env.example` 템플릿 제공 (민감 정보 제거)

5. **커뮤니티 기여**
   - Base 특화 예제는 `examples/base-specific/`에 추가
   - 한글 문서 개선은 `docs/korean/`에 기여
   - Pull Request 제출 환영

---

## 📚 문서 구조

### getting_started.ko.md
**역할**: Web2 개발자를 위한 x402 + Base 체인 진입 가이드

**주요 내용**:
- CDP Platform 계정 설정
- API 키 및 Wallet Secret 생성
- Web3 지갑 기본 개념 (MetaMask, Base Wallet)
- Private Key 보안 교육
- 환경 변수 설정
- 테스트 자금 획득

### x402-v2-specification.ko.md
**역할**: x402 v2 프로토콜 상세 스펙 (2025-12-11 출시)

**주요 내용**:
- v2 프로토콜 아키텍처
- HTTP/MCP/A2A 전송 프로토콜
- CAIP 표준 기반 네트워크/자산 식별
- ERC-1271, ERC-6492 스마트 컨트랙트 지갑 지원
- v1 vs v2 마이그레이션 가이드

### v1/examples/ (4개 실습 예제 문서 - Legacy)

**python-requests-client.ko.md**
- 간단한 방식: `x402_requests`
- 확장 가능한 방식: `x402_http_adapter`
- 동기 HTTP 클라이언트 구현

**python-httpx-client.ko.md**
- 비동기 클라이언트: `x402HttpxClient`
- 이벤트 훅: `x402_payment_hooks`
- `async/await` 패턴 및 동시성

**python-fastapi-server.ko.md**
- 유료 API 엔드포인트 구현
- USD 가격 vs 토큰 금액 설정
- 경로 패턴 기반 보호

**python-discovery.ko.md**
- x402 리소스 자동 검색
- Facilitator 클라이언트 사용
- 동적 서비스 연결 패턴

### 학습 경로
```
1단계: getting_started.ko.md (환경 설정)
    ↓
2단계: v1/examples/python-requests-client.ko.md (동기 클라이언트)
    ↓
3단계: v1/examples/python-httpx-client.ko.md (비동기 클라이언트)
    ↓
4단계: v1/examples/python-fastapi-server.ko.md (서버 구현)
    ↓
5단계: v1/examples/python-discovery.ko.md (고급 기능)
    ↓
6단계: x402-v2-specification.ko.md (v2 프로토콜 이해)
    ↓
7단계: Base Mainnet 배포 (준비 중)
```

---

## 🗂️ 중요 경로

### 한글 가이드
- `docs/korean/getting_started.ko.md` - 시작 가이드
- `docs/korean/x402-v2-specification.ko.md` - v2 프로토콜 스펙
- `docs/korean/v1/examples/` - v1 Python 예제 튜토리얼 (4개)
- `docs/korean/v2/` - v2 문서 (준비 중)

### 공식 예제 (읽기 전용)
- `external/x402/examples/python/legacy/` - Python v1 예제
- `external/x402/examples/typescript/` - TypeScript v2 예제
- `external/x402/examples/go/` - Go v2 예제

### Base 특화 예제
- `examples/v1/` - v1 Legacy 예제 (ap2-demo-coffee-shop)
- `examples/v2/` - v2 예제 (준비 중)

### 프로젝트 문서
- `README.md` - 프로젝트 소개 (한글/영문)
- `ROADMAP.md` - 개발 로드맵

---

## 🔒 보안 규칙 (CRITICAL)

### Private Key 보안 (최우선)

#### ❌ 절대 하지 말 것
1. **Git 커밋**: `.env` 파일 절대 커밋 금지
2. **콘솔 출력**: `console.log(privateKey)`, `print(private_key)` 금지
3. **하드코딩**: 코드에 Private Key 직접 입력 금지
4. **공개 공유**: Slack, Discord 등에 공유 금지
5. **화면 공유**: 스크린샷, 화면 공유 시 Private Key 노출 금지

#### ✅ 해야 할 것
1. **환경 변수**: `.env` 파일 + `.gitignore`
2. **지갑 분리**: 개발용 지갑 (소액만 보관) vs 실제 자산 지갑
3. **테스트넷 사용**: Base Sepolia에서 개발
4. **비밀번호 관리자**: 1Password, Bitwarden 등 사용

### 긴급 대응

**Private Key 유출 시**:
1. 즉시 새 지갑 생성
2. 남은 자산 이동 (ETH → USDC)
3. 유출된 지갑 사용 중단
4. 관련 API 키 갱신

### 네트워크 보안
- **개발**: `base-sepolia` (테스트넷, 무료 토큰)
- **프로덕션**: `base` (메인넷, 실제 USDC)
- 클라이언트/서버 네트워크 일치 확인

### .gitignore 보안 패턴
```gitignore
# 환경 변수 (Critical)
.env
.env.local
.env.*.local
*.env

# 개인 키 및 인증서 (Critical)
*.pem
*.key
*.cert
credentials.json
secrets.json
```

### Recovery Phrase vs Private Key

| 항목 | Recovery Phrase | Private Key |
|------|-----------------|-------------|
| 형태 | 12-24 단어 | 64자 16진수 |
| 복구 범위 | 전체 지갑 | 해당 계정만 |
| 중요도 | 매우 높음 | 높음 |

### 환경 변수 관리

**필수 설정** (`.env` 파일):
```bash
# CDP Platform
CDP_API_KEY_ID=
CDP_API_KEY_SECRET=
CDP_WALLET_SECRET=

# 개발용 지갑 (Base Sepolia)
PRIVATE_KEY=

# 네트워크 (테스트넷)
NETWORK=base-sepolia
```

**템플릿 제공** (`.env.example`):
- 민감 정보 제거
- 주석으로 설명 추가
- Git 커밋 가능

---

## 🚫 디렉토리 규칙

### 읽기 전용 (NEVER MODIFY)
- **`external/x402/`**: Git 서브모듈, 절대 수정 금지
  - 공식 x402 레포지토리 참조용
  - 업데이트: `git submodule update --remote external/x402`
  - 모든 커스터마이징은 루트 `examples/`에서 수행

### 쓰기 가능 (CAN MODIFY)
- **`docs/korean/`**: 한글 문서 작성
  - 시작 가이드, 예제 튜토리얼
  - Web2 → Web3 교육 방식
  - 타임스탬프 및 업데이트 경고 포함

- **`examples/v1/`**: v1 Legacy 예제
  - x402 v1 SDK 기반 데모
  - ap2-demo-coffee-shop 등

- **`examples/v2/`**: v2 예제 (준비 중)
  - x402 v2 SDK 기반 예제
  - 커뮤니티 기여 환영

---

## 💻 코드 작성 규칙

### Python (3.10+)
**패키지 관리자**: `uv` (권장)

**코드 스타일**:
- Type hints 사용 권장
- Async/await 패턴 (FastAPI, httpx)
- 환경 변수로 설정 로드 (하드코딩 금지)

**예제 실행**:
```bash
cd external/x402/examples/python/legacy/clients/requests
cp .env-local .env
# .env 파일에 Private Key 추가
uv sync
uv run python main.py
```

### TypeScript (Node.js ≥18.0.0)
**패키지 관리자**: `pnpm` (≥10.7.0, 필수)

**코드 스타일**:
- TypeScript 엄격 모드
- ESM (ECMAScript Modules)
- Async/await 패턴

### 환경 변수
**템플릿 제공** (`.env.example`):
- 민감 정보 제거
- 주석으로 설명 추가
- Git 커밋 가능

---

## 🔄 작업 워크플로우

### 프로젝트 클론 및 초기화

```bash
# 서브모듈과 함께 클론
git clone --recursive https://github.com/Daehan-Base/awesome-x402-on-base.git

# 또는 이미 클론한 경우
git submodule update --init --recursive
```

### 서브모듈 업데이트

```bash
# 최신 공식 예제 가져오기
git submodule update --remote external/x402

# 변경사항 확인
cd external/x402
git log -3
cd ../..
```

### Python 개발 환경 설정

```bash
# 가상 환경 생성
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 의존성 설치
pip install requests httpx fastapi uvicorn web3 eth-account
```

### 예제 실행

```bash
# Python requests 클라이언트
cd external/x402/examples/python/legacy/clients/requests
cp .env-local .env
# .env 파일에 Private Key 추가
uv sync
uv run python main.py
```

### 한글 가이드 작성

```bash
# 새 v1 가이드 작성
cd docs/korean/v1/examples
# 템플릿을 참고하여 새 .ko.md 파일 작성
# 타임스탬프 및 업데이트 경고 포함

# 또는 v2 문서 작성
cd docs/korean/v2
```

### Base 특화 예제 추가

```bash
# v1 예제 추가
cp -r external/x402/examples/python/legacy/servers/fastapi examples/v1/
# Base 최적화 적용 (가스비, USDC 통합)
# README.md 작성

# v2 예제 추가
cp -r external/x402/examples/typescript/servers examples/v2/
```

---

## 📝 한글 문서 작성 가이드

### 문서 템플릿

```markdown
# [제목]

> **작성 시점**: YYYY년 MM월 DD일
> **최종 검증**: CDP Platform YYYY년 MM월 기준
> ⚠️ **중요**: UI/프로세스 변경 가능, Issue나 PR로 기여 요청

## 개요
[목적 및 대상 사용자]

## 사전 요구사항
- [ ] 항목 1
- [ ] 항목 2

## 1단계: [제목]
[설명]

```bash
# 코드 예제
```

## 주요 개념
### [개념 1]
[Web2 비유 활용]

## 문제 해결
### [문제 제목]
**증상**: [설명]
**해결 방법**: [단계별]

## 다음 단계
- [관련 문서 링크]
```

### 작성 원칙

1. **Web2 비유 우선**
   - Gmail 앱 = 지갑, user@gmail.com = 계정
   - 친숙한 예시로 복잡한 개념 설명

2. **시각적 구조**
   - 화살표 (`→`), 체크리스트 (`- [ ]`)
   - 표, 코드 블록 적극 활용

3. **보안 경고 강조**
   - ⚠️ 이모지, 경고 블록
   - ✅/❌로 올바른/잘못된 예제 구분

4. **한글 전문 용어**
   - 병기: "지갑 (Wallet)", "계정 (Account)"
   - Private Key, Recovery Phrase는 번역 안 함

5. **타임스탬프 명시**
   - 작성 시점 기록
   - UI 변경 가능성 경고
   - 커뮤니티 기여 독려

---

## 📚 학습 경로

### 초보자 → 고급

```
1. docs/korean/getting_started.ko.md
   └─ CDP Platform 계정, 지갑 설정, 환경 변수
      ↓
2. docs/korean/v1/examples/python-requests-client.ko.md
   └─ 동기 HTTP 클라이언트 (v1 Legacy)
      ↓
3. docs/korean/v1/examples/python-httpx-client.ko.md
   └─ 비동기 클라이언트 (v1 Legacy)
      ↓
4. docs/korean/v1/examples/python-fastapi-server.ko.md
   └─ 유료 API 서버 구현 (v1 Legacy)
      ↓
5. docs/korean/v1/examples/python-discovery.ko.md
   └─ x402 서비스 자동 검색 (v1 Legacy)
      ↓
6. docs/korean/x402-v2-specification.ko.md
   └─ v2 프로토콜 이해
      ↓
7. examples/v2/ (준비 중)
   └─ Base Mainnet 배포, AI 에이전트 통합
```

---

## ⚡ 빠른 참조

### 핵심 개념

**x402 프로토콜**:
- HTTP 402 Payment Required 기반
- ~2초 결제 완료, 수수료 < $0.0001
- 마이크로페이먼트 ($0.001 최소)

**Base 체인**:
- Ethereum L2, EVM 호환
- 저비용, 빠른 최종성
- 네이티브 USDC 지원

**CDP Platform**:
- API Key: CDP API 인증
- Wallet Secret: 서버 월렛 제어 (TEE)
- Facilitator: x402 리소스 레지스트리

### 금지 사항
- ❌ `external/x402/` 수정
- ❌ Private Key 커밋
- ❌ 메인넷 키를 개발에 사용
- ❌ 공개 채널에 Private Key 공유

### 권장 사항
- ✅ 한글 가이드 먼저 확인
- ✅ Base Sepolia 테스트넷 사용
- ✅ `.env` + `.gitignore`
- ✅ 개발/프로덕션 지갑 분리
- ✅ 커뮤니티 기여 환영

---

## 🚀 개발 로드맵

- **Phase 1** ✅: 기반 구축 (완료)
- **Phase 2** 🔄: 한국어 문서화 (진행 중, ~70%)
  - ✅ v1/v2 디렉토리 구조 재편성
  - ✅ v1 Python 예제 가이드 4개 완료
  - ✅ x402 v2 프로토콜 스펙 문서 완료
  - ⏳ Base 체인 가이드 (USDC faucet, 가스비 최적화)
- **Phase 3** ⏳: AI 에이전트, 프로덕션 가이드 (계획)
- **Phase 4** ⏳: 글로벌 확장 (계획)

---

## 📞 지원 및 기여

### 이슈 및 질문
- GitHub Issues에 질문 또는 버그 리포트 등록

### Pull Request 환영
- 한글 문서 개선
- Base 특화 예제 추가
- 오타 수정 및 문서 업데이트

### 커뮤니티
- Base Korea Developer 커뮤니티
- x402 공식 Discord

---

**문서 버전**: 1.1
**최종 업데이트**: 2025-12-16
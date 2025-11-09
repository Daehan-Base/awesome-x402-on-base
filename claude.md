# awesome-x402-on-base

> Base 체인에서 x402 프로토콜을 사용하기 위한 한국어 리소스, 도구, 지식 모음

**관리자**: Logan (Base Korea Developer Ambassador)
**라이선스**: MIT License
**작성일**: 2025-01-08

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
│   ├── examples/           # 공식 예제 (Python, TS, Go, Java)
│   └── specs/              # 프로토콜 스펙
│
├── examples/               # 📝 Base 특화 예제
│   └── base-specific/      # Base 최적화 사용 사례 (준비 중)
│
├── docs/korean/            # 🇰🇷 한국어 문서
│   ├── getting_started.ko.md         # 시작 가이드
│   └── examples/                     # 예제별 한글 튜토리얼
│       ├── python-requests-client.ko.md
│       ├── python-httpx-client.ko.md
│       ├── python-fastapi-server.ko.md
│       └── python-discovery.ko.md
│
├── README.md               # 프로젝트 소개 (한글/영문)
├── ROADMAP.md              # 개발 로드맵
├── LICENSE                 # MIT 라이선스
├── claude.md               # Claude Code 컨텍스트 (이 파일)
└── .cursor/rules           # Cursor AI 규칙
```

### 디렉토리 역할

**`external/x402/`** (읽기 전용)
- Coinbase 공식 x402 코드 참조
- Git 서브모듈, 절대 수정 금지
- 업데이트: `git submodule update --remote external/x402`

**`examples/base-specific/`** (작성 중)
- Base 체인 최적화 예제
- 커뮤니티 기여 환영
- Base Mainnet 배포, USDC 통합, 가스비 최적화

**`docs/korean/`** (활발히 작성 중)
- 한국 개발자를 위한 단계별 가이드
- Web2 비유를 활용한 Web3 교육
- 보안 가이드라인 포함

---

## 🎯 핵심 개념

### 1. x402 프로토콜
**정의**: HTTP 402 Payment Required 상태 코드를 활용한 암호화폐 결제 프로토콜

**동작 원리**:
1. 클라이언트 → 서버: HTTP 요청
2. 서버 → 클라이언트: 402 응답 (결제 정보 포함)
3. 클라이언트: 결제 서명 생성
4. 클라이언트 → 서버: `X-PAYMENT` 헤더와 함께 재요청
5. 서버: 결제 검증 → 리소스 제공

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
   - 예제별 한글 튜토리얼 참조 (`docs/korean/examples/`)

2. **공식 예제 패턴 따르기**
   - `external/x402/examples/`에서 표준 구현 패턴 학습
   - Base 특화 최적화는 `examples/base-specific/`에 구현

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

### examples/ (4개 실습 예제 문서)

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
2단계: python-requests-client.ko.md (동기 클라이언트)
    ↓
3단계: python-httpx-client.ko.md (비동기 클라이언트)
    ↓
4단계: python-fastapi-server.ko.md (서버 구현)
    ↓
5단계: python-discovery.ko.md (고급 기능)
    ↓
6단계: Base Mainnet 배포 (준비 중)
```

---

## 🗂️ 중요 경로

### 한글 가이드
- `docs/korean/getting_started.ko.md` - 시작 가이드
- `docs/korean/examples/` - Python 예제 튜토리얼 (4개)

### 공식 예제 (읽기 전용)
- `external/x402/examples/python/clients/` - Python 클라이언트 예제
- `external/x402/examples/python/servers/` - Python 서버 예제
- `external/x402/examples/typescript/` - TypeScript 예제

### Base 특화 예제 (작성 중)
- `examples/base-specific/` - Base 최적화 사용 사례

### 프로젝트 문서
- `README.md` - 프로젝트 소개 (한글/영문)
- `ROADMAP.md` - 개발 로드맵

---

## 🔒 보안 규칙

### Private Key 보안 (Critical)

**위험성**:
- 유출 시 즉시 모든 자산 탈취 가능
- 영구적 접근 권한 (비밀번호 변경 불가)
- 블록체인 거래는 되돌릴 수 없음

**필수 수칙**:

✅ **해야 할 것**:
- `.env` 파일 + `.gitignore`
- 환경 변수로 로드
- 개발/프로덕션 지갑 분리
- 비밀번호 관리자 사용

❌ **절대 하지 말 것**:
- Git 커밋
- 콘솔 출력 (`console.log`, `print`)
- 공개 채널 공유 (Slack, Discord 등)
- 스크린샷/화면 공유 시 노출

### Recovery Phrase vs Private Key

| 항목 | Recovery Phrase | Private Key |
|------|-----------------|-------------|
| 형태 | 12-24 단어 | 64자 16진수 (0x 시작) |
| 예시 | `abandon ability able...` | `0xac0974bec39a17e...` |
| 생성 | 지갑 최초 생성 시 1번 | 각 계정마다 1개 |
| 복구 범위 | 전체 지갑 (모든 계정) | 해당 계정만 |
| 중요도 | 매우 높음 (모든 계정 접근) | 높음 (해당 계정 접근) |

### 환경 변수 관리

```bash
# .env (절대 커밋 금지)
CDP_API_KEY_ID=cdp-api-key-xxxxx
CDP_API_KEY_SECRET=-----BEGIN EC PRIVATE KEY-----...
CDP_WALLET_SECRET=your-wallet-secret-here
PRIVATE_KEY=0xac0974bec39a17e36f4ac7d1d5f1e3f...

# .env.example (Git 커밋 가능)
CDP_API_KEY_ID=
CDP_API_KEY_SECRET=
CDP_WALLET_SECRET=
PRIVATE_KEY=
```

### 네트워크 보안
- **개발**: `base-sepolia` (테스트넷, 실제 가치 없음)
- **프로덕션**: `base` (메인넷, HTTPS 필수)
- 클라이언트/서버 네트워크 일치 확인

### 긴급 대응 프로토콜

**Private Key 유출 시**:
1. 즉시 새 지갑 생성
2. 남은 자산 이동 (ETH 먼저)
3. 유출된 지갑 사용 중단
4. 관련 서비스 API 키 갱신

---

## 🔄 작업 워크플로우

### 프로젝트 클론 및 초기화

```bash
# 서브모듈과 함께 클론
git clone --recursive https://github.com/YOUR_USERNAME/awesome-x402-on-base.git

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
cd external/x402/examples/python/clients/requests
cp .env-local .env
# .env 파일에 Private Key 추가
uv sync
uv run python main.py
```

### 한글 가이드 작성

```bash
# 새 가이드 작성
cd docs/korean/examples
# 템플릿을 참고하여 새 .ko.md 파일 작성
# 타임스탬프 및 업데이트 경고 포함
```

### Base 특화 예제 추가

```bash
# 공식 예제를 examples/base-specific/에 복사
cp -r external/x402/examples/python/servers/fastapi examples/base-specific/
# Base 최적화 적용 (가스비, USDC 통합)
# README.md 작성
```

---

## 🎓 문서 작성 패턴

### 에이전트가 따라야 할 핵심 패턴

1. **Web2 비유 우선**
   - 복잡한 Web3 개념을 친숙한 비유로 설명
   - 예: 지갑 = Gmail 앱, 계정 = user@gmail.com

2. **시각적 구조**
   - 화살표 (`→`), 체크리스트 (`- [ ]`), 표 활용
   - 단계별 진행 명시

3. **코드 + 설명 분리**
   - 실행 가능한 전체 코드 제공
   - 주석으로 핵심 로직 설명
   - 별도 설명 섹션 추가

4. **보안 경고 강조**
   - ⚠️ 이모지와 경고 블록 사용
   - ✅/❌ 표시로 올바른/잘못된 예제 구분

5. **문제 해결 섹션**
   - 증상 → 해결 방법 패턴
   - 실제 발생 가능한 문제 다루기

6. **다음 단계 제시**
   - 학습 경로 명시
   - 관련 문서 링크

7. **타임스탬프 명시**
   ```markdown
   > **작성 시점**: 2025년 11월 8일
   > ⚠️ **중요**: UI/프로세스 변경 가능, Issue나 PR로 기여 요청
   ```

8. **한글 전문 용어**
   - 병기 방식: "지갑 (Wallet)", "계정 (Account)"
   - 일관성 유지: Private Key (번역 안 함)

---

## 🚀 개발 로드맵

### Phase 1: 기반 구축 ✅ (완료)
- Git 서브모듈 설정
- 디렉토리 구조 생성
- 한글 README 및 시작 가이드

### Phase 2: 한국어 문서화 🔄 (진행 중, ~50%)
- ✅ Python requests/httpx/FastAPI/Discovery 가이드
- ⏳ Base 체인 설정 가이드
- ⏳ USDC faucet 사용 가이드
- ⏳ Base Mainnet 전환 가이드

### Phase 3: 고급 콘텐츠 (계획)
- AI 에이전트 통합 (LangChain, Anthropic Claude)
- 프로덕션 배포 가이드
- 보안 체크리스트
- 모니터링 및 에러 핸들링

### Phase 4: 글로벌 확장 (계획)
- 영어 문서 번역
- 글로벌 x402 커뮤니티 연결
- 다국어 지원 확대

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

**문서 버전**: 1.0  
**최종 업데이트**: 2025-01-08  

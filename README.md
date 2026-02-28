[한국어](./README.md) | [English](./README.en.md)

# Awesome x402 on Base 🚀

> Base 체인에서 x402 프로토콜을 사용하기 위한 리소스, 도구, 지식 모음 - Base Korea Developer Ambassador가 관리합니다.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Base Chain](https://img.shields.io/badge/Chain-Base-blue.svg)](https://base.org)
[![x402 Protocol](https://img.shields.io/badge/Protocol-x402-green.svg)](https://www.x402.org)

## 📝 요약 (TL;DR)

**What**: Base 체인 x402 결제 프로토콜 한국어 가이드  
**Why**: 공식 예제가 이미 Base 사용 - 상세한 한글 튜토리얼 추가  
**How**: Git 서브모듈로 공식 코드(`external/`) 연결 + 한글 가이드(`docs/`)  
**Target**: 한국 개발자 & Base 특화 x402 구현에 관심있는 글로벌 빌더  

**Quick Start**: [Official Documentation](https://docs.cdp.coinbase.com/x402/welcome) | [Korean Guide](./docs/getting_started.md)

---

## 📖 이 레포지토리에 대하여

이 레포지토리는 Base 체인에서 **x402 프로토콜**을 사용하기 위한 **한국어 가이드와 문서**를 제공합니다. 공식 x402 예제는 이미 Base 체인을 기본으로 사용하므로, 각 예제에 대한 상세한 한글 튜토리얼과 커뮤니티 리소스 제공에 집중합니다.

**포함 내용:**
- 🔗 **공식 예제** (`external/`의 Git 서브모듈) - Coinbase의 x402 예제에 직접 접근
- 📝 **한글 가이드** (`docs/`) - 각 예제에 대한 단계별 한글 튜토리얼
- 🔵 **Base 특화 콘텐츠** (`examples/`) - Base 체인 최적화 및 사용 사례
- 🇰🇷 **한국 커뮤니티** - 한국 개발자를 위한 리소스

> **참고**: 이 레포지토리는 [공식 x402 레포지토리](https://github.com/coinbase/x402)를 보완하여 한국어 문서와 Base 중심 콘텐츠를 제공합니다.

## 🔍 x402란?

**x402**는 Coinbase가 개발한 오픈소스 결제 프로토콜로, 26년간 사용되지 않던 HTTP 402 상태 코드를 현대적으로 재해석하여 인터넷 네이티브 결제를 혁신합니다.

### 주요 특징

- ⚡ **빠른 속도** - 약 2초 내 결제 처리
- 💰 **초저비용** - 거래 수수료 < $0.0001, 최소 $0.001 결제 가능
- 🤖 **기계간 결제** - AI 에이전트와 IoT 기기의 자율적 리소스 결제
- 🔗 **체인 독립적** - Base, Solana, Polygon, Ethereum 등 지원
- 🌐 **HTTP 네이티브** - 웹 통합을 위해 HTTP 위에 구축

### 작동 원리

x402는 HTTP 402 "Payment Required" 상태 코드를 활용하여 인터넷을 위한 표준화된 결제 레이어를 만듭니다. 서비스가 결제를 요구하면 결제 지침이 포함된 402 응답을 반환합니다. 클라이언트(AI 에이전트 포함)는 계정, 세션, 복잡한 인증 없이 USDC와 같은 스테이블코인을 사용하여 자동으로 결제를 처리할 수 있습니다.

## 🎯 왜 Base 체인인가?

**Base**는 x402 프로토콜 도입에 최적의 네트워크입니다:

- 🚀 **높은 성능** - 빠른 최종성과 낮은 지연시간
- 💵 **최소 수수료** - x402 거래의 가스비 < $0.0001
- 🔐 **이더리움 보안** - 이더리움 위에 구축된 L2의 강력한 보안
- 🌊 **네이티브 지원** - Base Sepolia와 Base Mainnet에 대한 일급 지원
- 💎 **USDC 통합** - 기본 결제 통화로 네이티브 USDC 사용

Base는 x402의 마이크로페이먼트와 AI 에이전트 간 거래를 대규모로 가능하게 하는 완벽한 인프라를 제공합니다.

## 🌟 x402 생태계

x402 생태계는 주요 기술 기업들의 지원으로 빠르게 성장하고 있습니다:

- **Coinbase** - 프로토콜 제작자 및 주요 관리자
- **Cloudflare** - x402 Foundation 공동 설립자
- **Google** - 인프라 통합
- **Visa** - 결제 네트워크 파트너십
- **AWS** - 클라우드 인프라 지원
- **Circle** - USDC 스테이블코인 제공자
- **Anthropic** - AI 통합


## 📁 레포지토리 구조

```
awesome-x402-on-base/
├── external/x402/              # 🔗 Git 서브모듈 (공식 x402 레포지토리, 읽기 전용)
│
├── examples/                   # 📝 Base 특화 예제 및 데모
│   └── python/                 # Python 예제
│       ├── v1/                 # v1 Legacy SDK 예제
│       └── v2/                 # v2 SDK 예제
│
├── docs/                       # 🇰🇷 한국어 문서
│   ├── getting_started.md   # 시작 가이드
│   ├── x402-v2-specification.md  # v2 프로토콜 스펙
│   ├── python/                 # Python 문서
│   │   ├── v1/                 # v1 Legacy 문서
│   │   │   ├── clients/        # 클라이언트 (requests, httpx)
│   │   │   ├── servers/        # 서버 (FastAPI)
│   │   │   └── discovery/      # Discovery
│   │   └── v2/                 # v2 문서 (clients/, servers/)
│   └── typescript/             # TypeScript 문서
│       ├── v1/                 # v1 Legacy 문서 (준비 중)
│       └── v2/                 # v2 예제 가이드
│
├── ROADMAP.md                  # 🗺️ 개발 로드맵
└── LICENSE                     # 📄 MIT 라이선스
```

**명확한 구분:**
- **`external/`** = 공식 x402 예제 (서브모듈, 수정 금지)
- **`examples/`** = Base 특화 x402 예제
- **`docs/`** = 한글 가이드 및 튜토리얼 (언어 → 버전 구조)

## 🚀 빠른 시작

### 영어 사용자를 위해
→ [공식 x402 문서](https://docs.cdp.coinbase.com/x402/welcome)에서 시작하세요

### 한국 개발자분들을 위해 🇰🇷
→ [한글 빠른 시작 가이드](./docs/getting_started.md)에서 시작하세요

## 💡 예제 및 한글 가이드

### Python v2 예제 (최신)

| 예제 | 로컬 코드 | 원본 레포 | 한글 가이드 |
|------|----------|----------|------------|
| **requests 클라이언트** (동기) | [→ 로컬](./external/x402/examples/python/clients/requests/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/clients/requests) | [→ 가이드](./docs/python/v2/clients/requests/README.md) |
| **httpx 클라이언트** (비동기) | [→ 로컬](./external/x402/examples/python/clients/httpx/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/clients/httpx) | [→ 가이드](./docs/python/v2/clients/httpx/README.md) |
| **FastAPI 서버** (비동기) | [→ 로컬](./external/x402/examples/python/servers/fastapi/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/servers/fastapi) | [→ 가이드](./docs/python/v2/servers/fastapi/README.md) |
| **Flask 서버** (동기) | [→ 로컬](./external/x402/examples/python/servers/flask/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/servers/flask) | [→ 가이드](./docs/python/v2/servers/flask/README.md) |

### Python v1 예제 (Legacy)

| 예제 | 로컬 코드 | 원본 레포 | 한글 가이드 |
|------|----------|----------|------------|
| **requests 클라이언트** | [→ 로컬](./external/x402/examples/python/legacy/clients/requests/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/requests) | [→ 가이드](./docs/python/v1/clients/requests/README.md) |
| **httpx 클라이언트** | [→ 로컬](./external/x402/examples/python/legacy/clients/httpx/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/legacy/clients/httpx) | [→ 가이드](./docs/python/v1/clients/httpx/README.md) |
| **FastAPI 서버** | [→ 로컬](./external/x402/examples/python/legacy/servers/fastapi/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/legacy/servers/fastapi) | [→ 가이드](./docs/python/v1/servers/fastapi/README.md) |
| **Discovery** | [→ 로컬](./external/x402/examples/python/legacy/discovery/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/legacy/discovery) | [→ 가이드](./docs/python/v1/discovery/README.md) |

### TypeScript 예제 (v2 최신)

| 예제 | 로컬 코드 | 원본 레포 | 한글 가이드 |
|------|----------|----------|------------|
| **Axios 클라이언트** | [→ 로컬](./external/x402/examples/typescript/clients/axios/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/axios) | [→ 가이드](./docs/typescript/v2/clients/axios/) |
| **Fetch 클라이언트** | [→ 로컬](./external/x402/examples/typescript/clients/fetch/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/fetch) | [→ 가이드](./docs/typescript/v2/clients/fetch/) |
| **Express 서버** | [→ 로컬](./external/x402/examples/typescript/servers/express/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/express) | [→ 가이드](./docs/typescript/v2/servers/express/) |
| **Hono 서버** | [→ 로컬](./external/x402/examples/typescript/servers/hono/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/hono) | [→ 가이드](./docs/typescript/v2/servers/hono/) |
| **Next.js Fullstack** | [→ 로컬](./external/x402/examples/typescript/fullstack/next/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/fullstack/next) | [→ 가이드](./docs/typescript/v2/fullstack/next/) |
| **Farcaster Mini App** | [→ 로컬](./external/x402/examples/typescript/fullstack/miniapp/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/fullstack/miniapp) | [→ 가이드](./docs/typescript/v2/fullstack/miniapp/) |
| **MCP 클라이언트** | [→ 로컬](./external/x402/examples/typescript/clients/mcp/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/mcp) | [→ 가이드](./docs/typescript/v2/clients/mcp/) |

### 서브모듈 사용하기

⚠️ **중요**: `external/x402`는 Git 서브모듈입니다. 초기화가 필요합니다.

최초 설정:
```bash
# 서브모듈과 함께 이 레포지토리 클론
git clone --recursive https://github.com/Daehan-Base/awesome-x402-on-base.git

# 또는 이미 클론한 경우
git submodule update --init --recursive
```

공식 예제 접근:
```bash
# 먼저 서브모듈 초기화 확인
ls external/x402/examples/python  # 비어있으면 위의 명령어 실행

cd external/x402/examples/python
# docs/python/v1/의 한글 가이드를 따라하세요
```

## 🗺️ 로드맵

프로젝트의 상세한 개발 계획은 [ROADMAP.md](./ROADMAP.md)를 참고하세요.

## 🤝 기여하기

기여를 환영합니다! 자세한 가이드는 [CONTRIBUTING.md](./CONTRIBUTING.md)를 참고하세요.

### 기여 방법

- 📝 **문서 기여** - 한글 튜토리얼, 가이드 작성
- 💻 **예제 코드** - Base 특화 예제 추가
- 🐛 **버그 리포트** - 이슈 등록
- 💡 **기능 제안** - 새로운 아이디어 공유

[기여 가이드 보기 →](./CONTRIBUTING.md)

## 📚 리소스

### 공식 x402 리소스
- 📖 [공식 문서](https://docs.cdp.coinbase.com/x402/welcome)
- 💻 x402 GitHub: [📂 로컬](./external/x402/) | [🔗 원본](https://github.com/coinbase/x402)
- 📄 [x402 백서](https://www.x402.org/x402-whitepaper.pdf)
- 🌐 [x402 웹사이트](https://www.x402.org)

### x402 SDK & 예제

| SDK/예제 | 로컬 코드 | 원본 레포 |
|---------|----------|----------|
| Python SDK | [→ 로컬](./external/x402/python/x402/) | [→ 원본](https://github.com/coinbase/x402/tree/main/python/x402) |
| Python v2 예제 | [→ 로컬](./external/x402/examples/python/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python) |
| Python v1 예제 | [→ 로컬](./external/x402/examples/python/legacy/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/python/legacy) |
| TypeScript SDK | [→ 로컬](./external/x402/typescript/) | [→ 원본](https://github.com/coinbase/x402/tree/main/typescript) |
| Go 구현 | [→ 로컬](./external/x402/go/) | [→ 원본](https://github.com/coinbase/x402/tree/main/go) |

### Base 체인 리소스
- [Base 공식 웹사이트](https://base.org)
- [Base 문서](https://docs.base.org)
- [Base Sepolia Faucet](https://faucet.quicknode.com/base/sepolia)
- [Circle USDC Faucet](https://faucet.circle.com/)

## 📬 연락하기

- **이슈 & 질문** - 이 레포지토리에 이슈 열기
- **토론** - GitHub Discussions에서 의견 공유

## 📄 라이선스

이 레포지토리는 [MIT License](LICENSE)에 따라 라이선스가 부여됩니다.

---

**Logan (Base Korea Developer Ambassador)가 정성을 담아 관리합니다**

*인터넷 네이티브 결제의 미래를 만들어갑니다, 한 커밋씩.*

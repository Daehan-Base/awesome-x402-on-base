# 시작하기 가이드

> **작성 시점**: 2025년 11월 8일
> **최종 검증**: CDP Platform 2025년 11월 기준
>
> ⚠️ **중요**: 이 가이드는 작성 시점을 기준으로 하며, CDP Platform의 UI나 프로세스는 시간이 지남에 따라 변경될 수 있습니다. 만약 이 가이드의 내용이 더 이상 정확하지 않거나 업데이트가 필요하다면, [Issue를 생성](https://github.com/YOUR_USERNAME/awesome-x402-on-base/issues/new)하여 알려주시거나 Pull Request를 통해 기여해주세요. 여러분의 기여가 커뮤니티 전체에 도움이 됩니다! 🙏

---

x402 프로토콜을 Base 체인에서 사용하기 위한 완벽한 시작 가이드입니다. 이 문서는 CDP Platform 계정 설정부터 첫 번째 x402 애플리케이션 실행까지 모든 과정을 단계별로 안내합니다.

## 📋 목차

- [개요](#개요)
- [사전 요구사항](#사전-요구사항)
- [Web3 지갑 설정 (Web2 개발자 가이드)](#web3-지갑-설정-web2-개발자-가이드)
- [1단계: CDP Platform 계정 생성](#1단계-cdp-platform-계정-생성)
- [2단계: CDP API 키 생성](#2단계-cdp-api-키-생성)
- [3단계: Wallet Secret 생성](#3단계-wallet-secret-생성)
- [4단계: 환경 변수 설정](#4단계-환경-변수-설정)
- [5단계: 테스트 자금 확보](#5단계-테스트-자금-확보)
- [다음 단계](#다음-단계)
- [문제 해결](#문제-해결)

---

## 개요

x402 프로토콜을 사용하려면 다음이 필요합니다:

1. **CDP Platform 계정** - Coinbase Developer Platform에서 서버 월렛 사용
2. **API 인증 정보** - CDP API Key ID, Secret, Wallet Secret
3. **테스트 자금** - Base Sepolia 테스트넷의 USDC (개발용)

이 가이드는 위의 모든 것을 설정하는 방법을 안내합니다.

---

## 사전 요구사항

시작하기 전에 다음을 준비하세요:

- [ ] 유효한 이메일 주소
- [ ] 2단계 인증(2FA) 앱 (Google Authenticator, Authy 등)
- [ ] 안정적인 인터넷 연결
- [ ] 개발 환경 (Python 3.10+ 또는 Node.js 20+)
- [ ] EVM 호환 지갑 (MetaMask, Base Wallet 등) - 선택사항이지만 권장

---

## Web3 지갑 설정 (Web2 개발자 가이드)

> 💡 **Web2 개발자를 위한 참고사항**: Web3가 처음이신가요? 이 섹션에서 블록체인 지갑의 기본 개념을 간단히 설명합니다.

### Web3 지갑과 계정의 차이

많은 사람들이 "지갑"과 "계정"을 혼동합니다. 명확히 구분하면:

**지갑 (Wallet)**:
- 블록체인 계정들을 관리하는 **앱 또는 소프트웨어**
- 예: MetaMask, Base Wallet, Ledger

**계정 (Account)**:
- 지갑 안에 있는 **개별 주소와 Private Key 쌍**
- 하나의 지갑에 여러 개의 계정을 가질 수 있음

**Web2 비유**:
```
지갑 (Wallet) = 이메일 클라이언트 앱 (Gmail 앱, Outlook 앱)
계정 (Account) = 개별 이메일 주소 (user1@gmail.com, user2@gmail.com)

→ Gmail 앱 하나로 여러 이메일 계정을 관리하듯,
  MetaMask 지갑 하나로 여러 블록체인 계정을 관리
```

**핵심 개념**:
- **Recovery Phrase**: 전체 지갑과 그 안의 모든 계정들을 복구
- **Private Key**: 특정 계정 하나만 복구
- **EVM 호환 지갑**: Ethereum, Base, Polygon 등에서 사용 가능 (Base도 EVM 호환)

### 지갑 생성 방법

> 💡 **지갑 간 호환성**: Base Wallet과 MetaMask는 모두 EVM 호환 지갑입니다. **Recovery Phrase(복구 문구)를 사용하면 한 지갑에서 만든 계정을 다른 지갑 앱에서도 복구할 수 있습니다.** 예를 들어, Base Wallet에서 만든 지갑을 MetaMask에서 복구 문구로 불러올 수 있고, 그 반대도 가능합니다.

#### 옵션 1: Base Wallet (권장 - Base 체인 최적화)

**Base Wallet**은 Base 체인에 최적화된 공식 지갑입니다.

1. **설치**:
   - **브라우저**: Chrome 웹 스토어에서 "Coinbase Wallet" 검색 후 **wallet.coinbase.com**에서 배포한 확장 프로그램 추가
   - **모바일**: App Store 또는 Play Store에서 "Base Wallet" 검색 → **Coinbase Wallet** 개발자의 앱 다운로드

2. **지갑 생성**:
   - 앱 실행 → **Create New Wallet** 선택
   - 복구 문구 (12 또는 24단어)를 안전하게 저장
   - 비밀번호 설정 → 지갑 생성 완료

3. **Private Key 확인** (개발용):
   - 설정 → 보안 → Private Key 표시
   - 비밀번호 입력 후 Private Key 복사

#### 옵션 2: MetaMask (가장 대중적)

**MetaMask**는 가장 널리 사용되는 Web3 지갑입니다.

1. **설치**:
   - **브라우저**: Chrome 웹 스토어에서 "MetaMask" 검색 후 확장 프로그램 추가
   - **모바일**: App Store 또는 Play Store에서 "MetaMask" 검색 후 설치 → **MetaMask** 개발자의 앱 다운로드

2. **지갑 생성**:
   - **Get Started** → **Create a Wallet** 클릭
   - 비밀번호 설정
   - **Secret Recovery Phrase** (복구 문구) 저장 - **절대 분실하지 마세요!**
   - 복구 문구 확인 → 지갑 생성 완료

3. **Base 네트워크 추가**:
   - MetaMask 상단의 네트워크 드롭다운 클릭
   - **Add Network** → **Base Sepolia** 검색 및 추가

4. **Private Key 확인** (개발용):
   - 계정 메뉴 (⋮) → Account Details → Export Private Key
   - 비밀번호 입력 후 Private Key 복사



### 🔑 Recovery Phrase vs Private Key - 차이점

많은 초보자가 이 둘을 혼동합니다. 차이를 이해하는 것이 중요합니다:

| 항목 | Recovery Phrase (복구 문구) | Private Key |
|------|----------------------------|-------------|
| **형태** | 12-24개의 영어 단어 | 64자리 16진수 (0x 시작) |
| **예시** | `abandon ability able...` | `0xac0974bec39a17e...` |
| **생성** | 지갑 최초 생성 시 1번 | 각 계정마다 1개 |
| **관계** | 여러 개의 Private Key 생성 가능 | 1개의 주소에만 대응 |
| **복구** | 전체 지갑 복구 가능 | 해당 계정만 복구 |
| **중요도** | 매우 높음 (모든 계정 접근) | 높음 (해당 계정 접근) |

**간단히**:
- **Recovery Phrase**: 마스터 키 (집의 마스터 키)
- **Private Key**: 개별 계정 키 (특정 방의 열쇠)

> **⚠️ 절대 공유 금지**: 둘 다 유출되면 자산을 잃을 수 있습니다!

### Private Key란?

**Private Key**는 블록체인 계정에 접근하는 비밀 키입니다.

**형식**: 64자의 16진수 (앞에 `0x` 접두사)
```
0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
```

**주요 용도**:
- 트랜잭션 서명 (블록체인 거래)
- x402 결제 서명
- 계정 복구

**관계**:
```
Private Key (비밀) → Public Key (공개 가능) → Wallet Address (공개)
```

### 🚨 Private Key 보안 - 매우 중요!

> **⚠️ 경고**: Private Key가 유출되면 해당 지갑의 **모든 자산을 영구적으로 잃을 수 있습니다**. 블록체인 거래는 되돌릴 수 없습니다!

**유출 시 위험**:
- 즉시 모든 자산 탈취 가능
- 영구적인 접근 권한 부여 (비밀번호 변경 불가)
- 무단 결제 및 트랜잭션 실행

**안전하게 관리하는 방법**:

**✅ 해야 할 것**:
- `.env` 파일에 저장하고 `.gitignore`에 추가
- 환경 변수로 로드 (코드에 하드코딩 금지)
- **개발용 지갑과 실제 자산 지갑을 반드시 분리**
- 비밀번호 관리자 사용 (1Password, Bitwarden 등)

**❌ 절대 하지 말 것**:
- Git 저장소에 커밋
- 콘솔/로그에 출력
- 공개 채널(Slack, Discord, 이메일)에 공유
- 스크린샷, 화면 공유 시 노출
- 신뢰할 수 없는 사이트에 입력

> **💡 개발 환경 주의사항**: 테스트용 지갑(소액만 보관)과 실제 자산 지갑을 반드시 분리하세요. 개발 중 실수로 Private Key가 노출되어도 피해를 최소화할 수 있습니다.

**유출된 경우 긴급 대응**:
1. 즉시 새 지갑 생성
2. 남은 자산을 새 지갑으로 이동 (ETH 먼저, 그 다음 다른 자산)
3. 유출된 지갑 사용 중단

### 코드에서 사용하기

**Python**:
```python
import os
from eth_account import Account
from dotenv import load_dotenv

load_dotenv()
private_key = os.getenv("PRIVATE_KEY")
account = Account.from_key(private_key)
```

**JavaScript**:
```javascript
import dotenv from 'dotenv';
import { ethers } from 'ethers';

dotenv.config();
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY);
```

---

## 1단계: CDP Platform 계정 생성

### 1.1 회원가입

1. [Coinbase Developer Platform](https://portal.cdp.coinbase.com/)에 접속합니다.

2. **Sign Up** 버튼을 클릭하고 다음 정보를 입력합니다:
   - 이메일 주소
   - 비밀번호 (강력한 비밀번호 권장)
   - 이용 약관 동의

3. 이메일로 전송된 인증 링크를 클릭하여 이메일 주소를 확인합니다.

### 1.2 2단계 인증 설정

보안을 위해 2FA는 **필수**입니다:

1. CDP Portal에 로그인합니다.
2. **Settings** → **Security** 메뉴로 이동합니다.
3. **Enable 2FA** 버튼을 클릭합니다.
4. QR 코드를 2FA 앱으로 스캔합니다.
5. 앱에서 생성된 6자리 코드를 입력하여 설정을 완료합니다.

> **중요**: 백업 코드를 안전한 곳에 보관하세요. 2FA 기기를 분실할 경우 계정 복구에 필요합니다.

### 1.3 신원 인증 (KYC)

> **참고**: CDP Platform의 정확한 KYC 요구사항은 사용 사례와 지역에 따라 다를 수 있습니다. 일부 개발 용도의 경우 KYC가 필요하지 않을 수 있으며, 프로덕션 환경이나 특정 기능 사용 시 요구될 수 있습니다.

KYC가 필요한 경우:

1. CDP Portal에서 **Verification** 또는 **Identity Verification** 섹션을 찾습니다.
2. 요청되는 정보를 제공합니다:
   - 개인 정보 (이름, 생년월일, 주소)
   - 신분증 사진 (여권, 운전면허증 등)
   - 셀카 인증 (일부 경우)
3. 인증 프로세스가 완료될 때까지 기다립니다 (보통 몇 분~24시간 소요).

> **최신 정보**: KYC 요구사항은 변경될 수 있습니다. 최신 정보는 [CDP 공식 문서](https://docs.cdp.coinbase.com/)를 참조하거나 CDP 지원팀에 문의하세요.

---

## 2단계: CDP API 키 생성

### 2.1 프로젝트 생성

1. CDP Portal에 로그인합니다.
2. 좌측 메뉴에서 **Projects**를 선택합니다.
3. **Create Project** 버튼을 클릭합니다.
4. 프로젝트 정보를 입력합니다:
   - **Project Name**: `x402-base-project` (예시)
   - **Description**: x402 결제 프로토콜 개발
5. **Create** 버튼을 클릭합니다.

### 2.2 API 키 생성

1. 생성한 프로젝트를 선택합니다.
2. **API Keys** 탭으로 이동합니다.
3. **Create API Key** 버튼을 클릭합니다.
4. API 키 정보를 입력합니다:
   - **API Key Nickname**: `x402-dev-key` (예시)
   - **Permissions**: 필요한 권한 선택 (Server Wallets 관련 권한 포함)

5. **Create** 버튼을 클릭합니다.

### 2.3 인증 정보 저장

API 키가 생성되면 파일로 다운로드 됩니다.

**저장 방법**:
- API 키 파일을 다운로드하여 안전한 위치에 보관
- 비밀번호 관리자 (1Password, Bitwarden 등) 사용하여 관리
- 절대 Git 저장소에 커밋하지 마세요. 커밋 시 키가 노출될 수 있습니다.

### 2.4 2FA 인증

API 키 생성 과정에서 2FA 코드 입력이 요구될 수 있습니다.

---

## 3단계: Wallet Secret 생성

Server Wallet을 사용하려면 Wallet Secret이 필요합니다.

### 3.1 Wallet Secret 생성

1. CDP Portal에서 프로젝트를 선택합니다.
2. **Server Wallets** 섹션으로 이동합니다.
3. **Wallet Secret** 영역을 찾습니다.
4. **Generate** 버튼을 클릭합니다.

### 3.2 Wallet Secret 저장

생성된 Wallet Secret을 **즉시** 안전하게 저장하세요:

```
CDP_WALLET_SECRET=your-wallet-secret-here
```

> **⚠️ 중요**: Wallet Secret은 **다시 볼 수 없습니다**. 분실 시 새로운 Secret을 생성해야 하며, 기존 월렛에 대한 접근이 불가능할 수 있습니다.

### 3.3 Wallet Secret의 역할

Wallet Secret은 CDP의 TEE (Trusted Execution Environment)에서 생성되며:
- 트랜잭션 서명에 사용됩니다
- API Key와 결합하여 X-Wallet-Auth 헤더 생성
- Coinbase에서도 볼 수 없는 완전히 안전한 비밀 정보입니다

---

## 4단계: 환경 변수 설정

### 4.1 환경 변수 파일 생성

필요 시 프로젝트 루트에서 `.env` 파일을 생성하거나, 시스템 환경 변수로 설정합니다.

```bash
# CDP Platform 인증 정보
CDP_API_KEY_ID=cdp-api-key-xxxxx
CDP_API_KEY_SECRET=-----BEGIN EC PRIVATE KEY-----
...
-----END EC PRIVATE KEY-----
CDP_WALLET_SECRET=your-wallet-secret-here

# x402 서버 설정 (개발 환경)
RESOURCE_SERVER_URL=http://localhost:4021
ENDPOINT_PATH=/weather

# 네트워크 설정
NETWORK=base-sepolia
```

### 4.2 보안 주의사항

**✅ 해야 할 것**:
- `.env` 파일을 `.gitignore`에 추가
- 프로덕션에서는 환경 변수나 시크릿 관리 서비스 사용
- API 키에 최소 권한 원칙 적용
- 정기적으로 API 키 로테이션

**❌ 하지 말아야 할 것**:
- `.env` 파일을 Git에 커밋
- API 키를 코드에 하드코딩
- 공개 저장소에 인증 정보 노출
- 개발용 키를 프로덕션에서 사용

### 4.3 환경 변수 예제

프로젝트에 `.env.example` 파일을 생성하여 필요한 변수 구조를 공유하세요:

```bash
# .env.example
CDP_API_KEY_ID=
CDP_API_KEY_SECRET=
CDP_WALLET_SECRET=
RESOURCE_SERVER_URL=http://localhost:4021
ENDPOINT_PATH=/weather
NETWORK=base-sepolia
```

---

## 5단계: 테스트 자금 확보

개발 및 테스트를 위해 Base Sepolia 테스트넷에서 USDC를 받으세요.

### 5.1 CDP Faucet 사용

1. [CDP Faucet](https://portal.cdp.coinbase.com/products/faucet)에 접속합니다.
2. CDP Portal 계정으로 로그인합니다.
3. 월렛 주소를 입력합니다 (CDP Server Wallet 주소).
4. **Base Sepolia** 네트워크를 선택합니다.
5. **Request USDC** 버튼을 클릭합니다.

### 5.2 Circle USDC Faucet (대체 방법)

1. [Circle USDC Faucet](https://faucet.circle.com/)에 접속합니다.
2. 월렛 주소를 입력합니다.
3. **Base Sepolia** 네트워크를 선택합니다.
4. **Get Test USDC** 버튼을 클릭합니다.

### 5.3 잔액 확인

CDP Portal 또는 [Base Sepolia Explorer](https://sepolia.basescan.org/)에서 USDC 잔액을 확인하세요.

---

## 다음 단계

축하합니다! 이제 x402 개발을 시작할 준비가 되었습니다. 🎉

### 추천 학습 경로

1. **Python 예제 시작하기** (v1 Legacy)
   - [requests 클라이언트 가이드](./v1/examples/python-requests-client.ko.md)
   - [httpx 클라이언트 가이드](./v1/examples/python-httpx-client.ko.md)
   - [FastAPI 서버 가이드](./v1/examples/python-fastapi-server.ko.md)

2. **TypeScript 예제 탐색**
   - CDP SDK 클라이언트: `external/x402/examples/typescript/clients/cdp-sdk/`
   - Express 서버: `external/x402/examples/typescript/servers/express/`

3. **Discovery 기능 배우기** (v1 Legacy)
   - [Discovery 가이드](./v1/examples/python-discovery.ko.md)

4. **고급 주제**
   - Mainnet 배포
   - 커스텀 결제 로직
   - AI 에이전트 통합

### 유용한 리소스

- 📖 [x402 공식 문서](https://docs.cdp.coinbase.com/x402/welcome)
- 💻 [x402 GitHub](https://github.com/coinbase/x402)
- 🔵 [Base 문서](https://docs.base.org)
- 🇰🇷 [한글 커뮤니티 리소스](../../resources/korean-community.md)

---

## 문제 해결

### API 키 생성 실패

**증상**: API 키 생성 시 오류 발생

**해결 방법**:
1. 2FA가 올바르게 설정되었는지 확인
2. 브라우저 캐시 삭제 후 재시도
3. CDP 지원팀에 문의

### Wallet Secret을 분실한 경우

**해결 방법**:
1. 새로운 Wallet Secret을 생성합니다
2. 기존 월렛은 접근 불가능할 수 있으므로, 필요시 새 월렛을 생성합니다
3. 앱에서 환경 변수를 업데이트합니다

### USDC Faucet이 작동하지 않음

**해결 방법**:
1. 하루 한도를 초과했을 수 있습니다 (24시간 후 재시도)
2. 다른 Faucet (CDP 또는 Circle) 사용
3. Discord나 커뮤니티에서 테스트 USDC 요청

### 환경 변수 인식 오류

**증상**: `CDP_API_KEY_ID` 등의 환경 변수를 찾을 수 없다는 오류

**해결 방법**:
1. `.env` 파일이 올바른 위치에 있는지 확인
2. `dotenv` 패키지가 설치되었는지 확인
3. 환경 변수 이름과 값에 공백이 없는지 확인
4. 멀티라인 키의 경우 올바른 형식인지 확인

### 2FA 코드가 작동하지 않음

**해결 방법**:
1. 시스템 시간이 정확한지 확인
2. 2FA 앱을 재동기화
3. 백업 코드 사용
4. CDP 지원팀에 계정 복구 요청

---

## 기여하기

이 가이드에 오류나 누락된 정보가 있나요? 도움을 주세요!

- 🐛 [이슈 생성](https://github.com/YOUR_USERNAME/awesome-x402-on-base/issues/new) - 오류 보고 또는 개선 제안
- 📝 [Pull Request](https://github.com/YOUR_USERNAME/awesome-x402-on-base/pulls) - 직접 문서 개선
- 💬 [Discussions](https://github.com/YOUR_USERNAME/awesome-x402-on-base/discussions) - 질문 및 토론

여러분의 기여가 한국 x402 커뮤니티를 더욱 강하게 만듭니다! 🙏

---

## 라이선스

이 문서는 [MIT License](../../LICENSE)에 따라 제공됩니다.

---

**작성**: Logan (Base Korea Developer Ambassador)  
**마지막 업데이트**: 2025년 11월 8일  
**다음 검토 예정**: 2025년 12월  

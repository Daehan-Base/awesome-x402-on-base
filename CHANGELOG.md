# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2025-12-27]

### Added
- **Agent Skills** - [agentskills.io](https://agentskills.io) 오픈 스탠다드 준수 ([#16](https://github.com/Daehan-Base/awesome-x402-on-base/pull/16))
  - `.agents/skills/` 디렉토리에 4개 skill 추가
  - `validate-links`: 문서 링크 유효성 검사
  - `sync-docs`: 한/영 문서 쌍 확인 + 수정일 비교
  - `create-doc`: 문서 템플릿 생성
  - `check-contribution`: PR 전 체크리스트
  - `.claude/skills/` 심볼릭 링크로 Claude Code 연동
- **docs/ 루트 인덱스** - README.md, README.en.md 추가
- **docs/python/** - Python 문서 디렉토리 신설 (README.md, README.en.md)
- **docs/python/v1/** - feature-based 구조로 재편성
  - `clients/requests/`, `clients/httpx/`, `servers/fastapi/`, `discovery/`
- **Python v1 영문 문서** - 4개 README.en.md 추가 (requests, httpx, fastapi, discovery)
- **docs/typescript/** - TypeScript 문서 디렉토리 신설 (v1/, v2/)
- **docs/typescript/v2/fullstack/** - fullstack README 추가
- **external/README.en.md** - 영문 버전 추가
- **Python v2 SDK 참조** - PR [#841](https://github.com/coinbase/x402/pull/841) 링크 추가

### Changed
- **External 링크 이원화** - 모든 외부 x402 참조에 이중 링크 적용 (30개 파일)
  - 📂 로컬: `external/x402/` 서브모듈 경로
  - 🔗 원본: GitHub coinbase/x402 레포 링크
  - 테이블 형식: "로컬 코드" + "원본 레포" 열 분리
- **디렉토리 구조 재편** - "language-first" 패턴 도입
  - `docs/korean/` → `docs/` (언어 접두사 제거)
  - `docs/korean/v1/examples/` → `docs/python/v1/` (언어 → 버전 → 기능 구조)
  - `docs/korean/examples/typescript/` → `docs/typescript/v2/`
- **파일명 컨벤션 변경** - `.ko.md` 접미사 제거
  - `getting_started.ko.md` → `getting_started.md`
  - `x402-v2-specification.ko.md` → `x402-v2-specification.md`
- **examples/ 구조 변경** - 언어별 분류
  - `examples/v1/` → `examples/python/v1/`
  - `examples/v2/` → `examples/python/v2/`
- **Python v1 문서 구조** - 예제별 파일 → 기능별 디렉토리
  - `python-requests-client.ko.md` → `clients/requests/README.md`
  - `python-httpx-client.ko.md` → `clients/httpx/README.md`
  - `python-fastapi-server.ko.md` → `servers/fastapi/README.md`
  - `python-discovery.ko.md` → `discovery/README.md`
- **external/README.md** - 한국어를 기본으로 변경
- **TypeScript 예제 테이블** - 공식 coinbase/x402 GitHub 링크 추가
- **README.md, claude.md** - 새 디렉토리 구조 반영

### Removed
- `docs/korean/` 디렉토리 (→ `docs/`로 이동)
- `external/README.ko.md` (→ `README.md`가 한국어 기본)

---

## [2025-12-16]

### Added
- CONTRIBUTING.md 기여 가이드 추가
- x402 v2 프로토콜 스펙 한국어 문서 (`x402-v2-specification.ko.md`)
- v1/v2 디렉토리 구조 재편성 (`docs/korean/v1/`, `docs/korean/v2/`, `examples/v1/`, `examples/v2/`)
- 각 디렉토리별 README.md 추가
- GitHub Issue 템플릿 추가 (기능/예제 제안용) ([#5](https://github.com/Daehan-Base/awesome-x402-on-base/pull/5))
- **이중 언어 README 지원** - 모든 디렉토리에 README.md(한글) + README.en.md(영어) 쌍 추가
- v1 → v2 마이그레이션 가이드 링크 추가 (모든 v1/v2 문서)

### Changed
- README.md 기여하기 섹션 업데이트 (CONTRIBUTING.md 링크 추가)
- CLAUDE.md를 AI 코딩 에이전트 가이드라인 포맷으로 재구성 (729줄 → 193줄)
- 한글 예제 문서를 `docs/korean/v1/examples/`로 이동
- 서브모듈 링크를 GitHub URL로 변경 (접근성 개선)
- `korean-community.md` 실제 커뮤니티 링크로 업데이트
  - Daehan Base X, Telegram, Luma 추가
  - CDP Discord 추가
  - 이벤트 섹션을 Luma 구독 안내로 통합

### Fixed
- 깨진 문서 링크 수정 (`docs/korean/examples/` → `docs/korean/v1/examples/`)
- `YOUR_USERNAME` 플레이스홀더를 `Daehan-Base`로 교체
- `examples/v1/README.ko.md` 제거 (README.md로 통합)

---

## [2025-12-15]

### Fixed
- x402 v2 마이그레이션에 따른 Python 예제 경로 업데이트 ([#4](https://github.com/Daehan-Base/awesome-x402-on-base/pull/4))
  - `/examples/python/` → `/examples/python/legacy/`
- 문서 링크 및 디렉토리 구조 업데이트 ([#3](https://github.com/Daehan-Base/awesome-x402-on-base/pull/3))
  - 한글 가이드 링크를 `getting_started.ko.md`로 수정
  - `ap2-demo-coffee-shop` 디렉토리 구조 반영
  - Git 서브모듈 초기화 안내 강화

---

## [2025-12-11]

### Added
- 커피숍 에이전트 로깅 기능 강화 ([#2](https://github.com/Daehan-Base/awesome-x402-on-base/pull/2))
  - 다중 에이전트 상호작용 추적
  - 유저 에이전트 메시지, Task 정보, Session 정보 로깅

### Changed
- 프로젝트 문서 통합 및 규칙 단일화 ([#1](https://github.com/Daehan-Base/awesome-x402-on-base/pull/1))
  - Cursor AI 규칙과 Claude Code 컨텍스트를 `claude.md`로 통합
  - `.cursor/` 디렉토리 제거
  - `AGENTS.md`를 `CLAUDE.md`로 심볼릭 링크 설정

---

## [2025-11-22] - Initial Release

### Added
- 프로젝트 초기 설정
- Git 서브모듈로 공식 x402 레포지토리 연결 (`external/x402/`)
- 한국어 문서 기반 구축
  - `getting_started.ko.md` - 시작 가이드
  - Python 예제 튜토리얼 4개 (requests, httpx, fastapi, discovery)
- AP2 커피숍 데모 예제 (`examples/ap2-demo-coffee-shop/`)
- README.md (한글/영문)
- ROADMAP.md 개발 로드맵
- PR 템플릿

---

[2025-12-27]: https://github.com/Daehan-Base/awesome-x402-on-base/compare/a486461...HEAD
[2025-12-16]: https://github.com/Daehan-Base/awesome-x402-on-base/compare/87385c4...a486461
[2025-12-15]: https://github.com/Daehan-Base/awesome-x402-on-base/compare/722dda8...87385c4
[2025-12-11]: https://github.com/Daehan-Base/awesome-x402-on-base/compare/c79bfeb...722dda8
[2025-11-22]: https://github.com/Daehan-Base/awesome-x402-on-base/releases/tag/v0.1.0

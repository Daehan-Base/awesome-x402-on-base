# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2025-12-16]

### Added
- CONTRIBUTING.md 기여 가이드 추가
- x402 v2 프로토콜 스펙 한국어 문서 (`x402-v2-specification.ko.md`)
- v1/v2 디렉토리 구조 재편성 (`docs/korean/v1/`, `docs/korean/v2/`, `examples/v1/`, `examples/v2/`)
- 각 디렉토리별 README.md 추가
- GitHub Issue 템플릿 추가 (기능/예제 제안용) ([#5](https://github.com/Daehan-Base/awesome-x402-on-base/pull/5))

### Changed
- README.md 기여하기 섹션 업데이트 (CONTRIBUTING.md 링크 추가)
- CLAUDE.md를 AI 코딩 에이전트 가이드라인 포맷으로 재구성 (729줄 → 193줄)
- 한글 예제 문서를 `docs/korean/v1/examples/`로 이동

### Fixed
- 깨진 문서 링크 수정 (`docs/korean/examples/` → `docs/korean/v1/examples/`)
- `YOUR_USERNAME` 플레이스홀더를 `Daehan-Base`로 교체

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

[2025-12-16]: https://github.com/Daehan-Base/awesome-x402-on-base/compare/87385c4...HEAD
[2025-12-15]: https://github.com/Daehan-Base/awesome-x402-on-base/compare/722dda8...87385c4
[2025-12-11]: https://github.com/Daehan-Base/awesome-x402-on-base/compare/c79bfeb...722dda8
[2025-11-22]: https://github.com/Daehan-Base/awesome-x402-on-base/releases/tag/v0.1.0

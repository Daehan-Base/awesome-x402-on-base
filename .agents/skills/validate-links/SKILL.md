---
name: validate-links
description: Validates document links for correctness. Use when adding links to documentation, before submitting PRs, or after updating the x402 submodule. Checks local paths (external/x402/...), GitHub URLs, and relative document links.
compatibility: Requires git repository access. Works with Claude Code and similar agents.
---

# Validate Links

문서 내 링크의 유효성을 검사합니다.

## 사용 시점

- 문서에 링크 추가 후
- PR 제출 전 검증
- `external/x402/` 서브모듈 업데이트 후

## 검증 대상

### 1. 로컬 경로 (파일 존재 여부)

```
external/x402/examples/python/legacy/clients/requests/
docs/python/v1/README.md
```

### 2. 상대 경로 (문서간 링크)

```
../README.md
../../getting_started.md
```

### 3. GitHub 원본 링크 (HTTP 상태)

```
https://github.com/coinbase/x402/tree/main/examples/...
```

## 검증 방법

### Step 1: 대상 파일 지정

특정 파일 또는 디렉토리를 지정하세요:
- 단일 파일: `docs/python/v1/README.md`
- 디렉토리: `docs/` (하위 모든 .md 파일)

### Step 2: 링크 추출 및 검증

마크다운 파일에서 다음 패턴을 추출:
- `[텍스트](경로)` - 일반 링크
- `[텍스트](경로 "제목")` - 제목 포함 링크

### Step 3: 검증 실행

**로컬 경로 검증**:
```bash
# 파일 존재 확인
test -e "경로" && echo "OK" || echo "NOT FOUND"
```

**상대 경로 검증**:
```bash
# 현재 파일 기준 상대 경로 해석
realpath --relative-to=. "기준파일/../경로"
```

**외부 URL 검증** (선택적):
```bash
# HTTP HEAD 요청으로 상태 확인
curl -sI "URL" | head -1
```

## 출력 형식

```
[validate-links] 검증 결과

검사 파일: docs/python/v1/README.md

✅ 유효한 링크 (5개)
  - ./clients/requests/README.md
  - ../../../external/x402/examples/python/legacy/...
  - https://github.com/coinbase/x402/...

❌ 깨진 링크 (2개)
  - Line 15: ./old-path/README.md (NOT FOUND)
  - Line 45: https://github.com/coinbase/x402/old-page (404)

권장 조치:
1. Line 15: 경로를 ./new-path/README.md로 수정
2. Line 45: 최신 URL 확인 필요
```

## 이 프로젝트의 특수 규칙

### 이원화 링크 패턴

이 레포지토리는 로컬 + 원본 링크를 함께 제공합니다:

```markdown
| 📂 로컬 | 🔗 원본 |
|---------|---------|
| [external/x402/...](../external/x402/...) | [coinbase/x402/...](https://github.com/coinbase/x402/...) |
```

**검증 시 둘 다 확인하세요.**

### external/x402/ 경로 규칙

서브모듈 경로는 다음 구조를 따릅니다:
```
external/x402/examples/{language}/{version}/{type}/{name}/
```

예시:
- `external/x402/examples/python/legacy/clients/requests/`
- `external/x402/examples/typescript/clients/axios/`

## 관련 Skills

- `sync-docs`: 한/영 문서 쌍 확인
- `check-contribution`: PR 전 종합 체크

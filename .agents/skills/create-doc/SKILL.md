---
name: create-doc
description: Creates documentation templates following project conventions. Use when adding new examples or documentation sections. Generates Korean/English README pairs with proper headers, link tables, and navigation.
compatibility: Works with Claude Code and similar agents.
---

# Create Doc

프로젝트 규칙을 준수하는 문서 템플릿을 생성합니다.

## 사용 시점

- 새 예제 추가 시
- 새 문서 섹션 생성 시
- 기존 문서 표준화 시

## 생성되는 요소

### 1. 언어 스위처 헤더

```markdown
[한국어](./README.md) | [English](./README.en.md)
```

### 2. Legacy 경고 (v1 문서용)

```markdown
> ⚠️ **Legacy 문서 (v1)**
>
> 이 문서는 x402 **v1 SDK**를 다룹니다.
> 최신 v2 스펙은 [x402-v2-specification.md](경로)를 참조하세요.
```

### 3. 이원화 링크 테이블

```markdown
| 구분 | 경로 |
|------|------|
| 📂 로컬 | [`external/x402/...`](상대경로) |
| 🔗 원본 | [coinbase/x402/...](GitHub URL) |
```

### 4. 작성 시점 메타데이터

```markdown
> **작성일**: 2025년 12월 27일
> **최종 검증**: x402 v2.x.x 기준
```

### 5. 푸터 네비게이션

```markdown
---

[← 상위 문서](../README.md) | [다음 문서 →](./next/README.md)
```

## 사용 방법

### Step 1: 경로 지정

생성할 문서의 경로를 지정하세요:
- `docs/python/v2/clients/httpx/` (새 디렉토리)
- `examples/python/v2/demo-app/` (새 예제)

### Step 2: 버전 선택

- **v1 (Legacy)**: 레거시 경고 포함
- **v2 (Latest)**: 최신 버전 표시

### Step 3: 템플릿 적용

`templates/` 디렉토리의 템플릿을 참조하여 생성:
- `readme-ko.md` → `README.md`
- `readme-en.md` → `README.en.md`

## 템플릿 파일

### 한국어 (templates/readme-ko.md)

```markdown
[한국어](./README.md) | [English](./README.en.md)

# {{제목}}

{{#if isLegacy}}
> ⚠️ **Legacy 문서 (v1)**
>
> 이 문서는 x402 **v1 SDK**를 다룹니다.
> 최신 v2 스펙은 [x402-v2-specification.md]({{v2SpecPath}})를 참조하세요.
{{/if}}

> **작성일**: {{date}}

## 개요

{{설명}}

## 코드 위치

| 구분 | 경로 |
|------|------|
| 📂 로컬 | [`{{localPath}}`]({{localRelativePath}}) |
| 🔗 원본 | [{{repoPath}}]({{githubUrl}}) |

## 설정 및 실행

1. 환경 설정
2. 의존성 설치
3. 실행

## 다음 단계

- [관련 문서](링크)

---

[← 상위 문서](../README.md)
```

### 영어 (templates/readme-en.md)

```markdown
[한국어](./README.md) | [English](./README.en.md)

# {{title}}

{{#if isLegacy}}
> ⚠️ **Legacy Documentation (v1)**
>
> This document covers the x402 **v1 SDK**.
> For the latest v2 specification, see [x402-v2-specification.md]({{v2SpecPath}}).
{{/if}}

> **Created**: {{date}}

## Overview

{{description}}

## Code Location

| Type | Path |
|------|------|
| 📂 Local | [`{{localPath}}`]({{localRelativePath}}) |
| 🔗 Original | [{{repoPath}}]({{githubUrl}}) |

## Setup and Run

1. Environment setup
2. Install dependencies
3. Run

## Next Steps

- [Related docs](link)

---

[← Parent](../README.md)
```

## 출력 예시

```
[create-doc] 문서 생성 완료

생성 경로: docs/python/v2/clients/httpx/

생성된 파일:
  ✅ README.md (한국어)
  ✅ README.en.md (English)

적용된 설정:
  - 버전: v2 (Latest)
  - 언어 스위처: 포함
  - 이원화 링크: 포함
  - 푸터 네비게이션: 포함

다음 단계:
1. 생성된 파일의 {{placeholder}}를 실제 내용으로 교체
2. validate-links로 링크 검증
3. sync-docs로 동기화 확인
```

## 관련 Skills

- `sync-docs`: 생성 후 동기화 확인
- `validate-links`: 링크 검증

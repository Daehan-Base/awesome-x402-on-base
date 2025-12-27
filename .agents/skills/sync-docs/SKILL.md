---
name: sync-docs
description: Checks Korean/English document pair synchronization. Use after creating new documents or changing directory structure. Verifies that every README.md has a corresponding README.en.md and vice versa.
compatibility: Works with Claude Code and similar agents.
---

# Sync Docs

한국어/영어 문서 쌍의 동기화 상태를 확인합니다.

## 사용 시점

- 새 문서 작성 후
- 디렉토리 구조 변경 후
- PR 제출 전

## 이 프로젝트의 규칙

### 필수 쌍 구조

모든 README는 한/영 쌍으로 존재해야 합니다:

```
docs/python/v1/
├── README.md      ← 한국어
└── README.en.md   ← 영어
```

### 검사 대상 디렉토리

- `docs/` - 모든 문서
- `examples/` - 예제 설명 문서

## 검사 방법

### Step 1: README.md 파일 검색

```bash
find docs/ examples/ -name "README.md" -type f
```

### Step 2: 대응 파일 확인

각 `README.md`에 대해 `README.en.md` 존재 확인:

```bash
for f in $(find docs/ examples/ -name "README.md"); do
  en_file="${f%.md}.en.md"
  if [ ! -f "$en_file" ]; then
    echo "Missing: $en_file"
  fi
done
```

### Step 3: 역방향 검사

각 `README.en.md`에 대해 `README.md` 존재 확인:

```bash
for f in $(find docs/ examples/ -name "README.en.md"); do
  ko_file="${f%.en.md}.md"
  if [ ! -f "$ko_file" ]; then
    echo "Missing: $ko_file"
  fi
done
```

## 출력 형식

```
[sync-docs] 문서 동기화 검사 결과

검사 범위: docs/, examples/

✅ 동기화 완료 (25쌍)
  - docs/README.md ↔ docs/README.en.md
  - docs/python/v1/README.md ↔ docs/python/v1/README.en.md
  ...

❌ 누락된 영문 문서 (2개)
  - docs/python/v2/README.md → README.en.md 필요
  - examples/python/v2/README.md → README.en.md 필요

❌ 누락된 한글 문서 (0개)

권장 조치:
1. docs/python/v2/README.en.md 생성
2. examples/python/v2/README.en.md 생성

💡 create-doc skill을 사용하면 쌍으로 문서를 생성할 수 있습니다.
```

## 헤더 형식 검증 (선택)

올바른 언어 스위처 헤더가 있는지 확인:

**한국어 문서 (README.md)**:
```markdown
[한국어](./README.md) | [English](./README.en.md)
```

**영어 문서 (README.en.md)**:
```markdown
[한국어](./README.md) | [English](./README.en.md)
```

## 내용 동기화 검증 (선택)

파일 존재 여부뿐 아니라 내용이 동기화되어 있는지 확인합니다.

### 수정일 비교

한글 문서와 영문 문서의 마지막 수정일을 비교하여 동기화 상태 확인:

```bash
for f in $(find docs/ examples/ -name "README.md" -type f); do
  en_file="${f%.md}.en.md"
  if [ -f "$en_file" ]; then
    ko_date=$(git log -1 --format="%ci" -- "$f" 2>/dev/null)
    en_date=$(git log -1 --format="%ci" -- "$en_file" 2>/dev/null)

    if [ "$ko_date" != "$en_date" ]; then
      echo "⚠️ 동기화 필요: $f"
      echo "   한글: $ko_date"
      echo "   영문: $en_date"
    fi
  fi
done
```

### 출력 예시

```
[sync-docs] 내용 동기화 검사 결과

⚠️ 동기화 필요 (2개):

1. docs/python/v1/README.md
   한글: 2025-12-27 10:00:00
   영문: 2025-12-20 15:30:00
   → 한글 문서가 7일 더 최신

2. docs/getting_started.md
   한글: 2025-12-25 09:00:00
   영문: 2025-12-15 14:00:00
   → 한글 문서가 10일 더 최신

권장 조치:
- 영문 문서를 한글 문서 기준으로 업데이트하세요
```

### 동기화 판단 기준

- **같은 날 수정**: 동기화 완료로 간주
- **7일 이상 차이**: 동기화 필요로 경고
- **한글만 최신**: 영문 번역 업데이트 필요
- **영문만 최신**: 한글 문서 업데이트 필요 (드문 케이스)

## 관련 Skills

- `create-doc`: 한/영 문서 쌍 생성
- `validate-links`: 문서 링크 검증
- `check-contribution`: PR 전 종합 체크

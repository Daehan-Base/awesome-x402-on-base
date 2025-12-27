---
name: check-contribution
description: Comprehensive pre-PR checklist for contributions. Use before submitting pull requests. Combines sync-docs, validate-links, and commit message validation into a single workflow.
compatibility: Requires git repository access. Works with Claude Code and similar agents.
---

# Check Contribution

PR 제출 전 모든 필수 항목을 종합 검증합니다.

## 사용 시점

- PR 제출 직전
- 컨트리뷰션 완료 후 최종 점검

## 체크리스트

### 1. 문서 동기화 (sync-docs)

```
- [ ] 모든 README.md에 대응하는 README.en.md 존재
- [ ] 언어 스위처 헤더 포함 ([한국어] | [English])
```

### 2. 링크 유효성 (validate-links)

```
- [ ] 로컬 경로 (external/x402/...) 유효
- [ ] 상대 경로 (../README.md) 유효
- [ ] GitHub 원본 링크 유효 (선택)
```

### 3. 커밋 메시지 형식

```
- [ ] Conventional Commits 형식 준수
- [ ] 한글 + 영문 혼용 가능
```

**유효한 접두사**:
- `feat:` - 새 기능
- `docs:` - 문서 변경
- `fix:` - 버그 수정
- `refactor:` - 리팩토링
- `chore:` - 기타 작업

**예시**:
```
docs: Python v2 클라이언트 가이드 추가
feat: 새로운 예제 ap2-demo-coffee-shop 추가
fix: 깨진 링크 수정
```

### 4. PR 템플릿 준수

`.github/pull_request_template.md` 형식 확인:

```markdown
## 변경 사항
- 변경 내용 설명

## 변경 유형
- [ ] 버그 수정
- [ ] 새 기능
- [ ] 문서 업데이트

## 테스트 방법
1. 테스트 단계

## 체크리스트
- [ ] 코드 스타일 준수
- [ ] 문서 업데이트 완료
```

## 검증 실행 방법

### Step 1: 변경 파일 확인

```bash
git status
git diff --name-only HEAD~1
```

### Step 2: 각 검사 실행

1. **sync-docs**: 문서 쌍 확인
2. **validate-links**: 링크 검증
3. **커밋 메시지**: `git log --oneline -5`

### Step 3: 종합 리포트

## 출력 형식

```
[check-contribution] PR 준비 상태 체크

📋 종합 검사 결과:

1. 문서 동기화
   ✅ 모든 README.md에 대응하는 README.en.md 존재 (25쌍)

2. 링크 유효성
   ⚠️ 1개 깨진 링크 발견
   - docs/README.md:45 → ./old-path.md (NOT FOUND)

3. 커밋 메시지
   ✅ "docs: add TypeScript v2 client guide" - 형식 준수

4. 변경 파일
   - docs/typescript/v2/clients/README.md (추가)
   - docs/typescript/v2/clients/README.en.md (추가)

---

⚠️ 수정 필요 항목: 1개

권장 조치:
1. docs/README.md:45의 링크를 수정하세요

모든 항목 통과 시 PR 제출 가능합니다.
```

## 빠른 검사 (Quick Check)

긴급 수정 시 핵심 항목만 확인:

```bash
# 1. 문서 쌍 확인
find docs/ examples/ -name "README.md" | while read f; do
  [ ! -f "${f%.md}.en.md" ] && echo "Missing: ${f%.md}.en.md"
done

# 2. 커밋 메시지 형식
git log -1 --pretty=format:"%s" | grep -E "^(feat|docs|fix|refactor|chore):"
```

## 관련 Skills

- `sync-docs`: 문서 동기화 상세 검사
- `validate-links`: 링크 상세 검증

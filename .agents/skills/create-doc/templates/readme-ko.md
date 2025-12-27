[한국어](./README.md) | [English](./README.en.md)

# {{제목}}

<!-- v1 Legacy인 경우 아래 블록 포함 -->
<!--
> ⚠️ **Legacy 문서 (v1)**
>
> 이 문서는 x402 **v1 SDK**를 다룹니다.
> 최신 v2 스펙은 [x402-v2-specification.md]({{v2SpecPath}})를 참조하세요.
>
> **예제 경로**:
> - 📂 로컬: [`{{localPath}}`]({{localRelativePath}})
> - 🔗 원본: [{{repoPath}}]({{githubUrl}})
-->

> **작성일**: {{YYYY년 MM월 DD일}}

## 개요

{{간단한 설명을 작성하세요}}

## 코드 위치

| 구분 | 경로 |
|------|------|
| 📂 로컬 | [`{{localPath}}`]({{localRelativePath}}) |
| 🔗 원본 | [{{repoPath}}]({{githubUrl}}) |

## 사전 요구사항

- Python 3.10+ / Node.js 18+
- uv / pnpm
- Base Sepolia 테스트넷 ETH 및 USDC

## 설정 및 실행

### 1. 환경 설정

```bash
cd {{경로}}
cp .env-local .env
# .env 파일에 PRIVATE_KEY 추가
```

### 2. 의존성 설치

```bash
uv sync  # Python
# 또는
pnpm install  # TypeScript
```

### 3. 실행

```bash
uv run python main.py  # Python
# 또는
pnpm dev  # TypeScript
```

## 주요 개념

### {{개념 1}}

{{설명}}

### {{개념 2}}

{{설명}}

## 다음 단계

- [{{관련 문서 1}}](링크)
- [{{관련 문서 2}}](링크)

---

[← 상위 문서](../README.md) | [다음 문서 →]({{nextPath}})

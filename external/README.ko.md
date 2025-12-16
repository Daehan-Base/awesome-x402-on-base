# 외부 리소스

## 📝 요약 (TL;DR)

**What**: 공식 [coinbase/x402](https://github.com/coinbase/x402) 레포지토리를 연결하는 Git 서브모듈  
**Why**: 코드 중복 방지, 항상 최신 공식 예제 참조  
**Usage**: 읽기 전용 - `docs/korean/`의 한글 가이드를 따라하세요  
**Update**: `git submodule update --remote external/x402`  

---

이 디렉토리는 외부 레포지토리의 Git 서브모듈을 포함합니다.

## x402 공식 레포지토리

**서브모듈**: `external/x402/`
**출처**: https://github.com/coinbase/x402

### 포함된 내용

공식 x402 레포지토리에는 다음이 포함됩니다:
- Python SDK 구현
- Python 예제 (클라이언트, 서버, discovery)
- TypeScript 예제
- Go 구현
- Java 구현
- 프로토콜 사양

### 예제 접근하기

⚠️ **참고**: 서브모듈을 먼저 초기화해야 합니다:
```bash
git submodule update --init --recursive
```

그런 다음 Python 예제로 이동:
```bash
cd external/x402/examples/python/legacy

# 사용 가능한 예제:
# - clients/requests/  - Python requests 클라이언트 예제
# - clients/httpx/     - Python httpx 클라이언트 예제
# - servers/           - Python 서버 예제
# - discovery/         - x402 discovery 예제
```

### 한글 가이드

각 공식 예제에 대해 한글 문서를 제공합니다:

| 예제 | 코드 | 한글 가이드 |
|------|------|------------|
| requests 클라이언트 | `./x402/examples/python/legacy/clients/requests` | [→ 가이드](../docs/korean/v1/examples/python-requests-client.ko.md) |
| httpx 클라이언트 | `./x402/examples/python/legacy/clients/httpx` | [→ 가이드](../docs/korean/v1/examples/python-httpx-client.ko.md) |
| Python 서버 | `./x402/examples/python/legacy/servers` | [→ 가이드](../docs/korean/v1/examples/python-fastapi-server.ko.md) |
| Discovery | `./x402/examples/python/legacy/discovery` | [→ 가이드](../docs/korean/v1/examples/python-discovery.ko.md) |

### 서브모듈 업데이트

공식 레포지토리의 최신 변경사항을 받으려면:

```bash
git submodule update --remote external/x402
```

### 중요 사항

⚠️ **이 디렉토리의 파일을 직접 수정하지 마세요**. 이것은 공식 레포지토리에 대한 읽기 전용 참조입니다. 모든 수정사항은 루트 레벨의 `examples/` 디렉토리에서 이루어져야 합니다.

---

[← 메인 README로 돌아가기](../README.md)

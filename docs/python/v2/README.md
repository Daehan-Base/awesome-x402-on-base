[한국어](./README.md) | [English](./README.en.md)

# x402 v2 한국어 문서

> **x402 v2 SDK** 관련 문서입니다.
> v2는 2025년 12월 11일에 출시되었습니다.
>
> 📚 **v1에서 마이그레이션**: [Migration Guide](https://docs.cdp.coinbase.com/x402/migration-guide)

---

## v2 스펙 문서

- [x402-v2-specification.md](../../x402-v2-specification.md) - v2 프로토콜 전체 명세서

---

## v2 신기능

1. **다중 체인 지원** - Base, Solana, EVM 호환 체인 (CAIP 표준)
2. **다중 Transport** - HTTP, MCP (AI 에이전트), A2A (에이전트간)
3. **향상된 보안** - ERC1271, ERC6492 지원
4. **세션 관리** - 지갑 기반 재사용 액세스
5. **플러그인 아키텍처** - 독립적인 체인/결제 방식 확장
6. **동적 라우팅** - 요청별 `payTo` 수신자 지정
7. **자동 API 발견** - Bazaar/Discovery API

---

## v2 예제 (준비 중)

> 🚧 **Python v2 SDK 작업 중**: [PR #841](https://github.com/coinbase/x402/pull/841)
>
> TypeScript 예제:
> - 📂 로컬: [`external/x402/examples/typescript/`](../../../external/x402/examples/typescript/)
> - 🔗 원본: [coinbase/x402/.../examples/typescript/](https://github.com/coinbase/x402/tree/main/examples/typescript)

### TypeScript 예제

| 예제 | 로컬 코드 | 원본 레포 |
|------|----------|----------|
| 클라이언트 | [→ 로컬](../../../external/x402/examples/typescript/clients/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/clients/) |
| 서버 | [→ 로컬](../../../external/x402/examples/typescript/servers/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/servers/) |
| Facilitator | [→ 로컬](../../../external/x402/examples/typescript/facilitator/) | [→ 원본](https://github.com/coinbase/x402/tree/main/examples/typescript/facilitator/) |

---

[← 한국어 문서로 돌아가기](../README.md) | [v1 Legacy 보기 →](../v1/README.md)

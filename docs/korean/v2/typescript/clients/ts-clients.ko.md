# x402 Client 예제

이 디렉토리는 x402로 보호되는 엔드포인트에 HTTP 요청을 보내는 방법을 보여주는 TypeScript 기반 클라이언트 예제들을 포함하고 있습니다.

## 디렉토리 구조

| 디렉토리                                                            | 설명                                                    |
| ------------------------------------------------------------------- | ------------------------------------------------------- |
| [`fetch/`](/external/x402/examples/typescript/clients/fetch/)       | 네이티브 Fetch API와 함께 `@x402/fetch`를 사용하는 예제 |
| [`axios/`](/external/x402/examples/typescript/clients/axios/)       | Axios와 함께 `@x402/axios`를 사용하는 예제              |
| [`advanced/`](/external/x402/examples/typescript/clients/advanced/) | 고급 패턴: 라이프사이클 훅, 네트워크 선호도 설정        |
| [`custom/`](/external/x402/examples/typescript/clients/custom/)     | `@x402/core`만을 사용한 수동 구현 예제                  |

## 프레임워크 예제

**fetch** 및 **axios** 디렉토리는 HTTP 클라이언트에 x402 결제를 최소한의 방식으로 통합하는 방법을 보여줍니다. 이 예제들은 402 결제 흐름을 자동으로 처리하는 클라이언트 인터셉터를 사용합니다.

1. 402 응답 인터셉트
2. 결제 오구 사항 파싱
3. 결제 생성 및 서명
4. 결제 헤더를 포함하여 요청 재시도

사용 중인 HTTP 클라이언트에 맞는 예제를 선택하세요.

## 고급 예제

**advanced** 디렉토리는 클라이언트 인터셉터에서 지원하는 고급 기능들을 구현합니다.

- **라이프사이클 훅(Lifecycle Hooks)** — 결제 생성 이전(before)/이후(after)의 사용자 정의 로직 실행
- **네트워크 선호도(Network Preferences)** — 선호하는 결제 네트워크 설정 및 fallback 구성

이러한 패턴은 관측성(observability), 커스텀 검증, 사용자 선호도 관리가 필요한 프로덕션 환경에서 유용합니다.

## 커스텀 구현

**custom** 디렉토리는 클라이언트 인터셉터 없이 `@x402/core`만을 사용하여 x402 결제 처리를 직접 구현하는 방법을 보여줍니다.

- 결제 플로우에 대한 완전한 제어가 필요한 경우
- 아직 지원되지 않는 HTTP 클라이언트와 통합해야 하는 경우
- x402의 내부 동작 원리를 깊이 이해하고 싶은 경우

## 시작하기

1. 원하는 예제 디렉토리를 선택합니다.
2. 해당 디렉토리의 README를 따라 진행합니다.
3. 테스트를 위해 실행 중인 [서버](/external/x402/examples/typescript/servers/)가 있는지 확인합니다.

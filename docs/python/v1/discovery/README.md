[한국어](./README.md) | [English](./README.en.md)

# x402 Discovery 예제 (v1 Legacy)

> ⚠️ **Legacy 문서 (v1)**
>
> 이 문서는 x402 **v1 SDK**를 다룹니다.
> 최신 v2 스펙은 [x402-v2-specification.md](../../../x402-v2-specification.md)를 참조하세요.
>
> **v1 예제 경로**:
> - 📂 로컬: [`external/x402/examples/python/legacy/discovery/`](../../../../external/x402/examples/python/legacy/discovery/)
> - 🔗 원본: [coinbase/x402/.../python/legacy/discovery/](https://github.com/coinbase/x402/tree/main/examples/python/legacy/discovery)

---

x402 패키지의 discovery 기능을 사용하여 네트워크상의 x402로 보호된 리소스를 검색하고 나열하는 방법을 소개합니다.

## x402 Discovery란?

x402 Discovery는 네트워크상에서 사용 가능한 모든 x402로 보호된 리소스를 자동으로 찾아주는 기능입니다. 이를 통해 개발자는:

- **리소스 탐색**: 사용 가능한 모든 x402 보호 API와 서비스를 자동으로 검색
- **메타데이터 확인**: 각 리소스의 결제 방법, 가격, 네트워크 정보 확인
- **서비스 카탈로그**: x402 생태계의 서비스 디렉토리 역할
- **동적 연결**: 하드코딩 없이 동적으로 서비스 검색 및 연결

## 왜 Discovery가 유용한가?

### 1. 서비스 검색 자동화
수동으로 API 엔드포인트를 찾는 대신, Discovery를 통해 자동으로 사용 가능한 모든 서비스를 찾을 수 있습니다.

### 2. 투명한 가격 정보
각 리소스가 요구하는 결제 금액, 토큰 종류, 네트워크 정보를 사전에 확인할 수 있습니다.

### 3. 동적 생태계
새로운 서비스가 추가되면 자동으로 검색되어 애플리케이션에서 즉시 활용할 수 있습니다.

### 4. 개발자 경험 향상
API 문서를 찾아다니지 않고도 사용 가능한 모든 엔드포인트와 그 스펙을 한 번에 확인할 수 있습니다.

## 전제 조건

- Python 3.10 이상
- uv 패키지 매니저 ([docs.astral.sh/uv](https://docs.astral.sh/uv/)에서 설치)

## 설정 및 사용법

### 1. 의존성 설치

Python 예제 루트 디렉토리에서 모든 패키지를 설치하고 빌드합니다:

```bash
cd external/x402/examples/python/legacy
uv sync
cd discovery
```

### 2. Discovery 예제 실행

```bash
uv run python main.py
```

**참고**: Discovery 기능은 공개 리소스 목록을 조회하므로 API 키나 개인 키가 필요하지 않습니다.

## Discovery 프로토콜 작동 방식

x402 Discovery 프로토콜은 다음과 같이 동작합니다:

### 1. Facilitator 클라이언트 초기화
```python
from x402.facilitator import FacilitatorClient
from cdp.x402 import create_facilitator_config

# Facilitator 클라이언트 생성 (Discovery는 인증 불필요)
facilitator = FacilitatorClient(create_facilitator_config())
```

### 2. 리소스 목록 조회
```python
# 네트워크상의 모든 x402 리소스 검색
response = await facilitator.list()
```

### 3. 리소스 정보 파싱
각 리소스는 다음 정보를 포함합니다:
- **resource**: 리소스 URL
- **type**: 리소스 타입 (http, websocket 등)
- **lastUpdated**: 마지막 업데이트 시간
- **x402Version**: x402 프로토콜 버전
- **accepts**: 허용되는 결제 방법 배열
  - **scheme**: 가격 책정 방식 (exact, tiered 등)
  - **network**: 블록체인 네트워크 (base-sepolia 등)
  - **maxAmountRequired**: 최대 요구 금액 (wei 단위)
  - **asset**: 결제 토큰 주소
  - **payTo**: 결제 수신 주소
  - **description**: 리소스 설명
  - **mimeType**: 응답 데이터 타입

## 전체 예제 코드

```python
import json
import asyncio
from datetime import datetime
from x402.facilitator import FacilitatorClient
from cdp.x402 import create_facilitator_config

# Facilitator 클라이언트 초기화 (Discovery는 API 키 불필요)
facilitator = FacilitatorClient(create_facilitator_config())

async def main():
    try:
        # 리소스 목록 가져오기
        response = await facilitator.list()

        print("\n발견된 X402 리소스:")
        print("========================\n")

        # 각 리소스를 포맷팅하여 출력
        for index, item in enumerate(response.items, 1):
            print(f"리소스 {index}:")
            # 아이템을 JSON으로 변환하여 적절히 포맷팅
            item_json = json.loads(item.model_dump_json(by_alias=True))
            print(f"  리소스 URL: {item_json['resource']}")
            print(f"  타입: {item_json['type']}")
            print(f"  마지막 업데이트: {datetime.fromisoformat(item_json['lastUpdated'].replace('Z', '+00:00')).strftime('%Y년 %m월 %d일 %H:%M:%S')}")
            print(f"  X402 버전: {item_json['x402Version']}")
            print(f"  허용 결제 방법: {json.dumps(item_json['accepts'], indent=2, ensure_ascii=False)}")
            if item_json.get("metadata"):
                print(f"  메타데이터: {json.dumps(item_json['metadata'], indent=2, ensure_ascii=False)}")
            print("------------------------\n")

    except Exception as e:
        print(f"오류: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 코드 설명

### Facilitator 클라이언트
```python
# Facilitator는 x402 리소스의 중앙 레지스트리 역할
facilitator = FacilitatorClient(create_facilitator_config())
```

### 비동기 리소스 조회
```python
# list() 메소드는 모든 등록된 x402 리소스를 반환
response = await facilitator.list()
```

### 리소스 정보 포맷팅
```python
# 각 리소스를 JSON으로 변환하여 읽기 쉽게 출력
item_json = json.loads(item.model_dump_json(by_alias=True))
```

### 날짜 형식 변환
```python
# ISO 8601 형식의 날짜를 로컬 시간대로 변환
datetime.fromisoformat(item_json['lastUpdated'].replace('Z', '+00:00'))
    .strftime('%Y년 %m월 %d일 %H:%M:%S')
```

## 출력 예시

스크립트는 발견된 모든 x402 리소스를 포맷팅하여 출력합니다:

```
발견된 X402 리소스:
========================

리소스 1:
  리소스 URL: https://api.example.com/x402/endpoint
  타입: http
  마지막 업데이트: 2025년 08월 09일 01:07:04
  X402 버전: 1
  허용 결제 방법: [
    {
      "scheme": "exact",
      "network": "base-sepolia",
      "maxAmountRequired": "1000000",
      "resource": "https://api.example.com/x402/endpoint",
      "description": "예제 보호된 엔드포인트",
      "mimeType": "application/json",
      "payTo": "0x1234567890abcdef1234567890abcdef12345678",
      "maxTimeoutSeconds": 300,
      "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
    }
  ]
  메타데이터: {
    "category": "AI API",
    "rateLimit": "100 requests/hour"
  }
------------------------
```

## 실용적인 사용 사례

### 1. 서비스 디렉토리 구축
```python
async def build_service_catalog():
    """사용 가능한 모든 x402 서비스의 카탈로그 생성"""
    facilitator = FacilitatorClient(create_facilitator_config())
    response = await facilitator.list()

    # 카테고리별로 서비스 분류
    catalog = {}
    for item in response.items:
        item_json = json.loads(item.model_dump_json(by_alias=True))
        category = item_json.get('metadata', {}).get('category', 'Uncategorized')

        if category not in catalog:
            catalog[category] = []
        catalog[category].append({
            'url': item_json['resource'],
            'description': item_json['accepts'][0]['description'],
            'price': item_json['accepts'][0]['maxAmountRequired']
        })

    return catalog
```

### 2. 최저 가격 서비스 찾기
```python
async def find_cheapest_service(service_type: str):
    """특정 타입의 서비스 중 가장 저렴한 것 찾기"""
    facilitator = FacilitatorClient(create_facilitator_config())
    response = await facilitator.list()

    cheapest = None
    min_price = float('inf')

    for item in response.items:
        item_json = json.loads(item.model_dump_json(by_alias=True))

        # 서비스 타입 확인
        if service_type in item_json['accepts'][0].get('description', ''):
            price = int(item_json['accepts'][0]['maxAmountRequired'])
            if price < min_price:
                min_price = price
                cheapest = item_json

    return cheapest
```

### 3. 네트워크별 서비스 필터링
```python
async def filter_by_network(network: str = "base-sepolia"):
    """특정 블록체인 네트워크의 서비스만 필터링"""
    facilitator = FacilitatorClient(create_facilitator_config())
    response = await facilitator.list()

    filtered_services = []

    for item in response.items:
        item_json = json.loads(item.model_dump_json(by_alias=True))

        # 네트워크가 일치하는 서비스만 선택
        for accept in item_json['accepts']:
            if accept['network'] == network:
                filtered_services.append(item_json)
                break

    return filtered_services
```

### 4. 동적 클라이언트 생성
```python
async def create_dynamic_client(service_name: str, account):
    """서비스 이름으로 검색하여 자동으로 클라이언트 생성"""
    from x402.clients import x402HttpxClient

    # Discovery로 서비스 찾기
    facilitator = FacilitatorClient(create_facilitator_config())
    response = await facilitator.list()

    for item in response.items:
        item_json = json.loads(item.model_dump_json(by_alias=True))
        if service_name in item_json['accepts'][0].get('description', ''):
            service_url = item_json['resource']

            # 자동으로 클라이언트 생성 및 반환
            return x402HttpxClient(account=account, base_url=service_url)

    raise ValueError(f"서비스 '{service_name}'를 찾을 수 없습니다")
```

### 5. 서비스 헬스 모니터링
```python
async def monitor_service_updates():
    """서비스의 업데이트 시간을 모니터링하여 활성 상태 확인"""
    from datetime import datetime, timedelta

    facilitator = FacilitatorClient(create_facilitator_config())
    response = await facilitator.list()

    stale_services = []
    threshold = timedelta(hours=24)  # 24시간 이상 업데이트 없으면 오래된 것으로 간주

    for item in response.items:
        item_json = json.loads(item.model_dump_json(by_alias=True))
        last_updated = datetime.fromisoformat(
            item_json['lastUpdated'].replace('Z', '+00:00')
        )

        if datetime.now(last_updated.tzinfo) - last_updated > threshold:
            stale_services.append({
                'url': item_json['resource'],
                'last_updated': last_updated
            })

    return stale_services
```

## Discovery API 상세 정보

### FacilitatorClient 메소드

#### `list()`
네트워크상의 모든 x402 리소스 목록을 반환합니다.

**반환값**: `ListResponse` 객체
- `items`: 리소스 아이템 배열
- 각 아이템은 `ResourceItem` 모델

#### ResourceItem 구조
```python
{
    "resource": str,          # 리소스 URL
    "type": str,              # 리소스 타입 (http, ws 등)
    "lastUpdated": str,       # ISO 8601 형식의 타임스탬프
    "x402Version": int,       # x402 프로토콜 버전
    "accepts": [              # 허용되는 결제 방법 배열
        {
            "scheme": str,                # 가격 책정 방식
            "network": str,               # 블록체인 네트워크
            "maxAmountRequired": str,     # 최대 요구 금액 (wei)
            "resource": str,              # 리소스 URL
            "description": str,           # 설명
            "mimeType": str,              # MIME 타입
            "payTo": str,                 # 결제 수신 주소
            "maxTimeoutSeconds": int,     # 최대 타임아웃 (초)
            "asset": str                  # 결제 토큰 컨트랙트 주소
        }
    ],
    "metadata": dict          # 선택적 메타데이터
}
```

## 예제 코드 위치

```
external/x402/examples/python/legacy/discovery/
├── main.py           # Discovery 예제 메인 코드
├── pyproject.toml    # 프로젝트 의존성
└── README.md         # 영문 문서
```

## 주요 개념 정리

### Facilitator
x402 생태계의 중앙 레지스트리로, 모든 x402 보호 리소스의 메타데이터를 관리합니다.

### Resource Discovery
서비스가 자신을 Facilitator에 등록하면, 다른 클라이언트들이 Discovery를 통해 해당 서비스를 찾을 수 있습니다.

### Payment Metadata
각 리소스는 허용하는 결제 방법, 가격, 네트워크 정보를 명시하여 클라이언트가 사전에 결제 조건을 확인할 수 있습니다.

### Dynamic Service Connection
하드코딩된 URL 대신 Discovery를 통해 동적으로 서비스를 찾고 연결할 수 있어, 유연한 아키텍처 구축이 가능합니다.

## 문제 해결

### 리소스가 표시되지 않는 경우
- Facilitator 서비스가 정상 작동하는지 확인
- 네트워크 연결 상태 확인
- x402 패키지가 최신 버전인지 확인

### 오래된 리소스 정보
- 서비스 제공자가 메타데이터를 업데이트하지 않았을 수 있음
- `lastUpdated` 필드를 확인하여 정보의 신선도 판단

### 네트워크 타임아웃
- Facilitator 서버의 응답 시간이 느릴 수 있음
- 재시도 로직 추가 고려

## 다음 단계

- [requests 클라이언트 예제](../clients/requests/README.md) - 동기 클라이언트로 x402 리소스 사용
- [httpx 클라이언트 예제](../clients/httpx/README.md) - 비동기 클라이언트로 x402 리소스 사용
- [FastAPI 서버 예제](../servers/fastapi/README.md) - x402로 보호된 자체 서비스 구축

---

[← v1 문서로 돌아가기](../README.md) | [v2 스펙 보기 →](../../../x402-v2-specification.md)

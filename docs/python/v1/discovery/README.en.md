[한국어](./README.md) | [English](./README.en.md)

# x402 Discovery Example (v1 Legacy)

> **Legacy Documentation (v1)**
>
> This documentation covers x402 **v1 SDK**.
> For the latest v2 spec, see [x402-v2-specification.md](../../../x402-v2-specification.md).
>
> **v1 Example Path**:
> - 📂 Local: [`external/x402/examples/python/legacy/discovery/`](../../../../external/x402/examples/python/legacy/discovery/)
> - 🔗 Origin: [coinbase/x402/.../python/legacy/discovery/](https://github.com/coinbase/x402/tree/main/examples/python/legacy/discovery)

---

This guide introduces how to use the discovery feature of the x402 package to search for and list x402-protected resources on the network.

## What is x402 Discovery?

x402 Discovery is a feature that automatically finds all x402-protected resources available on the network. With this, developers can:

- **Resource Exploration**: Automatically discover all x402-protected APIs and services
- **Metadata Verification**: Check payment methods, pricing, and network information for each resource
- **Service Catalog**: Act as a directory for services in the x402 ecosystem
- **Dynamic Connection**: Dynamically discover and connect to services without hardcoding

## Why is Discovery Useful?

### 1. Automated Service Discovery
Instead of manually finding API endpoints, use Discovery to automatically find all available services.

### 2. Transparent Pricing Information
Check the payment amount, token type, and network information required by each resource in advance.

### 3. Dynamic Ecosystem
When new services are added, they are automatically discovered and can be used immediately in your application.

### 4. Improved Developer Experience
View all available endpoints and their specifications at once without searching through API documentation.

## Prerequisites

- Python 3.10 or higher
- uv package manager (install from [docs.astral.sh/uv](https://docs.astral.sh/uv/))

## Setup and Usage

### 1. Install Dependencies

Install and build all packages from the Python examples root directory:

```bash
cd external/x402/examples/python/legacy
uv sync
cd discovery
```

### 2. Run Discovery Example

```bash
uv run python main.py
```

**Note**: The Discovery feature queries public resource lists, so no API key or private key is required.

## How the Discovery Protocol Works

The x402 Discovery protocol works as follows:

### 1. Initialize Facilitator Client
```python
from x402.facilitator import FacilitatorClient
from cdp.x402 import create_facilitator_config

# Create Facilitator client (Discovery doesn't require authentication)
facilitator = FacilitatorClient(create_facilitator_config())
```

### 2. Query Resource List
```python
# Search for all x402 resources on the network
response = await facilitator.list()
```

### 3. Parse Resource Information
Each resource contains the following information:
- **resource**: Resource URL
- **type**: Resource type (http, websocket, etc.)
- **lastUpdated**: Last update time
- **x402Version**: x402 protocol version
- **accepts**: Array of accepted payment methods
  - **scheme**: Pricing scheme (exact, tiered, etc.)
  - **network**: Blockchain network (base-sepolia, etc.)
  - **maxAmountRequired**: Maximum required amount (in wei)
  - **asset**: Payment token address
  - **payTo**: Payment receiving address
  - **description**: Resource description
  - **mimeType**: Response data type

## Complete Example Code

```python
import json
import asyncio
from datetime import datetime
from x402.facilitator import FacilitatorClient
from cdp.x402 import create_facilitator_config

# Initialize Facilitator client (Discovery doesn't require API key)
facilitator = FacilitatorClient(create_facilitator_config())

async def main():
    try:
        # Get resource list
        response = await facilitator.list()

        print("\nDiscovered X402 Resources:")
        print("========================\n")

        # Format and print each resource
        for index, item in enumerate(response.items, 1):
            print(f"Resource {index}:")
            # Convert item to JSON for proper formatting
            item_json = json.loads(item.model_dump_json(by_alias=True))
            print(f"  Resource URL: {item_json['resource']}")
            print(f"  Type: {item_json['type']}")
            print(f"  Last Updated: {datetime.fromisoformat(item_json['lastUpdated'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  X402 Version: {item_json['x402Version']}")
            print(f"  Accepted Payment Methods: {json.dumps(item_json['accepts'], indent=2)}")
            if item_json.get("metadata"):
                print(f"  Metadata: {json.dumps(item_json['metadata'], indent=2)}")
            print("------------------------\n")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Code Explanation

### Facilitator Client
```python
# Facilitator serves as the central registry for x402 resources
facilitator = FacilitatorClient(create_facilitator_config())
```

### Async Resource Query
```python
# list() method returns all registered x402 resources
response = await facilitator.list()
```

### Resource Information Formatting
```python
# Convert each resource to JSON for readable output
item_json = json.loads(item.model_dump_json(by_alias=True))
```

### Date Format Conversion
```python
# Convert ISO 8601 format date to local timezone
datetime.fromisoformat(item_json['lastUpdated'].replace('Z', '+00:00'))
    .strftime('%Y-%m-%d %H:%M:%S')
```

## Sample Output

The script formats and outputs all discovered x402 resources:

```
Discovered X402 Resources:
========================

Resource 1:
  Resource URL: https://api.example.com/x402/endpoint
  Type: http
  Last Updated: 2025-08-09 01:07:04
  X402 Version: 1
  Accepted Payment Methods: [
    {
      "scheme": "exact",
      "network": "base-sepolia",
      "maxAmountRequired": "1000000",
      "resource": "https://api.example.com/x402/endpoint",
      "description": "Example protected endpoint",
      "mimeType": "application/json",
      "payTo": "0x1234567890abcdef1234567890abcdef12345678",
      "maxTimeoutSeconds": 300,
      "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
    }
  ]
  Metadata: {
    "category": "AI API",
    "rateLimit": "100 requests/hour"
  }
------------------------
```

## Practical Use Cases

### 1. Building a Service Directory
```python
async def build_service_catalog():
    """Create a catalog of all available x402 services"""
    facilitator = FacilitatorClient(create_facilitator_config())
    response = await facilitator.list()

    # Categorize services
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

### 2. Finding the Cheapest Service
```python
async def find_cheapest_service(service_type: str):
    """Find the cheapest service of a specific type"""
    facilitator = FacilitatorClient(create_facilitator_config())
    response = await facilitator.list()

    cheapest = None
    min_price = float('inf')

    for item in response.items:
        item_json = json.loads(item.model_dump_json(by_alias=True))

        # Check service type
        if service_type in item_json['accepts'][0].get('description', ''):
            price = int(item_json['accepts'][0]['maxAmountRequired'])
            if price < min_price:
                min_price = price
                cheapest = item_json

    return cheapest
```

### 3. Filtering Services by Network
```python
async def filter_by_network(network: str = "base-sepolia"):
    """Filter services by specific blockchain network"""
    facilitator = FacilitatorClient(create_facilitator_config())
    response = await facilitator.list()

    filtered_services = []

    for item in response.items:
        item_json = json.loads(item.model_dump_json(by_alias=True))

        # Select only services matching the network
        for accept in item_json['accepts']:
            if accept['network'] == network:
                filtered_services.append(item_json)
                break

    return filtered_services
```

### 4. Dynamic Client Creation
```python
async def create_dynamic_client(service_name: str, account):
    """Search by service name and automatically create client"""
    from x402.clients import x402HttpxClient

    # Find service via Discovery
    facilitator = FacilitatorClient(create_facilitator_config())
    response = await facilitator.list()

    for item in response.items:
        item_json = json.loads(item.model_dump_json(by_alias=True))
        if service_name in item_json['accepts'][0].get('description', ''):
            service_url = item_json['resource']

            # Automatically create and return client
            return x402HttpxClient(account=account, base_url=service_url)

    raise ValueError(f"Service '{service_name}' not found")
```

### 5. Service Health Monitoring
```python
async def monitor_service_updates():
    """Monitor service update times to check active status"""
    from datetime import datetime, timedelta

    facilitator = FacilitatorClient(create_facilitator_config())
    response = await facilitator.list()

    stale_services = []
    threshold = timedelta(hours=24)  # Consider stale if no update for 24+ hours

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

## Discovery API Details

### FacilitatorClient Methods

#### `list()`
Returns a list of all x402 resources on the network.

**Returns**: `ListResponse` object
- `items`: Array of resource items
- Each item is a `ResourceItem` model

#### ResourceItem Structure
```python
{
    "resource": str,          # Resource URL
    "type": str,              # Resource type (http, ws, etc.)
    "lastUpdated": str,       # ISO 8601 format timestamp
    "x402Version": int,       # x402 protocol version
    "accepts": [              # Array of accepted payment methods
        {
            "scheme": str,                # Pricing scheme
            "network": str,               # Blockchain network
            "maxAmountRequired": str,     # Maximum required amount (wei)
            "resource": str,              # Resource URL
            "description": str,           # Description
            "mimeType": str,              # MIME type
            "payTo": str,                 # Payment receiving address
            "maxTimeoutSeconds": int,     # Maximum timeout (seconds)
            "asset": str                  # Payment token contract address
        }
    ],
    "metadata": dict          # Optional metadata
}
```

## Example Code Location

```
external/x402/examples/python/legacy/discovery/
├── main.py           # Discovery example main code
├── pyproject.toml    # Project dependencies
└── README.md         # Documentation
```

## Key Concepts Summary

### Facilitator
The central registry of the x402 ecosystem that manages metadata for all x402-protected resources.

### Resource Discovery
When a service registers itself with the Facilitator, other clients can find that service through Discovery.

### Payment Metadata
Each resource specifies accepted payment methods, prices, and network information so clients can verify payment conditions in advance.

### Dynamic Service Connection
Instead of hardcoded URLs, use Discovery to dynamically find and connect to services, enabling flexible architecture.

## Troubleshooting

### Resources Not Displaying
- Verify the Facilitator service is running properly
- Check network connection status
- Ensure the x402 package is the latest version

### Stale Resource Information
- Service providers may not have updated metadata
- Check the `lastUpdated` field to judge information freshness

### Network Timeout
- Facilitator server response time may be slow
- Consider adding retry logic

## Next Steps

- [requests Client Example](../clients/requests/README.en.md) - Use x402 resources with sync client
- [httpx Client Example](../clients/httpx/README.en.md) - Use x402 resources with async client
- [FastAPI Server Example](../servers/fastapi/README.en.md) - Build your own x402-protected service

---

[← Back to v1 Documentation](../README.en.md) | [View v2 Spec →](../../../x402-v2-specification.md)

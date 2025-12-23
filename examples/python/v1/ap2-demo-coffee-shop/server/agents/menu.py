# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Coffee shop menu, sizes, and bean options with pricing logic."""

from typing import Any

# Base menu prices in micro USDC (1 USDC = 1,000,000 micro USDC)
# Prices are based on Tall size
MENU: dict[str, dict[str, Any]] = {
    "아메리카노": {
        "base_price": 45_000,  # $0.045 (1/100 of $4.50)
        "description": "진한 에스프레소",
        "description_en": "Rich espresso with water",
    },
    "카페라떼": {
        "base_price": 50_000,  # $0.050 (1/100 of $5.00)
        "description": "부드러운 우유와 에스프레소",
        "description_en": "Smooth milk with espresso",
    },
    "카푸치노": {
        "base_price": 55_000,  # $0.055 (1/100 of $5.50)
        "description": "풍성한 거품",
        "description_en": "Rich foam with espresso",
    },
    "바닐라라떼": {
        "base_price": 60_000,  # $0.060 (1/100 of $6.00)
        "description": "달콤한 바닐라 향",
        "description_en": "Sweet vanilla latte",
    },
    "카라멜마끼아또": {
        "base_price": 65_000,  # $0.065 (1/100 of $6.50)
        "description": "달콤한 카라멜 드리즐",
        "description_en": "Sweet caramel drizzle",
    },
    "모카": {
        "base_price": 60_000,  # $0.060 (1/100 of $6.00)
        "description": "초콜릿과 에스프레소의 조화",
        "description_en": "Chocolate and espresso harmony",
    },
}

# Size options with price difference from Tall (base)
SIZES: dict[str, dict[str, Any]] = {
    "Short": {
        "price_diff": -5_000,  # -$0.005 (1/100 of $0.50)
        "volume": "237ml",
        "volume_oz": "8oz",
    },
    "Tall": {
        "price_diff": 0,  # Base price
        "volume": "355ml",
        "volume_oz": "12oz",
    },
    "Grande": {
        "price_diff": 5_000,  # +$0.005 (1/100 of $0.50)
        "volume": "473ml",
        "volume_oz": "16oz",
    },
    "Venti": {
        "price_diff": 10_000,  # +$0.010 (1/100 of $1.00)
        "volume": "591ml",
        "volume_oz": "20oz",
    },
}

# Bean options with price difference
BEANS: dict[str, dict[str, Any]] = {
    "일반": {
        "price_diff": 0,
        "description": "하우스 블렌드",
        "description_en": "House blend",
    },
    "디카페인": {
        "price_diff": 3_000,  # +$0.003 (1/100 of $0.30)
        "description": "카페인 제거 원두",
        "description_en": "Decaffeinated beans",
    },
    "하프디카페인": {
        "price_diff": 3_000,  # +$0.003 (1/100 of $0.30)
        "description": "50% 디카페인 블렌드",
        "description_en": "50% decaf blend",
    },
}

# Default options
DEFAULT_SIZE = "Tall"
DEFAULT_BEAN = "일반"


def calculate_price(drink: str, size: str = DEFAULT_SIZE, bean: str = DEFAULT_BEAN) -> int:
    """
    Calculate the total price for a drink with options.
    
    Args:
        drink: Name of the drink (must be in MENU)
        size: Size option (Short/Tall/Grande/Venti)
        bean: Bean option (일반/디카페인/하프디카페인)
    
    Returns:
        Total price in micro USDC
    
    Raises:
        ValueError: If drink, size, or bean is not valid
    """
    if drink not in MENU:
        raise ValueError(f"Unknown drink: {drink}. Available: {list(MENU.keys())}")
    if size not in SIZES:
        raise ValueError(f"Unknown size: {size}. Available: {list(SIZES.keys())}")
    if bean not in BEANS:
        raise ValueError(f"Unknown bean: {bean}. Available: {list(BEANS.keys())}")
    
    base_price = MENU[drink]["base_price"]
    size_diff = SIZES[size]["price_diff"]
    bean_diff = BEANS[bean]["price_diff"]
    
    return base_price + size_diff + bean_diff


def format_price_usd(price_micro: int) -> str:
    """Format micro USDC price to USD string."""
    return f"${price_micro / 1_000_000:.2f}"


def get_menu_display() -> dict[str, Any]:
    """
    Get formatted menu for display to customers.
    
    Returns:
        Dictionary with menu items, sizes, and bean options
    """
    menu_items = []
    for name, info in MENU.items():
        menu_items.append({
            "name": name,
            "base_price_usd": format_price_usd(info["base_price"]),
            "base_price_micro": info["base_price"],
            "description": info["description"],
        })
    
    size_options = []
    for name, info in SIZES.items():
        diff_str = ""
        if info["price_diff"] > 0:
            diff_str = f"+{format_price_usd(info['price_diff'])}"
        elif info["price_diff"] < 0:
            diff_str = f"-{format_price_usd(abs(info['price_diff']))}"
        else:
            diff_str = "(기준)"
        
        size_options.append({
            "name": name,
            "volume": info["volume"],
            "price_diff": diff_str,
        })
    
    bean_options = []
    for name, info in BEANS.items():
        diff_str = ""
        if info["price_diff"] > 0:
            diff_str = f"+{format_price_usd(info['price_diff'])}"
        else:
            diff_str = "(기본)"
        
        bean_options.append({
            "name": name,
            "description": info["description"],
            "price_diff": diff_str,
        })
    
    return {
        "menu": menu_items,
        "sizes": size_options,
        "beans": bean_options,
        "note": "모든 가격은 Tall 사이즈 기준입니다. All prices are based on Tall size.",
    }


def validate_order(drink: str, size: str, bean: str) -> tuple[bool, str]:
    """
    Validate order parameters.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if drink not in MENU:
        return False, f"'{drink}'은(는) 메뉴에 없습니다. 가능한 메뉴: {', '.join(MENU.keys())}"
    if size not in SIZES:
        return False, f"'{size}'은(는) 올바른 사이즈가 아닙니다. 가능한 사이즈: {', '.join(SIZES.keys())}"
    if bean not in BEANS:
        return False, f"'{bean}'은(는) 올바른 원두 옵션이 아닙니다. 가능한 옵션: {', '.join(BEANS.keys())}"
    return True, ""


def get_order_description(drink: str, size: str, bean: str) -> str:
    """Get a human-readable description of the order."""
    bean_desc = "" if bean == "일반" else f" {bean}"
    return f"{size} {drink}{bean_desc}"


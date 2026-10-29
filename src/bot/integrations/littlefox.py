from __future__ import annotations

from dataclasses import dataclass

import httpx


class LittleFoxError(RuntimeError):
    def __init__(self, code: str, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code


@dataclass(frozen=True, slots=True)
class LittleFoxProduct:
    id: int
    name: str
    price_kopeks: int
    currency: str
    stock: int | None
    stock_unlimited: bool
    available: bool
    category: str | None
    description: str | None
    description_html: str | None


class LittleFoxClient:
    def __init__(self, base_url: str, api_key: str, *, timeout: float = 15.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout

    async def list_products(self, *, page: int = 1, limit: int = 50) -> list[LittleFoxProduct]:
        params = {"page": page, "limit": limit, "lang": "ru", "currency": "RUB"}
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(
                f"{self._base_url}/products",
                params=params,
                headers={"Authorization": f"Bearer {self._api_key}"},
            )
        payload = response.json()
        if response.is_error or not payload.get("ok"):
            error = payload.get("error", {})
            raise LittleFoxError(
                error.get("code", "provider_error"),
                error.get("message", "LittleFox request failed"),
                response.status_code,
            )

        items = payload.get("data", {}).get("items", [])
        return [self._parse_product(item) for item in items]

    @staticmethod
    def _parse_product(item: dict[str, object]) -> LittleFoxProduct:
        category = item.get("category")
        category_name = category.get("name") if isinstance(category, dict) else None
        return LittleFoxProduct(
            id=int(item["id"]),
            name=str(item["name"]),
            price_kopeks=int(item["price_kopeks"]),
            currency=str(item["currency"]),
            stock=int(item["stock"]) if item.get("stock") is not None else None,
            stock_unlimited=bool(item["stock_unlimited"]),
            available=bool(item["available"]),
            category=str(category_name) if category_name is not None else None,
            description=str(item["description"]) if item.get("description") is not None else None,
            description_html=(
                str(item["description_html"])
                if item.get("description_html") is not None
                else None
            ),
        )

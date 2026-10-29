from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Product
from bot.integrations.littlefox import LittleFoxProduct


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert_from_provider(self, item: LittleFoxProduct) -> Product:
        result = await self._session.execute(
            select(Product).where(Product.provider_product_id == item.id)
        )
        product = result.scalar_one_or_none()
        if product is None:
            product = Product(provider_product_id=item.id)
            self._session.add(product)

        product.name = item.name
        product.description = item.description
        product.description_html = item.description_html
        product.price_kopeks = item.price_kopeks
        product.currency = item.currency
        product.stock = item.stock
        product.stock_unlimited = item.stock_unlimited
        product.available = item.available
        product.category = item.category
        await self._session.flush()
        return product

    async def list_available(
        self,
        *,
        search: str | None = None,
        category: str | None = None,
        limit: int = 50,
    ) -> list[Product]:
        statement = select(Product).where(Product.available.is_(True)).order_by(Product.name)
        if search:
            statement = statement.where(Product.name.ilike(f"%{search}%"))
        if category:
            statement = statement.where(Product.category == category)
        statement = statement.limit(limit)
        result = await self._session.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self._session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

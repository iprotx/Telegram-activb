from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Favorite, Product


class FavoriteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_product_ids(self, user_id: int) -> list[int]:
        result = await self._session.execute(
            select(Favorite.product_id).where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc())
        )
        return list(result.scalars().all())

    async def add(self, user_id: int, product_id: int) -> None:
        product = await self._session.get(Product, product_id)
        if product is None:
            raise LookupError("product_not_found")
        existing = await self._session.scalar(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.product_id == product_id,
            )
        )
        if existing is None:
            self._session.add(Favorite(user_id=user_id, product_id=product_id))
            await self._session.flush()

    async def remove(self, user_id: int, product_id: int) -> None:
        await self._session.execute(
            delete(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.product_id == product_id,
            )
        )

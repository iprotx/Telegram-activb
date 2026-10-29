from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_product_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    price_kopeks: Mapped[int] = mapped_column(BigInteger)
    currency: Mapped[str] = mapped_column(String(3))
    stock: Mapped[int | None] = mapped_column(Integer, nullable=True)
    stock_unlimited: Mapped[bool] = mapped_column(Boolean, default=False)
    available: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    synced_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

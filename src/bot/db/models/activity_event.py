from datetime import datetime

from sqlalchemy import ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base


class ActivityEvent(Base):
    __tablename__ = "activity_events"
    __table_args__ = (
        UniqueConstraint("chat_member_id", "telegram_message_id", name="uq_activity_message"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_member_id: Mapped[int] = mapped_column(
        ForeignKey("chat_members.id", ondelete="CASCADE"), index=True
    )
    telegram_message_id: Mapped[int] = mapped_column(Integer)
    xp_awarded: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

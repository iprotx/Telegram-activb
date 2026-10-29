from datetime import datetime

from sqlalchemy import ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base


class ChatMember(Base):
    __tablename__ = "chat_members"
    __table_args__ = (UniqueConstraint("chat_id", "user_id", name="uq_chat_members_chat_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    xp: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    level: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    message_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    last_xp_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

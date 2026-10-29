from bot.db.models import ActivityEvent, Chat, ChatMember, User


def test_activity_models_are_registered_in_metadata() -> None:
    assert {"users", "chats", "chat_members", "activity_events"}.issubset(
        {table.name for table in Chat.metadata.tables.values()}
    )
    assert ChatMember.__tablename__ == "chat_members"
    assert ActivityEvent.__tablename__ == "activity_events"
    assert User.__tablename__ == "users"
    assert Chat.__tablename__ == "chats"

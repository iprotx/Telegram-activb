from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import hmac
import json
from hashlib import sha256
from urllib.parse import parse_qsl


class TelegramAuthError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class TelegramUser:
    user_id: int
    username: str | None
    first_name: str | None
    last_name: str | None


@dataclass(frozen=True, slots=True)
class TelegramInitData:
    user: TelegramUser
    auth_date: datetime


def validate_init_data(
    raw_init_data: str,
    bot_token: str,
    *,
    now: datetime | None = None,
    max_age_seconds: int = 3600,
) -> TelegramInitData:
    if not raw_init_data:
        raise TelegramAuthError("missing_init_data", "Telegram init data is required")

    pairs = parse_qsl(raw_init_data, keep_blank_values=True, strict_parsing=True)
    values = dict(pairs)
    received_hash = values.pop("hash", None)
    if not received_hash:
        raise TelegramAuthError("missing_signature", "Telegram init data signature is missing")

    data_check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(values.items())
    )
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), sha256).digest()
    expected_hash = hmac.new(secret_key, data_check_string.encode(), sha256).hexdigest()
    if not hmac.compare_digest(expected_hash, received_hash):
        raise TelegramAuthError("invalid_signature", "Telegram init data signature is invalid")

    try:
        auth_timestamp = int(values["auth_date"])
    except (KeyError, TypeError, ValueError) as exc:
        raise TelegramAuthError("invalid_auth_date", "Telegram auth_date is invalid") from exc

    current_time = now or datetime.now(UTC)
    age = current_time.timestamp() - auth_timestamp
    if age < -60 or age > max_age_seconds:
        raise TelegramAuthError("expired", "Telegram init data has expired")

    try:
        user_data = json.loads(values["user"])
        user = TelegramUser(
            user_id=int(user_data["id"]),
            username=user_data.get("username"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise TelegramAuthError("invalid_user", "Telegram user data is invalid") from exc

    return TelegramInitData(
        user=user,
        auth_date=datetime.fromtimestamp(auth_timestamp, tz=UTC),
    )

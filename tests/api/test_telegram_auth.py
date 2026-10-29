from datetime import UTC, datetime
import hmac
from hashlib import sha256
from urllib.parse import urlencode

import pytest

from bot.api.auth.telegram import TelegramAuthError, validate_init_data


def make_init_data(
    bot_token: str,
    *,
    auth_date: int,
    user: str = '{"id":123456789,"first_name":"Test","username":"tester"}',
) -> str:
    values = {"auth_date": str(auth_date), "user": user}
    check_string = "\n".join(f"{key}={value}" for key, value in sorted(values.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), sha256).digest()
    digest = hmac.new(secret_key, check_string.encode(), sha256).hexdigest()
    return urlencode({**values, "hash": digest})


def test_validate_init_data_rejects_invalid_signature() -> None:
    raw = make_init_data("123456:TEST", auth_date=int(datetime.now(UTC).timestamp()))
    raw = raw.replace("hash=", "hash=0", 1)

    with pytest.raises(TelegramAuthError) as exc_info:
        validate_init_data(raw, "123456:TEST", now=datetime.now(UTC))

    assert exc_info.value.code == "invalid_signature"


def test_validate_init_data_rejects_expired_data() -> None:
    raw = make_init_data("123456:TEST", auth_date=1)

    with pytest.raises(TelegramAuthError) as exc_info:
        validate_init_data(raw, "123456:TEST", now=datetime.now(UTC))

    assert exc_info.value.code == "expired"


def test_validate_init_data_returns_user() -> None:
    raw = make_init_data("123456:TEST", auth_date=int(datetime.now(UTC).timestamp()))

    result = validate_init_data(raw, "123456:TEST", now=datetime.now(UTC))

    assert result.user.user_id == 123456789
    assert result.user.username == "tester"
    assert result.user.first_name == "Test"


def test_validate_init_data_rejects_missing_user() -> None:
    raw = make_init_data("123456:TEST", auth_date=int(datetime.now(UTC).timestamp()), user="{}")

    with pytest.raises(TelegramAuthError) as exc_info:
        validate_init_data(raw, "123456:TEST", now=datetime.now(UTC))

    assert exc_info.value.code == "invalid_user"

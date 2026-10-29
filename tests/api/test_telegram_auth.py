from datetime import UTC, datetime
from hashlib import sha256
import hmac
from urllib.parse import urlencode

import pytest

from bot.api.auth.telegram import TelegramAuthError, validate_init_data


def make_init_data(bot_token: str, *, auth_date: int) -> str:
    values = {
        "auth_date": str(auth_date),
        "user": '{"id":123456789,"first_name":"Test","username":"tester"}',
    }
    check_string = "\n".join(f"{key}={value}" for key, value in sorted(values.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), sha256).digest()
    digest = hmac.new(secret_key, check_string.encode(), sha256).hexdigest()
    return urlencode({**values, "hash": digest})


@pytest.mark.parametrize(
    "mutator, expected",
    [
        (lambda value: value.replace("hash=", "hash=0"), "invalid_signature"),
        (lambda value: value.replace("auth_date=", "auth_date=0", 1), "expired"),
    ],
)
def test_validate_init_data_rejects_invalid_or_expired_data(mutator, expected: str) -> None:
    raw = make_init_data("123456:TEST", auth_date=int(datetime.now(UTC).timestamp()))
    if expected == "expired":
        raw = make_init_data("123456:TEST", auth_date=1)

    with pytest.raises(TelegramAuthError) as exc_info:
        validate_init_data(mutator(raw), "123456:TEST", now=datetime.now(UTC))

    assert exc_info.value.code == expected


def test_validate_init_data_returns_user() -> None:
    raw = make_init_data("123456:TEST", auth_date=int(datetime.now(UTC).timestamp()))

    result = validate_init_data(raw, "123456:TEST", now=datetime.now(UTC))

    assert result.user_id == 123456789
    assert result.username == "tester"
    assert result.first_name == "Test"


def test_validate_init_data_rejects_missing_user() -> None:
    raw = make_init_data("123456:TEST", auth_date=int(datetime.now(UTC).timestamp())).replace(
        "%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22username%22%3A%22tester%22%7D",
        "%7B%7D",
    )

    with pytest.raises(TelegramAuthError) as exc_info:
        validate_init_data(raw, "123456:TEST", now=datetime.now(UTC))

    assert exc_info.value.code == "invalid_user"

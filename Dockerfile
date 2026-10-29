FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --uid 10001 bot

COPY pyproject.toml .
COPY src ./src
COPY alembic.ini .
COPY alembic ./alembic

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir . \
    && chown -R bot:bot /app

USER bot

CMD ["sh", "-c", "alembic upgrade head && exec python -m bot.main"]

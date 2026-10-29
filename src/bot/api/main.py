import uvicorn

from bot.api.app import create_api_app
from bot.config import Settings
from bot.db.session import create_database


def main() -> None:
    settings = Settings()
    database = create_database(settings)
    app = create_api_app(settings, database.session_factory)
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)


if __name__ == "__main__":
    main()

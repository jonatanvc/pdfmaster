from dependency_injector import containers, providers
from requests import Session
from pdf_bot.database import DatabaseClient
from pdf_bot.settings import Settings

class Clients(containers.DeclarativeContainer):
    _settings = providers.Configuration(pydantic_settings=[Settings()])

    _session = Session()
    _session.hooks = {  # noqa: RUF012
        "response": lambda r, *_args, **_kwargs: r.raise_for_status()  # pragma: no cover
    }

    api = providers.Object(_session)
    database = providers.Singleton(DatabaseClient, database_url=_settings.database_url)


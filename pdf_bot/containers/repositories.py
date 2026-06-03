from dependency_injector import containers, providers
from pdf_bot.account import AccountRepository
from pdf_bot.analytics import AnalyticsRepository
from pdf_bot.language import LanguageRepository
from pdf_bot.settings import Settings
from pdf_bot.text import TextRepository

class Repositories(containers.DeclarativeContainer):
    _settings = providers.Configuration(pydantic_settings=[Settings()])
    clients = providers.DependenciesContainer()

    account = providers.Singleton(AccountRepository, db_client=clients.database)
    analytics = providers.Singleton(AnalyticsRepository, api_client=clients.api, settings=_settings)
    language = providers.Singleton(LanguageRepository, db_client=clients.database)
    text = providers.Singleton(
        TextRepository,
        api_client=clients.api,
        google_fonts_token=_settings.google_fonts_token,
    )


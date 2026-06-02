from dependency_injector import containers, providers
from .core import Core
from .clients import Clients
from .repositories import Repositories
from .services import Services
from .processors import Processors
from .handlers import Handlers

class Application(containers.DeclarativeContainer):
    core = providers.Container(Core)
    clients = providers.Container(Clients)
    repositories = providers.Container(Repositories, clients=clients)
    services = providers.Container(Services, core=core, clients=clients, repositories=repositories)
    processors = providers.Container(Processors, services=services)
    handlers = providers.Container(Handlers, services=services)

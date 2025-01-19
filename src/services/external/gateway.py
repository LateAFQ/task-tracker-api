from src.common.interfaces.gateway import BaseGateway
from src.core.settings import Settings
from src.database.gateway import DBGateway


class ExternalServiceGateway(BaseGateway):
    __slots__ = ("settings", "database")

    def __init__(self, settings: Settings, database: DBGateway) -> None:
        self.settings = settings
        self.database = database
        super().__init__(database)

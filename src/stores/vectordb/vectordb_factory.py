
from controllers.base_controller import base_controller
from .providers.qdrantprovider import QdrantProvider 


class VectorDBFactory:
    def __init__(self,config: dict):
        self.config = config
        self.db_path=base_controller().get_database_path()
    def create(self,provider_name: str):
        if provider_name == "qdrant":
            return QdrantProvider(db_path=self.db_path,distance_method=self.config.VECTOR_DB_DISTANCE_METHOD)
        else:
            raise ValueError(f"Unsupported VectorDB provider:{provider_name}")
            
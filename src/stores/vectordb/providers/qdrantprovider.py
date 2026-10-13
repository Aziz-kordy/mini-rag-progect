from ..vectordb_interface import VectorDBInterface
from qdrant_client import QdrantClient,models
import logging
from models.db_schemes.datachunk import RetrivedDocument

class QdrantProvider(VectorDBInterface):
    def __init__(self,db_path:str,distance_method:str):
        self.db_path = db_path
        self.distance_method = distance_method
        self.client = None
        self.logger = logging.getLogger(__name__)
        
        if distance_method == "cosine":
            self.distance_method = models.Distance.COSINE
        elif distance_method == "dot":
            self.distance_method = models.Distance.DOT
            
    def connect(self):
        self.client = QdrantClient(path=self.db_path)
        self.logger.info(f"Connected to Qdrant at {self.db_path}")   
        
    def disconnect(self):
        pass
    
    def is_collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_collections(self) -> list:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str):
        if not self.is_collection_exists(collection_name):
            self.logger.warning(f"Collection {collection_name} does not exist.")
            return  None
        return self.client.delete_collection(collection_name=collection_name)
    
    def create_collection(self, collection_name: str, embedding_size: int=1536, metadata: dict ={},do_reset: bool = False):
        if self.is_collection_exists(collection_name=collection_name):
            if do_reset:
                self.delete_collection(collection_name)
                
            else: 
              self.logger.warning(f"Collection {collection_name} already exists.")
                
              return False
           
            
        
        self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=embedding_size, distance=self.distance_method),
            ) 
        return True
            
        
        
            
            
    def  insert_one_vector(self, collection_name: str, vector: list, text: str, metadata: dict = {},record_id: str = None):
        if not self.is_collection_exists(collection_name):
            self.logger.error(f"Collection {collection_name} does not exist.")
            return None
        
        _=self.client.upsert(
            collection_name=collection_name,
            records=[models.Record(id=record_id,vector=vector,payload={"text": text, "metadata": metadata})]
            
        )
        self.logger.info(f"Inserted vector into collection {collection_name}.")    
        
    def insert_many_vectors(self, record_ids: list, collection_name: str, vectors: list, texts: list, metadatas: list, batch_size: int = 100):
        
        if record_ids is None:
           record_ids = list(range(len(texts)))
        if metadatas is None:
            metadatas=[{}]*len(texts)    
        if not self.is_collection_exists(collection_name):
                    self.logger.error(f"Collection {collection_name} does not exist.")
                    return None    
                
        for i in range(0,len(vectors),batch_size):
            batch_end=i+batch_size
            batch_vectors=vectors[i:batch_end]
            batch_texts=texts[i:batch_end]
            batch_metadatas=metadatas[i:batch_end]
            batch_record_ids=record_ids[i:batch_end]
            
            
            records=[models.Record(id=batch_record_ids[x],vector=batch_vectors[x],payload={"text": batch_texts[x], "metadata": batch_metadatas[x]}) for x in range(len(batch_vectors))]
            
            _=self.client.upsert(
                collection_name=collection_name,
                points=records
            )
            
        return True
    
    def search_by_vector(self, collection_name: str, vector: list, limit: int = 10):
        result= self.client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit
        ) 
        results=result.points  
        if not results :
            return None    
        
        return [ RetrivedDocument(** {"score":result.score , "text":result.payload["text"],})  for result in results]                  
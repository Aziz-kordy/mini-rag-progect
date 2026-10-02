

from .basedatamodel import BaseDataModel
from .db_schemes.datachunk import datachunk
from bson import ObjectId
from pymongo import InsertOne
class chunkmodel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection=self.db_client["chunks"]
    
    @classmethod
    async def creat_instance(cls,db_client:object):
          instance=cls(db_client)
          await instance.init_collection()
          return instance
        
        
    async def init_collection(self):
            all_collections=await self.db_client.list_collection_names()
            if "projects" not in all_collections:
                 self.collection=self.db_client["chunks"]
                 
                 indexes=datachunk.get_index()
            
                 for index in indexes :
                   await self.collection.create_index(keys=index["keys"],name=index["name"],unique=index["unique"])   
        
        
        # creat chunk
    async def creat_chunk(self,chunk:datachunk):
        result=await self.collection.insert_one(chunk.dict(by_alias=True,exclude_unset=True))
        return result.insert_id
    
    # get chunk by chunk_id
    async def get_chunk(self,chunk_id:str):
        
        result=await self.collection.find_one({"_id":ObjectId(chunk_id)}) 
        if result is None:
             return None
        return datachunk(**result)
    
    
    # insert all chunks 
    async def insert_all_chunks(self,chunks:list,batch_size:int=100):
        for i in range(0,len(chunks),batch_size):
            batch=chunks[i:i+batch_size]
            operations=[ InsertOne(chunk.dict(by_alias=True,exclude_unset=True))
                        for chunk in batch ]
     
            await self.collection.bulk_write(operations)  
            
        return len(chunks)        
         
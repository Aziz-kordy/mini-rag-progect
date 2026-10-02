

from pydantic import BaseModel, Field
from typing import Optional,Text
from bson import ObjectId
from typing import Dict, Any
class datachunk(BaseModel):
    id: Optional[ObjectId]= Field(default=None, alias="_id")
    chunk_text:str
    chunk_metadata:Dict
    chunk_project_id:[ObjectId]
    class Config:
            
            arbitrary_types_allowed = True
            
            
    @classmethod
    def get_index(cls):
            return[
                {
                    "keys":[("chunk_project_id",1)],
                    "name":"chunk_project_id_index_1",
                    "unique":False
                }
                
            ]    
                    
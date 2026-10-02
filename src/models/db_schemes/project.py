from enum import unique

from models.db_schemes import project
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId]= Field(default=None, alias="_id")
    project_id: str = Field(..., min_length=1, max_length=100)
    tototo:str="khkg"
    
    class Config:
        
        arbitrary_types_allowed = True
        
    @classmethod
    def get_index(cls):
        return[
            {
                "keys":[("project_id",1)],
                "name":"project_id_index_1",
                "unique":True
            }
            
        ]    
        
    
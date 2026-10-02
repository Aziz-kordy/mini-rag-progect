from email.policy import default

from models.db_schemes import project
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: Optional[ObjectId]= Field(default=None, alias="_id")
    asset_project_id:ObjectId
    asset_type:str
    asset_name:str
    asset_size:int=Field(ge=0,default=None)
    asset_pushed_date:datetime=Field(default_factory=datetime.utcnow)
    class Config:
            
            arbitrary_types_allowed = True
            
    @classmethod
    def get_index(cls):
            return[
                {
                    "keys":[("asset_project_id",1),("asset_name",1)],
                    "name":"asset_project_id_name_index_1",
                    "unique":False
                }
                
            ]    
                    
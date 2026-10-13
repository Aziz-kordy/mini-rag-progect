from pydantic import BaseModel
from typing import Optional
class pushrequest(BaseModel):
    do_reset: Optional[int] = 0
    
class SearchRequast(BaseModel):
    text:str    
    limit:Optional[int]=10
from .basedatamodel import BaseDataModel
from .db_schemes.asset import Asset
from bson import ObjectId

class assetmodel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client)
        self.collection=self.db_client["assets"]
        
    
    @classmethod
    async def create_instance(cls,db_client:object):
      instance=cls(db_client)
      await instance.init_collection()
      return instance
    
    
    async def init_collection(self):
        all_collections=await self.db_client.list_collection_names()
        if "assets" not in all_collections:
             self.collection=self.db_client["assets"]
             
             indexes=Asset.get_index()        
            
             for index in indexes :
                        await self.collection.create_index(keys=index["keys"],name=index["name"],unique=index["unique"])   
                        
        
    async def create_asset(self, asset:Asset):
            
            result=await self.collection.insert_one(asset.dict(by_alias=True,exclude_unset=True))
            asset.id=result.inserted_id
            return asset
   
    async def get_all_project_assets(self,asset_project_id:str,asset_type:str):
        all_assets=await self.collection.find({"asset_project_id":ObjectId(asset_project_id),"asset_type":asset_type}).to_list(length=None)
        return all_assets
        
                            
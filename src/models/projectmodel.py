from .basedatamodel import BaseDataModel
from .db_schemes.project import Project



class projectmodel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client)
        self.collection=self.db_client["projects"]
        
        
    @classmethod
    async def creat_instance(cls,db_client:object):
      instance=cls(db_client)
      await instance.init_collection()
      return instance
    
    
    async def init_collection(self):
        all_collections=await self.db_client.list_collection_names()
        if "projects" not in all_collections:
             self.collection=self.db_client["projects"]
             
        indexes=Project.get_index()
        
        for index in indexes :
            await self.collection.create_index(keys=index["keys"],name=index["name"],unique=index["unique"])   

                
        
    async def creat_project(self, project:Project):
        
        result=await self.collection.insert_one(project.dict(by_alias=True,exclude_unset=True))
        return result.inserted_id
    
    async def get_or_create_project(self,project_id:str):
        record=await self.collection.find_one({"project_id":project_id})
        
        if record is None:
            project=Project(project_id=project_id)
            project=await self.creat_project(project)
            return project
        return Project(**record)
    
    async def get_all_projects(self,page:int=1,page_size:int=10):
        
        
        skip=page_size*(page-1)
        total_records=await self.collection.count_documents({})
        total_pages=total_records//page_size
        if total_records%page_size>0:
            total_pages+=1
        
        
        cursor=self.collection.find().skip(skip).limit(page_size)
        projects=[]
        async for record in cursor:
            projects.append(Project(**record))
            
        return projects,total_records,total_pages    
                            
                            
       
            
        
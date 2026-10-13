







from fastapi import APIRouter, Depends,UploadFile,Request
from helpers.config import get_settings,Settings
from controllers import data_controller,project_controller
from models.db_schemes import datachunk
from models.db_schemes import asset
from routes import data
from .schemes.data import processrequest
import aiofiles
import os
from controllers.processcontroller import process_controller
from models.datachunkmodel import chunkmodel
from models.projectmodel import projectmodel
from models.db_schemes.datachunk import datachunk
from models.assetmodel import assetmodel
from models.db_schemes.asset import Asset
from models.db_schemes.project import Project
data_router = APIRouter()
@data_router.post("/upload/{project_id}")
async def upload_file(request:Request,project_id:str,file: UploadFile, app_settings = Depends(get_settings)):
    
    is_valid = data_controller().validate_file(file=file)
    if not is_valid :
      return {"error": "الملف غير صالح. يرجى التحقق من نوع الملف وحجمه."} 
    

    file_path,file_id = data_controller().generate_new_file_path(file.filename,project_id=project_id)


    project_model=await projectmodel.creat_instance(db_client=request.app.db_client)
    project=await project_model.get_or_create_project(project_id=project_id)


    

    async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await file.read(1024000) :  # Read the file in chunks
            await f.write(chunk)
    
    
      
    asset_model=await assetmodel.create_instance(db_client=request.app.db_client)    
    
    asset_resource=Asset(asset_project_id=project.id,
                         asset_type="files",
                         asset_name=file_id,
                         asset_size=os.path.getsize(file_path)
                         )
    asset_record=await asset_model.create_asset(asset=asset_resource)
    
    return {"asset_id":str(asset_record.id),
            "file_id": file_id}
        
        
        
        
         
        # return {"message": f"File '{file.filename}' uploaded successfully to project_id '{str(project)}'." ,
        #         "file_id": file_id 
        #         }      
        
    
    
@data_router.post("/process/{project_id}")
async def process_endpoint(requesttt:Request,request:processrequest, project_id:str):
    file_id=request.file_id
    Chunk_size=request.chunk_size
    overlap_size=request.overlap_size
    
    
     
    
    
    
     
    project_model=await projectmodel.creat_instance(db_client=requesttt.app.db_client)
    project=await project_model.get_or_create_project(project_id=project_id)
    
    project_files_ids=[]
    if file_id:
        project_files_ids=[file_id]
    else:
        asset_model=await assetmodel.create_instance(db_client=requesttt.app.db_client)
        all_project_assets=await asset_model.get_all_project_assets(asset_project_id=str(project.id),asset_type="files")
        project_files_ids=[asset["asset_name"] for asset in all_project_assets]
        
        
        
    no_records=0
    no_files=0     
    for file_id in project_files_ids:  
        
        file_content=process_controller(project_id=project_id).get_file_content(file_id=file_id)
            
        file_chunks=process_controller(project_id=project_id).get_file_process(file_content=file_content,file_id=file_id,
                                                                                chunk_size=Chunk_size,overlap_size=overlap_size)    
           
        if file_chunks is  None or len(file_chunks)==0:
                return   {"message": f'{len(file_chunks)}'}
         
                                                                                
        file_chunks_record = [
        datachunk(
            chunk_text=chunk.page_content,
            
            chunk_metadata=chunk.metadata,
            chunk_project_id=project.id)
                
        for chunk in file_chunks]
                            
            
        chunk_model=await chunkmodel.creat_instance(db_client=requesttt.app.db_client)
        
        no_records+=await chunk_model.insert_all_chunks(chunks=file_chunks_record)
        no_files+=1
    return {"chunk_no":no_records}
                        
        
               
            

    
    


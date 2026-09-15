

from fastapi import APIRouter, Depends,UploadFile
from helpers.config import get_settings,Settings
from controllers import data_controller,project_controller
from routes import data

import aiofiles
import os

data_router = APIRouter()
@data_router.post("/upload/{project_id}")
async def upload_file(project_id:str,file: UploadFile, app_settings = Depends(get_settings)):
    
    is_valid = data_controller().validate_file(file=file)
    if not is_valid :
      return {"error": "الملف غير صالح. يرجى التحقق من نوع الملف وحجمه."} 
    project_path = project_controller().get_project_path(project_id=project_id)

    file_path = os.path.join(project_path, file.filename)

    async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await file.read(1024000) :  # Read the file in chunks
            await f.write(chunk)
        
        return {"message": f"File '{file.filename}' uploaded successfully to project '{project_id}'." }      
        
        
        

    
    


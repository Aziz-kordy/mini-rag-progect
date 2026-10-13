from email.policy import default

from controllers import nlp_controller
from fastapi import APIRouter, Depends, UploadFile, Request
from helpers.config import get_settings, Settings
from models import datachunkmodel
from routes.schemes.nlp import pushrequest,SearchRequast
from models.projectmodel import projectmodel
from models.datachunkmodel import chunkmodel
from controllers.nlp_controller import NLPController
import json
nlp_router = APIRouter()

@nlp_router.post("/push/index/{project_id}")
async def push_index(request: Request, project_id: str, push_req: pushrequest):
    
    project_model=await projectmodel.creat_instance(db_client=request.app.db_client)  
    project=await project_model.get_or_create_project(project_id=project_id)
    
    chunk_model=await chunkmodel.creat_instance(db_client=request.app.db_client)
    nlp_controller=NLPController(template_parser=request.app.template_parser,vectordb_client=request.app.vectordb_client,embedding_client=request.app.embedding_client,generation_client=request.app.generation_client)    
    has_record=True
    page_no=1
    idx=0
   
    
    while has_record:
        
       page_chunks=await chunk_model.get_all_chunks(project_id=project.id,page=page_no)
       
        
       
       
        

        # مفيش chunks تاني
       if not page_chunks or len(page_chunks)==0:
           has_record=False
           return "loop is doneeeeeeeeeeeeee"
       chunk_ids=list(range(idx,idx + len(page_chunks)))
       idx+=len(page_chunks)
           
        
            
       is_inserted=nlp_controller.index_into_vectordb(project=project,chunks=page_chunks,chunk_ids=chunk_ids,do_reset=push_req)
       if len(page_chunks):
            page_no+=1       
       
    print("page_no",page_no)  
    print("chunk_no",len(page_chunks))
           
    return True            
    
    
@nlp_router.get("/info/index/{project_id}")
async def get_collection_info(request: Request, project_id: str):
    
  
    project_model=await projectmodel.creat_instance(db_client=request.app.db_client)  
    project=await project_model.get_or_create_project(project_id=project_id)  
    nlp_controller=NLPController(template_parser=request.app.template_parser,vectordb_client=request.app.vectordb_client,embedding_client=request.app.embedding_client,generation_client=request.app.generation_client)
    info=nlp_controller.get_vectordb_collection_info(project=project)
    return json.loads(json.dumps(info,default=lambda x:x.__dict__))

    
@nlp_router.post("/search/index/{project_id}")

async def search_by_vector(request:Request,project_id:str,search_req: SearchRequast):
    
        project_model=await projectmodel.creat_instance(db_client=request.app.db_client)  
        project=await project_model.get_or_create_project(project_id=project_id)  
        nlp_controller=NLPController(template_parser=request.app.template_parser,vectordb_client=request.app.vectordb_client,embedding_client=request.app.embedding_client,generation_client=request.app.generation_client)       
        results=nlp_controller.search_vectordb_collection(project=project,text=search_req.text,limit=search_req.limit)
        return results



@nlp_router.post("/answer/index/{project_id}")
   
async def answer(request:Request,project_id:str,search_req: SearchRequast):   
     project_model=await projectmodel.creat_instance(db_client=request.app.db_client)  
     project=await project_model.get_or_create_project(project_id=project_id)  
     nlp_controller=NLPController(template_parser=request.app.template_parser,vectordb_client=request.app.vectordb_client,embedding_client=request.app.embedding_client,generation_client=request.app.generation_client)
     answer,full_prompt,chat_history=nlp_controller.answer_rag_question(project=project,query=search_req.text,limit=search_req.limit)
     
     return (f"answer is:{answer} , full_prompt is:{full_prompt} ,chat_history is:{chat_history}")
    
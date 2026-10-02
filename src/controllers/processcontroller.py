





from controllers import data_controller

from .base_controller import base_controller
from helpers.config import get_settings
import os
from .project_controller import project_controller
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import CSVLoader
from .data_controller import data_controller
from langchain_text_splitters import RecursiveCharacterTextSplitter 

from routes.schemes.data import processrequest


class process_controller(base_controller):
    def __init__(self,project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=project_controller().get_project_path(project_id)
        
    def get_fil_extension(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    
    def get_loader(self,file_id:str):
        file_path=os.path.join(self.project_path,file_id)
        file_extension=self.get_fil_extension(file_id=file_id)
        if file_extension==".csv":
            return CSVLoader(file_path,encoding="utf-8")
        if file_extension in [".pdf",".PDF"]:
            return PyMuPDFLoader(file_path)  
        else:
            raise Exception(f"File extension {file_extension} not supported")
        
    def get_file_content(self,file_id:str):
       
        loader=self.get_loader(file_id=file_id)
        return loader.load()    
        

       
    
    def get_file_process(self,file_content:list,file_id:str,chunk_size:int,overlap_size:int):
        
        
       
     
        text_spliter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=overlap_size)
        
        file_content_text=[doc.page_content for doc in file_content]
        metadata_content=[doc.metadata for doc in file_content]
        
        chunks=text_spliter.create_documents(file_content_text,metadata_content)
        
        
        
        
        
        return chunks
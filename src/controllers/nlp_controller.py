

import json
import sre_constants

from models.db_schemes.datachunk import datachunk

from .base_controller import base_controller
from models.db_schemes.project import Project
from helpers.config import get_settings,Settings
app_settings=get_settings()

class NLPController(base_controller):
    def __init__(self,vectordb_client,embedding_client,generation_client,template_parser):
        super().__init__()
        
        
        self.vectordb_client=vectordb_client
        self.embedding_client=embedding_client
        self.generation_client=generation_client
        self.template_parser=template_parser
    
    def create_collection_name(self,project_id:str):
        return f"collection_{project_id}"
    
    def reset_collection(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    
    def get_vectordb_collection_info(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.get_collection_info(collection_name=collection_name)
    
    def index_into_vectordb(   self,project,chunk_ids: list,chunks: list,do_reset: bool = False  ):
        
        
        
        
  
 

        collection_name = self.create_collection_name(
            project_id=project.project_id
        )

        texts = [
            chunk.chunk_text
            for chunk in chunks
        ]

        vectors = self.embedding_client.embed_text(
            texts=texts,
            document_type="document")
                       

        if vectors is None:
            return False

        metadatas = [
            chunk.chunk_metadata
            for chunk in chunks
        ]

        self.vectordb_client.create_collection(
            collection_name=collection_name,
            do_reset=do_reset,
            embedding_size=self.embedding_client.embedding_size
        )

        self.vectordb_client.insert_many_vectors(
            collection_name=collection_name,
            vectors=vectors,
            texts=texts,
            metadatas=metadatas,
            record_ids=chunk_ids
        )

       

        return True
    
    
    
    def search_vectordb_collection(self,project:Project,text:str,limit:int=10):
        collection_name = self.create_collection_name(
                    project_id=project.project_id
                )
        
        vector=self.embedding_client.embed_text(texts=[text],document_type="query")[0]
        result=self.vectordb_client.search_by_vector(collection_name= collection_name, vector=vector, limit=limit)
        
        return result
    
    
    def answer_rag_question(self,project:Project,query:str,limit:int=10):
        
        retrived_documents=self.search_vectordb_collection(project=project,text=query,limit=limit)
        
        
        system_prompt=self.template_parser.get("rag","system_prompt")
        
        document_prompts=[self.template_parser.get("rag","document_prompt",{"doc_num":idx,  "chunk_text":doc.text})
                          for idx,doc in enumerate(retrived_documents,start=1)]
        
        footer_prompt=self.template_parser.get("rag","footer_prompt")
        
        
        
        if not system_prompt or not footer_prompt:
          raise ValueError("Required RAG template is missing")
      
        if any(prompt is None for prompt in document_prompts):
            raise ValueError("Document prompt template is missing")
                
        chat_history=[self.generation_client.construct_prompt(prompt=system_prompt,role="system"),
                      self.generation_client.construct_prompt(prompt=query,role="user")] #دي الي فيها ال system_prompt
        
        full_prompt="\n\n".join(document_prompts+[footer_prompt]) #دي الي فيها النصوص الي مشابهه للسؤال والفوتر كمان الي هو اخر امر 
        
        answer=self.generation_client.generate_text(prompt=full_prompt,chat_history=chat_history)
        
        return answer,full_prompt,chat_history
        
        
    
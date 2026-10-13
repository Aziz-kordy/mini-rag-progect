from pydoc import doc

from ..LLminterface import LLMinterface
import cohere
import logging

class CohereProvider(LLMinterface):
    def __init__(self,api_key:str,default_input_max_characters:int,default_output_max_tokens:int,default_temperature:float=0.1):
        self.api_key = api_key
        
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None
        
        self.logger=logging.getLogger(__name__)
        
        self.client = cohere.Client(api_key=self.api_key)
        
    def set_generation_model_id(self, model_id: str):
            self.generation_model_id = model_id
            
    def set_embedding_model_id(self, model_id: str,model_size:int):
            self.embedding_model_id = model_id  
            self.embedding_size=model_size  
    def construct_prompt(self, prompt:str, role:str):
            return {"role":role, "text":prompt}
        
    def generate_text(self,prompt:str,max_output_tokens:int=1024,temperature:float=0.2,chat_history:list=[]):
           if self.generation_model_id is None:
                self.logger.error("Generation model ID is not set.")
                raise ValueError("Generation model ID is not set.")
           if self.client is None:
                self.logger.error("COHERE client is not initialized.")
                raise ValueError("COHERE client is not initialized.")
           if not self.default_output_max_tokens:
               max_output_tokens = self.default_output_max_tokens
           if not self.default_temperature:
               temperature = self.default_temperature    
               
               
           
           
           response=self.client.chat(
                model=self.generation_model_id,
                message=prompt,
                max_tokens=max_output_tokens,
                temperature=temperature,
                chat_history=chat_history
            )
           
           if not response or not response.text or len(response.text) == 0:
                self.logger.error("No response received from COHERE API.")
                raise ValueError("No response received from COHERE API.")
           return response.text   
       
            
    def embed_text(self, texts:str , document_type: str):
                    if self.embedding_model_id is None:
                            self.logger.error("Embedding model ID is not set.")
                            raise ValueError("Embedding model ID is not set.")
                    if self.client is None:
                            self.logger.error("COHERE client is not initialized.")
                            raise ValueError("COHERE client is not initialized.")
                        
                        
                    input_type=None    
                    if document_type == "query":
                        input_type="search_query"
                    elif document_type == "document":
                        input_type="search_document"
                      
                            
                        
                    response = self.client.embed(
                            model=self.embedding_model_id,
                            texts=texts,
                            embedding_types=["float"],
                            input_type=input_type
                            )
                        
                    if not response or not response.embeddings.float or len(response.embeddings.float) == 0:
                            self.logger.error("No embedding received from COHERE API.")
                            raise ValueError("No embedding received from COHERE API.")
                    
                    return response.embeddings.float

          
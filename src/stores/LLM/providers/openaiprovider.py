from ..LLminterface import LLMinterface

from openai import OpenAI
import logging

class OpenAIProvider(LLMinterface):
    def __init__(self,api_key:str,api_url:str,default_input_max_characters:int,default_output_max_tokens:int,default_temperature:float=0.1):
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None
        
        self.logger=logging.getLogger(__name__)
        
        self.client = OpenAI(api_key=self.api_key, api_url=self.api_url)
        
        def set_generation_model_id(self, model_id: str):
            self.generation_model_id = model_id
            
        def set_embedding_model_id(self, model_id: str,model_size:int):
            self.embedding_model_id = model_id  
            self.embeddin_model_size=model_size  
        def construct_prompt(self, prompt:str, role:str):
            return {"role":role, "content":prompt}
        
        def generate_text(self,prompt:str,max_output_tokens:int,temperature:float,chat_history:list=[]):
           if self.generation_model_id is None:
                self.logger.error("Generation model ID is not set.")
                raise ValueError("Generation model ID is not set.")
           if self.client is None:
                self.logger.error("OpenAI client is not initialized.")
                raise ValueError("OpenAI client is not initialized.")
           if not self.max_output_tokens:
               max_output_tokens = self.default_output_max_tokens
           if not self.temperature:
               temperature = self.default_temperature    
               
               
           chat_history.append(self.construct_prompt(prompt, "user"))
           
           response=self.client.chat.complimetions.create(
                model=self.generation_model_id,
                messages=chat_history,
                max_tokens=max_output_tokens,
                temperature=temperature
            )
           
           if not response or not response.choices or len(response.choices) == 0:
                self.logger.error("No response received from OpenAI API.")
                
           return response.choices[0].message.content    
       
       
    
        def embed_text(self, text: str, document_type: str):
            if self.embedding_model_id is None:
                     self.logger.error("Embedding model ID is not set.")
                     raise ValueError("Embedding model ID is not set.")
            if self.client is None:
                     self.logger.error("OpenAI client is not initialized.")
                     raise ValueError("OpenAI client is not initialized.")
                  
            response = self.client.embeddings.create(
                     model=self.embedding_model_id,
                     input=text
                    )
                  
            if not response or not response.data or len(response.data) == 0:
                     self.logger.error("No embedding received from OpenAI API.")
                     
            return response.data[0].embedding   
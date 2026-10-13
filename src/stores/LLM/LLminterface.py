from abc import ABC, abstractmethod

class LLMinterface(ABC):
    @abstractmethod
    def set_generation_model_id(self, model_id: str) :
        pass
    
    @abstractmethod
    def set_embedding_model_id(self, model_id: str) :
        pass
    
    @abstractmethod
    def generate_text(self,prompt:str,max_output_tokens:int,temperature:float,chat_history:list=[]):
        pass
    
    @abstractmethod
    def embed_text(self,text:str,document_type:str) :
        pass
    
    @abstractmethod
    def construct_prompt(self, prompt:str, role:str):
        pass
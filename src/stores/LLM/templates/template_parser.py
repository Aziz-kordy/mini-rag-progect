import os
from typing import Self


class TemplateParser():
    def __init__(self,language:str=None,default_language:str="english"):
        
        self.default_language=default_language
        self.current_path=os.path.dirname(os.path.abspath(__file__))
        self.language=None
        self.target_language=self.set_language(language=language)
        
    def set_language(self,language:str):
        
        language = language or self.default_language
        if not language:
            self.language=self.default_language
            
        language_path=os.path.join(self.current_path,"locales",language)
        
        if os.path.exists(language_path):
            self.language=language
            
        else:
            self.language=self.default_language   
            
        return self.language      
            
    def get (self,group:str,key:str,vars:dict={}):
        
        
        group_path=os.path.join(self.current_path,"locales",f"{self.target_language}",f"{group}.py")  
        
        print("TEMPLATE PATH:", group_path)
        print("FILE EXISTS:", os.path.exists(group_path))  
        
        if not group or not key:
                    return None
                      
        if not os.path.exists(group_path):
            return None
        module=__import__(f"stores.LLM.templates.locales.{self.target_language}.{group}",fromlist=[group]) 
        key_attribute=getattr(module, key)
        return key_attribute.substitute(vars)
    
    
        
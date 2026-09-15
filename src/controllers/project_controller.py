from .base_controller import base_controller
from helpers.config import get_settings
import os


class project_controller(base_controller):
    def __init__(self):
        super().__init__()
    
    def get_project_path(self, project_id:str):
        project_path=os.path.join(self.files_dir,project_id)
        
        
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        return project_path
    
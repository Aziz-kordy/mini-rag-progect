from operator import ne
from .project_controller import project_controller
from .base_controller import base_controller
import os
class data_controller(base_controller):
    def __init__(self):
        super().__init__()
        
    def validate_file(self,file):
        # Implement your file validation logic here
        # For example, check file type, size, etc.
        if not file:
            return ("No file provided")
        if file.content_type not in self.app_settings.valid_file_types:
            return ("Invalid file type. Only the allowed types are permitted.")
        return True,"الملف ميه الميه"
        
    def generate_new_file_path(self,filename,project_id):
        random_file_name=self.generate_random_string()
        new_file_name=f"{random_file_name}_{filename}"
        new_file_path= os.path.join(project_controller().get_project_path(project_id),new_file_name)
        
        while os.path.exists(new_file_path):
            random_string=self.generate_random_string()
            new_file_name=f"{random_string}_{filename}"
            new_file_path= os.path.join(project_controller().get_project_path(project_id),new_file_name)
           
        return new_file_path,new_file_name
       
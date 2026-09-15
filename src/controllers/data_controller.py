from .base_controller import base_controller

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
        
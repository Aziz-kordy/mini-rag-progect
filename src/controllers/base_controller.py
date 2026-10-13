

from helpers.config import get_settings
import os
import random
import string


app_settings=get_settings()
class base_controller:
    
    def __init__ (self):
        self.app_settings=get_settings()
        self.base_dir=os.path.dirname(os.path.dirname(__file__))
        self.files_dir=os.path.join(self.base_dir, "assets/files")
        
    def get_database_path(self):
        self.db_dir=os.path.join(self.base_dir, "assets/data_bases")
        database_path=os.path.join(self.db_dir, self.app_settings.VECTOR_DB_NAME)
        if not os.path.exists(database_path):
            os.makedirs(database_path)
        return database_path    
        
    def generate_random_string(self, length: int = 5):
     """Generate a random string of fixed length."""
     letters = string.ascii_lowercase + string.digits
     return ''.join(random.choices(letters, k=length))
        
        
        
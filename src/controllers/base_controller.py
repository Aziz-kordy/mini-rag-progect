

from helpers.config import get_settings
import os
import random
import string

class base_controller:
    
    def __init__ (self):
        self.app_settings=get_settings()
        self.base_dir=os.path.dirname(os.path.dirname(__file__))
        self.files_dir=os.path.join(self.base_dir, "assets/files")
        
    def generate_random_string(self, length: int = 5):
     """Generate a random string of fixed length."""
     letters = string.ascii_lowercase + string.digits
     return ''.join(random.choices(letters, k=length))
        
        
        
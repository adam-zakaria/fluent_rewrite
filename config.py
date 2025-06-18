import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # API Host configuration
    API_HOST = os.getenv('API_HOST')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = 'flask_session'
    
    @classmethod
    def get_api_host(cls, request=None):
        """Get the API host dynamically"""
        # Check for environment variable first
        if cls.API_HOST:
            return cls.API_HOST
        
        if cls.DEBUG:
            return f'http://localhost:{cls.PORT}'
        else:
            # In production, use the same host as the request
            if request:
                return request.host_url.rstrip('/')
            return f'http://{cls.HOST}:{cls.PORT}' 
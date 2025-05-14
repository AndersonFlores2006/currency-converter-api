import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    API_KEY = os.getenv('API_KEY', '')
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en') 
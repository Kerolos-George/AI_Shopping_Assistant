import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEEPSEEK_API_KEY = "sk-8a2123c4dbeb4a59b2601ce807a33bfd"
    DEEPSEEK_BASE_URL = "https://api.deepseek.com"
    
    # Memory storage options
    MEMORY_TYPE = "file"  # Options: "memory", "file"
    MEMORY_FILE_PATH = "buyer_history.json"
    
    # Product catalog settings
    MAX_SEARCH_RESULTS = 3 
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'supabase')  # 'mysql' or 'supabase'
    
    # MySQL configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'hackathon_db')
    
    # Supabase configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # API Keys
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # IntaSend payment configuration
    INTASEND_PUBLIC_KEY = os.getenv('INTASEND_PUBLIC_KEY')
    INTASEND_SECRET_KEY = os.getenv('INTASEND_SECRET_KEY')
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
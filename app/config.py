import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class Config: 
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")

def get_db_connection():
    database_connection  = psycopg2.connect(DATABASE_URL)
    return database_connection   
    
    
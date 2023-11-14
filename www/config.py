import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path('.env'))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True
    PORT = 5050
    HOST = '0.0.0.0'
class DBParams:
    dbname = os.environ.get('POSTGRES_DB')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = 'db'
    port = 5432

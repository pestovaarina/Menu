import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

POSTGRES_USER_TEST = os.environ.get('POSTGRES_USER_TEST')
POSTGRES_PASSWORD_TEST = os.environ.get('POSTGRES_PASSWORD_TEST')
POSTGRES_DB_TEST = os.environ.get('POSTGRES_DB_TEST')

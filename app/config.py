from os import getenv

from dotenv import load_dotenv

load_dotenv()

database_url = getenv('DATABASE') 

DATABASE = database_url

print(DATABASE)
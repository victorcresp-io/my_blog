import os

from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE') 

DATABASE = database_url

print(DATABASE)

# titulo da postagem
# data postagen
# topico
# conteudo da postagem 
#
import sqlite3
import os

from flask import g
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv('DATABASE') 
DATABASE = database_url


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


DATABASE = database_url


print(DATABASE)

os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

conn = sqlite3.connect(DATABASE)




cursor = conn.cursor()
print('ok')


cursor.execute("""
SELECT sql
FROM sqlite_master
WHERE type='table' AND name='users';
""")

res = cursor.fetchall()
print(res)


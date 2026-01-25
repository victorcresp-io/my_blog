import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask, render_template, request
from .utils import get_db, close_db
from dotenv import load_dotenv

load_dotenv()

DATABASE = os.getenv('DATABASE') 
print(DATABASE)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=DATABASE,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.teardown_appcontext(close_db)

    # a simple page that says hello
    @app.route('/')
    def hello():
        db = get_db()
        row = db.execute("SELECT * FROM users").fetchall()
        
        return render_template('teste.html', posts = row)
    @app.route('/publicar', methods=['GET','POST'])
    def publicar():
        if request.method == 'POST':
            titulo = request.form['titulo']
            conteudo = request.form['conteudo']
            topico = 'Google Cloud'
            data = '09/11/2025'

            db = get_db()
            

            db.execute("""
            INSERT INTO users (titulo, conteudo, topico, data)
            VALUES (?, ?, ?, ?);
            """, (titulo, conteudo, topico, data))
            db.commit()

            print(titulo)
            print(conteudo)
        return render_template("post.html")

    def get_db_connection():
        load_dotenv()
        database_url = os.getenv('DATABASE') 
        DATABASE = database_url
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
        return conn

    @app.route("/posts")
    def listar_posts():
        post_id = request.args.get("id", type=int)
        db = get_db()
        row = db.execute("SELECT * FROM users WHERE id = ?", (post_id,)).fetchone()
        #conn = get_db()
        #cursor = conn.cursor()
        #cursor.execute("SELECT conteudo, titulo FROM users")
        #res = cursor.fetchall()
        return render_template("postagens.html", posts=row)

    return app
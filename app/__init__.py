import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask, render_template, request

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('main_pg.html')
    @app.route('/publicar', methods=['POST'])
    def publicar():
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        topico = 'Google Cloud'
        data = '09/11/2025'


        load_dotenv()
        database_url = os.getenv('DATABASE') 
        DATABASE = database_url
        #os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users (titulo, conteudo, topico, data)
        VALUES (?, ?, ?, ?);
        """, (titulo, conteudo, topico, data));

        conn.commit()
        conn.close()    
        print(titulo)
        print(conteudo)
        return 'deu certo'

    def get_db_connection():
        load_dotenv()
        database_url = os.getenv('DATABASE') 
        DATABASE = database_url
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
        return conn

    @app.route("/posts")
    def listar_posts():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT conteudo, titulo FROM users")
        posts = cursor.fetchone()
        print(posts[1])
        conn.close()

        return render_template("post.html", posts=posts)

    return app
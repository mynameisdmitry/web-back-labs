from flask import Blueprint, render_template, request, session, redirect
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

lab5 = Blueprint('lab5', __name__, url_prefix='/lab5')



def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='dmitry_igumenshev_knowledge_base',
        user='dmitry_igumenshev_knowledge_base',
        password='Dima2005',
        port=5432
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()



@lab5.route('')
@lab5.route('/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))



@lab5.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    cur.execute("SELECT login FROM users WHERE login = %s", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)

    cur.execute(
        "INSERT INTO users (login, password) VALUES (%s, %s)",
        (login, password_hash)
    )

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)



@lab5.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните поля')

    conn, cur = db_connect()

    cur.execute("SELECT * FROM users WHERE login = %s", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login

    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)



@lab5.route('/create', methods=['GET', 'POST'])
def create():
    user_login = session.get('login')
    if not user_login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not (title and article_text):
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn, cur = db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s", (user_login,))
    user = cur.fetchone()
    user_id = user['id']

    cur.execute(
        "INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)",
        (user_id, title, article_text)
    )

    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/list')
def list():
    user_login = session.get('login')
    if not user_login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # id текущего пользователя
    cur.execute("SELECT id FROM users WHERE login=%s", (user_login,))
    row = cur.fetchone()
    user_id = row['id']

    # все статьи только этого пользователя
    cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY id DESC", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)
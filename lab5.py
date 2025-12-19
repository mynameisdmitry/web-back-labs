from flask import Blueprint, render_template, request, session, redirect, current_app
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from werkzeug.security import generate_password_hash, check_password_hash

lab5 = Blueprint('lab5', __name__, url_prefix='/lab5')


# ----------------------------
# DB helpers (Postgres/SQLite)
# ----------------------------

def q(sql_text: str, db_type: str) -> str:
    """
    В коде пишем запросы в стиле Postgres (%s),
    а для SQLite автоматически заменяем %s -> ?
    """
    if db_type == 'sqlite':
        return sql_text.replace('%s', '?')
    return sql_text


def db_connect():
    """
    Возвращает (conn, cur, db_type).
    db_type берём из app.config['DB_TYPE'] -> 'postgres' или 'sqlite'.
    """
    db_type = current_app.config.get('DB_TYPE', 'postgres')

    if db_type == 'postgres':
        conn = psycopg2.connect(
            host=os.environ.get('PG_HOST', '127.0.0.1'),
            port=int(os.environ.get('PG_PORT', '5432')),
            database=os.environ.get('PG_DB', 'dmitry_igumenshev_knowledge_base'),
            user=os.environ.get('PG_USER', 'dmitry_igumenshev_knowledge_base'),
            password=os.environ.get('PG_PASSWORD', 'Dima2005'),
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cur, db_type

    # sqlite
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # чтобы row['id'] работало
    cur = conn.cursor()
    return conn, cur, db_type


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


# ----------------------------
# MAIN
# ----------------------------




@lab5.route('/')
def lab():
    username = session.get('login') or 'Anonymous'
    return render_template('lab5/lab5.html', username=username)


# ----------------------------
# REGISTER
# ----------------------------

@lab5.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = (request.form.get('login') or '').strip()
    password = (request.form.get('password') or '').strip()

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn = cur = None
    try:
        conn, cur, db_type = db_connect()

        # проверяем, что логина нет
        cur.execute(q("SELECT id FROM users WHERE login=%s", db_type), (login,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error='Такой пользователь уже существует')

        password_hash = generate_password_hash(password)

        cur.execute(
            q("INSERT INTO users (login, password) VALUES (%s, %s)", db_type),
            (login, password_hash)
        )

        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)

    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return render_template('lab5/register.html', error=f'Ошибка базы данных: {e}')


# ----------------------------
# LOGIN
# ----------------------------

@lab5.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login_value = (request.form.get('login') or '').strip()
    password = (request.form.get('password') or '').strip()

    if not login_value or not password:
        return render_template('lab5/login.html', error='Заполните поля')

    conn = cur = None
    try:
        conn, cur, db_type = db_connect()

        cur.execute(q("SELECT id, login, password FROM users WHERE login=%s", db_type), (login_value,))
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        # password в БД — это хеш
        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        session['login'] = login_value

        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login_value)

    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {e}')


# ----------------------------
# CREATE ARTICLE
# ----------------------------

@lab5.route('/create', methods=['GET', 'POST'])
def create():
    login_value = session.get('login')
    if not login_value:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = (request.form.get('title') or '').strip()
    article_text = (request.form.get('article_text') or '').strip()

    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn = cur = None
    try:
        conn, cur, db_type = db_connect()

        # находим id пользователя
        cur.execute(q("SELECT id FROM users WHERE login=%s", db_type), (login_value,))
        row = cur.fetchone()
        if not row:
            db_close(conn, cur)
            session.pop('login', None)
            return redirect('/lab5/login')

        login_id = row['id']

        cur.execute(
            q("INSERT INTO articles (login_id, title, article_text) VALUES (%s, %s, %s)", db_type),
            (login_id, title, article_text)
        )

        db_close(conn, cur)
        return redirect('/lab5')

    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return render_template('lab5/create_article.html', error=f'Ошибка базы данных: {e}')


# ----------------------------
# LIST ARTICLES (only own)
# ----------------------------

@lab5.route('/list')
def list_articles():
    login_value = session.get('login')
    if not login_value:
        return redirect('/lab5/login')

    conn = cur = None
    try:
        conn, cur, db_type = db_connect()

        cur.execute(q("SELECT id FROM users WHERE login=%s", db_type), (login_value,))
        row = cur.fetchone()
        if not row:
            db_close(conn, cur)
            session.pop('login', None)
            return redirect('/lab5/login')

        login_id = row['id']

        cur.execute(
            q("SELECT id, title, article_text FROM articles WHERE login_id=%s ORDER BY id DESC", db_type),
            (login_id,)
        )
        articles = cur.fetchall()

        db_close(conn, cur)
        return render_template('lab5/articles.html', articles=articles)

    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return f"Ошибка базы данных: {e}", 500
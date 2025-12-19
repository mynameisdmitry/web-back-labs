from flask import Blueprint, render_template, request, session, redirect, current_app

import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash
from os import path

lab5 = Blueprint('lab5', __name__, url_prefix='/lab5')


def sql(query_ps: str) -> str:
    """
    Пишем запросы в стиле Postgres (%s),
    а для SQLite автоматически заменяем %s -> ?
    """
    db_type = current_app.config.get('DB_TYPE', 'postgres')
    if db_type == 'sqlite':
        return query_ps.replace('%s', '?')
    return query_ps


def db_connect():
    """
    Возвращает (conn, cur)
    DB_TYPE берём из app.config['DB_TYPE'] -> 'postgres' или 'sqlite'
    """
    db_type = current_app.config.get('DB_TYPE', 'postgres')

    if db_type == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='dmitry_igumenshev_knowledge_base',
            user='dmitry_igumenshev_knowledge_base',
            password='Dima2005',
            port=5432
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cur

    # sqlite
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


# ---------- MAIN ----------
@lab5.route('/')
def lab():
    username = session.get('login') or 'Anonymous'
    return render_template('lab5/lab5.html', username=username)


# ---------- REGISTER ----------
@lab5.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login_value = (request.form.get('login') or '').strip()
    password = (request.form.get('password') or '').strip()

    if not login_value or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn = cur = None
    try:
        conn, cur = db_connect()

        # проверка существования логина (защита от SQL-инъекций)
        cur.execute(sql("SELECT id FROM users WHERE login=%s"), (login_value,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error='Такой пользователь уже существует')

        password_hash = generate_password_hash(password)

        cur.execute(
            sql("INSERT INTO users (login, password) VALUES (%s, %s)"),
            (login_value, password_hash)
        )

        db_close(conn, cur)
        return render_template('lab5/success.html', login=login_value)

    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return render_template('lab5/register.html', error=f'Ошибка базы данных: {e}')


# ---------- LOGIN ----------
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
        conn, cur = db_connect()

        cur.execute(sql("SELECT id, login, password FROM users WHERE login=%s"), (login_value,))
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин или пароль неверны')





        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин или пароль неверны')

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


# ---------- CREATE ARTICLE ----------
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
        conn, cur = db_connect()

        cur.execute(sql("SELECT id FROM users WHERE login=%s"), (login_value,))
        user_row = cur.fetchone()
        if not user_row:
            db_close(conn, cur)
            session.pop('login', None)
            return redirect('/lab5/login')

        user_id = user_row['id']

        cur.execute(
            sql("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)"),
            (user_id, title, article_text)
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


# ---------- LIST ----------
@lab5.route('/list')
def list_articles():
    login_value = session.get('login')
    if not login_value:
        return redirect('/lab5/login')

    conn = cur = None
    try:
        conn, cur = db_connect()

        cur.execute(sql("SELECT id FROM users WHERE login=%s"), (login_value,))
        user_row = cur.fetchone()
        if not user_row:
            db_close(conn, cur)
            session.pop('login', None)
            return redirect('/lab5/login')

        user_id = user_row['id']

        cur.execute(
            sql("SELECT id, title, article_text FROM articles WHERE user_id=%s ORDER BY id DESC"),
            (user_id,)
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
    
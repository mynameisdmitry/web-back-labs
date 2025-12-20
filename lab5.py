from flask import Blueprint, render_template, request, session, redirect, current_app, url_for

import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

from werkzeug.security import generate_password_hash, check_password_hash

lab5 = Blueprint('lab5', __name__, url_prefix='/lab5')


# -------------------------
# Helpers: SQL placeholders
# -------------------------
def sql(query_ps: str) -> str:
    """
    Запросы пишем в стиле Postgres (%s),
    а для SQLite автоматически заменяем %s -> ?
    """
    db_type = current_app.config.get('DB_TYPE', 'postgres')
    if db_type == 'sqlite':
        return query_ps.replace('%s', '?')
    return query_ps


# -------------------------
# Helpers: DB connect/close
# -------------------------
def db_connect():
    """
    Возвращает (conn, cur)
    DB_TYPE: 'postgres' или 'sqlite'
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

    # sqlite (на PythonAnywhere обычно будет именно он)
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


def get_login_id():
    """
    Возвращает (login_value, login_id).
    login_id — это users.id.
    """
    login_value = session.get('login')
    if not login_value:
        return None, None

    conn = cur = None
    try:
        conn, cur = db_connect()
        cur.execute(sql("SELECT id FROM users WHERE login=%s"), (login_value,))
        row = cur.fetchone()
        db_close(conn, cur)

        if not row:
            return login_value, None
        return login_value, row['id']

    except Exception:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return login_value, None


# -------------------------
# MAIN
# -------------------------
@lab5.route('/')
def lab():
    username = session.get('login') or 'Anonymous'
    return render_template('lab5/lab5.html', username=username)



@lab5.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('lab5.lab'))


# -------------------------
# REGISTER
# -------------------------
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


# -------------------------
# LOGIN
# -------------------------
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

        if (not user) or (not check_password_hash(user['password'], password)):
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


# -------------------------
# CREATE ARTICLE
# -------------------------
@lab5.route('/create', methods=['GET', 'POST'])
def create():
    login_value, login_id = get_login_id()
    if not login_value or not login_id:
        session.pop('login', None)
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

        # В БД колонка называется login_id
        cur.execute(
            sql("INSERT INTO articles (login_id, title, article_text) VALUES (%s, %s, %s)"),
            (login_id, title, article_text)
        )

        db_close(conn, cur)
        return redirect('/lab5/list')

    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return render_template('lab5/create_article.html', error=f'Ошибка базы данных: {e}')


# -------------------------
# LIST ARTICLES (only own)
# -------------------------
@lab5.route('/list')
def list_articles():
    login_value, login_id = get_login_id()
    if not login_value or not login_id:
        session.pop('login', None)
        return redirect('/lab5/login')

    conn = cur = None
    try:
        conn, cur = db_connect()

        cur.execute(
            sql("SELECT id, title, article_text FROM articles WHERE login_id=%s ORDER BY id DESC"),
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


# -------------------------
# EDIT ARTICLE
# -------------------------
@lab5.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login_value, login_id = get_login_id()
    if not login_value or not login_id:
        session.pop('login', None)
        return redirect('/lab5/login')

    conn = cur = None
    try:
        conn, cur = db_connect()

        if request.method == 'GET':
            cur.execute(
                sql("SELECT id, title, article_text FROM articles WHERE id=%s AND login_id=%s"),
                (article_id, login_id)
            )
            article = cur.fetchone()
            db_close(conn, cur)

            if not article:
                return "Статья не найдена", 404

            return render_template('lab5/edit_article.html', article=article)

        # POST
        title = (request.form.get('title') or '').strip()
        text = (request.form.get('article_text') or '').strip()

        if not title or not text:

            db_close(conn, cur)
            return render_template(
                'lab5/edit_article.html',
                article={'id': article_id, 'title': title, 'article_text': text},
                error='Заполните все поля'
            )

        cur.execute(
            sql("UPDATE articles SET title=%s, article_text=%s WHERE id=%s AND login_id=%s"),
            (title, text, article_id, login_id)
        )
        db_close(conn, cur)
        return redirect('/lab5/list')

    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return f"Ошибка базы данных: {e}", 500


# -------------------------
# DELETE ARTICLE
# -------------------------
@lab5.route('/delete/<int:article_id>')
def delete_article(article_id):
    login_value, login_id = get_login_id()
    if not login_value or not login_id:
        session.pop('login', None)
        return redirect('/lab5/login')

    conn = cur = None
    try:
        conn, cur = db_connect()

        cur.execute(
            sql("DELETE FROM articles WHERE id=%s AND login_id=%s"),
            (article_id, login_id)
        )

        db_close(conn, cur)
        return redirect('/lab5/list')

    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return f"Ошибка базы данных: {e}", 500

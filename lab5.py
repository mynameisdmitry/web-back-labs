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
    """Запросы пишем в стиле Postgres (%s), а для SQLite автоматически заменяем %s -> ?"""
    db_type = current_app.config.get('DB_TYPE', 'postgres')
    if db_type == 'sqlite':
        return query_ps.replace('%s', '?')
    return query_ps


# -------------------------
# Helpers: DB connect/close
# -------------------------
def db_connect():
    """Возвращает (conn, cur) DB_TYPE: 'postgres' или 'sqlite'"""
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
    """Возвращает (login_value, user_id, real_name). user_id — это users.id."""
    login_value = session.get('login')
    if not login_value:
        return None, None, None
    
    conn = cur = None
    try:
        conn, cur = db_connect()
        cur.execute(sql("SELECT id, real_name FROM users WHERE login=%s"), (login_value,))
        row = cur.fetchone()
        db_close(conn, cur)
        
        if not row:
            return login_value, None, None
        
        return login_value, row['id'], row.get('real_name', '')
    except Exception:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return login_value, None, None



# -------------------------
# MAIN
# -------------------------
@lab5.route('/')
def lab():
    username = session.get('login') or 'Anonymous'
    login_value, user_id, real_name = get_login_id()
    
    # Если пользователь авторизован, показываем его реальное имя
    if real_name and real_name.strip():
        display_name = real_name
    elif username != 'Anonymous':
        display_name = username
    else:
        display_name = 'Anonymous'
    
    return render_template('lab5/lab5.html', username=display_name)

@lab5.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('lab5.lab'))

# -------------------------
# FORGOT PASSWORD
# -------------------------
@lab5.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('lab5/forgot_password.html')
    
    login_value = (request.form.get('login') or '').strip()
    
    if not login_value:
        return render_template('lab5/forgot_password.html', error='Введите логин')
    
    conn = cur = None
    try:
        conn, cur = db_connect()
        cur.execute(sql("SELECT id, login, real_name FROM users WHERE login=%s"), (login_value,))
        user = cur.fetchone()
        db_close(conn, cur)
        
        if not user:
            return render_template('lab5/forgot_password.html', 
                                 error='Пользователь с таким логином не найден')
        
        # В реальном приложении здесь была бы отправка email с ссылкой на сброс пароля
        # Но для простоты просто покажем сообщение
        return render_template('lab5/forgot_password_success.html', 
                             login=login_value,
                             real_name=user.get('real_name', ''))
    
    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return render_template('lab5/forgot_password.html', error=f'Ошибка базы данных: {e}')
    
# -------------------------
# REGISTER (обновленный с полем реального имени)
# -------------------------
@lab5.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login_value = (request.form.get('login') or '').strip()
    password = (request.form.get('password') or '').strip()
    real_name = (request.form.get('real_name') or '').strip()
    
    if not login_value or not password:
        return render_template('lab5/register.html', error='Заполните обязательные поля')
    
    conn = cur = None
    try:
        conn, cur = db_connect()
        
        # Проверяем, существует ли пользователь
        cur.execute(sql("SELECT id FROM users WHERE login=%s"), (login_value,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error='Такой пользователь уже существует')
        
        # Хешируем пароль
        password_hash = generate_password_hash(password)
        
        # Вставляем нового пользователя
        cur.execute(
            sql("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s)"),
            (login_value, password_hash, real_name)
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
        cur.execute(sql("SELECT id, login, password, real_name FROM users WHERE login=%s"), (login_value,))
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
# CREATE ARTICLE (ИСПРАВЛЕНО: user_id вместо login_id)
# -------------------------
@lab5.route('/create', methods=['GET', 'POST'])
def create():
    login_value, user_id, real_name = get_login_id()
    if not login_value or not user_id:
        session.pop('login', None)
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = (request.form.get('title') or '').strip()
    article_text = (request.form.get('article_text') or '').strip()
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните все поля')
    
    conn = cur = None
    try:
        conn, cur = db_connect()
        
        cur.execute(
            sql("INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) VALUES (%s, %s, %s, %s, %s)"),
            (user_id, title, article_text, is_favorite, is_public)
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
# LIST ARTICLES (ИСПРАВЛЕНО: user_id вместо login_id)
# -------------------------
@lab5.route('/list')
def list_articles():
    login_value, user_id, real_name = get_login_id()
    
    # Публичные статьи доступны всем
    public_articles = []
    
    conn = cur = None
    try:
        conn, cur = db_connect()
        
        # Получаем публичные статьи (ИСПРАВЛЕНО JOIN)
        cur.execute(
            sql("""
                SELECT a.id, a.title, a.article_text, a.is_favorite, a.is_public, 
                       u.login as author_login, u.real_name as author_name
                FROM articles a
                JOIN users u ON a.user_id = u.id
                WHERE a.is_public = TRUE
                ORDER BY a.is_favorite DESC, a.id DESC
            """)
        )
        public_articles = cur.fetchall()
        
        # Если пользователь авторизован, получаем его статьи
        user_articles = []
        if login_value and user_id:
            cur.execute(
                sql("""
                    SELECT id, title, article_text, is_favorite, is_public
                    FROM articles 
                    WHERE user_id=%s 
                    ORDER BY is_favorite DESC, id DESC
                """),
                (user_id,)
            )
            user_articles = cur.fetchall()
        
        db_close(conn, cur)
        
        return render_template('lab5/articles.html', 
                             articles=user_articles,
                             public_articles=public_articles,
                             username=login_value or 'Anonymous')
    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return f"Ошибка базы данных: {e}", 500


# -------------------------
# EDIT ARTICLE (ИСПРАВЛЕНО: user_id вместо login_id)
# -------------------------
@lab5.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login_value, user_id, real_name = get_login_id()
    if not login_value or not user_id:
        session.pop('login', None)
        return redirect('/lab5/login')
    
    conn = cur = None
    try:
        conn, cur = db_connect()
        
        if request.method == 'GET':
            cur.execute(
                sql("SELECT id, title, article_text, is_favorite, is_public FROM articles WHERE id=%s AND user_id=%s"),
                (article_id, user_id)
            )
            article = cur.fetchone()
            db_close(conn, cur)
            
            if not article:
                return "Статья не найдена", 404
            
            return render_template('lab5/edit_article.html', article=article)
        
        # POST запрос
        title = (request.form.get('title') or '').strip()
        text = (request.form.get('article_text') or '').strip()
        is_favorite = request.form.get('is_favorite') == 'on'
        is_public = request.form.get('is_public') == 'on'
        
        if not title or not text:

            db_close(conn, cur)
            return render_template(
                'lab5/edit_article.html',
                article={'id': article_id, 'title': title, 'article_text': text},
                error='Заполните все поля'
            )
        
        cur.execute(
            sql("UPDATE articles SET title=%s, article_text=%s, is_favorite=%s, is_public=%s WHERE id=%s AND user_id=%s"),
            (title, text, is_favorite, is_public, article_id, user_id)
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
# DELETE ARTICLE (ИСПРАВЛЕНО: user_id вместо login_id)
# -------------------------
@lab5.route('/delete/<int:article_id>')
def delete_article(article_id):
    login_value, user_id, real_name = get_login_id()
    if not login_value or not user_id:
        session.pop('login', None)
        return redirect('/lab5/login')
    
    conn = cur = None
    try:
        conn, cur = db_connect()

        cur.execute(
            sql("DELETE FROM articles WHERE id=%s AND user_id=%s"),
            (article_id, user_id)
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
# НОВАЯ СТРАНИЦА: Список пользователей
# -------------------------
@lab5.route('/users')
def list_users():
    conn = cur = None
    try:
        conn, cur = db_connect()
        cur.execute(
            sql("SELECT id, login, real_name FROM users ORDER BY login")
        )
        users = cur.fetchall()
        db_close(conn, cur)
        
        return render_template('lab5/users.html', users=users)
    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return f"Ошибка базы данных: {e}", 500

# -------------------------
# НОВАЯ СТРАНИЦА: Профиль пользователя (смена имени и пароля)
# -------------------------
@lab5.route('/profile', methods=['GET', 'POST'])
def profile():
    login_value, user_id, real_name = get_login_id()
    if not login_value or not user_id:
        session.pop('login', None)
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/profile.html', real_name=real_name or '', login=login_value)
    
    # Обработка POST запроса
    new_real_name = (request.form.get('real_name') or '').strip()
    current_password = (request.form.get('current_password') or '').strip()
    new_password = (request.form.get('new_password') or '').strip()
    confirm_password = (request.form.get('confirm_password') or '').strip()
    
    conn = cur = None
    try:
        conn, cur = db_connect()
        
        # Проверяем текущий пароль
        cur.execute(sql("SELECT password FROM users WHERE id=%s"), (user_id,))
        user = cur.fetchone()
        
        if not user or not check_password_hash(user['password'], current_password):
            db_close(conn, cur)
            return render_template('lab5/profile.html', 
                                 real_name=new_real_name or real_name or '',
                                 login=login_value,
                                 error='Неверный текущий пароль')
        
        # Проверяем новый пароль
        if new_password:
            if new_password != confirm_password:
                db_close(conn, cur)
                return render_template('lab5/profile.html', 
                                     real_name=new_real_name or real_name or '',
                                     login=login_value,
                                     error='Новый пароль и подтверждение не совпадают')
            
            if len(new_password) < 6:
                db_close(conn, cur)
                return render_template('lab5/profile.html', 
                                     real_name=new_real_name or real_name or '',
                                     login=login_value,
                                     error='Новый пароль должен содержать минимум 6 символов')
            
            # Хешируем новый пароль
            new_password_hash = generate_password_hash(new_password)
            
            # Обновляем имя и пароль
            cur.execute(
                sql("UPDATE users SET real_name=%s, password=%s WHERE id=%s"),
                (new_real_name, new_password_hash, user_id)
            )
        else:
            # Обновляем только имя
            cur.execute(
                sql("UPDATE users SET real_name=%s WHERE id=%s"),
                (new_real_name, user_id)
            )
        
        db_close(conn, cur)
        return render_template('lab5/profile_success.html', login=login_value)
    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return render_template('lab5/profile.html', 
                             real_name=new_real_name or real_name or '',
                             login=login_value,
                             error=f'Ошибка базы данных: {e}')

# -------------------------
# НОВАЯ СТРАНИЦА: Успешное обновление профиля
# -------------------------
@lab5.route('/profile/success')
def profile_success():
    login_value, user_id, real_name = get_login_id()
    if not login_value:
        return redirect('/lab5/login')
    
    return render_template('lab5/profile_success.html', login=login_value)

# -------------------------
# НОВАЯ СТРАНИЦА: Публичные статьи (ИСПРАВЛЕНО: user_id вместо login_id)
# -------------------------
@lab5.route('/public')
def public_articles():
    conn = cur = None
    try:
        conn, cur = db_connect()
        
        cur.execute(
            sql("""
                SELECT a.id, a.title, a.article_text, a.is_favorite, a.is_public,
                       u.login as author_login, u.real_name as author_name
                FROM articles a
                JOIN users u ON a.user_id = u.id
                WHERE a.is_public = TRUE
                ORDER BY a.is_favorite DESC, a.id DESC
            """)
        )
        articles = cur.fetchall()
        
        db_close(conn, cur)
        return render_template('lab5/public_articles.html', articles=articles)
    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return f"Ошибка базы данных: {e}", 500
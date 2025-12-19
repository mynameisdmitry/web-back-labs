from flask import Blueprint, render_template, request, session
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__, url_prefix='/lab5')


def db_connect():
    return psycopg2.connect(
        host='127.0.0.1',
        database='dmitry_igumenshev_knowledge_base',
        user='dmitry_igumenshev_knowledge_base',
        password='Dima2005',
        port=5432
    )


@lab5.route('')
@lab5.route('/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


@lab5.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    try:
        conn = db_connect()
        cur = conn.cursor()

        cur.execute("SELECT login FROM users WHERE login = %s", (login,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return render_template('lab5/register.html', error='Такой пользователь уже существует')

        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password))
        conn.commit()

        cur.close()
        conn.close()

        return render_template('lab5/success.html', login=login)

    except psycopg2.OperationalError as e:
        return render_template('lab5/register.html', error=f'Ошибка подключения к БД: {e}')
    except Exception as e:
        return render_template('lab5/register.html', error=f'Ошибка базы данных: {e}')


@lab5.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните поля')

    conn = None
    cur = None
    try:
        conn = db_connect()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM users WHERE login = %s", (login,))
        user = cur.fetchone()

        if not user:
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        if user['password'] != password:
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        session['login'] = login

        return render_template('lab5/success_login.html', login=login)

    except psycopg2.OperationalError as e:
        return render_template('lab5/login.html', error=f'Ошибка подключения к БД: {e}')
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {e}')
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

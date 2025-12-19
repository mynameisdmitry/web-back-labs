from flask import Blueprint, render_template, request
import psycopg2

lab5 = Blueprint('lab5', __name__, url_prefix='/lab5')

@lab5.route('')
@lab5.route('/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='dmitry_igumenshev_knowledge_base',
            user='dmitry_igumenshev_knowledge_base',
            password='Dima2005',
            port=5432
        )
        cur = conn.cursor()

        cur.execute("SELECT login FROM users WHERE login = %s", (login,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password))
        conn.commit()

        cur.close()
        conn.close()

        return render_template('lab5/success.html', login=login)

    except psycopg2.OperationalError as e:
        return render_template('lab5/register.html', error=f'Ошибка подключения к БД: {e}')
    except Exception as e:
        return render_template('lab5/register.html', error=f'Ошибка базы данных: {e}')
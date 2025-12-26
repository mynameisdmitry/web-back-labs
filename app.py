from flask import Flask, url_for, request, redirect, abort, render_template, session
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from functools import wraps
import datetime
import os

app = Flask(__name__)

# Важные настройки для PythonAnywhere
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'секретно-секретный-секрет'),
    # Настройки для сессий на PythonAnywhere
    SESSION_COOKIE_NAME='flask_session',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # True если используете HTTPS
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600,  # 1 час
    # Важно для PythonAnywhere
    APPLICATION_ROOT='/'
)

app.secret_key = app.config['SECRET_KEY']

# Определяем окружение
IS_PYTHONANYWHERE = bool(os.environ.get('PYTHONANYWHERE_DOMAIN'))

# Позволяем переопределять явно через переменную окружения DB_TYPE,
# но по умолчанию: локально Postgres, на PythonAnywhere SQLite
default_db = 'sqlite' if IS_PYTHONANYWHERE else 'postgres'
app.config['DB_TYPE'] = os.environ.get('DB_TYPE', default_db)


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)

access_log = []

COMMON_STYLES = '''
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(45deg, #f0f4ff, #e6f7ff);
        min-height: 100vh;
        padding: 20px;
        padding-bottom: 100px;
    }
    .container {
        max-width: 1000px;
        margin: 0 auto;
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 3px solid #2c3e50;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
        font-size: 2.5em;
        font-weight: 700;
    }
    h2 {
        color: #2c3e50;
        margin: 25px 0 15px;
        font-size: 1.8em;
        font-weight: 600;
    }
    p {
        color: #5a6c7d;
        line-height: 1.6;
        margin: 15px 0;
        font-size: 1.1em;
    }
    a {
        color: #2c3e50;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    a:hover {
        color: #1a252f;
        text-decoration: underline;
    }
    .button {
        display: inline-block;
        background: #2c3e50;
        color: white;
        padding: 12px 30px;
        text-decoration: none;
        border-radius: 25px;
        font-weight: bold;
        margin: 10px 5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(44, 62, 80, 0.3);
        border: none;
        cursor: pointer;
    }
    .button:hover {
        background: #1a252f;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(44, 62, 80, 0.4);
        text-decoration: none;
    }
    .nav-menu {
        text-align: center;
        margin: 30px 0;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 10px;
    }
    .nav-menu a {
        margin: 0 15px;
        font-size: 1.1em;
        color: #2c3e50;
    }
    .nav-menu a:hover {
        color: #1a252f;
    }
    ul, ol {
        margin: 15px 0;
        padding-left: 30px;
    }
    li {
        margin: 10px 0;
        color: #2c3e50;
    }
    li a {
        color: #2c3e50;
    }
    li a:hover {
        color: #1a252f;
    }
    .highlight {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 4px solid #2c3e50;
    }
    .code {
        background: #2c3e50;
        color: #ecf0f1;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        margin: 15px 0;
    }
    .emoji {
        font-size: 1.2em;
        margin: 0 3px;
    }
    footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        padding: 15px 0;
        background: #2c3e50;
        color: white;
        text-align: center;
        box-shadow: 0 -1px 4px rgba(0,0,0,0.08);
        z-index: 1000;
    }
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    .info-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #2c3e50;
    }
    img {
        max-width: 100%;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        margin: 20px 0;
    }
    .error-code {
        font-size: 100px;
        color: #e74c3c;
        text-align: center;
        margin: 0;
        text-shadow: 3px 3px 0 #e0e0e0;
        font-weight: 800;
    }
    .error-message {
        color: #2c3e50;
        text-align: center;
        margin: 10px 0 30px;
        font-size: 28px;
        font-weight: 600;
    }
    .image-container {
        text-align: center;
        margin: 30px 0;
    }
    .error-image {
        max-width: 250px;
        margin: 20px auto;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
        display: block;
    }
    .error-image:hover {
        transform: scale(1.05);
    }
    .quote {
        font-style: italic;
        color: #7f8c8d;
        border-left: 4px solid #2c3e50;
        padding-left: 15px;
        margin: 25px auto;
        text-align: center;
    }
    .technical-info {
        background: #fff5f5;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #e74c3c;
        margin: 20px 0;
    }
    .routes-list {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 10px;
        margin: 25px 0;
    }
    .routes-list h3 {
        color: #2c3e50;
        margin-bottom: 15px;
        font-size: 1.4em;
    }
    .route-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 15px;
        margin: 8px 0;
        background: white;
        border-radius: 8px;
        border-left: 4px solid #2c3e50;
        transition: all 0.3s ease;
    }
    .route-item:hover {
        transform: translateX(5px);
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    .route-path {
        font-family: 'Courier New', monospace;
        font-weight: bold;
        color: #2c3e50;
    }
    .route-desc {
        color: #5a6c7d;
        font-size: 0.95em;
    }
    .log-container {
        background: #2c3e50;
        color: #ecf0f1;
        padding: 20px;
        border-radius: 10px;
        margin: 25px 0;
        max-height: 400px;
        overflow-y: auto;
    }
    .log-header {
        color: #ecf0f1;
        text-align: center;
        margin-bottom: 15px;
        font-size: 1.3em;
        font-weight: 600;
    }
    .log-entry {
        padding: 10px;
        margin: 8px 0;
        background: #34495e;
        border-radius: 5px;
        border-left: 3px solid #ecf0f1;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }
    .log-timestamp {
        color: #e74c3c;
        font-weight: bold;
    }
    .log-ip {
        color: #2ecc71;
        font-weight: bold;
    }
    .log-path {
        color: #f39c12;
    }
    .client-info {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #2c3e50;
    }
    .client-info h3 {
        color: #2c3e50;
        margin-bottom: 10px;
    }
</style>
'''

FOOTER = '''
<footer>
    Игуменшев Дмитрий Евгеньевич, ФБИ-33, 3 курс, 2025 год
</footer>
'''

@app.errorhandler(500)
def internal_server_error(err):
    return f'''
<!doctype html>
<html>
    <head>
        <title>500 - Ошибка сервера</title>
        {COMMON_STYLES}
    </head>
    <body>
        <div class="container">
            <div class="error-code">500</div>
            <div class="error-message">Внутренняя ошибка сервера</div>
            
            <div class="image-container">
                <img class="error-image" src="{url_for('static', filename='lab1/500.png')}" alt="Ошибка сервера">
            </div>
            
            <p>На сервере произошла непредвиденная ошибка. Наши инженеры уже работают над решением проблемы.</p>
            
            <div class="technical-info">
                <h3>Что произошло?</h3>
                <p>Сервер столкнулся с внутренней ошибкой и не может выполнить ваш запрос.</p>
                <p>Это может быть связано с временными техническими неполадками или ошибкой в коде.</p>
            </div>
            
            <div class="quote">
                "Даже у серверов бывают плохие дни... Но мы уже исправляем ситуацию!"
            </div>
            
            <div style="text-align: center;">
                <a href="/" class="button">Вернуться на главную</a>
                <a href="/lab1" class="button">К лабораторным работам</a>
            </div>
        </div>
        {FOOTER}
    </body>
</html>''', 500

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_path = request.path
    
    log_entry = {
        'timestamp': access_date,
        'ip': client_ip,
        'path': requested_path
    }
    access_log.append(log_entry)
    
    if len(access_log) > 50:
        access_log.pop(0)
    
    log_html = ''
    for entry in reversed(access_log):
        log_html += f'''
        <div class="log-entry">
            <span class="log-timestamp">[{entry['timestamp']}]</span> 
            <span class="log-ip">IP: {entry['ip']}</span> 
            посетил <span class="log-path">{entry['path']}</span>
        </div>
        '''
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>404 - Страница потерялась в лабиринте</title>
        {COMMON_STYLES}
        <style>
            .error-code {{
                color: #2c3e50;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="error-code">404</div>
            <div class="error-message">Страница потерялась в лабиринте</div>
            
            <div class="image-container">
                <img class="error-image" src="{url_for('static', filename='lab1/404.png')}" alt="Заблудившийся путешественник">
            </div>
            
            <div class="client-info">
                <h3>Информация о вашем посещении:</h3>
                <p><strong>Ваш IP-адрес:</strong> {client_ip}</p>
                <p><strong>Дата и время доступа:</strong> {access_date}</p>
                <p><strong>Запрошенный адрес:</strong> {requested_path}</p>
            </div>
            
            <p>Кажется, эта страница отправилась в собственное приключение и не может найти дорогу назад.</p>
            
            <div class="quote">
                "Иногда заблудиться - значит найти нечто большее, чем искал"
            </div>
            
            <p>Но не беспокойтесь! Пока страница ищет свой путь, вы можете вернуться в безопасную гавань главной страницы.</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="/" class="button">Вернуться на главную страницу</a>
                <a href="/lab1" class="button">К лабораторным работам</a>
            </div>
            
            <div class="log-container">
                <div class="log-header">Журнал посещений (последние 50 записей)</div>
                {log_html if log_html else '<div class="log-entry">Журнал посещений пуст</div>'}
            </div>
        </div>
        {FOOTER}
    </body>
</html>''', 404



@app.route("/")
@app.route("/index")
def index():
    return f"""
<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <link rel="icon" type="image/x-icon" href="/static/fav/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/static/fav/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/static/fav/favicon-16x16.png">
    <title>НГТУ, ФБ, Лабораторные работы</title>
    {COMMON_STYLES}
</head>
<body>
    <div class="container">
        <h1>НГТУ, ФБ, WEB-программирование, часть 2</h1>
        <h2>Список лабораторных работ</h2>

        <div class="highlight">
            <p>Добро пожаловать на платформу для выполнения лабораторных работ по WEB-программированию!</p>
        </div>

        <div class="info-grid">
            <div class="info-card">
                <h3>Лабораторная работа 1</h3>
                <p>Знакомство с Flask и создание базового веб-приложения</p>
                <a href="/lab1" class="button">Перейти к работе</a>
            </div>

            <div class="info-card">
                <h3>Лабораторная работа 2</h3>
                <p>Работа с шаблонами и маршрутизацией</p>
                <a href="/lab2" class="button">Перейти к работе</a>
            </div>

            <div class="info-card">
                <h3>Лабораторная работа 3</h3>
                <p>Работа с cookies и сессиями</p>
                <a href="/lab3" class="button">Перейти к работе</a>
            </div>

            <div class="info-card">
                <h3>Лабораторная работа 4</h3>
                <p>Формы (POST), сессии</p>
                <a href="/lab4" class="button">Перейти к работе</a>
            </div>

            <div class="info-card">
                <h3>Лабораторная работа 5</h3>
                <p>Flask и БД</p>
                <a href="/lab5" class="button">Перейти к работе</a>
            </div>

            <div class="info-card">
                <h3>Лабораторная работа 6</h3>
                <p>API JSON-RPC</p>
                <a href="/lab6" class="button">Перейти к работе</a>
            </div>
            <div class="info-card">
                <h3>Лабораторная работа 7</h3>
                <p>API REST</p>
                <a href="/lab7" class="button">Перейти к работе</a>
            </div>
        </div>

    {FOOTER}
</body>
</html>
"""





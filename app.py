from flask import Flask, url_for, request, redirect, abort, render_template
import datetime

app = Flask(__name__)

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
        border: 3px solid #4a90e2;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
        font-size: 2.5em;
        font-weight: 700;
    }
    h2 {
        color: #34495e;
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
        color: #4a90e2;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    a:hover {
        color: #357abd;
        text-decoration: underline;
    }
    .button {
        display: inline-block;
        background: #4a90e2;
        color: white;
        padding: 12px 30px;
        text-decoration: none;
        border-radius: 25px;
        font-weight: bold;
        margin: 10px 5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
        border: none;
        cursor: pointer;
    }
    .button:hover {
        background: #357abd;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
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
    }
    ul, ol {
        margin: 15px 0;
        padding-left: 30px;
    }
    li {
        margin: 10px 0;
        color: #5a6c7d;
    }
    .highlight {
        background: #e3f2fd;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 4px solid #4a90e2;
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
        border-left: 4px solid #4a90e2;
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
        border-left: 4px solid #4a90e2;
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
        border-left: 4px solid #4a90e2;
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
        color: #4a90e2;
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
        border-left: 3px solid #4a90e2;
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
        background: #e8f4fd;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #3498db;
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
                <img class="error-image" src="{url_for('static', filename='500.png')}" alt="Ошибка сервера">
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
            
                color: #4a90e2;

            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="error-code">404</div>
            <div class="error-message">Страница потерялась в лабиринте</div>
            
            <div class="image-container">
                <img class="error-image" src="{url_for('static', filename='404.png')}" alt="Заблудившийся путешественник">
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

@app.route('/lab1/server_error')
def server_error():
    result = 10 / 0
    return "Эта строка никогда не выполнится"

@app.route("/")
@app.route("/index")
def index():
    return f"""
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
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
            </div>
            
            <div class="nav-menu">
                <a href="/lab1/http_codes">Тестирование HTTP кодов</a> |
                <a href="/nonexistent-page">Тест 404 ошибки</a> |
                <a href="/lab1/server_error">Тест 500 ошибки</a>
            </div>
        </div>
        {FOOTER}
    </body>
</html>
"""


@app.route("/lab1")
def lab1():
    return f'''
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Лабораторная 1</title>
    {COMMON_STYLES}
</head>
<body>
    <div class="container">
        <h1>Лабораторная работа 1</h1>
        
        <div class="highlight">
            <p><strong>Flask</strong> — фреймворк для создания веб-приложений на языке программирования Python,
            использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2.
            Относится к категории так называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        </div>
        
        <div class="nav-menu">
            <a href="/lab1/author">Author</a> |
            <a href="/lab1/web">Web</a> |
            <a href="/lab1/image">Image</a> |
            <a href="/lab1/counter">Counter</a> |
            <a href="/lab1/http_codes">HTTP коды</a> |
            <a href="/lab1/server_error">Тест 500 ошибки</a>
        </div>

        <h2>Список роутов</h2>
        
        <div class="routes-list">
            <h3>Основные роуты лабораторной работы 1:</h3>
            
            <div class="route-item">
                <div>
                    <a href="/" class="route-path">/</a>
                    <div class="route-desc">Главная страница со списком лабораторных работ</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/index" class="route-path">/index</a>
                    <div class="route-desc">Альтернативный адрес главной страницы</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1" class="route-path">/lab1</a>
                    <div class="route-desc">Основная страница лабораторной работы 1</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/author" class="route-path">/lab1/author</a>
                    <div class="route-desc">Страница с информацией об авторе</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/web" class="route-path">/lab1/web</a>
                    <div class="route-desc">Демонстрация работы веб-сервера с кастомными заголовками</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/image" class="route-path">/lab1/image</a>
                    <div class="route-desc">Страница с изображением океана и дополнительными заголовками</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/counter" class="route-path">/lab1/counter</a>
                    <div class="route-desc">Счётчик посещений с информацией о клиенте</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/reset_counter" class="route-path">/lab1/reset_counter</a>
                    <div class="route-desc">Сброс счётчика посещений</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/info" class="route-path">/lab1/info</a>
                    <div class="route-desc">Редирект на страницу автора</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/http_codes" class="route-path">/lab1/http_codes</a>
                    <div class="route-desc">Тестирование различных HTTP кодов ответов</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/bad_request" class="route-path">/lab1/bad_request</a>
                    <div class="route-desc">Тест кода 400 - Bad Request</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/unauthorized" class="route-path">/lab1/unauthorized</a>
                    <div class="route-desc">Тест кода 401 - Unauthorized</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/payment_required" class="route-path">/lab1/payment_required</a>
                    <div class="route-desc">Тест кода 402 - Payment Required</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/forbidden" class="route-path">/lab1/forbidden</a>
                    <div class="route-desc">Тест кода 403 - Forbidden</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/method_not_allowed" class="route-path">/lab1/method_not_allowed</a>
                    <div class="route-desc">Тест кода 405 - Method Not Allowed</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/teapot" class="route-path">/lab1/teapot</a>
                    <div class="route-desc">Тест кода 418 - I'm a teapot</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/lab1/server_error" class="route-path">/lab1/server_error</a>
                    <div class="route-desc">Тест кода 500 - Internal Server Error</div>
                </div>
            </div>
            
            <div class="route-item">
                <div>
                    <a href="/created" class="route-path">/created</a>
                    <div class="route-desc">Тест кода 201 - Created</div>
                </div>
            </div>
        </div>
        
        <div style="text-align: center;">
            <a href="/" class="button">На главную</a>
        </div>
    </div>
    {FOOTER}
</body>
</html>
'''

@app.route("/lab1/author")
def author():
    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>Об авторе</title>
        {COMMON_STYLES}
    </head>
    <body>
        <div class="container">
            <h1>Об авторе</h1>
            
            <div class="info-grid">
                <div class="info-card">
                    <h3>Личная информация</h3>
                    <p><strong>ФИО:</strong> Игуменшев Дмитрий Евгеньевич</p>
                    <p><strong>Группа:</strong> ФБИ-33</p>
                    <p><strong>Курс:</strong> 3 курс</p>
                </div>
                
                <div class="info-card">
                    <h3>Образование</h3>
                    <p><strong>Учебное заведение:</strong> НГТУ</p>
                    <p><strong>Факультет:</strong> ФБ</p>
                    <p><strong>Год:</strong> 2025</p>
                </div>
            </div>
            
            <div class="highlight">
                <p><strong>О проекте:</strong> Данный веб-сайт разработан в рамках изучения 
                WEB-программирования с использованием фреймворка Flask. Цель проекта — освоение 
                принципов работы веб-серверов и создание динамических веб-приложений.</p>
            </div>
            
            <div style="text-align: center;">
                <a href="/lab1" class="button">Назад к лабораторной работе 1</a>
                <a href="/" class="button">На главную</a>
            </div>
        </div>
        {FOOTER}
    </body>
</html>
'''

@app.route("/lab1/web")
def web():
    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>Web-сервер на Flask</title>
        {COMMON_STYLES}
    </head>
    <body>
        <div class="container">
            <h1>Web-сервер на Flask</h1>
            
            <div class="highlight">
                <p>Эта страница демонстрирует работу веб-сервера, построенного на фреймворке Flask.</p>
            </div>
            
            <div class="info-card">
                <h3>Заголовки ответа</h3>
                <p>Сервер возвращает следующие заголовки:</p>
                <div class="code">
                    X-Server: sample<br>
                    Content-Type: text/html; charset=utf-8
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="/lab1/author" class="button">Перейти к автору</a>
                <a href="/lab1" class="button">Назад</a>
            </div>
        </div>
        {FOOTER}
    </body>
</html>''', 200, {
    'X-Server': 'sample',
    'Content-Type': 'text/html; charset=utf-8'
}


@app.route('/lab1/image')
def image():
    path = url_for("static", filename="ocean.jpg")

    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">

        <title>Океан</title>
        {COMMON_STYLES}
    </head>
    <body>
        <div class="container">
            <h1>Изображение океана</h1>
            
            <div class="highlight">
                <p>Эта страница демонстрирует работу со статическими файлами в Flask.</p>
            </div>
            
            <img src="{path}" alt="Великолепный океан">
            
            <p>Океан — это непрерывная водная оболочка Земли, окружающая материки и острова. 
            Он играет crucial роль в формировании климата планеты и является домом для 
            бесчисленного множества видов живых организмов.</p>
            
            <div style="text-align: center;">
                <a href="/lab1" class="button">Назад к лабораторной работе 1</a>
            </div>
        </div>
        {FOOTER}
    </body>
</html>
''', 200, {
    'Content-Type': 'text/html; charset=utf-8',
    'Content-Language': 'ru',
    'X-Image-Description': 'Great Ocean View',
    'X-Server-Info': 'Flask Web Server v1.0',
    'Cache-Control': 'no-cache'
}

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    
    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>Счётчик посещений</title>
        {COMMON_STYLES}
    </head>
    <body>
        <div class="container">
            <h1>Счётчик посещений</h1>
            
            <div class="info-card">
                <h3>Статистика посещений</h3>
                <p><strong>Количество посещений:</strong> {count}</p>
                <p><strong>Дата и время:</strong> {time}</p>
                <p><strong>Запрошенный адрес:</strong> {url}</p>
                <p><strong>Ваш IP-адрес:</strong> {client_ip}</p>
            </div>
            
            <div class="highlight">
                <p>Эта страница использует глобальную переменную для подсчета количества посещений.</p>
            </div>
            
            <div style="text-align: center;">
                <a href="/lab1/reset_counter" class="button">Очистить счётчик</a>
                <a href="/lab1" class="button">Назад</a>
            </div>
        </div>
        {FOOTER}
    </body>
</html>
'''





@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>Счётчик очищен</title>
        {COMMON_STYLES}
    </head>
    <body>
        <div class="container">
            <h1>Счётчик очищен!</h1>
            
            <div class="highlight">
                <p>Счётчик посещений был успешно сброшен до нуля.</p>
            </div>
            
            <div style="text-align: center;">
                <a href="/lab1/counter" class="button">Вернуться на счётчик</a>
                <a href="/lab1" class="button">Назад</a>
            </div>
        </div>
        {FOOTER}
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/created")
def created():
    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>Создано успешно</title>
        {COMMON_STYLES}
    </head>
    <body>
        <div class="container">
            <h1>Создано успешно</h1>
            
            <div class="highlight">
                <p>Запрос был обработан успешно, и новый ресурс был создан.</p>
            </div>
            
            <p><em>Что-то важное было создано...</em></p>
            
            <div style="text-align: center;">
                <a href="/" class="button">На главную</a>
            </div>
        </div>
        {FOOTER}
    </body>
</html>
''', 201

@app.route('/lab1/http_codes')
def http_codes():
    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>HTTP коды ответов</title>
        {COMMON_STYLES}
    </head>
    <body>
        <div class="container">
            <h1>Тестирование HTTP кодов ответов</h1>
            
            <div class="highlight">
                <p>Выберите код для тестирования. Каждая страница вернет соответствующий HTTP статус код.</p>
            </div>
            
            <div class="info-grid">
                <div class="info-card">
                    <h3>4xx - Ошибки клиента</h3>
                    <ul>
                        <li><a href="/lab1/bad_request">400 - Bad Request</a> - Неверный запрос</li>
                        <li><a href="/lab1/unauthorized">401 - Unauthorized</a> - Неавторизован</li>
                        <li><a href="/lab1/payment_required">402 - Payment Required</a> - Необходима оплата</li>
                        <li><a href="/lab1/forbidden">403 - Forbidden</a> - Запрещено</li>
                        <li><a href="/lab1/method_not_allowed">405 - Method Not Allowed</a> - Метод не разрешен</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>5xx - Ошибки сервера</h3>
                    <ul>
                        <li><a href="/lab1/server_error">500 - Internal Server Error</a> - Внутренняя ошибка сервера</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>Специальные коды</h3>
                    <ul>
                        <li><a href="/lab1/teapot">418 - I'm a teapot</a> - Я - чайник</li>
                    </ul>
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="/lab1" class="button">Назад к лабораторной работе 1</a>
            </div>
        </div>
        {FOOTER}
    </body>
</html>
'''


@app.route('/lab1/bad_request')
def bad_request():
    return '''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>400 Bad Request</title>
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Неверный запрос</p>
        <hr>
        <p><a href="/">На главную</a></p>
    </body>
</html>
''', 400


@app.route('/lab1/unauthorized')
def unauthorized():
    return '''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация для доступа к ресурсу.</p>
        <hr>
        <p><a href="/">На главную</a></p>
    </body>
</html>
''', 401


@app.route('/lab1/payment_required')
def payment_required():
    return '''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Необходима оплата</p>
        <hr>
        <p><a href="/">На главную</a></p>
    </body>
</html>
''', 402


@app.route('/lab1/forbidden')
def forbidden():
    return '''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ запрещен</p>
        <hr>
        <p><a href="/">На главную</a></p>
    </body>
</html>
''', 403


@app.route('/lab1/method_not_allowed')
def method_not_allowed():
    return '''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод не разрешен</p>
        <hr>
        <p><a href="/">На главную</a></p>
    </body>
</html>
''', 405


@app.route('/lab1/teapot')
def teapot():
    return '''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я - чайник</p>
        <hr>
        <p><a href="/">На главную</a></p>
    </body>
</html>
''', 418


if __name__ == '__main__':
    app.run(debug=False)

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]
    
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка:  {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Дмитрий Игуменшев'
    return render_template('example.html')
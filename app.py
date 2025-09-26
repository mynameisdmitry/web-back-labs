from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

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
            
            <p>Кажется, эта страница отправилась в собственное приключение и не может найти дорогу назад.</p>
            
            <div class="quote">
                "Иногда заблудиться - значит найти нечто большее, чем искал"
            </div>
            
            <p>Но не беспокойтесь! Пока страница ищет свой путь, вы можете вернуться в безопасную гавань главной страницы.</p>
            
            <div style="text-align: center;">
                <a href="/" class="button">Вернуться на главную</a>
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

        <div style="text-align: center; margin-top: 30px;">
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
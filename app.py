from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)


FOOTER = '''
<footer style="position:fixed; left:0; bottom:0; width:100%; padding:10px 0; background-color:#f0f0f0; color:#333; text-align:center; box-shadow:0 -1px 4px rgba(0,0,0,0.08);">
    Игуменшев Дмитрий Евгеньевич, ФБИ-33, 3 курс, 2025 год
</footer>
'''

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404


@app.route("/")
@app.route("/index")
def index():
    return f"""
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <style>body {{ margin:0; font-family: Arial, sans-serif; }}</style>
    </head>
    <body>
        <header>
            <h1 style="padding:20px; text-align:center;">НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <main style="padding:20px;">
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
        </main>
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
    <style>
        body {{ font-family: Arial, sans-serif; text-align:center; margin:0; padding:20px; }}
        a {{ text-decoration: none; color: blue; margin: 0 10px; }}
    </style>
</head>
<body>
    <h1>Лабораторная работа 1</h1>
    <p>
        Flask — фреймворк для создания веб-приложений на языке программирования Python,
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2.
        Относится к категории так называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
    </p>
    
    <nav>
        <a href="/lab1/author">Author</a> |
        <a href="/lab1/web">Web</a> |
        <a href="/lab1/image">Image</a> |
        <a href="/lab1/counter">Counter</a> |
        <a href="/lab1/http_codes">HTTP коды</a>
    </nav>

    <p><a href="/">На главную</a></p>
    {FOOTER}
</body>
</html>
'''


@app.route("/lab1/web")
def web():
    body = f"""<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>Web-сервер на Flask</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; margin: 0; padding-bottom:70px; }}
            footer {{ margin-top: 50px; padding: 10px; background-color: #f0f0f0; color: #333; }}
        </style>
    </head>
    <body>
        <h1>web-сервер на flask</h1>
        <a href="/lab1/author">author</a>
        {FOOTER}
    </body>
</html>"""
    return body, 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/html; charset=utf-8'
    }


@app.route('/lab1/image')
def image():
    path = url_for("static", filename="ocean.jpg")
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <title>Океан</title>
    </head>
    <body style="padding-bottom:80px;">
        <h1>Океан</h1>
        <img src="{path}" alt="ocean">
        {FOOTER}
    </body>
</html>
'''


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
        <title>Счётчик</title>
    </head>
    <body style="padding:20px; padding-bottom:80px;">
        Сколько раз вы сюда заходили: {count}
        <hr>
        Дата и время: {time}<br>
        Запрошенный адрес: {url}<br>
        Ваш IP-адрес: {client_ip}<br>
        <p><a href="/lab1/reset_counter">Очистить счётчик</a></p>
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
        <title>Создано</title>
    </head>
    <body style="padding-bottom:80px;">
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
        {FOOTER}
    </body>
</html>
''', 201


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
    </head>
    <body style="padding-bottom:80px;">
        <h1>Счётчик очищен!</h1>
        <a href="/lab1/counter">Вернуться на счётчик</a>
        {FOOTER}
    </body>
</html>
'''


# Новые маршруты для HTTP кодов ответов
@app.route('/lab1/http_codes')
def http_codes():
    return f'''
<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>HTTP коды ответов</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; padding-bottom: 80px; }}
            .code-list {{ list-style-type: none; padding: 0; }}
            .code-list li {{ margin: 10px 0; }}
            .code-list a {{ text-decoration: none; color: #0066cc; font-weight: bold; }}
            .code-list a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>Тестирование HTTP кодов ответов</h1>
        <p>Выберите код для тестирования:</p>
        <ul class="code-list">
            <li><a href="/lab1/bad_request">400 - Bad Request</a> - Неверный запрос</li>
            <li><a href="/lab1/unauthorized">401 - Unauthorized</a> - Неавторизован</li>
            <li><a href="/lab1/payment_required">402 - Payment Required</a> - Необходима оплата</li>
            <li><a href="/lab1/forbidden">403 - Forbidden</a> - Запрещено</li>
            <li><a href="/lab1/method_not_allowed">405 - Method Not Allowed</a> - Метод не разрешен</li>
            <li><a href="/lab1/teapot">418 - I'm a teapot</a> - Я - чайник</li>
        </ul>
        <p><a href="/lab1">← Назад к лабораторной работе 1</a></p>
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
    app.run(debug=True)
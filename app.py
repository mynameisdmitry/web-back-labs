from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

# Универсальный подвал — будет добавлен внизу каждой страницы
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
    return f"""<!doctype html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>Лабораторная 1</title>
        <style>body {{ margin:0; font-family: Arial, sans-serif; }}</style>
    </head>
    <body>
        <main style="padding:20px;">
            <h1>Лабораторная работа 1</h1>
            <ul>
                <li><a href="/lab1/author">author</a></li>
                <li><a href="/lab1/web">web</a></li>
                <li><a href="/lab1/image">image</a></li>
                <li><a href="/lab1/counter">counter</a></li>
            </ul>
        </main>
        {FOOTER}
    </body>
</html>"""


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


if __name__ == '__main__':
    app.run(debug=True)
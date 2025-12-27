from flask import Blueprint, url_for, request, redirect, render_template
import datetime

lab1 = Blueprint('lab1', __name__)

# Глобальный счётчик посещений
count = 0


@lab1.route('/lab1/server_error')
def server_error():
    result = 10 / 0
    return "Эта строка никогда не выполнится"


@lab1.route("/lab1/")
def lab():
    routes = [
        {'path': '/', 'description': 'Главная страница со списком лабораторных работ'},
        {'path': '/index', 'description': 'Альтернативный адрес главной страницы'},
        {'path': '/lab1', 'description': 'Основная страница лабораторной работы 1'},
        {'path': '/lab1/author', 'description': 'Страница с информацией об авторе'},
        {'path': '/lab1/web', 'description': 'Демонстрация работы веб-сервера с кастомными заголовками'},
        {'path': '/lab1/image', 'description': 'Страница с изображением океана и дополнительными заголовками'},
        {'path': '/lab1/counter', 'description': 'Счётчик посещений с информацией о клиенте'},
        {'path': '/lab1/reset_counter', 'description': 'Сброс счётчика посещений'},
        {'path': '/lab1/info', 'description': 'Редирект на страницу автора'},
        {'path': '/lab1/http_codes', 'description': 'Тестирование различных HTTP кодов ответов'},
        {'path': '/lab1/bad_request', 'description': 'Тест кода 400 - Bad Request'},
        {'path': '/lab1/unauthorized', 'description': 'Тест кода 401 - Unauthorized'},
        {'path': '/lab1/payment_required', 'description': 'Тест кода 402 - Payment Required'},
        {'path': '/lab1/forbidden', 'description': 'Тест кода 403 - Forbidden'},
        {'path': '/lab1/method_not_allowed', 'description': 'Тест кода 405 - Method Not Allowed'},
        {'path': '/lab1/teapot', 'description': 'Тест кода 418 - I''m a teapot'},
        {'path': '/lab1/server_error', 'description': 'Тест кода 500 - Internal Server Error'},
        {'path': '/created', 'description': 'Тест кода 201 - Created'},
    ]
    return render_template('lab1/lab1.html', routes=routes)


@lab1.route("/lab1/author")
def author():
    return render_template('lab1/author.html')


@lab1.route("/lab1/web")
def web():
    return render_template('lab1/web.html'), 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/html; charset=utf-8'
    }


@lab1.route('/lab1/image')
def image():
    return render_template('lab1/image.html'), 200, {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Language': 'ru',
        'X-Image-Description': 'Great Ocean View',
        'X-Server-Info': 'Flask Web Server v1.0',
        'Cache-Control': 'no-cache'
    }


@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url_path = request.url
    client_ip = request.remote_addr
    
    return render_template('lab1/counter.html', 
                         count=count, 
                         time=time, 
                         url=url_path, 
                         client_ip=client_ip)


@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return render_template('lab1/reset_counter.html')


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/created")
def created():
    return render_template('lab1/created.html'), 201


@lab1.route('/lab1/http_codes')
def http_codes():
    return render_template('lab1/http_codes.html')


@lab1.route('/lab1/bad_request')
def bad_request():
    return render_template('lab1/error.html', 
                         code=400, 
                         title='Bad Request', 
                         message='Неверный запрос'), 400


@lab1.route('/lab1/unauthorized')
def unauthorized():
    return render_template('lab1/error.html', 
                         code=401, 
                         title='Unauthorized', 
                         message='Требуется аутентификация для доступа к ресурсу.'), 401


@lab1.route('/lab1/payment_required')
def payment_required():
    return render_template('lab1/error.html', 
                         code=402, 
                         title='Payment Required', 
                         message='Необходима оплата'), 402


@lab1.route('/lab1/forbidden')
def forbidden():
    return render_template('lab1/error.html', 
                         code=403, 
                         title='Forbidden', 
                         message='Доступ запрещен'), 403


@lab1.route('/lab1/method_not_allowed')
def method_not_allowed():
    return render_template('lab1/error.html', 
                         code=405, 
                         title='Method Not Allowed', 
                         message='Метод не разрешен'), 405


@lab1.route('/lab1/teapot')
def teapot():
    return render_template('lab1/error.html', 
                         code=418, 
                         title="I'm a teapot", 
                         message='Я - чайник'), 418

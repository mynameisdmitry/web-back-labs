from flask import Flask, url_for, request
import datetime
app = Flask(__name__)

@app.route("/")

@app.route("/lab1")
def lab1():
    return """<!doctype html>
        <html>
            <body>
                <ul>
                    <h1>Лабораторная работа 1</h1>
                    <li><a href="/author">author</a></li>
                    <li><a href="/web">web</a></li>
                    <li><a href="/image">image</a></li>
                    <li><a href="/counter">counter</a></li>
                </ul>
            </body>
        </html>"""    

@app.route("/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/author">author</a>
            </body>
        </html>"""

@app.route("/author")
def author():
    name = "Игуменшев Дмитрий Евгеньевич"
    group = "ФБИ-33"
    faculty = "ФБ"
    
    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route('/image') 
def image():
    path = url_for("static", filename="ocean.jpg")
    return '''
<!doctype html>
<html>
    <body>
        <h1>Океан</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''

count = 0

@app.route('/counter') 
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
    </body>
</html>
'''
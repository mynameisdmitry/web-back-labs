from flask import Blueprint, url_for, request, redirect, abort, render_template

lab2 = Blueprint('lab2', __name__)

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

@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330},
    {'name': 'георгин', 'price': 300},
    {'name': 'гладиолус', 'price': 310}
]
    

@lab2.route('/lab2/flowers')
def all_flowers():
    """Страница со списком всех цветов"""
    return render_template('flowers.html', flowers=flower_list)

@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    """Добавление нового цветка с ценой по умолчанию"""
    flower_list.lab2end({'name': name, 'price': 300})
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Цветок добавлен</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .success {{ background: #e8f5e8; padding: 20px; border-radius: 10px; color: #2e7d32; }}
            .flower-list {{ background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; }}
            .button {{ display: inline-block; padding: 10px 20px; background: #4caf50; color: white; text-decoration: none; border-radius: 5px; margin: 10px 5px; }}
        </style>
    </head>
    <body>
        <h1>Цветок успешно добавлен!</h1>
        
        <div class="success">
            <h2>Название нового цветка: <em>{name}</em></h2>
            <p>Цветок был добавлен в коллекцию под ID: {len(flower_list) - 1}</p>
        </div>

        <div class="flower-list">
            <h3>Текущая коллекция цветов:</h3>
            <p><strong>Всего цветов:</strong> {len(flower_list)}</p>
            <ol>
                {''.join(f'<li>{flower}' + (' <strong>← новый!</strong>' if i == len(flower_list)-1 else '') + '</li>' for i, flower in enumerate(flower_list))}
            </ol>
        </div>

        <div>
            <a href="/lab2/flowers" class="button">Посмотреть все цветы</a>
            <a href="/lab2/add_flower/роза" class="button">Добавить ещё цветок</a>
            <a href="/lab2" class="button">Назад к лабораторной 2</a>
        </div>
    </body>
    </html>
'''


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        abort(404)
    else:
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Цветок #{flower_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .flower-card {{ background: linear-gradient(135deg, #ffebee, #fce4ec); padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0; }}
                .flower-name {{ font-size: 2em; color: #d32f2f; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 10px 20px; background: #2196f3; color: white; text-decoration: none; border-radius: 5px; margin: 10px 5px; }}
                .nav {{ margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1>Информация о цветке</h1>
            
            <div class="flower-card">
                <div class="flower-name">{flower_list[flower_id]}</div>
                <p><strong>ID:</strong> {flower_id}</p>
                <p><strong>Позиция в списке:</strong> {flower_id + 1} из {len(flower_list)}</p>
            </div>

            <div class="nav">
                {f'<a href="/lab2/flowers/{flower_id - 1}" class="button">← Предыдущий цветок</a>' if flower_id > 0 else ''}
                {f'<a href="/lab2/flowers/{flower_id + 1}" class="button">Следующий цветок →</a>' if flower_id < len(flower_list) - 1 else ''}
            </div>

            <div>
                <a href="/lab2/flowers" class="button">Посмотреть все цветы</a>
                <a href="/lab2" class="button">Назад к лабораторной 2</a>
            </div>
        </body>
        </html>
        '''


@lab2.route('/lab2/example')
def example():
    name = 'Дмитрий Игуменшев'
    group = 'ФБИ-33'
    course = '3 курс'
    number = '2'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
    ]
    return render_template('example.html', 
                        name=name, number=number, group=group, 
                        course=course, fruits=fruits)

@lab2.route('/lab2/')
def lab22():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    """Удаление всех цветов"""
    global flower_list
    flower_list.clear()
    return redirect('/lab2/flowers')

@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    """Удаление цветка по номеру"""
    if flower_id >= len(flower_list) or flower_id < 0:
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/flowers')

@lab2.route('/lab2/add_flower/')
def add_flower_form():
    """Обработка добавления цветка из формы"""
    name = request.args.get('name', '').strip()
    if not name:
        return f'''
        <!doctype html>
        <html>
        <head>
            <title>Ошибка</title>
            <link rel="icon" href="{url_for('static', filename='favicon.ico')}" type="image/x-icon">
        </head>
        <body>
            <h1>Ошибка: не указано название цветка</h1>
            <a href="/lab2/flowers">Вернуться к списку цветов</a>
        </body>
        </html>
        ''', 400
    
    flower_list.lab2end({'name': name, 'price': 300})
    return redirect('/lab2/flowers')

@lab2.route('/lab2/calc/')
def calc_default():
    """Перенаправление на /lab2/calc/1/1"""
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    """Перенаправление на /lab2/calc/a/1"""
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    """Страница с математическими операциями над двумя числами"""
    return render_template('calc.html', a=a, b=b)

books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказы', 'pages': 350},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 128}
]

@lab2.route('/lab2/books')
def books_list():
    "Страница со списком книг"
    return render_template('books.html', books=books)

berries = [
    {'name': 'Клубника', 'description': 'Сочная красная ягода с сладким вкусом', 'image': 'Клубника.jpg'},
    {'name': 'Малина', 'description': 'Нежная ароматная ягода красного цвета', 'image': 'Малина.jpg'},
    {'name': 'Черника', 'description': 'Маленькая тёмно-синяя ягода с насыщенным вкусом', 'image': 'Черника.jpg'},
    {'name': 'Ежевика', 'description': 'Тёмная ягода с кисло-сладким вкусом', 'image': 'Ежевика.jpg'},
    {'name': 'Смородина', 'description': 'Бывает красная, чёрная и белая, с характерной кислинкой', 'image': 'Смородина.jpg'},
    {'name': 'Крыжовник', 'description': 'Зелёная или красная ягода с освежающим вкусом', 'image': 'Крыжовник.jpg'},
    {'name': 'Земляника', 'description': 'Лесная ягода с интенсивным ароматом', 'image': 'Земляника.jpg'},
    {'name': 'Брусника', 'description': 'Красная ягода с горьковатым привкусом', 'image': 'Брусника.jpg'},
    {'name': 'Клюква', 'description': 'Красная кислая ягода, растущая на болотах', 'image': 'Клюква.jpg'},
    {'name': 'Облепиха', 'description': 'Оранжевая ягода с высоким содержанием витаминов', 'image': 'Облепиха.jpg'},
    {'name': 'Виноград', 'description': 'Сладкие ягоды, растущие гроздьями', 'image': 'Виноград.jpg'},
    {'name': 'Вишня', 'description': 'Тёмно-красная ягода с кисло-сладким вкусом', 'image': 'Вишня.jpeg'},
    {'name': 'Черешня', 'description': 'Сладкая ягода, близкий родственник вишни', 'image': 'Черешня.jpg'},
    {'name': 'Шелковица', 'description': 'Сладкие ягоды белого, красного или чёрного цвета', 'image': 'Шелковица.jpg'},
    {'name': 'Голубика', 'description': 'Синяя ягода, похожая на чернику, но крупнее', 'image': 'Голубика.jpg'},
    {'name': 'Арония', 'description': 'Чёрноплодная рябина с терпким вкусом', 'image': 'Арония.jpg'},
    {'name': 'Ирга', 'description': 'Сине-чёрные сладкие ягоды', 'image': 'Ирга.jpg'},
    {'name': 'Жимолость', 'description': 'Синие продолговатые ягоды с оригинальным вкусом', 'image': 'Жимолость.jpg'},
    {'name': 'Калина', 'description': 'Красные горьковатые ягоды', 'image': 'Калина.jpg'},
    {'name': 'Рябина', 'description': 'Оранжево-красные ягоды с горьким вкусом', 'image': 'Рябина.jpg'}
]

@lab2.route('/lab2/berries')
def berries_list():
    "Страница со списком ягод"
    return render_template('berries.html', berries=berries)
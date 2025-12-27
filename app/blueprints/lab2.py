from flask import Blueprint, url_for, request, redirect, abort, render_template

lab2 = Blueprint('lab2', __name__)

# Список цветов
flower_list = [
    {'name': 'роза', 'price': 350},
    {'name': 'тюльпан', 'price': 200},
    {'name': 'незабудка', 'price': 150},
    {'name': 'ромашка', 'price': 180},
]


@lab2.route('/lab2/flowers')
def all_flowers():
    """Страница со списком всех цветов"""
    return render_template('lab2/flowers.html', flowers=flower_list)


@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    """Добавление нового цветка с ценой по умолчанию"""
    flower_list.append({'name': name, 'price': 300})
    return render_template('lab2/add_flower.html', 
                         flower_name=name,
                         flower_id=len(flower_list) - 1,
                         total_flowers=len(flower_list),
                         flowers=flower_list)


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        abort(404)
    return render_template('lab2/flower_detail.html',
                         flower=flower_list[flower_id],
                         flower_id=flower_id,
                         total_flowers=len(flower_list))


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
    return render_template('lab2/example.html', 
                        name=name, number=number, group=group, 
                        course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab22():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


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
        return render_template('lab2/add_flower_error.html'), 400
    
    flower_list.append({'name': name, 'price': 300})
    return redirect('/lab2/flowers')


@lab2.route('/lab2/calc/')
@lab2.route('/lab2/calc/<int:a>/')
@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a=1, b=1):
    return render_template('lab2/calc.html', a=a, b=b)


@lab2.route('/lab2/books')
def books():
    books = [
        {'author': 'Достоевский Ф.М.', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
        {'author': 'Толстой Л.Н.', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1300},
        {'author': 'Пушкин А.С.', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 384},
        {'author': 'Булгаков М.А.', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
        {'author': 'Чехов А.П.', 'title': 'Вишневый сад', 'genre': 'Пьеса', 'pages': 96},
        {'author': 'Гоголь Н.В.', 'title': 'Мертвые души', 'genre': 'Поэма', 'pages': 352},
        {'author': 'Тургенев И.С.', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 256},
        {'author': 'Лермонтов М.Ю.', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 192},
        {'author': 'Шолохов М.А.', 'title': 'Тихий Дон', 'genre': 'Роман-эпопея', 'pages': 1200},
        {'author': 'Солженицын А.И.', 'title': 'Один день Ивана Денисовича', 'genre': 'Рассказ', 'pages': 176},
    ]
    return render_template('lab2/books.html', books=books)


@lab2.route('/lab2/berries')
def berries():
    berries = [
        {
            'name': 'Клубника',
            'description': 'Садовая земляника крупноплодная',
            'image': url_for('static', filename='Клубника.jpg')
        },
        {
            'name': 'Малина',
            'description': 'Многолетнее растение семейства розовых',
            'image': url_for('static', filename='Малина.jpg')
        },
        {
            'name': 'Черника',
            'description': 'Низкорослый кустарничек из семейства вересковых',
            'image': url_for('static', filename='Черника.jpg')
        },
        {
            'name': 'Смородина',
            'description': 'Листопадный кустарник, ягодная культура',
            'image': url_for('static', filename='Смородина.jpg')
        },
        {
            'name': 'Крыжовник',
            'description': 'Многолетний, многоствольный кустарник',
            'image': url_for('static', filename='Крыжовник.jpg')
        },
    ]
    return render_template('lab2/berries.html', berries=berries)

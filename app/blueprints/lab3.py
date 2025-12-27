from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name = name if name else "Аноним"
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    age = age if age else "Неизвестно"
    return render_template('/lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    
    sex = request.args.get('sex')
    
    if user and age and not errors:
        return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)
    else:
        return render_template('lab3/form1.html', user=None, age=age, sex=sex, errors=errors)
    

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    background_color = request.args.get('background_color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')
    
    if color or background_color or font_size or font_family:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if background_color:
            resp.set_cookie('background_color', background_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_family:
            resp.set_cookie('font_family', font_family)
        return resp
    
    color = request.cookies.get('color', '#000000')
    background_color = request.cookies.get('background_color', '#414344')
    font_size = request.cookies.get('font_size', '14')
    font_family = request.cookies.get('font_family', 'Arial, sans-serif')
    
    return render_template('lab3/settings.html', 
                         color=color,
                         background_color=background_color,
                         font_size=font_size,
                         font_family=font_family)

@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('background_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_family')
    return resp


@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')

    if fio and shelf and age and departure and destination and date:
        if not fio.strip():
            errors['fio'] = 'Заполните ФИО пассажира'
        
        try:
            age_int = int(age)
            if age_int < 1 or age_int > 120:
                errors['age'] = 'Возраст должен быть от 1 до 120 лет'
        except ValueError:
            errors['age'] = 'Возраст должен быть числом'
        
        if not departure.strip():
            errors['departure'] = 'Заполните пункт выезда'
        
        if not destination.strip():
            errors['destination'] = 'Заполните пункт назначения'
        
        if not date:
            errors['date'] = 'Выберите дату поездки'

        if not errors:
            return render_template('lab3/ticket_result.html',
                                 fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                                 age=age, departure=departure, destination=destination,
                                 date=date, insurance=insurance)
    
    return render_template('lab3/ticket.html', errors=errors,
                         fio=fio or '', shelf=shelf or '', linen=linen or '',
                         baggage=baggage or '', age=age or '', departure=departure or '',
                         destination=destination or '', date=date or '', insurance=insurance or '')



products = [
    {'name': 'Война и мир', 'price': 1339, 'brand': 'Лев Толстой', 'color': 'Коричневый', 'storage': 'Твердый переплет'},
    {'name': 'Преступление и наказание', 'price': 629, 'brand': 'Федор Достоевский', 'color': 'Темно-синий', 'storage': 'Мягкая обложка'},
    {'name': 'Мастер и Маргарита', 'price': 799, 'brand': 'Михаил Булгаков', 'color': 'Черный', 'storage': 'Твердый переплет'},
    {'name': '1984', 'price': 569, 'brand': 'Джордж Оруэлл', 'color': 'Серый', 'storage': 'Твердый переплет'},
    {'name': 'Три товарища', 'price': 699, 'brand': 'Эрих Мария Ремарк', 'color': 'Бежевый', 'storage': 'Твердый переплет'},
    {'name': 'Анна Каренина', 'price': 499, 'brand': 'Лев Толстой', 'color': 'Красный', 'storage': 'Мягкая обложка'},
    {'name': 'Сто лет одиночества', 'price': 599, 'brand': 'Габриэль Гарсиа Маркес', 'color': 'Зеленый', 'storage': 'Твердый переплет'},
    {'name': 'Маленький принц', 'price': 299, 'brand': 'Антуан де Сент-Экзюпери', 'color': 'Голубой', 'storage': 'Мягкая обложка'},
    {'name': 'Гарри Поттер и философский камень', 'price': 899, 'brand': 'Джоан Роулинг', 'color': 'Черный', 'storage': 'Твердый переплет'},
    {'name': 'Властелин колец', 'price': 1299, 'brand': 'Джон Р. Р. Толкин', 'color': 'Золотой', 'storage': 'Подарочное издание'},
    {'name': 'Шерлок Холмс', 'price': 679, 'brand': 'Артур Конан Дойл', 'color': 'Темно-коричневый', 'storage': 'Сборник'},
    {'name': 'Гордость и предубеждение', 'price': 449, 'brand': 'Джейн Остин', 'color': 'Розовый', 'storage': 'Мягкая обложка'},
    {'name': 'Улисс', 'price': 999, 'brand': 'Джеймс Джойс', 'color': 'Синий', 'storage': 'Твердый переплет'},
    {'name': 'Лолита', 'price': 579, 'brand': 'Владимир Набоков', 'color': 'Фиолетовый', 'storage': 'Твердый переплет'},
    {'name': 'Великий Гэтсби', 'price': 419, 'brand': 'Фрэнсис Скотт Фицджеральд', 'color': 'Золотой', 'storage': 'Твердый переплет'},
    {'name': 'Над пропастью во ржи', 'price': 329, 'brand': 'Джером Сэлинджер', 'color': 'Желтый', 'storage': 'Мягкая обложка'},
    {'name': 'Атлант расправил плечи', 'price': 1999, 'brand': 'Айн Рэнд', 'color': 'Серебряный', 'storage': 'Три тома'},
    {'name': 'Код да Винчи', 'price': 449, 'brand': 'Дэн Браун', 'color': 'Красный', 'storage': 'Мягкая обложка'},
    {'name': 'Игра престолов', 'price': 899, 'brand': 'Джордж Мартин', 'color': 'Темно-серый', 'storage': 'Твердый переплет'},
    {'name': 'Дюна', 'price': 759, 'brand': 'Фрэнк Герберт', 'color': 'Песочный', 'storage': 'Твердый переплет'}
]

@lab3.route('/lab3/products')
def products_search():
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    all_prices = [product['price'] for product in products]
    real_min_price = min(all_prices)
    real_max_price = max(all_prices)
    
    min_price_input = request.args.get('min_price', '')
    max_price_input = request.args.get('max_price', '')

    if 'reset' in request.args:
        resp = make_response(render_template('lab3/products.html',
                                           products=products,
                                           min_price='',
                                           max_price='',
                                           real_min_price=real_min_price,
                                           real_max_price=real_max_price,
                                           filtered_count=len(products),
                                           total_count=len(products)))
        resp.set_cookie('min_price', '', expires=0)
        resp.set_cookie('max_price', '', expires=0)
        return resp
    
    if min_price_input or max_price_input:
        min_price = int(min_price_input) if min_price_input else real_min_price
        max_price = int(max_price_input) if max_price_input else real_max_price
        
        if min_price > max_price:
            min_price, max_price = max_price, min_price
        
        filtered_products = [
            product for product in products 
            if min_price <= product['price'] <= max_price
        ]
        
        resp = make_response(render_template('lab3/products.html',
                                           products=filtered_products,
                                           min_price=min_price,
                                           max_price=max_price,
                                           real_min_price=real_min_price,
                                           real_max_price=real_max_price,
                                           filtered_count=len(filtered_products),
                                           total_count=len(products)))
        resp.set_cookie('min_price', str(min_price), max_age=60*60*24*30)
        resp.set_cookie('max_price', str(max_price), max_age=60*60*24*30)
        return resp
    
    if min_price_cookie and max_price_cookie:
        min_price = int(min_price_cookie)
        max_price = int(max_price_cookie)
        
        filtered_products = [
            product for product in products 
            if min_price <= product['price'] <= max_price
        ]
        
        return render_template('lab3/products.html',
                             products=filtered_products,
                             min_price=min_price,
                             max_price=max_price,
                             real_min_price=real_min_price,
                             real_max_price=real_max_price,
                             filtered_count=len(filtered_products),
                             total_count=len(products))
    
    return render_template('lab3/products.html',
                         products=products,
                         min_price='',
                         max_price='',
                         real_min_price=real_min_price,
                         real_max_price=real_max_price,
                         filtered_count=len(products),
                         total_count=len(products))
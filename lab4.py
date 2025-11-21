from flask import Blueprint, render_template, request, redirect
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div', methods=['GET', 'POST'])
def div_form():
    if request.method == 'GET':
        return render_template('lab4/div.html')
    
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = float(x1)
        x2 = float(x2)
    except ValueError:
        return render_template('lab4/div.html', error='Оба поля должны содержать числа!')
    
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum', methods=['GET', 'POST'])
def sum_form():
    if request.method == 'GET':
        return render_template('lab4/sum.html')
    
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    try:
        x1 = float(x1) if x1 != '' else 0.0
        x2 = float(x2) if x2 != '' else 0.0
    except ValueError:
        return render_template('lab4/sum.html', error='Поля должны содержать числа!')
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub', methods=['GET', 'POST'])
def sub_form():
    if request.method == 'GET':
        return render_template('lab4/sub.html')
    
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = float(x1)
        x2 = float(x2)
    except ValueError:
        return render_template('lab4/sub.html', error='Оба поля должны содержать числа!')
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul', methods=['GET', 'POST'])
def mul_form():
    if request.method == 'GET':
        return render_template('lab4/mul.html')
    
    x1 = request.form.get('x1', '1')
    x2 = request.form.get('x2', '1')
    
    try:
        x1 = float(x1) if x1 != '' else 1.0
        x2 = float(x2) if x2 != '' else 1.0
    except ValueError:
        return render_template('lab4/mul.html', error='Поля должны содержать числа!')
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow', methods=['GET', 'POST'])
def pow_form():
    if request.method == 'GET':
        return render_template('lab4/pow.html')
    
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = float(x1)
        x2 = float(x2)
    except ValueError:
        return render_template('lab4/pow.html', error='Оба поля должны содержать числа!')
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Ноль в степени ноль не определен!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count = 0
MAX_TREES = 10

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees=MAX_TREES)

    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < MAX_TREES:
        tree_count += 1

    return redirect('/lab4/tree')

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("lab4/login.html", authorized=False)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if login == 'alex' and password == '123':
        return render_template('/lab4/login.html', login=login, authorized=True)
    
    error = 'Неверный логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False)
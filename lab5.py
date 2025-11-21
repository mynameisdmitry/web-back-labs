from flask import Blueprint, render_template
import os

lab5 = Blueprint('lab5', __name__)

@lab5.route('/')
def main():
    print("Рендерим шаблон lab5.html")
    print("Путь к шаблону:", os.path.join('templates', 'lab5', 'lab5.html'))
    print("Файл существует:", os.path.exists(os.path.join('templates', 'lab5', 'lab5.html')))
    return render_template('lab5/lab5.html', username='anonymous')

@lab5.route('/login')
def login():
    return "Страница входа"

@lab5.route('/register')
def register():
    return "Страница регистрации"

@lab5.route('/list')
def list_articles():
    return "Список статей"

@lab5.route('/create')
def create_article():
    return "Создание статьи"
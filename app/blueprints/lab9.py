# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session, jsonify, redirect
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import Users
import random

lab9 = Blueprint("lab9", __name__)

# Хранилище открытых подарков (в реальном приложении использовать БД)
OPENED_GIFTS = set()

GIFTS = [
    {"id": 1, "message": "🎄 С Новым Годом! Желаю счастья, здоровья и успехов!", "image": "🎁", "auth_required": False},
    {"id": 2, "message": "✨ Пусть этот год принесёт море радости и улыбок!", "image": "⭐", "auth_required": False},
    {"id": 3, "message": "🎉 Исполнения всех желаний и новых достижений!", "image": "🎊", "auth_required": False},
    {"id": 4, "message": "🌟 Пусть удача сопутствует во всех начинаниях!", "image": "💫", "auth_required": False},
    {"id": 5, "message": "🎈 Радости, любви и тепла в Новом Году!", "image": "❤️", "auth_required": False},
    {"id": 6, "message": "🎀 Пусть сбудутся самые заветные мечты!", "image": "💝", "auth_required": True},
    {"id": 7, "message": "🎊 Здоровья, благополучия и процветания!", "image": "🌺", "auth_required": True},
    {"id": 8, "message": "💫 Ярких эмоций и незабываемых моментов!", "image": "🎆", "auth_required": True},
    {"id": 9, "message": "🌈 Пусть каждый день будет наполнен счастьем!", "image": "☀️", "auth_required": True},
    {"id": 10, "message": "🎵 Гармонии, вдохновения и творческих успехов!", "image": "🎼", "auth_required": True},
]


def generate_gift_positions():
    """Генерация позиций для подарков с равномерным распределением"""
    
    # Заранее определённые базовые позиции для 10 подарков
    # Распределены равномерно по всей области (с учетом размера подарков ~10%)
    base_positions = [
        # Верхний ряд (3 подарка)
        {'left': 12, 'top': 18},
        {'left': 45, 'top': 15},
        {'left': 78, 'top': 18},
        # Средний ряд (4 подарка)
        {'left': 5, 'top': 48},
        {'left': 30, 'top': 45},
        {'left': 55, 'top': 48},
        {'left': 80, 'top': 45},
        # Нижний ряд (3 подарка)
        {'left': 18, 'top': 75},
        {'left': 48, 'top': 78},
        {'left': 75, 'top': 75},
    ]
    
    positions = []
    
    # Перемешиваем базовые позиции
    shuffled_bases = base_positions.copy()
    random.shuffle(shuffled_bases)
    
    for base in shuffled_bases:
        # Добавляем небольшое случайное смещение для естественности
        # Ограничиваем позиции, чтобы не выходили за границы
        left = base['left'] + random.uniform(-4, 4)
        top = base['top'] + random.uniform(-3, 3)
        
        # Гарантируем, что подарки не выйдут за границы (с учетом их размера ~12%)
        left = max(3, min(85, left))
        top = max(8, min(82, top))
        
        position = {
            'left': left,
            'top': top,
            'rotation': random.uniform(-8, 8)
        }
        positions.append(position)
    
    return positions


@lab9.route('/lab9/')
def main():
    """Главная страница с новогодними подарками"""
    if 'opened_count' not in session:
        session['opened_count'] = 0
    
    # Генерируем позиции подарков один раз для сессии
    # Можно сбросить добавив параметр ?reset=1
    if 'gift_positions' not in session or request.args.get('reset'):
        session['gift_positions'] = generate_gift_positions()
        session.modified = True
    
    # Передаем информацию о том, какие подарки требуют авторизации
    auth_gifts = [g['id'] for g in GIFTS if g.get('auth_required', False)]
    
    return render_template(
        'lab9/gifts.html', 
        gift_positions=session['gift_positions'],
        auth_gifts=auth_gifts,
        is_authenticated=current_user.is_authenticated
    )


@lab9.route('/lab9/gifts/open', methods=['POST'])
def open_gift():
    """Открытие подарка (REST API)"""
    data = request.get_json()
    gift_id = data.get('gift_id')
    
    if not gift_id or not isinstance(gift_id, int):
        return jsonify({'error': 'Некорректный ID подарка'}), 400
    
    # Инициализация сессии
    if 'opened_count' not in session:
        session['opened_count'] = 0
    
    # Проверка лимита открытых подарков
    if session['opened_count'] >= 3:
        return jsonify({
            'error': 'Вы уже открыли максимальное количество подарков (3)!',
            'opened_count': session['opened_count'],
            'available_count': len([g for g in GIFTS if g['id'] not in OPENED_GIFTS])
        }), 403
    
    # Проверка, не открыт ли уже этот подарок
    if gift_id in OPENED_GIFTS:
        return jsonify({
            'error': 'Этот подарок уже забрали!',
            'opened_count': session['opened_count'],
            'available_count': len([g for g in GIFTS if g['id'] not in OPENED_GIFTS])
        }), 409
    
    # Поиск подарка
    gift = next((g for g in GIFTS if g['id'] == gift_id), None)
    if not gift:
        return jsonify({'error': 'Подарок не найден'}), 404
    
    # Проверка авторизации для особых подарков
    if gift.get('auth_required', False) and not current_user.is_authenticated:
        return jsonify({
            'error': 'Этот подарок доступен только авторизованным пользователям! Войдите в систему.',
            'auth_required': True
        }), 403
    
    # Открываем подарок
    OPENED_GIFTS.add(gift_id)
    session['opened_count'] = session['opened_count'] + 1
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': gift['message'],
        'image': gift['image'],
        'opened_count': session['opened_count'],
        'available_count': len([g for g in GIFTS if g['id'] not in OPENED_GIFTS])
    })


@lab9.route('/lab9/gifts/status', methods=['GET'])
def gifts_status():
    """Получение статуса подарков"""
    if 'opened_count' not in session:
        session['opened_count'] = 0
    
    return jsonify({
        'opened_count': session['opened_count'],
        'available_count': len([g for g in GIFTS if g['id'] not in OPENED_GIFTS]),
        'opened_gifts': list(OPENED_GIFTS),
        'total_gifts': len(GIFTS)
    })


@lab9.route('/lab9/gifts/santa', methods=['POST'])
def santa_reset():
    """Дед Мороз наполняет коробки снова (только для авторизованных)"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Только авторизованные пользователи могут вызвать Деда Мороза!'}), 403
    
    OPENED_GIFTS.clear()
    session['opened_count'] = 0
    session.modified = True
    return jsonify({'success': True, 'message': 'Дед Мороз наполнил все коробки снова! 🎅'})


# Маршруты авторизации
@lab9.route("/lab9/login", methods=["GET", "POST"])
def lab9_login():
    """Страница входа"""
    if request.method == "GET":
        return render_template('lab9/login.html')
    
    login_form = request.form.get("login")
    password_form = request.form.get("password")

    user = Users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        remember = True if request.form.get('remember') == 'on' else False
        login_user(user, remember=remember)
        return redirect('/lab9')

    return render_template('lab9/login.html', error='Неверный логин или пароль')


@lab9.route("/lab9/register", methods=["GET", "POST"])
def lab9_register():
    """Страница регистрации"""
    if request.method == "GET":
        return render_template('lab9/register.html')
    
    login_form = (request.form.get("login") or '').strip()
    password_form = (request.form.get("password") or '').strip()

    if not login_form or not password_form:
        return render_template('lab9/register.html', error='Введите логин и пароль')

    login_exists = Users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab9/register.html', error="Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password_form)
    new_user = Users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=False)
    return redirect('/lab9')


@lab9.route("/lab9/logout")
@login_required
def lab9_logout():
    """Выход из системы"""
    logout_user()
    return redirect('/lab9')
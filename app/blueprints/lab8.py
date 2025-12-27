# -*- coding: utf-8 -*-
from re import U
import re
from flask import Blueprint, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import Users, Articles

# flask-login
from flask_login import login_user, login_required, logout_user, current_user

lab8 = Blueprint("lab8", __name__)


@lab8.route('/lab8/')
def main():
    return render_template('lab8/index.html')


@lab8.route("/lab8/login", methods=["GET", "POST"])
def lab8_login():
    if request.method == "GET":
        return render_template('lab8/login.html')
    
    login_form = request.form.get("login")
    password_form = request.form.get("password")

    user = Users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        remember = True if request.form.get('remember') == 'on' else False
        login_user(user, remember=remember)
        return redirect('/lab8/articles')

    return render_template('lab8/login.html', error='Неверный логин или пароль')

@lab8.route("/lab8/register", methods=["GET", "POST"])
def lab8_register():
    if request.method == "GET":
        return render_template('lab8/register.html')
    
    login_form = (request.form.get("login") or '').strip()
    password_form = (request.form.get("password") or '').strip()

    # валидация
    if not login_form or not password_form:
        return render_template('lab8/register.html', error='Введите логин и пароль')

    login_exists = Users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error="Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password_form)
    new_user = Users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    # автологин после регистрации
    login_user(new_user, remember=False)
    return redirect('/lab8/articles')

@lab8.route("/lab8/articles", methods=["GET"])
@login_required
def lab8_articles():
    # показываем авторизованному пользователю его статьи и публичные статьи других
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        # Регистронезависимый поиск по заголовку и тексту статьи
        articles = Articles.query.filter(
            db.or_(
                db.and_(Articles.login_id == current_user.id),
                db.and_(Articles.is_public == True, Articles.login_id != current_user.id)
            ),
            db.or_(
                Articles.title.ilike(f'%{search_query}%'),
                Articles.article_text.ilike(f'%{search_query}%')
            )
        ).order_by(Articles.id.desc()).all()
    else:
        articles = Articles.query.filter(
            db.or_(
                Articles.login_id == current_user.id,
                db.and_(Articles.is_public == True, Articles.login_id != current_user.id)
            )
        ).order_by(Articles.id.desc()).all()
    
    # Подготовим author_login для шаблона
    from db.models import Users
    for a in articles:
        user = Users.query.get(a.login_id)
        a.author_login = user.login if user else None
    return render_template('lab8/articles.html', articles=articles, search_query=search_query)


@lab8.route('/lab8/logout')
@login_required
def lab8_logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/public', methods=['GET'])
def lab8_public_articles():
    """Публичные статьи доступны всем пользователям (авторизованным и нет)"""
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        # Регистронезависимый поиск по публичным статьям
        articles = Articles.query.filter(
            Articles.is_public == True,
            db.or_(
                Articles.title.ilike(f'%{search_query}%'),
                Articles.article_text.ilike(f'%{search_query}%')
            )
        ).order_by(Articles.id.desc()).all()
    else:
        articles = Articles.query.filter_by(is_public=True).order_by(Articles.id.desc()).all()
    
    # Подготовим author_login для шаблона
    from db.models import Users
    for a in articles:
        user = Users.query.get(a.login_id)
        a.author_login = user.login if user else None
    return render_template('lab8/public_articles.html', articles=articles, search_query=search_query)


@lab8.route("/lab8/create", methods=["GET", "POST"])
@login_required
def lab8_create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = (request.form.get('title') or '').strip()
    text = (request.form.get('article_text') or '').strip()
    is_public = True if request.form.get('is_public') == 'on' else False
    if not title or not text:
        return render_template('lab8/create.html', error='Заполните все поля')

    new_article = Articles(login_id=current_user.id, title=title, article_text=text, is_public=is_public, is_favorite=False)
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles')


# Редактирование статьи
@lab8.route('/lab8/articles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Articles.query.get_or_404(id)
    if article.login_id != current_user.id:
        return "Forbidden", 403
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    title = (request.form.get('title') or '').strip()
    text = (request.form.get('article_text') or '').strip()
    is_public = True if request.form.get('is_public') == 'on' else False
    if not title or not text:
        return render_template('lab8/edit.html', article=article, error='Заполните все поля')
    article.title = title
    article.article_text = text
    article.is_public = is_public
    db.session.commit()
    return redirect('/lab8/articles')


# Удаление статьи
@lab8.route('/lab8/articles/<int:id>/delete', methods=['POST'])
@login_required
def delete_article(id):
    article = Articles.query.get_or_404(id)
    if article.login_id != current_user.id:
        return "Forbidden", 403
    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles')


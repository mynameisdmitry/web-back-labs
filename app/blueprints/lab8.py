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
        login_user(user, remember=False)
        return redirect('/lab8/articles')

    return render_template('lab8/login.html', error='Неверный логин или пароль')

@lab8.route("/lab8/register", methods=["GET", "POST"])
def lab8_register():
    if request.method == "GET":
        return render_template('lab8/register.html')
    
    login_form = request.form.get("login")
    password_form = request.form.get("password")

    login_exists = Users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error="Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password_form)
    new_user = Users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/lab8/")

@lab8.route("/lab8/articles", methods=["GET"])
@login_required
def lab8_articles():
    # здесь в будущем будем выводить статьи
    return render_template('lab8/articles.html')


@lab8.route('/lab8/logout')
@login_required
def lab8_logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route("/lab8/create", methods=["POST"])
def lab8_create_article():
    return "Lab 8 Create Article Page"


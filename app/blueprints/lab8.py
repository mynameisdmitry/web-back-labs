from flask import Blueprint, render_template

lab8 = Blueprint("lab8", __name__)


@lab8.route('/lab8/')
def main():
    return render_template('lab8/index.html')


@lab8.route("/lab8/login", methods=["POST"])
def lab8_login():
    return "Lab 8 Login Page"

@lab8.route("/lab8/register", methods=["POST"])
def lab8_register():
    return "Lab 8 Register Page"

@lab8.route("/lab8/articles", methods=["GET"])
def lab8_articles():
    return "Lab 8 Articles Page"


@lab8.route("/lab8/create", methods=["POST"])
def lab8_create_article():
    return "Lab 8 Create Article Page"


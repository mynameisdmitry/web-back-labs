"""
Flask Application Factory
"""
import datetime
import os
from os import path
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from db import db


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Загрузка конфигурации из config.py
    from config import config
    app.config.from_object(config[config_name])

    # DB: настроим SQLALCHEMY_DATABASE_URI в зависимости от DB_TYPE
    db_type = app.config.get('DB_TYPE', 'postgres')
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        if db_type == 'postgres':
            db_name = app.config.get('DB_NAME')
            db_user = app.config.get('DB_USER')
            db_password = app.config.get('DB_PASSWORD')
            host_ip = app.config.get('DB_HOST')
            host_port = app.config.get('DB_PORT')
            app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}"
        else:
            # sqlite
            dir_path = path.dirname(path.realpath(__file__))
            db_path = path.join(dir_path, 'database.db')
            app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    # SQLAlchemy settings
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    # JSON настройки для поддержки UTF-8
    app.json.ensure_ascii = False
    app.config['JSON_AS_ASCII'] = False
    
    # Настройка кодировки для HTML ответов
    @app.after_request
    def after_request(response):
        if 'text/html' in response.content_type:
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    
    # Инициализируем SQLAlchemy
    db.init_app(app)

    # Инициализируем LoginManager
    try:
        from flask_login import LoginManager
        from db.models import Users
        login_manager = LoginManager()
        login_manager.login_view = 'lab8.lab8_login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            return Users.query.get(int(user_id))
    except Exception:
        # flask-login не установлен или модель Users недоступна в момент импорта
        pass

    # Регистрация blueprints
    from app.blueprints import lab1, lab2, lab3, lab4, lab5, lab6, lab7, lab8, lab9
    
    app.register_blueprint(lab1)
    app.register_blueprint(lab2)
    app.register_blueprint(lab3)
    app.register_blueprint(lab4)
    app.register_blueprint(lab5)
    app.register_blueprint(lab6)
    app.register_blueprint(lab7)
    app.register_blueprint(lab8)
    app.register_blueprint(lab9)
    
    # Журнал доступа для страницы 404
    access_log = []
    
    # Error handlers
    @app.errorhandler(500)
    def internal_server_error(err):
        """Обработчик ошибки 500"""
        return render_template('500.html'), 500
    
    @app.errorhandler(404)
    def not_found(err):
        """Обработчик ошибки 404 с логированием"""
        client_ip = request.remote_addr
        access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        requested_path = request.path
        
        log_entry = {
            'timestamp': access_date,
            'ip': client_ip,
            'path': requested_path
        }
        access_log.append(log_entry)
        
        if len(access_log) > 50:
            access_log.pop(0)
        
        return render_template('404.html',
                             client_ip=client_ip,
                             access_date=access_date,
                             requested_path=requested_path,
                             access_log=reversed(access_log)), 404
    
    # Main routes
    @app.route("/")
    @app.route("/index")
    def index():
        """Главная страница со списком лабораторных работ"""
        return render_template('index.html')
    
    return app

"""
Flask Application Factory
"""
from flask import Flask, render_template, request
import datetime
import os


def create_app(config=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Конфигурация
    app.json.ensure_ascii = False
    
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'секретно-секретный-секрет'),
        SESSION_COOKIE_NAME='flask_session',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=3600,
        APPLICATION_ROOT='/'
    )
    
    app.secret_key = app.config['SECRET_KEY']
    
    # Определяем окружение
    IS_PYTHONANYWHERE = bool(os.environ.get('PYTHONANYWHERE_DOMAIN'))
    default_db = 'sqlite' if IS_PYTHONANYWHERE else 'postgres'
    app.config['DB_TYPE'] = os.environ.get('DB_TYPE', default_db)
    
    # Регистрация blueprints
    from app.blueprints import lab1, lab2, lab3, lab4, lab5, lab6, lab7
    
    app.register_blueprint(lab1)
    app.register_blueprint(lab2)
    app.register_blueprint(lab3)
    app.register_blueprint(lab4)
    app.register_blueprint(lab5)
    app.register_blueprint(lab6)
    app.register_blueprint(lab7)
    
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

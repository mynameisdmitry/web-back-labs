"""
Configuration settings for Flask application
"""
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
    SESSION_COOKIE_NAME = 'flask_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600
    APPLICATION_ROOT = '/'
    
    # JSON и кодировка
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    
    # Database
    IS_PYTHONANYWHERE = bool(os.environ.get('PYTHONANYWHERE_DOMAIN'))
    DB_TYPE = os.environ.get('DB_TYPE', 'sqlite' if IS_PYTHONANYWHERE else 'postgres')
    
    # PostgreSQL Configuration
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = int(os.environ.get('DB_PORT', '5432'))
    DB_NAME = os.environ.get('DB_NAME', 'dmitry_igumenshev_knowledge_base')
    DB_USER = os.environ.get('DB_USER', 'dmitry_igumenshev_knowledge_base')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Dima2005')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

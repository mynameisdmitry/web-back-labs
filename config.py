"""
Configuration settings for Flask application
"""
import os


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
    SESSION_COOKIE_NAME = 'flask_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600
    APPLICATION_ROOT = '/'
    
    # Database
    IS_PYTHONANYWHERE = bool(os.environ.get('PYTHONANYWHERE_DOMAIN'))
    DB_TYPE = os.environ.get('DB_TYPE', 'sqlite' if IS_PYTHONANYWHERE else 'postgres')


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

"""
Entry point for Flask application
"""
from app import create_app
import os

# Определяем окружение из переменной FLASK_ENV
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True)

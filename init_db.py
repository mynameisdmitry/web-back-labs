#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для инициализации базы данных
Создаёт все необходимые таблицы
"""

from app import create_app
from db import db

def init_database():
    """Создание всех таблиц в базе данных"""
    app = create_app('production')
    
    with app.app_context():
        print("Создание таблиц в базе данных...")
        db.create_all()
        print("✓ Все таблицы успешно созданы!")
        
        # Вывод списка созданных таблиц
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\nСозданные таблицы ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")

if __name__ == '__main__':
    init_database()

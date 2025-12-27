from app import create_app
from app.blueprints.lab7 import _ensure_db
from app.blueprints.lab5 import db_connect, db_close, sql


def test_crud_flow():
    app = create_app('default')
    # принудительно используем sqlite для тестов
    app.config['DB_TYPE'] = 'sqlite'
    with app.app_context():
        # Создадим таблицу
        _ensure_db()
        conn, cur = db_connect()
        # Очистим таблицу перед тестом
        cur.execute(sql("DELETE FROM films"))
        db_close(conn, cur)

        client = app.test_client()

        # Create
        payload = {'title': 'T1', 'title_ru': 'Т1', 'year': 2020, 'description': 'd'}
        r = client.post('/lab7/rest-api/films/', json=payload)
        assert r.status_code == 200
        new_id = r.get_json()['id']

        # Read
        r = client.get('/lab7/rest-api/films/' + str(new_id))
        assert r.status_code == 200
        assert r.get_json()['title'] == 'T1'

        # Update
        r = client.put('/lab7/rest-api/films/' + str(new_id), json={'title':'T1-up','title_ru':'Т1','year':2021,'description':'dd'})
        assert r.status_code == 200
        assert r.get_json()['title'] == 'T1-up'

        # Delete
        r = client.delete('/lab7/rest-api/films/' + str(new_id))
        assert r.status_code == 204

        # Not found
        r = client.get('/lab7/rest-api/films/' + str(new_id))
        assert r.status_code == 404

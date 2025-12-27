import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app('default')
    return app.test_client()


def test_missing_title_ru(client):
    payload = {'title':'Orig','title_ru':'','year':2020,'description':'x'}
    r = client.post('/lab7/rest-api/films/', json=payload)
    assert r.status_code == 400
    assert 'title_ru' in r.get_json()


def test_title_and_title_ru_missing(client):
    payload = {'title':'','title_ru':'','year':2020,'description':'x'}
    r = client.post('/lab7/rest-api/films/', json=payload)
    assert r.status_code == 400
    assert 'title' in r.get_json() or 'title_ru' in r.get_json()


def test_year_bounds(client):
    payload = {'title':'A','title_ru':'B','year':1800,'description':'x'}
    r = client.post('/lab7/rest-api/films/', json=payload)
    assert r.status_code == 400
    assert 'year' in r.get_json()


def test_description_length(client):
    payload = {'title':'A','title_ru':'B','year':2020,'description':'x'*2001}
    r = client.post('/lab7/rest-api/films/', json=payload)
    assert r.status_code == 400
    assert 'description' in r.get_json()

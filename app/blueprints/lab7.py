from flask import Blueprint, render_template, jsonify, abort, request, current_app

# Подключаем хелперы для работы с БД из lab5
from app.blueprints.lab5 import db_connect, db_close, sql

lab7 = Blueprint("lab7", __name__)

# Начальные данные (seed) — будут импортированы в БД при первом запуске
initial_films = [
    {
        "title": "The Matrix",
        "title_ru": "Матрица",
        "year": 1999,
        "description": "Программист Нео узнаёт, что привычный мир — цифровая симуляция.",
    },
    {
        "title": "Gladiator",
        "title_ru": "Гладиатор",
        "year": 2000,
        "description": "Римский полководец Максимус теряет всё и становится гладиатором.",
    },
    {
        "title": "Se7en",
        "title_ru": "Семь",
        "year": 1995,
        "description": "Два детектива расследуют серию убийств, связанных с семью смертными грехами.",
    },
    {
        "title": "Whiplash",
        "title_ru": "Одержимость",
        "year": 2014,
        "description": "Молодой барабанщик сталкивается с жестким преподавателем и ценой успеха.",
    },
    {
        "title": "Arrival",
        "title_ru": "Прибытие",
        "year": 2016,
        "description": "Лингвист пытается понять язык пришельцев, чтобы предотвратить глобальный конфликт.",
    },
]


def _ensure_db():
    """Create films table if not exists and seed initial data if table is empty."""
    conn = cur = None
    try:
        conn, cur = db_connect()
        db_type = current_app.config.get('DB_TYPE', 'postgres')

        if db_type == 'sqlite':
            create_sql = (
                "CREATE TABLE IF NOT EXISTS films ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "title TEXT NOT NULL,"
                "title_ru TEXT NOT NULL,"
                "year INTEGER NOT NULL,"
                "description TEXT NOT NULL"
                ")"
            )
            cur.execute(create_sql)
        else:
            # Postgres
            create_sql = (
                "CREATE TABLE IF NOT EXISTS films ("
                "id SERIAL PRIMARY KEY,"
                "title TEXT NOT NULL,"
                "title_ru TEXT NOT NULL,"
                "year INTEGER NOT NULL,"
                "description TEXT NOT NULL"
                ")"
            )
            cur.execute(create_sql)

        # Проверим, пустая ли таблица
        cur.execute(sql("SELECT COUNT(*) as cnt FROM films"))
        row = cur.fetchone()
        cnt = row['cnt'] if isinstance(row, dict) and 'cnt' in row else (row[0] if row else 0)
        if cnt == 0:
            # Вставим seed данные
            for f in initial_films:
                cur.execute(sql("INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s)"),
                            (f['title'], f['title_ru'], f['year'], f['description']))
        db_close(conn, cur)
    except Exception:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        raise


def _exists_film(id: int) -> bool:
    conn = cur = None
    try:
        conn, cur = db_connect()
        cur.execute(sql("SELECT 1 FROM films WHERE id=%s"), (id,))
        row = cur.fetchone()
        db_close(conn, cur)
        return bool(row)
    except Exception:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return False


def _validate_film_payload(data):
    """Валидация структуры фильма.

    Возвращаем (ok, errors). Если есть ошибки по полям, errors — dict
    с ключами полей, например: {"description": "Заполните описание"}.
    """
    if not isinstance(data, dict):
        return False, {"_general": "Ожидается JSON-объект"}

    # Убедимся, что все поля присутствуют
    required = ["title", "title_ru", "year", "description"]
    for k in required:
        if k not in data:
            return False, {"_general": f"Отсутствует поле: {k}"}

    errors = {}

    # title_ru обязательно
    if not str(data.get("title_ru", "")).strip():
        errors["title_ru"] = "Поле \"Название (рус.)\" обязательно"

    # title — либо непустой, либо может быть заполнено из title_ru раньше
    if not str(data.get("title", "")).strip() and not str(data.get("title_ru", "")).strip():
        errors["title"] = "Поле \"Название (ориг.)\" обязательно, если нет русского названия"

    # год — число и в диапазоне [1895, текущий]
    try:
        data["year"] = int(data["year"])
        import datetime
        this_year = datetime.datetime.now().year
        if data["year"] < 1895 or data["year"] > this_year:
            errors["year"] = f"Год должен быть от 1895 до {this_year}"
    except Exception:
        errors["year"] = "Поле \"Год\" должно быть целым числом"

    # описание — непустое и не более 2000 символов
    desc = str(data.get("description", ""))
    if not desc.strip():
        errors["description"] = "Заполните описание"
    elif len(desc) > 2000:
        errors["description"] = "Описание не должно превышать 2000 символов"

    if errors:
        return False, errors

    return True, {}



@lab7.route("/lab7/")
def index():
    # При первом запросе убеждаемся, что таблица существует и заполнена
    _ensure_db()
    return render_template("lab7/index.html")


# GET: все фильмы
@lab7.route("/lab7/rest-api/films/", methods=["GET"])
def get_films():
    _ensure_db()
    conn = cur = None
    try:
        conn, cur = db_connect()
        cur.execute(sql("SELECT id, title, title_ru, year, description FROM films ORDER BY id"))
        rows = cur.fetchall()
        db_close(conn, cur)
        films = []
        for r in rows:
            if isinstance(r, dict):
                films.append(r)
            else:
                films.append({
                    'id': r[0], 'title': r[1], 'title_ru': r[2], 'year': r[3], 'description': r[4]
                })
        return jsonify(films)
    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return jsonify({'error': str(e)}), 500


# GET: один фильм
@lab7.route("/lab7/rest-api/films/<int:id>", methods=["GET"])
def get_film(id: int):
    _ensure_db()
    conn = cur = None
    try:
        conn, cur = db_connect()
        cur.execute(sql("SELECT id, title, title_ru, year, description FROM films WHERE id=%s"), (id,))
        r = cur.fetchone()
        db_close(conn, cur)
        if not r:
            return jsonify({'error': 'Not found'}), 404
        if isinstance(r, dict):
            return jsonify(r)
        return jsonify({'id': r[0], 'title': r[1], 'title_ru': r[2], 'year': r[3], 'description': r[4]})
    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return jsonify({'error': str(e)}), 500


# DELETE: удалить фильм, ответ 204
@lab7.route("/lab7/rest-api/films/<int:id>", methods=["DELETE"])
def del_film(id: int):
    _ensure_db()
    if not _exists_film(id):
        abort(404)
    conn = cur = None
    try:
        conn, cur = db_connect()
        cur.execute(sql("DELETE FROM films WHERE id=%s"), (id,))
        db_close(conn, cur)
        return "", 204
    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return jsonify({'error': str(e)}), 500

# PUT: заменить фильм целиком, вернуть обновлённый фильм
@lab7.route("/lab7/rest-api/films/<int:id>", methods=["PUT"])
def put_film(id: int):
    _ensure_db()
    if not _exists_film(id):
        abort(404)

    film = request.get_json(silent=True)
    # Если оригинальное название пусто, но есть русское — используем его
    if isinstance(film, dict) and not str(film.get('title', '')).strip() and film.get('title_ru'):
        film['title'] = film.get('title_ru')

    ok, err = _validate_film_payload(film)
    if not ok:
        return jsonify(err), 400

    conn = cur = None
    try:
        conn, cur = db_connect()
        cur.execute(sql("UPDATE films SET title=%s, title_ru=%s, year=%s, description=%s WHERE id=%s"),
                    (film['title'], film['title_ru'], film['year'], film['description'], id))
        # вернём обновлённый объект
        cur.execute(sql("SELECT id, title, title_ru, year, description FROM films WHERE id=%s"), (id,))
        r = cur.fetchone()
        db_close(conn, cur)
        if isinstance(r, dict):
            return jsonify(r)
        return jsonify({'id': r[0], 'title': r[1], 'title_ru': r[2], 'year': r[3], 'description': r[4]})
    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return jsonify({'error': str(e)}), 500


# POST: добавить новый фильм, вернуть индекс нового элемента (как в методичке)
@lab7.route("/lab7/rest-api/films/", methods=["POST"])
def add_film():
    _ensure_db()
    film = request.get_json(silent=True)
    # Если оригинальное название пусто, но есть русское — используем его
    if isinstance(film, dict) and not str(film.get('title', '')).strip() and film.get('title_ru'):
        film['title'] = film.get('title_ru')

    ok, err = _validate_film_payload(film)
    if not ok:
        return jsonify(err), 400

    conn = cur = None
    try:
        conn, cur = db_connect()
        db_type = current_app.config.get('DB_TYPE', 'postgres')
        if db_type == 'postgres':
            cur.execute(sql("INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s) RETURNING id"),
                        (film['title'], film['title_ru'], film['year'], film['description']))
            r = cur.fetchone()
            new_id = r['id'] if isinstance(r, dict) and 'id' in r else r[0]
        else:
            cur.execute(sql("INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s)"),
                        (film['title'], film['title_ru'], film['year'], film['description']))
            new_id = cur.lastrowid
        db_close(conn, cur)
        return jsonify({"id": new_id})
    except Exception as e:
        if conn and cur:
            try:
                db_close(conn, cur)
            except Exception:
                pass
        return jsonify({'error': str(e)}), 500

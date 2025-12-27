from flask import Blueprint, render_template, jsonify, abort, request

lab7 = Blueprint("lab7", __name__)


films = [
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


def _check_id(id: int) -> None:
    if id < 0 or id >= len(films):
        abort(404)


def _validate_film_payload(data):
    """Минимальная валидация структуры фильма.

    Возвращаем (ok, error). Если есть ошибки по полям, error может быть dict
    с ключами полей, например: {"description": "Заполните описание"}.
    """
    if not isinstance(data, dict):
        return False, {"_general": "Expected JSON object"}

    required = ["title", "title_ru", "year", "description"]
    for k in required:
        if k not in data:
            return False, {"_general": f"Missing field: {k}"}

    try:
        data["year"] = int(data["year"])
    except Exception:
        return False, {"year": "Field 'year' must be an integer"}

    # Поле description не должно быть пустым
    if not str(data.get("description", "")).strip():
        return False, {"description": "Заполните описание"}

    return True, {}



@lab7.route("/lab7/")
def index():
    return render_template("lab7/index.html")


# GET: все фильмы
@lab7.route("/lab7/rest-api/films/", methods=["GET"])
def get_films():
    return jsonify(films)


# GET: один фильм
@lab7.route("/lab7/rest-api/films/<int:id>", methods=["GET"])
def get_film(id: int):
    _check_id(id)
    return jsonify(films[id])


# DELETE: удалить фильм, ответ 204
@lab7.route("/lab7/rest-api/films/<int:id>", methods=["DELETE"])
def del_film(id: int):
    _check_id(id)
    del films[id]
    return "", 204


# PUT: заменить фильм целиком, вернуть обновлённый фильм
@lab7.route("/lab7/rest-api/films/<int:id>", methods=["PUT"])
def put_film(id: int):
    _check_id(id)

    film = request.get_json(silent=True)
    ok, err = _validate_film_payload(film)
    if not ok:
        return jsonify(err), 400

    films[id] = film
    return jsonify(films[id])


# POST: добавить новый фильм, вернуть индекс нового элемента (как в методичке)
@lab7.route("/lab7/rest-api/films/", methods=["POST"])
def add_film():
    film = request.get_json(silent=True)
    ok, err = _validate_film_payload(film)
    if not ok:
        return jsonify(err), 400

    films.append(film)
    new_id = len(films) - 1
    return jsonify({"id": new_id})

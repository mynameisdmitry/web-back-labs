from flask import Blueprint, render_template, jsonify, abort

lab7 = Blueprint("lab7", __name__)

# Список фильмов в памяти (минимум 5)
films = [
    {
        "title": "The Matrix",
        "title_ru": "Матрица",
        "year": 1999,
        "description": (
            "Программист Нео узнаёт, что привычный мир — цифровая симуляция. "
            "Он становится ключевой фигурой в борьбе людей против машин, контролирующих реальность."
        ),
    },
    {
        "title": "The Lord of the Rings: The Fellowship of the Ring",
        "title_ru": "Властелин колец: Братство Кольца",
        "year": 2001,
        "description": (
            "Хоббит Фродо получает Кольцо Всевластия и отправляется в опасный путь, "
            "чтобы уничтожить его и предотвратить возвращение тьмы в Средиземье."
        ),
    },
    {
        "title": "Gladiator",
        "title_ru": "Гладиатор",
        "year": 2000,
        "description": (
            "Римский полководец Максимус теряет всё из-за дворцового переворота и становится гладиатором. "
            "Он ищет справедливость и шанс изменить судьбу империи."
        ),
    },
    {
        "title": "Se7en",
        "title_ru": "Семь",
        "year": 1995,
        "description": (
            "Два детектива расследуют серию убийств, связанных с семью смертными грехами. "
            "Дело превращается в психологический поединок с преступником, который тщательно продумал каждую деталь."
        ),
    },
    {
        "title": "Whiplash",
        "title_ru": "Одержимость",
        "year": 2014,
        "description": (
            "Молодой барабанщик поступает в престижную музыкальную школу и попадает к жесткому преподавателю. "
            "Их противостояние проверяет границы таланта, дисциплины и цены успеха."
        ),
    },
]


@lab7.route("/lab7/")
def index():
    return render_template("lab7/index.html")


# GET: вернуть все фильмы
@lab7.route("/lab7/rest-api/films/", methods=["GET"])
def get_films():
    return jsonify(films)


# GET: вернуть один фильм по индексу (нумерация с 0)
@lab7.route("/lab7/rest-api/films/<int:id>", methods=["GET"])
def get_film(id: int):
    if id < 0 or id >= len(films):
        abort(404)
    return jsonify(films[id])


# DELETE: удалить фильм по индексу и вернуть 204 No Content
@lab7.route("/lab7/rest-api/films/<int:id>", methods=["DELETE"])
def del_film(id: int):
    if id < 0 or id >= len(films):
        abort(404)

    del films[id]
    return "", 204

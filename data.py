EGO = "Me"

PEOPLE = [
    ("Андрей Коробенков", "friend"),
    ("Александр Мартынов", "friend"),
    ("Евгений Самигуллин", "work"),
    ("Евгений Бурлаков", "work"),
]


def group(members, relation):
    return {
        "type": "group",
        "members": members,
        "relation": relation,
    }


RELATIONS_BETWEEN_OTHERS = [
    group(
        ["Евгений Самигуллин", "Евгений Бурлаков"],
        relation="work"
    ),
    group(
        ["Андрей Коробенков", "Александр Мартынов"],
        relation="friends"
    ),
]

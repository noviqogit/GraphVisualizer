EGO = "Me"

PEOPLE = [
    ("Alice", "friend"),
    ("Bob", "work"),
    ("Charlie", "family"),
    ("Diana", "romantic"),
    ("Eve", "friend"),
    ("Frank", "work"),
    ("Grace", "friend"),
]


def group(members, relation):
    return {
        "type": "group",
        "members": members,
        "relation": relation,
    }

RELATIONS_BETWEEN_OTHERS = [
    group(
        ["Alice", "Bob", "Charlie", "Diana"],
        relation="work"
    ),
    group(
        ["Eve", "Frank", "Grace"],
        relation="friends"
    ),
]

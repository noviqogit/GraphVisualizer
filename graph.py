import igraph as ig
from itertools import combinations
from data import EGO, PEOPLE, RELATIONS_BETWEEN_OTHERS


RELATION_COLORS = {
    "friend": "dodgerblue",
    "friends": "dodgerblue",
    "work": "orange",
    "family": "green",
    "romantic": "crimson",
    "other": "gray",
}


def build_graph():
    g = ig.Graph()
    g.add_vertex(EGO)

    # добавляем всех людей
    for name, _ in PEOPLE:
        if name not in g.vs["name"]:
            g.add_vertex(name)

    # связи ego -> people
    for name, relation in PEOPLE:
        g.add_edge(EGO, name, relation=relation)

    # связи между остальными
    for item in RELATIONS_BETWEEN_OTHERS:
        if item["type"] == "group":
            members = item["members"]
            relation = item["relation"]

            for u, v in combinations(members, 2):
                g.add_edge(u, v, relation=relation)

    return g


def build_ego_graph(graph, radius=1):
    ego_idx = graph.vs.find(name=EGO).index
    return graph.induced_subgraph(
        graph.neighborhood(ego_idx, order=radius)
    )

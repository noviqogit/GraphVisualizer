import igraph as ig


VERTEX_COLORS = {
    "self": "gold",
    "friends": "green",
    "work": "skyblue",
    "family": "salmon",
}


def plot_ego_graph(g, edge_colors, center_id="me"):
    center = g.vs.find(id=center_id).index
    ego = g.induced_subgraph(g.neighborhood(center, order=1))

    ego.vs["color"] = [
        VERTEX_COLORS.get(group, "gray")
        for group in ego.vs["group"]
    ]

    ego.vs["size"] = [
        40 if v["id"] == center_id else 25
        for v in ego.vs
    ]

    ego.es["color"] = [
        edge_colors.get(t, "gray")
        for t in ego.es["relation_type"]
    ]

    ego.es["width"] = ego.es["weight"]

    layout = ego.layout("fr")

    ig.plot(
        ego,
        layout=layout,
        target="ego_graph.png",
        vertex_label=ego.vs["label"],
        bbox=(800, 800),
        margin=80,
    )

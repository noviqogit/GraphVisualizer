import igraph as ig


def build_graph(people, relations):
    g = ig.Graph(directed=False)

    g.add_vertices(len(people))
    g.vs["id"] = people["id"].tolist()
    g.vs["label"] = people["name"].tolist()
    g.vs["group"] = people["group"].tolist()

    id_to_idx = {vid: i for i, vid in enumerate(g.vs["id"])}

    edges, weights, relation_types = [], [], []

    for r in relations.itertuples():
        edges.append((id_to_idx[r.source], id_to_idx[r.target]))
        weights.append(r.weight)
        relation_types.append(r.relation_type)

    g.add_edges(edges)
    g.es["weight"] = weights
    g.es["relation_type"] = relation_types

    return g

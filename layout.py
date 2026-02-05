def compute_ego_layout_3d(graph, ego="Me"):
    layout = graph.layout_fruchterman_reingold_3d()

    pos = {
        v["name"]: coord
        for v, coord in zip(graph.vs, layout)
    }

    pos[ego] = (0.0, 0.0, 0.0)
    return pos

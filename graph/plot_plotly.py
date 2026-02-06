import random
import plotly.graph_objects as go


VERTEX_COLORS = {
    "self": "gold",
    "friends": "green",
    "work": "blue",
    "family": "red",
}

EDGE_COLORS = {
    "friends": "green",
    "work": "blue",
    "family": "red",
}

DIRECTION_VECTORS = {
    "friends": (1, 0, 0),
    "work": (0, 1, 0),
    "family": (0, -1, 0),
}

BASE_DISTANCE = 10
JITTER = 3


def plot_ego_graph_3d(g, center_id="me"):
    center_idx = g.vs.find(id=center_id).index
    ego = g.induced_subgraph(g.neighborhood(center_idx, order=1))

    # координаты вручную
    coords = []

    for v in ego.vs:
        if v["id"] == center_id:
            coords.append((0, 0, 0))
            continue

        # ищем связь с центром
        e = ego.es.find(_between=([v.index], [ego.vs.find(id=center_id).index]))
        rel_type = e["relation_type"]

        dx, dy, dz = DIRECTION_VECTORS.get(rel_type, (0, 0, 1))

        x = dx * BASE_DISTANCE + random.uniform(-JITTER, JITTER)
        y = dy * BASE_DISTANCE + random.uniform(-JITTER, JITTER)
        z = dz * BASE_DISTANCE + random.uniform(-JITTER, JITTER)

        coords.append((x, y, z))

    x, y, z = zip(*coords)

    # --- рёбра
    edge_x, edge_y, edge_z = [], [], []

    for e in ego.es:
        s, t = e.tuple
        edge_x += [x[s], x[t], None]
        edge_y += [y[s], y[t], None]
        edge_z += [z[s], z[t], None]

    edge_trace = go.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode="lines",
        line=dict(
            width=4,
            color="gray",
        ),
        hoverinfo="none",
    )

    # --- вершины
    node_colors = [
        VERTEX_COLORS.get(v["group"], "gray")
        for v in ego.vs
    ]

    node_sizes = [
        24 if v["id"] == center_id else 12
        for v in ego.vs
    ]

    node_trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers+text",
        text=ego.vs["label"],
        textposition="top center",
        hovertext=[
            f"id: {v['id']}<br>group: {v['group']}"
            for v in ego.vs
        ],
        marker=dict(
            size=node_sizes,
            color=node_colors,
            opacity=0.9,
        ),
    )

    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        title="Social Ego Graph (directional)",
        showlegend=False,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )

    fig.show()

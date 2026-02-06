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


def plot_ego_graph_3d(g, center_id="me"):
    # --- эго-граф
    center = g.vs.find(id=center_id).index
    ego = g.induced_subgraph(g.neighborhood(center, order=1))

    # --- 3D layout
    layout = ego.layout("fr", dim=3)
    coords = layout.coords
    x, y, z = zip(*coords)

    # --- рёбра
    edge_x, edge_y, edge_z, edge_color = [], [], [], []

    for e in ego.es:
        s, t = e.tuple
        color = EDGE_COLORS.get(e["relation_type"], "gray")

        edge_x += [x[s], x[t], None]
        edge_y += [y[s], y[t], None]
        edge_z += [z[s], z[t], None]
        edge_color.append(color)

    edge_trace = go.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode="lines",
        line=dict(width=4, color="gray"),
        hoverinfo="none",
    )

    # --- вершины
    node_colors = [
        VERTEX_COLORS.get(v["group"], "gray")
        for v in ego.vs
    ]

    node_sizes = [
        18 if v["id"] == center_id else 10
        for v in ego.vs
    ]

    node_trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers+text",
        text=ego.vs["label"],
        textposition="top center",
        hovertext=ego.vs["id"],
        marker=dict(
            size=node_sizes,
            color=node_colors,
            opacity=0.9,
        ),
    )

    # --- фигура
    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        title="Social Ego Graph (3D)",
        showlegend=False,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )

    fig.show()

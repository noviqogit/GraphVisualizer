import plotly.graph_objects as go
from graph import RELATION_COLORS
from data import EGO


def visualize_ego_3d(graph, pos):
    edge_x, edge_y, edge_z = [], [], []

    for e in graph.es:
        u = graph.vs[e.source]["name"]
        v = graph.vs[e.target]["name"]
        x0, y0, z0 = pos[u]
        x1, y1, z1 = pos[v]

        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]

    edges = go.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode="lines",
        line=dict(width=2, color="lightgray"),
        hoverinfo="none"
    )

    node_x, node_y, node_z = [], [], []
    colors, sizes, labels = [], [], []

    for v in graph.vs:
        name = v["name"]
        x, y, z = pos[name]

        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        labels.append(name)

        if name == EGO:
            colors.append("black")
            sizes.append(22)
        else:
            eid = graph.get_eid(EGO, name, error=False)
            relation = graph.es[eid]["relation"] if eid != -1 else "other"
            colors.append(RELATION_COLORS.get(relation, "gray"))
            sizes.append(10)

    nodes = go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode="markers+text",
        text=labels,
        textposition="top center",
        marker=dict(
            size=sizes,
            color=colors,
            opacity=0.9
        )
    )

    fig = go.Figure(data=[edges, nodes])
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    fig.show()

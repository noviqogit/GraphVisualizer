import math
import random
import plotly.graph_objects as go


VERTEX_COLORS = {
    "self": "gold",
    "friends": "green",
    "work": "blue",
    "family": "red",
}

EDGE_COLOR = "gray"

# ---- НАПРАВЛЕНИЯ ПО ТИПАМ СВЯЗЕЙ ----
RELATION_DIRECTIONS = {
    "family": (0, 0, 1),     # вверх
    "work": (1, 0, 0),       # вправо
    "friends": (0, 1, 0),    # вперёд
}

DEFAULT_DIRECTION = (-1, 0, 0)

# ---- ДИСТАНЦИИ (усиленное влияние weight) ----
MIN_DISTANCE = 5     # weight = 5
MAX_DISTANCE = 42    # weight = 1
K = 1.15             # чем больше — тем сильнее контраст

LEVEL_2_OFFSET = 14

JITTER_DISTANCE = 1.2
JITTER_ANGLE = 0.35


def normalize(v):
    l = math.sqrt(sum(c * c for c in v))
    return tuple(c / l for c in v)


def random_unit_vector():
    phi = random.uniform(0, 2 * math.pi)
    costheta = random.uniform(-1, 1)
    theta = math.acos(costheta)
    return (
        math.sin(theta) * math.cos(phi),
        math.sin(theta) * math.sin(phi),
        math.cos(theta),
    )


def jitter_direction(base):
    bx, by, bz = normalize(base)
    rx, ry, rz = random_unit_vector()

    x = bx * (1 - JITTER_ANGLE) + rx * JITTER_ANGLE
    y = by * (1 - JITTER_ANGLE) + ry * JITTER_ANGLE
    z = bz * (1 - JITTER_ANGLE) + rz * JITTER_ANGLE

    return normalize((x, y, z))


def weight_to_distance(weight: float) -> float:
    """
    weight ∈ [1..5]
    5 → очень близко
    1 → далеко
    """
    weight = max(1, min(5, weight))
    return MIN_DISTANCE + (MAX_DISTANCE - MIN_DISTANCE) * math.exp(
        -K * (weight - 1)
    )


def get_weight_and_level(ego, v_idx, center_idx):
    if ego.are_connected(v_idx, center_idx):
        e = ego.es.find(_between=([v_idx], [center_idx]))
        return e["weight"], 1

    for n in ego.neighbors(v_idx):
        if ego.are_connected(n, center_idx):
            e = ego.es.find(_between=([n], [center_idx]))
            return e["weight"], 2

    return 1, 2


def plot_ego_graph_3d(g, center_id="me"):
    center_idx = g.vs.find(id=center_id).index
    ego = g.induced_subgraph(
        g.neighborhood(center_idx, order=2)
    )

    coords = []
    center_ego_idx = ego.vs.find(id=center_id).index

    for v in ego.vs:
        if v.index == center_ego_idx:
            coords.append((0, 0, 0))
            continue

        weight, level = get_weight_and_level(
            ego, v.index, center_ego_idx
        )

        relation = v["group"]
        base_dir = RELATION_DIRECTIONS.get(
            relation, DEFAULT_DIRECTION
        )

        dx, dy, dz = jitter_direction(base_dir)

        distance = weight_to_distance(weight)
        if level == 2:
            distance += LEVEL_2_OFFSET

        x = dx * distance + random.uniform(-JITTER_DISTANCE, JITTER_DISTANCE)
        y = dy * distance + random.uniform(-JITTER_DISTANCE, JITTER_DISTANCE)
        z = dz * distance + random.uniform(-JITTER_DISTANCE, JITTER_DISTANCE)

        coords.append((x, y, z))

    x, y, z = zip(*coords)

    # ---- РЁБРА (ОДИНАКОВАЯ ТОЛЩИНА, РАЗНАЯ ДЛИНА) ----
    edge_traces = []

    for e in ego.es:
        s, t = e.tuple

        edge_traces.append(
            go.Scatter3d(
                x=[x[s], x[t]],
                y=[y[s], y[t]],
                z=[z[s], z[t]],
                mode="lines",
                line=dict(
                    width=2,
                    color=EDGE_COLOR,
                ),
                hoverinfo="none",
            )
        )

    # ---- УЗЛЫ ----
    node_trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers+text",
        text=ego.vs["label"],
        textposition="top center",
        marker=dict(
            size=[
                28 if v["id"] == center_id else 12
                for v in ego.vs
            ],
            color=[
                VERTEX_COLORS.get(v["group"], "gray")
                for v in ego.vs
            ],
            opacity=0.9,
        ),
    )

    fig = go.Figure(edge_traces + [node_trace])
    fig.update_layout(
        title="Social Ego Graph (edge length = weight)",
        showlegend=False,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )

    fig.show()

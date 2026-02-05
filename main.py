from graph import build_graph, build_ego_graph
from layout import compute_ego_layout_3d
from visualize import visualize_ego_3d
from data import EGO


def main():
    graph = build_graph()
    ego_graph = build_ego_graph(graph, radius=1)

    pos = compute_ego_layout_3d(ego_graph, ego=EGO)
    visualize_ego_3d(ego_graph, pos)


if __name__ == "__main__":
    main()

from graph.load_graph import load_data
from graph.build_graph import build_graph
from graph.plot_plotly import plot_ego_graph_3d


def main():
    people, relations, _ = load_data()
    graph = build_graph(people, relations)
    plot_ego_graph_3d(graph, center_id="me")


if __name__ == "__main__":
    main()

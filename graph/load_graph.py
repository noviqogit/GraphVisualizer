import pandas as pd


def load_data(data_dir="data"):
    people = pd.read_csv(f"{data_dir}/people.csv")
    relations = pd.read_csv(f"{data_dir}/relations.csv")
    relation_types = pd.read_csv(f"{data_dir}/relation_types.csv")

    edge_colors = dict(
        zip(relation_types["type"], relation_types["color"])
    )

    return people, relations, edge_colors

import networkx as nx
import pandas as pd


def get_edges_rus(data: pd.DataFrame):
    df = data[['word', 'assoc', 'weight', 'mirror_weight', 'dir']]

    # Create a new DataFrame for unique edges
    edges = df[df['dir'].isin(['DIR', 'BIDIR'])][['word', 'assoc', 'weight']]
    edges.columns = ['сue', 'asso', 'weight']

    # Calculate sum for every сue
    total_weight = edges.groupby('сue')['weight'].transform('sum')

    # Calculate the normalized weight for each edge
    edges['weight'] = edges['weight'] / total_weight

    # Convert the edges DataFrame to a list of tuples
    edges = list(edges.itertuples(index=False, name=None))
    return edges


def get_edges_dutch(data: pd.DataFrame):
    # Melt the DataFrame to long form
    edges = data.melt(id_vars='cue', value_vars=['asso1', 'asso2', 'asso3'], value_name='asso')

    # Create a new DataFrame with the edges and their counts
    edges = edges.groupby(['cue', 'asso']).size().reset_index(name='count')

    # Calculate sum for every cue
    total_count = edges.groupby('cue')['count'].transform('sum')

    # Calculate the normalized weight for each edge
    edges['weight'] = edges['count'] / total_count
    # Drop extra column
    edges = edges.drop(columns='count')

    # Convert the edges DataFrame to a list of tuples
    edges = list(edges.itertuples(index=False, name=None))
    return edges


def get_rus():
    data = pd.read_csv("original_csv/rus.csv", sep=';')
    g = nx.DiGraph()
    # Get all edges with correct edge weights
    edges = get_edges_rus(data)
    g.add_weighted_edges_from(edges)

    nx.write_graphml(g, "original_graphml/rus.graphml")
    print("Граф успешно записан в файл rus.graphml")


def get_dutch():
    data = pd.read_csv("original_csv/swow-nl.csv", sep=';')
    g = nx.DiGraph()
    # Get all edges with correct edge weights
    edges = get_edges_dutch(data)
    g.add_weighted_edges_from(edges)

    nx.write_graphml(g, "original_graphml/dutch.graphml")
    print("Граф успешно записан в файл dutch.graphml")


def get_en_swow(number):
    data = pd.read_csv(f"swow-en.r{number}.csv", sep='\t')
    g = nx.DiGraph()

    for i, row in data.iterrows():
        cue, response, strength = row['cue'], row['response'], row[f'R{number}.Strength']
        g.add_edge(cue, response, weight=strength)

    # Запись графа в файл GraphML
    nx.write_graphml(g, f"en_r{number}.graphml")

    print(f"Граф успешно записан в файл en_r{number}.graphml")


if __name__ == '__main__':
    get_rus()
    get_dutch()
    get_en_swow("1")
    get_en_swow("123")
    # get_en_usf()

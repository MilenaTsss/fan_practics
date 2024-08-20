import networkx as nx


def main():
    names = ['rus', 'en_r1', 'en_r123', 'dutch']
    for name in names:
        g = nx.read_graphml(f"original_graphml/{name}.graphml")
        scc_s = list(nx.strongly_connected_components(g))
        largest_scc = max(scc_s, key=len)
        subgraph = g.subgraph(largest_scc).copy()
        nx.write_graphml(subgraph, f"strong_graphml/{name}_main.graphml")
        print(f"Сильно связная компонента сохранена в 'final_graphml/{name}_main.graphml'")


if __name__ == '__main__':
    main()

import networkx as nx
import numpy as np
import csv


def get_limited_graph(name: str, limit: float):
    g = nx.read_graphml(name)
    edges_to_remove = [(u, v) for u, v, d in g.edges(data=True) if d["weight"] < limit]
    g.remove_edges_from(edges_to_remove)
    g.remove_nodes_from(list(nx.isolates(g)))

    return g


def main():
    names = ["rus", "en_r1", "en_r123", "dutch"]
    limits = [0.07, 0.08, 0.09, 0.1, 0.15, 0.2]

    # Open a CSV file for writing
    with open("graph_characteristics.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Name",
                "Limit",
                "Number of nodes",
                "Number of edges",
                "Is_strongly_connected",
                "Diameter",
                "Radius",
                "ASPL",
                "Transitivity",
                "ACC",
                "Clique number",
                "Density",
                "Average node degree",
                "Node degree variance",
                "Average node in-degree" "Node in-degree variance",
                "Average node out-degree",
                "Node out-degree variance",
            ]
        )

        for name in names:
            for limit in limits:
                print(name, limit)
                g = get_limited_graph(f"original_graphml/{name}.graphml", limit)

                number_of_nodes, number_of_edges = (
                    g.number_of_nodes(),
                    g.number_of_edges(),
                )
                print("Number of nodes:", number_of_nodes)
                print("Number of edges:", number_of_edges)
                
                is_strongly_connected = nx.is_strongly_connected(g)
                
                if is_strongly_connected:
                    diameter = nx.diameter(g)
                    print("Diameter:", diameter)
                    radius = nx.radius(g)
                    print("Radius:", radius)
                    aspl = round(nx.average_shortest_path_length(g), 4)
                    print("ASPL:", round(aspl))
                else:
                    print("Graph not strongly connected, diam et al for max SCC")
                    sub = g.subgraph(max(nx.strongly_connected_components(g), key=len))
                    diameter = nx.diameter(sub)
                    print("Diameter:", diameter)
                    radius = nx.radius(sub)
                    print("Radius:", radius)
                    aspl = round(nx.average_shortest_path_length(sub), 4)
                    print("ASPL:", round(aspl))

                transitivity = round(nx.transitivity(g), 4)
                acc = round(nx.average_clustering(g), 4)
                clique_number = nx.graph_clique_number(g.to_undirected())
                density = round(nx.density(g), 4)

                print("Transitivity:", transitivity)
                print("ACC:", acc)
                print("Clique number:", clique_number)
                print("Density:", density)

                degrees = np.array(list(dict(g.degree()).values()))
                in_degrees = np.array(list(dict(g.in_degree()).values()))
                out_degrees = np.array(list(dict(g.out_degree()).values()))

                print("Average node degree: {0:.2f}".format(degrees.mean()))
                print("Node degree variance: {0:.2f}".format(degrees.var()))
                print("Average node in-degree: {0:.2f}".format(in_degrees.mean()))
                print("Node in-degree variance: {0:.2f}".format(in_degrees.var()))
                print("Average node out-degree: {0:.2f}".format(out_degrees.mean()))
                print("Node out-degree variance: {0:.2f}".format(out_degrees.var()))

                writer.writerow(
                    [
                        name,
                        limit,
                        number_of_nodes,
                        number_of_edges,
                        is_strongly_connected,
                        diameter,
                        radius,
                        aspl,
                        transitivity,
                        acc,
                        clique_number,
                        density,
                        degrees.mean(),
                        degrees.var(),
                        in_degrees.mean(),
                        in_degrees.var(),
                        out_degrees.mean(),
                        out_degrees.var(),
                    ]
                )


if __name__ == "__main__":
    main()

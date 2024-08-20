import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigs


def get_limited_graph(name: str, limit: float):
    g = nx.read_graphml(name)
    edges_to_remove = [(u, v) for u, v, d in g.edges(data=True) if d['weight'] < limit]
    g.remove_edges_from(edges_to_remove)
    g.remove_nodes_from(list(nx.isolates(g)))

    return g


def main():
    names = ['rus', 'en_r1', 'en_r123', 'dutch']
    limits = [0.07, 0.08, 0.09, 0.1, 0.15, 0.2]
    for name in names:
        for limit in limits:
            print(name, limit)
            g = get_limited_graph(f'original_graphml/{name}.graphml', limit)
            print("Got graph with ", g.number_of_nodes(), g.number_of_edges())
            adj_matrix = nx.to_scipy_sparse_array(g)
            print("Got adj matrix")
            eigvals = eigs(adj_matrix, k=g.number_of_nodes() - 2, which='SM', return_eigenvectors=False)
            print("Got eigvals")
            np.savetxt(f'eigvals_with_limits/{name}/{limit}.csv', eigvals, delimiter=',')


if __name__ == '__main__':
    main()

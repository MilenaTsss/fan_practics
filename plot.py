import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def main():
    names = ["rus", "en_r1", "en_r123", "dutch"]
    limits = [0.07, 0.08, 0.09, 0.1, 0.2]
    for name in names:
        for limit in limits:
            print(name, limit)
            eigvals = np.genfromtxt(f"eigvals_with_limits/{name}/{limit}.csv", dtype=complex)
            plt.scatter(np.real(eigvals), np.imag(eigvals))

            plt.xlabel("Real")
            plt.ylabel("Imaginary")
            plt.title(f"Limit = {limit}, name = {name}, Simple eigvals")
            plt.savefig(f"eigvals_with_limits/{name}/{limit}.jpeg")
            plt.close('all')
            
            z_statistics = np.genfromtxt(f"eigvals_with_limits/{name}/z_{limit}.csv", dtype=complex)
            plt.scatter(np.real(z_statistics), np.imag(z_statistics))

            plt.xlabel("Real")
            plt.ylabel("Imaginary")
            plt.title(f"Limit = {limit}, name = {name}, Z statistics")
            plt.savefig(f"eigvals_with_limits/{name}/z_{limit}.jpeg")
            plt.close('all')
            


if __name__ == "__main__":
    print(111)
    main()

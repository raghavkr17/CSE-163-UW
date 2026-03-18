# Author: Raghav Krishna
# Course: CSE 163 THA4
# Description: Creates and saves a practice undirected
# graph and a directed digraph.

import networkx as nx
import matplotlib.pyplot as plt


def get_practice_graph() -> nx.Graph:
    """
    Creates and returns the undirected practice graph.
    Also used to save visualization in main.
    """
    g = nx.Graph()

    edges = [
        ("A", "B"), ("A", "C"),
        ("B", "C"), ("B", "D"),
        ("C", "D"), ("C", "F"),
        ("D", "E"), ("D", "F")
    ]

    g.add_edges_from(edges)
    return g


def get_practice_digraph() -> nx.DiGraph:
    """
    Creates and returns the directed practice graph.
    """
    g = nx.DiGraph()

    # Add ALL nodes 1–8 first
    g.add_nodes_from(range(1, 9))

    # Then add directed edges
    edges = [
        (1, 2), (1, 3),
        (2, 3),
        (3, 4), (3, 8),
        (6, 7)
    ]

    g.add_edges_from(edges)

    return g


def main() -> None:
    # Undirected graph
    g1 = get_practice_graph()
    nx.draw(g1, with_labels=True)
    plt.savefig("practice_graph.png")
    plt.clf()

    # Directed graph
    g2 = get_practice_digraph()
    nx.draw(g2, with_labels=True)
    plt.savefig("practice_digraph.png")


if __name__ == "__main__":
    main()

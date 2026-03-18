"""
Suh Young Choi

Creates a simple graph using networkx to
verify successful installation
"""

import networkx as nx
import matplotlib.pyplot as plt


def main():
    test = nx.Graph()
    test.add_edge('A', 'B')
    test.add_edge('B', 'C')

    nx.draw(test, with_labels=True)
    plt.savefig('test_graph.png')
    print('NetworkX is installed correctly!')


if __name__ == '__main__':
    main()

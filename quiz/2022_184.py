import networkx as nx
import networkx.algorithms.community as nx_comm
import matplotlib.pyplot as plt

g = nx.Graph()
g.add_edges_from(
    [
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 0],
        [0, 4],
        [1, 4],
        [2, 4],
        [3, 4],
        [2, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 6],
        [6, 10],
        [7, 10],
        [8, 10],
        [9, 10],
    ]
)

communities = [[0, 1, 2, 3], [4], [5], [6, 7, 8, 9, 10]]

options = {
    "node_color": "white",
    "edgecolors": "black",
    "with_labels": True,
}
nx.draw_shell(g, **options)
plt.savefig("2022_184.png")
plt.close()

print(f"Modularity = {nx_comm.modularity(g, communities)}")

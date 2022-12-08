import networkx as nx
import networkx.algorithms.community as nx_comm
import matplotlib.pyplot as plt

g = [nx.Graph(), nx.Graph()]

g[0].add_edges_from(
    [
        [1, 2],
        [2, 3],
        [3, 1],
        [4, 5],
        [5, 6],
        [6, 4],
        [7, 8],
        [8, 9],
        [9, 7],
        [3, 10],
        [6, 10],
        [9, 10],
    ]
)

g[1].add_edges_from(
    [
        [1, 2],
        [2, 3],
        [3, 1],
        [3, 4],
        [4, 5],
        [5, 6],
        [6, 4],
        [6, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [10, 6],
    ]
)

c = [
    [[1, 2, 3], [4, 5, 6, 10], [7, 8, 9]],
    [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10]],
]

options = {
    "node_color": "white",
    "edgecolors": "black",
    "with_labels": True,
}
for i in range(len(g)):
    nx.draw_shell(g[i], **options)
    plt.savefig(f"2021_068_{i}.png")
    plt.close()
    print(f"m(g({i+1})) = {nx_comm.modularity(g[i], c[i])}")

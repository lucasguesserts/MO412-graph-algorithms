import os

from rfa import *

NA = NetworkAnalyzer
import matplotlib.pyplot as plt

output_dir: str = "output/"
os.makedirs(output_dir, exist_ok=True)

if __name__ == "__main__":

    reader = WikiDataReader("data/original.txt")
    graph_maker = WikiDataGraphMaker()
    graph_maker.data = reader.data
    g = graph_maker.make()

    # basic statistics
    print("number_of_nodes = ", NA.number_of_nodes(g))
    print("number_of_edges = ", NA.number_of_edges(g))
    print(
        "weakely_connected_components = ",
        NA.weakely_connected_components(g)["number_of_connected_componets"],
    )
    print("has cycle = ", NA.has_cycle(g))

    # gephi
    NA.export_to_gephi(g, os.path.join(output_dir, "gephi.gexf"))

    # number of votes per year
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    gpy = GraphPerYear(reader.data)
    gpy.plot(
        ax,
        lambda g: NA.number_of_edges(g),
        y_label="number of votes",
    )
    fig.savefig(os.path.join(output_dir, "number_of_votes_per_year.png"))
    plt.close(fig)

    # cummulative degree distribution
    figure_title = "cumulative out-degree distribution"
    figure_file_name = os.path.join(
        output_dir, "cummulative_out_degree_distribution.png"
    )
    plot_degree_distribution(g, figure_title, figure_file_name)

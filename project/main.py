from src.WikiData import *
from src.NetworkAnalyzer import NetworkAnalyzer as NA
from src.cumulative_degree_distribution import plot_degree_distribution

if __name__ == "__main__":

    reader = WikiDataReader("data/original.txt")
    graph_maker = WikiDataGraphMaker(reader.data)
    g = graph_maker.make()
    print("number_of_nodes = ", NA.number_of_nodes(g))
    print("number_of_edges = ", NA.number_of_edges(g))
    print(
        "weakely_connected_components = ",
        NA.weakely_connected_components(g)["number_of_connected_componets"],
    )
    print("has cycle = ", NA.has_cycle(g))

    figure_title = "cumulative out-degree distribution"
    figure_file_name = "foo.png"
    plot_degree_distribution(g, figure_title, figure_file_name)

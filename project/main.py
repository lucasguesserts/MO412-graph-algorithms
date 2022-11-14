from rfa import *
NA = NetworkAnalyzer

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

    years, votes = NA.number_of_votes_per_year(g)

    plot_votes_per_year(years, votes)

    # NA.export_to_gephi(g, "foo.gexf")

    figure_title = "cumulative out-degree distribution"
    figure_file_name = "cummulative_out_degree_distribution.png"
    plot_degree_distribution(g, figure_title, figure_file_name)

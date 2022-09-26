import os
from typing import Callable

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import scipy.optimize

plt.rcParams.update({"text.usetex": True, "font.family": "Helvetica"})


def load_edge_list(file_path: str):
    edge_list = np.loadtxt(file_path, delimiter=",", dtype=int)
    return edge_list


def load_graph_from_file(file_path: str) -> nx.Graph:
    edge_list = load_edge_list(file_path)
    graph = nx.Graph()
    for edge in edge_list:
        graph.add_edge(*edge)
    return graph


def compute_degree_distribution(graph: nx.Graph):
    degree_of_vertices = list(map(lambda v: graph.degree(v), graph.nodes))
    count = np.bincount(degree_of_vertices)
    probabilities = count / len(degree_of_vertices)
    degrees = np.arange(0, np.max(degree_of_vertices) + 1, 1, dtype=int)
    degrees = degrees[1:]
    probabilities = probabilities[1:]
    assert np.abs(sum(probabilities) - 1) < 1.0e-6
    assert degrees[0] == 1
    assert len(degrees) == len(probabilities)
    return [degrees, probabilities]


def compute_power_law_furve_fit_function(
    degrees, probabilities
) -> tuple[str, Callable[[int], float]]:
    function = lambda k, C, gamma: C * k ** (-gamma)
    popt, pcov = scipy.optimize.curve_fit(function, degrees, probabilities)
    C = popt[0]
    gamma = popt[1]
    # perr = np.sqrt(np.diag(pcov))
    # C_error = perr[0]
    # gamma_error = perr[1]
    # x_name = "k"
    # y_name = "p_k"
    # print(f"Curve fit:")
    # print(f"\t{y_name} = f({x_name}) = C * {x_name}**(gamma)")
    # print(f"\tC = {C} +- {C_error}")
    # print(f"\tgamma = {gamma} +- {gamma_error}")
    # print("")
    function_as_string = (
        r"$p_{k} = "
        + "{:.2f}".format(C)
        + r" \cdot k^{-"
        + "{:.2f}".format(gamma)
        + r"}$"
    )
    function = lambda k: C * k ** (-gamma)
    return (function_as_string, function)


def plot_degree_distribution(
    graph: nx.Graph, figure_title: str, figure_file_name: str
) -> None:
    [degrees, probabilities] = compute_degree_distribution(graph)
    curve_fit_as_string, curve_fit_function = compute_power_law_furve_fit_function(
        degrees, probabilities
    )
    plt.loglog(
        degrees,
        probabilities,
        color="black",
        linestyle="",
        marker=".",
        label="degree distribution",
    )
    plt.loglog(
        degrees,
        curve_fit_function(degrees),
        color="gray",
        linestyle="--",
        label=curve_fit_as_string,
    )
    plt.title(figure_title)
    plt.xlabel(r"$k$")
    plt.ylabel(r"$p_{k}$")
    plt.ylim([None, 1])
    plt.legend(loc="best")
    plt.grid(which="both", alpha=0.4)
    print(f"Saving figure {figure_file_name}")
    plt.savefig(figure_file_name)
    plt.close()
    return


if __name__ == "__main__":
    current_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = os.path.join(os.path.abspath(os.getcwd()), "output")
    os.makedirs(output_dir, exist_ok=True)
    for data_file_name in ["net1.csv", "net2.csv"]:
        network_file_path = os.path.join(current_dir, "data/", data_file_name)
        graph = load_graph_from_file(network_file_path)
        figure_file_name = os.path.join(
            output_dir, data_file_name.replace("csv", "png")
        )
        figure_title = data_file_name.replace(".csv", "")
        plot_degree_distribution(graph, figure_title, figure_file_name)

import os
import pickle
from typing import Callable

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import scipy.optimize

plt.rcParams.update({"text.usetex": True, "font.family": "Helvetica"})


def load_graph(file_name: str) -> nx.Graph:
    with open(file_name, "rb") as file:
        graph: nx.Graph = pickle.load(file)
    return graph


def compute_degree_distribution(graph: nx.MultiDiGraph):
    degree_of_vertices = list(map(lambda v: graph.in_degree(v), graph.nodes))
    count = np.bincount(degree_of_vertices)
    probabilities = count / len(degree_of_vertices)
    degrees = np.arange(0, np.max(degree_of_vertices) + 1, 1, dtype=int)
    degrees = degrees[1:]
    probabilities = probabilities[1:]
    # remove zeros
    p = []
    d = []
    for i in range(len(probabilities)):
        if probabilities[i] > 1e-6 and degrees[i] > 20:
            p.append(probabilities[i])
            d.append(degrees[i])
    probabilities = np.array(p)
    degrees = np.array(d)
    # cumulative distribution
    probabilities = np.array(list(map(
        lambda i: np.sum(probabilities[i:]),
        range(len(probabilities))
    )))
    # assert np.abs(sum(probabilities) - 1) < 1.0e-6
    assert len(degrees) == len(probabilities)
    return [degrees, probabilities]


def compute_power_law_furve_fit_function(
    degrees, probabilities
) -> tuple[str, Callable[[int], float]]:
    function = lambda k, C, gamma: C * k ** (-gamma + 1)
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
        + r"+1}$"
    )
    function = lambda k: C * k ** (-gamma + 1)
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
    # plt.ylim([None, 1])
    plt.legend(loc="best")
    plt.grid(which="both", alpha=0.4)
    plt.savefig(figure_file_name)
    plt.close()
    return


if __name__ == "__main__":
    output_dir = os.path.join(os.path.abspath(os.getcwd()), "output")
    checkpoint_list: list[int] = [100, 1_000, 10_000]
    for checkpoint in checkpoint_list:
        file_name: str = os.path.join(
            output_dir,
            f"{checkpoint}.pkl"
        )
        graph = load_graph(file_name)
        figure_title = r"cumulative distribution for $k > 20$ and " + f"{checkpoint} nodes"
        figure_file_name = os.path.join(
            output_dir,
            f"{checkpoint}.png"
        )
        plot_degree_distribution(graph, figure_title, figure_file_name)

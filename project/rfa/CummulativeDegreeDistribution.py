import os
from typing import Callable

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import scipy.optimize

from .DegreeType import DegreeType

plt.rcParams.update({"text.usetex": True, "font.family": "Helvetica"})


class CummulativeDegreeDistribution:
    def __init__(
        self, graph: nx.MultiDiGraph, degree_type: DegreeType = DegreeType.OUT
    ):
        self._graph = graph
        self._degree_type = degree_type
        if self._degree_type not in DegreeType:
            raise ValueError(
                f"degree_type must be one of {[e.value for e in DegreeType]}, but '{degree_type}' was provided"
            )
        return

    @property
    def title(self) -> str:
        return self._degree_type.__str__().split(".")[-1].title() + "Degree Distribution"

    @property
    def file_name(self) -> str:
        return self._degree_type.__str__().split(".")[-1].lower() + "_degree_distribution.png"

    def plot(self, ax: plt.Axes) -> None:
        [degrees, probabilities] = self._compute_degree_distribution()
        (
            curve_fit_as_string,
            curve_fit_function,
        ) = self._compute_power_law_furve_fit_function(degrees, probabilities)
        ax.loglog(
            degrees,
            probabilities,
            color="black",
            linestyle="",
            marker=".",
            label="degree distribution",
        )
        ax.loglog(
            degrees,
            curve_fit_function(degrees),
            color="gray",
            linestyle="--",
            label=curve_fit_as_string,
        )
        ax.set_title(self.title)
        ax.set_xlabel(r"$k$")
        ax.set_ylabel(r"$p_{k}$")
        # ax.set_ylim([None, 1])
        ax.legend(loc="best")
        ax.grid(which="both", alpha=0.4)
        return

    def _compute_degree_distribution(self):
        graph_degree_function = (
            self._graph.out_degree
            if self._degree_type == DegreeType.OUT
            else self._graph.in_degree
        )
        degree_of_vertices = list(
            map(lambda v: graph_degree_function(v), self._graph.nodes)
        )
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
        probabilities = np.array(
            list(map(lambda i: np.sum(probabilities[i:]), range(len(probabilities))))
        )
        # assert np.abs(sum(probabilities) - 1) < 1.0e-6
        assert len(degrees) == len(probabilities)
        return [degrees, probabilities]

    def _compute_power_law_furve_fit_function(
        self, degrees, probabilities
    ) -> tuple[str, Callable[[int], float]]:
        function = lambda k, C, gamma: C * k ** (-gamma + 1)
        popt, pcov = scipy.optimize.curve_fit(function, degrees, probabilities)
        C = popt[0]
        gamma = popt[1]
        function_as_string = (
            r"$p_{k} = "
            + "{:.2f}".format(C)
            + r" \cdot k^{-"
            + "{:.2f}".format(gamma)
            + r"+1}$"
        )
        function = lambda k: C * k ** (-gamma + 1)
        return (function_as_string, function)

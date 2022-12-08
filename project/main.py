import itertools
import math
import os
import pickle

from rfa import *

NA = NetworkAnalyzer
import matplotlib.pyplot as plt

output_dir: str = "output/"
os.makedirs(output_dir, exist_ok=True)

# reader = WikiDataReader("data/original.txt")

# graph_maker = WikiDataGraphMaker()
# graph_maker.data = reader.data
# g = graph_maker.make()

if __name__ == "__main__":
    # data_on_years = GraphPerYear(
    #     reader.data,
    #     build_robustness = True
    # )
    # with open(os.path.join(output_dir, "per_year.pkl"), "wb") as file:
    #     pickle.dump(data_on_years, file)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)

    with open(os.path.join(output_dir, "per_year.pkl"), "rb") as file:
        data = pickle.load(file)

    tail_cut = [math.ceil(0.15 * len(vs.ps)) for vs in data.robustness.values()]
    colors = ['red', 'green', 'blue', 'cyan', 'pink']
    linestyle = ['-', '--']
    cl = itertools.product(colors, linestyle)
    for year, r, tc, clp in zip(data.robustness.keys(), data.robustness.values(), tail_cut, cl):
        fs, ps = r.fs, r.ps
        ax.plot(fs[:-tc], ps[:-tc], color=clp[0], linestyle=clp[1], label=f"{year}")
    ax.grid(True)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_title("Network under attack")
    ax.legend(loc="best")
    fig.savefig(os.path.join(output_dir, "robustness_per_year.png"))
    plt.close(fig)

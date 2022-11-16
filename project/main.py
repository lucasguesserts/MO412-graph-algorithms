import os

from rfa import *

NA = NetworkAnalyzer
import matplotlib.pyplot as plt

output_dir: str = "output/"
os.makedirs(output_dir, exist_ok=True)

reader = WikiDataReader("data/original.txt")

graph_maker = WikiDataGraphMaker()
graph_maker.data = reader.data
g = graph_maker.make()

if __name__ == "__main__":
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    gpy = GraphPerYear(reader.data)
    gpy.plot_quartiles(
        ax=ax,
        degree_type=DegreeType.IN,
        outliers=False
    )
    fig.savefig(os.path.join(output_dir, "quartiles_in.png"))
    plt.close(fig)

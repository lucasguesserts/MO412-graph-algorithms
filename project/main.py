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
    output_file = os.path.join(output_dir, "robustness.pkl")
    r = RobustnessToAttack(g)
    r.save(output_file)

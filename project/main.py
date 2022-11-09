from src.WikiData import *

if __name__ == "__main__":
    reader = WikiDataReader("data/original.txt")
    graph_maker = WikiDataGraphMaker(reader.data)
    graph = graph_maker.make()
    print(graph.number_of_nodes())


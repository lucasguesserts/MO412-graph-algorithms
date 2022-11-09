import networkx as nx

class NetworkAnalyzer:
    @staticmethod
    def number_of_nodes(g: nx.MultiDiGraph) -> int:
        return g.number_of_nodes()

    @staticmethod
    def number_of_edges(g: nx.MultiDiGraph) -> int:
        return g.number_of_edges()

    @staticmethod
    def weakely_connected_components(dg: nx.MultiDiGraph) -> int:
        components = list(nx.weakly_connected_components(dg))
        return {
            "components": components,
            "number_of_connected_componets": len(components)
        }


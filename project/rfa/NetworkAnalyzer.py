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

    @staticmethod
    def has_cycle(dg: nx.MultiDiGraph) -> int:
        try:
            cycle = nx.find_cycle(dg)
            return True
        except nx.NetworkXNoCycle:
            return False

    @staticmethod
    def export_to_gephi(dg: nx.MultiDiGraph, file_path: str) -> None:
        with open(file_path, "w") as file:
            linefeed = chr(10)
            s = linefeed.join(nx.generate_gexf(dg))
            for line in nx.generate_gexf(dg):
                file.write(line)
        return

    @staticmethod
    def _count_by_property(dg: nx.MultiDiGraph, property_name: str, value) -> int:
        property_value_list = list(map(
            lambda arc: dg.get_edge_data(*arc)[0][property_name],
            dg.edges()
        ))
        return len(list(filter(
            lambda x: x == value,
            property_value_list
        )))

    @staticmethod
    def number_of_votes_per_year(dg: nx.MultiDiGraph) -> list[int]:
        years = list(range(2003, 2013+1))
        votes_per_year: list[int] = list(map(
            lambda year: NetworkAnalyzer._count_by_property(dg, "year", year),
            years
        ))
        return [years, votes_per_year]

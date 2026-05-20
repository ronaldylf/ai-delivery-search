from __future__ import annotations

import networkx as nx

from delivery_search.domain.point import Point
from delivery_search.search.result import RouteResult


class DroneRouteFinder:
    """Busca de rota com A* e heurística euclidiana (admissível para voo em linha reta)."""

    def __init__(self, graph: nx.Graph) -> None:
        self._graph = graph

    def find_route(self, origin_id: str, destination_id: str) -> RouteResult:
        if origin_id not in self._graph:
            raise ValueError(f"Origem desconhecida: {origin_id}")
        if destination_id not in self._graph:
            raise ValueError(f"Destino desconhecido: {destination_id}")

        def heuristic(current_id: str, target_id: str) -> float:
            current = Point(*self._graph.nodes[current_id]["pos"])
            target = Point(*self._graph.nodes[target_id]["pos"])
            return current.distance_to(target)

        try:
            node_ids = nx.astar_path(
                self._graph,
                origin_id,
                destination_id,
                heuristic=heuristic,
                weight="weight",
            )
            total_distance_m = nx.astar_path_length(
                self._graph,
                origin_id,
                destination_id,
                heuristic=heuristic,
                weight="weight",
            )
        except nx.NetworkXNoPath as error:
            raise ValueError(
                f"Não há rota aérea permitida entre {origin_id} e {destination_id}."
            ) from error

        return RouteResult(
            node_ids=tuple(node_ids),
            total_distance_m=total_distance_m,
        )

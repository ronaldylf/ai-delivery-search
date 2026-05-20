from __future__ import annotations

from collections.abc import Sequence

import networkx as nx

from delivery_search.domain.point import Point
from delivery_search.domain.waypoint import Waypoint
from delivery_search.obstacles.protocol import Obstacle


class CityGraphBuilder:
    """Monta o grafo de rotas aéreas permitidas entre waypoints da cidade."""

    def __init__(
        self,
        *,
        max_link_distance_m: float,
        obstacles: Sequence[Obstacle] = (),
    ) -> None:
        self._max_link_distance_m = max_link_distance_m
        self._obstacles = tuple(obstacles)

    def build(self, waypoints: Sequence[Waypoint]) -> nx.Graph:
        graph = nx.Graph()
        positions: dict[str, Point] = {}

        for waypoint in waypoints:
            graph.add_node(
                waypoint.id,
                label=waypoint.label,
                kind=waypoint.kind.value,
                pos=(waypoint.position.x, waypoint.position.y),
            )
            positions[waypoint.id] = waypoint.position

        waypoint_ids = [waypoint.id for waypoint in waypoints]
        for index, origin_id in enumerate(waypoint_ids):
            origin = positions[origin_id]
            for destination_id in waypoint_ids[index + 1 :]:
                destination = positions[destination_id]
                if not self._can_fly_directly(origin, destination):
                    continue
                distance_m = origin.distance_to(destination)
                graph.add_edge(origin_id, destination_id, weight=distance_m)

        return graph

    def _can_fly_directly(self, origin: Point, destination: Point) -> bool:
        distance_m = origin.distance_to(destination)
        if distance_m > self._max_link_distance_m:
            return False
        return not any(
            obstacle.blocks_segment(origin, destination) for obstacle in self._obstacles
        )

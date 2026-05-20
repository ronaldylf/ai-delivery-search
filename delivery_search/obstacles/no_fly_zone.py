from __future__ import annotations

from dataclasses import dataclass

from delivery_search.domain.point import Point
from delivery_search.obstacles.geometry import closest_point_on_segment


@dataclass(frozen=True, slots=True)
class NoFlyZone:
    """Zona de exclusão aérea circular (ex.: área militar, aeroporto)."""

    name: str
    center: Point
    radius_m: float

    def blocks_segment(self, start: Point, end: Point) -> bool:
        if start.distance_to(self.center) <= self.radius_m:
            return True
        if end.distance_to(self.center) <= self.radius_m:
            return True

        closest = closest_point_on_segment(self.center, start, end)
        return closest.distance_to(self.center) < self.radius_m

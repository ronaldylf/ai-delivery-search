from __future__ import annotations

from dataclasses import dataclass

from delivery_search.domain.point import Point
from delivery_search.obstacles.geometry import segments_intersect


@dataclass(frozen=True, slots=True)
class Building:
    """Prédio alto modelado como retângulo que bloqueia voo em linha reta."""

    name: str
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def blocks_segment(self, start: Point, end: Point) -> bool:
        if self._contains(start) or self._contains(end):
            return True

        corners = (
            Point(self.x_min, self.y_min),
            Point(self.x_max, self.y_min),
            Point(self.x_max, self.y_max),
            Point(self.x_min, self.y_max),
        )
        edges = (
            (corners[0], corners[1]),
            (corners[1], corners[2]),
            (corners[2], corners[3]),
            (corners[3], corners[0]),
        )
        return any(segments_intersect(start, end, edge[0], edge[1]) for edge in edges)

    def _contains(self, point: Point) -> bool:
        return self.x_min <= point.x <= self.x_max and self.y_min <= point.y <= self.y_max

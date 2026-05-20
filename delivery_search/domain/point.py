from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point:
    """Posição no plano urbano (metros em coordenadas X, Y)."""

    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

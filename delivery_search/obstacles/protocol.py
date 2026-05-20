from __future__ import annotations

from typing import Protocol

from delivery_search.domain.point import Point


class Obstacle(Protocol):
    """Restrição que pode bloquear um trecho aéreo direto entre dois pontos."""

    name: str

    def blocks_segment(self, start: Point, end: Point) -> bool: ...

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from delivery_search.domain.point import Point


class WaypointKind(StrEnum):
    HOSPITAL = "hospital"
    HEALTH_POST = "health_post"
    HUB = "hub"


@dataclass(frozen=True, slots=True)
class Waypoint:
    """Ponto de referência da cidade (vértice do grafo)."""

    id: str
    label: str
    position: Point
    kind: WaypointKind = WaypointKind.HUB

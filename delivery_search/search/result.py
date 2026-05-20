from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RouteResult:
    """Rota encontrada entre origem e destino."""

    node_ids: tuple[str, ...]
    total_distance_m: float

    @property
    def hops(self) -> int:
        return max(0, len(self.node_ids) - 1)

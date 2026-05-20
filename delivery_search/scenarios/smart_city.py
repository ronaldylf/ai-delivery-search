from __future__ import annotations

import networkx as nx

from delivery_search.domain.point import Point
from delivery_search.domain.waypoint import Waypoint, WaypointKind
from delivery_search.graph.builder import CityGraphBuilder
from delivery_search.obstacles.building import Building
from delivery_search.obstacles.no_fly_zone import NoFlyZone
from delivery_search.search.pathfinder import DroneRouteFinder
from delivery_search.search.result import RouteResult


def build_demo_graph() -> nx.Graph:
    """Cenário urbano: hospital central entrega medicamentos a um posto periférico."""
    waypoints = (
        Waypoint("hospital", "Hospital Central", Point(10, 10), WaypointKind.HOSPITAL),
        Waypoint("norte_1", "Praça Norte", Point(30, 55)),
        Waypoint("norte_2", "Avenida Norte", Point(55, 60)),
        Waypoint("centro_1", "Ponte Centro", Point(45, 35)),
        Waypoint("centro_2", "Mercado Central", Point(70, 40)),
        Waypoint("leste_1", "Parque Leste", Point(90, 55)),
        Waypoint("sul_1", "Terminal Sul", Point(35, 15)),
        Waypoint("sul_2", "Bairro Industrial", Point(65, 18)),
        Waypoint(
            "posto_vila_verde",
            "Posto Vila Verde",
            Point(95, 20),
            WaypointKind.HEALTH_POST,
        ),
    )

    obstacles = (
        NoFlyZone("Base Aérea Militar", Point(50, 45), radius_m=14),
        Building("Torre Comercial Orion", 58, 28, 72, 48),
        Building("Complexo Antenas 5G", 38, 38, 48, 50),
    )

    builder = CityGraphBuilder(
        max_link_distance_m=45,
        obstacles=obstacles,
    )
    return builder.build(waypoints)


def solve_demo_delivery() -> RouteResult:
    graph = build_demo_graph()
    finder = DroneRouteFinder(graph)
    return finder.find_route("hospital", "posto_vila_verde")


def format_route_report(graph: nx.Graph, route: RouteResult) -> str:
    lines = [
        "=== Entrega de medicamentos por drone (cidade inteligente) ===",
        "",
        f"Origem: {graph.nodes[route.node_ids[0]]['label']}",
        f"Destino: {graph.nodes[route.node_ids[-1]]['label']}",
        f"Trechos aéreos: {route.hops}",
        f"Distância total (peso g): {route.total_distance_m:.1f} m",
        "",
        "Rota:",
    ]

    for index, node_id in enumerate(route.node_ids):
        label = graph.nodes[node_id]["label"]
        pos = graph.nodes[node_id]["pos"]
        prefix = "  └─" if index == len(route.node_ids) - 1 else "  ├─"
        lines.append(f"{prefix} {label} ({pos[0]:.0f}, {pos[1]:.0f})")

    lines.extend(
        [
            "",
            "Heurística h(n): distância euclidiana até o destino (admissível).",
            "Limitações do modelo: sem vento em tempo real nem carga variável na bateria.",
        ]
    )
    return "\n".join(lines)

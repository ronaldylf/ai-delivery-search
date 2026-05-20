from delivery_search.scenarios.smart_city import (
    build_demo_graph,
    format_route_report,
    solve_demo_delivery,
)


def main() -> None:
    graph = build_demo_graph()
    route = solve_demo_delivery()
    print(format_route_report(graph, route))


if __name__ == "__main__":
    main()

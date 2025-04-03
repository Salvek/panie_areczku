import math
from src.point import Point
from typing import List


def move_truck_along_route(start: Point, route: List[Point]) -> dict:
    total_distance = 0
    current = start
    history = [start]
    steps = []

    print(f"Start z punktu ({current.x}, {current.y})")

    for next_point in route:
        dx = current.x - next_point.x
        dy = current.y - next_point.y
        distance = math.sqrt(dx**2 + dy**2)
        steps.append({
            "from": (current.x, current.y),
            "to": (next_point.x, next_point.y),
            "distance": round(distance, 2),
            "from_id": str(current.id),
            "to_id": str(next_point.id)
        })
        total_distance += distance
        print(f"Jedzie do ({next_point.x}, {next_point.y}) | dystans: {distance:.2f}")
        current = next_point
        history.append(current)

    print(f"Trasa zakończona. Łączny dystans: {total_distance:.2f}")

    return {
        "total_distance": round(total_distance, 2),
        "visited": history,
        "visited_ids": [str(p.id) for p in history],
        "steps": steps
    }


def plan_route(start: Point, targets: List[Point]) -> List[Point]:
    route = []
    current = start
    remaining = targets.copy()

    while remaining:
        next_point = min(remaining, key=lambda p: math.dist((current.x, current.y), (p.x, p.y)))
        route.append(next_point)
        remaining.remove(next_point)
        current = next_point

    return route

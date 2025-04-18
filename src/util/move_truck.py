import math
from point import Point
from typing import List

def tuna_devourer(distance: float, tuna_weight: int) -> int:
    return tuna_weight - int(math.ceil(distance)) if(tuna_weight>int(math.ceil(distance))) else 0

def step(from_p: Point, to_p: Point, dist: float):
    return {
        "from": (from_p.x, from_p.y),
        "to": (to_p.x, to_p.y),
        "distance": round(dist, 2),
        "from_id": str(from_p.id),
        "to_id": str(to_p.id),
    }

def preload_for_route(truck, start: Point, route: List[Point]):
    demands = {p: 0 for p in truck.cargo.keys()}
    total_dist = 0.0
    curr = start
    for p in route:
        for prod, q in p.cargo.items():
            if q < 0:
                demands[prod] += abs(q)
        total_dist += curr.calc_dist(p)
        curr = p

    if truck.cat and demands["tuńczyk"] > 0:
        cat_snack = math.ceil(total_dist)
        demands["tuńczyk"] += cat_snack
        print(f"{truck.name}: kot zje dodatkowo {cat_snack}kg tuńczyka na trasie.")

    for prod, qty in demands.items():
        loaded = truck.load_from_warehouse(prod, qty)
        print(f"{truck.name}: załadowano {loaded}kg {prod} na początek trasy.")

def move_truck_along_route(truck, start: Point, route: List[Point]) -> dict:
    total_distance = 0.0
    steps = []
    current = start

    preload_for_route(truck, start, route)

    print(f"\n--- {truck.name} START TRASY ---")
    for point in route:
        while any(q != 0 for q in point.cargo.values()):
            dist = current.calc_dist(point)
            if truck.cat and truck.cargo["tuńczyk"] > 0:
                before = truck.cargo["tuńczyk"]
                after = tuna_devourer(dist, before)
                eaten = before - after
                truck.cargo["tuńczyk"] = after
                if eaten > 0:
                    print(f"{truck.name}: kot zjadł {eaten}kg tuńczyka podczas jazdy ({dist:.2f}km).")
            steps.append(step(current, point, dist))
            total_distance += dist
            current = point
            print(f"{truck.name}: jedzie do punktu {point.id}")

            for prod, need in point.cargo.items():
                if need < 0 and truck.cargo.get(prod, 0) < abs(need):
                    print(f"{truck.name}: brak {prod} do dostawy ({abs(need)}kg), wracam do magazynu.")
                    d_back = current.calc_dist(start)
                    steps.append(step(current, start, d_back))
                    total_distance += d_back
                    current = start
                    to_load = abs(need) - truck.cargo.get(prod, 0)
                    loaded = truck.load_from_warehouse(prod, to_load)
                    print(f"{truck.name}: załadowano dodatkowo {loaded}kg {prod} w magazynie.")
                    d_go = current.calc_dist(point)
                    steps.append(step(current, point, d_go))
                    total_distance += d_go
                    current = point

            for prod, need in list(point.cargo.items()):
                if need < 0:
                    to_deliver = min(abs(need), truck.cargo.get(prod, 0))
                    if to_deliver > 0:
                        delivered = truck.deliver(prod, to_deliver)
                        point.cargo[prod] += delivered
                        print(f"{truck.name}: dostarczono {delivered}kg {prod}.")

            for prod, supply in list(point.cargo.items()):
                if supply > 0 and (not truck.can_load(prod, point) or truck.space_left < supply):
                    print(f"{truck.name}: brak miejsca lub konflikt dla {prod} ({supply}kg), wracam do magazynu.")
                    d_back = current.calc_dist(start)
                    steps.append(step(current, start, d_back))
                    total_distance += d_back
                    current = start
                    for p in list(truck.cargo):
                        if truck.cargo[p] > 0:
                            print(f"{truck.name}: rozładowuję {truck.cargo[p]}kg {p} w magazynie.")
                    truck.unload_cargo()
                    d_go = current.calc_dist(point)
                    steps.append(step(current, point, d_go))
                    total_distance += d_go
                    current = point

            for prod, supply in list(point.cargo.items()):
                if supply > 0 and truck.can_load(prod, point):
                    to_pick = min(truck.space_left, supply)
                    truck.pick_up(prod, to_pick)
                    point.cargo[prod] -= to_pick
                    print(f"{truck.name}: odebrano {to_pick}kg {prod}.")

        print(f"{truck.name}: punkt {point.id} obsłużony w całości.")

    print(f"{truck.name} zakończył trasę. Dystans: {total_distance:.2f} km\n")
    return {"total_distance": round(total_distance, 2), "steps": steps}

def plan_route(start: Point, targets: List[Point]) -> List[Point]:
    route = []
    current = start
    remaining = targets.copy()
    while remaining:
        next_point = min(
            remaining, key=lambda p: math.dist((current.x, current.y), (p.x, p.y))
        )
        route.append(next_point)
        remaining.remove(next_point)
        current = next_point
    return route

def print_board(board: List[Point]):
    print("\n=== STAN PUNKTÓW ===")
    for p in board:
        print(
            f"{str(p.id)[:8]} | Tuna: {p.cargo.get('tuńczyk', 0)}kg | "
            f"Oranges: {p.cargo.get('pomarańcze', 0)}kg | "
            f"Uranium: {p.cargo.get('uran', 0)}kg | "
            f"Warehouse: {p.is_warehouse}"
        )

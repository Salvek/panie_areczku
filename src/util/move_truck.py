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
    demands = {}

    # Zlicza zapotrzebowanie z całej trasy
    for point in route:
        for prod, q in point.cargo.items():
            if q < 0:  # tylko zapotrzebowanie
                demands[prod] = demands.get(prod, 0) + abs(q)

    # Dodaje tuńczyka dla kota
    if truck.cat:
        total_dist = 0.0
        curr = start
        for p in route:
            total_dist += curr.calc_dist(p)
            curr = p
        cat_snack = math.ceil(total_dist)
        demands["tuńczyk"] = demands.get("tuńczyk", 0) + cat_snack
        print(f"{truck.name}: kot zje {cat_snack}kg tuńczyka na trasie.")

    # Załaduj wszystko co się da
    for prod, qty in demands.items():
        if qty <= 0:
            continue
        loaded = truck.load_from_warehouse(prod, qty)
        if loaded > 0:
            print(f"{truck.name}: załadowano {loaded}kg {prod} na początek trasy.")
        if loaded < qty:
            print(f"{truck.name}: NIE załadowano pełnej ilości {prod} ({qty}kg), tylko {loaded}kg.")

def move_truck_along_route(truck, start: Point, route: List[Point]) -> dict:
    total_distance = 0.0
    steps = []
    current = start
    skipped_points = []
    attempts = {}

    preload_for_route(truck, start, route)

    print(f"\n--- {truck.name} START TRASY ---")
    full_route = route.copy()  # do obsługi głównej trasy + późniejszych prób

    while full_route:
        point = full_route.pop(0)

        point_id = str(point.id)
        attempts[point_id] = attempts.get(point_id, 0) + 1
        if attempts[point_id] > 3:
            print(f"{truck.name}: Zbyt wiele prób obsługi punktu {point_id}, pomijam trwale.")
            continue

        while any(q != 0 for q in point.cargo.values()):
            dist = current.calc_dist(point)
            if truck.cat and truck.cargo.get("tuńczyk", 0) > 0:
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

            # DOSTAWA
            delivery_failed = False
            for prod, need in list(point.cargo.items()):
                if need < 0:
                    available = truck.cargo.get(prod, 0)
                    if available < abs(need):
                        missing = abs(need) - available
                        if truck.space_left < missing:
                            print(f"{truck.name}: nie ma miejsca na brakujące {missing}kg {prod}, pomijam punkt.")
                            skipped_points.append(point)
                            delivery_failed = True
                            break

                        print(f"{truck.name}: brak {prod} do dostawy ({abs(need)}kg), próbuję uzupełnić po drodze...")

                        found_source = False
                        for alt_point in route:
                            if alt_point.id == point.id:
                                continue
                            if alt_point.cargo.get(prod, 0) > 0:
                                to_pick = min(missing, alt_point.cargo[prod], truck.space_left)
                                if to_pick > 0:
                                    d_alt = current.calc_dist(alt_point)
                                    steps.append(step(current, alt_point, d_alt))
                                    total_distance += d_alt
                                    current = alt_point
                                    truck.pick_up(prod, to_pick)
                                    alt_point.cargo[prod] -= to_pick
                                    print(f"{truck.name}: odebrano {to_pick}kg {prod} z punktu {alt_point.id} (zamiast magazynu).")
                                    found_source = True
                                    break

                        if not found_source:
                            print(f"{truck.name}: nie znaleziono alternatywnego źródła {prod}, wracam do magazynu.")
                            d_back = current.calc_dist(start)
                            steps.append(step(current, start, d_back))
                            total_distance += d_back
                            current = start
                            loaded = truck.load_from_warehouse(prod, missing)
                            print(f"{truck.name}: załadowano {loaded}kg {prod} w magazynie.")

                    # Teraz dostawa
                    to_deliver = min(abs(point.cargo[prod]), truck.cargo.get(prod, 0))
                    if to_deliver > 0:
                        delivered = truck.deliver(prod, to_deliver)
                        point.cargo[prod] += delivered
                        print(f"{truck.name}: dostarczono {delivered}kg {prod}.")

            if delivery_failed:
                break  # Wyjdź z obsługi tego punktu (zostanie obsłużony później)

            # ODBIÓR
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

                if supply > 0 and truck.can_load(prod, point):
                    to_pick = min(truck.space_left, supply)
                    truck.pick_up(prod, to_pick)
                    point.cargo[prod] -= to_pick
                    print(f"{truck.name}: odebrano {to_pick}kg {prod}.")

        print(f"{truck.name}: punkt {point.id} obsłużony w całości.")

    # Spróbuj ponownie pominięte punkty
    if skipped_points:
        print(f"{truck.name}: podejście 2 do pominiętych punktów.")
        full_route.extend(skipped_points)
        skipped_points.clear()

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

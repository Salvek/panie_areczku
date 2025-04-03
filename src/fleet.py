import random
from typing import List
from point import Point
from src.truck import Truck
from config import TRUCK_TYPES


def _generate_random_fleet() -> List[Truck]:
    fleet = []
    num_trucks = random.randint(3, 6)
    for i in range(num_trucks):
        color = random.choice(list(TRUCK_TYPES.keys()))
        name = f"Truck-{i+1} ({color})"
        capacity = TRUCK_TYPES[color]
        fleet.append(Truck(name, capacity))
    print(f"🛠️  Wygenerowano {len(fleet)} ciężarówek:")
    for t in fleet:
        print(f"   • {t.name} | {t.capacity}kg")
    return fleet


class Fleet:
    def __init__(self):
        self.trucks = _generate_random_fleet()
        self.routes_assigned = 0

    def assign_routes(self, routes: List[List[Point]], starts: List[Point]):
        """
        Przypisuje trasy do ciężarówek z listy tras.
        """
        for i, route in enumerate(routes):
            if i < len(self.trucks):
                self.trucks[i].assign_route(starts[i], route)
                self.routes_assigned += 1
            else:
                print("⚠️ Brakuje ciężarówek do obsłużenia trasy.")

    def dispatch(self):
        for truck in self.trucks:
            if truck.route:
                truck.run()

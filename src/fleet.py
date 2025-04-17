import random
from typing import List
from point import Point
from truck import Truck
from config import TRUCK_TYPES, CATS_NUMBER, TRUCK_MIN_NUMBER , TRUCK_MAX_NUMBER


class Fleet:
    def __init__(self):
        self.trucks = self.__generate_random_fleet()
        self.routes_assigned = 0

    @staticmethod
    def __generate_random_fleet() -> List[Truck]:
        fleet = []
        num_trucks = random.randint(TRUCK_MIN_NUMBER, TRUCK_MAX_NUMBER)
        trucker_cats = []
        for _ in range(CATS_NUMBER):
            while len(trucker_cats) < CATS_NUMBER:
                trucker_cat = random.randint(1,num_trucks)
                if trucker_cat not in trucker_cats:
                    trucker_cats.append(trucker_cat)
        for i in range(num_trucks):
            color = random.choice(list(TRUCK_TYPES.keys()))
            name = f"Truck-{i + 1} ({color})"
            capacity = TRUCK_TYPES[color]
            if(i+1 in trucker_cats):
                fleet.append(Truck(name, capacity, cat = True))
            else:
                fleet.append(Truck(name, capacity, cat = False))
        print(f"Wygenerowano {len(fleet)} ciężarówek:")
        for t in fleet:
            print(f"   • {t.name} | {t.capacity}kg | Zawiera kota: {t.cat}")
        return fleet

    def assign_routes(self, routes: List[List[Point]], starts: List[Point]):
        for i, route in enumerate(routes):
            if i < len(self.trucks):
                self.trucks[i].assign_route(starts[i], route)
                self.routes_assigned += 1
            else:
                print("Brakuje ciężarówek do obsłużenia trasy.")

    def dispatch(self):
        for truck in self.trucks:
            if truck.route:
                truck.run()


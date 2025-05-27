import uuid
from typing import List
from point import Point
from util.move_truck import move_truck_along_route

class Truck:
    def __init__(self, name: str, capacity: int, cat: bool):
        self.id = uuid.uuid4()
        self.name = name
        self.capacity = capacity
        self.cargo = {"tuńczyk": 0, "pomarańcze": 0, "uran": 0}
        self.cat = cat
        self.route: List[Point] = []
        self.start: Point = None
        self.total_distance = 0.0
        self.result = {}

    @property
    def space_left(self) -> int:
        return self.capacity - sum(self.cargo.values())

    def assign_route(self, start: Point, route: List[Point]):
        self.start = start
        self.route = route

    def can_load(self, prod_type: str, point: Point) -> bool:
        if point.cargo[prod_type] > 0:
            if (prod_type == "uran" and self.cargo.get("pomarańcze", 0) > 0) or \
               (prod_type == "pomarańcze" and self.cargo.get("uran", 0) > 0):
                return False
            return self.space_left > 0
        elif point.cargo[prod_type] < 0:
            return self.cargo.get(prod_type, 0) > 0
        return True

    def deliver(self, product: str, qty: int) -> int:
        available = min(self.cargo.get(product, 0), qty)
        if available <= 0:
            return 0
        self.cargo[product] -= available
        return available

    def pick_up(self, product: str, amount: int):
        self.cargo[product] += amount

    def load_from_warehouse(self, product: str, qty: int) -> int:
        available = min(qty, self.space_left)
        if available <= 0:
            print(f"{self.name}: NIE MOŻNA ZAŁADOWAĆ WIĘCEJ {product} (brak miejsca).")
            return 0
        self.cargo[product] += available
        return available

    def unload_cargo(self) -> None:
        for prod in list(self.cargo.keys()):
            self.cargo[prod] = 0

    def run(self):
        if not self.start or not self.route:
            raise ValueError(f"{self.name} nie ma przypisanej trasy.")
        print(f"\n{self.name} rusza w trasę (ładowność: {self.capacity}kg)")
        self.result = move_truck_along_route(self, self.start, self.route)
        self.total_distance = self.result.get("total_distance", 0.0)
        
        remaining_points = [p for p in self.route if any(val != 0 for val in p.cargo.values())]

        if remaining_points:
            print(f"{self.name}: wykryto nieobsłużone punkty, podejmuję kolejną próbę.")
            from util.move_truck import plan_route
            from_point = self.result.get("last", self.start)
            additional_route = plan_route(from_point, remaining_points)

            if additional_route:
                result2 = move_truck_along_route(self, from_point, additional_route)
                self.result["steps"].extend(result2.get("steps", []))
                self.total_distance += result2.get("total_distance", 0.0)
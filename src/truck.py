import uuid
from typing import List, Optional
from point import Point
from util.move_truck import move_truck_along_route


class Truck:
    def __init__(self, name: str, capacity: int, cat: bool):
        self.id = uuid.uuid4()
        self.name = name
        self.capacity = capacity
        self.cargo = {"tuńczyk": 0, "pomarańcze": 0, "uran": 0}
        self.space_left = capacity - sum(self.cargo.values())
        self.cat = cat
        self.route: List[Point] = []
        self.start: Point = None
        self.total_distance = 0
        self.result = {}

    def assign_route(self, start: Point, route: List[Point]):
        self.start = start
        self.route = route

    def can_load(self, type: str, point: Point) -> bool:
        weight = point.cargo[type]
        if weight < 0 and (
            type == "pomarańcze"
            and self.cargo["uran"] != 0
            or type == "uran"
            and self.cargo["pomarańcze"] != 0
        ):
            return False  # nie można pomarańczy z uranem

        if weight > 0:
            # czy jedziemy tylko do punktów, które obsłużymy w 100%?
            return self.cargo[type] > 0
        elif weight < 0:
            return self.space_left > 0
        else:
            return True

    def load_cargo(self, type: str, point: Point) -> None:
        weight = point.cargo[type]
        if weight > 0:
            cargo_to_load = weight if weight <= self.space_left else self.space_left
            self.cargo[type] -= cargo_to_load
            self.space_left += cargo_to_load
            point.cargo[type] -= cargo_to_load
        elif weight < 0:
            cargo_to_load = (
                weight if abs(weight) <= self.space_left else -self.space_left
            )
            self.cargo[type] -= cargo_to_load
            self.space_left += cargo_to_load
            point.cargo[type] -= cargo_to_load

    def unload_cargo(self) -> None:
        self.space_left = self.cargo
        self.cargo = {key: 0 for key, _ in self.cargo.items()}

    def run(self):
        if not self.start or not self.route:
            raise ValueError(f"🚫 {self.name} nie ma przypisanej trasy.")
        print(f"\n{self.name} rusza w trasę (ładowność: {self.capacity}kg)")
        self.result = move_truck_along_route(self.start, self.route)
        self.total_distance = self.result["total_distance"]
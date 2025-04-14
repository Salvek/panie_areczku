import uuid
from typing import List
from point import Point
from util.move_truck import move_truck_along_route


class Truck:
    def __init__(self, name: str, capacity: int):
        self.id = uuid.uuid4()
        self.name = name
        self.capacity = capacity
        self.cargo = {"tuna": 0, "oranges": 0, "uranium": 0}
        self.space_left = capacity - sum(self.cargo.values())
        self.route: List[Point] = []
        self.start: Point = None
        self.total_distance = 0
        self.result = {}

    def assign_route(self, start: Point, route: List[Point]):
        self.start = start
        self.route = route

    def can_load(self, weight: int) -> bool:
        return weight <= self.space_left

    def run(self):
        if not self.start or not self.route:
            raise ValueError(f"🚫 {self.name} nie ma przypisanej trasy.")
        print(f"\n{self.name} rusza w trasę (ładowność: {self.capacity}kg)")
        self.result = move_truck_along_route(self.start, self.route)
        self.total_distance = self.result["total_distance"]

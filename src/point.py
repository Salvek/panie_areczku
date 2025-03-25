from random import randint, choice
from math import sqrt
from uuid import uuid1
import config


class Point:

    def __init__(self):
        self.id = uuid1()
        self.x = randint(0, config.BOARD_SIZE)
        self.y = randint(0, config.BOARD_SIZE)
        self.tuna = Point.__generate_cargo()
        self.oranges = Point.__generate_cargo()
        self.uranium = Point.__generate_cargo()
        self.is_warehouse = False

    @staticmethod
    def __generate_cargo() -> int:
        return (
            randint(
                config.CARGO_LOWER_POSITIVE_BOUNDARY,
                config.CARGO_UPPER_POSITIVE_BOUNDARY,
            )
            if choice([True, False])
            else randint(
                config.CARGO_LOWER_NEGATIVE_BOUNDARY,
                config.CARGO_UPPER_NEGATIVE_BOUNDARY,
            )
        )

    def calc_dist(self, point: "Point") -> float:
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def __str__(self):
        return "\nPoint {0}\nX - {1}\nY - {2}\nTuna - {3} kg\nOranges - {4} kg\nUranium - {5} kg\nWarehouse - {6}".format(
            self.id,
            self.x,
            self.y,
            self.tuna,
            self.oranges,
            self.uranium,
            self.is_warehouse,
        )

    def toggle_warehouse(self) -> None:
        self.is_warehouse = not self.is_warehouse
        self.tuna = 0
        self.oranges = 0
        self.uranium = 0

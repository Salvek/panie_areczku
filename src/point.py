from random import randint, choice
from math import sqrt
from uuid import uuid1
import config


class Point:

    def __init__(self):
        self.id = uuid1()
        self.x = randint(0, config.BOARD_SIZE)
        self.y = randint(0, config.BOARD_SIZE)
        self.cargo = {p: Point.__generate_cargo() for p in config.PRODUCTS}
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
            self.cargo["tuńczyk"],
            self.cargo["pomarańcze"],
            self.cargo["uran"],
            self.is_warehouse,
        )

    def toggle_warehouse(self) -> None:
        self.is_warehouse = not self.is_warehouse
        self.cargo["tuńczyk"] = 0
        self.cargo["pomarańcze"] = 0
        self.cargo["uran"] = 0

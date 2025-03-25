import random
from math import sqrt
from uuid import uuid1, UUID
import numpy as np
import matplotlib.pyplot as plt


SEED = 10
WAREHOUSES_NUMBER = 5
CARGO_UPPER_POSITIVE_BOUNDARY = 200
CARGO_LOWER_POSITIVE_BOUNDARY = 100
CARGO_UPPER_NEGATIVE_BOUNDARY = -100
CARGO_LOWER_NEGATIVE_BOUNDARY = -200

random.seed(SEED)


class Point:

    def __init__(self):
        self.id = uuid1()
        self.x = random.randint(0, 100)
        self.y = random.randint(0, 100)
        self.tuna = Point.__generate_cargo()
        self.oranges = Point.__generate_cargo()
        self.uranium = Point.__generate_cargo()
        self.is_warehouse = False

    @staticmethod
    def __generate_cargo() -> int:
        return (
            random.randint(CARGO_LOWER_POSITIVE_BOUNDARY, CARGO_UPPER_POSITIVE_BOUNDARY)
            if random.choice([True, False])
            else random.randint(
                CARGO_LOWER_NEGATIVE_BOUNDARY, CARGO_UPPER_NEGATIVE_BOUNDARY
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


class Board:

    def __init__(self, points: list[Point] = [], x_dim: int = 100, y_dim=100):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.points = points

    def populate_board(self, points_number=100) -> None:
        if len(self.points) > 0:
            print("Board is already populated")
            return
        occupied_coord = []
        while points_number > 0:
            new_point = Point()
            if (new_point.x, new_point.y) in occupied_coord:
                continue
            self.points.append(new_point)
            occupied_coord.append((new_point.x, new_point.y))
            points_number -= 1

    def delete_point(self, id: UUID) -> None:
        self.points = list(filter(lambda p: p.id != id, self.points))

    def toggle_warehouses(self) -> None:
        warehouses = random.choices(self.points, k=WAREHOUSES_NUMBER)
        for p in self.points:
            if p.id in [w.id for w in warehouses]:
                p.toggle_warehouse()

    def __str__(self):
        return "\n".join([str(p) for p in self.points])

    def display(self) -> None:
        points_coord = []
        warehouses_coord = []

        for p in self.points:
            (
                warehouses_coord.append([p.x, p.y])
                if p.is_warehouse
                else points_coord.append([p.x, p.y])
            )
        np_points_coord = np.array(points_coord)
        np_warehouses_coord = np.array(warehouses_coord)
        plt.scatter(np_points_coord[:, 0], np_points_coord[:, 1])
        plt.scatter(np_warehouses_coord[:, 0], np_warehouses_coord[:, 1])
        plt.title("Board")
        plt.xlabel("X coordinates")
        plt.ylabel("Y coordinates")
        plt.show()


if __name__ == "__main__":
    board = Board()
    board.populate_board()
    board.toggle_warehouses()
    print(str(board))
    board.display()

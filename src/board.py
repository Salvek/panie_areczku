import random
from uuid import UUID
import numpy as np
import matplotlib.pyplot as plt
import config
from point import Point


class Board:

    def __init__(
        self,
        points: list[Point] = [],
        x_dim: int = config.BOARD_SIZE,
        y_dim=config.BOARD_SIZE,
    ):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.points = points

    def populate_board(self, points_number=config.POINTS_NUMBER) -> None:
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
        warehouses = random.choices(self.points, k=config.WAREHOUSES_NUMBER)
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
    pass

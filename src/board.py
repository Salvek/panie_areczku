import random
from uuid import UUID
import numpy as np
import matplotlib.pyplot as plt
import config
from point import Point
from typing import Optional


class Board:

    def __init__(
        self,
        points: Optional[list[Point]] = None,
        x_dim: int = config.BOARD_SIZE,
        y_dim=config.BOARD_SIZE,
    ):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.points = points if points is not None else []

    def populate_board(self, points_number=config.POINTS_NUMBER) -> None:
        occupied_coord = []
        while points_number > 0:
            new_point = Point()
            if (new_point.x, new_point.y) in occupied_coord:
                continue
            self.points.append(new_point)
            occupied_coord.append((new_point.x, new_point.y))
            points_number -= 1

    def delete_point(self, id: UUID) -> None:
        if not self.points:
            print("No points on the board")
            return
        self.points = list(filter(lambda p: p.id != id, self.points))

    def toggle_warehouses(self) -> None:
        if not self.points:
            print("No points on the board")
            return
        warehouses = random.choices(self.points, k=config.WAREHOUSES_NUMBER)
        for p in self.points:
            if p.id in [w.id for w in warehouses]:
                p.toggle_warehouse()

    def __str__(self):
        if not self.points:
            return ""
        return "\n".join([str(p) for p in self.points])

    def display(self, truck_paths: list = None) -> None:
        if not self.points:
            print("No points to display")
            return
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

        plt.figure(figsize=(8, 8))
        if len(np_points_coord) > 0:
            plt.scatter(np_points_coord[:, 0], np_points_coord[:, 1], label="Klienci", color='blue')
        if len(np_warehouses_coord) > 0:
            plt.scatter(np_warehouses_coord[:, 0], np_warehouses_coord[:, 1], label="Magazyny", color='red')

        if truck_paths:
            colors = ["green", "orange", "purple", "black", "pink", "cyan"]
            for i, truck_steps in enumerate(truck_paths):
                c = colors[i % len(colors)]
                for step in truck_steps:
                    x_vals = [step["from"][0], step["to"][0]]
                    y_vals = [step["from"][1], step["to"][1]]
                    plt.plot(x_vals, y_vals, color=c, linestyle='-', linewidth=2,
                             label=f"Truck {i + 1}" if step == truck_steps[0] else "")

        plt.title("Mapa trasy")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.show()

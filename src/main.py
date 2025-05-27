from board import Board
from util.move_truck import plan_route
from fleet import Fleet

if __name__ == "__main__":
    fleet = Fleet()
    board = Board()
    board.populate_board()
    board.toggle_warehouses()

    warehouses = [p for p in board.points if p.is_warehouse][:3]
    clients = [p for p in board.points if not p.is_warehouse]
    client_chunks = [clients[i::3] for i in range(3)]
    routes = [
        plan_route(start, chunk) for start, chunk in zip(warehouses, client_chunks)
    ]

    start_point = board.points[0]
    targets = board.points[1:]

    fleet.assign_routes(routes, warehouses)
    fleet.dispatch()
    for truck in fleet.trucks:
        print(f"{truck.name} | dystans: {truck.total_distance} km")

    truck_paths = [t.result["steps"] for t in fleet.trucks if "steps" in t.result]

    print("\n=== RAPORT KOŃCOWY ===")
    for p in board.points:
        for prod, qty in p.cargo.items():
            if qty < 0:
                print(f"{p.id}: ZA DUŻO {prod} -> {qty}kg")
            elif qty > 0 and not p.is_warehouse:
                print(f"{p.id}: NIEOBSŁUŻONO {prod} -> {qty}kg")
            else:
                print(f"{p.id}: OK {prod} -> {qty}kg")

    board.display(truck_paths)
    print(str(board))

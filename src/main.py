from board import Board


if __name__ == "__main__":
    board = Board()
    board.populate_board()
    board.toggle_warehouses()
    print(str(board))
    board.display()

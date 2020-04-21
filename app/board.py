from enum import Enum, auto
from itertools import product
from copy import deepcopy


class Figure(Enum):
    EMPTY = auto()
    BLACK = auto()
    WHITE = auto()


class Board:
    def __init__(self):
        self.board = [[Figure.EMPTY for _ in range(8)] for _ in range(8)]
        self.board[3][3] = self.board[4][3] = Figure.BLACK
        self.board[3][4] = self.board[4][4] = Figure.WHITE
        self.is_black_move = True
        self.history = [(self.board, self.is_black_move)]
        self.last_move = None

    def place_ok(self, x, y):
        if x not in range(0, 8):
            return False
        if y not in range(0, 8):
            return False
        if self.is_black_move and not self.board[x][y] == Figure.WHITE:
            return False
        if not self.is_black_move and not self.board[x][y] == Figure.BLACK:
            return False
        return True

    def count_move_score(self, x, y, is_black):
        if self.board[x][y] != Figure.EMPTY:
            return 0
        ways = list(product([-1, 0, 1], [-1, 0, 1]))
        ways.remove((0, 0))
        max_score = 0
        for way in ways:
            current_score = 0

            def shift(s):
                return x + s * way[0], y + s * way[1]
            while self.place_ok(*shift(current_score + 1)):
                current_score += 1
            last_x, last_y = shift(current_score + 1)
            if current_score == 0 or last_x not in range(0, 8) or last_y not in range(0, 8):
                continue
            if is_black and not self.board[last_x][last_y] == Figure.BLACK:
                continue
            if not is_black and not self.board[last_x][last_y] == Figure.WHITE:
                continue
            max_score = max(max_score, current_score)
        return max_score

    def get_possible_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                value = self.count_move_score(i, j, self.is_black_move)
                if value > 0:
                    moves.append([i, j])
        return moves

    def get_score(self):
        return [sum(j.count(i) for j in self.board) for i in [Figure.BLACK, Figure.WHITE]]

    def apply_move(self, x, y):
        self.last_move = (x, y)
        self.history.append(deepcopy((self.board, self.is_black_move)))
        ways = list(product([-1, 0, 1], [-1, 0, 1]))
        ways.remove((0, 0))
        self.board[x][y] = Figure.BLACK if self.is_black_move else Figure.WHITE
        for way in ways:
            cur_shift = 1

            def shift(s):
                return x + s * way[0], y + s * way[1]

            while self.place_ok(*shift(cur_shift)):
                cur_shift += 1

            last_x, last_y = shift(cur_shift)
            if cur_shift == 1 or last_x not in range(0, 8) or last_y not in range(0, 8):
                continue
            if self.is_black_move and not self.board[last_x][last_y] == Figure.BLACK:
                continue
            if not self.is_black_move and not self.board[last_x][last_y] == Figure.WHITE:
                continue

            cur_shift = 1
            while self.place_ok(*shift(cur_shift)):
                xc, yc = shift(cur_shift)
                self.board[xc][yc] = self.board[x][y]
                cur_shift += 1

        self.change_player()

    def pop_move(self):
        if len(self.history) > 0:
            (self.board, self.is_black_move) = self.history.pop()

    def change_player(self):
        if not self.game_over():
            self.is_black_move = bool(int(self.is_black_move) ^ 1)
            if len(self.get_possible_moves()) == 0:
                self.is_black_move = bool(int(self.is_black_move) ^ 1)

    def game_over(self) -> bool:
        if len(self.get_possible_moves()) == 0:
            self.is_black_move = bool(int(self.is_black_move) ^ 1)
            game_over = len(self.get_possible_moves()) == 0
            self.is_black_move = bool(int(self.is_black_move) ^ 1)
            return game_over
        return False

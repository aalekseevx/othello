from app.board import Board
from app.ai import get_move
from app.board import Figure

E = Figure.EMPTY
B = Figure.BLACK
W = Figure.WHITE

simple_cases = [[
    [E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E],
    [E, W, W, W, W, W, W, B],
    [E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E]
],
[
    [E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, B, E],
    [E, E, E, E, E, W, E, E],
    [E, E, E, E, W, E, E, E],
    [E, E, E, W, E, E, E, E],
    [E, E, W, E, E, E, E, E],
    [E, W, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E]
],
[
    [E, E, E, E, E, E, E, E],
    [E, E, E, E, W, E, E, E],
    [E, E, E, E, E, W, E, E],
    [E, E, E, E, E, E, W, E],
    [E, E, E, E, E, E, E, B],
    [E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E]
],
[
    [E, E, E, E, E, E, E, B],
    [E, E, W, E, E, E, W, E],
    [E, W, E, E, E, W, E, E],
    [B, E, E, E, W, E, E, E],
    [E, E, E, W, E, E, E, E],
    [E, E, W, E, E, E, E, E],
    [E, W, E, E, E, E, W, E],
    [E, E, E, E, E, B, E, E]
],
[
    [E, E, E, E, E, E, E, E],
    [E, E, E, E, W, E, E, E],
    [E, E, E, E, E, W, E, E],
    [E, E, E, E, E, E, W, E],
    [E, E, E, E, E, E, E, B],
    [E, E, E, E, E, E, E, E],
    [E, W, W, W, W, W, W, B],
    [E, E, E, E, E, E, E, E]
],
]

correct_scores = [
    [8, 0],
    [7, 0],
    [5, 0],
    [10, 3],
    [9, 3]
]


def run_simple_case(number):
    board = Board()
    board.board = simple_cases[number]
    board.apply_move(*get_move(board, number, True))
    assert board.get_score() == correct_scores[number]


def test_simple_case_0():
    run_simple_case(0)


def test_simple_case_1():
    run_simple_case(1)


def test_simple_case_2():
    run_simple_case(2)


def test_simple_case_3():
    run_simple_case(3)


def test_simple_case_4():
    run_simple_case(4)

from copy import deepcopy
from .board import Board
import config


def fast_evaluation(board: Board, is_ai_black: bool):
    score_black, score_white = board.get_score()
    if is_ai_black:
        return score_black - score_white
    else:
        return score_white - score_black


def slow_evaluation(board: Board, depth_left=config.DEPTH, is_ai_black: bool = True):
    c_score = 2**depth_left * fast_evaluation(board, is_ai_black)
    if depth_left > 0:
        for move in board.get_possible_moves():
            board.apply_move(*move)
            opposite_move = get_move(board, depth_left - 1, bool(int(is_ai_black) ^ 1))
            if opposite_move is None:
                c_score *= 2
            else:
                board.apply_move(*opposite_move)
            c_score += slow_evaluation(board, depth_left - 1, is_ai_black)
            board.pop_move()
    return c_score


def score(board: Board, move, depth: int, is_ai_black: bool):
    board_copy = deepcopy(board)
    board_copy.apply_move(*move)
    return slow_evaluation(board_copy, depth, is_ai_black)


def get_move(board: Board, depth: int = config.DEPTH, is_ai_black: bool = False):
    possible = board.get_possible_moves()
    if len(possible) == 0:
        return None
    return max(possible, key=lambda x: score(board, x, depth, is_ai_black))

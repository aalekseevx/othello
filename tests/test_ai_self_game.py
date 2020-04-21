from app.board import Board
from app.ai import get_move
import config
import sys
import threading
import _thread as thread


def quit_function(fn_name):
    thread.interrupt_main()


def exit_after(s):
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner

    return outer


def run_with_depth(depth, seconds):
    board = Board()
    is_black = True
    ai_get = exit_after(seconds)(get_move)
    count = 0
    while not board.game_over():
        move = ai_get(board, depth, is_black)
        board.apply_move(*move)
        is_black = not is_black
        count += 1


def test_stupid_ai_self_game():
    run_with_depth(0, 1)


def test_smart_ai_self_game():
    run_with_depth(1, 10)


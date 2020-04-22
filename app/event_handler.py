from .board import Board
from pygame import Surface, USEREVENT
import pygame
from loguru import logger
from itertools import product
from .board import Figure
import app.ai
import pickle

AIREQUIRED = USEREVENT + 1


class GameController:
    def __init__(self, screen: Surface):
        self.board: Board = Board()
        self.screen: Surface = screen

    def update_screen(self):
        elem_size = self.screen.get_size()[0] // 8
        back_color = (249, 231, 159)
        black = (0, 0, 0)
        red = (229, 152, 102)
        white = (255, 255, 255)
        pos_x = pos_y = 0
        self.screen.fill(back_color)

        for x, y in product(range(8), range(8)):
            position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
            pygame.draw.rect(self.screen, black, position, 3)
            if self.board.board[x][y] != Figure.EMPTY:
                figure_color = black if self.board.board[x][y] == Figure.BLACK else white
                pygame.draw.circle(self.screen, figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2),
                                   elem_size // 2 - 10)
                if (x, y) == self.board.last_move:
                    pygame.draw.circle(self.screen, red,
                                       (position[0] + elem_size // 2, position[1] + elem_size // 2),
                                       elem_size // 2 - 8, 4)
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render("/".join(map(str, self.board.get_score())), False,  (236, 112, 99))
        self.screen.blit(text_surface, (10, 10))
        pygame.display.flip()

    @staticmethod
    def arrange_ai():
        my_event = pygame.event.Event(AIREQUIRED, {})
        pygame.event.post(my_event)

    def handle_ai(self):
        self.board.apply_move(*app.ai.get_move(self.board))

    def handle_move(self, pos):
        elem_size = self.screen.get_size()[0] // 8
        x, y = pos[0] // elem_size, pos[1] // elem_size
        if self.board.count_move_score(x, y, self.board.is_black_move) > 0:
            self.board.apply_move(x, y)
            if not self.board.game_over():
                self.arrange_ai()

    def handle_save(self):
        with open("snapshot.pickle", "wb") as fout:
            pickle.dump(self.board, fout)

    def handle_load(self):
        with open("snapshot.pickle", "rb") as fin:
            self.board = pickle.load(fin)

    def handle_undo(self):
        self.board.pop_move()
        self.board.pop_move()

    def handle(self, event: pygame.event) -> bool:
        event_handled = True

        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handle_move(event.pos)
        elif event.type == AIREQUIRED:
            self.handle_ai()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.handle_save()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            self.handle_load()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            self.handle_undo()
        else:
            event_handled = False

        if event_handled:
            logger.info(f"Handling an event: {event}")
            self.update_screen()
        return False

import config
from app.event_handler import GameController
from loguru import logger
from pygame import Surface
import pygame

if __name__ == '__main__':
    pygame.init()
    screen: Surface = pygame.display.set_mode([512, 512])
    event_handler = GameController(screen)
    pygame.font.init()
    event_handler.update_screen()
    logger.success("Initialization successful")
    while True:
        die_time = False
        for event in pygame.event.get():
            die_time |= event_handler.handle(event)
        if die_time:
            logger.info("Caught QUIT event")
            break

    pygame.quit()
    logger.info("Stopped")


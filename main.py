import pygame
from random import randint
import os

#WINDOW
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480
WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("PySnake!")


SIZE_OF_BLOCKS = 20

BLOCK_WIDTH = WINDOW_WIDTH // SIZE_OF_BLOCKS
BLOCK_HEIGHT = WINDOW_HEIGHT // SIZE_OF_BLOCKS

FPS = 4

#COLORS
LIGHT_GREEN = (105, 209, 84)
DARK_GREEN = (45, 117, 30)

class Game:

    def __init__(self):
        pygame.init()
        self.__snake = Snake()
        self.__berry = Berry()
        self.__run = True
        self.__zivot = True

    def playGame(self):
        clock = pygame.time.Clock()
        while self.__run:
            if self.__zivot:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__run = False
                    elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                        self.__run = False
                self.__draw()
            else:
                pass

    def __draw(self):
        self.__draw_playground()
        pygame.display.update()


    def __draw_playground(self):
        for y in range(0, int(BLOCK_HEIGHT)):
            for x in range (0, int(BLOCK_WIDTH)):
                if (x + y) % 2 == 0:
                    r = pygame.Rect((x * SIZE_OF_BLOCKS, y * SIZE_OF_BLOCKS), (SIZE_OF_BLOCKS, SIZE_OF_BLOCKS))
                    pygame.draw.rect(WINDOW, LIGHT_GREEN, r)
                else:
                    r = pygame.Rect((x * SIZE_OF_BLOCKS, y * SIZE_OF_BLOCKS), (SIZE_OF_BLOCKS, SIZE_OF_BLOCKS))
                    pygame.draw.rect(WINDOW, DARK_GREEN, r)

class Snake:

    def __init__(self):
        pass


class Berry:

    def __init__(self):
        pass


if __name__ == '__main__':
    game = Game()
    game.playGame()
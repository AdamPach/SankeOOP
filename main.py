import pygame
from random import randint
import os

#WINDOW
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("PySnake!")


SIZE_OF_BLOCKS = 50

BLOCK_WIDTH = WINDOW_WIDTH // SIZE_OF_BLOCKS
BLOCK_HEIGHT = WINDOW_HEIGHT // SIZE_OF_BLOCKS

FPS = 4

#COLORS
LIGHT_GREEN = (105, 209, 84)
DARK_GREEN = (45, 117, 30)
BLUE = (43, 122, 186)
RED = (186, 43, 43)

SNAKE_COLIDE_WALL = pygame.USEREVENT + 1
SNAKE_ATE_BERRY = pygame.USEREVENT + 2
SNAKE_ATE_HIMSELF = pygame.USEREVENT + 3

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
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:   #NAHORU
                        self.__snake.zmenSmerHada(0, -SIZE_OF_BLOCKS)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:   #DOLU
                        self.__snake.zmenSmerHada(0, SIZE_OF_BLOCKS)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:   #DOLEVA
                        self.__snake.zmenSmerHada(-SIZE_OF_BLOCKS, 0)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:   #DOPRAVA
                        self.__snake.zmenSmerHada(SIZE_OF_BLOCKS, 0)
                self.__snake.snakeMovement(self.__berry)
                for event in pygame.event.get():
                    if event.type == SNAKE_COLIDE_WALL:
                        self.__zivot = False
                    elif event.type == SNAKE_ATE_HIMSELF:
                        self.__zivot = False
                    elif event.type == SNAKE_ATE_BERRY:
                        self.__berry.generateNewBerry()

                self.__draw()
            else:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__run = False
                    elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                        self.__run = False
        pygame.quit()

    def __draw(self):
        self.__draw_playground()
        snake = self.__snake.returnSnake()
        berry = self.__berry.returnBerry()
        for partOfSnake in snake:
            pygame.draw.rect(WINDOW, BLUE, partOfSnake)
        pygame.draw.rect(WINDOW, RED, berry)
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
        self.__snake = [pygame.Rect(WINDOW_WIDTH // 2,WINDOW_HEIGHT // 2,SIZE_OF_BLOCKS, SIZE_OF_BLOCKS),pygame.Rect(WINDOW_WIDTH // 2 - SIZE_OF_BLOCKS,WINDOW_HEIGHT // 2,SIZE_OF_BLOCKS, SIZE_OF_BLOCKS),pygame.Rect(WINDOW_WIDTH // 2 - SIZE_OF_BLOCKS * 2,WINDOW_HEIGHT // 2,SIZE_OF_BLOCKS, SIZE_OF_BLOCKS)]
        self.__smerHada_x = 0
        self.__smerHada_y = 0

    def returnSnake(self):
        return self.__snake

    def zmenSmerHada(self, smerHada_x, smerHada_y):
        self.__smerHada_x = smerHada_x
        self.__smerHada_y = smerHada_y

    def snakeMovement(self, berry):
        if self.__smerHada_x == 0 and self.__smerHada_y == 0:
            pass
        else:
            if self.__snake[0].x + self.__smerHada_x >= WINDOW_WIDTH or self.__snake[0].x + self.__smerHada_x < 0:
                pygame.event.post(pygame.event.Event(SNAKE_COLIDE_WALL))
            else:
                if self.__snake[0].y + self.__smerHada_y >= WINDOW_HEIGHT or self.__snake[0].y + self.__smerHada_y < 0:
                    pygame.event.post(pygame.event.Event(SNAKE_COLIDE_WALL))
                else:
                    lastPartOfSnake = self.__returnLastPartOfSnake()
                    snakeCopy = self.__snake[:-1]
                    snakeCopy.insert(0, pygame.Rect(snakeCopy[0].x + self.__smerHada_x, snakeCopy[0].y + self.__smerHada_y, SIZE_OF_BLOCKS, SIZE_OF_BLOCKS))
                    self.__snake = snakeCopy
                    self.__snakeAteBerry(berry, lastPartOfSnake)
                    self.__snakeAteHimself()

    def __returnLastPartOfSnake(self):
        snakeLength = len(self.__snake)
        lastPartOfSnake = self.__snake[snakeLength - 1]
        return lastPartOfSnake

    def __snakeAteBerry(self, berry, lastPartOfSnake):
        if self.__snake[0].colliderect(berry.returnBerry()):
            self.__snake.append(lastPartOfSnake)
            pygame.event.post(pygame.event.Event(SNAKE_ATE_BERRY))

    def __snakeAteHimself(self):
        for index in range(len(self.__snake)):
            if index == 0:
                pass
            elif self.__snake[0].colliderect(self.__snake[index]):
                pygame.event.post(pygame.event.Event(SNAKE_ATE_HIMSELF))

class Berry:

    def __init__(self):
        self.__berry = pygame.Rect(randint(0, BLOCK_WIDTH - 1) * SIZE_OF_BLOCKS, randint(0, BLOCK_HEIGHT - 1) * SIZE_OF_BLOCKS, SIZE_OF_BLOCKS, SIZE_OF_BLOCKS)

    def returnBerry(self):
        return self.__berry

    def generateNewBerry(self):
        self.__berry = pygame.Rect(randint(0, BLOCK_WIDTH - 1) * SIZE_OF_BLOCKS, randint(0, BLOCK_HEIGHT - 1) * SIZE_OF_BLOCKS, SIZE_OF_BLOCKS, SIZE_OF_BLOCKS)


if __name__ == '__main__':
    game = Game()
    game.playGame()
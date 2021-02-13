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
WHITE = (0, 0, 0)

SNAKE_COLIDE_WALL = pygame.USEREVENT + 1
SNAKE_ATE_BERRY = pygame.USEREVENT + 2
SNAKE_ATE_HIMSELF = pygame.USEREVENT + 3


MIKYR_OBLICEJ = pygame.image.load(os.path.join("Assets","mikyr.png"))
KALETA_OBLICEJ = pygame.image.load(os.path.join("Assets","kaleta.png"))

MIKYR = pygame.transform.scale(MIKYR_OBLICEJ, (SIZE_OF_BLOCKS, SIZE_OF_BLOCKS))
KALETA = pygame.transform.scale(KALETA_OBLICEJ, (SIZE_OF_BLOCKS, SIZE_OF_BLOCKS))

class Game:

    def __init__(self):
        #ZAKLADNI ATRIBUTY
        pygame.init()
        self.__snake = Snake()
        self.__berry = Berry()
        self.__run = True
        self.__zivot = True
        self.__points = 0

        #TEXTY
        pygame.font.init()
        self.__font = pygame.font.SysFont("comicsans", 40)

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
                        self.__points += 1

                self.__draw()
            else:
                if self.__points == 0:
                    END_TEXT = f"Získal jsi {self.__points} jednotek pozornosti"
                elif self.__points == 1:
                    END_TEXT = f"Získal jsi {self.__points} jednotku pozornosti"
                elif self.__points >= 2 and self.__points <= 4:
                    END_TEXT = f"Získal jsi {self.__points} jednotky pozornosti"
                else:
                    END_TEXT = f"Získal jsi {self.__points} jednotek pozornosti"
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__run = False
                    elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                        self.__run = False
                    elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                        self.__restartGame()
                self.__draw_after_end(END_TEXT)
        pygame.quit()

    def __draw(self):
        self.__draw_playground()
        snake = self.__snake.returnSnake()
        berry = self.__berry.returnBerry()
        for index in range(len(snake)):
            if index == 0:
                pygame.draw.rect(WINDOW,BLUE, snake[index])
                WINDOW.blit(MIKYR, (snake[0].x, snake[0].y))
            else:
                pygame.draw.rect(WINDOW, BLUE, snake[index])
        WINDOW.blit(KALETA, (berry.x, berry.y))
        if self.__snake.returnNoWay:
            TEXT = self.__font.render("Pro start zmackni W,S,D", True, WHITE)
            TEXT2 = self.__font.render("Posbírej co nejvíce MARCUSU pro co nejvíce jednotek pozornosti", True, WHITE)
            WINDOW.blit(TEXT2, (WINDOW_WIDTH * 0.01, WINDOW_HEIGHT * 0.4))
            WINDOW.blit(TEXT, (WINDOW_WIDTH * 0.35, WINDOW_HEIGHT * 0.45))
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

    def __draw_after_end(self, END_TEXT):
        END = self.__font.render(END_TEXT, True, WHITE)
        RESTART = self.__font.render("Pro restart zamckni R", True, WHITE)
        WINDOW.blit(END, (WINDOW_WIDTH * 0.3, WINDOW_HEIGHT * 0.4))
        WINDOW.blit(RESTART, (WINDOW_WIDTH * 0.35, WINDOW_HEIGHT * 0.45))
        pygame.display.update()

    def __restartGame(self):
        self.__zivot = True
        self.__snake.restartSnake()
        self.__berry.generateNewBerry()

class Snake:

    def __init__(self):
        self.__snake = [pygame.Rect(WINDOW_WIDTH // 2,WINDOW_HEIGHT // 2,SIZE_OF_BLOCKS, SIZE_OF_BLOCKS),pygame.Rect(WINDOW_WIDTH // 2 - SIZE_OF_BLOCKS,WINDOW_HEIGHT // 2,SIZE_OF_BLOCKS, SIZE_OF_BLOCKS),pygame.Rect(WINDOW_WIDTH // 2 - SIZE_OF_BLOCKS * 2,WINDOW_HEIGHT // 2,SIZE_OF_BLOCKS, SIZE_OF_BLOCKS)]
        self.__smerHada_x = 0
        self.__smerHada_y = 0
        self.__startSnake = self.__snake

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

    @property
    def returnNoWay(self):
        return self.__smerHada_x == 0 and self.__smerHada_y == 0

    def restartSnake(self):
        self.__snake = self.__startSnake
        self.__smerHada_x = 0
        self.__smerHada_y = 0

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
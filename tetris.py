import pygame
from random import choice
from colors import *
import os

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
display_size = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
screen = pygame.display.set_mode(display_size)

level_speed = [800, 716, 633, 550, 466, 383, 300, 130, 100, 83, 83, 83,
66, 66, 66, 50, 50, 50, 33, 33]

T = [[1, 1, 1],
     [0, 1, 0]]
S = [[0, 1, 1],
     [1, 1, 0]]
Z = [[1, 1, 0],
     [0, 1, 1]]
J = [[1, 0, 0],
     [1, 1, 1]]
L = [[0, 0, 1],
     [1, 1, 1]]
I = [[1, 1, 1, 1]]
O = [[1, 1],
     [1, 1]]

TETROMINOES = [T, S, Z, J, L, I, O]

class Tetris:

    def __init__(self):
        self.x = 3
        self.y = 0
        self.left = DISPLAY_WIDTH/2 - 5 * 35  
        self.top = DISPLAY_HEIGHT/2 - 10 * 35 
        self.score = 0
        self.level = 0
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.boardcolor = [[black for _ in range(10)] for _ in range(20)]        
        self.getRandomPiece()
        self.draw()
        
    def displayBoard(self):
        for col in range(20):
            for row in range(10):
                try:
                    if self.board[col][row] or col - self.y >= 0 and row - self.x >=0 and (self.tetromino[col - self.y][row -self.x]):
                        print('B', end='', flush=True)
                    else:
                        print('.', end='', flush=True)
                except:
                    print('.', end='', flush=True)
            print('')
        print('')

    def drawGrid(self):
        self.border = pygame.Rect(0,0, 10*35 + 5, 20*35 + 5)
        rect = pygame.Rect(0,0,10*35, 20*35)
        self.border.center = rect.center = (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2)
        screen.fill(black)
        pygame.draw.rect(screen, white, self.border)
        pygame.draw.rect(screen, black, rect)
        myfont = pygame.font.Font(os.getcwd() + "/8-Bit-Madness.ttf", 30)
        scoretext = myfont.render("SCORE "+str(self.score), 1, white)        
        screen.blit(scoretext, (DISPLAY_WIDTH/2 + 6.5 * 35, DISPLAY_HEIGHT/2 - 4.5 * 35))
        myfont1 = pygame.font.Font(os.getcwd() + "/8-Bit-Madness.ttf", 30)
        leveltext = myfont1.render("LEVEL "+str(self.level), 1, white)        
        screen.blit(leveltext, (DISPLAY_WIDTH/2 + 6.5 * 35, DISPLAY_HEIGHT/2 - 6 * 35))

        for col in range(20):
            for row in range(10):
                if self.board[col][row]:
                    rect = pygame.Rect(0,0,35, 35)
                    rect.x = self.left + row * 35
                    rect.y = self.top + col * 35
                    pygame.draw.rect(screen, self.boardcolor[col][row], rect)
        # self.displayBoard()
        pygame.display.update()

    def getRandomPiece(self):
        self.x = 3
        self.y = 0
        self.tetromino = choice(TETROMINOES)
        self.color = choice(tetrocolors)

    def draw(self):
        self.drawGrid()
        for i in range(len(self.tetromino)):
            for j in range(len(self.tetromino[i])):
                if(self.tetromino[i][j]):
                    tmp = pygame.Rect(0, 0, 35, 35)
                    tmp.y = self.top + self.y * 35 + i * 35
                    tmp.x = self.left + self.x * 35 + j * 35
                    pygame.draw.rect(screen, self.color, tmp)
        pygame.display.update()
    
    def dropPiece(self):
        tmp = self.tetromino
        tmp1 = self.color
        while tmp == self.tetromino and tmp1 == self.color:
            self.moveDown() 

    def moveDown(self):
        self.y+=1
        if self.outOfBounds() or self.collision():
            self.y-=1
            self.makeTaken()
            self.clearLine()
        self.draw()
            
    def moveRight(self):
        self.x+=1
        if self.outOfBounds() or self.collision():
            self.x-=1
        self.draw()

    def moveLeft(self):
        self.x-=1
        if self.outOfBounds() or self.collision():
            self.x+=1
        self.draw()

    def rotate(self):
        new_tetromino = self.rotate_clockwise(self.tetromino)
        tmp = self.tetromino
        self.tetromino = new_tetromino
        if self.outOfBounds() or self.collision():
            self.tetromino = tmp
        self.draw()

    def rotate_clockwise(self, tetromino):
        return [
            [
                tetromino[y][x] for y in range(len(tetromino))
            ] for x in range(len(tetromino[0]) - 1, -1, -1)
        ]

    def outOfBounds(self):
        for y in range(len(self.tetromino)):
            if (y+1) + self.y > 20 or self.y < 0:
                return True
            for ind, x in enumerate(self.tetromino[y]):
                if (ind+1) * x + self.x > 10 or self.x < 0:
                    return True
        return False

    def collision(self):
        for i in range(len(self.tetromino)):
            for j in range(len(self.tetromino[i])):
                if self.tetromino[i][j] and self.board[self.y + i][self.x + j]:
                    return True
        return False
        
    def makeTaken(self):
        for col in range(20):
            for row in range(10):
                try:
                    if col - self.y >= 0 and row - self.x >=0 and self.tetromino[col - self.y][row -self.x]:
                        self.board[col][row] = 1
                        self.boardcolor[col][row] = self.color
                except:
                    pass
        if not self.gameOver():
            self.getRandomPiece()
            self.moveDown()

    def clearLine(self):
        for i in range(len(self.board)):
            if(sum(self.board[i]) == 10):
                self.board.pop(i)
                self.boardcolor.pop(i)
                self.board.insert(0, [0 for i in range(10)])
                self.boardcolor.insert(0, [black for i in range(10)])
                self.score+=1
                self.level = int(self.score/10)
        if(self.level >=19):
            pygame.time.set_timer(pygame.USEREVENT,level_speed[19])
        else:
            pygame.time.set_timer(pygame.USEREVENT,level_speed[self.level])

    def gameOver(self):
        if self.x == 3 and self.y == 0 and self.collision():
            return True
        return False
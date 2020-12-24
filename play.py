from tetris import *
from sys import exit

def main():
    pygame.font.init()
    pygame.display.set_caption('Tetris') 
    tetris = Tetris()
    pygame.time.set_timer(pygame.USEREVENT,800)
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if tetris.gameOver():
                    print('hi')
                    pygame.time.set_timer(pygame.USEREVENT,0)
                    break
                tetris.moveDown()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tetris.dropPiece()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    tetris.rotate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    tetris.moveDown()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    tetris.moveLeft()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    tetris.moveRight()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


main()


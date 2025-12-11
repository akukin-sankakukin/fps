
import pygame
import sys
import random
from pygame.locals import *

GOLD= (255, 216, 0)

def main():
    pygame.init()
    pygame.display.set_caption("fps")
    screen = pygame.display.set_mode((640, 360))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 60)

   

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT or event.key == K_RETURN:
                    screen = pygame.display.set_mode((640, 360), pygame.FULLSCREEN)
                
                if event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((640, 360))

        mouseX, mouseY = pygame.mouse.get_pos()

        txt1 = font.render("{}, {}".format(mouseX, mouseY), True, 'blue')

        mbtn1, mbnt2, mbtn3 = pygame.mouse.get_pressed()

        txt2 = font.render("{}, {}, {}".format(mbtn1, mbnt2, mbtn3 ), True, 'red')

        
        pygame.draw.ellipse(screen, GOLD, [100, 100, 150, 150], 60)
        

        

        screen.fill('black')
        screen.blit(txt1, [100, 100])
        screen.blit(txt2, [100, 200])

        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()






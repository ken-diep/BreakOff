import pygame, sys
from pygame.locals import *

WINHEIGHT = 480
WINWIDTH = 640

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

pygame.init()

DISPLAY = pygame.display.set_mode((WINWIDTH, WINHEIGHT),0,32)

BRICKWIDTH = 80
BRICKHEIGHT = 30

XPOS = 10  # Start of bricks
YPOS = 150

PADDLEWIDTH = 80
PADDLEHEIGHT = 15
PADDLEXPOS = 320
PADDLEYPOS = 300
PADDLEVEL = 5 #Paddle velocity

global BALLPOS
BALLHEIGHT = 10
BALLWIDTH = 10
BALLYPOS = 200
BALLXPOS = 320
BALLYVEL = 5 #Ball velocity
BALLHVEL = 0

BALLDIRECT = 1 #1: Ball is falling, 0: ball is rising

DISPLAY.fill(WHITE)
DISPLAY.get_rect()
for i in range(7):
    pygame.draw.rect(DISPLAY, BLUE, (XPOS, YPOS, BRICKWIDTH, BRICKHEIGHT))
    XPOS += BRICKWIDTH + 5

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if pygame.key.get_pressed()[K_LEFT]: #move paddle left if left arrow is pressed
        if PADDLEXPOS >= 0: #Imposes boundary
            PADDLEVEL = -5

    elif pygame.key.get_pressed()[K_RIGHT]:
        if PADDLEXPOS <= 640 - BRICKWIDTH:
            PADDLEVEL = 5

    else:
        PADDLEVEL = 0

    PADDLEXPOS += PADDLEVEL

    DISPLAY.fill(WHITE)
    BALLCLOCK = pygame.time.Clock()
    BALLCLOCK.tick(30)

    for i in range(7):
        pygame.draw.rect(DISPLAY, BLUE, (XPOS, YPOS, BRICKWIDTH, BRICKHEIGHT))
        XPOS += BRICKWIDTH + 5

    pygame.draw.rect(DISPLAY, BLUE, (PADDLEXPOS, PADDLEYPOS, PADDLEWIDTH, PADDLEHEIGHT))

    pygame.draw.rect(DISPLAY, BLUE, (BALLXPOS,BALLYPOS,BALLWIDTH,BALLHEIGHT)) #Ball

    #vert collision detection
    if ((BALLYPOS + BALLHEIGHT == PADDLEYPOS) and (BALLXPOS in range(PADDLEXPOS,PADDLEXPOS+PADDLEWIDTH))):
        BALLYVEL = -BALLYVEL
        if PADDLEVEL > 0: #Paddle moving right
            BALLHVEL = -5
        elif PADDLEVEL < 0: #Paddle moving left
            BALLHVEL = 5
    elif BALLYPOS == 0:
        BALLYVEL = -BALLYVEL
    elif BALLXPOS == 0 or BALLXPOS+BALLWIDTH == 640:
        BALLHVEL = -BALLHVEL

    if BALLCLOCK.get_time() > 30: #Every 100ms, ball will fall
        BALLYPOS += BALLYVEL
        BALLXPOS += BALLHVEL

    pygame.display.update()

    



import pygame, sys
from pygame.locals import *

#Screen Size
WIN_HEIGHT = 480
WIN_WIDTH = 640

#Colour RHB values
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

#Brick dimensions
BRICKWIDTH = 70
BRICKHEIGHT = 20

#Paddle Dimensions
PADDLEWIDTH = 80
PADDLEHEIGHT = 15
PADDLE_X = 280 #Paddle starting X position
PADDLE_Y = 380
PADDLEVEL = 5 #Paddle velocity

#Ball Dimensions
BALLHEIGHT = 10
BALLWIDTH = 10
BALLRADIUS = 5
BALLDIAMETER = BALLRADIUS*2
BALL_Y = 290
BALL_X = 320

#States
STATE_BALL_ON_PADDLE = 0
STATE_PLAYING = 1
STATE_WIN = 2
STATE_GAMEOVER = 3
state = STATE_BALL_ON_PADDLE

class BreakOff:
    def __init__(self):
        self.PADDLEVEL = 0
        self.BALL_VEL = [0, 0]  # Ball velocity X,Y

        pygame.init()

        self.DISPLAY = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)
        self.StartGame()

        pygame.display.set_caption("Break Off")


    def StartGame(self):
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_ON_PADDLE

        self.paddle = pygame.Rect(PADDLE_X, PADDLE_Y, PADDLEWIDTH, PADDLEHEIGHT) #Draw paddle
        self.ball = pygame.Rect(BALL_X, BALL_Y, BALLDIAMETER, BALLDIAMETER)

        self.CreateBricks()
    def CreateBricks(self):
        self.bricks = []

        YPOS = 80
        for j in range(5):
            XPOS = 20  # Start of bricks
            for i in range(8):
                self.bricks.append(pygame.Rect(XPOS, YPOS, BRICKWIDTH, BRICKHEIGHT))
                XPOS += BRICKWIDTH + 5
            YPOS += BRICKHEIGHT + 5

    def CollisionDetect(self):

        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.bricks.remove(brick)
                self.BALL_VEL[1] = -self.BALL_VEL[1]
                self.score += 100
                break

        if self.ball.colliderect(self.paddle):
            self.ball.top = self.paddle.top - BALLDIAMETER
            self.BALL_VEL[1] = -self.BALL_VEL[1]

            if self.PADDLEVEL > 0:  # Paddle moving right
                self.BALL_VEL[0] = -5 #Ball moves left
            elif self.PADDLEVEL < 0:  # Paddle moving left
                self.BALL_VEL[0] = 5

        elif self.ball.top <= 0: #Hits top of screen
            self.BALL_VEL[1] = -self.BALL_VEL[1]

        elif self.ball.left <= 0 or self.ball.right >= 640: #Hits side of screen
            self.BALL_VEL[0] = -self.BALL_VEL[0]

        if self.paddle.left < 0: #Imposes left boundary
            self.paddle.left = 0

        elif self.paddle.right > 640:
            self.paddle.right = 640

    def InputChecker(self):

        if pygame.key.get_pressed()[K_LEFT]:  # move paddle left if left arrow is pressed
            self.PADDLEVEL = -5 #Can move left if paddle is not already at edge

        elif pygame.key.get_pressed()[K_RIGHT]:
            self.PADDLEVEL = 5

        else:
            self.PADDLEVEL = 0

        self.paddle.left += self.PADDLEVEL

    def GameLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.DISPLAY.fill(WHITE)

            if self.state != STATE_GAMEOVER:
                for y in self.bricks:
                    pygame.draw.rect(self.DISPLAY, BLUE, y)

                self.ball.top += self.BALL_VEL[1]
                self.ball.left += self.BALL_VEL[0]
                self.InputChecker()
                self.CollisionDetect()

                if self.state == STATE_BALL_ON_PADDLE:
                    self.BALL_VEL[1] = 0
                    self.ball.centerx = self.paddle.centerx
                    self.ball.bottom = self.paddle.top - 1
                    if pygame.key.get_pressed()[K_SPACE]:
                        self.BALL_VEL = [0,-5]
                        self.state = STATE_PLAYING

                BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
                GameOverSurf = BASICFONT.render("Game Over. Press enter to play again.", True, BLUE)
                GameOverRect = GameOverSurf.get_rect()
                GameOverRect.center = ((WIN_WIDTH/2), (WIN_HEIGHT/2)) #Game over, over half the screen

                SMALLFONT = pygame.font.Font('freesansbold.ttf', 16)
                StatSurf = SMALLFONT.render(("Score: " + str(self.score) + " Lives: " +
                                             str(self.lives)), True, BLUE)
                self.DISPLAY.blit(StatSurf, (250, 5))

                BALLCLOCK = pygame.time.Clock()
                BALLCLOCK.tick(30)

                if self.ball.top > 480: #Ball hits bottom
                    self.state = STATE_BALL_ON_PADDLE
                    self.lives -= 1

                if self.lives == 0 or pygame.key.get_pressed()[K_0]:
                    self.state = STATE_GAMEOVER

                pygame.draw.rect(self.DISPLAY, BLUE, self.paddle)
                pygame.draw.circle(self.DISPLAY, BLUE, (self.ball.left + BALLRADIUS,
                                                        self.ball.top + BALLRADIUS), BALLRADIUS)

            else:
                self.DISPLAY.blit(GameOverSurf, GameOverRect)
                if pygame.key.get_pressed()[K_RETURN]:
                    self.StartGame()

            pygame.display.update()

if __name__ == "__main__":
    BreakOff().GameLoop()




    



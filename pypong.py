import pygame
import random
import keyboard
import pygame.freetype


#-----------------------------------------------------CONSTANTS---------------------------------------------------------
MAXWIDTH = 1200
MAXHEIGHT = 700
LINE_WIDTH = 10

win = pygame.display.set_mode((MAXWIDTH, MAXHEIGHT))
pygame.display.set_caption("Pythong")
clock = pygame.time.Clock()
pygame.font.init()
pygame.freetype.init()
random.seed()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WEIRD = (100,100,100)
CBLUE = (100, 149, 237)

ROUND = 1
targetY = 100

#-------------------------------------------------------CLASSES---------------------------------------------------------
#------------------------                        BALL CLASS                 --------------------------------------------
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, x, y, xVel, yVel):
        super().__init__()
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.image = pygame.Surface([radius, radius])
        self.rect = self.image.get_rect()
    def draw(self, surface):
        #pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, self.radius)
        pygame.draw.rect(surface, self.color, (self.x - self.radius/2, self.y - self.radius/2, self.radius*2, self.radius*2))

    def update(self, paddleY, paddleWidth, paddleHeight, AIpaddleY):
        aiPoints, humanPoints = 0, 0
        global ROUND

        self.x += self.xVel
        self.y += self.yVel

    #--------making sure the ball doesn't reach lightspeed-----------
        if self.xVel > 25:
            self.xVel = 23
        elif self.xVel < -25:
            self.xVel = -23

    #-----------checking to see if the ball hits a paddle-------------
        if self.y <= 0 + self.radius or self.y >= MAXHEIGHT - self.radius:
            self.yVel = -self.yVel
        if self.x <= (0 + self.radius + paddleWidth + 10) and self.x >= 0:                       #REACHING LEFT BOUNDS
            if(self.y >= (paddleY - 2) and self.y <= paddleY + paddleHeight + 2):                 #CONTACT WITH PADDLE
                if(self.y >= (paddleY - 2) and self.y < (paddleY + paddleHeight/2)):        #CONTACT WITH UPPER PADDLE
                    if self.yVel >= 0:
                        self.yVel = (self.yVel * -1) - random.randint(0,2)
                elif(self.y >= (paddleY + 2 + paddleHeight/2) and self.y < paddleY + paddleHeight + 2): #LOWER CONTACT
                    if self.yVel <= 0:
                        self.yVel = (self.yVel * -1) + random.randint(0,2)
                self.xVel = 23 if abs(self.xVel) >= 24 else -self.xVel + (random.randint(-2,4)) + ROUND
        if self.x < 0:
            aiPoints = 1
            ROUND += 1
            self.x = 600
            self.y = random.randint(200, 500)

            self.xVel = random.choice([-1, 1]) * 9
            self.yVel = 4 if random.randint(0, 1) == 0 else -4

        if self.x >= (1200 - self.radius - paddleWidth - 10) and self.x <= 1200:                       #REACHING RIGHT BOUNDS
            if(self.y >= (AIpaddleY - 2) and self.y <= AIpaddleY + paddleHeight + 2):                 #CONTACT WITH  aiPADDLE
                if(self.y >= (AIpaddleY - 2) and self.y < (AIpaddleY + paddleHeight/2)):        #CONTACT WITH UPPER aiPADDLE
                    if self.yVel >= 0:
                        self.yVel = (self.yVel * -1) - random.randint(0, 2)
                elif(self.y >= (AIpaddleY + 2 + paddleHeight/2) and self.y < AIpaddleY + paddleHeight + 2): #LOWER CONTACT
                    if self.yVel <= 0:
                        self.yVel = (self.yVel * -1) + random.randint(0,2)
                self.xVel = -23 if abs(self.xVel) >= 24 else -self.xVel - (random.randint(-2, 4)) - ROUND

        if self.x > 1200:
            humanPoints = 1
            ROUND += 1
            self.x = 600
            self.y = random.randint(200, 500)

            self.xVel = random.choice([-1, 1]) * 9
            self.yVel = 4 if random.randint(0, 1) == 0 else -4

        if self.y >= 1190 or self.y <= 10:
            if self.yVel == 0:
                self.yVel = -4

        return aiPoints, humanPoints

    #getter functions
    def getY(self):
        return self.y

    def getYVel(self):
        return self.yVel

    def getX(self):
        return self.x

    def getXVel(self):
        return self.xVel
#------------------------                      PADDLE CLASS                 --------------------------------------------
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, yVel):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.yVel = yVel
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height),)
    def update(self, yVel):
        self.yVel = yVel
        if self.y + self.height >= (MAXHEIGHT - 10):
            self.y = (MAXHEIGHT - 11) - self.height
            #self.yVel = 0
        elif self.y <= 10:
            self.y = 11
            #self.yVel = 0
        self.y += self.yVel
    def getY(self):
        return self.y
    def getPaddleHeight(self):
        return self.height
    def getPaddleWidth(self):
        return self.width
#------------------------                   AI   PADDLE CLASS               --------------------------------------------
class AIPaddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, yVel, speed):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.yVel = yVel
        self.speed = speed
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()

    def update(self, ballX, ballY, ballXVel, ballYVel):
        global targetY
        if ballX > 600 and ballX < 630:             #setting a 'virtual' target Y coordinate for the aipaddle
            timeToReach = (1155 - ballX) / ballXVel
            targetY = timeToReach * ballYVel + ballY
            if targetY > 600:
                targetY -= 600
                targetY = 1200 - targetY
            elif targetY < 0:
                targetY = - targetY
            if min(18, ROUND) < random.randint(0, 20):  #making the computer make mistakes so the humans don't feel bad :)
                targetY += random.randint(-100, 100)


        distance = self.y - targetY

        if distance > 0:                               #trying to get to the target Y coordinate in time
            self.yVel = -self.speed
        elif distance < -80:
            self.yVel = self.speed
        elif distance == 0 or distance >= -80:
            self.yVel = 0

    #-------------------bounding code-------------------
        if self.y + self.height >= (MAXHEIGHT - 10):
            self.y = (MAXHEIGHT - 11) - self.height

        elif self.y <= 10:
            self.y = 11

        self.y += self.yVel

    def getY(self):
        return self.y

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height),)

    def getyVel(self):
        return self.yVel
#----------------------------------------------INITIALIZING OBJECTS-----------------------------------------------------

ball = Ball(WHITE, 8, 600, 20, -5, -4)
paddle = Paddle(WHITE, 20, 100, 10, 100, 0)
aiPaddle = AIPaddle(WHITE, 20, 100, 1170, 100, 0, 15)

aiPoints = 0
humanPoints = 0
aiPointsTemp = 0
humanPointsTemp = 0

pygame.freetype.SysFont("consolas", 24, False, False)
ballSpeed = pygame.freetype.SysFont("consolas", 20)
humanPointsDisplay = pygame.freetype.SysFont("consolas", 50)
roundDisplay = pygame.freetype.SysFont("consolas", 30)
menuDisplay = pygame.freetype.SysFont("consolas", 60)
menuItemsSmall = pygame.freetype.SysFont("consolas", 25)
menuItemsSmallest = pygame.freetype.SysFont("consolas", 15)

yVelocity = 0

#------------------------------------------------ACTUAL GAME LOOP-------------------------------------------------------
run = True
menu = True
stats = False
tick = 60

'''
while True:
    try:
        if keyboard.is_pressed('w'):
            run = True
            break
    except:
        break'''

def rules(rule):
    while rule:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rule = False
                main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    rule = False
                    main_menu()

        win.fill(BLACK)

        menuDisplay.render_to(win, (480, 10), "CONTROLS", WHITE)
        menuItemsSmall.render_to(win, (470, 300), "(UP) MOVE PADDLE UP" , WHITE)
        menuItemsSmall.render_to(win, (465, 400), "(DOWN) MOVE PADDLE DOWN", WHITE)
        menuItemsSmall.render_to(win, (471, 500), "(E) EXIT TO GAME", WHITE)
        if stats:
            menuItemsSmall.render_to(win, (451, 600), "(<-) (->) CONTROL TICK RATE", WHITE)
        menuItemsSmallest.render_to(win, (290, 680), "*Debug Mode enables tickrate control and displays velocity values", WHITE)

        pygame.display.update()

def main_menu():
    global menu
    global stats
    global run
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    menu = False
                elif event.key == pygame.K_s:
                    stats = not(stats)
                elif event.key == pygame.K_h:
                    rules(True)
                elif event.key == pygame.K_q:
                    run = False
                    menu = False

        win.fill(BLACK)

        menuDisplay.render_to(win, (480, 10),"PyThong" , WHITE)
        menuItemsSmall.render_to(win, (450, 300), "(S) DEBUG MODE* : "+str(stats), WHITE)
        menuItemsSmall.render_to(win, (450, 400), "(E) Start Game", WHITE)
        menuItemsSmall.render_to(win, (450, 500), "(H) HELP", WHITE)
        menuItemsSmall.render_to(win, (450, 600), "(Q) QUIT", WHITE)
        menuItemsSmallest.render_to(win, (290, 680), "*Debug Mode enables tickrate control and displays velocity values", WHITE)

        pygame.display.update()

while run:

    main_menu()

    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                yVelocity = -15 - ROUND // 5
            elif event.key == pygame.K_DOWN:
                yVelocity = +15 + ROUND // 5
            elif event.key == pygame.K_q:
                run = False

            elif event.key == pygame.K_LEFT:
                if stats:
                    if tick > 10:
                        tick -= 10
                    else:
                        tick = 10
            elif event.key == pygame.K_RIGHT:
                if stats:
                    tick += 10
        else:
            yVelocity = 0

    i = 40
    while i < MAXHEIGHT - 100:
        pygame.draw.rect(win, WEIRD, (596, i, 8, 30))
        i += 60

    ball.draw(win)

    aiPointsTemp, humanPointsTemp = ball.update(paddle.getY(),paddle.getPaddleWidth(), paddle.getPaddleHeight(), aiPaddle.getY())
    aiPoints += aiPointsTemp
    humanPoints += humanPointsTemp

    if stats:
        ballSpeed.render_to(win, (10, 40),"Ball Speed: "+ str(ball.getXVel())+","+str(ball.getYVel())+ "   AI Paddle: " +str(aiPaddle.getyVel()) , WHITE)
        ballSpeed.render_to(win, (900, 40)," TargetY : "+str(targetY), WHITE)

    humanPointsDisplay.render_to(win, (490, 40), str(humanPoints), WHITE)
    humanPointsDisplay.render_to(win, (700, 40), str(aiPoints), WHITE)
    roundDisplay.render_to(win, (500, 650), "Round : "+str(ROUND), WHITE)

    paddle.draw(win)
    paddle.update(yVelocity)

    aiPaddle.draw(win)
    aiPaddle.update(ball.getX(), ball.getY(),ball.getXVel(), ball.getYVel())



    pygame.display.update()
    clock.tick(tick)

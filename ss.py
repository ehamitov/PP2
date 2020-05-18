import pygame,random,os,sys,time,json,pika,uuid
from threading import Thread
from enum import Enum

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((1000, 600))
background_image = pygame.image.load("background3.png")
shoot_sound = pygame.mixer.Sound("crash.wav")
life1=3
life2=3
FPS = 30
mainClock = pygame.time.Clock()
pygame.mixer.music.load('sound.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
font = pygame.font.SysFont('Times new roman', 32)

def scores (x,y):
    result = font.render('life:  ' + str(life1), True, (255, 123, 100)) #draw text on a new Surf
    screen.blit(result, (x,y))

def scores1 (x,y):
    result = font.render('life:  ' + str(life2), True, (100, 230, 40)) #draw text on a new Surf
    screen.blit(result, (x,y))

def ends(life1,life2):
    myfont = pygame.font.SysFont('arial', 48)
    ending1 = myfont.render('P2 wins', True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    ending2 = myfont.render('P1 wins', True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    if life1==0:
        background_image = pygame.image.load('gameover5.jpg')
        screen.blit(background_image,(0,0))
        screen.blit(ending2,(300, 100))
        tank1.direction = Direction.STOP
        tank2.direction = Direction.STOP
    if life2==0:
        background_image = pygame.image.load('gameover5.jpg')
        screen.blit(background_image,(0,0))
        screen.blit(ending1,(300, 100))
        tank1.direction = Direction.STOP
        tank2.direction = Direction.STOP
def pluslife(life1,life2):
    myfont = pygame.font.SysFont('arial', 32)
    scan1 = myfont.render('P2 got one life',True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    scan2 = myfont.render('P1 got one life',True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    if sp1 == 1:
        screen.blit(scan1,(800,350))
    if sp2 == 1:
        screen.blit(scan2,(800,300))

def draw_pan():
    col =  ((127,127,127))
    pygame.draw.rect(screen,col,(800,0,200,600))


def drawText(text, font, color, surface, x, y) :
    textObject = font.render(text , 1, color)
    textRect = textObject.get_rect()
    textRect.topleft = (x,y)
    surface.blit(textObject, textRect)
    

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5

class Tank:
    def __init__(self, x, y, speed, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN, d_stop=pygame.K_RALT):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = 20
        self.direction = Direction.STOP
        self.life = 3

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN,
                    d_stop: Direction.STOP}

    def draw(self):
        tank_c = (self.x + int(self.width / 2), self.y + int(self.width / 2))
        pygame.draw.rect(screen, self.color,(self.x, self.y, self.width, self.width))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + int(self.width / 2), self.y + int(self.width / 2)), 4)
        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (self.x - int(self.width / 2), self.y + int(self.width / 2)), 4)
        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y - int(self.width / 2)), 4)
        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y + self.width + int(self.width / 2)), 4)
        if self.direction == Direction.STOP:
            if lastMoveOfTank1 == "right":
                pygame.draw.line(screen, tank1.color, (tank1.x + int(tank1.width / 2), tank1.y + int(tank1.width / 2)), (tank1.x + tank1.width + int(tank1.width / 2), tank1.y + int(tank1.width / 2)), 4)
            if lastMoveOfTank1 == "left":
                pygame.draw.line(screen, tank1.color, (tank1.x + int(tank1.width / 2), tank1.y + int(tank1.width / 2)), (tank1.x - int(tank1.width / 2), tank1.y + int(tank1.width / 2)), 4)
            if lastMoveOfTank1 == "up":
                pygame.draw.line(screen, tank1.color, (tank1.x + int(tank1.width / 2), tank1.y + int(tank1.width / 2)), (tank1.x + int(tank1.width / 2), tank1.y - int(tank1.width / 2)), 4)
            if lastMoveOfTank1 == "down":
                pygame.draw.line(screen, tank1.color, (tank1.x + int(tank1.width / 2), tank1.y + int(tank1.width / 2)), (tank1.x + int(tank1.width / 2), tank1.y + tank1.width + int(tank1.width / 2)), 4)

            if lastMoveOfTank2 == "right":
                pygame.draw.line(screen, tank2.color, (tank2.x + int(tank2.width / 2), tank2.y + int(tank2.width / 2)), (tank2.x + tank2.width + int(tank2.width / 2), tank2.y + int(tank2.width / 2)), 4)
            if lastMoveOfTank2 == "left":
                pygame.draw.line(screen, tank2.color, (tank2.x + int(tank2.width / 2), tank2.y + int(tank2.width / 2)), (tank2.x - int(tank2.width / 2), tank2.y + int(tank2.width / 2)), 4)
            if lastMoveOfTank2 == "up":
                pygame.draw.line(screen, tank2.color, (tank2.x + int(tank2.width / 2), tank2.y + int(tank2.width / 2)), (tank2.x + int(tank2.width / 2), tank2.y - int(tank2.width / 2)), 4)
            if lastMoveOfTank2 == "down":
                pygame.draw.line(screen, tank2.color, (tank2.x + int(tank2.width / 2), tank2.y + int(tank2.width / 2)), (tank2.x + int(tank2.width / 2), tank2.y + tank2.width + int(tank2.width / 2)), 4)

    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.speed0 = self.speed
            self.x -= self.speed0
        if self.direction == Direction.RIGHT: 
            self.speed0 = self.speed
            self.x += self.speed0
        if self.direction == Direction.UP: 
            self.speed0 = self.speed
            self.y -= self.speed0
        if self.direction == Direction.DOWN: 
            self.speed0 = self.speed
            self.y += self.speed0
        if self.direction == Direction.STOP:
            self.speed0 = 0
        self.draw()

class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 35, 35)

class Food():
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    
    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y) ,self.radius)

class bul():  
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color 

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

def edge1():
    if tank1.x > 800:
        tank1.x = 0
        tank1.x += tank1.speed
    if tank1.x < 0:
        tank1.x = 800
        tank1.x += tank1.speed
    if tank1.y > 600:
        tank1.y = 0
        tank1.y += tank1.speed
    if tank1.y < 0:
        tank1.y = 600
        tank1.y += tank1.speed

def edge2():
    if tank2.x > 800:
        tank2.x = 0
        tank2.x += tank2.speed
    if tank2.x < 0:
        tank2.x = 800
        tank2.x += tank2.speed
    if tank2.y > 600:
        tank2.y = 0
        tank2.y += tank2.speed
    if tank2.y < 0:
        tank2.y = 600
        tank2.y += tank2.speed
bullets1 = []
bullets2 = []
food1 = []
lastMoveOfTank1 = "left"
lastMoveOfTank2 = "right"

move1 = "RIGHT"
move2 = "RIGHT"

tank1 = Tank(540, 400, 3, (255, 123, 100))
tank2 = Tank(220, 380, 3, (100, 230, 40), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s,pygame.K_q)

tanks = [tank1, tank2]
blue= (0,0,200)
bright_blue = (0,0,255)
def button(msg,x,y,w,h,ic,ac, action = None):
    ms = pygame.mouse.get_pos()
    cl = pygame.mouse.get_pressed()

    if x+w > ms[0] > x and y+h > ms[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if cl[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h),4)

    Text = pygame.font.Font("freesansbold.ttf",15)
    textSurf, textRect = text_objects(msg, Text)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()

def menu():
    global run
    while True :
        menu_image = pygame.image.load("ground.jpg")
        screen.blit(menu_image, (0, 0))
        drawText("TANK Game", font, (255,255,255), screen, 200, 100)
         
        button("Single Player mode", 50,200,150,50,blue, bright_blue, singlePlayer)
        if run == False:
            button("Single Player mode", 50,200,150,50,blue, bright_blue, singlePlayer)

        button("Multiplayer mode", 50,300, 150,50, blue, bright_blue,multi)
        button("Multiplayer al mode", 50,400, 150,50, blue, bright_blue, multi_al)

        button("Exit",50,500, 150,50, blue, bright_blue,exit)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        mainClock.tick(30)      
run = True
sp1 = 0
sp2 = 0
def singlePlayer():  
    global run,life1,life2,lastMoveOfTank2,lastMoveOfTank1,sp1,sp2
    eat_food1 = False
    eat_food2 = False
    start_time = None
    bullet1 = 10
    bullet2 = 10
    start_time1 = None
    eat_food3 = False
    eat_food4 = False
    start_time2 = None
    foodinpole = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RETURN:
                    shoot_sound.play()
                    if len(bullets1) == 0:
                        if lastMoveOfTank1 == "right":
                            bullets1.append(bul(tank1.x + tank1.width + int(tank1.width / 2), tank1.y + int(tank1.width / 2), 5, (random.randint(0,255), random.randint(0,255), 100)))
                            move1 = "RIGHT"
                        if lastMoveOfTank1 == "left":
                            bullets1.append(bul(tank1.x - tank1.width + int(tank1.width / 2), tank1.y + int(tank1.width / 2), 5, (random.randint(0,255), random.randint(0,255), 100)))
                            move1 = "LEFT"
                        if lastMoveOfTank1 == "up": 
                            bullets1.append(bul(tank1.x + int(tank1.width / 2), tank1.y - int(tank1.width / 2), 5, (random.randint(0,255), random.randint(0,255), 100)))
                            move1 = "UP"
                        if lastMoveOfTank1 == "down":
                            bullets1.append(bul(tank1.x + int(tank1.width / 2), tank1.y + tank1.width + int(tank1.width / 2), 5, (random.randint(0,255), random.randint(0,255), 100)))
                            move1 = "DOWN"
                if event.key == pygame.K_SPACE:
                    shoot_sound.play()    
                    if len(bullets2) == 0: 
                        if lastMoveOfTank2 == "right":
                            bullets2.append(bul(tank2.x + tank2.width + int(tank2.width / 2), tank2.y + int(tank2.width / 2), 5, (random.randint(0,255), random.randint(0,255), 100)))
                            move2 = "RIGHT"
                        if lastMoveOfTank2 == "left":
                            bullets2.append(bul(tank2.x - tank2.width + int(tank2.width / 2), tank2.y + int(tank2.width / 2), 5, (random.randint(0,255), random.randint(0,255), 100)))
                            move2 = "LEFT"
                        if lastMoveOfTank2 == "up": 
                            bullets2.append(bul(tank2.x + int(tank2.width / 2), tank2.y - int(tank2.width / 2), 5, (random.randint(0,255), random.randint(0,255), 100)))
                            move2 = "UP"
                        if lastMoveOfTank2 == "down":
                            bullets2.append(bul(tank2.x + int(tank2.width / 2), tank2.y + tank2.width + int(tank2.width / 2), 5, (random.randint(0,255), random.randint(0,255), 100)))
                            move2 = "DOWN"

                for tank in tanks: 
                    if event.key in tank.KEY.keys():
                        tank.change_direction(tank.KEY[event.key])
        
        if len(food1) == 0:
            f = random.randint(10,770)
            g = random.randint(10,570)
            food1.append(Food(f,g,12,(random.randint(0,255), random.randint(0,255), 100)))
        if tank1.direction == Direction.LEFT:
            lastMoveOfTank1 = "left"
        if tank1.direction == Direction.RIGHT:
            lastMoveOfTank1 = "right"
        if tank1.direction == Direction.UP:
            lastMoveOfTank1 = "up"
        if tank1.direction == Direction.DOWN:
            lastMoveOfTank1 = "down"

        if tank2.direction == Direction.LEFT:
            lastMoveOfTank2 = "left"
        if tank2.direction == Direction.RIGHT:
            lastMoveOfTank2 = "right"
        if tank2.direction == Direction.UP:
            lastMoveOfTank2 = "up"
        if tank2.direction == Direction.DOWN:
            lastMoveOfTank2 = "down"
        
        for bullet in bullets1:
            if bullet.x > 0 and bullet.x < 800 and bullet.y > 0 and bullet.y < 600:
                if move1 == "RIGHT":
                    bullet.x += bullet1
                if move1 == "LEFT":
                    bullet.x -= bullet1
                if move1 == "UP":
                    bullet.y -= bullet1
                if move1 == "DOWN":
                    bullet.y += bullet1
            else:
                bullets1.pop(bullets1.index(bullet))

        for bullet in bullets2:
            if bullet.x > 0 and bullet.x < 800 and bullet.y > 0 and bullet.y < 600:
                if move2 == "RIGHT":
                    bullet.x += bullet2
                if move2 == "LEFT":
                    bullet.x -= bullet2
                if move2 == "UP":
                    bullet.y -= bullet2
                if move2 == "DOWN":
                    bullet.y += bullet2
            else:
                bullets2.pop(bullets2.index(bullet))
        
        #changeplaceofbullet
        for bullet in bullets1 :
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RCTRL]:
                tank1.x = bullet.x
                tank1.y = bullet.y
                bullets1.pop(bullets1.index(bullet))
            if bullet.y >= tank2.y and bullet.y <= tank2.y + tank2.width and bullet.x >= tank2.x and bullet.x <= tank2.x + tank2.width :
                bullets1.pop(bullets1.index(bullet))
                life2 -= 1
                tank2.x,tank2.y = 220,380
            
        #changeplaceofbullet
        for bullet in bullets2 :
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LCTRL]:
                tank2.x = bullet.x
                tank2.y = bullet.y
                bullets2.pop(bullets2.index(bullet))
            if bullet.y >= tank1.y and bullet.y <= tank1.y + tank1.width and bullet.x >= tank1.x and bullet.x <= tank1.x + tank1.width :
                bullets2.pop(bullets2.index(bullet))
                life1 -= 1
                tank1.x,tank1.y = 540,400
        #collision
        if tank2.x + tank2.width >= tank1.x >= tank2.x and tank2.y + tank2.width >= tank1.y >= tank2.y:
            tank1.x += tank1.speed
            tank2.x -= tank2.speed
        if tank2.x + tank2.width >= tank1.x + tank1.width >= tank2.x and tank2.y + tank2.width >= tank1.y >= tank2.y:
            tank1.y += tank1.speed
            tank2.y -= tank2.speed
        if tank2.x + tank2.width >= tank1.x >= tank2.x and tank2.y + tank2.width >= tank1.y + tank1.width >= tank2.y:
            tank1.y -= tank1.speed
            tank2.y += tank2.speed
        if tank2.x + tank2.width >= tank1.x + tank1.width >= tank2.x and tank2.y + tank2.width >= tank1.y + tank1.width >= tank2.y:
            tank1.x -= tank1.speed
            tank2.x += tank2.speed
        
        for wall in walls:
            if wall.rect.x + wall.rect.width >= tank1.x >= wall.rect.x and wall.rect.y + wall.rect.width >= tank1.y >= wall.rect.y:
                walls.pop(walls.index(wall))
                life1 -= 1
                tank1.x,tank1.y = 540,400
                tank1.direction = Direction.STOP
                if life1 == 0:
                    tank1.direction = Direction.STOP
                    tank2.direction = Direction.STOP

            if wall.rect.x + wall.rect.width >= tank1.x + tank1.width >= wall.rect.x and wall.rect.y + wall.rect.width >= tank1.y >= wall.rect.y:
                walls.pop(walls.index(wall))
                life1 -= 1
                tank1.x,tank1.y = 540,400
                tank1.direction = Direction.STOP
                if life1 == 0:
                    tank1.direction = Direction.STOP
                    tank2.direction = Direction.STOP

            if wall.rect.x + wall.rect.width >= tank1.x >= wall.rect.x and wall.rect.y + wall.rect.width >= tank1.y + tank1.width >= wall.rect.y:
                walls.pop(walls.index(wall))
                life1 -= 1
                tank1.x,tank1.y = 540,400
                tank1.direction = Direction.STOP
                if life1 == 0:
                    tank1.direction = Direction.STOP
                    tank2.direction = Direction.STOP

            if wall.rect.x + wall.rect.width >= tank1.x + tank1.width >= wall.rect.x and wall.rect.y + wall.rect.width >= tank1.y + tank1.width >= wall.rect.y:
                walls.pop(walls.index(wall))
                life1 -= 1
                tank1.x,tank1.y = 540,400
                tank1.direction = Direction.STOP
                if life1 == 0:
                    tank1.direction = Direction.STOP
                    tank2.direction = Direction.STOP
        
        for wall in walls:
            if wall.rect.x + wall.rect.width >= tank2.x >= wall.rect.x and wall.rect.y + wall.rect.width >= tank2.y >= wall.rect.y:
                walls.pop(walls.index(wall))
                life2 -= 1
                tank2.x,tank2.y = 220,380
                tank2.direction = Direction.STOP
                if life2 == 0:
                    tank1.direction = Direction.STOP
                    tank2.direction = Direction.STOP

            if wall.rect.x + wall.rect.width >= tank2.x + tank2.width >= wall.rect.x and wall.rect.y + wall.rect.width >= tank2.y >= wall.rect.y:
                walls.pop(walls.index(wall))
                life2 -= 1
                tank2.x,tank2.y = 220,380
                tank2.direction = Direction.STOP
                if life2 == 0:
                    tank1.direction = Direction.STOP
                    tank2.direction = Direction.STOP

            if wall.rect.x + wall.rect.width >= tank2.x >= wall.rect.x and wall.rect.y + wall.rect.width >= tank2.y + tank2.width >= wall.rect.y:
                walls.pop(walls.index(wall))
                life2 -= 1
                tank2.x,tank2.y = 220,380
                tank2.direction = Direction.STOP
                if life2 == 0:
                    tank1.direction = Direction.STOP
                    tank2.direction = Direction.STOP

            if wall.rect.x + wall.rect.width >= tank2.x + tank1.width >= wall.rect.x and wall.rect.y + wall.rect.width >= tank2.y + tank2.width >= wall.rect.y:
                walls.pop(walls.index(wall))
                life2 -= 1
                tank2.x,tank2.y = 220,380
                tank2.direction = Direction.STOP
                if life2 == 0:
                    tank1.direction = Direction.STOP
                    tank2.direction = Direction.STOP

        for bullet in bullets1:
            for wall in walls:
                if bullet.y >= wall.rect.y and bullet.y <= wall.rect.y + wall.rect.width and bullet.x >= wall.rect.x and bullet.x <= wall.rect.x + wall.rect.width :
                    walls.pop(walls.index(wall))
                    bullets1.pop(bullets1.index(bullet))

        for bullet in bullets2:
            for wall in walls:
                if bullet.y >= wall.rect.y and bullet.y <= wall.rect.y + wall.rect.width and bullet.x >= wall.rect.x and bullet.x <= wall.rect.x + wall.rect.width :
                    walls.pop(walls.index(wall))
                    bullets2.pop(bullets2.index(bullet))
        
        for food in food1:
            if food.y >= tank1.y and food.y <= tank1.y + tank1.width and food.x >= tank1.x and food.x <= tank1.x + tank1.width :
                if random.randint(1,2) == 1:
                    eat_food3 = True
                    life1+=1
                    start_time1 = pygame.time.get_ticks()
                if random.randint(1,2) == 2:
                    eat_food1 = True
                    start_time = pygame.time.get_ticks()
                start_time2 = pygame.time.get_ticks()
                foodinpole = True
                food1.pop(food1.index(food))
        if foodinpole == True:
            if start_time2:
                if pygame.time.get_ticks()-start_time2 >(random.randint(10,20)*1000):
                    foodinpole = False
                if foodinpole == False:
                    food1.pop(food1.index(food))
        if eat_food3 == True:
            sp1 = 1
            if start_time1:
                if pygame.time.get_ticks()-start_time1 > 3000:
                    eat_food3 = False
            if eat_food3 == False:
                sp1 = 0
        if eat_food1 == True:
            tank1.speed = 2
            bullet1 = 20
            if start_time:
                if pygame.time.get_ticks()-start_time > 5000:
                    eat_food1 = False
            if eat_food1 == False:
                tank1.speed = 3
                bullet1 = 10              
        
        for food in food1:
            if food.y >= tank2.y and food.y <= tank2.y + tank2.width and food.x >= tank2.x and food.x <= tank2.x + tank2.width :
                if random.randint(1,2) == 1:
                    eat_food4 = True
                    life2+=1
                    start_time1 = pygame.time.get_ticks()
                if random.randint(1,2) == 2:
                    eat_food2 = True
                    start_time = pygame.time.get_ticks()
                start_time2 = pygame.time.get_ticks()
                foodinpole = True
                food1.pop(food1.index(food))
        if foodinpole == True:
            if start_time2:
                if pygame.time.get_ticks()-start_time2 >(random.randint(10,20)*1000):
                    foodinpole = False
                if foodinpole == False:
                    food1.pop(food1.index(food))
        if eat_food4 == True:
            sp2 = 1
            if start_time1:
                if pygame.time.get_ticks()-start_time1 > 3000:
                    eat_food4 = False
            if eat_food4 == False:
                sp2 = 0
        if eat_food2 == True:
            tank2.speed = 2
            bullet2 = 20
            if start_time:
                if pygame.time.get_ticks()-start_time > 5000:
                    eat_food2 = False
            if eat_food2 == False:
                tank2.speed = 3
                bullet2 = 10


        screen.blit(background_image, (0, 0))
        pygame.display.set_caption('TANK Game')
        for wall in walls:
            pygame.draw.rect(screen, (255, 255, 255), wall.rect,3)
        draw_pan()
        edge1()
        edge2()
        pluslife(life1,life2)
        for tank in tanks:
            tank.move()
        for bullet in bullets1:
            bullet.draw(screen)
        for bullet in bullets2:
            bullet.draw(screen)
        for food in food1:
            food.draw(screen)
        ends(life1,life2)
        mainClock.tick(FPS)
        scores(850,530)
        scores1(850,30)
        pygame.display.flip()
def multi():
    screen = pygame.display.set_mode((1000, 600))


    IP = '34.254.177.17'
    PORT = 5672
    VIRTUAL_HOST = 'dar-tanks'
    USER = 'dar-tanks'
    PASSWORD = '5orPLExUYnyVYZg48caMpX'


    class TankRpcClient():
        
        def __init__(self):
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = IP,
                    port = PORT,
                    virtual_host = VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username = USER,
                        password = PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            queue = self.channel.queue_declare(queue='',auto_delete=True,exclusive=True)
            self.callback_queue = queue.method.queue
            self.channel.queue_bind(
                exchange='X:routing.topic',
                queue = self.callback_queue)

            self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
                auto_ack=True
            )

            self.response = None
            self.corr_id = None
            self.token = None
            self.tank_id = None
            self.room_id = None

        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = json.loads(body)
                print(self.response)
    

        def call(self, key, message={}):
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key=key,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=json.dumps(message)
                )
            while self.response is None:
                self.connection.process_data_events()
        
        def check_server_status(self):
            self.call('tank.request.healthcheck')
            return self.response['status'] == '200'
        
        def obtain_token(self, room_id):
            
            message = {
                'roomId': room_id
            }
            self.call('tank.request.register', message)
            if 'token' in self.response:
                self.token = self.response['token']
                self.tank_id = self.response['tankId']
                if self.tank_id == client.tank_id:
                    return 1
                else : return 0
                self.room_id = self.response['roomId']
                return True
            return False


        def turn_tank(self, token, direction):
            message = {
                'token': token,
                'direction': direction
            }
            self.call('tank.request.turn', message)

        def fire_bullet(self, token):
            message = {
                'token': token
            }
            self.call('tank.request.fire', message)
        
        

    class TankConsumerClient(Thread):
        def __init__(self, room_id):
            super().__init__()
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = IP,
                    port = PORT,
                    virtual_host = VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username = USER,
                        password = PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            queue = self.channel.queue_declare(queue='',auto_delete=True,exclusive=True)

            event_listener = queue.method.queue
            self.channel.queue_bind(exchange='X:routing.topic', queue=event_listener, routing_key='event.state.'+room_id)

            self.channel.basic_consume(
                queue=event_listener,
                on_message_callback=self.on_response,
                auto_ack=True
            )
            self.response = None
        def on_response(self, ch, method, props, body):
            self.response = json.loads(body)
        def run(self):
            self.channel.start_consuming()

        def close(self):
            self.connection.close()
        

    UP = 'UP'
    DOWN = 'DOWN'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'

    tank1_down = pygame.image.load('ver1 down.png')
    tank1_down= pygame.transform.scale(tank1_down,(31,31))
    tank1_up = pygame.image.load('ver1 up.png')
    tank1_up= pygame.transform.scale(tank1_up,(31,31))
    tank1_right = pygame.image.load('ver1 right.png')
    tank1_right= pygame.transform.scale(tank1_right,(31,31))
    tank1_left = pygame.image.load('ver1 left.png')
    tank1_left= pygame.transform.scale(tank1_left,(31,31))
    tank2_down = pygame.image.load('ver2 down.png')
    tank2_down= pygame.transform.scale(tank2_down,(31,31))
    tank2_up = pygame.image.load('ver2 up.png')
    tank2_up= pygame.transform.scale(tank2_up,(31,31))
    tank2_right = pygame.image.load('ver2 right.png')
    tank2_right= pygame.transform.scale(tank2_right,(31,31))
    tank2_left = pygame.image.load('ver2 left.png')
    tank2_left= pygame.transform.scale(tank2_left,(31,31))
    background = pygame.image.load('ic1.jpg')
    background = pygame.transform.scale(background,(800,600))

    def draw_bullets(x, y, width, height, direction):
        col = (127,127,127)
        bullet_c = (x + int(width / 2), y + int(height / 2))
        pygame.draw.rect(screen, col,
                        (x, y, width, height), 2)
    def draw_bullets1(x, y, width, height, direction):
        col = (255,234,99)
        bullet1_c = (x + int(width / 2), y + int(height / 2))
        pygame.draw.rect(screen, col,
                        (x, y, width, height), 2)

    def draw_tank(x, y, width, height, direction,health,score,id):
        if direction == 'RIGHT':
            screen.blit(tank1_right, (x,y))
        if direction == 'LEFT':
            screen.blit(tank1_left, (x,y))
        if direction == 'UP':
            screen.blit(tank1_up, (x,y))
        if direction == 'DOWN':
            screen.blit(tank1_down, (x,y))
        screen.blit(Font1.render(f"{id}",True,(255,255,255)),(x,y-int(width/2)))
    Font1 = pygame.font.Font('freesansbold.ttf', 12)
    def draw_tank1(x, y, width, height, direction,health,score,id):
        if direction == 'RIGHT':
            screen.blit(tank2_right, (x,y))
        if direction == 'LEFT':
            screen.blit(tank2_left, (x,y))
        if direction == 'UP':
            screen.blit(tank2_up, (x,y))
        if direction == 'DOWN':
            screen.blit(tank2_down, (x,y))
        screen.blit(Font1.render(f"{id}",True,(255,255,255)),(x,y-int(width/2)))
    def draw_pan():
        col = (255,255,255)
        pygame.draw.rect(screen,col,(800,0,200,600))
    def game_over():
        background_image = pygame.image.load('gameover4.jpg')
        screen.blit(background_image,(0,0))
    def game1_over():
        background_image = pygame.image.load('gameover4.jpg')
        screen.blit(background_image,(0,0))
    def game2_over():
        background_image = pygame.image.load('gameover4.jpg')
        screen.blit(background_image,(0,0))
    def game_start():
        mainloop = True
        font = pygame.font.Font('freesansbold.ttf', 32)
        font1 = pygame.font.Font('freesansbold.ttf', 12)
        eazy = False
        eazy1 = False
        eazy2 = False
        while mainloop:
            screen.blit(background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False
                    if event.key == pygame.K_RIGHT:
                        client.turn_tank(client.token, RIGHT)
                    if event.key == pygame.K_LEFT:
                        client.turn_tank(client.token, LEFT)
                    if event.key == pygame.K_UP:
                        client.turn_tank(client.token, UP)
                    if event.key == pygame.K_DOWN:
                        client.turn_tank(client.token, DOWN)
                    if event.key == pygame.K_SPACE:
                        shoot_sound.play()
                        client.fire_bullet(client.token)


            try:
                draw_pan()
                remaining_time = event_client.response['remainingTime']
                text = font.render('Remaining Time: {}'.format(remaining_time), True, (255,255,255))
                tanks = event_client.response['gameField']['tanks']
                bullets = event_client.response['gameField']['bullets']
                winners = event_client.response['winners']
                losers = event_client.response['losers']
                kicked = event_client.response['kicked']
                hits = event_client.response['hits']
                textRect = text.get_rect()
                textRect.center = (400,50)
                screen.blit(text, textRect)
                for kicks in kicked:
                    if kicks['tankId'] == client.tank_id:
                        eazy2 = True
                if eazy2 == True:
                    game2_over()
                    myfont = pygame.font.SysFont('arial', 48)
                    ending1_1 = myfont.render(' You kicked. Total score:{}'.format(kicks['score']), True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                    screen.blit(ending1_1,(300, 100))
                for lose in losers:
                    if lose['tankId'] == client.tank_id:
                        eazy1 = True
                if eazy1 == True:
                    game1_over()
                    myfont = pygame.font.SysFont('arial', 48)
                    ending1_1 = myfont.render('You lose. Total score:{}'.format(lose['score']), True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                    screen.blit(ending1_1,(300, 100))
                for win in winners:
                    if win['tankId'] == client.tank_id:
                        eazy = True
                if eazy == True:
                    game_over()
                    myfont = pygame.font.SysFont('arial', 48)
                    ending1_1 = myfont.render(' You won. Total score:{}'.format(win['score']), True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                    screen.blit(ending1_1,(300, 100))
                for bullet in bullets:
                    if bullet['owner'] == client.tank_id:
                        bullet_x = bullet['x']
                        bullet_y = bullet['y']
                        bullet_width = bullet['width']
                        bullet_height = bullet['height']
                        bullet_direction = bullet['direction']
                        draw_bullets(bullet_x, bullet_y, bullet_width, bullet_height,bullet_direction)
                    else:
                        bullet1_x = bullet['x']
                        bullet1_y = bullet['y']
                        bullet1_width = bullet['width']
                        bullet1_height = bullet['height']
                        bullet1_direction = bullet['direction']
                        draw_bullets1(bullet1_x, bullet1_y, bullet1_width, bullet1_height,bullet1_direction)

                l = 0
                for tank in sorted(tanks, key = lambda x:x['score'],reverse=True):
                    text1 = font1.render('ID: {}'.format(tank["id"])+' Health: {}'.format(tank["health"])+' Score:{}'.format(tank["score"]), True, (0, 0, 0))
                    screen.blit(text1, (800,l))
                    l+=20
                    if tank["id"] == client.tank_id:
                        tank_x = tank['x']
                        tank_y = tank['y']
                        tank_width = tank['width']
                        tank_height = tank['height']
                        tank_direction = tank['direction']
                        tank_health = tank['health']
                        tank_score = tank['score']
                        tank_id =tank['id']
                        draw_tank(tank_x, tank_y, tank_width, tank_height, tank_direction,tank_health,tank_score,tank_id)
                    else:
                        tank1_x = tank['x']
                        tank1_y = tank['y']
                        tank1_width = tank['width']
                        tank1_height = tank['height']
                        tank1_direction = tank['direction']
                        tank1_health = tank['health']
                        tank1_score = tank['score']
                        tank1_id = tank['id']
                        draw_tank1(tank1_x,tank1_y, tank1_width, tank1_height, tank1_direction,tank1_health,tank1_score,tank1_id)
            except:
                pass
            pygame.display.flip()
        client.connection.close()

    client = TankRpcClient()
    client.check_server_status()
    rooms = ['room-1','room-2','room-3','room-4','room-5','room-6','room-7',
            'room-8','room-9','room-10','room-11','room-12','room-13','room-14',
            'room-15','room-16','room-17','room-18','room-19','room-20',
            'room-21','room-22','room-23','room-24','room-25','room-26','room-27',
            'room-28','room-29','room-30']
    room = random.choice(rooms)
    client.obtain_token(room)
    event_client = TankConsumerClient(room)

    event_client.start()
    game_start()

def multi_al():    
    screen = pygame.display.set_mode((1000, 600))


    IP = '34.254.177.17'
    PORT = 5672
    VIRTUAL_HOST = 'dar-tanks'
    USER = 'dar-tanks'
    PASSWORD = '5orPLExUYnyVYZg48caMpX'


    class TankRpcClient():
        
        def __init__(self):
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = IP,
                    port = PORT,
                    virtual_host = VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username = USER,
                        password = PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            queue = self.channel.queue_declare(queue='',auto_delete=True,exclusive=True)
            self.callback_queue = queue.method.queue
            self.channel.queue_bind(
                exchange='X:routing.topic',
                queue = self.callback_queue)

            self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
                auto_ack=True
            )

            self.response = None
            self.corr_id = None
            self.token = None
            self.tank_id = None
            self.room_id = None

        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = json.loads(body)
                print(self.response)
    

        def call(self, key, message={}):
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key=key,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=json.dumps(message)
                )
            while self.response is None:
                self.connection.process_data_events()
        
        def check_server_status(self):
            self.call('tank.request.healthcheck')
            return self.response['status'] == '200'
        
        def obtain_token(self, room_id):
            
            message = {
                'roomId': room_id
            }
            self.call('tank.request.register', message)
            if 'token' in self.response:
                self.token = self.response['token']
                self.tank_id = self.response['tankId']
                if self.tank_id == client.tank_id:
                    return 1
                else : return 0
                self.room_id = self.response['roomId']
                return True
            return False


        def turn_tank(self, token, direction):
            message = {
                'token': token,
                'direction': direction
            }
            self.call('tank.request.turn', message)

        def fire_bullet(self, token):
            message = {
                'token': token
            }
            self.call('tank.request.fire', message)
        
        

    class TankConsumerClient(Thread):
        def __init__(self, room_id):
            super().__init__()
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = IP,
                    port = PORT,
                    virtual_host = VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username = USER,
                        password = PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            queue = self.channel.queue_declare(queue='',auto_delete=True,exclusive=True)

            event_listener = queue.method.queue
            self.channel.queue_bind(exchange='X:routing.topic', queue=event_listener, routing_key='event.state.'+room_id)

            self.channel.basic_consume(
                queue=event_listener,
                on_message_callback=self.on_response,
                auto_ack=True
            )
            self.response = None
        def on_response(self, ch, method, props, body):
            self.response = json.loads(body)
        def run(self):
            self.channel.start_consuming()

        def close(self):
            self.connection.close()
        

    UP = 'UP'
    DOWN = 'DOWN'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'

    tank1_down = pygame.image.load('ver1 down.png')
    tank1_down= pygame.transform.scale(tank1_down,(31,31))
    tank1_up = pygame.image.load('ver1 up.png')
    tank1_up= pygame.transform.scale(tank1_up,(31,31))
    tank1_right = pygame.image.load('ver1 right.png')
    tank1_right= pygame.transform.scale(tank1_right,(31,31))
    tank1_left = pygame.image.load('ver1 left.png')
    tank1_left= pygame.transform.scale(tank1_left,(31,31))
    tank2_down = pygame.image.load('ver2 down.png')
    tank2_down= pygame.transform.scale(tank2_down,(31,31))
    tank2_up = pygame.image.load('ver2 up.png')
    tank2_up= pygame.transform.scale(tank2_up,(31,31))
    tank2_right = pygame.image.load('ver2 right.png')
    tank2_right= pygame.transform.scale(tank2_right,(31,31))
    tank2_left = pygame.image.load('ver2 left.png')
    tank2_left= pygame.transform.scale(tank2_left,(31,31))
    background = pygame.image.load('ic1.jpg')
    background = pygame.transform.scale(background,(800,600))
    Font1 = pygame.font.Font('freesansbold.ttf', 12)

    def draw_bullets(x, y, width, height, direction):
        col = (127,127,127)
        bullet_c = (x + int(width / 2), y + int(height / 2))
        pygame.draw.rect(screen, col,
                        (x, y, width, height), 2)
    def draw_bullets1(x, y, width, height, direction):
        col = (255,234,99)
        bullet1_c = (x + int(width / 2), y + int(height / 2))
        pygame.draw.rect(screen, col,
                        (x, y, width, height), 2)

    def draw_tank(x, y, width, height, direction,health,score,id):
        if direction == 'RIGHT':
            screen.blit(tank1_right, (x,y))
        if direction == 'LEFT':
            screen.blit(tank1_left, (x,y))
        if direction == 'UP':
            screen.blit(tank1_up, (x,y))
        if direction == 'DOWN':
            screen.blit(tank1_down, (x,y))
        screen.blit(Font1.render(f"{id}",True,(255,255,255)),(x,y-int(width/2)))

    def draw_tank1(x, y, width, height, direction,health,score,id):
        if direction == 'RIGHT':
            screen.blit(tank2_right, (x,y))
        if direction == 'LEFT':
            screen.blit(tank2_left, (x,y))
        if direction == 'UP':
            screen.blit(tank2_up, (x,y))
        if direction == 'DOWN':
            screen.blit(tank2_down, (x,y))
        screen.blit(Font1.render(f"{id}",True,(255,255,255)),(x,y-int(width/2)))
    def draw_pan():
        col = (255,255,255)
        pygame.draw.rect(screen,col,(800,0,200,600))
    def game_over():
        background_image = pygame.image.load('gameover4.jpg')
        screen.blit(background_image,(0,0))

    def game1_over():
        background_image = pygame.image.load('gameover4.jpg')
        screen.blit(background_image,(0,0))
    def game2_over():
        background_image = pygame.image.load('gameover4.jpg')
        screen.blit(background_image,(0,0))

    def game_start():
        mainloop = True
        font = pygame.font.Font('freesansbold.ttf', 32)
        font1 = pygame.font.Font('freesansbold.ttf', 12)
        eazy = False
        eazy1 = False
        eazy2 = False
        while mainloop:
            screen.blit(background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False
            try:
                draw_pan()
                remaining_time = event_client.response['remainingTime']
                text = font.render('Remaining Time: {}'.format(remaining_time), True, (255,255,255))
                tanks = event_client.response['gameField']['tanks']
                bullets = event_client.response['gameField']['bullets']
                winners = event_client.response['winners']
                losers = event_client.response['losers']
                kicked = event_client.response['kicked']
                hits = event_client.response['hits']
                textRect = text.get_rect()
                textRect.center = (400,50)
                screen.blit(text, textRect)
                for kicks in kicked:
                    if kicks['tankId'] == client.tank_id:
                        eazy2 = True
                if eazy2 == True:
                    game2_over()
                    myfont = pygame.font.SysFont('arial', 48)
                    ending1_1 = myfont.render(' You kicked. Total score:{}'.format(kicks['score']), True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                    screen.blit(ending1_1,(300, 100))
                for lose in losers:
                    if lose['tankId'] == client.tank_id:
                        eazy1 = True
                if eazy1 == True:
                    game1_over()
                    myfont = pygame.font.SysFont('arial', 48)
                    ending1_1 = myfont.render('You lose. Total score:{}'.format(lose['score']), True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                    screen.blit(ending1_1,(300, 100))
                for win in winners:
                    if win['tankId'] == client.tank_id:
                        eazy = True
                if eazy == True:
                    game_over()
                    myfont = pygame.font.SysFont('arial', 48)
                    ending1_1 = myfont.render(' You won. Total score:{}'.format(win['score']), True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                    screen.blit(ending1_1,(300, 100))
                for bullet in bullets:
                    if bullet['owner'] == client.tank_id:
                        bullet_x = bullet['x']
                        bullet_y = bullet['y']
                        bullet_width = bullet['width']
                        bullet_height = bullet['height']
                        bullet_direction = bullet['direction']
                        draw_bullets(bullet_x, bullet_y, bullet_width, bullet_height,bullet_direction)
                    else:
                        bullet1_x = bullet['x']
                        bullet1_y = bullet['y']
                        bullet1_width = bullet['width']
                        bullet1_height = bullet['height']
                        bullet1_direction = bullet['direction']
                        draw_bullets1(bullet1_x, bullet1_y, bullet1_width, bullet1_height,bullet1_direction)
                
                l = 0
                for tank in sorted(tanks, key = lambda x:x['score'],reverse=True):
                    text1 = font1.render('ID: {}'.format(tank["id"])+' Health: {}'.format(tank["health"])+' Score:{}'.format(tank["score"]), True, (0,0,0))
                    screen.blit(text1, (800,l))
                    l+=20
                    if tank["id"] == client.tank_id:
                        tank_x = tank['x']
                        tank_y = tank['y']
                        tank_width = tank['width']
                        tank_height = tank['height']
                        tank_direction = tank['direction']
                        tank_health = tank['health']
                        tank_score = tank['score']
                        tank_id = tank['id']
                        draw_tank(tank_x, tank_y, tank_width, tank_height, tank_direction,tank_health,tank_score,tank_id)
                    else:
                        tank1_x = tank['x']
                        tank1_y = tank['y']
                        tank1_width = tank['width']
                        tank1_height = tank['height']
                        tank1_direction = tank['direction']
                        tank1_health = tank['health']
                        tank1_score = tank['score']
                        tank1_id = tank['id']
                        draw_tank1(tank1_x,tank1_y, tank1_width, tank1_height, tank1_direction,tank1_health,tank1_score,tank1_id)
                if tank_y <= tank1_y + 62 and tank_y >= tank1_y - 62 and tank_x > tank1_x and tank1_direction == LEFT:
                    client.turn_tank(client.token, LEFT)
                    client.fire_bullet(client.token)
                elif tank_y <= tank1_y + 62 and tank_y >= tank1_y - 62 and tank_x < tank1_x and tank1_direction == RIGHT:
                    client.turn_tank(client.token, RIGHT)
                    client.fire_bullet(client.token)
                elif tank_x <= tank1_x + 62 and tank_x >= tank1_x - 62 and tank_y > tank1_y and tank1_direction== UP:
                    client.turn_tank(client.token, UP)
                    client.fire_bullet(client.token)
                elif tank_x <= tank1_x + 62 and tank_x >= tank1_x - 62 and tank_y < tank1_y and tank1_direction== DOWN:
                    client.turn_tank(client.token, DOWN)
                    client.fire_bullet(client.token)
                elif tank_x <= tank1_x + 62 and tank_x >= tank1_x - 62 and tank_y < tank1_y and tank1_direction==UP:
                    client.turn_tank(client.token, DOWN)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, RIGHT)
                elif tank_x <= tank1_x + 62 and tank_x >= tank1_x - 62 and tank_y < tank1_y and tank1_direction==LEFT:
                    client.turn_tank(client.token, DOWN)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, LEFT)
                elif tank_x <= tank1_x + 62 and tank_x >= tank1_x - 62 and tank_y > tank1_y and tank1_direction==DOWN:
                    client.turn_tank(client.token, UP)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, RIGHT)
                elif tank_y <= tank1_y + 62 and tank_y >= tank1_y - 62 and tank_x > tank1_x and tank1_direction == RIGHT:
                    client.turn_tank(client.token, LEFT)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, DOWN)
                elif tank_y <= tank1_y + 62 and tank_y >= tank1_y - 62 and tank_x < tank1_x and tank1_direction == LEFT:
                    client.turn_tank(client.token, RIGHT)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, DOWN)
                elif tank_y <= tank1_y + 62 and tank_y >= tank1_y - 62 and tank_x < tank1_x and tank1_direction==UP:
                    client.turn_tank(client.token, RIGHT)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, UP)
                elif tank_y <= tank1_y + 62 and tank_y >= tank1_y - 62 and tank_x > tank1_x and tank1_direction==DOWN:
                    client.turn_tank(client.token, LEFT)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, DOWN)
                elif tank_x <= tank1_x + 62 and tank_x >= tank1_x - 62 and tank_y > tank1_y  and tank1_direction==RIGHT:
                    client.turn_tank(client.token, UP)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, RIGHT)
                elif tank_y <= tank1_y + 62 and tank_y >= tank1_y - 62 and tank_x > tank1_x and tank1_direction==UP:
                    client.turn_tank(client.token, LEFT)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, UP)
                elif tank_y <= tank1_y + 62 and tank_y >= tank1_y - 62 and tank_x < tank1_x and tank1_direction==DOWN:
                    client.turn_tank(client.token, RIGHT)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, DOWN)
                elif tank_x <= tank1_x + 62 and tank_x >= tank1_x - 62 and tank_y < tank1_y  and tank1_direction==RIGHT:
                    client.turn_tank(client.token, DOWN)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, RIGHT)
                elif tank_x <= tank1_x + 62 and tank_x >= tank1_x - 62 and tank_y > tank1_y and tank1_direction==LEFT:
                    client.turn_tank(client.token, UP)
                    client.fire_bullet(client.token)
                    client.turn_tank(client.token, LEFT)
                elif tank_x >= bullet1_x - 20 and tank_x <= bullet1_x + 20 and tank_y > bullet1_y:
                    client.turn_tank(client.token, RIGHT)
                elif tank_x >= bullet1_x - 20 and tank_x <= bullet1_x + 20 and tank_y > bullet1_y:
                    client.turn_tank(client.token, RIGHT)
                elif tank_y >= bullet1_y - 20 and tank_y <= bullet1_y + 20 and tank_x > bullet1_x:
                    client.turn_tank(client.token, UP)
                elif tank_y >= bullet1_y - 20 and tank_y <= bullet1_y + 20 and tank_x < bullet1_x:
                    client.turn_tank(client.token, UP)
            except:
                pass
            pygame.display.flip()
        client.connection.close()

    client = TankRpcClient()
    client.check_server_status()
    #rooms = ['room-1','room-2','room-3','room-4','room-5','room-6','room-7',
            #'room-8','room-9','room-10','room-11','room-12','room-13','room-14',
            #'room-15','room-16','room-17','room-18','room-19','room-20',
            #'room-21','room-22','room-23','room-24','room-25','room-26','room-27',
            #'room-28','room-29','room-30']
    #room = random.choice(rooms)
    #client.obtain_token(room)
    #event_client = TankConsumerClient(room)
    client.obtain_token('room-7')
    event_client = TankConsumerClient('room-7')

    event_client.start()
    game_start()
def exit():
    pygame.quit()

walls = [] 

map1 = [
" WWW   W     WW     WWW",
"    WWWW   WW     W   W",
"         WWWWWW   WW  W",
"   WWWW       W       W",
"   W        WWWW      W",
" WWW  WWWW        WW  W",
"   W     W W     W    W",
"   W     W   WWW    WWW",
"   WWW WWW   W W W   WW",
"     W   W   W W W    W",
"WW   W   WWWWW W      W",
" W      WW  WW     W  W",
" W   WWWW   WWW   WW  W",
"     W        W       W",
"    WW           W     ",
" WW    W   WWWW   WW   ",
"   WW  W      WWW     W",
]
map2 =[
"     W WW    WWW      W",
"WWW       W     w wwwwW",
"         WW           W",
"   WWWW       W       W",
"   W        WWWWWW    W",
" WWWWWWWWW            W",
"   WW      WWWW  WWW  W",
" W   W WW  WWWW     WWW",
"WW WWW   W   W W W   WW",
"     W   W   W W W    W",
"  WWW    WWW      WW   ",
"WW      WW  WW     W  W",
" W   WWWW   WWW   WW  W",
"W W  W      WWW       W",
"    WW      WWWWWW     ",
" WWW   W  W     WWWW   ",
"       W   WW WW     WW",
]
map3 =[
" WWW        WWW     WWW",
"   WWWWW   WW     W   W",
"   W  WW    WWW   WW  W",
"   WWWWW      W       W",
"   W        WWWW      W",
" WWW  WWWW        WW  W",
"   W WW   WWW    W    W",
"   WWW    W   WWW  WWWW",
"             W W W   WW",
"W W W W W W W W W W W W",
"WW   W   WWWWW W      W",
" W      WW  WW     W  W",
" W   WWWW   WWW   WW  W",
"     W        W       W",
"    WWWWWWW     WWW    ",
" WW    WWWW       WW   ",
"      W WW    WWWW    W",  
]
maps = [map1,map2,map3]
level = random.choice(maps)

x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        x += 35
    y += 35
    x = 0

menu()
pygame.quit()
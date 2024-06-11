import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *
#import main

pygame.init()
pygame.font.init()
messageFont = pygame.font.Font(pygame.font.get_default_font(), 60)
# From main.py
# variables to be used through the program
vec = pygame.math.Vector2
HEIGHT = 400
WIDTH = 732
ACC = 0.3
FRIC = -0.03
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
screen = pygame.display.set_mode((732, 400))

runGame = False


displaysurface = pygame.display.set_mode((732, 400))
pygame.display.set_caption("Star Catcher!")
#************************************************************************************************************
#creating classes
#background
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load()
        self.bgimage = pygame.transform.scale(self.bgimage, (732, 300))
        self.rectBGimg = self.bgimage.get_rect()
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))


#ground
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load()
        self.image = pygame.transform.scale(self.image, (732, 100))
        self.rect = self.image.get_rect(center=(0, 0))
        self.bgX1 = 0
        self.bgY1 = 300

    def render(self):
        displaysurface.blit(self.image, (self.bgX1, self.bgY1))


#sprite (skater cat)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load()
        self.image = pygame.transform.scale(self.image, (150, 100))
        self.rect = self.image.get_rect(center=(0, 0))

        # Position and direction
        self.vx = 0
        self.pos = vec((366, 306))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        #self.direction = "RIGHT"

        # Movement
        self.jumping = False
        self.running = False 
        self.move_frame = 0
        self.update = False

    def move(self):
        
        self.acc = vec(0, 0)

        # Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        # Accelerates the player in the direction of the key press
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 25 * self.acc  # Updates Position with new values

        # This causes character warping from one point of the screen to the other
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos  # Update rect with new pos

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False


class star1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Abhishek Kumar\Downloads\download (34).png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(366, 0))
        self.starscore = 0

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 0))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.y = 0
        self.x = 0

    def getScore(self):
        return self.starscore 

    def stmove(self):
        # Keep a constant acceleration of 0.5
        self.acc = vec(0, 5)

        # Will set running to False if the player has slowed down to a certain extent
        '''if abs(self.vel.x) > 0.3:
                self.running = True
          else:
                self.running = False'''

        # Formulas to calculate velocity while accounting for friction+
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel * 0 + self.acc # Updates Position with new values

        # This causes character warping from one point of the screen to the otherclass

        if self.pos.y > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

        #if if self.pos.y > 300:
        if pygame.sprite.spritecollide(player, star1_group, False):
            self.pos.x = random.randint(0, 700)
            self.pos.y = 0
            self.starscore += 1
            
 
background = Background()
ground = Ground()
player = Player()
star1 = star1()
star1_group = pygame.sprite.Group()
star1_group.add(star1)
stspeed = 5
ground_group = pygame.sprite.Group()
ground_group.add(ground)

class score():
  def _init_(self):
    self.score = 0
    self.score_font = pygame.font.SysFont(None, 25)

  def updateself(self):
    if pygame.sprite.spritecollide(player, star1_group, True):
      self.score += 1
    self.stscore = self.score_font.render(str(self.score), True, (255,255,255), (0,0,0))
  
  def drawself(self):
    displaysurface.blit(self.stscore, (30,30))
    
score = score()   
score._init_()   
score.updateself()
score.drawself()

#*************************************************************************************************************

welcomeMessage = " - Star Catcher! - "
thanksMessage = " - Game Over! -"

# Define the background colour
# using RGB color coding.
background_colour = (119, 98, 177)
background_color2 = (119, 98, 177)

#Screen Class

class ScreenDesc():
    def __init__(self, title, fill, width=732, height=400):
        self.title = title
        self.width = width
        self.height= height
        self.fill= fill
        self.current = False
        #self.screen = pygame.display.set_mode((width,height))

    def makeCurrent(self):
        pygame.display.set_caption(self.title)
        self.current = True
        self.screen = pygame.display.set_mode((732,400))
        #self.screen = pygame.display.set_mode((self.width,self.height))


    def endCurrent(self):
        self.current = False


    def checkUpdate(self):
        return self.current


    def screenUpdate(self):
        if(self.current):
            self.screen.fill(self.fill)


    def returnTitle(self):
        return self.screen


# Class button

class Button():
    def __init__(self, x, y, sx, sy, bcolor, fbcolor, font, fontsize, fcolor, text):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.bcolor = bcolor
        self.fbcolor = fbcolor
        self.font = font
        self.fontsize = fontsize
        self.fcolor = fcolor
        self.text = text
        self.current = False
        self.buttonf = pygame.font.SysFont(font,fontsize)
        


    def showButton(self, display):
        if(self.current):
            pygame.draw.rect(display, self.fbcolor, (self.x,self.y,self.sx,self.sy))

        else:
            pygame.draw.rect(display, self.bcolor,  (self.x,self.y,self.sx,self.sy) )

        textsurface = self.buttonf.render(self.text, False, self.fcolor)
        display.blit(textsurface,(self.x+self.sx/3,self.y+self.sy/3))
    
    def focusCheck(self, mousepos, mouseclick):
        if(mousepos[0] >= self.x and mousepos[0] <= self.x + self.sx and mousepos[1] >= self.y and mousepos[1] <= self.y+ self.sy):
            self.current = True
            return mouseclick[0]

        else:
            self.current = False
            return False

# Text blit for display text in screen
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

# Text render in screen
def drawText(screen, t, x, y, fg, alpha):
    text = messageFont.render(t, True, fg)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x,y)

    blit_alpha(screen, text, (x,y), alpha)


screen1 = ScreenDesc("Main Menu",background_colour)
screen2 = ScreenDesc("Thank You",background_color2)


win = screen1.makeCurrent()


# Update the display using flip
pygame.display.flip()
  
# Variable to keep our game loop running
running = True
toggle = False
testButton = Button(300,150,150,50,(167, 118, 187),(203, 113, 195), "calibri", 20,(255,255,255), "Start" )


# game loop
while running:
    screen1.screenUpdate()
    screen2.screenUpdate()
    
      
    mousepos = pygame.mouse.get_pos()
    mouseclick = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    
        
    #screen 1 page code
    if screen1.checkUpdate():
        drawText(screen1.screen, welcomeMessage, 110, 30, (255,227,187), 255)
        screen2button = testButton.focusCheck(mousepos,mouseclick)
        testButton.showButton(screen1.returnTitle())
        
        if screen2button:
            ##win = screen2.makeCurrent()
            screen1.endCurrent()
            runGame = True
    #**************************************************************************
            while runGame:
                background.render()
                ground.render()
                player.move()
                star1.stmove()

                displaysurface.blit(star1.image, star1.rect)
                displaysurface.blit(player.image, player.rect)
                pygame.display.update()
                pygame.display.flip()
                FPS_CLOCK.tick(20)

                if star1.pos.y > 300:
                    #########*****************
                    
                    screen2.makeCurrent()
                    drawText(screen2.screen, thanksMessage, 130, 40, (255,227,187), 255)
                    drawText(screen2.screen, "Stars collected: " + str(star1.getScore()), 90,150,(208,205,230), 255 )
                    pygame.display.update()
                    pygame.display.flip()
                    screen2.screenUpdate()
                   
                    ########************
                    break
                                    
                #print(str(star1.getScore()))
                for event in pygame.event.get():
                # Check for QUIT event      
                    if event.type == pygame.QUIT:
                        runGame = False
    #**************************************************************************
              
    #screen 2 page code
    elif screen2.checkUpdate():
        drawText(screen2.screen, thanksMessage, 130, 40, (255,227,1875), 60)
        drawText(screen2.screen, "Stars Collected: " + str(star1.getScore()), 90,150,(208,205,230), 255 )
        
     
    if screen2.checkUpdate():
        drawText(screen2.screen, thanksMessage, 130, 40, (255,227,187), 60)
        drawText(screen2.screen, "Stars Collected: " + str(star1.getScore()), 90,150,(208,205,230), 255 )
       
   
    pygame.display.update()
    
# for loop through the event queue  
    for event in pygame.event.get():
      
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False

    #pygame.display.update()

pygame.quit()
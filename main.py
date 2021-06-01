import pygame, os, sys,  queue, random
os.environ['SDL_AUDIODRIVER'] = 'dsp'
from pygame.locals import *
pygame.init()


WIDTH = 720
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
CLK = pygame.time.Clock()

green = (44, 219, 96)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
gold = (255,223,0)
speed  = 5
fps = 60
# bg = pygame.image.load("background.png")
# bg = pygame.transform.scale(bg, (720,480))
# screen.blit(bg,(0,0))
# pygame.display.flip()

class Snake:
  def __init__ (self,x,y):
    self.snakex = x
    self.snakey = y
    self.tail = queue.Queue()
    self.color = black
    self.points = 10
  
  def draw(self, screen,):
    circles = []
    while self.tail.qsize()>0:
      circles.append(self.tail.get())
    for circle in circles:
      self.tail.put(circle)
      pygame.draw.circle(screen,green,(circle[0],circle[1]),10,0)
    pygame.draw.circle(screen,green,(self.snakex,self.snakey),10,0)

    while self.tail.qsize()>self.points:
      self.tail.get()
  
  def move(self,moveto,screen):
    if moveto == "up":
      self.snakey = self.snakey-speed
      self.color = screen.get_at((self.snakex,self.snakey-10))
    if moveto == "down":
      self.snakey = self.snakey+speed
      self.color = screen.get_at((self.snakex,self.snakey+10))
    if moveto == "left":
      self.snakex = self.snakex-speed
      self.color = screen.get_at((self.snakex-10,self.snakey))
    if moveto == "right":
      self.snakex = self.snakex+speed
      self.color = screen.get_at((self.snakex+10,self.snakey))
    

    if self.snakey>(HEIGHT-50):
      self.snakey = HEIGHT-50
    if self.snakey<(50):
      self.snakey=50
    if self.snakex>(WIDTH-50):
      self.snakex = WIDTH-50
    if self.snakex<(50):
      self.snakex=50

    self.tail.put([self.snakex,self.snakey])
    
    return(self.color)
  
def drawGrid():
  for x in range(0,WIDTH,30):
    pygame.draw.line(screen, white, (x,0),(x,HEIGHT))
  for y in range(0,HEIGHT,30):
    pygame.draw.line(screen, white, (0,y),(WIDTH,y))

  pygame.draw.line(screen,red,(50,HEIGHT-50),(WIDTH-50,HEIGHT-50),10)
  pygame.draw.line(screen,red,(50,50),(WIDTH-50,50),10)
  pygame.draw.line(screen,red,(50,50),(50,HEIGHT-50),10)
  pygame.draw.line(screen,red,(WIDTH-50,50),(WIDTH-50,HEIGHT-50),10)

player1=Snake(75,75)
block= pygame.Rect(60,60,40,40)
moving = "down"
runGame = True
wordFont = pygame.font.Font('freesansbold.ttf',50)
word = wordFont.render(str(player1.points),True,white)
while runGame:
  for event in pygame.event.get():
    if event==pygame.QUIT:
      runGame = False
  position = pygame.mouse.get_pos()
  if pygame.key.get_pressed()[pygame.K_UP]:
    moving =  "up"
  if pygame.key.get_pressed()[pygame.K_DOWN]:
    moving =  "down"
  if pygame.key.get_pressed()[pygame.K_LEFT]:
    moving =  "left"
  if pygame.key.get_pressed()[pygame.K_RIGHT]:
    moving =  "right"

  player1.move(moving,screen)
  if player1.color==red:
    runGame=False
  
  if block.collidepoint(player1.snakex,player1.snakey):
    player1.points = player1.points + 10
    word = wordFont.render(str(player1.points),True,white)
    block.x = random.randint(50,WIDTH-50)
    block.y = random.randint(50,HEIGHT-50)
  screen.fill(black)
  drawGrid()
  pygame.draw.rect(screen,gold,block)
  player1.draw(screen)
  screen.blit(word,(0,0))

  pygame.display.flip()
  CLK.tick(fps)

word = wordFont.render(str(player1.points) + " Game Over",True,white)
screen.blit(word,(0,0))
pygame.display.flip()
CLK.tick(fps)

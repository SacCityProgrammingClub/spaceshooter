import pygame
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision")

#create main rectangle & obstacle rectangle
rect_1 = pygame.Rect(0, 0, 25, 25)
obstacle_rect = pygame.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)

#define colours
BG = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.mixer.init()
background_music = pygame.mixer.music.load("assets/cafe.mp3")
boop_sound = pygame.mixer.Sound("assets/643139__joelleohworld__boop.wav")
#hide mouse cursor
pygame.mouse.set_visible(False)

#play background music
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

run = True
while run:


  #update background
  screen.fill(BG)

  #check collision and change colour
  col = GREEN
  if rect_1.colliderect(obstacle_rect):
    # Include explosion
    pygame.mixer.Sound.play(boop_sound)
    col = RED

  #get mouse coordinates and use them to position the rectangle
  pos = pygame.mouse.get_pos()
  rect_1.center = pos

  #draw both rectangles
  pygame.draw.rect(screen, col, rect_1)
  pygame.draw.rect(screen, BLUE, obstacle_rect)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
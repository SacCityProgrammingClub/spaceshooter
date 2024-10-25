# Simple Games

Go to collision.py for simple collision logic and sound effects.

This should be self-explanitory
use the colliderect(obj) to detect collision between rectangles

More info of Rect in [PyGame Docs](https://www.pygame.org/docs/ref/rect.html)

```python
if rect_1.colliderect(obstacle_rect):
    ''' do some cool logic '''
    pass
```

How we did it is we change the color of the object when collide and played some cool music

Initialize the sounds when collide
```python
boop_sound = pygame.mixer.Sound("assets/643139__joelleohworld__boop.wav")
```

Within the game loop
```python
while run:


  #update background
  screen.fill(BG)

  #check collision and change colour
  col = GREEN
  if rect_1.colliderect(obstacle_rect):
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

```

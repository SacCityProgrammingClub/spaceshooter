import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10

# Enemy
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_speed = 5
enemy_list = [enemy_pos]

# Bullet
bullet_size = 5
bullet_speed = 15
bullet_list = []

# Game variables
score = 0
font = pygame.font.SysFont("monospace", 35)

# Helper functions
def drop_enemies(enemy_list):
    if len(enemy_list) < 10:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list):
    global score
    for enemy_pos in enemy_list:
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.remove(enemy_pos)
            score += 1

def fire_bullet():
    bullet_list.append([player_pos[0] + player_size//2 - bullet_size//2, player_pos[1]])

def update_bullet_positions():
    for bullet in bullet_list:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullet_list.remove(bullet)

def check_bullet_hits():
    global score
    for bullet in bullet_list:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)
        for enemy in enemy_list:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
            if bullet_rect.colliderect(enemy_rect):
                bullet_list.remove(bullet)
                enemy_list.remove(enemy)
                score += 1
                return

# Game loop
game_over = False
clock = pygame.time.Clock()

while not game_over:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_bullet()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    # Update enemy positions and drop new enemies
    drop_enemies(enemy_list)
    update_enemy_positions(enemy_list)
    update_bullet_positions()
    check_bullet_hits()

    # Draw player
    pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))

    # Draw enemies
    draw_enemies(enemy_list)

    # Draw bullets
    for bullet in bullet_list:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_size, bullet_size))

    # Display score
    score_text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Collision detection with player and enemies
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for enemy_pos in enemy_list:
        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            game_over = True
            break

    pygame.display.update()
    clock.tick(30)

pygame.quit()

import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (147, 0, 211)

# Create stars for background
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.randint(1, 3)
        self.size = random.randint(1, 3)
        self.color = random.choice([(255, 255, 255), (200, 200, 255), (255, 200, 200)])

stars = [Star() for _ in range(100)]

# Player
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10
player_shape = [
    (0, player_size),
    (player_size//2, 0),
    (player_size, player_size)
]

# Enemy
enemy_size = 40
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_speed = 5
enemy_list = [enemy_pos]

# Bullet
bullet_size = 5
bullet_speed = 15
bullet_list = []

# Explosion particles
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)
        self.lifetime = random.randint(10, 20)
        self.color = random.choice([RED, (255, 165, 0), (255, 255, 0)])
        self.size = random.randint(2, 4)

explosions = []

# Powerups
class Powerup:
    def __init__(self):
        self.size = 20
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.type = random.choice(['speed', 'shield'])
        self.color = BLUE if self.type == 'speed' else PURPLE
        self.active = False
        self.duration = 300  # frames

powerups = []
player_powerups = {'speed': 0, 'shield': 0}

# Game variables
score = 0
font = pygame.font.Font(None, 36)
game_over = False

def create_powerup():
    if random.random() < 0.01:  # 1% chance each frame
        powerups.append(Powerup())

def update_powerups():
    global player_speed
    for powerup in powerups[:]:
        powerup.y += 2
        if powerup.y > HEIGHT:
            powerups.remove(powerup)
        
        # Check collision with player
        if (player_pos[0] < powerup.x + powerup.size and 
            player_pos[0] + player_size > powerup.x and 
            player_pos[1] < powerup.y + powerup.size and 
            player_pos[1] + player_size > powerup.y):
            
            player_powerups[powerup.type] = powerup.duration
            powerups.remove(powerup)

    # Update active powerup durations
    for power_type in player_powerups:
        if player_powerups[power_type] > 0:
            player_powerups[power_type] -= 1

def draw_powerups():
    for powerup in powerups:
        pygame.draw.rect(screen, powerup.color, 
                        (powerup.x, powerup.y, powerup.size, powerup.size))

def create_explosion(x, y):
    particles = [Particle(x, y) for _ in range(20)]
    explosions.append(particles)

def update_explosions():
    for explosion in explosions[:]:
        for particle in explosion[:]:
            particle.x += particle.dx
            particle.y += particle.dy
            particle.lifetime -= 1
            if particle.lifetime <= 0:
                explosion.remove(particle)
        if not explosion:
            explosions.remove(explosion)

def draw_explosions():
    for explosion in explosions:
        for particle in explosion:
            pygame.draw.circle(screen, particle.color, 
                             (int(particle.x), int(particle.y)), 
                             particle.size)

def update_stars():
    for star in stars:
        star.y += star.speed
        if star.y > HEIGHT:
            star.y = 0
            star.x = random.randint(0, WIDTH)

def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, star.color, (star.x, int(star.y)), star.size)

def draw_player():
    # Draw shield if active
    if player_powerups['shield'] > 0:
        pygame.draw.circle(screen, PURPLE, 
                         (int(player_pos[0] + player_size//2), 
                          int(player_pos[1] + player_size//2)), 
                         player_size, 2)
    
    # Draw player triangle
    points = [(player_pos[0] + x, player_pos[1] + y) for x, y in player_shape]
    pygame.draw.polygon(screen, GREEN, points)
    
    # Draw engine flame
    flame_points = [
        (player_pos[0] + player_size//2, player_pos[1] + player_size),
        (player_pos[0] + player_size//3, player_pos[1] + player_size + 10),
        (player_pos[0] + 2*player_size//3, player_pos[1] + player_size + 10),
    ]
    pygame.draw.polygon(screen, (255, 165, 0), flame_points)

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        # Draw enemy spaceship
        points = [
            (enemy_pos[0] + enemy_size//2, enemy_pos[1]),
            (enemy_pos[0], enemy_pos[1] + enemy_size),
            (enemy_pos[0] + enemy_size, enemy_pos[1] + enemy_size)
        ]
        pygame.draw.polygon(screen, RED, points)

def fire_bullet():
    bullet_list.append([
        player_pos[0] + player_size//2 - bullet_size//2,
        player_pos[1]
    ])

# Game loop
clock = pygame.time.Clock()

while not game_over:
    screen.fill(BLACK)
    
    # Draw and update stars
    update_stars()
    draw_stars()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_bullet()
                
    # Movement with speed powerup
    current_speed = player_speed * 2 if player_powerups['speed'] > 0 else player_speed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= current_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += current_speed

    # Update game elements
    if len(enemy_list) < 10:
        enemy_list.append([random.randint(0, WIDTH - enemy_size), -enemy_size])

    # Update enemy positions
    for enemy_pos in enemy_list[:]:
        enemy_pos[1] += enemy_speed
        if enemy_pos[1] > HEIGHT:
            enemy_list.remove(enemy_pos)
            score += 1

    # Update bullets and check collisions
    for bullet in bullet_list[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullet_list.remove(bullet)
        else:
            for enemy_pos in enemy_list[:]:
                if (bullet[0] < enemy_pos[0] + enemy_size and
                    bullet[0] + bullet_size > enemy_pos[0] and
                    bullet[1] < enemy_pos[1] + enemy_size and
                    bullet[1] + bullet_size > enemy_pos[1]):
                    create_explosion(enemy_pos[0] + enemy_size//2, enemy_pos[1] + enemy_size//2)
                    if bullet in bullet_list:
                        bullet_list.remove(bullet)
                    enemy_list.remove(enemy_pos)
                    score += 1

    # Check for collisions with player
    for enemy_pos in enemy_list:
        if (player_pos[0] < enemy_pos[0] + enemy_size and
            player_pos[0] + player_size > enemy_pos[0] and
            player_pos[1] < enemy_pos[1] + enemy_size and
            player_pos[1] + player_size > enemy_pos[1]):
            if player_powerups['shield'] <= 0:
                game_over = True
            else:
                enemy_list.remove(enemy_pos)
                create_explosion(enemy_pos[0] + enemy_size//2, enemy_pos[1] + enemy_size//2)

    # Create and update powerups
    create_powerup()
    update_powerups()

    # Draw game elements
    draw_player()
    draw_enemies(enemy_list)
    
    # Draw bullets
    for bullet in bullet_list:
        pygame.draw.rect(screen, (0, 255, 255), 
                        (bullet[0], bullet[1], bullet_size, bullet_size))
    
    draw_powerups()
    update_explosions()
    draw_explosions()

    # Draw HUD
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw powerup indicators
    if player_powerups['speed'] > 0:
        speed_text = font.render("SPEED", True, BLUE)
        screen.blit(speed_text, (WIDTH - 100, 10))
    if player_powerups['shield'] > 0:
        shield_text = font.render("SHIELD", True, PURPLE)
        screen.blit(shield_text, (WIDTH - 100, 40))

    pygame.display.update()
    clock.tick(60)

# Game over screen
screen.fill(BLACK)
game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
restart_text = font.render("Press R to Restart", True, WHITE)
text_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
restart_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
screen.blit(game_over_text, text_rect)
screen.blit(restart_text, restart_rect)
pygame.display.update()

# Wait for restart
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                waiting = False
                exec(open(__file__).read())

pygame.quit()
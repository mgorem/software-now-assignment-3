import pygame

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Side-Scroller Game")

# Set the frame rate
clock = pygame.time.Clock()

# Font for text display
font = pygame.font.Font(None, 36)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))  # Player size
        self.image.fill((0, 255, 0))  # Player color
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 50, SCREEN_HEIGHT - 100  # Start position
        self.speed = 5
        self.jump_strength = 15
        self.velocity_y = 0
        self.gravity = 0.8
        self.lives = 3
        self.health = 100
        self.score = 0  # Initialize score

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.velocity_y = -self.jump_strength

        # Gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Prevent falling through the ground
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery)
        projectiles.add(projectile)

    def update(self):
        self.move()

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))  # Projectile color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 8

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:  # Remove if off-screen
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0))  # Enemy color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed  # Move left
        if self.rect.x < -50:  # Remove when off-screen
            self.kill()

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, boost_type):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        if boost_type == 'health':
            self.image.fill((0, 255, 255))
        elif boost_type == 'life':
            self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass  # Add logic for collectibles if needed

# Drawing the score on the screen
def draw_score():
    score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))  # White text
    screen.blit(score_text, (10, 10))  # Top-left corner

# Drawing the player's health bar on the screen
def draw_health():
    pygame.draw.rect(screen, (255, 0, 0), (10, 50, 100, 20))  # Red background bar
    pygame.draw.rect(screen, (0, 255, 0), (10, 50, player.health, 20))  # Green health bar

# Drawing the number of lives on the screen
def draw_lives():
    lives_text = font.render(f'Lives: {player.lives}', True, (255, 255, 255))
    screen.blit(lives_text, (10, 80))  # Display below the health bar

# Load a specific level with enemies and collectibles
def load_level(level):
    all_sprites.empty()
    enemies.empty()
    collectibles.empty()

    all_sprites.add(player)

    if level == 1:
        for i in range(3):
            enemy = Enemy(700 + i * 150, SCREEN_HEIGHT - 100)
            all_sprites.add(enemy)
            enemies.add(enemy)

        collectible = Collectible(500, SCREEN_HEIGHT - 100, 'health')
        all_sprites.add(collectible)
        collectibles.add(collectible)
    
    elif level == 2:
        for i in range(5):
            enemy = Enemy(700 + i * 150, SCREEN_HEIGHT - 100)
            all_sprites.add(enemy)
            enemies.add(enemy)

        collectible = Collectible(600, SCREEN_HEIGHT - 100, 'life')
        all_sprites.add(collectible)
        collectibles.add(collectible)

    elif level == 3:
        for i in range(6):
            enemy = Enemy(700 + i * 150, SCREEN_HEIGHT - 100)
            all_sprites.add(enemy)
            enemies.add(enemy)

        boss = Enemy(1000, SCREEN_HEIGHT - 100)  # Boss enemy
        boss.image = pygame.Surface((60, 80))
        boss.image.fill((255, 165, 0))  # Boss color
        all_sprites.add(boss)
        enemies.add(boss)

# Check if a level is completed (no enemies left)
def check_level_completion():
    if len(enemies) == 0:
        global level
        level += 1
        if level <= 3:
            load_level(level)
        else:
            print("You won the game!")
            pygame.quit()

# Show the Game Over screen
def game_over():
    game_over_text = font.render('GAME OVER. Press R to Restart', True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH//4, SCREEN_HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Pause for 2 seconds

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return True  # Restart game

# Player hit logic (reduce health and lives)
def player_hit():
    player.health -= 20
    if player.health <= 0:
        player.lives -= 1
        player.health = 100

# Sprite groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Load the first level
level = 1
load_level(level)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Press 'F' to shoot
                player.shoot()

    # Update all sprites
    all_sprites.update()

    # Check for collisions between player and collectibles
    collected_items = pygame.sprite.spritecollide(player, collectibles, True)
    for item in collected_items:
        player.score += 10  # Increase score

    # Check for collisions between projectiles and enemies
    hits = pygame.sprite.groupcollide(enemies, projectiles, True, True)
    for hit in hits:
        player.score += 20  # Increase score

    # Check for player-enemy collision
    if pygame.sprite.spritecollideany(player, enemies):
        player_hit()

    # Check if all enemies are defeated to load the next level
    check_level_completion()

    # Clear the screen
    screen.fill((0, 0, 0))  # Black background

    # Draw everything
    all_sprites.draw(screen)
    draw_score()
    draw_health()
    draw_lives()

    # Check if game over (no lives left)
    if player.lives <= 0:
        if game_over():
            player.lives = 3
            player.health = 100
            player.score = 0
            level = 1
            load_level(level)
        else:
            running = False

    # Refresh the display
    pygame.display.flip()
    clock.tick(60)  # 60 frames per second

# Quit Pygame
pygame.quit()

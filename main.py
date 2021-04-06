import pygame
import random
from os import path

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), 'images')

score = 0

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

font_name = pygame.font.match_font('arial')
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_hb(surface, x, y, percent):
    if percent < 0:
        percent = 0
    BAR_L = 100
    BAR_H = 10
    fill = (percent/100) * BAR_L
    outline_rect = pygame.Rect(x, y, BAR_L, BAR_H)
    fill_rect = pygame.Rect(x, y, fill, BAR_H)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)
    pygame.draw.rect(surface, GREEN, fill_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 22
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speedx = 0
        self.health = 100
    
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_LEFT]:
            self.speedx = -8

        self.rect.x += self.speedx

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 17
        self.rect.y = random.randrange(-100, -20)
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -20)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy

class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self):
        self.type = random.choice(['sheild', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update():
        self.rect.y += self.speedy

background = pygame.image.load(path.join(img_dir, 'spacepython.jpg')).convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, 'shooter.png')).convert()
player_img = pygame.transform.scale(player_img, (60,50))

enemy_img = pygame.image.load(path.join(img_dir, 'spaceinvaders.png')).convert()
enemy_img = pygame.transform.scale(enemy_img, (30, 30))

bullet_img = pygame.image.load(path.join(img_dir, 'laserRed08.png')).convert()
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

running = True

p1 = Player()
all_sprites.add(p1)

for i in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

while running == True:
    # loop runs at 30 FPS
    clock.tick(FPS)

    # processing input events
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                p1.shoot()

    # Update Section
    all_sprites.update()
    
    hits = pygame.sprite.spritecollide(p1, enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        p1.health -= 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        if p1.health <= 0:
            running = False
    
    bullet_hit = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in bullet_hit:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        score += 10

    # Draw Section
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 20, SCREEN_WIDTH/2, 10)
    draw_hb(screen, 5, 5, p1.health)

    # *AFTER* drawing everything, we flip the display
    pygame.display.flip()

pygame.quit()
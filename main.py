import pygame
import random
from os import path
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 400
FPS = 60

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

POWERUP_TIME = 5000


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
img_dir = path.join(path.dirname(__file__), 'images')
score = 0
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

font_name = pygame.font.match_font('arial')
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

def draw_hb(surface, x, y, percent):
    if percent < 0:
        percent = 0
    BAR_L = 100
    BAR_W = 10
    fill = (percent/100) * BAR_L
    outline_rect = pygame.Rect(x, y, BAR_L, BAR_W)
    fill_rect = pygame.Rect(x, y, fill, BAR_W)
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
            self.rect.bottom = SCREEN_HEIGHT-10
            self.speedx = 0  
            self.health = 100
            self.power = 1
            self.power_time = pygame.time.get_ticks()
            self.last_shot = pygame.time.get_ticks()
            self.shot_delay = 250

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx=8
        if keystate[pygame.K_LEFT]:
           self.speedx = -8

        self.rect.x += self.speedx

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
            if self.power >= 3:
    
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
    

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)   
        self.image = enemies_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 17
        self.rect.y = random.randrange(-100,-20)
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > SCREEN_HEIGHT or self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -20)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3,3)    




class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite   .__init__(self)
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
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, "shield_gold.png")).convert() 
powerup_images['gun'] = pygame.image.load(path.join(img_dir, "bolt_gold.png")).convert() 


backround = pygame.image.load(path.join(img_dir, 'spacepython.jpg')).convert()
backround = pygame.transform.scale(backround, (SCREEN_WIDTH, SCREEN_HEIGHT))
backround_rect = backround.get_rect()

player_img = pygame.image.load(path.join(img_dir, 'shooter.png')).convert()
player_img = pygame.transform.scale(player_img, (60,50))

enemies_img = pygame.image.load(path.join(img_dir, 'spaceinvaders.png')).convert()
enemies_img = pygame.transform.scale(enemies_img, (30,30))  

bullet_img = pygame.image.load(path.join(img_dir, 'laserRed08.png')).convert()
bullet_img = pygame.transform.scale(bullet_img, (10, 20))



        
running = True

p1 = Player()
all_sprites.add(p1)

for i in range(5):
    enemy=Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)
 

while running == True:
    clock.tick(FPS)
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                p1.shoot()
    all_sprites.update()

    hits = pygame.sprite.spritecollide(p1, enemies, True, pygame.sprite.collide_circle)
    for hits in hits: 
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
        score+=10
        if random.random() > 0.8:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)

    powerhit = pygame.sprite.spritecollide(p1, powerups, True, pygame.sprite.collide_circle)
    for hit in powerhit:
        if hit.type == 'shield':
            p1.health += random.randrange(10, 30)
            if p1.health >= 100:
                p1.health = 100
        if hit.type == 'gun':
            p1.powerup()

    screen.fill(BLACK)
    screen.blit(backround, backround_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 20, SCREEN_WIDTH/2, 10)
    draw_hb(screen, 5, 5, p1.health)
    pygame.display.flip()

pygame.quit()

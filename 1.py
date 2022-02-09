import pygame
import random
import os
# 初始化
pygame.init()
pygame.mixer.init()
WIDTH = 600
HEIGHT = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('harper的第一个游戏')

FPS = 60
BLACK = (0, 0, 0)
clock = pygame.time.Clock()
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
# 载入图片
back = pygame.image.load(os.path.join('image', '1.jpg')).convert()
rock_img = pygame.image.load(os.path.join('image', '2.png')).convert()
player_img = pygame.image.load(os.path.join('image', 'gang.png')).convert()
player_live_image = pygame.transform.scale(player_img, (60, 80))
pygame.display.set_icon(player_img)
player_live_image.set_colorkey(BLACK)
score = 0
font_name = os.path.join('msyh.ttc')
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
for i in range(10):
    expl_img = pygame.image.load(os.path.join('image', f'b{i}.png')).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
power_imgs = {}
power_img1 = pygame.image.load(os.path.join('image', 'live.jpg')).convert()
power_img2 = pygame.image.load(os.path.join('image', 'live1.jpg')).convert()
power_img1.set_colorkey(WHITE)
power_img2.set_colorkey(WHITE)
power_imgs['live'] = pygame.transform.scale(power_img1, (45, 45))
power_imgs['live1'] = pygame.transform.scale(power_img2, (45, 45))
# 载入音乐
shoot_sound = pygame.mixer.Sound(os.path.join('sounds', 'sheji.wav'))
boom_sound = pygame.mixer.Sound(os.path.join('sounds', 'baozha.wav'))
pygame.mixer.music.load(os.path.join('sounds', 'back.flac'))
pygame.mixer.music.set_volume(0.9)
shield_sound = pygame.mixer.Sound(os.path.join('sounds', 'shied.wav'))
up_sound = pygame.mixer.Sound(os.path.join('sounds', 'up.wav'))


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    lenght = 150
    height = 15
    fill = (hp / 100) * lenght
    outline_rect = pygame.Rect(x, y, lenght, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 60 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_init():
    screen.blit(back, (0, 0))
    draw_text(screen, '阿刚保卫战', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, '←  → 移动 空格射击', 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, '按任意键开始游戏', 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (120, 150))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.radius = 50
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 160
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        if self.gun > 1 and pygame.time.get_ticks() - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        key_predded = pygame.key.get_pressed()
        if key_predded[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_predded[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_predded[pygame.K_UP]:
            self.rect.x += self.speedx
        if key_predded[pygame.K_DOWN]:
            self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not (self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.x, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 500)

    def Gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()


class Rock(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = pygame.transform.scale(rock_img, (60, 70))
        self.image = self.image_ori.copy()
        self.image_ori.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 8)
        self.speedx = random.randrange(-3, 3)
        self.totao_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.totao_degree += self.rot_degree
        self.totao_degree = self.totao_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.totao_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 8)
            self.speedx = random.randrange(-3, 3)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):

    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


class Power(pygame.sprite.Sprite):

    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['live', 'live1'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)


pygame.mixer.music.play(-1)
# 游戏循环
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        score = 0
        rock = Rock()
        for i in range(8):
            new_rock()
    clock.tick(FPS)
    # 输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # 更新
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        boom_sound.play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)

        new_rock()
    hits = pygame.sprite.spritecollide(player, rocks, True,
                                       pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            player.hide()

    # 判断buff
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'live1':
            player.health += 50
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        elif hit.type == 'live':
            player.Gunup()
            up_sound.play()
    if player.lives == 0:
        show_init = True
    # 显示
    screen.fill(BLACK)
    screen.blit(back, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health(screen, player.health, 10, 20)
    draw_lives(screen, player.lives, player_live_image, WIDTH - 180, 15)
    pygame.display.update()
pygame.quit()

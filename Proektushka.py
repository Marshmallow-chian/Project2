import pygame
import os
import random
from os import path


RED = (255, 0, 0)
GRAVITI = 0.00000000000000001



class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 3 - HEIGHT // 1.4)


camera = Camera()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    intro_text = ["                       GALACTIC SHOOTRER", " ",
                  " ",
                  " ",
                  " ",
                  " ",
                  " ",
                  "                      Нажмите что-бы начать"]

    fon = pygame.transform.scale(load_image('space_planet_stars.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("rockets.png", BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()



class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("asteroid.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.x = pos_x
        self.y = pos_y
        self.shield = 100
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self, *args):
        if args:
            if args[0].type == pygame.MOUSEBUTTONDOWN:
                if args[0].button == 1:
                    player.shoot()
            if args[0].type == pygame.KEYDOWN:

                if pygame.key.get_pressed()[pygame.K_w]:
                    self.rect.y -= 25
                    if pygame.sprite.spritecollideany(self, wall_group):
                        self.rect.y += 25
                if pygame.key.get_pressed()[pygame.K_s]:
                    self.rect.y += 100
                    if pygame.sprite.spritecollideany(self, wall_group):
                        self.rect.y -= 100
                if pygame.key.get_pressed()[pygame.K_a]:
                    self.rect.x -= 25
                    if pygame.sprite.spritecollideany(self, wall_group):
                        self.rect.x += 25
                if pygame.key.get_pressed()[pygame.K_d]:
                    self.rect.x += 25
                    if pygame.sprite.spritecollideany(self, wall_group):
                        self.rect.x -= 25
                if pygame.sprite.spritecollideany(self, wall_group):
                    create_particles((self.rect.centerx, self.rect.centery))
        self.rect

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

    def update1(self):
        self.rect.y -= 1 / FPS
        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect.y += 1
            create_particles((self.rect.centerx, self.rect.centery))
        self.rect

def newmob():
    m = Mob()
    all_sprites.add(m)
    wall_group.add(m)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
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
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


pygame.init()
size = WIDTH, HEIGHT = 500, 600
screen_rect = (0, 0, WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)


class Particle(pygame.sprite.Sprite):
    fire = [load_image('laser.png', -1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        # Рё СЃРІРѕРё РєРѕРѕСЂРґРёРЅР°С‚С‹
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITI

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


size = WIDTH, HEIGHT = 500, 600
screen_rect = (0, 0, WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
tile_images = {'wall': load_image('asteroid.png', -1), 'empty': load_image('sputnik.png', -1)}
player_image = load_image('spaceship.png', -1)
tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = Player(WIDTH / 2, HEIGHT)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
bullets = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    wall_group.add(m)
shoot_sound = pygame.mixer.Sound(path.join('data/rocket.wav'))
shoot_sound1 = pygame.mixer.Sound(path.join('data/pew.wav'))
pygame.mixer.music.load(path.join('data/for_game.mp3'))
pygame.mixer.music.set_volume(0.6)
FPS = 60
start_screen()
running = True
game_over = False
pause = False

pygame.mixer.music.play(loops=-1)

while running:
    if not pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    player.shoot()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
            player.update(event)
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, wall_group, True, pygame.sprite.collide_circle)
            if hits:
                for hit in hits:
                    pass
                    newmob()
                    expl = Explosion(hit.rect.center, 'lg')
                    all_sprites.add(expl)
                bullet.kill()
                newmob()

        player.update1()
        hits = pygame.sprite.spritecollide(player, wall_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius * 2
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                game_over = True
        explosion_anim = {}
        explosion_anim['lg'] = []
        explosion_anim['sm'] = []
        explosion_anim['player'] = []
        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join('data/' + filename)).convert()
            img.set_colorkey(BLACK)
            img_lg = pygame.transform.scale(img, (75, 75))
            explosion_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            explosion_anim['sm'].append(img_sm)
            filename = 'sonicExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join('data/' + filename)).convert()
            img.set_colorkey(BLACK)
            explosion_anim['player'].append(img)
        if game_over:
            game_over = False
            size = WIDTH, HEIGHT = 500, 600
            screen_rect = (0, 0, WIDTH, HEIGHT)
            screen = pygame.display.set_mode(size)
            tile_images = {'wall': load_image('asteroid.png', -1),
                           'empty': load_image('sputnik.png', -1)}
            player_image = load_image('spaceship.png', -1)
            tile_width = tile_height = 50
            all_sprites = pygame.sprite.Group()
            tiles_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            player = Player(WIDTH / 2, HEIGHT)
            BLACK = (0, 0, 0)

            clock = pygame.time.Clock()
            bullets = pygame.sprite.Group()
            wall_group = pygame.sprite.Group()
            for i in range(8):
                m = Mob()
                all_sprites.add(m)
                wall_group.add(m)
            shoot_sound = pygame.mixer.Sound(path.join('data/rocket.wav'))
            shoot_sound1 = pygame.mixer.Sound(path.join('data/pew.wav'))
            pygame.mixer.music.load(path.join('data/for_game_2.mp3'))
            pygame.mixer.music.set_volume(0.6)
            FPS = 60
            start_screen()
            running = True
            game_over = False
            pause = False

            pygame.mixer.music.play(loops=-1)

            while running:
                if not pause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 3:
                                player.shoot()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pause = True
                        player.update(event)
                    if player.shield <= 0:
                        death_explosion = Explosion(player.rect.center, 'player')
                        all_sprites.add(death_explosion)
                    hits = pygame.sprite.groupcollide(wall_group, bullets, True, True)
                    for bullet in bullets:
                        hits = pygame.sprite.spritecollide(bullet, wall_group, True, pygame.sprite.collide_circle)
                        if hits:
                            for hit in hits:
                                newmob()
                            expl = Explosion(hit.rect.center, 'lg')
                            all_sprites.add(expl)
                            bullet.kill()
                            newmob()
                    player.update1()
                    hits = pygame.sprite.spritecollide(player, wall_group, True,
                                                       pygame.sprite.collide_circle)
                    for hit in hits:
                        player.shield -= hit.radius * 2
                        expl = Explosion(hit.rect.center, 'sm')
                        all_sprites.add(expl)
                        newmob()
                        if player.shield <= 0:
                            death_explosion = Explosion(player.rect.center, 'player')
                            all_sprites.add(death_explosion)
                            game_over = True
                    explosion_anim = {}
                    explosion_anim['lg'] = []
                    explosion_anim['sm'] = []
                    explosion_anim['player'] = []
                    for i in range(9):
                        filename = 'regularExplosion0{}.png'.format(i)
                        img = pygame.image.load(path.join('data/' + filename)).convert()
                        img.set_colorkey(BLACK)
                        img_lg = pygame.transform.scale(img, (75, 75))
                        explosion_anim['lg'].append(img_lg)
                        img_sm = pygame.transform.scale(img, (32, 32))
                        explosion_anim['sm'].append(img_sm)
                        filename = 'sonicExplosion0{}.png'.format(i)
                        img = pygame.image.load(path.join('data/' + filename)).convert()
                        img.set_colorkey(BLACK)
                        explosion_anim['player'].append(img)
                    if game_over:
                        game_over = True
                        break
                    camera.update(player)
                    for sprite in all_sprites:
                        camera.apply(sprite)
                    screen.fill((0, 0, 0))
                    all_sprites.draw(screen)
                    all_sprites.update()
                    hits = pygame.sprite.groupcollide(wall_group, bullets, True, True)
                    player_group.draw(screen)
                    clock.tick(FPS)
                    pygame.display.flip()
                elif pause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pause = False
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill((0, 0, 0))

        all_sprites.draw(screen)
        all_sprites.update()
        hits = pygame.sprite.groupcollide(wall_group, bullets, True, True)
        player_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    elif pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False

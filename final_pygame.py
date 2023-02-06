import os
import pygame
import sys
import sqlite3

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)

con = sqlite3.connect('pygame.db')
cur = con.cursor()
numb_level = input('Введите уровень сложности:')


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        hp, dmg = None, None
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        if event.key == pygame.K_RIGHT:
            hero.rect.x += 50
        elif event.key == pygame.K_LEFT:
            hero.rect.x -= 50
        elif event.key == pygame.K_UP:
            hero.rect.y -= 50
        elif event.key == pygame.K_DOWN:
            hero.rect.y += 50
        #  self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                              # tile_height * self.pos[1] + 5)
        # camera.dx -= tile_width * (x - self.pos[0])
        # camera.dy -= tile_height * (y - self.pos[1])
        # for sprite in tiles_group:
        #     camera.apply(sprite)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x1, pos_y1):
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(tile_width * pos_x1 + 15, tile_height * pos_y1 + 5)
        hp, dmg = None, None
        self.pos = (pos_x1, pos_y1)

    def move(self, x1, y1):
        self.pos = (x1, y1)
        #  self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
        #                                         tile_height * self.pos[1] + 5)
        if event.key == pygame.K_RIGHT:
            enemy.rect.x -= 50
        elif event.key == pygame.K_LEFT:
            enemy.rect.x += 50
        elif event.key == pygame.K_UP:
            enemy.rect.y -= 50
        elif event.key == pygame.K_DOWN:
            enemy.rect.y += 50


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 10))
        self.image.fill('YELLOW')
        self.rect = self.image.get_rect()
        self.rect.bottom = x
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.x += self.speedy
        if self.rect.bottom < max_y:
            self.kill()

def load_level(filename):
    filename = "datapygame/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('datapygame', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('hero.png')
enemy_image = load_image('enemy.jpg')

tile_width = tile_height = 50


def generate_level(level):
    new_enemy, new_player, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'e':
                Tile('empty', x, y)
                new_enemy = Enemy(x, y)
        # вернем игрока, а также размер поля в клетках
    return new_enemy, new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and (level_map[y - 1][x] == '.' or level_map[y - 1][x] == '@' or
                      level_map[y - 1][x] == 'e'):
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < max_y - 1 and (level_map[y + 1][x] == '.' or level_map[y + 1][x] == '@' or
                              level_map[y + 1][x] == 'e'):
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and (level_map[y][x - 1] == '.' or level_map[y][x - 1] == '@' or
                      level_map[y][x - 1] == 'e'):
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < max_x and (level_map[y][x + 1] == '.' or level_map[y][x + 1] == '@' or
                          level_map[y][x + 1] == 'e'):
            hero.move(x + 1, y)


def move1(enemy, movement):
    x1, y1 = enemy.pos
    if movement == 'up':
        if y1 > 0 and (level_map[y1 - 1][x1] == '.' or level_map[y1 - 1][x1] == '@'):
            enemy.move(x1, y1 - 1)
    elif movement == 'down':
        if y1 < max_y - 1 and (level_map[y1 + 1][x1] == '.' or level_map[y1 + 1][x1] == '@'):
            enemy.move(x1, y1 + 1)
    elif movement == 'left':
        if x1 > 0 and (level_map[y1][x1 - 1] == '.' or level_map[y1][x1 - 1] == '@'):
            enemy.move(x1 - 1, y1)
    elif movement == 'right':
        if x1 < max_x and (level_map[y1][x1 + 1] == '.' or level_map[y1][x1 + 1] == '@'):
            enemy.move(x1 + 1, y1)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()

all_sprites.update()

# Проверка, не ударил ли моб игрока
hits = pygame.sprite.groupcollide(enemy_group, bullets, True, True)

FPS = 50


def terminate():
    pygame.quit()
    sys.exit()

clock = pygame.time.Clock()


def error_screen():
    text = ['Произошла ошибка',
            'Нажмите любую клавишу',
            'для выхода из игры']

    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in text:
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
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры: Нажимайте кнопки", ]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()
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
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BackGround = Background('fon.jpg', [0,0])


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

filename = input('Введите название файла:')
start_screen()
try:
    level = load_level(filename)
except (FileNotFoundError, IOError):
    error_screen()
level_map = load_level(filename)
enemy, hero, max_x, max_y = generate_level(level_map)
running = True
hero_hp = cur.execute(f'''SELECT hp_player from game WHERE 
                      numb == {numb_level}''')
new_hero_hp = 0
for elem1 in hero_hp:
    new_hero_hp += int(*elem1)
enemy_dmg = cur.execute(f'''SELECT dmg_enemy from game WHERE 
                      numb == {numb_level}''')
new_enemy_dmg = 0
for elem in enemy_dmg:
    new_enemy_dmg += int(*elem)
camera = Camera()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero, 'up')
                move1(enemy, 'up')
            elif event.key == pygame.K_DOWN:
                move(hero, 'down')
                move1(enemy, 'down')
            elif event.key == pygame.K_LEFT:
                move(hero, 'left')
                move1(enemy, 'right')
            elif event.key == pygame.K_RIGHT:
                move(hero, 'right')
                move1(enemy, 'left')
            if event.key == pygame.K_SPACE:
                hero.shoot()
    all_sprites.update()
    hits = pygame.sprite.groupcollide(enemy_group, bullets, True, True)
    hits1 = pygame.sprite.spritecollide(hero, enemy_group, False)
    if hits1:
        new_hero_hp -= new_enemy_dmg
        if new_hero_hp == 0:
            error_screen()
    camera.update(hero)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    all_sprites.draw(screen)
    player_group.draw(screen)
    enemy_group.draw(screen)
    sys.excepthook = except_hook
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()

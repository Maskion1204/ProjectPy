import os
import sys
import pygame

# Инициализация Pygame
pygame.init()
pygame.key.set_repeat(200, 70)

# Константы
FPS = 50
WIDTH, HEIGHT = 400, 300
STEP = 10
TILE_SIZE = 50

# Окно и таймер
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, color_key=None):  # Загрузка изображений из папки 'data/'
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):  # Загрузка уровня из файла 'data/filename'
    filepath = os.path.join('data', filename)
    with open(filepath, 'r', encoding="utf-8") as file:
        level_map = [line.strip() for line in file]

    max_width = max(map(len, level_map))
    return [line.ljust(max_width, '.') for line in level_map]


# Загрузка изображений
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')


class Tile(pygame.sprite.Sprite):  # Класс тайлов карты
    def __init__(self, tile_type, x, y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(TILE_SIZE * x, TILE_SIZE * y)


class Player(pygame.sprite.Sprite):  # Класс игрока
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(TILE_SIZE * x + 15, TILE_SIZE * y + 15)


def generate_level(level):  # Создание объектов уровня и возвращение позиции игрока
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player


def terminate():  # Завершение программы
    pygame.quit()
    sys.exit()


def start_screen():  # Отображение стартового экрана
    intro_text = ["Заставка", "",
                  "Правила игры:",
                  "WASD - движение", "X - выход"]

    background = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
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
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return
        pygame.display.flip()
        clock.tick(FPS)


# Запуск игры
start_screen()

# Загрузка уровня
player = generate_level(load_level("levels.txt"))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Отслеживание клавиш
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.rect.x += STEP
            elif event.key == pygame.K_a:
                player.rect.x -= STEP
            elif event.key == pygame.K_w:
                player.rect.y -= STEP
            elif event.key == pygame.K_s:
                player.rect.y += STEP

    # Отрисовка сцены
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

terminate()

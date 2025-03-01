import os
import sys
import pygame

# Инициализация Pygame
pygame.init()  # Инициализация всех модулей Pygame
pygame.key.set_repeat(200, 70)  # Настройка автоповтора нажатий клавиш (задержка 200 мс, интервал 70 мс)

# Константы
FPS = 50  # Количество кадров в секунду
WIDTH, HEIGHT = 800, 600  # Размеры окна игры
STEP = 6  # Шаг перемещения игрока
TILE_SIZE = 40  # Размер одного тайла на карте

# Окно и таймер
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна игры с заданными размерами
clock = pygame.time.Clock()  # Создание объекта для управления FPS
pygame.display.set_caption('Лабиринт')  # Установка заголовка окна

# Группы спрайтов
all_sprites = pygame.sprite.Group()  # Группа для всех спрайтов
tiles_group = pygame.sprite.Group()  # Группа для тайлов (стен, пола и т.д.)
player_group = pygame.sprite.Group()  # Группа для игрока


def terminate():
    pygame.quit()  # Завершение работы Pygame
    sys.exit()  # Завершение работы программы


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)  # Полный путь к файлу изображения
    try:
        image = pygame.image.load(fullname)  # Загрузка изображения
    except:
        image = pygame.image.load(os.path.join('data', 'missing.png'))  # Загрузка альтернативного изображения

    if color_key is not None:  # Если указан ключ цвета для прозрачности
        image = image.convert()  # Конвертация изображения для оптимизации
        if color_key == -1:  # Если ключ цвета равен -1, берем цвет из верхнего левого угла
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)  # Устанавливаем прозрачность
    else:
        image = image.convert_alpha()  # Конвертация с поддержкой альфа-канала
    return image


# Загрузка изображений
tile_images = {
    'wall': load_image('wall.png'),  # Загрузка изображения стены
    'empty': load_image('floor.png'),  # Загрузка изображения пола
    'missing': load_image('missing.png'),  # Загрузка изображения пустоты
    'exit': load_image('exit.png')  # Загрузка изображения выхода
}
player_image = load_image('mario.png')  # Загрузка изображения игрока


# Загрузка уровня
def load_level(filename):
    filepath = os.path.join('levels', filename)  # Полный путь к файлу уровня
    with open(filepath, 'r', encoding="utf-8") as file:  # Открытие файла на чтение
        level_map = [line.strip() for line in file]  # Чтение строк и удаление лишних пробелов

    max_width = max(map(len, level_map))  # Определение максимальной ширины уровня
    return [line.ljust(max_width, '.') for line in level_map]  # Выравнивание строк уровня до максимальной ширины


class ExitTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tiles_group, all_sprites)  # Инициализация спрайта и добавление в группы
        self.image = tile_images['exit']  # Установка изображения тайла выхода
        self.rect = self.image.get_rect().move(TILE_SIZE * x, TILE_SIZE * y)  # Позиция тайла на экране


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(tiles_group, all_sprites)  # Инициализация спрайта и добавление в группы
        self.image = tile_images[tile_type]  # Установка изображения тайла
        self.rect = self.image.get_rect().move(TILE_SIZE * x, TILE_SIZE * y)  # Позиция тайла на экране


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)  # Инициализация спрайта и добавление в группы
        self.image = player_image  # Установка изображения игрока
        self.rect = self.image.get_rect().move(TILE_SIZE * x + 15, TILE_SIZE * y + 15)  # Позиция игрока на экране


# Генерация уровня
def generate_level(level):
    new_player = None  # Изначально игрок не создан
    for y in range(len(level)):  # Проход по строкам уровня
        for x in range(len(level[y])):  # Проход по символам в строке
            if level[y][x] == '.':  # Если символ '.', создаем пол
                Tile('empty', x, y)
            elif level[y][x] == '#':  # Если символ '#', создаем стену
                Tile('wall', x, y)
            elif level[y][x] == '@':  # Если символ '@', создаем игрока
                Tile('empty', x, y)  # Сначала создаем пол под игроком
                new_player = Player(x, y)  # Затем создаем игрока
            elif level[y][x] == 'E':  # Если символ 'E', создаем выход
                Tile('empty', x, y)  # Сначала создаем пол под выходом
                ExitTile(x, y)  # Затем создаем тайл выхода
    return new_player  # Возвращаем объект игрока


# Заставка
def start_screen():
    splash_image = load_image('background.png')  # Загрузка изображения для заставки
    screen.blit(splash_image, (0, 0))  # Отображение изображения на весь экран
    pygame.display.flip()  # Обновление экрана

    waiting = True  # Флаг ожидания
    while waiting:
        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Если событие - закрытие окна
                terminate()  # Завершение программы
            elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:  # Если нажата клавиша или кнопка мыши
                waiting = False  # Завершение ожидания


def settings():
    settings_image = load_image('settings_background.png')  # Загрузка фона для экрана настроек

    font = pygame.font.Font(None, 50)  # Шрифт для текста
    easy_text = font.render("Простая", True, pygame.Color('white'))  # Текст кнопки
    middle_text = font.render("Средняя", True, pygame.Color('white'))  # Текст кнопки
    hard_text = font.render("Сложная", True, pygame.Color('white'))  # Текст кнопки
    back_text = font.render("Назад", True, pygame.Color('white'))  # Текст кнопки "Назад"

    easy_rect = easy_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))  # Позиция кнопки
    middle_rect = middle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Позиция кнопки
    hard_rect = hard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))  # Позиция кнопки
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))  # Позиция кнопки "Назад"

    while True:
        settings_func = read_settings()['Сложность']  # Чтение текущих настроек
        now_diff = ''
        if settings_func == 1:
            now_diff = 'Простая'
        elif settings_func == 2:
            now_diff = 'Средняя'
        elif settings_func == 3:
            now_diff = 'Сложная'
        now_text = font.render(f"Текущая сложность: {now_diff}", True, pygame.Color('white'))  # Обновление текста
        now_rect = now_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 125))  # Позиция текста

        screen.blit(settings_image, (0, 0))  # Отрисовка фона меню
        screen.blit(now_text, now_rect)  # Отрисовка текста текущей сложности
        screen.blit(easy_text, easy_rect)  # Отрисовка кнопки
        screen.blit(middle_text, middle_rect)  # Отрисовка кнопки
        screen.blit(hard_text, hard_rect)  # Отрисовка кнопки
        screen.blit(back_text, back_rect)  # Отрисовка кнопки

        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Если событие - закрытие окна
                terminate()  # Завершение программы
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Если нажата кнопка мыши
                settings_dict = read_settings()  # Чтение настроек
                if easy_rect.collidepoint(event.pos):  # Если нажата кнопка "Простая"
                    settings_dict['Сложность'] = 1  # Изменение сложности
                    update_settings(settings_dict)  # Обновление настроек
                elif middle_rect.collidepoint(event.pos):  # Если нажата кнопка "Средняя"
                    settings_dict['Сложность'] = 2  # Изменение сложности
                    update_settings(settings_dict)  # Обновление настроек
                elif hard_rect.collidepoint(event.pos):  # Если нажата кнопка "Сложная"
                    settings_dict['Сложность'] = 3  # Изменение сложности
                    update_settings(settings_dict)  # Обновление настроек
                elif back_rect.collidepoint(event.pos):  # Если нажата кнопка "Назад"
                    return  # Возврат в предыдущее меню

        pygame.display.flip()  # Обновление экрана
        clock.tick(FPS)  # Ограничение FPS


def read_settings():
    settings_dict = {}  # Словарь для статистики
    settings_file = os.path.join('data', 'settings.txt')  # Путь к файлу статистики
    try:
        with open(settings_file, 'r', encoding='utf-8') as file:  # Открытие файла на чтение
            for line in file:  # Чтение строк
                key, value = line.strip().split(' - ')  # Разделение строки на ключ и значение
                settings_dict[key] = int(value)  # Добавление значения в словарь
    except FileNotFoundError:  # Если файл не найден
        settings_dict = {  # Создание начальных значений
            'Сложность': 0
        }

        update_settings(settings_dict)  # Обновление файла статистики
    return settings_dict  # Возврат статистики


def update_settings(settings_dict):
    settings_file = os.path.join('data', 'settings.txt')  # Путь к файлу настроек
    with open(settings_file, 'w', encoding='utf-8') as file:  # Открытие файла на запись
        for key, value in settings_dict.items():  # Проход по элементам словаря
            file.write(f"{key} - {value}\n")  # Запись строки в файл


# Экран статистики
def stats_screen():
    stats_image = load_image('stats_background.png')  # Загрузка фона для экрана статистики
    stats = read_stats()  # Чтение статистики

    font = pygame.font.Font(None, 50)  # Шрифт для текста
    levels_text = font.render(f"Уровней пройдено: {stats['уровней пройдено']}", True, pygame.Color('white'))  # Текст
    # статистики
    time_text = font.render(f"Общее время: {stats['общее время']} сек", True, pygame.Color('white'))  # Текст времени
    wins_text = font.render(f"Побед: {stats['кол-во побед']}", True, pygame.Color('white'))  # Текст побед
    losses_text = font.render(f"Поражений: {stats['кол-во поражений']}", True, pygame.Color('white'))  # Текст поражений
    back_text = font.render("Назад", True, pygame.Color('white'))  # Текст кнопки "Назад"

    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))  # Позиция кнопки "Назад"

    while True:
        screen.blit(stats_image, (0, 0))  # Отрисовка фона
        screen.blit(levels_text, (WIDTH // 2 - levels_text.get_width() // 2, HEIGHT // 2 - 100))  # Отрисовка текста
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 - 50))  # Отрисовка текста
        screen.blit(wins_text, (WIDTH // 2 - wins_text.get_width() // 2, HEIGHT // 2))  # Отрисовка текста
        screen.blit(losses_text, (WIDTH // 2 - losses_text.get_width() // 2, HEIGHT // 2 + 50))  # Отрисовка текста
        screen.blit(back_text, back_rect)  # Отрисовка кнопки "Назад"

        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Если событие - закрытие окна
                terminate()  # Завершение программы
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Если нажата кнопка мыши
                if back_rect.collidepoint(event.pos):  # Если нажата кнопка "Назад"
                    return  # Возврат в главное меню

        pygame.display.flip()  # Обновление экрана
        clock.tick(FPS)  # Ограничение FPS


# Чтение статистики из файла
def read_stats():
    stats = {}  # Словарь для статистики
    stats_file = os.path.join('data', 'stats.txt')  # Путь к файлу статистики
    try:
        with open(stats_file, 'r', encoding='utf-8') as file:  # Открытие файла на чтение
            for line in file:  # Чтение строк
                key, value = line.strip().split(' - ')  # Разделение строки на ключ и значение
                stats[key] = int(value)  # Добавление значения в словарь
    except FileNotFoundError:  # Если файл не найден
        stats = {  # Создание начальных значений
            'уровней пройдено': 0,
            'общее время': 0,
            'кол-во побед': 0,
            'кол-во поражений': 0,
        }
        update_stats(stats)  # Обновление файла статистики
    return stats  # Возврат статистики


# Обновление статистики в файле
def update_stats(stats):
    stats_file = os.path.join('data', 'stats.txt')  # Путь к файлу статистики
    with open(stats_file, 'w', encoding='utf-8') as file:  # Открытие файла на запись
        for key, value in stats.items():  # Проход по элементам словаря
            file.write(f"{key} - {value}\n")  # Запись строки в файл


def win():
    stats = read_stats()  # Чтение статистики
    stats['кол-во побед'] += 1  # Увеличение количества побед
    stats['уровней пройдено'] += 1
    update_stats(stats)  # Обновление статистики

    gameover_image = load_image('win.png')  # Загрузка изображения победы
    screen.blit(gameover_image, (0, 0))  # Отображение изображения на экране
    pygame.display.flip()  # Обновление экрана

    start_time = pygame.time.get_ticks()  # Время начала показа экрана
    input_locked = True  # Флаг блокировки ввода (первые 3 секунды)
    total_wait_time = 5000  # Общее время показа (5 секунд)

    while True:
        current_time = pygame.time.get_ticks()  # Текущее время
        elapsed = current_time - start_time  # Прошедшее время

        if elapsed >= 3000:  # Если прошло 3 секунды
            input_locked = False  # Разблокировка ввода

        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Если событие - закрытие окна
                terminate()  # Завершение программы
            elif not input_locked:  # Если ввод разблокирован
                if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:  # Если нажата клавиша или кнопка мыши
                    return  # Возврат в меню

        if elapsed >= total_wait_time:  # Если прошло 5 секунд
            return  # Автоматический возврат в меню

        clock.tick(FPS)  # Ограничение FPS


def gameover():
    stats = read_stats()  # Чтение статистики
    stats['кол-во поражений'] += 1  # Увеличение количества поражений
    stats['уровней пройдено'] += 1
    update_stats(stats)  # Обновление статистики

    gameover_image = load_image('gameover.png')  # Загрузка изображения поражения
    screen.blit(gameover_image, (0, 0))  # Отображение изображения на экране
    pygame.display.flip()  # Обновление экрана

    start_time = pygame.time.get_ticks()  # Время начала показа экрана
    input_locked = True  # Флаг блокировки ввода (первые 3 секунды)
    total_wait_time = 5000  # Общее время показа (5 секунд)

    while True:
        current_time = pygame.time.get_ticks()  # Текущее время
        elapsed = current_time - start_time  # Прошедшее время

        if elapsed >= 3000:  # Если прошло 3 секунды
            input_locked = False  # Разблокировка ввода

        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Если событие - закрытие окна
                terminate()  # Завершение программы
            elif not input_locked:  # Если ввод разблокирован
                if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:  # Если нажата клавиша или кнопка мыши
                    return  # Возврат в меню

        if elapsed >= total_wait_time:  # Если прошло 5 секунд
            return  # Автоматический возврат в меню

        clock.tick(FPS)  # Ограничение FPS


class Wave:
    def __init__(self, level_width, level_height):
        self.active = False  # Флаг активности волны
        self.level_width = level_width  # Ширина уровня
        self.level_height = level_height  # Высота уровня
        self.y_position = 0  # Текущая позиция волны
        self.speed = 3  # Скорость движения волны
        self.height = 30  # Высота волны

    # Активация волны
    def activate(self):
        self.active = True  # Установка флага активности
        self.y_position = 0  # Сброс позиции волны

    # Обновление позиции волны
    def update(self):
        if self.active:  # Если волна активна
            self.y_position += self.speed  # Движение волны вниз
            if self.y_position >= self.level_height:  # Если волна достигла низа уровня
                self.active = False  # Деактивация волны

    # Отрисовка волны
    def draw(self, screen, camera):
        if self.active:  # Если волна активна
            wave_rect = pygame.Rect(0, self.y_position, self.level_width, self.height)  # Создание прямоугольника волны
            adjusted_rect = camera.apply_rect(wave_rect)  # Применение камеры
            surface = pygame.Surface((wave_rect.width, wave_rect.height), pygame.SRCALPHA)  # Создание поверхности
            surface.fill((0, 0, 255, 128))  # Заливка поверхности цветом
            screen.blit(surface, adjusted_rect.topleft)  # Отрисовка поверхности на экране

    # Проверка столкновения волны с игроком
    def check_collision(self, player_rect):
        if self.active:  # Если волна активна
            wave_rect = pygame.Rect(0, self.y_position, self.level_width, self.height)  # Создание прямоугольника волны
            return player_rect.colliderect(wave_rect)  # Проверка столкновения
        return False  # Если волна не активна, столкновения нет


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  # Прямоугольник камеры
        self.width = width  # Ширина камеры
        self.height = height  # Высота камеры

    # Применение камеры к объекту
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)  # Смещение объекта относительно камеры

    # Обновление позиции камеры
    def update(self, target):
        x = -target.rect.x + int(self.width / 2)  # Вычисление смещения по X
        y = -target.rect.y + int(self.height / 2)  # Вычисление смещения по Y
        x = min(0, x)  # Ограничение смещения по X
        y = min(0, y)  # Ограничение смещения по Y
        x = max(-(level_width - self.width), x)  # Ограничение смещения по X
        y = max(-(level_height - self.height), y)  # Ограничение смещения по Y
        self.camera = pygame.Rect(x, y, self.width, self.height)  # Обновление прямоугольника камеры

    # Применение камеры к прямоугольнику
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)  # Смещение прямоугольника относительно камеры


# Главное меню
def main_menu():
    menu_image = load_image('menu_background.png')  # Загрузка фона меню
    font = pygame.font.Font(None, 50)  # Шрифт для текста
    play_text = font.render("Играть", True, pygame.Color('white'))  # Текст кнопки "Играть"
    stats_text = font.render("Статистика", True, pygame.Color('white'))  # Текст кнопки "Статистика"
    settings_text = font.render("Настройки", True, pygame.Color('white'))  # Текст кнопки "Настройки"
    exit_text = font.render("Выход", True, pygame.Color('white'))  # Текст кнопки "Выход"

    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))  # Позиция кнопки "Играть"
    stats_rect = stats_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Позиция кнопки "Статистика"
    settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))  # Позиция кнопки "Настройки"
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 * 2))  # Позиция кнопки "Выход"

    while True:
        screen.blit(menu_image, (0, 0))  # Отрисовка фона меню
        screen.blit(play_text, play_rect)  # Отрисовка кнопки "Играть"
        screen.blit(stats_text, stats_rect)  # Отрисовка кнопки "Статистика"
        screen.blit(settings_text, settings_rect)  # Отрисовка кнопки "Настройки"
        screen.blit(exit_text, exit_rect)  # Отрисовка кнопки "Выход"

        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Если событие - закрытие окна
                terminate()  # Завершение программы
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Если нажата кнопка мыши
                if play_rect.collidepoint(event.pos):  # Если нажата кнопка "Играть"
                    return  # Возврат из меню
                elif stats_rect.collidepoint(event.pos):  # Если нажата кнопка "Статистика"
                    stats_screen()  # Переход на экран статистики
                elif settings_rect.collidepoint(event.pos):  # Если нажата кнопка "Настройки"
                    settings()  # Переход на экран настроек
                elif exit_rect.collidepoint(event.pos):  # Если нажата кнопка "Выход"
                    terminate()  # Завершение программы

        pygame.display.flip()  # Обновление экрана
        clock.tick(FPS)  # Ограничение FPS


start_screen()  # Отображение стартового экрана
levels = ['lvl 1.txt', 'lvl 2.txt', 'lvl 3.txt', 'lvl 4.txt', 'lvl 5.txt']
count_level = 0

# Основной цикл игры
while True:
    main_menu()  # Переход в главное меню

    # Инициализация новой игры
    all_sprites.empty()  # Очистка всех спрайтов
    tiles_group.empty()  # Очистка тайлов
    player_group.empty()  # Очистка игрока

    player = generate_level(load_level(levels[count_level]))  # Генерация уровня и создание игрока
    level = load_level(levels[count_level])  # Загрузка уровня
    level_width = len(level[0]) * TILE_SIZE  # Ширина уровня в пикселях
    level_height = len(level) * TILE_SIZE  # Высота уровня в пикселях
    wave = Wave(level_width, level_height)  # Создание волны
    level_start_time = pygame.time.get_ticks()  # Время начала уровня
    camera = Camera(WIDTH, HEIGHT)  # Создание камеры

    running = True  # Флаг работы игрового цикла
    font = pygame.font.Font(None, 36)  # Шрифт для текста (можно изменить размер)

    while running:
        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Если событие - закрытие окна
                terminate()  # Завершение программы

        keys = pygame.key.get_pressed()  # Получение состояния клавиш
        old_x, old_y = player.rect.x, player.rect.y  # Текущая позиция игрока
        dx, dy = 0, 0  # Смещение игрока

        if keys[pygame.K_a]: dx -= STEP  # Движение влево
        if keys[pygame.K_d]: dx += STEP  # Движение вправо
        if keys[pygame.K_w]: dy -= STEP  # Движение вверх
        if keys[pygame.K_s]: dy += STEP  # Движение вниз

        if dx != 0 or dy != 0:  # Если игрок движется
            length = (dx ** 2 + dy ** 2) ** 0.5  # Длина вектора движения
            dx = dx / length * STEP  # Нормализация по X
            dy = dy / length * STEP  # Нормализация по Y

        new_x = old_x + dx  # Новая позиция по X
        new_y = old_y + dy  # Новая позиция по Y

        # Проверка столкновений
        temp_rect_x = player.rect.move(dx, 0)  # Временный прямоугольник для проверки по X
        temp_rect_y = player.rect.move(0, dy)  # Временный прямоугольник для проверки по Y

        collided_x = any(  # Проверка столкновений по X
            tile.image == tile_images['wall'] and temp_rect_x.colliderect(tile.rect) for tile in tiles_group
        )
        collided_y = any(  # Проверка столкновений по Y
            tile.image == tile_images['wall'] and temp_rect_y.colliderect(tile.rect) for tile in tiles_group
        )

        if not collided_x: player.rect.x = new_x  # Если нет столкновения по X, обновляем позицию
        if not collided_y: player.rect.y = new_y  # Если нет столкновения по Y, обновляем позицию

        # Проверка выхода
        for tile in tiles_group:  # Проход по тайлам
            if isinstance(tile, ExitTile) and player.rect.colliderect(tile.rect):  # Если игрок на выходе
                win()  # Вызов экрана победы
                if count_level == 5:
                    count_level = 0
                else:
                    count_level += 1
                running = False  # Завершение игрового цикла

        # Обновление волны
        current_time = pygame.time.get_ticks()  # Текущее время
        Diff = read_settings()['Сложность']
        time_for_live = 0
        if Diff == 1:
            time_for_live = 16000
        elif Diff == 2:
            time_for_live = 12000
        elif Diff == 3:
            time_for_live = 8000
        if not wave.active and (current_time - level_start_time) >= time_for_live:  # Если прошло n секунд
            wave.activate()  # Активация волны

        if wave.active:  # Если волна активна
            wave.update()  # Обновление позиции волны
            if wave.check_collision(player.rect):  # Если волна столкнулась с игроком
                gameover()  # Вызов экрана поражения
                count_level = 0
                running = False  # Завершение игрового цикла

        # Отрисовка
        camera.update(player)  # Обновление камеры
        screen.fill((0, 0, 0))  # Очистка экрана
        for tile in tiles_group:  # Отрисовка тайлов
            screen.blit(tile.image, camera.apply(tile))
        wave.draw(screen, camera)  # Отрисовка волны
        screen.blit(player.image, camera.apply(player))  # Отрисовка игрока

        # Секундомер
        elapsed_time = current_time - level_start_time  # Прошедшее время в миллисекундах
        seconds = elapsed_time // 1000  # Преобразование в секунды
        minutes = seconds // 60  # Преобразование в минуты
        seconds %= 60  # Оставшиеся секунды
        timer_text = font.render(f"Время: {minutes:02}:{seconds:02}", True,
                                 pygame.Color('white'))  # Форматирование времени
        screen.blit(timer_text, (10, 10))  # Отрисовка времени (координаты: x=10, y=50)

        pygame.display.flip()  # Обновление экрана
        clock.tick(FPS)  # Ограничение FPS

# Завершение программы
terminate()

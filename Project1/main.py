import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Блокировка вывода в консоль информации о pygame
import pygame
import random
import time
from collections import deque
import sys
import json
import math

# --- БЛОК для компиляции кода ---
def resource_path(relative_path):
    """ Получает правильный путь к ресурсам, независимо код (main.py) или exe файл. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# ---------------------------------

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# --- УСТАНОВКА ИКОНКИ ОКНА ---
try:
    # Загружаем именно .ico
    icon_path = resource_path("icon.ico")
    icon_image = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_image)
except Exception as e:
    # Этот принт скроется, так как вы используете --noconsole
    print(f"Не удалось установить иконку: {e}")

# КОНФИГУРАЦИЯ ИГРОВЫХ ПАРАМЕТРОВ
DIFFICULTY_LEVELS = {
    1: {'MAZE_WIDTH': 21, 'MAZE_HEIGHT': 23, 'SPIDERS_COUNT': 5, 'SWORDS_COUNT': 5, 
        'TIME_COUNT': 10, 'POINTERS_COUNT': 10, 'time_TIMER_MAX': 240.0, 'time_BONUS_TIME': 60.0,
        'spider_SPEED': 8, 'EXTRA_PATHS': 2, 'HOUSE_SWORDS_COUNT': 3, 'NAME': 'EASY'},
    
    2: {'MAZE_WIDTH': 31, 'MAZE_HEIGHT': 33, 'SPIDERS_COUNT': 10, 'SWORDS_COUNT': 10,
        'TIME_COUNT': 15, 'POINTERS_COUNT': 15, 'time_TIMER_MAX': 300.0, 'time_BONUS_TIME': 60.0,
        'spider_SPEED': 8, 'EXTRA_PATHS': 10, 'HOUSE_SWORDS_COUNT': 5, 'NAME': 'NORMAL'},
    
    3: {'MAZE_WIDTH': 41, 'MAZE_HEIGHT': 43, 'SPIDERS_COUNT': 20, 'SWORDS_COUNT': 23,
        'TIME_COUNT': 20, 'POINTERS_COUNT': 20, 'time_TIMER_MAX': 360.0, 'time_BONUS_TIME': 60.0,
        'spider_SPEED': 7, 'EXTRA_PATHS': 30, 'HOUSE_SWORDS_COUNT': 10, 'NAME': 'HARD'},
    
    4: {'MAZE_WIDTH': 51, 'MAZE_HEIGHT': 53, 'SPIDERS_COUNT': 40, 'SWORDS_COUNT': 45,
        'TIME_COUNT': 45, 'POINTERS_COUNT': 45, 'time_TIMER_MAX': 420.0, 'time_BONUS_TIME': 60.0,
        'spider_SPEED': 6, 'EXTRA_PATHS': 50, 'HOUSE_SWORDS_COUNT': 25, 'NAME': 'CHALLENGING'},
    
    5: {'MAZE_WIDTH': 61, 'MAZE_HEIGHT': 63, 'SPIDERS_COUNT': 70, 'SWORDS_COUNT': 75,
        'TIME_COUNT': 75, 'POINTERS_COUNT': 75, 'time_TIMER_MAX': 480.0, 'time_BONUS_TIME': 60.0,
        'spider_SPEED': 6, 'EXTRA_PATHS': 80, 'HOUSE_SWORDS_COUNT': 35, 'NAME': 'DIFFICULT'},
    
    6: {'MAZE_WIDTH': 71, 'MAZE_HEIGHT': 73, 'SPIDERS_COUNT': 90, 'SWORDS_COUNT': 95,
        'TIME_COUNT': 95, 'POINTERS_COUNT': 95, 'time_TIMER_MAX': 540.0, 'time_BONUS_TIME': 60.0,
        'spider_SPEED': 5, 'EXTRA_PATHS': 120, 'HOUSE_SWORDS_COUNT': 45, 'NAME': 'EXTREME'},
    
    7: {'MAZE_WIDTH': 101, 'MAZE_HEIGHT': 103, 'SPIDERS_COUNT': 100, 'SWORDS_COUNT': 105,
        'TIME_COUNT': 105, 'POINTERS_COUNT': 105, 'time_TIMER_MAX': 600.0, 'time_BONUS_TIME': 60.0,
        'spider_SPEED': 4, 'EXTRA_PATHS': 150, 'HOUSE_SWORDS_COUNT': 50, 'NAME': 'NIGHTMARE'}
}

CURRENT_DIFFICULTY = 2

class GameConfig:
    """Класс для хранения конфигурации игры"""
    # Размеры окна и лабиринта
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    MAZE_WIDTH = DIFFICULTY_LEVELS[CURRENT_DIFFICULTY]['MAZE_WIDTH']
    MAZE_HEIGHT = DIFFICULTY_LEVELS[CURRENT_DIFFICULTY]['MAZE_HEIGHT']
    # Исходные размеры
    ORIGINAL_CELL_SIZE = 60
    ORIGINAL_INFO_PANEL_HEIGHT = 40
    ORIGINAL_UI_PANEL_WIDTH = 100
    # Коэффициенты
    LINE_SPACING = 1.5
    SPIDER_ANIMATION_SPEED = 500
    PLAYER_ANIMATION_SPEED = 100
    time_TIMER_MAX = DIFFICULTY_LEVELS[CURRENT_DIFFICULTY]['time_TIMER_MAX']
    time_BONUS_TIME = DIFFICULTY_LEVELS[CURRENT_DIFFICULTY]['time_BONUS_TIME']
    HOUSE_X, HOUSE_Y = 1, 1
    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK_GREEN = (0, 170, 0)
    LIGHT_GREEN = (144, 238, 144) # Светло-зеленый
    RED = (255, 0, 0)
    TOMATO = (255,99,71) # Томатный
    SWORD_COLOR = (0, 0, 139)
    YELLOW = (255, 255, 0)
    HOUSE_COLOR = (139, 69, 19)
    PURPLE = (128, 0, 128)
    INFO_BACKGROUND = (30, 30, 30)
    BAR_BACKGROUND = (50, 50, 50)
    BAR_FOREGROUND = (255, 0, 0)
    BAR_BORDER = (200, 200, 200)
    BLUE = (0, 0, 255)
    GREY = (169, 169, 169)
    LIGHT_YELLOW = (255, 255, 224)
    SEPARATOR_COLOR = (100, 100, 100)
    GOLD = (255, 215, 0)  # Золотой для GOD MODE
    LABYRINTH_BORDER_COLOR = GREY
    LABYRINTH_BORDER_WIDTH = 2
    MENU_BAR_COLOR = (50, 50, 50)
    MENU_ITEM_COLOR = WHITE
    MENU_ITEM_HOVER_COLOR = LIGHT_YELLOW
    MENU_TEXT_BACKGROUND = (0, 0, 0, 180)
    PATH_COLOR = (128, 0, 128)
    # Анимация
    SPIDER_DEATH_ANIMATION_DURATION = 7.0
    SPIDER_DEATH_ANIMATION_SPEED = 0.25

class ResourceManager:
    """Класс для управления ресурсами (изображения, звуки)"""
    def __init__(self):
        self.scaled_images = {}
        self.editor_ui_icons = {}
        self.original_images = {}
        self.sounds = {}
        
    def load_image(self, filepath):
        """Загрузка изображения с обработкой ошибок"""
        filepath = resource_path(os.path.join("img", filepath))  # добавляем resource_path
        if not os.path.exists(filepath):
            return pygame.Surface((32, 32))
        try:
            return pygame.image.load(filepath).convert_alpha()
        except pygame.error as e:
            return pygame.Surface((32, 32))

    def load_all_images(self):
        """Загрузка всех исходных изображений"""
        images_to_load = {
            'sword': "sword.png",
            'swords': "swords.png",
            'time': "time.png",
            'spider': "spider.png",
            'spider1': "spider1.png",
            'map': "map.png",
            'map1': "map1.png",

            'spider_dead1': "spider_dead1.png",
            'spider_dead2': "spider_dead2.png",
            'player_killed_spider1': "player_killed_spider1.png",
            'player_killed_spider2': "player_killed_spider2.png",
            'player_stop': "player_stop.png",
            'player_run1': "player_run1.png",
            'player_run2': "player_run2.png",
            'player_run3': "player_run3.png",
            
            'player_down_run1': "player_down_run1.png",
            'player_down_run2': "player_down_run2.png",
            'player_up_run1': "player_up_run1.png",
            'player_up_run2': "player_up_run2.png",
            
            'player_sword_run1': "player_sword_run1.png",
            'player_sword_run2': "player_sword_run2.png",
            'player_sword_run3': "player_sword_run3.png",
            
            'player_sword_up1': "player_sword_up1.png",
            'player_sword_up2': "player_sword_up2.png",
            'player_sword_down1': "player_sword_down1.png",
            'player_sword_down2': "player_sword_down2.png",
            'player_sword_stop': "player_sword_stop.png",
            
            'rip': "rip.png",
            'player_treasure_run1': "player_treasure_run1.png",
            'player_treasure_run2': "player_treasure_run2.png",

            'player_treasure_down1': "player_treasure_down1.png",
            'player_treasure_down2': "player_treasure_down2.png",
            'player_treasure_up1': "player_treasure_up1.png",
            'player_treasure_up2': "player_treasure_up2.png",
            'player_treasure_stop': "player_treasure_stop.png",

            'treasure': "treasure.png",
            'house': "home.png",
            # 'wall': "wall.png",
            'door': "door.png"
        }

        # === ДОБАВЛЯЕМ ВСЕ ВАРИАНТЫ СТЕН ===
        # Динамически добавляем wall1.png, wall2.png, wall3.png, ...
        for i in range(1, 34): # стены wall1.png, wall2.png, wall3.png, ...
            images_to_load[f'wall{i}'] = f"wall{i}.png"
        
        # Стандартная стена (запасной вариант)
        images_to_load['wall'] = "wall.png"
               
        for key, filename in images_to_load.items():
            self.original_images[key] = self.load_image(filename)
    
    def scale_images(self, cell_size, scale_factor):
        """Масштабирование всех изображений"""
        self.scaled_images.clear()
        
        for key, image in self.original_images.items():
            if image:
                self.scaled_images[key] = pygame.transform.scale(image, (cell_size, cell_size))
        
        # Специальная обработка для иконок редактора
        icon_scale_factor = 1.0 / 3.0
        scaled_icon_size = int(GameConfig.ORIGINAL_UI_PANEL_WIDTH * 0.8 * icon_scale_factor)
        
        self.editor_ui_icons = {
            'wall': pygame.transform.scale(self.original_images.get('wall', pygame.Surface((32, 32))), 
                                         (scaled_icon_size, scaled_icon_size)),
            'door': pygame.transform.scale(self.original_images.get('door', pygame.Surface((32, 32))), 
                                        (scaled_icon_size, scaled_icon_size)), 
            'path': pygame.transform.scale(self.load_image('path.png'), 
                                         (scaled_icon_size, scaled_icon_size)),
            'sword': pygame.transform.scale(self.original_images.get('sword', pygame.Surface((32, 32))), 
                                          (scaled_icon_size, scaled_icon_size)),
            'time': pygame.transform.scale(self.original_images.get('time', pygame.Surface((32, 32))), 
                                         (scaled_icon_size, scaled_icon_size)),
            'pointer': pygame.transform.scale(self.original_images.get('map', pygame.Surface((32, 32))), 
                                            (scaled_icon_size, scaled_icon_size)),
            'spider': pygame.transform.scale(self.original_images.get('spider', pygame.Surface((32, 32))), 
                                           (scaled_icon_size, scaled_icon_size)),
            'treasure': pygame.transform.scale(self.original_images.get('treasure', pygame.Surface((32, 32))), 
                                             (scaled_icon_size, scaled_icon_size)),
            'house': pygame.transform.scale(self.original_images.get('house', pygame.Surface((32, 32))), 
                                          (scaled_icon_size, scaled_icon_size)),
        }

    def load_sounds(self):
        """Загрузка звуков из папки sound"""
        sound_files = {
            'move': 'run.wav',
            'victory': 'victory.wav', 
            'sword': 'sword.wav',
            'take': 'take.wav',
            'game_over': 'game-over.wav'
        }
        
        for sound_name, filename in sound_files.items():
            try:
                sound_path = resource_path(os.path.join("sound", filename))
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
            except Exception as e:
                print(f"Не удалось загрузить звук {filename}: {e}")
                self.sounds[sound_name] = None

class Player:
    """Класс игрока"""
    __slots__ = ('x', 'y', 'has_sword', 'has_treasure', 'direction', 'is_moving', 
                 'current_frame_index', 'last_frame_change_time')

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_sword = False
        self.has_treasure = False
        self.direction = 'right'
        self.is_moving = False
        self.current_frame_index = 0
        self.last_frame_change_time = 0

    def move(self, dx, dy, maze):
        new_x, new_y = self.x + dx, self.y + dy
        
        # Проверяем проходимость: обычный проход ИЛИ дополнительный проход (дверь)
        is_passable = (
            (0 <= new_x < len(maze.grid) and 0 <= new_y < len(maze.grid[0])) and
            (maze.grid[new_x][new_y] == 0 or  # обычный проход
            (new_x, new_y) in getattr(maze, 'extra_paths', set()))  # дополнительный проход (дверь)
        )
        
        if is_passable:
            self.x, self.y = new_x, new_y
            self.is_moving = True
            
            # Обновление направления
            if dx > 0: self.direction = 'down'
            elif dx < 0: self.direction = 'up'
            elif dy > 0: self.direction = 'right'
            elif dy < 0: self.direction = 'left'
                
            return True
        
        self.is_moving = False
        return False

    def get_image(self, resource_manager, game_over=False, show_death_image=False):
            """Получение текущего изображения игрока"""
            if game_over and show_death_image:
                return resource_manager.scaled_images.get('rip')
            
            current_time = pygame.time.get_ticks()
            if self.is_moving and current_time - self.last_frame_change_time >= GameConfig.PLAYER_ANIMATION_SPEED:
                self.current_frame_index = (self.current_frame_index + 1) % 3  # 3 кадра анимации
                self.last_frame_change_time = current_time
            
            # Определяем базовые наборы анимаций для каждого состояния
            if self.has_treasure:
                # Анимация для игрока с кладом с полной поддержкой направлений
                if self.is_moving:
                    if self.direction == 'down':
                        # Движение вниз с сокровищем - 2 кадра
                        frame_key = 'player_treasure_down1' if self.current_frame_index < 2 else 'player_treasure_down2'
                    elif self.direction == 'up':
                        # Движение вверх с сокровищем - 2 кадра
                        frame_key = 'player_treasure_up1' if self.current_frame_index < 2 else 'player_treasure_up2'
                    else:
                        # Боковая анимация с сокровищем - 2 кадра
                        frame_key = 'player_treasure_run1' if self.current_frame_index < 2 else 'player_treasure_run2'
                else:
                    # Стоячая поза с сокровищем
                    frame_key = 'player_treasure_stop'
                    
            elif self.has_sword:
                # Анимация для игрока с мечом с полной поддержкой направлений
                if self.is_moving:
                    if self.direction == 'down':
                        # Движение вниз с мечом - 2 кадра
                        frame_key = 'player_sword_down1' if self.current_frame_index < 2 else 'player_sword_down2'
                    elif self.direction == 'up':
                        # Движение вверх с мечом - 2 кадра
                        frame_key = 'player_sword_up1' if self.current_frame_index < 2 else 'player_sword_up2'
                    else:
                        # Боковая анимация с мечом (влево/вправо) - 3 кадра
                        if self.current_frame_index == 0:
                            frame_key = 'player_sword_run1'
                        elif self.current_frame_index == 1:
                            frame_key = 'player_sword_run2'
                        else:
                            frame_key = 'player_sword_run3'
                else:
                    # Стоячая поза с мечом
                    frame_key = 'player_sword_stop'

            else:
                # Анимация для игрока без меча
                if self.is_moving:
                    if self.direction == 'down':
                        # Движение вниз - 2 кадра
                        frame_key = 'player_down_run1' if self.current_frame_index < 2 else 'player_down_run2'
                    elif self.direction == 'up':
                        # Движение вверх - 2 кадра
                        frame_key = 'player_up_run1' if self.current_frame_index < 2 else 'player_up_run2'
                    else:
                        # Боковая анимация (влево/вправо) - 3 кадра
                        if self.current_frame_index == 0:
                            # ИСПРАВЛЕНИЕ 1: Должен быть 'player_run1', а не 'player_stop'
                            frame_key = 'player_run1'
                        elif self.current_frame_index == 1:
                            frame_key = 'player_run2'
                        else:
                            frame_key = 'player_run3'
                else:
                    # Стоячая поза без меча - ВСЕГДА player_stop.png
                    frame_key = 'player_stop'
            
            image = resource_manager.scaled_images.get(frame_key)
            
            # Применяем зеркальное отражение для левого направления
            if image and self.direction == 'left':
                # Определяем, для каких анимаций нужно применять отражение
                need_flip = False
                
                if self.has_treasure:
                    # Для сокровища - отражение только для боковых анимаций
                    need_flip = frame_key in ['player_treasure_run1', 'player_treasure_run2']
                elif self.has_sword:
                    # Для меча - отражение только для боковых анимаций
                    need_flip = frame_key in ['player_sword_run1', 'player_sword_run2', 'player_sword_run3']
                else:
                    # ИСПРАВЛЕНИЕ 2: Отражение только для бегущих кадров (включая 'player_run1')
                    need_flip = frame_key in ['player_run1', 'player_run2', 'player_run3']
                
                if need_flip:
                    image = pygame.transform.flip(image, True, False)
            
            return image

class SpiderEnemy:
    """Класс паука"""
    __slots__ = ('x', 'y', 'defeated', 'defeated_time', 'old_pos')

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.defeated = False
        self.defeated_time = 0
        self.old_pos = (x, y)
    
    def get_image(self, resource_manager, current_image_index):
        """Получение изображения паука"""
        if self.defeated:
            elapsed = time.time() - self.defeated_time
            if elapsed < GameConfig.SPIDER_DEATH_ANIMATION_DURATION:
                frame = 'spider_dead1' if int(elapsed / GameConfig.SPIDER_DEATH_ANIMATION_SPEED) % 2 == 0 else 'spider_dead2'
                return resource_manager.scaled_images.get(frame)
            return None
        
        frame_key = 'spider' if current_image_index == 0 else 'spider1'
        return resource_manager.scaled_images.get(frame_key)

class Maze:
    """Класс лабиринта"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1] * width for _ in range(height)]
        self.swords_positions = []
        self.swords_set = set()  # множество для быстрого поиска
        self.times_positions = []
        self.times_set = set()
        self.path_pointers_positions = []
        self.pointers_set = set()
        self.spiders = []
        self.treasure_position = None
        self.extra_paths = set()
    
    def generate(self):
        """Генерация нового лабиринта с использованием итеративного подхода"""
        self.grid = [[1] * self.width for _ in range(self.height)]
        
        def carve_path_iterative(start_x, start_y):
            stack = [(start_x, start_y)]
            self.grid[start_x][start_y] = 0
            
            while stack:
                cx, cy = stack[-1]
                directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
                random.shuffle(directions)
                
                found = False
                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if (0 < nx < self.height - 1 and 0 < ny < self.width - 1 
                        and self.grid[nx][ny] == 1):
                        # Прорубаем стену между текущей и новой клеткой
                        self.grid[nx - dx//2][ny - dy//2] = 0
                        self.grid[nx][ny] = 0
                        stack.append((nx, ny))
                        found = True
                        break
                
                if not found:
                    stack.pop()
        
        # Начинаем с центра для больших лабиринтов
        start_x, start_y = self.height // 2, self.width // 2
        if start_x % 2 == 0: start_x -= 1
        if start_y % 2 == 0: start_y -= 1
        
        carve_path_iterative(start_x, start_y)
        
        # Гарантируем, что дом доступен
        self.grid[1][1] = 0
        if self.grid[1][2] == 1 and self.grid[2][1] == 1:
            self.grid[1][2] = 0  # Гарантируем выход из дома

        # Создаем двери на всех проходах вокруг дома
        house_x, house_y = 1, 1
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # справа, слева, снизу, сверху
        
        for dx, dy in directions:
            door_x, door_y = house_x + dx, house_y + dy
            # Если это проход и в пределах лабиринта - делаем дверью
            if (0 <= door_x < self.height and 0 <= door_y < self.width and 
                self.grid[door_x][door_y] == 0):
                self.extra_paths.add((door_x, door_y))

    def add_random_paths(self, num_extra_paths=100):
        """Добавление проходов - избегаем одинарных стен"""
        paths_added = 0
        attempts = 0
        max_attempts = num_extra_paths * 30

        while paths_added < num_extra_paths and attempts < max_attempts:
            x = random.randint(2, self.height - 3)
            y = random.randint(2, self.width - 3)
            attempts += 1
            
            # Гарантируем, что это стена (не проход)
            if self.grid[x][y] != 1:
                continue
                
            # Горизонтальная стена - проверяем что это стена между двумя проходами
            if (self.grid[x][y-1] == 0 and self.grid[x][y+1] == 0 and
                self.grid[x-1][y] == 1 and self.grid[x+1][y] == 1 and
                self.grid[x][y-2] == 1 and self.grid[x][y+2] == 1):
                
                # === НОВАЯ ПРОВЕРКА: не создаст ли это одинарную стену ===
                creates_single_wall = False
                
                # Проверяем соседние стены сверху и снизу
                for dx in [-1, 1]:
                    nx = x + dx
                    # Если соседняя клетка - стена, проверяем не станет ли она одинарной
                    if self.grid[nx][y] == 1:
                        # Считаем сколько проходов вокруг этой соседней стены
                        path_count = 0
                        for dxx, dyy in [(-1,0), (1,0), (0,-1), (0,1)]:
                            nnx, nny = nx + dxx, y + dyy
                            if 0 <= nnx < self.height and 0 <= nny < self.width:
                                if self.grid[nnx][nny] == 0:
                                    path_count += 1
                        
                        # Если будет 3 или больше проходов - это станет одинарной стеной
                        if path_count >= 3:
                            creates_single_wall = True
                            break
                
                if not creates_single_wall:
                    self.grid[x][y] = 0  # ПРЕВРАЩАЕМ В ПРОХОД
                    self.extra_paths.add((x, y))  # И ДОБАВЛЯЕМ В СПИСОК ДВЕРЕЙ
                    paths_added += 1
                    continue
                
            # Вертикальная стена - проверяем что это стена между двумя проходами
            elif (self.grid[x-1][y] == 0 and self.grid[x+1][y] == 0 and
                self.grid[x][y-1] == 1 and self.grid[x][y+1] == 1 and
                self.grid[x-2][y] == 1 and self.grid[x+2][y] == 1):
                
                # === НОВАЯ ПРОВЕРКА: не создаст ли это одинарную стену ===
                creates_single_wall = False
                
                # Проверяем соседние стены слева и справа
                for dy in [-1, 1]:
                    ny = y + dy
                    # Если соседняя клетка - стена, проверяем не станет ли она одинарной
                    if self.grid[x][ny] == 1:
                        # Считаем сколько проходов вокруг этой соседней стены
                        path_count = 0
                        for dxx, dyy in [(-1,0), (1,0), (0,-1), (0,1)]:
                            nnx, nny = x + dxx, ny + dyy
                            if 0 <= nnx < self.height and 0 <= nny < self.width:
                                if self.grid[nnx][nny] == 0:
                                    path_count += 1
                        
                        # Если будет 3 или больше проходов - это станет одинарной стеной
                        if path_count >= 3:
                            creates_single_wall = True
                            break
                
                if not creates_single_wall:
                    self.grid[x][y] = 0  # ПРЕВРАЩАЕМ В ПРОХОД
                    self.extra_paths.add((x, y))  # И ДОБАВЛЯЕМ В СПИСОК ДВЕРЕЙ
                    paths_added += 1
        
        print(f"Из {num_extra_paths} добавлено {paths_added} проходов (попыток: {attempts})")
        return paths_added

    def is_adjacent_to_path(self, position):
        """Проверяет, является ли стена рядом с проходом"""
        x, y = position
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.height and 0 <= ny < self.width and self.grid[nx][ny] == 0:
                return True
        return False

class GameState:
    def __init__(self):
        self.game_over = False
        self.game_won = False
        self.game_paused = False
        self.pause_start_time = None
        self.show_death_image = False
        self.show_path = False
        self.path_hide_time = None
        self.time_timer = GameConfig.time_TIMER_MAX
        self.timer_running = False
        self.last_timer_update = time.time()
        self.scale_factor = 1.0
        self.game_mode = 'game'
        self.show_minimap = False
        self.show_combined_dialog = False
        self.combined_dialog_mode = None
        self.file_list = []
        self.selected_file_index = 0
        self.current_directory = "."
        self.combined_filename_input = ""
        self.last_second_time = time.time()
        self.timer_active = False
        self.pause_type = None  # 'space_pause' или 'menu_pause'
        self.current_score = 0
        self.total_score = 0  # Общий счет за всю сессию
        self.high_score = 0   # Рекорд
        self.maps_completed = 0 # счетчик пройденных карт
        self.campaign_mode = False
        self.campaign_level = 1  # текущий уровень в кампании (1-7)
        self.campaign_wins = 0   # количество побед на текущем уровне
        self.campaign_completed = False  # полное прохождение кампании
        self.show_exit_campaign_dialog = False  # Новое состояние для диалога
        self.show_enter_campaign_dialog = False  # Новое состояние для диалога входа
        self.time_timer_enabled = True  # По умолчанию таймер включен

        self.spider_speed_custom = False  # Флаг использования пользовательской скорости
        self.spider_speed_value = 8  # Значение пользовательской скорости (по умолчанию 8)  
        self.god_mode = False # пасхалка      

class Game:
    """Основной класс игры"""
    def __init__(self):
        self.config = GameConfig()
        self.resource_manager = ResourceManager()
        self.maze = Maze(self.config.MAZE_WIDTH, self.config.MAZE_HEIGHT)
        self.player = Player(self.config.HOUSE_X, self.config.HOUSE_Y)
        self.state = GameState()
        self.current_difficulty = CURRENT_DIFFICULTY
        self.difficulty_names = {
            1: "EASY",
            2: "NORMAL", 
            3: "HARD",
            4: "CHALLENGING",
            5: "DIFFICULT", 
            6: "EXTREME",
            7: "NIGHTMARE"
        }

        # Для навигации по меню FREE PLAY - Выбор Level
        self.level_navigation_index = 0
        self.screen = None
        self.cell_size = self.config.ORIGINAL_CELL_SIZE
        self.info_panel_height = self.config.ORIGINAL_INFO_PANEL_HEIGHT
        self.ui_panel_width = self.config.ORIGINAL_UI_PANEL_WIDTH
        self.visible_maze_width = 0
        self.visible_maze_height = 0
        self.fonts = {}
        
        # Добавлена поверхность для лабиринта
        self.labyrinth_surface = None
        
        self.clock = pygame.time.Clock()
        
        # Увеличена частота кадров и скорректированы задержки
        self.FPS = 12  # При большом FPS управление от клавиш усложняется (мгновенное срабатывание)
        self.move_delay = 0.0
        self.swap_delay = 0.3
        
        self.last_move_time = time.time()
        self.last_swap_time = 0.0
        self.spider_move_counter = 0
        
        self.spider_speed = DIFFICULTY_LEVELS[self.current_difficulty]['spider_SPEED']

        self.current_spider_image_index = 0
        self.last_spider_image_change_time = 0
        self.current_map_pointer_index = 0
        self.last_map_pointer_change_time = 0
        self.MAP_POINTER_ANIMATION_SPEED = 500  # мс между сменой кадров
        self.menu_items = ["Menu", "FREE PLAY", "CAMPAIGN", "Instructions", "About"]
        self.menu_rects = {}
        self.active_menu_item = None
        self.show_overlay_text = None
        self.menu_open_with_keyboard = False
        
        self.instruction_text = [
            "--- CONTROLS ---",
            "Arrow Keys (Up, Down, Left, Right) or WASD: Move/Navigation Menu",
            "Alt: Menu, Enter: menu item selection",
            "Tab: Toggle Map Editor mode",
            "Space: Pause the game",
            "Esc: Cancel/Return",
            "The prisoner will guide your way",
            "--- GAME MISSIONS ---",
            "Bring the treasure home or kill all the spiders",
            "--- MAP EDITOR ---",
            "Mouse Left Click: Place objects",
            "Mouse Right Click: Remove objects",
            "Tool Panel: Select what to place",
            "Available: Wall, Door, Path, Sword, time,",
            "Pointer, Spider, Treasure, House",
            "--- SAVE/LOAD ---",
            "Buttons or Menu - Save/Load: Map or Game with Map",
            "Type filename - Press Enter"
        ]
        
        self.about_text = [
            "Developer",
            "sh17aleksandr@gmail.com",
            "Version 1.0"
        ]

        self.editor_tools = ['wall', 'door', 'path', 'sword', 'time', 'pointer', 'spider', 'treasure', 'house']
        self.selected_tool = None  # Изменено: по умолчанию ничего не выбрано
        self.editor_message = ""
        self.editor_message_time = 0
        self.prev_window_size = (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT)
        self.is_maximized = False
        self.last_resize_time = 0
        self.resize_delay = 0.05  # 50 мс, ограничение частоты обновления окна
        self.menu_navigation_index = 0 # Новые переменные для навигации по меню
        self.horizontal_nav_index = 0  # Индекс для горизонтальной навигации по меню
        self.menu_open_with_keyboard = False
        self.sound_enabled = True
        self.win_animation_time = 0
        self.win_particles = []
        self.win_animation_duration = 3.0  # длительность анимации в секундах
        self.cached_maze_dimensions = None # Кэш
        
        # Добавлен кэш для UI текстов
        self.ui_text_cache = {}
        self.last_cached_scale = None
        
        self.load_high_score() # Загрузка рекорда из файла
        self.mouse_move_target = None
        self.mouse_move_path = []
        self.mouse_move_index = 0
        self.last_mouse_move_time = 0
        self.mouse_move_delay = self.move_delay
        self.mouse_move_take_item = False  # Флаг для взятия предмета
        self.mouse_move_item_to_take = None
        self.exit_dialog_selected_button = 'cancel'  # По умолчанию Cancel выделен
        self.enter_dialog_selected_button = 'cancel'  # По умолчанию Cancel выделен

        self.current_wall_image = 'wall'  # По умолчанию стандартная стена

    def handle_campaign_interaction(self, current_time):
        """Универсальная обработка взаимодействия с кампанией"""
        # Всегда показываем актуальное описание кампании
        self.show_overlay_text = self.campaign_description
        self.state.game_paused = True
        self.state.pause_start_time = current_time
        
        # Если кампания не активна или завершена - запускаем новую
        if not (self.state.campaign_mode and not self.state.campaign_completed):
            self.active_menu_item = None
            self.menu_open_with_keyboard = False
            self.start_campaign()

    @property
    def campaign_description(self):
        """Динамическое описание кампании с текущим прогрессом"""
        return [
            "CAMPAIGN MODE",
            " ",
            f"Current Level: {self.get_level_name(self.state.campaign_level)}",
            f"Wins: {self.state.campaign_wins}/3",
            " ",
            "Win 3 times on each level",
            "to complete the campaign!",
            " ",
            "Progress:",
            "Easy -> Normal -> Hard -> Challenging",
            "-> Difficult -> Extreme -> Nightmare",
            " "
        ]

    # === Методы для работы с очками ===
    def add_score(self, points, reason=""):
        """Добавление очков"""
        self.state.current_score += points

        # Обновляем рекорд если текущий счет больше
        if self.state.current_score > self.state.high_score:
            self.state.high_score = self.state.current_score
            self.save_high_score()
        
        if reason:
            self.set_editor_message(f"Score +{points}: {reason}")

    def reset_score(self):
        self.state.current_score = 0 # Сброс текущего счета (при проигрыше)

    def load_high_score(self):
        """Загрузка рекорда из файла"""
        try:
            if os.path.exists("highscore.dat"):
                with open("highscore.dat", "r") as f:
                    self.state.high_score = int(f.read())
        except:
            self.state.high_score = 0

    def save_high_score(self):
        """Сохранение рекорда в файл"""
        try:
            with open("highscore.dat", "w") as f:
                f.write(str(self.state.high_score))
        except:
            pass  # Игнорируем ошибки сохранения
    # === Конец блока Методы для работы с очками ===

    """ Определяет, должна ли игровая логика быть приостановлена. Возвращает True если открыто любое меню, диалог или игра завершена."""
    def should_pause_game_logic(self):

        return (self.state.game_paused or 
                self.state.show_minimap or 
                self.state.show_combined_dialog or
                self.state.show_exit_campaign_dialog or
                self.state.show_enter_campaign_dialog or
                self.active_menu_item is not None or
                self.show_overlay_text is not None or
                self.menu_open_with_keyboard or
                self.state.game_over or
                self.state.game_won or
                (self.state.game_mode == 'editor' and self.selected_tool is not None))

    def get_maze_dimensions(self):
        """Возвращает кэшированные размеры лабиринта в пикселях"""
        if self.cached_maze_dimensions is None:
            self.cached_maze_dimensions = (
                len(self.maze.grid[0]) * self.cell_size,
                len(self.maze.grid) * self.cell_size
            )
        return self.cached_maze_dimensions
    
    def invalidate_maze_cache(self):
        """Сбрасывает кэш размеров лабиринта"""
        self.cached_maze_dimensions = None

    # === Обновление иконки стены сбоку !!!
    def update_wall_icon(self):
        """Обновление иконки стены в UI панели"""
        # Берем текущий стиль стены
        wall_image = self.resource_manager.original_images.get(self.current_wall_image)
        if wall_image is None:
            wall_image = self.resource_manager.original_images.get('wall', pygame.Surface((32, 32)))
        
        # Масштабируем под размер иконки
        icon_scale_factor = 1.0 / 3.0
        scaled_icon_size = int(GameConfig.ORIGINAL_UI_PANEL_WIDTH * 0.8 * icon_scale_factor * self.state.scale_factor)
        
        # Обновляем иконку в editor_ui_icons
        self.resource_manager.editor_ui_icons['wall'] = pygame.transform.scale(
            wall_image, 
            (scaled_icon_size, scaled_icon_size)
        )
        
        # Очищаем кэш масштабированных иконок для стены
        cache_keys = [key for key in self.resource_manager.scaled_images.keys() if key.startswith('icon_wall_')]
        for key in cache_keys:
            del self.resource_manager.scaled_images[key]


    # === Стили стены по кругу !!! ===
    def cycle_wall_style(self, direction=1):
        """
        Переключение стиля стены по кругу
        direction: 1 - вперед, -1 - назад
        """
        # Получаем все доступные стили стен 
        wall_styles = []
        for i in range(1, 34): # стены wall1.png, wall2.png, wall3.png, ...
            key = f'wall{i}'
            if key in self.resource_manager.scaled_images:
                wall_styles.append(key)
        
        # Добавляем стандартную стену как запасной вариант
        if 'wall' in self.resource_manager.scaled_images and 'wall' not in wall_styles:
            wall_styles.append('wall')
        
        if not wall_styles:
            self.set_editor_message("No wall styles available!")
            return
        
        # Находим текущий индекс
        try:
            current_index = wall_styles.index(self.current_wall_image)
        except ValueError:
            current_index = -1
        
        # Переключаем
        next_index = (current_index + direction) % len(wall_styles)
        self.current_wall_image = wall_styles[next_index]

        # === ОБНОВЛЯЕМ ИКОНКУ В МЕНЮ !!! ===
        self.update_wall_icon()
        
        # Показываем номер стиля (например: "Wall: 3/8")
        style_num = next_index + 1
        total_styles = len(wall_styles)
        self.set_editor_message(f"Wall: {style_num}/{total_styles}")

    # Создайте метод для анимации победы
    def start_win_animation(self):
        """Запуск анимации победы"""
        self.win_animation_time = time.time()
        self.win_particles = []

        # Воспроизводим звук победы
        if self.sound_enabled and self.resource_manager.sounds.get('victory'):
            pygame.mixer.stop()  # Останавливаем другие звуки
            self.resource_manager.sounds['victory'].play()

        # Создаем частицы для анимации
        for _ in range(50):
            particle = {
                'x': random.randint(0, self.visible_maze_width),
                'y': random.randint(0, self.config.SCREEN_HEIGHT),
                'size': random.randint(2, 8),
                'speed_x': random.uniform(-3, 3),
                'speed_y': random.uniform(-5, -1),
                'color': random.choice([
                    self.config.YELLOW, 
                    self.config.WHITE, 
                    self.config.RED, 
                    self.config.BLUE,
                    self.config.PURPLE
                ]),
                'time': random.uniform(1.0, 3.0)
            }
            self.win_particles.append(particle)

    """Обновление анимации победы"""
    def update_win_animation(self):
        current_time = time.time()
        elapsed = current_time - self.win_animation_time
        
        # Обновляем частицы
        for particle in self.win_particles[:]:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['time'] -= 0.016  # примерно 60 FPS
            
            # Гравитация
            particle['speed_y'] += 0.1
            
            # Удаляем "мертвые" частицы
            if particle['time'] <= 0:
                self.win_particles.remove(particle)
        
        # Добавляем новые частицы, если анимация еще идет
        if elapsed < self.win_animation_duration and len(self.win_particles) < 50:
            if random.random() < 0.3:  # 30% шанс добавить новую частицу
                particle = {
                    'x': random.randint(0, self.visible_maze_width),
                    'y': self.config.SCREEN_HEIGHT,  # появляются снизу
                    'size': random.randint(2, 6),
                    'speed_x': random.uniform(-2, 2),
                    'speed_y': random.uniform(-8, -4),
                    'color': random.choice([self.config.YELLOW, self.config.WHITE]),
                    'time': random.uniform(1.0, 2.0)
                }
                self.win_particles.append(particle)
        
        return elapsed < self.win_animation_duration

    def initialize(self):
        """Инициализация игры"""
        pygame.display.set_caption("-=MaziacsAs=- WASD or Arrows(Up,Down,Left,Right)-Move/Navigation,Tab-Map/Edit,Alt-Menu,Space-Pause,Esc-Return,Enter-Select")
        
        # Устанавливаем начальный масштаб
        base_width = 1280
        base_height = 720
        width_scale = self.config.SCREEN_WIDTH / base_width
        height_scale = self.config.SCREEN_HEIGHT / base_height
        self.state.scale_factor = min(width_scale, height_scale)
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT), pygame.RESIZABLE) # создаем окно (инициализируем видео режим)

        # === ЗАМЕНА ЯРЛЫКА pygame НА icon.png ===
        game_icon = pygame.image.load(resource_path("icon.png"))
        pygame.display.set_icon(game_icon)
        # ============================================

        self.resource_manager.load_all_images() # загружаем ресурсы (после инициализации видео режима)
        self.resource_manager.load_sounds()
        # И только потом обновляем размеры
        self.update_dimensions() # в методе есть сброс кэш
        self.reset_game(keep_wall_style=False) # в методе есть сброс кэш

    def update_dimensions(self):
        """Обновление размеров элементов (без создания окна)"""
        self.cell_size = int(self.config.ORIGINAL_CELL_SIZE * self.state.scale_factor)
        self.info_panel_height = int(self.config.ORIGINAL_INFO_PANEL_HEIGHT * self.state.scale_factor)
        self.ui_panel_width = int(self.config.ORIGINAL_UI_PANEL_WIDTH * 1.5 * self.state.scale_factor)
        self.cached_maze_dimensions = None # Сбрасываем кэш при изменении размеров
        self.visible_maze_width = self.config.SCREEN_WIDTH - self.ui_panel_width
        self.visible_maze_height = self.config.SCREEN_HEIGHT - self.info_panel_height

        # Создаем поверхность один раз
        self.labyrinth_surface = pygame.Surface((self.visible_maze_width, self.visible_maze_height)).convert()

        # Создание шрифтов
        self.fonts = {
            'text': pygame.font.Font(None, int(self.cell_size * 2)),
            'char': pygame.font.Font(None, int(self.cell_size)),
            'info': pygame.font.Font(None, int(24 * self.state.scale_factor)),
            'ui_header': pygame.font.Font(None, int(30 * self.state.scale_factor)),
            'menu': pygame.font.Font(None, int(28 * self.state.scale_factor))
        }

        # Масштабирование изображений
        self.resource_manager.scale_images(self.cell_size, self.state.scale_factor)

        # === ОБНОВЛЯЕМ ИКОНКУ СТЕНЫ В СООТВЕТСТВИИ С ТЕКУЩИМ СТИЛЕМ !!! ===
        self.update_wall_icon()
        
        # === СБРОС UI RECTS ПРИ ИЗМЕНЕНИИ РАЗМЕРОВ ===
        if hasattr(self, 'editor_ui_rects'):
            self.editor_ui_rects = {}
        if hasattr(self, 'game_ui_rects'):
            self.game_ui_rects = {}

    def update_ui_text_cache(self):
        """Обновление кэша UI текстов при изменении масштаба"""
        if self.last_cached_scale == self.state.scale_factor:
            return

        self.last_cached_scale = self.state.scale_factor
        self.ui_text_cache.clear()

        # Кэшируем статические тексты
        static_texts = {
            'wall': "Wall",
            'path': "Path", 
            'sword': "Sword",
            'time': "Time",
            'pointer': "Pointer", 
            'spider': "Spider",
            'treasure': "Treasure",
            'house': "House",
            'save_map': "Save Map",
            'load_map': "Load Map",
            'check_map': "Check Map",
            'save_game': "Save Game", 
            'load_game': "Load Game"
        }
        
        for key, text in static_texts.items():
            self.ui_text_cache[key] = self.fonts['info'].render(text, True, self.config.WHITE)

    # === ДОБАВИТЬ ЗВУК взятия предмета ===
    def play_take_sound(self):
        """Воспроизведение звука взятия предмета"""
        if self.sound_enabled and self.resource_manager.sounds.get('take'):
            take_channel = pygame.mixer.Channel(4)  # Используем отдельный канал
            take_channel.play(self.resource_manager.sounds['take'])

    def resize_window(self, width, height):
        """Изменение размеров окна с автоматическим масштабированием"""
        min_width, min_height = 800, 600
        width = max(width, min_width)
        height = max(height, min_height)
        
        # Обновляем размеры в конфиге
        self.config.SCREEN_WIDTH = width
        self.config.SCREEN_HEIGHT = height
        
        # Вычисляем масштаб
        base_width = 1280
        base_height = 720
        width_scale = width / base_width
        height_scale = height / base_height
        self.state.scale_factor = min(width_scale, height_scale)
        self.state.scale_factor = max(0.5, min(2.0, self.state.scale_factor))
        
        # ОБНОВЛЯЕМ существующее окно (не создаем новое)
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        
        # Обновляем размеры. ВНУТРИ ЭТОГО МЕТОДА УЖЕ ЕСТЬ сброс кэш
        self.update_dimensions()

    # === Начало блока - МЕТОДЫ save load game map ===
    def _get_common_map_data(self):
        """Сбор общих данных карты для сохранения (используется и в map, и в game)"""
        return {
            'maze': self.maze.grid,
            'swords': self.maze.swords_positions,
            'times': self.maze.times_positions,
            'pointers': self.maze.path_pointers_positions,
            'spiders': [{'x': h.x, 'y': h.y, 'defeated': h.defeated} for h in self.maze.spiders],
            'treasure': self.maze.treasure_position,
            'difficulty_level': self.current_difficulty,
            'difficulty_name': DIFFICULTY_LEVELS[self.current_difficulty]['NAME'],
            'extra_paths': list(getattr(self.maze, 'extra_paths', set())),
            # Позиция дома и игрока часто совпадают при старте карты
            'house_position': (self.config.HOUSE_X, self.config.HOUSE_Y),
            # ДОБАВИТЬ: информацию о группе мечей у дома
            'house_sword_position': getattr(self.maze, 'house_sword_position', None),
            'house_swords_count': getattr(self.maze, 'house_swords_count', 0),
            # === ДОБАВЛЯЕМ СОХРАНЕНИЕ ТЕКУЩЕЙ СТЕНЫ ===
            'wall_image': self.current_wall_image
        }

    def _restore_common_map_data(self, data):
        """Восстановление общих данных карты (используется и в map, и в game)"""
        # 1. Восстановление настроек сложности и пересоздание лабиринта
        if 'difficulty_level' in data:
            self.current_difficulty = data['difficulty_level']
            diff_params = DIFFICULTY_LEVELS[self.current_difficulty]
            
            self.config.MAZE_WIDTH = diff_params['MAZE_WIDTH']
            self.config.MAZE_HEIGHT = diff_params['MAZE_HEIGHT']
            self.config.time_TIMER_MAX = diff_params['time_TIMER_MAX']
            self.config.time_BONUS_TIME = diff_params['time_BONUS_TIME']
            
            self.spider_speed = diff_params['spider_SPEED']

            self.maze = Maze(self.config.MAZE_WIDTH, self.config.MAZE_HEIGHT)

        # 2. Загрузка списков
        self.maze.grid = data['maze']
        self.maze.swords_positions = [tuple(pos) for pos in data['swords']]
        self.maze.times_positions = [tuple(pos) for pos in data['times']]
        self.maze.path_pointers_positions = [tuple(pos) for pos in data['pointers']]
        self.maze.treasure_position = tuple(data['treasure']) if data['treasure'] else None
        self.maze.extra_paths = set(tuple(pos) for pos in data['extra_paths'])
        
        # 3. ВОССТАНОВЛЕНИЕ МНОЖЕСТВ (Критически важно!)
        self.maze.swords_set = set(self.maze.swords_positions)
        self.maze.time_set = set(self.maze.times_positions)
        self.maze.pointers_set = set(self.maze.path_pointers_positions)

        # 4. Восстановление пауков
        self.maze.spiders = []
        for h_data in data['spiders']:
            x, y = h_data['x'], h_data['y']
            if 0 <= x < len(self.maze.grid) and 0 <= y < len(self.maze.grid[0]):
                spider_enemy = SpiderEnemy(x, y)
                spider_enemy.defeated = h_data.get('defeated', False)
                self.maze.spiders.append(spider_enemy)

        # 5. Позиция дома
        if 'house_position' in data:
             self.config.HOUSE_X, self.config.HOUSE_Y = data['house_position']

        # 6. Восстановление группы мечей у дома
        if 'house_sword_position' in data and data['house_sword_position'] is not None:
            self.maze.house_sword_position = tuple(data['house_sword_position'])
            self.maze.house_swords_count = data.get('house_swords_count', 0)
        else:
            # Если нет в сохранении - сбрасываем
            self.maze.house_sword_position = None
            self.maze.house_swords_count = 0

        # === ВОССТАНАВЛИВАЕМ СТЕНУ !!! ===
        if 'wall_image' in data:
            if data['wall_image'] in self.resource_manager.scaled_images:
                self.current_wall_image = data['wall_image']
            else:
                # Если стена не найдена - переключаем на следующую
                self.cycle_wall_style(1)
        else:
            # Если нет в сохранении - переключаем на следующую
            self.cycle_wall_style(1)            
        # ====================================== 

        self.cached_maze_dimensions = None # Сброс кэша

    def _save_to_json(self, filename, data, success_message):
        """Универсальное сохранение в JSON"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2) # indent=2 меньше занимает места чем 4
            self.set_editor_message(success_message)
            return True
        except Exception as e:
            self.set_editor_message(f"Save failed: {e}")
            return False

    def _load_from_json(self, filename):
        """Универсальная загрузка из JSON"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.set_editor_message(f"File not found: {filename}")
        except Exception as e:
            self.set_editor_message(f"Load failed: {e}")
        return None

    def save_map(self, filename='map_1.map'):
        """Сохранение карты (оптимизированное)"""
        if not filename.endswith('.map'):
            filename += '.map'
            
        # Получаем общие данные и добавляем специфичные для карты
        map_data = self._get_common_map_data()
        map_data['player_start'] = (self.config.HOUSE_X, self.config.HOUSE_Y)
        
        self._save_to_json(filename, map_data, f"Map saved: {filename}")

    def save_game_state(self, filename='game_1.save'):
        """Сохранение игры (оптимизированное)"""
        if not filename.endswith('.save'):
            filename += '.save'
            
        # Получаем общие данные
        game_data = self._get_common_map_data()
        
        # Добавляем специфичные данные состояния игры
        game_data.update({
            'game_mode': self.state.game_mode,
            'player': {
                'x': self.player.x,
                'y': self.player.y,
                'has_sword': self.player.has_sword,
                'has_treasure': self.player.has_treasure,
                'direction': self.player.direction,
            },
            'game_state': {
                'game_over': self.state.game_over,
                'game_won': self.state.game_won,
                'game_paused': self.state.game_paused,
                'show_death_image': self.state.show_death_image,
                'show_path': self.state.show_path,
                'path_hide_time': self.state.path_hide_time,
                'time_timer': self.state.time_timer,
                'timer_active': self.state.timer_active,
                'current_score': self.state.current_score,
                'total_score': self.state.total_score,
                'maps_completed': self.state.maps_completed,
                'campaign_mode': self.state.campaign_mode,
                'campaign_level': self.state.campaign_level,
                'campaign_wins': self.state.campaign_wins,
                'campaign_completed': self.state.campaign_completed,
            }
        })
        
        return self._save_to_json(filename, game_data, f"Game saved: {filename}")

    def load_map(self, filename='map_1.map'):
        """Загрузка карты (оптимизированная)"""
        if not filename.endswith('.map'):
            filename += '.map'
            
        data = self._load_from_json(filename)
        if not data: return False

        # Восстанавливаем лабиринт и предметы (общая логика)
        self._restore_common_map_data(data)
        
        # Специфика карты: ставим игрока на старт
        if 'player_start' in data:
            self.player.x, self.player.y = data['player_start']
        else:
            self.player.x, self.player.y = self.config.HOUSE_X, self.config.HOUSE_Y

        # # === ВОССТАНАВЛИВАЕМ СТЕНУ (если не восстановилась в _restore_common_map_data) ===
        # if 'wall_image' in data:
        #     if data['wall_image'] in self.resource_manager.scaled_images:
        #         self.current_wall_image = data['wall_image']
        #     else:
        #         self.current_wall_image = self.get_random_wall_image()
        # else:
        #     self.current_wall_image = self.get_random_wall_image()

        # === ВОССТАНАВЛИВАЕМ СТЕНУ ===
        if 'wall_image' in data:
            if data['wall_image'] in self.resource_manager.scaled_images:
                self.current_wall_image = data['wall_image']
            else:
                self.cycle_wall_style(1)  # Вместо get_random_wall_image()
        else:
            self.cycle_wall_style(1)  # Вместо get_random_wall_image()

        # =================================================================================
            
        self.set_editor_message(f"Map loaded: {filename}")
        return True

    def load_game_state(self, filename='game_1.save'):
        """Загрузка игры (оптимизированная)"""
        if not filename.endswith('.save'):
            filename += '.save'

        data = self._load_from_json(filename)
        if not data: return False
        
        if 'player' not in data or 'game_state' not in data:
            self.set_editor_message(f"Error: Invalid save file structure")
            return False

        # Восстанавливаем лабиринт и предметы (общая логика)
        self._restore_common_map_data(data)

        # Восстанавливаем специфику сохранения (игрок и состояние)
        p_data = data['player']
        self.player.x = p_data['x']
        self.player.y = p_data['y']
        self.player.has_sword = p_data['has_sword']
        self.player.has_treasure = p_data['has_treasure']
        self.player.direction = p_data['direction']
        
        # Сброс движения
        self.player.is_moving = False
        self.player.current_frame_index = 0
        self.mouse_move_target = None
        self.mouse_move_path = []
        
        s_data = data['game_state']
        self.state.game_over = s_data['game_over']
        self.state.game_won = s_data['game_won']
        self.state.game_paused = s_data['game_paused']
        self.state.show_death_image = s_data['show_death_image']
        self.state.show_path = s_data['show_path']
        self.state.path_hide_time = s_data['path_hide_time']
        self.state.time_timer = s_data['time_timer']
        self.state.timer_active = s_data.get('timer_active', False)
        self.state.last_second_time = time.time()
        self.state.current_score = s_data.get('current_score', 0)
        self.state.total_score = s_data.get('total_score', 0)
        self.state.maps_completed = s_data.get('maps_completed', 0)
        self.state.campaign_mode = s_data.get('campaign_mode', False)
        self.state.campaign_level = s_data.get('campaign_level', 1)
        self.state.campaign_wins = s_data.get('campaign_wins', 0)
        self.state.campaign_completed = s_data.get('campaign_completed', False)
        self.state.game_mode = data.get('game_mode', 'game')

        # === ВОССТАНАВЛИВАЕМ СТЕНУ !!! ===
        if 'wall_image' in data:
            if data['wall_image'] in self.resource_manager.scaled_images:
                self.current_wall_image = data['wall_image']
            else:
                self.cycle_wall_style(1)  # Вместо get_random_wall_image()
        else:
            self.cycle_wall_style(1)  # Вместо get_random_wall_image()
        # ================================================================================= 
        
        self.update_dimensions()

        # Формирование сообщения
        msg = f"Game loaded: {filename}"
        if self.state.campaign_mode:
            level_name = self.get_level_name(self.state.campaign_level)
            msg += f" | Campaign: {level_name}"
        else:
            msg += f" | Free Play"
        self.set_editor_message(msg)
        return True
    # === Конец блока - МЕТОДЫ save load game map ===

    def get_file_list(self, file_type):
        """Получение списка файлов определенного типа"""
        try:
            files = []
            for filename in os.listdir(self.state.current_directory):
                if filename.endswith(file_type):
                    file_path = os.path.join(self.state.current_directory, filename)
                    file_size = os.path.getsize(file_path)
                    files.append({
                        'name': filename,
                        'size': file_size,
                        'full_path': file_path
                    })
            
            # Сортируем по имени
            files.sort(key=lambda x: x['name'].lower())
            return files
        except Exception as e:
            print(f"Error reading directory: {e}")
            return []

    def refresh_file_list(self):
        """Обновление списка файлов в зависимости от режима"""
        if self.state.combined_dialog_mode in ['save_map', 'load_map']:
            self.state.file_list = self.get_file_list('.map')
        elif self.state.combined_dialog_mode in ['save_game', 'load_game']:
            self.state.file_list = self.get_file_list('.save')
        self.state.selected_file_index = 0

    def show_combined_dialog(self, mode):
        """Показать комбинированный диалог с списком файлов и полем ввода"""
        self.state.show_combined_dialog = True
        self.state.combined_dialog_mode = mode
        self.state.game_paused = True
        self.state.combined_filename_input = ""
        self.state.file_list_scroll = 0
        self.refresh_file_list()
   
    def get_visible_file_items_count(self):
        """Получить количество видимых файлов в списке с учетом масштаба"""
        dialog_rect = self.get_combined_dialog_rect()
        list_height = dialog_rect.height - int(220 * self.state.scale_factor)
        file_item_height = int(25 * self.state.scale_factor)
        return max(1, list_height // file_item_height)

    def handle_combined_dialog_events(self, event):
        """Обработка событий в комбинированном диалоге"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close_all_interfaces_and_resume()
                return True
            
            elif event.key == pygame.K_DELETE:  # ПРОСТОЕ УДАЛЕНИЕ
                if self.state.file_list and 0 <= self.state.selected_file_index < len(self.state.file_list):
                    selected_file = self.state.file_list[self.state.selected_file_index]
                    try:
                        os.remove(selected_file['full_path'])
                        self.refresh_file_list()  # Обновляем список
                        # Корректируем индекс
                        if self.state.selected_file_index >= len(self.state.file_list):
                            self.state.selected_file_index = max(0, len(self.state.file_list) - 1)
                        self.dialog_error_message = f"Deleted: {selected_file['name']}"
                        self.dialog_error_time = time.time()
                    except Exception as e:
                        self.dialog_error_message = f"Delete failed: {e}"
                        self.dialog_error_time = time.time()
                    return True
                
            elif event.key == pygame.K_RETURN:
                # Если в поле ввода пусто - копируем выбранный файл
                if not self.state.combined_filename_input.strip() and self.state.file_list:
                    if self.state.selected_file_index < len(self.state.file_list):
                        selected_file = self.state.file_list[self.state.selected_file_index]
                        filename_without_ext = os.path.splitext(selected_file['name'])[0]
                        self.state.combined_filename_input = filename_without_ext
                    return True
                else:
                    # Если в поле ввода есть текст - подтверждаем действие
                    filename = self.state.combined_filename_input.strip()
                    if filename:
                        self.process_combined_dialog_action(filename)
                    return True
                
            elif event.key == pygame.K_UP:
                if self.state.file_list:
                    self.state.selected_file_index = max(0, self.state.selected_file_index - 1)
                    # Автопрокрутка при навигации клавишами
                    visible_items = self.get_visible_file_items_count()
                    if self.state.selected_file_index < self.state.file_list_scroll:
                        self.state.file_list_scroll = self.state.selected_file_index
                    elif self.state.selected_file_index >= self.state.file_list_scroll + visible_items:
                        self.state.file_list_scroll = self.state.selected_file_index - visible_items + 1
                return True
                
            elif event.key == pygame.K_DOWN:
                if self.state.file_list:
                    self.state.selected_file_index = min(len(self.state.file_list) - 1, self.state.selected_file_index + 1)
                    # Автопрокрутка при навигации клавишами
                    visible_items = self.get_visible_file_items_count()
                    if self.state.selected_file_index < self.state.file_list_scroll:
                        self.state.file_list_scroll = self.state.selected_file_index
                    elif self.state.selected_file_index >= self.state.file_list_scroll + visible_items:
                        self.state.file_list_scroll = self.state.selected_file_index - visible_items + 1
                return True
                
            elif event.key == pygame.K_BACKSPACE:
                self.state.combined_filename_input = self.state.combined_filename_input[:-1]
                return True

            # Ввод текста - ОГРАНИЧЕНИЕ ДО 8 СИМВОЛОВ
            elif event.unicode and event.unicode.isprintable():
                # Проверяем режим диалога и ограничиваем длину для save_map и save_game
                if (self.state.combined_dialog_mode in ['save_map', 'save_game'] and 
                    len(self.state.combined_filename_input) >= 16):
                    return True  # Игнорируем ввод если уже 16 символов
                self.state.combined_filename_input += event.unicode
                return True

        # === ОБЪЕДИНЕННЫЙ ОБРАБОТЧИК МЫШИ ===
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            dialog_rect = self.get_combined_dialog_rect()
            
            # Если кликнули ВНЕ диалога - закрываем его
            if not dialog_rect.collidepoint(mouse_pos):
                self.close_all_interfaces_and_resume()
                return True
            
            # Обработка кликов по списку файлов с учетом масштаба
            # Координаты списка файлов с масштабированием
            list_rect = pygame.Rect(
                dialog_rect.x + int(30 * self.state.scale_factor),
                dialog_rect.y + int(140 * self.state.scale_factor),
                dialog_rect.width - int(60 * self.state.scale_factor),
                dialog_rect.height - int(220 * self.state.scale_factor)
            )
            
            if list_rect.collidepoint(mouse_pos):
                file_item_height = int(25 * self.state.scale_factor)
                relative_y = mouse_pos[1] - list_rect.y
                clicked_index = relative_y // file_item_height + self.state.file_list_scroll
                
                if 0 <= clicked_index < len(self.state.file_list):
                    self.state.selected_file_index = clicked_index
                    # Автоматически копируем выбранный файл в поле ввода
                    selected_file = self.state.file_list[clicked_index]
                    filename_without_ext = os.path.splitext(selected_file['name'])[0]
                    self.state.combined_filename_input = filename_without_ext
                return True
            
            # Если кликнули внутри диалога, но не по списку файлов - не закрываем диалог
            return True
            
        # Обработка колесика мыши (для совместимости)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5):
                if self.state.show_combined_dialog:
                    scroll_amount = -1 if event.button == 4 else 1
                    visible_items = self.get_visible_file_items_count()
                    max_scroll = max(0, len(self.state.file_list) - visible_items)
                    self.state.file_list_scroll = max(0, min(self.state.file_list_scroll + scroll_amount * 3, max_scroll))
                    return True
        
        elif event.type == pygame.MOUSEWHEEL:
            # Прокрутка колесиком мыши
            if self.state.show_combined_dialog:
                visible_items = self.get_visible_file_items_count()
                max_scroll = max(0, len(self.state.file_list) - visible_items)
                self.state.file_list_scroll = max(0, min(self.state.file_list_scroll - event.y, max_scroll))
                return True
        
        # ДОБАВЛЕННЫЙ БЛОК ДЛЯ ВЫДЕЛЕНИЯ ПРИ ДВИЖЕНИИ МЫШИ
        elif event.type == pygame.MOUSEMOTION:
            # Обработка движения мыши над списком файлов
            mouse_pos = pygame.mouse.get_pos()
            dialog_rect = self.get_combined_dialog_rect()
            
            # Координаты списка файлов с масштабированием
            list_rect = pygame.Rect(
                dialog_rect.x + int(30 * self.state.scale_factor),
                dialog_rect.y + int(140 * self.state.scale_factor),
                dialog_rect.width - int(60 * self.state.scale_factor),
                dialog_rect.height - int(220 * self.state.scale_factor)
            )
            
            if list_rect.collidepoint(mouse_pos):
                file_item_height = int(25 * self.state.scale_factor)
                relative_y = mouse_pos[1] - list_rect.y
                hover_index = relative_y // file_item_height + self.state.file_list_scroll
                
                if 0 <= hover_index < len(self.state.file_list):
                    self.state.selected_file_index = hover_index
            return True
            
        return False

    def process_combined_dialog_action(self, filename):
        """Обработка действия в комбинированном диалоге"""
        if self.state.combined_dialog_mode == 'save_map':
            self.save_map(filename + ".map")
            self.close_all_interfaces_and_resume()
            
        elif self.state.combined_dialog_mode == 'load_map':

            # === ПАСХАЛЬНОЕ ЯЙЦО: GOD MODE ===
            # Безопасная проверка с учетом типов
            if filename and isinstance(filename, str):
                filename_lower = filename.lower().strip()
                
                # Включение
                if filename_lower in ["god mode on", "godmodeon", "god on", "gmon"]:
                    self.state.time_timer_enabled = False
                    self.state.god_mode = True
                    self.player.has_sword = True
                    self.state.current_score += 100
                    self.close_all_interfaces_and_resume()
                    return
                
                # Выключение
                elif filename_lower in ["god mode off", "godmodeoff", "god off", "gmoff"]:
                    self.state.time_timer_enabled = True
                    self.state.god_mode = False
                    self.close_all_interfaces_and_resume()
                    return
                
                # Переключение
                elif filename_lower == "god":
                    self.state.god_mode = not self.state.god_mode
                    if self.state.god_mode:
                        self.state.time_timer_enabled = False
                    else:
                        self.state.time_timer_enabled = True
                    self.close_all_interfaces_and_resume()
                    return
            # === КОНЕЦ ПАСХАЛЬНОГО ЯЙЦА ===

            full_filename = filename + ".map"
            if not os.path.exists(full_filename):
                self.dialog_error_message = f"No file: {full_filename}"
                self.dialog_error_time = time.time()
            else:
                result = self.reset_game(full_filename, keep_wall_style=False)
                if result == "OK":
                    self.set_editor_message(f"Map: {filename} loaded")
                    self.close_all_interfaces_and_resume()
                else:
                    self.dialog_error_message = f"Failed to load: {full_filename}"
                    self.dialog_error_time = time.time()
                    
        elif self.state.combined_dialog_mode == 'save_game':
            success = self.save_game_state(filename + ".save")
            if success:
                self.close_all_interfaces_and_resume()
                    
        elif self.state.combined_dialog_mode == 'load_game':
            full_filename = filename + ".save"
            if not os.path.exists(full_filename):
                self.dialog_error_message = f"No file: {full_filename}"
                self.dialog_error_time = time.time()
            else:
                success = self.load_game_state(full_filename)
                if success:
                    self.close_all_interfaces_and_resume()
                else:
                    self.dialog_error_message = f"Failed to load: {full_filename}"
                    self.dialog_error_time = time.time()

    def close_all_interfaces_and_resume(self, current_time=None, keep_space_pause=False):
        """Закрывает ВСЕ меню, диалоги и снимает паузу"""
        if current_time is None:
            current_time = time.time()
        
        # Закрываем ВСЕ диалоги
        self.state.show_combined_dialog = False
        self.state.combined_dialog_mode = None
        self.state.combined_filename_input = ""
        self.state.show_exit_campaign_dialog = False
        self.state.show_enter_campaign_dialog = False
        
        # Сбрасываем сообщения об ошибках диалогов
        if hasattr(self, 'dialog_error_message'):
            self.dialog_error_message = None
        
        # Закрываем ВСЕ меню
        self.active_menu_item = None
        self.menu_open_with_keyboard = False
        self.show_overlay_text = None

        # Снимаем паузу и корректируем таймер
        if self.state.game_paused:
            # Сохраняем тип паузы по пробелу если нужно
            if keep_space_pause and self.state.pause_type == 'space_pause':
                # Не сбрасываем паузу по пробелу
                pass
            else:
                if self.state.pause_start_time:
                    pause_duration = current_time - self.state.pause_start_time
                    self.state.last_timer_update += pause_duration
                    self.state.pause_start_time = None
                self.state.game_paused = False
                self.state.pause_type = None

    def draw_combined_dialog(self):
        """Отрисовка комбинированного диалога с списком файлов и полосой прокрутки"""
        dialog_width = int(700 * self.state.scale_factor)
        dialog_height = int(500 * self.state.scale_factor)
        dialog_x = (self.config.SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (self.config.SCREEN_HEIGHT - dialog_height) // 2

        # Фон диалога
        dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
        dialog_surface.fill((0, 0, 0, 230))
        pygame.draw.rect(dialog_surface, self.config.WHITE, (0, 0, dialog_width, dialog_height), 2)

        # Заголовок
        mode_titles = {
            'save_map': "SAVE MAP - Select file or enter new name",
            'load_map': "LOAD MAP - Select file or enter name", 
            'save_game': "SAVE GAME - Select file or enter new name",
            'load_game': "LOAD GAME - Select file or enter name"
        }

        title = mode_titles.get(self.state.combined_dialog_mode, "File Dialog")
        title_text = self.fonts['menu'].render(title, True, self.config.WHITE)
        title_rect = title_text.get_rect(center=(dialog_width // 2, int(30 * self.state.scale_factor)))
        dialog_surface.blit(title_text, title_rect)

        # Поле ввода имени файла
        input_label = self.fonts['info'].render("File name:", True, self.config.WHITE)
        dialog_surface.blit(input_label, (int(30 * self.state.scale_factor), int(60 * self.state.scale_factor)))

        input_rect = pygame.Rect(
            int(150 * self.state.scale_factor),
            int(55 * self.state.scale_factor),
            dialog_width - int(180 * self.state.scale_factor),
            int(30 * self.state.scale_factor)
        )
        pygame.draw.rect(dialog_surface, self.config.WHITE, input_rect, 1)

        # Текст в поле ввода
        input_text = self.fonts['info'].render(self.state.combined_filename_input, True, self.config.WHITE)
        dialog_surface.blit(input_text, (input_rect.x + 5, input_rect.y + 5))

        # Мигающий курсор
        if int(time.time() * 2) % 2 == 0:
            cursor_x = input_rect.x + 5 + input_text.get_width()
            cursor_rect = pygame.Rect(cursor_x, input_rect.y + 5, 2, input_rect.height - 10)
            pygame.draw.rect(dialog_surface, self.config.WHITE, cursor_rect)

        # Сообщение об ошибке (если есть)
        if (hasattr(self, 'dialog_error_message') and 
            hasattr(self, 'dialog_error_time') and 
            time.time() - self.dialog_error_time < 3):
            
            error_text = self.fonts['info'].render(self.dialog_error_message, True, self.config.RED)
            error_rect = error_text.get_rect(center=(dialog_width // 2, int(100 * self.state.scale_factor)))
            dialog_surface.blit(error_text, error_rect)

        # Список существующих файлов
        list_label = self.fonts['info'].render("Existing files:", True, self.config.WHITE)
        dialog_surface.blit(list_label, (int(30 * self.state.scale_factor), int(120 * self.state.scale_factor)))

        # Область списка файлов
        list_rect = pygame.Rect(
            int(30 * self.state.scale_factor),
            int(140 * self.state.scale_factor),
            dialog_width - int(60 * self.state.scale_factor),
            dialog_height - int(220 * self.state.scale_factor)
        )
        pygame.draw.rect(dialog_surface, (30, 30, 30), list_rect)
        pygame.draw.rect(dialog_surface, self.config.WHITE, list_rect, 1)

        # Параметры прокрутки
        file_item_height = int(25 * self.state.scale_factor)
        visible_items = list_rect.height // file_item_height
        total_items = len(self.state.file_list)

        # Вычисляем смещение прокрутки
        max_scroll = max(0, total_items - visible_items)
        if not hasattr(self.state, 'file_list_scroll'):
            self.state.file_list_scroll = 0

        # Ограничиваем прокрутку
        self.state.file_list_scroll = max(0, min(self.state.file_list_scroll, max_scroll))

        # Отображение файлов (только видимые)
        for i in range(visible_items):
            file_index = i + self.state.file_list_scroll
            if file_index >= total_items:
                break

            file_info = self.state.file_list[file_index]
            file_rect = pygame.Rect(
                list_rect.x + 5,
                list_rect.y + 5 + i * file_item_height,
                list_rect.width - 20,
                file_item_height
            )

            # Подсветка выбранного файла
            if file_index == self.state.selected_file_index:
                pygame.draw.rect(dialog_surface, self.config.BLUE, file_rect)
                pygame.draw.rect(dialog_surface, self.config.YELLOW, file_rect, 2)

            # Имя файла
            name_text = self.fonts['info'].render(file_info['name'], True, self.config.WHITE)
            dialog_surface.blit(name_text, (file_rect.x + 5, file_rect.y + 5))

            # Размер файла
            size_kb = file_info['size'] / 1024
            size_text = self.fonts['info'].render(f"{size_kb:.1f} KB", True, self.config.LIGHT_YELLOW)
            dialog_surface.blit(size_text, (file_rect.right - 120, file_rect.y + 5))

        # Полоса прокрутки (если нужно)
        if total_items > visible_items:
            scrollbar_width = int(10 * self.state.scale_factor)
            scrollbar_rect = pygame.Rect(
                list_rect.right - scrollbar_width - 2,
                list_rect.y + 2,
                scrollbar_width,
                list_rect.height - 4
            )

            pygame.draw.rect(dialog_surface, (80, 80, 80), scrollbar_rect) # Фон полосы прокрутки

            # Бегунок полосы прокрутки
            thumb_height = max(20, (visible_items / total_items) * scrollbar_rect.height)
            thumb_y = scrollbar_rect.y + (self.state.file_list_scroll / max_scroll) * (scrollbar_rect.height - thumb_height)
            thumb_rect = pygame.Rect(
                scrollbar_rect.x,
                thumb_y,
                scrollbar_rect.width,
                thumb_height
            )
            pygame.draw.rect(dialog_surface, self.config.WHITE, thumb_rect)

        # Подсказки
        hints = [
            "ARROWS Cursor or Mouse CLICK - Select file | or Keyboard Input Filename",
            "ENTER - Select and Apply | DELETE - Delete file | ESC - Cancel", 
            f"Files found: {len(self.state.file_list)} | Mouse WHEEL - Scroll"
        ]

        for j, hint in enumerate(hints):
            hint_text = self.fonts['info'].render(hint, True, self.config.YELLOW)
            hint_rect = hint_text.get_rect(center=(
                dialog_width // 2,
                dialog_height - int(60 * self.state.scale_factor) + j * int(20 * self.state.scale_factor)
            ))
            dialog_surface.blit(hint_text, hint_rect)

        self.screen.blit(dialog_surface, (dialog_x, dialog_y))

    def get_combined_dialog_rect(self):
        """Получение rect комбинированного диалога для обработки кликов"""
        dialog_width = int(700 * self.state.scale_factor)
        dialog_height = int(500 * self.state.scale_factor)
        dialog_x = (self.config.SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (self.config.SCREEN_HEIGHT - dialog_height) // 2
        return pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)

    def find_path_bfs(self, start, end_condition):
        """Поиск пути с помощью BFS (игрок может ходить через двери)"""
        grid = self.maze.grid
        rows, cols = len(grid), len(grid[0])
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            (pos, path) = queue.popleft()
            
            if end_condition(pos):
                return path

            x, y = pos
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy

                # Проверяем проходимость для ИГРОКА
                is_passable_for_player = (
                    0 <= nx < rows and 0 <= ny < cols and 
                    (grid[nx][ny] == 0 or  # обычный проход
                    (nx, ny) in getattr(self.maze, 'extra_paths', set()))  # дверь
                )

                if is_passable_for_player and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    new_path = list(path)
                    new_path.append((nx, ny))
                    queue.append(((nx, ny), new_path))

        return None

    def check_map_solvability(self):
        """Проверка проходимости карты"""
        if self.maze.treasure_position is None:
            return False

        # Проверяем, что у клада есть хотя бы одна проходимая клетка рядом
        tx, ty = self.maze.treasure_position
        has_adjacent_path = False
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (0 <= tx + dx < len(self.maze.grid) and 
                0 <= ty + dy < len(self.maze.grid[0]) and 
                self.maze.grid[tx + dx][ty + dy] == 0):
                has_adjacent_path = True
                break

        if not has_adjacent_path:
            return False

        # Поиск всех достижимых клеток
        rows, cols = len(self.maze.grid), len(self.maze.grid[0])
        queue = deque([(self.config.HOUSE_X, self.config.HOUSE_Y)])
        reachable_cells = {(self.config.HOUSE_X, self.config.HOUSE_Y)}

        while queue:
            (x, y) = queue.popleft()
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < rows and 0 <= ny < cols and self.maze.grid[nx][ny] == 0 and 
                    (nx, ny) not in reachable_cells):
                    reachable_cells.add((nx, ny))
                    queue.append((nx, ny))

        # Проверка доступности клада
        tx, ty = self.maze.treasure_position
        treasure_accessible = False
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            adj_pos = (tx + dx, ty + dy)
            if adj_pos in reachable_cells:
                treasure_accessible = True
                break

        if not treasure_accessible:
            return False

        # Подсчет доступных мечей и пауков
        accessible_swords = 0
        for sword_pos in self.maze.swords_positions:
            if (0 <= sword_pos[0] < rows and 0 <= sword_pos[1] < cols and 
                self.maze.grid[sword_pos[0]][sword_pos[1]] == 1 and 
                self.maze.is_adjacent_to_path(sword_pos)):
                accessible_swords += 1

        accessible_spiders = 0
        for spider in self.maze.spiders:
            if (spider.x, spider.y) in reachable_cells:
                accessible_spiders += 1

        # Проверка баланса мечей и пауков
        total_swords_available = 1 + accessible_swords
        return total_swords_available >= accessible_spiders

    def check_wall_interaction(self, dx, dy):
            """Проверка взаимодействия со стеной при попытке движения"""
            wall_pos = (self.player.x + dx, self.player.y + dy)

            # Проверяем, что позиция валидна и это стена (НЕ дверь)
            if (0 <= wall_pos[0] < len(self.maze.grid) and 
                0 <= wall_pos[1] < len(self.maze.grid[0]) and 
                self.maze.grid[wall_pos[0]][wall_pos[1]] == 1 and
                wall_pos not in getattr(self.maze, 'extra_paths', set())):  # НЕ дверь

                current_time = time.time()

                # Проверка задержки обмена
                if current_time - self.last_swap_time < self.swap_delay:
                    return False  # Задержка еще не прошла

                # Используем множества (set) для мгновенного поиска
                is_sword_at_wall = wall_pos in self.maze.swords_set
                is_treasure_at_wall = wall_pos == self.maze.treasure_position
                is_time_at_wall = wall_pos in self.maze.time_set
                is_pointer_at_wall = wall_pos in self.maze.pointers_set

                # ВЗАИМОДЕЙСТВИЯ С МЕЧОМ И КЛАДОМ
                if self.player.has_treasure and is_sword_at_wall:
                    self.player.has_treasure = False
                    self.player.has_sword = True
                    self.maze.swords_positions.remove(wall_pos) # Удаляем ОДИН меч из списка
                    # Удаляем из множества ТОЛЬКО если мечей в этом месте больше нет
                    if wall_pos not in self.maze.swords_positions:
                        self.maze.swords_set.discard(wall_pos)
                    self.maze.treasure_position = wall_pos
                    self.last_swap_time = current_time
                    self.play_take_sound()
                    return True

                elif self.player.has_sword and is_treasure_at_wall:
                    self.player.has_sword = False
                    self.player.has_treasure = True
                    self.maze.treasure_position = None
                    
                    # Возвращаем меч на стену
                    self.maze.swords_positions.append(wall_pos)
                    self.maze.swords_set.add(wall_pos)
                    
                    self.last_swap_time = current_time
                    self.play_take_sound()
                    return True

                elif not self.player.has_sword and not self.player.has_treasure and is_sword_at_wall:
                    self.player.has_sword = True
                    self.maze.swords_positions.remove(wall_pos) # Удаляем ОДИН меч из списка
                    # Удаляем из множества ТОЛЬКО если мечей в этом месте больше нет
                    if wall_pos not in self.maze.swords_positions:
                        self.maze.swords_set.discard(wall_pos)

                    self.last_swap_time = current_time
                    self.play_take_sound()
                    return True

                elif not self.player.has_sword and not self.player.has_treasure and is_treasure_at_wall:
                    self.player.has_treasure = True
                    self.maze.treasure_position = None
                    self.last_swap_time = current_time
                    self.play_take_sound()
                    return True

                if is_time_at_wall:
                    self.state.time_timer += self.config.time_BONUS_TIME
                    if self.state.time_timer > self.config.time_TIMER_MAX:
                        self.state.time_timer = self.config.time_TIMER_MAX
                    
                    self.maze.times_positions.remove(wall_pos)
                    if wall_pos not in self.maze.times_positions:
                        self.maze.time_set.discard(wall_pos)
                    
                    self.last_swap_time = current_time
                    self.play_take_sound()
                    return True

                if is_pointer_at_wall:
                    self.state.show_path = True
                    self.state.path_hide_time = time.time() + 10
                    self.last_swap_time = current_time
                    self.play_take_sound()
                    return True

            return False

    def generate_new_maze_and_items(self):
        """Генерация нового лабиринта и предметов с оптимизацией для больших размеров"""
        max_attempts = 10  # Ограничиваем количество попыток
        attempt = 0

        while attempt < max_attempts:
            attempt += 1
            print(f"Попытка генерации лабиринта {attempt}/{max_attempts}")

            try:
                # Генерируем лабиринт
                self.maze.generate()

                # Добавляем дополнительные проходы в зависимости от уровня сложности
                extra_paths = DIFFICULTY_LEVELS[self.current_difficulty]['EXTRA_PATHS']
                if extra_paths > 0:
                    # Для больших лабиринтов уменьшаем количество дополнительных путей
                    if self.maze.width > 100 or self.maze.height > 100:
                        extra_paths = min(extra_paths, extra_paths // 2)
                    self.maze.add_random_paths(extra_paths)

                # Оптимизированный сбор позиций с использованием генераторов
                all_path_positions = []
                all_wall_positions = []

                # Эффективный сбор позиций без создания огромных списков
                for r in range(self.maze.height):
                    for c in range(self.maze.width):
                        if self.maze.grid[r][c] == 0:
                            all_path_positions.append((r, c))
                        elif self.maze.grid[r][c] == 1 and self.maze.is_adjacent_to_path((r, c)):
                            all_wall_positions.append((r, c))

                # Проверяем минимальные требования
                if len(all_path_positions) < 10 or len(all_wall_positions) < 10:
                    continue

                # Удаляем позицию дома из доступных путей
                house_pos = (self.config.HOUSE_X, self.config.HOUSE_Y)
                if house_pos in all_path_positions:
                    all_path_positions.remove(house_pos)

                # Инициализация списков предметов и множеств
                self.maze.swords_positions = []
                self.maze.times_positions = []
                self.maze.path_pointers_positions = []
                self.maze.spiders = []
                
                # Инициализируем множества для быстрого поиска
                self.maze.swords_set = set()
                self.maze.time_set = set()
                self.maze.pointers_set = set()

                # Размещение клада на дальней стене
                max_possible_dist = self.maze.height + self.maze.width
                min_treasure_dist = max_possible_dist * 0.4  # Уменьшил для больших лабиринтов

                # Эффективный поиск дальних позиций
                far_wall_positions = []
                for pos in all_wall_positions:
                    dist = abs(pos[0] - house_pos[0]) + abs(pos[1] - house_pos[1])
                    if dist > min_treasure_dist:
                        far_wall_positions.append(pos)

                if not far_wall_positions: # Если нет дальних позиций, берем самые удаленные
                    all_wall_positions.sort(
                        key=lambda pos: abs(pos[0] - house_pos[0]) + abs(pos[1] - house_pos[1]), 
                        reverse=True
                    )
                    far_wall_positions = all_wall_positions[:min(10, len(all_wall_positions))]

                if not far_wall_positions:
                    continue

                self.maze.treasure_position = random.choice(far_wall_positions)

                # Создаем копии для безопасного удаления
                available_wall_positions = [pos for pos in all_wall_positions if pos != self.maze.treasure_position]
                available_path_positions = [
                    p for p in all_path_positions 
                    if abs(p[0] - self.config.HOUSE_X) + abs(p[1] - self.config.HOUSE_Y) > 3  # Уменьшил дистанцию
                ]

                # Перемешиваем позиции
                random.shuffle(available_wall_positions)
                random.shuffle(available_path_positions)

                # Получаем параметры из текущего уровня сложности
                spiders_count = DIFFICULTY_LEVELS[self.current_difficulty]['SPIDERS_COUNT']
                swords_count = DIFFICULTY_LEVELS[self.current_difficulty]['SWORDS_COUNT']
                time_count = DIFFICULTY_LEVELS[self.current_difficulty]['TIME_COUNT']
                pointers_count = DIFFICULTY_LEVELS[self.current_difficulty]['POINTERS_COUNT']
                house_swords_count = DIFFICULTY_LEVELS[self.current_difficulty]['HOUSE_SWORDS_COUNT']

                # Проверяем достаточно ли позиций
                required_walls = swords_count + time_count + pointers_count
                if house_swords_count > 0:
                    required_walls += 1  # +1 для группы мечей у дома

                if (len(available_wall_positions) < required_walls or 
                    len(available_path_positions) < spiders_count):
                    continue

                # Размещаем группу мечей рядом с домом
                house_sword_position = None
                house_neighbors = [
                    (self.config.HOUSE_X, self.config.HOUSE_Y + 1),   # справа
                    (self.config.HOUSE_X, self.config.HOUSE_Y - 1),   # слева  
                    (self.config.HOUSE_X + 1, self.config.HOUSE_Y),   # снизу
                    (self.config.HOUSE_X - 1, self.config.HOUSE_Y)    # сверху
                ]

                # Ищем подходящую позицию для группы мечей
                for pos in house_neighbors:
                    x, y = pos
                    if (0 <= x < self.maze.height and 
                        0 <= y < self.maze.width and 
                        self.maze.grid[x][y] == 1 and
                        pos in available_wall_positions):

                        house_sword_position = pos
                        # Добавляем группу мечей в одну позицию
                        for _ in range(house_swords_count):
                            self.maze.swords_positions.append(pos)
                            self.maze.swords_set.add(pos)  # добавляем в множество

                        # Удаляем эту позицию из доступных
                        if pos in available_wall_positions:
                            available_wall_positions.remove(pos)

                        break

                # Если не нашли подходящую позицию, создаем мечи в случайных местах
                if house_sword_position is None:
                    for _ in range(house_swords_count):
                        if available_wall_positions:
                            pos = available_wall_positions.pop()
                            self.maze.swords_positions.append(pos)
                            self.maze.swords_set.add(pos)  # добавляем в множество

                # Сохраняем информацию о группе мечей для отрисовки
                self.maze.house_sword_position = house_sword_position
                self.maze.house_swords_count = house_swords_count

                # Размещаем обычные мечи
                for _ in range(swords_count):
                    if available_wall_positions:
                        pos = available_wall_positions.pop()
                        self.maze.swords_positions.append(pos)
                        self.maze.swords_set.add(pos)  # добавляем в множество

                # Размещаем жизни
                for _ in range(time_count):
                    if available_wall_positions:
                        pos = available_wall_positions.pop()
                        self.maze.times_positions.append(pos)
                        self.maze.time_set.add(pos)  # добавляем в множество

                # Размещаем указатели
                for _ in range(pointers_count):
                    if available_wall_positions:
                        pos = available_wall_positions.pop()
                        self.maze.path_pointers_positions.append(pos)
                        self.maze.pointers_set.add(pos)  # добавляем в множество

                # Размещаем пауков
                for _ in range(spiders_count):
                    if available_path_positions:
                        pos = available_path_positions.pop()
                        self.maze.spiders.append(SpiderEnemy(pos[0], pos[1]))

                # Сбрасываем кэш
                self.cached_maze_dimensions = None

                # Проверяем проходимость карты
                if self.check_map_solvability():
                    self.player.x, self.player.y = self.config.HOUSE_X, self.config.HOUSE_Y
                    return

            except (IndexError, ValueError, MemoryError) as e:
                print(f"Ошибка при генерации: {e} - пробуем снова")
                continue

        # Если не удалось сгенерировать за max_attempts попыток
        self.create_fallback_maze()

    def create_fallback_maze(self):
        """Создание резервного лабиринта если основная генерация не удалась"""
        # Простой гарантированно проходимый лабиринт
        width = self.maze.width
        height = self.maze.height

        # Создаем простую сетку
        for i in range(height):
            for j in range(width):
                # Чередуем стены и проходы
                if i % 2 == 1 and j % 2 == 1:
                    self.maze.grid[i][j] = 0  # Основные клетки
                elif i == 0 or i == height - 1 or j == 0 or j == width - 1:
                    self.maze.grid[i][j] = 1  # Границы
                else:
                    self.maze.grid[i][j] = 1 if random.random() > 0.7 else 0

        # Гарантируем проход от дома
        self.maze.grid[1][1] = 0  # Дом
        self.maze.grid[1][2] = 0  # Выход из дома
        self.maze.grid[2][1] = 0  # Альтернативный выход

        # Инициализация списков и множеств
        self.maze.swords_positions = [(3, 3), (5, 5)]
        self.maze.times_positions = [(7, 7)]
        self.maze.path_pointers_positions = [(9, 9)]
        
        # Инициализируем множества
        self.maze.swords_set = set(self.maze.swords_positions)
        self.maze.time_set = set(self.maze.times_positions)
        self.maze.pointers_set = set(self.maze.path_pointers_positions)

        # Клад в противоположном углу
        treasure_x = min(height - 2, 10)
        treasure_y = min(width - 2, 10)
        self.maze.treasure_position = (treasure_x, treasure_y)

        # Несколько пауков
        self.maze.spiders = [
            SpiderEnemy(15 % height, 15 % width),
            SpiderEnemy(20 % height, 20 % width)
        ]

        # Группа мечей у дома
        self.maze.house_sword_position = (1, 2)
        self.maze.house_swords_count = 3
        for _ in range(3):
            self.maze.swords_positions.append((1, 2))
            self.maze.swords_set.add((1, 2))  # добавляем в множество

        self.player.x, self.player.y = self.config.HOUSE_X, self.config.HOUSE_Y
        self.cached_maze_dimensions = None

    def reset_game(self, map_filename=None, keep_wall_style=False):
        """Сброс игры с новым таймером, но сохранением режима кампании"""
        try: 
            # ========== ВЫБИРАЕМ СЛЕДУЮЩУЮ СТЕНУ ПО КРУГУ !!! ==========
            if not keep_wall_style: 
                self.cycle_wall_style(1)    
            # ===========================================================

            if map_filename:
                if not map_filename.endswith('.map'):
                    map_filename += '.map'
                self.load_map(map_filename)
            else:
                # === СОХРАНЯЕМ РЕЖИМ КАМПАНИИ ПРИ ПЕРЕЗАПУСКЕ ===
                campaign_mode = self.state.campaign_mode
                campaign_level = self.state.campaign_level
                campaign_wins = self.state.campaign_wins
                campaign_completed = self.state.campaign_completed

                # В режиме кампании используем уровень кампании, иначе текущую сложность
                if campaign_mode and not campaign_completed:
                    target_difficulty = campaign_level
                else:
                    target_difficulty = self.current_difficulty

                # ОБНОВЛЯЕМ КОНФИГ ПЕРЕД ГЕНЕРАЦИЕЙ
                self.config.MAZE_WIDTH = DIFFICULTY_LEVELS[target_difficulty]['MAZE_WIDTH']
                self.config.MAZE_HEIGHT = DIFFICULTY_LEVELS[target_difficulty]['MAZE_HEIGHT']
                self.config.time_TIMER_MAX = DIFFICULTY_LEVELS[target_difficulty]['time_TIMER_MAX']
                self.config.time_BONUS_TIME = DIFFICULTY_LEVELS[target_difficulty]['time_BONUS_TIME']

                # ПЕРЕСОЗДАЕМ лабиринт с новыми размерами
                self.maze = Maze(self.config.MAZE_WIDTH, self.config.MAZE_HEIGHT)
                self.generate_new_maze_and_items()

                # === ВОССТАНАВЛИВАЕМ РЕЖИМ КАМПАНИИ ===
                self.state.campaign_mode = campaign_mode
                self.state.campaign_level = campaign_level
                self.state.campaign_wins = campaign_wins
                self.state.campaign_completed = campaign_completed

            # СБРОС ТАЙМЕРА - новый подход
            self.state.time_timer = self.config.time_TIMER_MAX  # Используем актуальное значение из конфига
            self.state.timer_active = False
            self.state.last_second_time = time.time()

            # ОЧКИ НЕ СБРАСЫВАЕМ - они сохраняются между уровнями. Сброс происходит только при game_over

        except Exception as e:
            return f"Error: {e}"

        # Сброс состояния игры (но не режима кампании!)
        self.player.has_sword = True
        self.player.has_treasure = False
        self.state.game_over = False
        self.state.game_won = False
        self.state.show_path = False
        self.state.path_hide_time = None
        self.state.show_death_image = False
        self.state.game_paused = False

        # СБРОС ПЕРЕМЕЩЕНИЯ МЫШЬЮ
        self.mouse_move_target = None
        self.mouse_move_path = []
        self.mouse_move_index = 0
        self.mouse_move_take_item = False
        self.mouse_move_item_to_take = None
        self.player.is_moving = False

        for spider in self.maze.spiders:
            spider.defeated = False
        return "OK"

    def move_spiders(self):
        """Движение пауков (НЕ могут ходить через двери)"""
        # 1: Локальные ссылки для быстрого доступа
        grid = self.maze.grid
        maze_height = self.maze.height
        maze_width = self.maze.width
        extra_paths = getattr(self.maze, 'extra_paths', set())
        player_x, player_y = self.player.x, self.player.y
        
        # 2: Используем генератор вместо списка + предварительная фильтрация
        active_spiders = []
        occupied_positions = set()
        
        # Единый проход для сбора активных пауков и занятых позиций
        for spider in self.maze.spiders:
            if not spider.defeated:
                active_spiders.append(spider)
                occupied_positions.add((spider.x, spider.y))
                spider.old_pos = (spider.x, spider.y)  # Сохраняем старую позицию сразу
        
        # Быстрый выход если нет активных пауков
        if not active_spiders:
            return
        
        # 3: Предварительно вычисленные направления (константа)
        DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))
        
        # 4: Перемешиваем один раз
        random.shuffle(active_spiders)
        
        # 5: Вынесенная функция проверки проходимости (без замыканий)
        def is_passable_for_spider(x, y):
            return (0 <= x < maze_height and 
                    0 <= y < maze_width and 
                    grid[x][y] == 0 and  # только обычные проходы
                    (x, y) not in extra_paths)  # НЕ двери
        
        # 6: Словарь для намеченных перемещений
        intended_moves = {}
        
        # 7: Основной цикл движения с минимальными вычислениями
        for spider in active_spiders:
            hx, hy = spider.x, spider.y
            current_pos = (hx, hy)
            
            # 8: Быстрое вычисление направления к игроку
            dx = 1 if player_x > hx else (-1 if player_x < hx else 0)
            dy = 1 if player_y > hy else (-1 if player_y < hy else 0)
            
            # 9: Приоритетное направление движения
            primary_pos = None
            secondary_positions = []
            
            # Определяем основное и второстепенные направления
            if abs(player_x - hx) > abs(player_y - hy):
                # Горизонтальное движение в приоритете
                if dx != 0:
                    primary_pos = (hx + dx, hy)
                if dy != 0:
                    secondary_positions.append((hx, hy + dy))
            else:
                # Вертикальное движение в приоритете
                if dy != 0:
                    primary_pos = (hx, hy + dy)
                if dx != 0:
                    secondary_positions.append((hx + dx, hy))
            
            # 10: Проверка основного направления
            next_pos = current_pos
            if primary_pos and is_passable_for_spider(*primary_pos):
                next_pos = primary_pos
            else:
                # 11: Проверка второстепенных направлений (без лишнего перемешивания)
                for pos in secondary_positions:
                    if is_passable_for_spider(*pos):
                        next_pos = pos
                        break
                else:
                    # 12: Если оба основных направления недоступны - случайное движение
                    # Сразу проверяем все 4 направления без создания промежуточных списков
                    available_moves = []
                    for dx, dy in DIRECTIONS:
                        nx, ny = hx + dx, hy + dy
                        if is_passable_for_spider(nx, ny):
                            available_moves.append((nx, ny))
                    
                    if available_moves:
                        next_pos = random.choice(available_moves)
            
            # 13: Проверка конфликтов с другими пауками
            if next_pos in occupied_positions:
                # Ищем альтернативные доступные позиции
                alternative_moves = []
                for dx, dy in DIRECTIONS:
                    alt_x, alt_y = hx + dx, hy + dy
                    if (is_passable_for_spider(alt_x, alt_y) and 
                        (alt_x, alt_y) not in occupied_positions):
                        alternative_moves.append((alt_x, alt_y))
                
                if alternative_moves:
                    next_pos = random.choice(alternative_moves)
                else:
                    next_pos = current_pos  # Остаемся на месте
            
            intended_moves[current_pos] = next_pos
        
        # 14: Разрешение конфликтов перемещений в один проход
        final_moves = {}
        occupied_final = set()
        
        # Сначала обрабатываем пауков, которые остаются на месте (нет конфликтов)
        for spider in active_spiders:
            current_pos = (spider.x, spider.y)
            intended_pos = intended_moves.get(current_pos, current_pos)
            
            if intended_pos == current_pos:
                final_moves[current_pos] = intended_pos
                occupied_final.add(intended_pos)
        
        # Затем обрабатываем пауков, которые хотят двигаться
        for spider in active_spiders:
            current_pos = (spider.x, spider.y)
            intended_pos = intended_moves.get(current_pos, current_pos)
            
            if intended_pos != current_pos:
                if intended_pos not in occupied_final:
                    final_moves[current_pos] = intended_pos
                    occupied_final.add(intended_pos)
                else:
                    # Конфликт - остаемся на месте
                    final_moves[current_pos] = current_pos
                    occupied_final.add(current_pos)
        
        # 15: Применяем финальные перемещения
        for spider in active_spiders:
            current_pos = (spider.x, spider.y)
            new_x, new_y = final_moves.get(current_pos, current_pos)
            spider.x, spider.y = new_x, new_y

    def toggle_pause(self):
        """Переключение паузы по пробелу (только в игре и редакторе)"""
        if self.state.game_mode in ['game', 'editor']:
            if not self.state.game_paused:
                # Включаем паузу по пробелу
                self.state.game_paused = True
                self.state.pause_type = 'space_pause'
                self.state.pause_start_time = time.time()
            elif self.state.pause_type == 'space_pause':
                # Выключаем только паузу по пробелу
                self.state.game_paused = False
                self.state.pause_type = None
                self.state.pause_start_time = None

    def quit_game(self):
        """Выход из игры"""
        pygame.quit()
        exit()

    def draw_minimap_path(self, surface, path, color, map_cell_size, offset_x, offset_y):
        """Отрисовка пути на миникарте в режиме редактирования"""
        if not path:
            return

        for point in path:
            draw_x = point[1] * map_cell_size + map_cell_size // 2 + offset_x
            draw_y = point[0] * map_cell_size + map_cell_size // 2 + offset_y
            pygame.draw.circle(surface, color, (draw_x, draw_y), 3 * self.state.scale_factor)

    def draw_god_mode_indicator(self, surface, cell_size, offset_x, offset_y):
        """Отрисовка игрок в круге GOD MODE"""
        if not self.state.god_mode or self.state.game_over:
            return
        
        player_pos = (self.player.x, self.player.y)
        
        # Проверяем валидность позиции
        if not (0 <= player_pos[0] < len(self.maze.grid) and 
                0 <= player_pos[1] < len(self.maze.grid[0])):
            return
        
        center_x = player_pos[1] * cell_size + cell_size // 2 + offset_x
        center_y = player_pos[0] * cell_size + cell_size // 2 + offset_y
        
        # Золотая аура
        pygame.draw.circle(surface, self.config.GOLD, (center_x, center_y), cell_size // 2 + 5, 3)

    def draw_map(self, surface, mode="game", cell_size=32, offset=(0, 0), show_editor_ui=True):
        """Отрисовка карты с оптимизацией для больших размеров"""
        ox, oy = offset

        # Для больших лабиринтов в игровом режиме рисуем только видимую область
        if mode == "game" and (len(self.maze.grid) > 50 or len(self.maze.grid[0]) > 50):
            self.draw_visible_area_only(surface, cell_size, ox, oy)
            return

        if mode == "editor": # текущий вариант масштаба лабиринта
            map_margin = 1
            map_width = self.visible_maze_width - map_margin * 2
            map_height = self.visible_maze_height - map_margin * 2
            map_cell_size = min(map_width // len(self.maze.grid[0]), map_height // len(self.maze.grid))
            ox = (self.visible_maze_width - len(self.maze.grid[0]) * map_cell_size) // 2
            oy = (self.visible_maze_height - len(self.maze.grid) * map_cell_size) // 2
            actual_cell_size = map_cell_size
        else:
            actual_cell_size = cell_size

        def draw_element(image, pos, scale=False):
            if not pos or not image:
                return
            img = image
            if scale:
                img = pygame.transform.scale(image, (actual_cell_size, actual_cell_size))
            rect = img.get_rect(center=(
                pos[1] * actual_cell_size + actual_cell_size // 2 + ox,
                pos[0] * actual_cell_size + actual_cell_size // 2 + oy
            ))
            surface.blit(img, rect)

        for row in range(len(self.maze.grid)):
            for col in range(len(self.maze.grid[row])):
                draw_x = col * actual_cell_size + ox
                draw_y = row * actual_cell_size + oy
                rect = pygame.Rect(draw_x, draw_y, actual_cell_size, actual_cell_size)

                if self.maze.grid[row][col] == 0:
                    # ПРОХОД - проверяем, это обычный проход или дверь
                    if (row, col) in getattr(self.maze, 'extra_paths', set()):
                        # ДВЕРЬ
                        door_img = self.resource_manager.scaled_images.get('door')
                        if door_img:
                            if mode == "editor":
                                door_img = pygame.transform.scale(door_img, (actual_cell_size, actual_cell_size))
                            surface.blit(door_img, (draw_x, draw_y))
                        else:
                            pygame.draw.rect(surface, self.config.PATH_COLOR, rect)
                    else:
                        # ОБЫЧНЫЙ ПРОХОД
                        pygame.draw.rect(surface, self.config.BLACK, rect)
                else:
                    # ОБЫЧНАЯ СТЕНА
                    wall_img = self.resource_manager.scaled_images.get(self.current_wall_image, self.resource_manager.scaled_images.get('wall'))
                    if wall_img:
                        if mode == "editor":
                            wall_img = pygame.transform.scale(wall_img, (actual_cell_size, actual_cell_size))
                        surface.blit(wall_img, (draw_x, draw_y))

        # Отрисовка пути
        if self.state.show_path:
            path_to_follow = self.find_path_to_follow()
            if path_to_follow:
                if mode == "editor":
                    self.draw_minimap_path(surface, path_to_follow, self.config.YELLOW, actual_cell_size, ox, oy)
                else:
                    self.draw_path(surface, path_to_follow, self.config.YELLOW, actual_cell_size, ox, oy)
                    self.draw_minimap_path(surface, path_to_follow, self.config.YELLOW, actual_cell_size, ox, oy)

        # Вспомогательная функция для проверки позиций
        def is_valid_position(pos):
            return (0 <= pos[0] < len(self.maze.grid) and 
                    0 <= pos[1] < len(self.maze.grid[0]))
        scale = (mode == "editor")

        # Отрисовка объектов на стенах
        for sword_pos in self.maze.swords_positions:
            if is_valid_position(sword_pos) and self.maze.grid[sword_pos[0]][sword_pos[1]] == 1:
                # Проверяем, это позиция с мечами возле дома?
                if (hasattr(self.maze, 'house_sword_position') and 
                    self.maze.house_sword_position is not None and 
                    sword_pos[0] == self.maze.house_sword_position[0] and 
                    sword_pos[1] == self.maze.house_sword_position[1]):

                    # Считаем сколько мечей осталось в этой позиции
                    swords_in_position = self.maze.swords_positions.count(self.maze.house_sword_position)

                    if swords_in_position > 1:
                        # Если больше 1 меча - используем специальное изображение
                        draw_element(self.resource_manager.scaled_images.get('swords'), sword_pos, scale)
                    else:
                        # Если 1 меч или меньше - используем обычное изображение
                        draw_element(self.resource_manager.scaled_images.get('sword'), sword_pos, scale)
                else:
                    # Обычные мечи
                    draw_element(self.resource_manager.scaled_images.get('sword'), sword_pos, scale)

        for time_pos in self.maze.times_positions:
            if is_valid_position(time_pos) and self.maze.grid[time_pos[0]][time_pos[1]] == 1:
                draw_element(self.resource_manager.scaled_images.get('time'), time_pos, scale)

        for pointer_pos in self.maze.path_pointers_positions:
            if is_valid_position(pointer_pos) and self.maze.grid[pointer_pos[0]][pointer_pos[1]] == 1:
                frame_key = 'map' if self.current_map_pointer_index == 0 else 'map1'
                draw_element(self.resource_manager.scaled_images.get(frame_key), pointer_pos, scale)

        # Клад
        if (self.maze.treasure_position and 
            is_valid_position(self.maze.treasure_position) and 
            self.maze.grid[self.maze.treasure_position[0]][self.maze.treasure_position[1]] == 1):
            draw_element(self.resource_manager.scaled_images.get('treasure'), self.maze.treasure_position, scale)

        # Отрисовка объектов на путях
        house_pos = (self.config.HOUSE_X, self.config.HOUSE_Y)
        if (is_valid_position(house_pos) and 
            self.maze.grid[house_pos[0]][house_pos[1]] == 0):
            draw_element(self.resource_manager.scaled_images.get('house'), house_pos, scale)

        # Игрок
        player_pos = (self.player.x, self.player.y)
        if (is_valid_position(player_pos) and 
            self.maze.grid[self.player.x][self.player.y] == 0):
            player_img = self.player.get_image(self.resource_manager, self.state.game_over, self.state.show_death_image)
            if player_img:
                draw_element(player_img, player_pos, scale)

        # Пауки
        for spider in self.maze.spiders:
            spider_pos = (spider.x, spider.y)
            if (is_valid_position(spider_pos) and 
                self.maze.grid[spider.x][spider.y] == 0):
                
                if not spider.defeated:
                    # Живой паук
                    img = self.resource_manager.scaled_images.get(f'spider{"" if self.current_spider_image_index == 0 else "1"}')
                    draw_element(img, spider_pos, scale)
                
                elif spider.defeated_time > 0:
                    # Убитый паук
                    elapsed = time.time() - spider.defeated_time
                    
                    if elapsed < self.config.SPIDER_DEATH_ANIMATION_DURATION:
                        # === НОВАЯ ПРОВЕРКА: игрок стоит на месте убитого паука? ===
                        if (self.player.x == spider.x and self.player.y == spider.y and
                            not self.state.game_over and not self.state.game_won):
                            # Специальная анимация: игрок на месте паука
                            frame_index = int(elapsed / self.config.SPIDER_DEATH_ANIMATION_SPEED) % 2
                            frame_key = 'player_killed_spider1' if frame_index == 0 else 'player_killed_spider2'
                            img = self.resource_manager.scaled_images.get(frame_key)
                            draw_element(img, spider_pos, scale)
                        else:
                            # Обычная анимация смерти паука
                            frame = 'spider_dead1' if int(elapsed / self.config.SPIDER_DEATH_ANIMATION_SPEED) % 2 == 0 else 'spider_dead2'
                            img = self.resource_manager.scaled_images.get(frame)
                            draw_element(img, spider_pos, scale)

        # Отрисовка GOD MODE индикатора
        self.draw_god_mode_indicator(surface, actual_cell_size, ox, oy)

    def draw_visible_area_only(self, surface, cell_size, offset_x, offset_y):
        """Отрисовка только видимой области для больших лабиринтов (оптимизированная)"""
        # Локальные ссылки для скорости
        grid = self.maze.grid
        scaled_images = self.resource_manager.scaled_images
        blit = surface.blit
        draw_rect = pygame.draw.rect
        path_color = self.config.PATH_COLOR
        # wall_img = scaled_images.get('wall')
        wall_img = scaled_images.get(self.current_wall_image, scaled_images.get('wall'))
        door_img = scaled_images.get('door')
        extra_paths = getattr(self.maze, 'extra_paths', set())

        start_col = max(0, (-offset_x) // cell_size - 1)
        end_col = min(len(grid[0]), (self.visible_maze_width - offset_x) // cell_size + 1)
        start_row = max(0, (-offset_y) // cell_size - 1)
        end_row = min(len(grid), (self.visible_maze_height - offset_y) // cell_size + 1)
        
        # 1. Отрисовываем стены, пол и двери
        for row in range(start_row, end_row):
            draw_y = row * cell_size + offset_y  # вынесли из внутреннего цикла
            
            for col in range(start_col, end_col):
                draw_x = col * cell_size + offset_x
                
                if (draw_x + cell_size < 0 or draw_x > self.visible_maze_width or
                    draw_y + cell_size < 0 or draw_y > self.visible_maze_height):
                    continue
                    
                if grid[row][col] == 0:
                    # ПРОХОД - проверяем, это обычный проход или дверь
                    if (row, col) in extra_paths:
                        if door_img:
                            blit(door_img, (draw_x, draw_y))
                        else:
                            draw_rect(surface, path_color, (draw_x, draw_y, cell_size, cell_size))
                    else:
                        # ОБЫЧНЫЙ ПРОХОД - не рисуем, так как фон уже черный
                        pass
                else:
                    # ОБЫЧНАЯ СТЕНА
                    if wall_img:
                        blit(wall_img, (draw_x, draw_y))
        
        # 2. Отрисовка пути ПЕРЕД объектами
        if self.state.show_path:
            path_to_follow = self.find_path_to_follow()
            if path_to_follow:
                self.draw_path(surface, path_to_follow, self.config.YELLOW, cell_size, offset_x, offset_y)
        
        # 3. Отрисовка объектов ПОСЛЕ пути
        self.draw_objects_in_visible_area(surface, cell_size, offset_x, offset_y, 
                                        start_row, end_row, start_col, end_col)
        
        # 4. Отрисовка GOD MODE индикатора
        self.draw_god_mode_indicator(surface, cell_size, offset_x, offset_y)


    def draw_path(self, surface, path, color, cell_size, offset_x=0, offset_y=0):
        """Отрисовка пути с оптимизацией для больших лабиринтов"""
        if not path:
            return
        
        # Для больших лабиринтов определяем видимую область
        start_col = end_col = start_row = end_row = 0
        is_large_maze = (len(self.maze.grid) > 50 or len(self.maze.grid[0]) > 50)
        
        if is_large_maze:
            start_col = max(0, (-offset_x) // cell_size - 1)
            end_col = min(len(self.maze.grid[0]), (self.visible_maze_width - offset_x) // cell_size + 1)
            start_row = max(0, (-offset_y) // cell_size - 1)
            end_row = min(len(self.maze.grid), (self.visible_maze_height - offset_y) // cell_size + 1)
        
        for point in path:
            row, col = point
            
            # Для больших лабиринтов проверяем видимость точки
            if is_large_maze:
                if not (start_row <= row < end_row and start_col <= col < end_col):
                    continue
            
            draw_x = col * cell_size + cell_size // 2 + offset_x
            draw_y = row * cell_size + cell_size // 2 + offset_y
            
            # Проверка что точка видна на экране (с небольшим запасом)
            if (draw_x < -10 or draw_x > self.visible_maze_width + 10 or
                draw_y < -10 or draw_y > self.visible_maze_height + 10):
                continue
                
            pygame.draw.circle(surface, color, (int(draw_x), int(draw_y)), 
                            max(3, int(5 * self.state.scale_factor)))

    def draw_objects_in_visible_area(self, surface, cell_size, offset_x, offset_y, 
                                    start_row, end_row, start_col, end_col):
        """Отрисовка объектов только в видимой области"""
        
        def draw_element(image, pos, scale=False):
            if not pos or not image:
                return
            row, col = pos
            
            # Проверяем что объект в видимой области
            if not (start_row <= row < end_row and start_col <= col < end_col):
                return
                
            img = image
            if scale:
                img = pygame.transform.scale(image, (cell_size, cell_size))
            rect = img.get_rect(center=(
                col * cell_size + cell_size // 2 + offset_x,
                row * cell_size + cell_size // 2 + offset_y
            ))
            surface.blit(img, rect)
        
        # Отрисовка объектов на стенах (только в видимой области)
        for sword_pos in self.maze.swords_positions:
            if (0 <= sword_pos[0] < len(self.maze.grid) and 
                0 <= sword_pos[1] < len(self.maze.grid[0]) and 
                self.maze.grid[sword_pos[0]][sword_pos[1]] == 1):
                
                # Проверяем это позиция с группой мечей возле дома?
                if (hasattr(self.maze, 'house_sword_position') and 
                    self.maze.house_sword_position is not None and 
                    sword_pos[0] == self.maze.house_sword_position[0] and 
                    sword_pos[1] == self.maze.house_sword_position[1]):
                    
                    swords_in_position = self.maze.swords_positions.count(self.maze.house_sword_position)
                    if swords_in_position > 1:
                        draw_element(self.resource_manager.scaled_images.get('swords'), sword_pos)
                    else:
                        draw_element(self.resource_manager.scaled_images.get('sword'), sword_pos)
                else:
                    draw_element(self.resource_manager.scaled_images.get('sword'), sword_pos)
        
        for time_pos in self.maze.times_positions:
            if (0 <= time_pos[0] < len(self.maze.grid) and 
                0 <= time_pos[1] < len(self.maze.grid[0]) and 
                self.maze.grid[time_pos[0]][time_pos[1]] == 1):
                draw_element(self.resource_manager.scaled_images.get('time'), time_pos)
        
        for pointer_pos in self.maze.path_pointers_positions:
            if (0 <= pointer_pos[0] < len(self.maze.grid) and 
                0 <= pointer_pos[1] < len(self.maze.grid[0]) and 
                self.maze.grid[pointer_pos[0]][pointer_pos[1]] == 1):
                frame_key = 'map' if self.current_map_pointer_index == 0 else 'map1'
                draw_element(self.resource_manager.scaled_images.get(frame_key), pointer_pos)
        
        # Клад
        if (self.maze.treasure_position and 
            0 <= self.maze.treasure_position[0] < len(self.maze.grid) and 
            0 <= self.maze.treasure_position[1] < len(self.maze.grid[0]) and 
            self.maze.grid[self.maze.treasure_position[0]][self.maze.treasure_position[1]] == 1):
            draw_element(self.resource_manager.scaled_images.get('treasure'), self.maze.treasure_position)
        
        # Дом
        house_pos = (self.config.HOUSE_X, self.config.HOUSE_Y)
        if (0 <= house_pos[0] < len(self.maze.grid) and 
            0 <= house_pos[1] < len(self.maze.grid[0]) and 
            self.maze.grid[house_pos[0]][house_pos[1]] == 0):
            draw_element(self.resource_manager.scaled_images.get('house'), house_pos)
        
        # Игрок
        player_pos = (self.player.x, self.player.y)
        if (0 <= player_pos[0] < len(self.maze.grid) and 
            0 <= player_pos[1] < len(self.maze.grid[0]) and 
            self.maze.grid[self.player.x][self.player.y] == 0):
            player_img = self.player.get_image(self.resource_manager, self.state.game_over, self.state.show_death_image)
            if player_img:
                draw_element(player_img, player_pos)
        
        # пауки
        for spider in self.maze.spiders:
            spider_pos = (spider.x, spider.y)
            if (0 <= spider_pos[0] < len(self.maze.grid) and 
                0 <= spider_pos[1] < len(self.maze.grid[0]) and 
                self.maze.grid[spider.x][spider.y] == 0):
                
                if not spider.defeated:
                    img = self.resource_manager.scaled_images.get(f'spider{"" if self.current_spider_image_index == 0 else "1"}')
                    draw_element(img, spider_pos)
                
                elif spider.defeated_time > 0:
                    elapsed = time.time() - spider.defeated_time
                    if elapsed < self.config.SPIDER_DEATH_ANIMATION_DURATION:
                        if (self.player.x == spider.x and self.player.y == spider.y and
                            not self.state.game_over and not self.state.game_won):
                            frame_index = int(elapsed / self.config.SPIDER_DEATH_ANIMATION_SPEED) % 2
                            frame_key = 'player_killed_spider1' if frame_index == 0 else 'player_killed_spider2'
                            img = self.resource_manager.scaled_images.get(frame_key)
                            draw_element(img, spider_pos)
                        else:
                            frame = 'spider_dead1' if int(elapsed / self.config.SPIDER_DEATH_ANIMATION_SPEED) % 2 == 0 else 'spider_dead2'
                            img = self.resource_manager.scaled_images.get(frame)
                            draw_element(img, spider_pos)

    def handle_events(self):
        """Обработка событий (поддерживает плавное изменение размера по диагонали)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Обрабатываем как VIDEORESIZE (старое), так и WINDOWRESIZED (pygame 2)
            if event.type in (pygame.VIDEORESIZE, getattr(pygame, "WINDOWRESIZED", None)):
                w = getattr(event, "w", None)
                h = getattr(event, "h", None)
                if w is None or h is None:
                    try:
                        w, h = pygame.display.get_window_size()
                    except Exception:
                        continue

                # Проверяем полноэкранный режим
                if not self.is_maximized and (w > 1.4 * self.config.SCREEN_WIDTH or h > 1.4 * self.config.SCREEN_HEIGHT):
                    self.prev_window_size = (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT)
                    self.is_maximized = True
                elif self.is_maximized and (w < self.config.SCREEN_WIDTH or h < self.config.SCREEN_HEIGHT):
                    self.is_maximized = False
                    w, h = self.prev_window_size

                # Просто сохраняем новый размер — применим чуть позже
                self.pending_resize = (max(w, 800), max(h, 480))
                self.last_resize_time = time.time()
                continue

            # ЕСЛИ открыт комбинированный диалог — передаём событие ТОЛЬКО туда
            if self.state.show_combined_dialog:
                self.handle_combined_dialog_events(event)
                continue  # Пропускаем остальную обработку событий

            # === ДОБАВЛЕНО: ОБРАБОТКА ДИАЛОГА ВЫХОДА ИЗ КАМПАНИИ ===
            if self.state.show_exit_campaign_dialog:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if hasattr(self, 'exit_dialog_buttons'):
                        if self.exit_dialog_buttons['ok'].collidepoint(mouse_pos):
                            self.handle_exit_campaign_dialog(True)
                            continue
                        elif self.exit_dialog_buttons['cancel'].collidepoint(mouse_pos):
                            self.handle_exit_campaign_dialog(False)
                            continue

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.exit_dialog_selected_button = 'ok'
                        continue
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.exit_dialog_selected_button = 'cancel'
                        continue
                    elif event.key == pygame.K_RETURN:
                        self.handle_exit_campaign_dialog(self.exit_dialog_selected_button == 'ok')
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        self.handle_exit_campaign_dialog(False)
                        continue

                continue  # пропускаем остальную обработку

            # === ДОБАВЛЕНО: ОБРАБОТКА ДИАЛОГА ВХОДА В КАМПАНИЮ ===
            if self.state.show_enter_campaign_dialog:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if hasattr(self, 'enter_dialog_buttons'):
                        if self.enter_dialog_buttons['start'].collidepoint(mouse_pos):
                            self.start_campaign()  # Просто запускаем кампанию
                        # Cancel ничего не делает - просто закрываем диалог
                        self.state.show_enter_campaign_dialog = False
                        self.state.game_paused = False
                        continue

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.enter_dialog_selected_button = 'start'
                        continue
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.enter_dialog_selected_button = 'cancel'
                        continue
                    elif event.key == pygame.K_RETURN:
                        if self.enter_dialog_selected_button == 'start':
                            self.start_campaign()  # Просто запускаем кампанию
                        # Cancel ничего не делает
                        self.state.show_enter_campaign_dialog = False
                        self.state.game_paused = False
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        self.state.show_enter_campaign_dialog = False
                        self.state.game_paused = False
                        continue

                continue  # пропускаем остальную обработку

            # Нормальные события мыши/клавиш (только если диалоги не открыты)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    # Сначала проверяем клики по UI элементам
                    if not self.handle_ui_click(event):
                        # Если не кликнули по UI, обрабатываем клик по карте
                        if self.state.game_mode == 'game':
                            # В игровом режиме - перемещение
                            self.handle_map_click_for_movement(event)
                        elif self.state.game_mode == 'editor':
                            # В режиме редактора - размещение объектов
                            mouse_pos = pygame.mouse.get_pos()
                            labyrinth_rect = pygame.Rect(0, self.info_panel_height, self.visible_maze_width, self.visible_maze_height)
                            if labyrinth_rect.collidepoint(mouse_pos):
                                self.handle_editor_map_click(event, mouse_pos)
                elif event.button == 3:  # Правая кнопка мыши
                    # Обрабатываем правую кнопку только в режиме редактора
                    if self.state.game_mode == 'editor':
                        mouse_pos = pygame.mouse.get_pos()
                        labyrinth_rect = pygame.Rect(0, self.info_panel_height, self.visible_maze_width, self.visible_maze_height)
                        if labyrinth_rect.collidepoint(mouse_pos):
                            self.handle_editor_map_click(event, mouse_pos)

            if event.type == pygame.KEYDOWN:
                # Обработка Tab только когда нет активных диалогов
                if event.key == pygame.K_TAB:
                    if (not self.state.show_combined_dialog and  # Только комбинированный диалог
                        not self.active_menu_item and not self.menu_open_with_keyboard and 
                        not self.show_overlay_text and
                        not self.state.show_exit_campaign_dialog):  # Добавлена проверка на диалог выхода
                        self.toggle_editor_mode()
                        continue  # Пропускаем дальнейшую обработку для Tab
                self.handle_keydown(event)

        return True

    def handle_ui_click(self, event):
        """Обработка кликов по UI элементам. Возвращает True если клик был по UI."""
        # Проверяем клик по верхнему меню
        for item_name, rect in self.menu_rects.items():
            expanded_rect = rect.inflate(
                int(10 * self.state.scale_factor), 
                int(5 * self.state.scale_factor)
            )
            if expanded_rect.collidepoint(event.pos):
                self.handle_mouse_click(event)
                return True
        
        # Проверяем клик по подменю если активно
        if self.active_menu_item in ["Menu", "FREE PLAY"]:
            if self.handle_menu_click(event):
                return True
        
        # Проверяем клик по UI панели в редакторе
        if self.state.game_mode == 'editor':
            ui_panel_x = self.visible_maze_width
            ui_panel_rect = pygame.Rect(ui_panel_x, self.info_panel_height, 
                                    self.ui_panel_width, 
                                    self.config.SCREEN_HEIGHT - self.info_panel_height)
            if ui_panel_rect.collidepoint(event.pos):
                self.handle_editor_click(event)
                return True
                
        # === ДОБАВЛЕНО: Проверка кликов по UI панели в ИГРЕ ===
        if self.state.game_mode == 'game':
            ui_panel_x = self.visible_maze_width
            ui_panel_rect = pygame.Rect(ui_panel_x, self.info_panel_height, 
                                    self.ui_panel_width, 
                                    self.config.SCREEN_HEIGHT - self.info_panel_height)
            if ui_panel_rect.collidepoint(event.pos):
                self.handle_game_ui_click(event)
                return True
        
        return False

    def handle_game_ui_click(self, event):
        """Обработка кликов по UI в игровом режиме"""
        # Пауза
        if self.should_pause_game_logic():
            return
            
        mouse_pos = pygame.mouse.get_pos()
        
        # Используем сохраненные rect'ы из draw_unified_ui
        if hasattr(self, 'game_ui_rects'):
            for button_name, rect in self.game_ui_rects.items():
                if rect.collidepoint(mouse_pos):
                    if button_name == 'save_game':
                        self.show_save_game_dialog()
                    elif button_name == 'load_game':
                        self.show_load_game_dialog()
                    elif button_name == 'cycle_wall':
                        self.cycle_wall_style(1)  # Переключить на следующий стиль
                    return

    def handle_map_click_for_movement(self, event):
        """Обработка клика по карте для перемещения игрока и взятия предметов"""
        # Пауза
        if self.should_pause_game_logic():
            return
        
        # В режиме редактора обрабатываем клики только если НЕ выбран инструмент
        if self.state.game_mode == 'editor' and self.selected_tool is not None:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Проверяем что клик в области лабиринта
        labyrinth_rect = pygame.Rect(0, self.info_panel_height, self.visible_maze_width, self.visible_maze_height)
        if not labyrinth_rect.collidepoint(mouse_pos):
            return
        
        # === РЕЖИМ РЕДАКТОРА: используем другой расчет координат ===
        if self.state.game_mode == 'editor':
            # В редакторе используем расчет из handle_editor_map_click
            map_margin = 1
            map_width = self.visible_maze_width - map_margin * 2
            map_height = self.visible_maze_height - map_margin * 2
            
            map_cell_width = map_width // len(self.maze.grid[0])
            map_cell_height = map_height // len(self.maze.grid)
            map_cell_size = min(map_cell_width, map_cell_height)
            
            map_total_width = len(self.maze.grid[0]) * map_cell_size
            map_total_height = len(self.maze.grid) * map_cell_size
            
            offset_x = (self.visible_maze_width - map_total_width) // 2
            offset_y = (self.visible_maze_height - map_total_height) // 2
            
            col = (mouse_pos[0] - offset_x) // map_cell_size
            row = (mouse_pos[1] - self.info_panel_height - offset_y) // map_cell_size
            
            # Проверяем что координаты валидны
            if not (0 <= row < len(self.maze.grid) and 0 <= col < len(self.maze.grid[0])):
                return
                
            maze_x, maze_y = row, col
            
        else:
            # === РЕЖИМ ИГРЫ: используем оригинальный расчет ===
            maze_x, maze_y = self.screen_to_maze_coords(mouse_pos)
            
            # Проверяем что координаты валидны
            if not (0 <= maze_x < len(self.maze.grid) and 0 <= maze_y < len(self.maze.grid[0])):
                return
        
        # Проверяем, кликнули ли на предмет на стене (работает в обоих режимах)
        clicked_on_item = False
        item_position = None
        item_type = None
        
        # === ИСПОЛЬЗУЕМ МНОЖЕСТВА (SETS) ===
        if (maze_x, maze_y) in self.maze.swords_set:
            clicked_on_item = True
            item_position = (maze_x, maze_y)
            item_type = 'sword'
        elif (maze_x, maze_y) in self.maze.time_set:
            clicked_on_item = True
            item_position = (maze_x, maze_y)
            item_type = 'time'
        elif (maze_x, maze_y) in self.maze.pointers_set:
            clicked_on_item = True
            item_position = (maze_x, maze_y)
            item_type = 'pointer'
        elif self.maze.treasure_position == (maze_x, maze_y):
            clicked_on_item = True
            item_position = (maze_x, maze_y)
            item_type = 'treasure'
        
        # Если кликнули на предмет на стене
        if clicked_on_item and self.maze.grid[maze_x][maze_y] == 1:
            # Проверяем, стоит ли игрок рядом с предметом
            is_adjacent = False
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if (self.player.x == maze_x + dx and self.player.y == maze_y + dy):
                    is_adjacent = True
                    break
            
            if is_adjacent:
                # Игрок уже стоит рядом с предметом - сразу берем его
                self.mouse_move_target = None
                self.mouse_move_path = []
                self.mouse_move_take_item = True
                self.mouse_move_item_to_take = (item_position, item_type)
                self.mouse_move_index = 0
                
                # Немедленно берем предмет
                self.take_item_immediately()
                return
            else:
                # Игрок не рядом - находим путь к ближайшей проходимой клетке
                adjacent_paths = []
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = maze_x + dx, maze_y + dy
                    if (0 <= nx < len(self.maze.grid) and 
                        0 <= ny < len(self.maze.grid[0]) and 
                        self.maze.grid[nx][ny] == 0):
                        adjacent_paths.append((nx, ny))
                
                if adjacent_paths:
                    # Находим ближайшую к игроку проходимую клетку
                    min_distance = float('inf')
                    closest_path = None
                    for path_cell in adjacent_paths:
                        distance = abs(path_cell[0] - self.player.x) + abs(path_cell[1] - self.player.y)
                        if distance < min_distance:
                            min_distance = distance
                            closest_path = path_cell
                    
                    target_pos = closest_path
                    take_item_on_arrival = True
                    self.mouse_move_item_to_take = (item_position, item_type)
                else:
                    return
        
        # Если кликнули на проходимую клетку
        elif self.maze.grid[maze_x][maze_y] == 0:
            target_pos = (maze_x, maze_y)
            take_item_on_arrival = False
            self.mouse_move_item_to_take = None
        else:
            # Кликнули на стену без предмета - ничего не делаем
            return
        
        # Если кликнули на текущую позицию игрока - отменяем перемещение
        if target_pos and target_pos[0] == self.player.x and target_pos[1] == self.player.y:
            self.mouse_move_target = None
            self.mouse_move_path = []
            return
        
        # Находим путь к целевой клетке
        if target_pos:
            path = self.find_path_bfs(
                (self.player.x, self.player.y), 
                lambda pos: pos == target_pos
            )
            
            if path:  # Принимаем путь любой длины, даже если это текущая позиция
                self.mouse_move_target = target_pos
                self.mouse_move_path = path[1:] if len(path) > 1 else []  # Исключаем текущую позицию только если путь длиннее 1
                self.mouse_move_index = 0
                self.last_mouse_move_time = 0
                self.mouse_move_take_item = take_item_on_arrival

    def screen_to_maze_coords(self, screen_pos):
        """Преобразование экранных координат в координаты лабиринта"""
        screen_x, screen_y = screen_pos
        
        # Вычитаем смещение информационной панели
        screen_y -= self.info_panel_height
        
        # Получаем размеры лабиринта в пикселях
        maze_width_px, maze_height_px = self.get_maze_dimensions()
        
        # Расчет камеры (такой же как в основном цикле отрисовки)
        visible_width_half = self.visible_maze_width // 2
        visible_height_half = self.visible_maze_height // 2
        cell_size_half = self.cell_size // 2
        
        cam_x = self.player.y * self.cell_size - visible_width_half + cell_size_half
        cam_y = self.player.x * self.cell_size - visible_height_half + cell_size_half
        
        cam_x = max(0, min(cam_x, maze_width_px - self.visible_maze_width))
        cam_y = max(0, min(cam_y, maze_height_px - self.visible_maze_height))
        
        # Преобразуем экранные координаты в координаты лабиринта
        maze_col = (screen_x + cam_x) // self.cell_size
        maze_row = (screen_y + cam_y) // self.cell_size
        
        return int(maze_row), int(maze_col)

    def update_mouse_movement(self, current_time):
        """Обновление перемещения по клику мыши с взятием предметов"""
        # Если путь пустой, но нужно взять предмет - берем сразу
        if (not self.mouse_move_path and 
            self.mouse_move_take_item and 
            self.mouse_move_item_to_take):
            
            self.take_item_immediately()
            return
        
        # Если перемещение завершено или нет активного пути
        if (self.mouse_move_index >= len(self.mouse_move_path) or
            self.state.game_over or 
            self.state.game_won or 
            self.state.game_paused):
            
            # Если достигли цели и нужно взять предмет
            if (self.mouse_move_target is None and 
                self.mouse_move_take_item and 
                self.mouse_move_item_to_take):
                
                self.take_item_immediately()
            
            # Сбрасываем состояние движения когда нет активного перемещения
            if self.mouse_move_target is None:
                self.player.is_moving = False
            return
        
        # Поддерживаем состояние движения во время всего перемещения
        self.player.is_moving = True
        
        # Проверяем задержку между шагами
        if current_time - self.last_mouse_move_time < self.mouse_move_delay:
            return
        
        # Выполняем один шаг перемещения
        self.execute_mouse_move_step(current_time)

    def take_item_immediately(self):
            """Немедленное взятие предмета"""
            item_pos, item_type = self.mouse_move_item_to_take
            
            # Берем предмет
            if item_type == 'sword':
                # ОБМЕН МЕЧА И КЛАДА
                if self.player.has_treasure:
                    self.player.has_treasure = False
                    self.player.has_sword = True
                    self.maze.treasure_position = item_pos
                    
                    if item_pos in self.maze.swords_positions:
                        self.maze.swords_positions.remove(item_pos)

                        if item_pos not in self.maze.swords_positions:
                            self.maze.swords_set.discard(item_pos)

                    self.play_take_sound()

                elif not self.player.has_sword:
                    self.player.has_sword = True
                    
                    if item_pos in self.maze.swords_positions:
                        self.maze.swords_positions.remove(item_pos)

                        if item_pos not in self.maze.swords_positions:
                            self.maze.swords_set.discard(item_pos)

                    self.play_take_sound()

            elif item_type == 'time':
                if item_pos in self.maze.times_positions:
                    self.maze.times_positions.remove(item_pos)

                    if item_pos not in self.maze.times_positions:
                        self.maze.time_set.discard(item_pos)

                    self.state.time_timer += self.config.time_BONUS_TIME
                    if self.state.time_timer > self.config.time_TIMER_MAX:
                        self.state.time_timer = self.config.time_TIMER_MAX
                    self.play_take_sound()

            elif item_type == 'pointer':
                self.state.show_path = True
                self.state.path_hide_time = time.time() + 10
                self.play_take_sound()
                    
            elif item_type == 'treasure':
                if self.player.has_sword:
                    self.player.has_sword = False
                    self.player.has_treasure = True
                    
                    self.maze.swords_positions.append(item_pos)
                    self.maze.swords_set.add(item_pos)
                    
                    self.maze.treasure_position = None
                    self.play_take_sound()
                elif not self.player.has_treasure:
                    self.player.has_treasure = True
                    self.maze.treasure_position = None
                    self.play_take_sound()
            
            # Сбрасываем флаги
            self.mouse_move_take_item = False
            self.mouse_move_item_to_take = None

    def execute_mouse_move_step(self, current_time):
        """Выполнение одного шага перемещения мышью"""
        # Получаем следующую позицию в пути
        next_pos = self.mouse_move_path[self.mouse_move_index]
        next_x, next_y = next_pos

        # Вычисляем направление движения для анимации
        dx = next_x - self.player.x
        dy = next_y - self.player.y

        # Обновляем направление игрока
        if dx > 0: 
            self.player.direction = 'down'
        elif dx < 0: 
            self.player.direction = 'up'
        elif dy > 0: 
            self.player.direction = 'right'
        elif dy < 0: 
            self.player.direction = 'left'

        # Перемещаем игрока
        self.player.x, self.player.y = next_x, next_y

        # Воспроизводим звук шагов (только если не воспроизводится уже)
        if self.resource_manager.sounds.get('move') and self.sound_enabled:
            move_channel = pygame.mixer.Channel(1)
            if not move_channel.get_busy():
                move_channel.play(self.resource_manager.sounds['move'])

        # Переходим к следующему шагу
        self.mouse_move_index += 1
        self.last_mouse_move_time = current_time
        
        # Если достигли цели
        if self.mouse_move_index >= len(self.mouse_move_path):
            self.mouse_move_target = None
            self.mouse_move_path = []

    def handle_mouse_click(self, event):
        """Обработка кликов мыши с учетом масштаба"""
        current_time = time.time()
        mouse_pos = event.pos
        menu_clicked = False
        
        # Сначала проверяем клик по верхнему меню с масштабированием
        menu_item_x = int(10 * self.state.scale_factor)
        self.menu_rects = {}
        
        for item in self.menu_items:
            text_surface = self.fonts['menu'].render(item, True, self.config.MENU_ITEM_COLOR)
            text_rect = text_surface.get_rect(topleft=(
                menu_item_x, 
                (self.info_panel_height - text_surface.get_height()) // 2
            ))
            self.menu_rects[item] = text_rect
            menu_item_x += text_rect.width + int(20 * self.state.scale_factor)
        
        # Проверяем клик по пунктам верхнего меню
        for item_name, rect in self.menu_rects.items():
            # Создаем увеличенную область клика для лучшего UX
            expanded_rect = rect.inflate(
                int(10 * self.state.scale_factor), 
                int(5 * self.state.scale_factor)
            )
            if expanded_rect.collidepoint(mouse_pos):
                menu_clicked = True

                # При открытии меню сбрасываем тип паузы по пробелу
                if self.state.pause_type == 'space_pause':
                    self.state.pause_type = None

                if item_name == "Menu":
                    # ПРОСТАЯ ЛОГИКА: переключаем только Menu
                    self.active_menu_item = "Menu" if self.active_menu_item != "Menu" else None
                    self.show_overlay_text = None
                    if self.active_menu_item == "Menu":
                        self.menu_open_with_keyboard = True
                        self.menu_navigation_index = 0
                        self.state.game_paused = True
                        self.state.pause_start_time = current_time
                    else:
                        self.close_all_interfaces_and_resume(current_time)
                    return True  # ВАЖНО: возвращаем управление

                elif item_name == "FREE PLAY":
                    # Если мы в кампании - показываем диалог подтверждения выхода
                    if self.state.campaign_mode and not self.state.campaign_completed:
                        self.show_exit_campaign_confirmation()
                        return True
                    
                    # Обычная логика для FREE PLAY (если не в кампании)
                    self.active_menu_item = "FREE PLAY" if self.active_menu_item != "FREE PLAY" else None
                    self.show_overlay_text = None
                    if self.active_menu_item == "FREE PLAY":
                        self.menu_open_with_keyboard = True
                        self.level_navigation_index = self.current_difficulty - 1
                        self.state.game_paused = True
                        self.state.pause_start_time = current_time
                    else:
                        self.close_all_interfaces_and_resume(current_time)
                    return True  # ВАЖНО: возвращаем управление

                elif item_name == "CAMPAIGN":
                    # Если мы в Free Play - показываем диалог подтверждения перехода в кампанию
                    if not self.state.campaign_mode:
                        self.show_enter_campaign_confirmation()
                        self.active_menu_item = None
                        self.horizontal_nav_index = -1
                        return True
                    # Универсальная обработка кампании
                    self.handle_campaign_interaction(current_time)
                    return True  # ВАЖНО: возвращаем управление

                elif item_name == "Instructions":
                    # ЗАКРЫВАЕМ все другие меню при открытии Instructions
                    self.active_menu_item = None
                    self.menu_open_with_keyboard = False
                    self.show_overlay_text = self.instruction_text
                    self.state.game_paused = True
                    self.state.pause_start_time = current_time
                    return True  # ВАЖНО: возвращаем управление

                elif item_name == "About":
                    # ЗАКРЫВАЕМ все другие меню при открытии About
                    self.active_menu_item = None
                    self.menu_open_with_keyboard = False
                    self.show_overlay_text = self.about_text
                    self.state.game_paused = True
                    self.state.pause_start_time = current_time
                    return True  # ВАЖНО: возвращаем управление

                break

        # === ПРОВЕРКА КЛИКОВ ВНЕ ВСЕХ ОКОН ===
        if not menu_clicked and (self.active_menu_item or 
                                self.state.show_combined_dialog or 
                                self.show_overlay_text or
                                self.state.show_exit_campaign_dialog or
                                self.state.show_enter_campaign_dialog):
            # Кликнули вне открытых окон - закрываем всё
            self.close_all_interfaces_and_resume(current_time)
            return True  # ВАЖНО: возвращаем True чтобы клик не передавался дальше
        
        # Если кликнули по подменю (только если меню активно)
        if self.active_menu_item in ["Menu", "FREE PLAY"]:
            if self.handle_menu_click(event):
                return True  # ВАЖНО: возвращаем True чтобы клик не передавался дальше
        
        # Если кликнули не по меню и нет открытых окон
        if not menu_clicked:
            self.close_all_interfaces_and_resume(current_time)
            
            # Обработка кликов в редакторе (только если не в меню)
            if self.state.game_mode == 'editor' and not self.state.game_paused:
                self.handle_editor_click(event)

        return True

    def handle_menu_click(self, event):
        """Обработка кликов в меню. Возвращает True если клик был в меню."""
        current_time = time.time()
        mouse_pos = event.pos
        submenu_x = self.menu_rects[self.active_menu_item].left
        submenu_y_start = self.info_panel_height
        submenu_item_height = int(30 * self.state.scale_factor)
        
        # Подменю для Menu
        if self.active_menu_item == "Menu":
            submenu_options = [
                {"name": "New Game", "action": lambda: self.reset_game(keep_wall_style=False)},  # <-- Меняем стену
                {"name": "Save Game", "action": lambda: self.show_save_game_dialog()},
                {"name": "Load Game", "action": lambda: self.show_load_game_dialog()},
                {"name": "Edit Map", "action": lambda: self.toggle_editor_mode()},
                {"name": "Sound: ON" if self.sound_enabled else "Sound: OFF", "action": lambda: self.toggle_sound()},
                {"name": f"Game Speed: {self.FPS}", "action": lambda: self.toggle_fps()},
                {"name": f"Spiders Speed: {self.spider_speed}", "action": lambda: self.toggle_spider_speed()},
                {"name": f"Timer: {'ON' if self.state.time_timer_enabled else 'OFF'}", "action": lambda: self.toggle_time_timer()},
                {"name": "Save Map", "action": lambda: self.show_save_dialog_handler()},
                {"name": "Load Map", "action": lambda: self.show_load_dialog_handler()},
                {"name": "Exit", "action": lambda: self.quit_game()}
            ]
            
            # Вычисляем ширину через общий метод
            submenu_width = self.calculate_submenu_width(submenu_options)

            for i, option in enumerate(submenu_options):
                item_rect = pygame.Rect(submenu_x, submenu_y_start + (i * submenu_item_height), 
                                    submenu_width, submenu_item_height)
                if item_rect.collidepoint(mouse_pos):
                    if option["action"]:
                        self.menu_navigation_index = i
                        option["action"]()
                        
                        if i == 0:  # New Game
                            self.state.maps_completed = 0
                        
                        if option["name"] in ["New Game", "Edit Map", "Exit"]:
                            self.close_all_interfaces_and_resume(current_time)
                    return True
        
        # Подменю для FREE PLAY
        elif self.active_menu_item == "FREE PLAY":
            submenu_options = [
                {"name": "Easy", "action": lambda: self.set_difficulty(1), "level": 1},
                {"name": "Normal", "action": lambda: self.set_difficulty(2), "level": 2},
                {"name": "Hard", "action": lambda: self.set_difficulty(3), "level": 3},
                {"name": "Challenging", "action": lambda: self.set_difficulty(4), "level": 4},
                {"name": "Difficult", "action": lambda: self.set_difficulty(5), "level": 5},
                {"name": "Extreme", "action": lambda: self.set_difficulty(6), "level": 6},
                {"name": "Nightmare", "action": lambda: self.set_difficulty(7), "level": 7}
            ]
            
            # Вычисляем ширину через общий метод
            submenu_width = self.calculate_submenu_width(submenu_options)

            for i, option in enumerate(submenu_options):
                item_rect = pygame.Rect(submenu_x, submenu_y_start + (i * submenu_item_height), 
                                    submenu_width, submenu_item_height)
                if item_rect.collidepoint(mouse_pos):
                    if option["action"]:
                        self.level_navigation_index = i
                        option["action"]()   # <-- Здесь вызывается set_difficulty(), который уже использует keep_wall_style=True !!!
                        self.close_all_interfaces_and_resume(current_time)
                    return True
        
        # Проверка кликов в области подменю (здесь submenu_width может быть не определен!)
        # Поэтому нужно сохранить submenu_width или пересчитать
        if 'submenu_options' in locals() and 'submenu_width' in locals():
            submenu_rect = pygame.Rect(submenu_x, submenu_y_start, 
                                    submenu_width,
                                    len(submenu_options) * submenu_item_height)
            if submenu_rect.collidepoint(mouse_pos):
                return True
        
        # Клик был вне подменю - закрываем меню
        self.close_all_interfaces_and_resume(current_time)
        return True

    def toggle_spider_speed(self):
        """Циклическое переключение скорости пауков"""
        speed_options = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        
        # Находим текущую скорость в списке
        current_speed = self.spider_speed
        if current_speed in speed_options:
            current_index = speed_options.index(current_speed)
        else:
            current_index = 2  # 8 - по умолчанию
        
        # Переходим к следующей скорости
        new_index = (current_index + 1) % len(speed_options)
        new_speed = speed_options[new_index]
        
        # Устанавливаем новую скорость
        self.spider_speed = new_speed
        self.state.spider_speed_custom = True
        self.state.spider_speed_value = new_speed
        
        self.set_editor_message(f"Speed: {new_speed} (10-min...1-max)")

    def reset_spider_speed_to_default(self):
        """Сброс скорости пауков к стандартной для текущего уровня сложности"""
        if not self.state.spider_speed_custom:
            self.spider_speed = DIFFICULTY_LEVELS[self.current_difficulty]['spider_SPEED']

    def toggle_fps(self):
        """Циклическое переключение FPS"""
        fps_options = [10, 11, 12, 13, 14, 15, 16,17,18,19,20,30,60]
        try:
            current_index = fps_options.index(self.FPS)
        except ValueError:
            current_index = 2 # Дефолтные 12 FPS если текущего нет в списке
                
        new_index = (current_index + 1) % len(fps_options)
        self.FPS = fps_options[new_index]

    def handle_editor_click(self, event):
        """Обработка кликов в редакторе (только когда нет активных меню)"""
        # Не обрабатываем клики в редакторе если открыты меню, диалоги или пауза
        if (self.active_menu_item or 
            self.show_overlay_text or 
            self.state.show_combined_dialog or
            self.state.game_paused):
            return
                
        mouse_pos = pygame.mouse.get_pos()
        ui_panel_x = self.visible_maze_width

        # ПЕРВОЕ: проверяем клики по кнопкам редактора
        if hasattr(self, 'editor_ui_rects'):
            for tool_name, rect in self.editor_ui_rects.items():
                if rect.collidepoint(mouse_pos):
                    if tool_name in ['save_map', 'load_map', 'check_map']:
                        # Это кнопка - обрабатываем и ВЫХОДИМ
                        if tool_name == 'save_map':
                            self.show_save_dialog_handler()
                        elif tool_name == 'load_map':
                            self.show_load_dialog_handler()
                        elif tool_name == 'check_map':
                            self.check_map_solvability_handler()
                        return  # ВАЖНО: выходим после обработки кнопки
                    else:
                        # Это инструмент - выбираем его
                        self.selected_tool = tool_name
                        self.set_editor_message(f"Edit: {tool_name}")
                        return  # ВАЖНО: выходим после выбора инструмента

        # ВТОРОЕ: если кликнули не по UI, проверяем клик по карте
        labyrinth_rect = pygame.Rect(0, self.info_panel_height, self.visible_maze_width, self.visible_maze_height)
        if labyrinth_rect.collidepoint(mouse_pos):
            # Обрабатываем ВСЕ клики по карте в редакторе
            # Независимо от выбранного инструмента (если он есть или нет)
            self.handle_editor_map_click(event, mouse_pos)
            return  # ВАЖНО: выходим после обработки клика по карте

    def handle_editor_map_click(self, event, mouse_pos):
        """Обработка кликов на карте в редакторе"""
        # Если выбран инструмент - обрабатываем как редактирование
        if self.selected_tool is not None:
            # Оригинальная логика редактирования
            map_margin = 1
            map_width = self.visible_maze_width - map_margin * 2
            map_height = self.visible_maze_height - map_margin * 2
            
            map_cell_width = map_width // len(self.maze.grid[0])
            map_cell_height = map_height // len(self.maze.grid)
            map_cell_size = min(map_cell_width, map_cell_height)
            
            map_total_width = len(self.maze.grid[0]) * map_cell_size
            map_total_height = len(self.maze.grid) * map_cell_size
            
            offset_x = (self.visible_maze_width - map_total_width) // 2
            offset_y = (self.visible_maze_height - map_total_height) // 2
            
            col = (mouse_pos[0] - offset_x) // map_cell_size
            row = (mouse_pos[1] - self.info_panel_height - offset_y) // map_cell_size
            
            if 0 <= row < self.config.MAZE_HEIGHT and 0 <= col < self.config.MAZE_WIDTH:
                if event.button == 1:  # Левая кнопка мыши
                    if self.selected_tool == 'wall':
                        # Стена - превращаем в стену и удаляем объекты
                        if self.maze.grid[row][col] == 0:
                            self.maze.grid[row][col] = 1
                            # Удаляем из дверей если это был проход
                            if (row, col) in getattr(self.maze, 'extra_paths', set()):
                                self.maze.extra_paths.discard((row, col))
                            self.remove_object_from_position((row, col))  # Удаляем объекты со стены
                            self.cached_maze_dimensions = None  # Сброс кэш
                        else:
                            self.set_editor_message("On the path!")
                            
                    elif self.selected_tool == 'door':
                        # Дверь - превращаем стену в проход и добавляем в extra_paths
                        if self.maze.grid[row][col] == 1:
                            self.maze.grid[row][col] = 0
                            self.maze.extra_paths.add((row, col))
                            # Удаляем объекты если они есть
                            if (self.maze.treasure_position == (row, col) or
                                (row, col) in self.maze.swords_set or
                                (row, col) in self.maze.time_set or
                                (row, col) in self.maze.pointers_set):
                                self.remove_object_from_position((row, col))
                            self.cached_maze_dimensions = None  # Сброс кэш
                        else:
                            self.set_editor_message("On the wall!")
                            
                    elif self.selected_tool == 'path':
                        # Обычный проход - превращаем в проход и удаляем из extra_paths
                        if self.maze.grid[row][col] == 1:
                            self.maze.grid[row][col] = 0
                            # Удаляем из дверей если это был проход
                            if (row, col) in getattr(self.maze, 'extra_paths', set()):
                                self.maze.extra_paths.discard((row, col))
                            self.remove_object_from_position((row, col))  # Удаляем объекты
                            self.cached_maze_dimensions = None  # Сброс кэш
                        else:
                            self.set_editor_message("On the wall!")
                            
                    elif self.selected_tool == 'sword':
                        # Меч можно ставить только на стены
                        if self.maze.grid[row][col] == 1:
                            self.maze.swords_positions.append((row, col))
                            self.maze.swords_set.add((row, col))  # добавляем в множество
                        else:
                            self.set_editor_message("On the wall!")
                            
                    elif self.selected_tool == 'time':
                        # Жизнь можно ставить только на стены
                        if self.maze.grid[row][col] == 1:
                            self.maze.times_positions.append((row, col))
                            self.maze.time_set.add((row, col))
                        else:
                            self.set_editor_message("On the wall!")
                            
                    elif self.selected_tool == 'pointer':
                        # Указатель можно ставить только на стены
                        if self.maze.grid[row][col] == 1:
                            self.maze.path_pointers_positions.append((row, col))
                            self.maze.pointers_set.add((row, col))
                        else:
                            self.set_editor_message("On the wall!")
                            
                    elif self.selected_tool == 'spider':
                        # паука можно ставить только на пути
                        if self.maze.grid[row][col] == 0:
                            self.maze.spiders.append(SpiderEnemy(row, col))
                        else:
                            self.set_editor_message("On the path!")
                            
                    elif self.selected_tool == 'treasure':
                        # Клад можно ставить только на стены
                        if self.maze.grid[row][col] == 1:
                            self.maze.treasure_position = (row, col)
                        else:
                            # НЕ убираем клад с предыдущей позиции, если новая позиция невалидна
                            self.set_editor_message("On the wall!")

                    elif self.selected_tool == 'house':
                        # Дом можно ставить только на пути
                        if self.maze.grid[row][col] == 0:
                            self.config.HOUSE_X, self.config.HOUSE_Y = row, col
                            self.player.x, self.player.y = row, col
                        else:
                            self.set_editor_message("On the path!")
                    
                elif event.button == 3:  # Правая кнопка - удаление
                    # УДАЛЕНИЕ СТЕНЫ: превращаем стену в проход
                    if self.maze.grid[row][col] == 1:
                        self.maze.grid[row][col] = 0
                        # Удаляем из дверей если это был проход
                        if (row, col) in getattr(self.maze, 'extra_paths', set()):
                            self.maze.extra_paths.discard((row, col))
                        self.cached_maze_dimensions = None  # Сброс кэш
                    else:
                        # Для проходов - обычное удаление объектов
                        self.remove_object_from_position((row, col))
        
        # Если НЕ выбран инструмент - обрабатываем как перемещение игрока
        else:
            if event.button == 1:  # Левая кнопка мыши - перемещение
                # Создаем фейковое событие для передачи в handle_map_click_for_movement
                fake_event = type('Event', (), {
                    'pos': mouse_pos,
                    'button': 1
                })()
                self.handle_map_click_for_movement(fake_event)
            
            elif event.button == 3:  # Правая кнопка - удаление
                # Оригинальная логика удаления
                map_margin = 1
                map_width = self.visible_maze_width - map_margin * 2
                map_height = self.visible_maze_height - map_margin * 2
                
                map_cell_width = map_width // len(self.maze.grid[0])
                map_cell_height = map_height // len(self.maze.grid)
                map_cell_size = min(map_cell_width, map_cell_height)
                
                map_total_width = len(self.maze.grid[0]) * map_cell_size
                map_total_height = len(self.maze.grid) * map_cell_size
                
                offset_x = (self.visible_maze_width - map_total_width) // 2
                offset_y = (self.visible_maze_height - map_total_height) // 2
                
                col = (mouse_pos[0] - offset_x) // map_cell_size
                row = (mouse_pos[1] - self.info_panel_height - offset_y) // map_cell_size
                
                if 0 <= row < self.config.MAZE_HEIGHT and 0 <= col < self.config.MAZE_WIDTH:
                    # УДАЛЕНИЕ СТЕНЫ: превращаем стену в проход
                    if self.maze.grid[row][col] == 1:
                        self.maze.grid[row][col] = 0
                        # Удаляем из дверей если это был проход
                        if (row, col) in getattr(self.maze, 'extra_paths', set()):
                            self.maze.extra_paths.discard((row, col))
                        self.cached_maze_dimensions = None  # Сброс кэш
                    else:
                        # Для проходов - обычное удаление объектов
                        self.remove_object_from_position((row, col))

    def remove_object_from_position(self, position):
        """Удаление объекта из указанной позиции"""
        # Удаляем из списков и множеств
        if position in self.maze.swords_positions:
            self.maze.swords_positions.remove(position)
            self.maze.swords_set.discard(position)

        if position in self.maze.times_positions:
            self.maze.times_positions.remove(position)
            self.maze.time_set.discard(position)

        if position in self.maze.path_pointers_positions:
            self.maze.path_pointers_positions.remove(position)
            self.maze.pointers_set.discard(position)
        
        # пауков удаляем по координатам
        self.maze.spiders[:] = [h for h in self.maze.spiders if (h.x, h.y) != position]

        # Удаляем клад и дом только если кликнули именно по их текущей позиции
        if self.maze.treasure_position == position:
            self.maze.treasure_position = None

        if (self.config.HOUSE_X, self.config.HOUSE_Y) == position:
            self.config.HOUSE_X, self.config.HOUSE_Y = 0, 0

        # ДОБАВИТЬ: Удаление из дверей
        if position in getattr(self.maze, 'extra_paths', set()):
            self.maze.extra_paths.discard(position)

    def handle_editor_buttons_click(self, mouse_pos):
        """Обработка кликов на кнопках редактора"""
        # Используем сохраненные rect'ы из draw_editor_ui
        if hasattr(self, 'editor_ui_rects'):
            for button_name, rect in self.editor_ui_rects.items():
                if button_name in ['save_map', 'load_map', 'check_map'] and rect.collidepoint(mouse_pos):
                    if button_name == 'save_map':
                        self.show_save_dialog_handler()
                    elif button_name == 'load_map':
                        self.show_load_dialog_handler()
                    elif button_name == 'check_map':
                        self.check_map_solvability_handler()
                    return

    def show_save_dialog_handler(self):
        """Обработчик показа диалога сохранения карты"""
        self.show_combined_dialog('save_map')

    def show_load_dialog_handler(self):
        """Обработчик показа диалога загрузки карты"""
        self.show_combined_dialog('load_map')

    def show_save_game_dialog(self):
        """Обработчик показа диалога сохранения игры"""
        if self.state.game_over or self.state.game_won:
            self.set_editor_message("Cannot save: game over/win")
            return
        self.show_combined_dialog('save_game')

    def show_load_game_dialog(self):
        """Обработчик показа диалога загрузки игры"""
        self.show_combined_dialog('load_game')

    def check_map_solvability_handler(self):
        """Обработчик проверки проходимости карты"""
        if self.check_map_solvability():
            self.set_editor_message("Passable!")
        else:
            self.set_editor_message("Impassable!")

    def toggle_editor_mode(self):
        """Переключение режима редактора"""
        self.state.game_mode = 'editor' if self.state.game_mode == 'game' else 'game'
        self.active_menu_item = None
        self.show_overlay_text = None
        self.state.game_paused = False
        self.state.pause_type = None  # Сбросить тип паузы
        
        # ОБНОВЛЯЕМ РАЗМЕРЫ UI ПРИ ПЕРЕКЛЮЧЕНИИ РЕЖИМОВ
        self.update_dimensions()
        
        # Сбрасываем состояние игры при переключении режимов
        self.state.game_over = False
        self.state.game_won = False
        self.state.show_death_image = False
        # СБРАСЫВАЕМ ВЫБРАННЫЙ ИНСТРУМЕНТ ПРИ ПЕРЕКЛЮЧЕНИИ РЕЖИМОВ
        self.selected_tool = None

    def handle_keydown(self, event):
        """Обработка нажатий клавиш (диалоги кампании обрабатываются в handle_events)"""
        current_time = time.time()

        # === ПЕРВЫЙ ПРИОРИТЕТ: СНЯТИЕ ПАУЗЫ ПО ПРОБЕЛУ ===
        if (self.state.game_paused and 
            self.state.pause_type == 'space_pause' and
            not self.state.show_combined_dialog and
            not self.active_menu_item and
            not self.menu_open_with_keyboard and
            not self.show_overlay_text and
            not self.state.show_exit_campaign_dialog and
            not self.state.show_enter_campaign_dialog):
            
            # Снимаем паузу ЛЮБОЙ клавишей (включая стрелки)
            self.state.game_paused = False
            self.state.pause_type = None
            return

        # === ВТОРОЙ ПРИОРИТЕТ: РЕЖИМ РЕДАКТОРА С ИНСТРУМЕНТОМ ===
        if (self.state.game_mode == 'editor' and self.selected_tool is not None):
            self.selected_tool = None
            return
        
        # === ТРЕТИЙ ПРИОРИТЕТ: ПЕРЕЗАПУСК ИГРЫ ПОСЛЕ GAME OVER/WIN ===
        if event.key == pygame.K_RETURN:
            if self.state.game_over or self.state.game_won:
                # Сбрасываем игру в обоих режимах - игра сразу запускается
                self.reset_game(keep_wall_style=False)
                # Убедимся, что пауза снята
                self.state.game_paused = False
                self.state.pause_start_time = None
                return

        # === ЧЕТВЕРТЫЙ ПРИОРИТЕТ: ОБРАБОТКА ESC ===
        if event.key == pygame.K_ESCAPE:
            # Закрываем ВСЕ открытые меню/диалоги и снимаем паузу
            self.close_all_interfaces_and_resume()
            
            # Дополнительные действия для ESC (не входящие в стандартное закрытие)
            if self.state.show_minimap:
                self.state.show_minimap = False
            
            # ВСЕГДА СБРАСЫВАЕМ ВЫБРАННЫЙ ИНСТРУМЕНТ ПРИ ESC
            self.selected_tool = None
            return

        # === ПЯТЫЙ ПРИОРИТЕТ: ОБРАБОТКА ПРОБЕЛА ДЛЯ ПАУЗЫ ===
        if event.key == pygame.K_SPACE:
            if self.state.game_mode in ['game', 'editor']:
                self.toggle_pause()
                # Сбрасываем меню при включении/выключении паузы
                self.active_menu_item = None
                self.menu_open_with_keyboard = False
                self.show_overlay_text = None
                return

        # === ШЕСТОЙ ПРИОРИТЕТ: ОБРАБОТКА ALT ДЛЯ МЕНЮ ===
        if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
            if not self.menu_open_with_keyboard and not self.show_overlay_text:
                # Открываем клавиатурную навигацию по верхнему меню
                self.menu_open_with_keyboard = True
                self.horizontal_nav_index = 0
                self.menu_navigation_index = 0
                self.level_navigation_index = 0
                self.active_menu_item = None

                # === ИЗМЕНЕНИЕ: СРАЗУ ОТКРЫВАЕМ ПОДМЕНЮ "Menu" ===
                self.active_menu_item = "Menu"
                self.menu_navigation_index = 0

                # Устанавливаем паузу и сбрасываем тип паузы по пробелу
                self.state.game_paused = True
                self.state.pause_type = None
                self.state.pause_start_time = current_time
            else:
                # Если уже был открыт режим навигации, закрываем его
                # Сохраняем паузу по пробелу если она активна
                self.close_all_interfaces_and_resume(current_time, keep_space_pause=True)

            return

        # === СЕДЬМОЙ ПРИОРИТЕТ: НАВИГАЦИЯ ПО МЕНЮ ===
        if self.menu_open_with_keyboard:
            # Если подменю "Menu" открыто — обрабатываем вертикальную навигацию по нему
            if self.active_menu_item == "Menu":
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    # Если находимся на первом пункте подменю - стрелка вверх закрывает подменю
                    if self.menu_navigation_index == 0:
                        self.active_menu_item = None
                        self.menu_navigation_index = 0
                    else:
                        self.menu_navigation_index = (self.menu_navigation_index - 1) % 11
                    return
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.menu_navigation_index = (self.menu_navigation_index + 1) % 11
                    return
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    # Стрелка вправо в подменю переходит к следующему пункту горизонтального меню
                    self.active_menu_item = None
                    self.menu_navigation_index = 0
                    self.horizontal_nav_index = (self.horizontal_nav_index + 1) % len(self.menu_items)
                    return
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    # Стрелка влево в подменю переходит к предыдущему пункту горизонтального меню
                    self.active_menu_item = None
                    self.menu_navigation_index = 0
                    self.horizontal_nav_index = (self.horizontal_nav_index - 1) % len(self.menu_items)
                    return
                elif event.key == pygame.K_RETURN:
                    # Выполнить действие выбранного пункта подменю
                    self.execute_menu_action()
                    return

            # Если подменю "FREE PLAY" открыто — обрабатываем вертикальную навигацию по нему
            elif self.active_menu_item == "FREE PLAY":
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.level_navigation_index == 0:
                        self.active_menu_item = None
                        self.level_navigation_index = 0
                    else:
                        self.level_navigation_index = (self.level_navigation_index - 1) % 7
                    return
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.level_navigation_index = (self.level_navigation_index + 1) % 7
                    return
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    # Стрелка вправо в подменю переходит к следующему пункту горизонтального меню
                    self.active_menu_item = None
                    self.level_navigation_index = 0
                    self.horizontal_nav_index = (self.horizontal_nav_index + 1) % len(self.menu_items)
                    return
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    # Стрелка влево в подменю переходит к предыдущему пункту горизонтального меню
                    self.active_menu_item = None
                    self.level_navigation_index = 0
                    self.horizontal_nav_index = (self.horizontal_nav_index - 1) % len(self.menu_items)
                    return
                elif event.key == pygame.K_RETURN:
                    # === ИСПРАВЛЕННАЯ ЛОГИКА: ПРОВЕРЯЕМ КАМПАНИЮ ПРИ ВЫБОРЕ УРОВНЯ ===
                    if self.state.campaign_mode and not self.state.campaign_completed:
                        self.show_exit_campaign_confirmation()
                        # Сохраняем выбранный уровень
                        self.pending_difficulty = self.level_navigation_index + 1
                    else:
                        # Обычный выбор уровня
                        level_actions = [
                            lambda: self.set_difficulty(1),
                            lambda: self.set_difficulty(2), 
                            lambda: self.set_difficulty(3),
                            lambda: self.set_difficulty(4),
                            lambda: self.set_difficulty(5),
                            lambda: self.set_difficulty(6),
                            lambda: self.set_difficulty(7)
                        ]
                        if 0 <= self.level_navigation_index < len(level_actions):
                            level_actions[self.level_navigation_index]()
                    # Закрываем меню после выбора уровня
                    self.close_all_interfaces_and_resume(current_time, keep_space_pause=True)
                    return

            # Горизонтальная навигация между верхними пунктами (когда подменю не открыто)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.horizontal_nav_index = (self.horizontal_nav_index - 1) % len(self.menu_items)
                self.active_menu_item = None
                self.menu_navigation_index = 0
                self.level_navigation_index = 0
                return
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.horizontal_nav_index = (self.horizontal_nav_index + 1) % len(self.menu_items)
                self.active_menu_item = None
                self.menu_navigation_index = 0
                self.level_navigation_index = 0
                return
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                # Переход в подменю по стрелке вниз
                selected = self.menu_items[self.horizontal_nav_index]
                if selected == "Menu":
                    # Открываем подменю Menu и начинаем вертикальную навигацию по нему
                    self.active_menu_item = "Menu"
                    self.menu_navigation_index = 0
                elif selected == "FREE PLAY":
                    # Открываем подменю FREE PLAY и начинаем вертикальную навигацию по нему
                    self.active_menu_item = "FREE PLAY"
                    self.level_navigation_index = self.current_difficulty - 1  # устанавливаем на текущий уровень
                elif selected == "CAMPAIGN":
                    # Если мы в Free Play - показываем диалог подтверждения перехода в кампанию
                    if not self.state.campaign_mode:
                        self.show_enter_campaign_confirmation()
                        return
                    # Универсальная обработка кампании
                    self.handle_campaign_interaction(current_time)
                return
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                # Стрелка вверх в горизонтальном меню тоже закрывает навигацию (альтернатива Esc)
                # Сохраняем паузу по пробелу если она активна
                self.close_all_interfaces_and_resume(current_time, keep_space_pause=True)
                return
            elif event.key == pygame.K_RETURN:
                # Enter выполняет действие для всех пунктов верхнего меню
                selected = self.menu_items[self.horizontal_nav_index]
                if selected == "Menu":
                    # Enter на пункте "Menu" открывает подменю (альтернатива стрелке вниз)
                    self.active_menu_item = "Menu"
                    self.menu_navigation_index = 0
                elif selected == "FREE PLAY":
                    # === ИСПРАВЛЕННАЯ ЛОГИКА: ПРОВЕРЯЕМ КАМПАНИЮ ТОЛЬКО ДЛЯ FREE PLAY ===
                    if self.state.campaign_mode and not self.state.campaign_completed:
                        self.show_exit_campaign_confirmation()
                    else:
                        # Обычная логика для FREE PLAY
                        self.active_menu_item = "FREE PLAY"
                        self.level_navigation_index = self.current_difficulty - 1
                elif selected == "CAMPAIGN":
                    # Если мы в Free Play - показываем диалог подтверждения перехода в кампанию
                    if not self.state.campaign_mode:
                        self.show_enter_campaign_confirmation()
                        return
                    # Универсальная обработка кампании
                    self.handle_campaign_interaction(current_time)
                elif selected == "Instructions":
                    self.active_menu_item = None
                    self.menu_open_with_keyboard = False
                    self.show_overlay_text = self.instruction_text
                    # Устанавливаем паузу для инструкций и сбрасываем тип паузы по пробелу
                    self.state.game_paused = True
                    self.state.pause_type = None
                    self.state.pause_start_time = current_time
                elif selected == "About":
                    self.active_menu_item = None
                    self.menu_open_with_keyboard = False
                    self.show_overlay_text = self.about_text
                    # Устанавливаем паузу для информации "О программе" и сбрасываем тип паузы по пробелу
                    self.state.game_paused = True
                    self.state.pause_type = None
                    self.state.pause_start_time = current_time
                return

        # === ВОСЬМОЙ ПРИОРИТЕТ: ПЕРЕКЛЮЧЕНИЕ РЕЖИМОВ TAB ===
        if event.key == pygame.K_TAB:
            if (not self.active_menu_item and 
                not self.menu_open_with_keyboard and 
                not self.show_overlay_text and
                not self.state.show_combined_dialog and
                not self.state.show_exit_campaign_dialog and
                not self.state.show_enter_campaign_dialog):
                self.toggle_editor_mode()
                return

    def execute_menu_action(self):
        """Выполнение выбранного действия в меню"""
        current_time = time.time()
        menu_actions = [
            {"name": "New Game", "action": lambda: self.reset_game()},
            {"name": "Save Game", "action": lambda: self.show_save_game_dialog()},
            {"name": "Load Game", "action": lambda: self.show_load_game_dialog()},
            {"name": "Edit Map", "action": lambda: self.toggle_editor_mode()},
            {"name": "Sound", "action": lambda: self.toggle_sound()},
            {"name": "Game Speed", "action": lambda: self.toggle_fps()},
            {"name": "Spiders Speed", "action": lambda: self.toggle_spider_speed()},
            {"name": "Timer", "action": lambda: self.toggle_time_timer()},
            {"name": "Save Map", "action": lambda: self.show_save_dialog_handler()},
            {"name": "Load Map", "action": lambda: self.show_load_dialog_handler()},
            {"name": "Exit", "action": lambda: self.quit_game()}
        ]
        
        if 0 <= self.menu_navigation_index < len(menu_actions):
            action = menu_actions[self.menu_navigation_index]["action"]
            action()
        
        # Закрываем меню только для определенных действий
        if self.menu_navigation_index not in [1, 2, 4, 5, 6, 7, 8, 9]:  # Не закрываем для диалогов 1,2-Save/Load Game, 4-Sound, 5—Speed 6-Timer,7-spider Speed, 8,9—Save/Load Map
            # ПРИ ЯВНОМ ВЫБОРЕ "NEW GAME" СБРАСЫВАЕМ СЧЕТЧИК КАРТ
            if self.menu_navigation_index == 0:
                self.state.maps_completed = 0

            self.close_all_interfaces_and_resume(current_time)

    def update_game_state(self):
        """Обновление состояния игры с новым таймером-секундомером"""
        current_time = time.time()

        # === ЕСЛИ ИГРА НЕ НА ПАУЗЕ - ЗАКРЫВАЕМ МЕНЮ ===
        if not self.should_pause_game_logic() and (self.active_menu_item or self.menu_open_with_keyboard):
            self.active_menu_item = None
            self.menu_open_with_keyboard = False

        # ПРОСТАЯ ОСТАНОВКА ВСЕЙ ИГРЫ В РЕДАКТОРЕ ПРИ ВЫБОРЕ ИНСТРУМЕНТА
        if self.state.game_mode == 'editor' and self.selected_tool is not None:
            return  # Выходим из метода - ВСЁ останавливается

        # Обновляем игру только если НЕ должна быть пауза
        if self.should_pause_game_logic():
            return

        # Обновляем перемещение по клику мыши (ДО обработки клавиш!)
        self.update_mouse_movement(current_time)

        # Сброс указателя пути через 10 секунд
        if self.state.show_path and self.state.path_hide_time and current_time > self.state.path_hide_time:
            self.state.show_path = False
            self.state.path_hide_time = None

        # Определяем, должен ли таймер работать
        should_timer_run = (
            not self.should_pause_game_logic() and
            self.state.game_mode in ['game', 'editor']
        )
        
        # Управление состоянием таймера
        if should_timer_run and not self.state.timer_active and self.state.time_timer_enabled:
            # Запускаем таймер
            self.state.timer_active = True
            self.state.last_second_time = current_time
            
        elif not should_timer_run and self.state.timer_active:
            # Останавливаем таймер
            self.state.timer_active = False
        
        # Логика секундомера: вычитаем по 1 секунде
        if self.state.timer_active and self.state.time_timer_enabled:
            time_since_last_second = current_time - self.state.last_second_time
            
            if time_since_last_second >= 1.0:  # Прошла 1 секунда
                self.state.time_timer -= 1.0
                self.state.last_second_time = current_time
                
                # Проверка окончания времени
                if self.state.time_timer <= 0:
                    self.state.time_timer = 0
                    self.state.timer_active = False
                    if self.sound_enabled and self.resource_manager.sounds.get('game_over'):
                        game_over_channel = pygame.mixer.Channel(3)
                        game_over_channel.play(self.resource_manager.sounds['game_over'])
                    self.state.game_over = True
        
        # Анимация пауков
        if current_time - self.last_spider_image_change_time >= self.config.SPIDER_ANIMATION_SPEED / 2000:
            self.current_spider_image_index = 1 - self.current_spider_image_index
            self.last_spider_image_change_time = current_time

        # Анимация указателей пути
        if current_time - self.last_map_pointer_change_time >= self.MAP_POINTER_ANIMATION_SPEED / 1000:
            self.current_map_pointer_index = 1 - self.current_map_pointer_index
            self.last_map_pointer_change_time = current_time
        
        # Движение игрока от клавиш (только если нет активного перемещения мышью)
        if not self.mouse_move_path and current_time - self.last_move_time >= self.move_delay:
            keys = pygame.key.get_pressed()
            moved = False
            interaction = False
            
            # Сбрасываем состояние движения перед проверкой клавиш
            self.player.is_moving = False
            
            # Объединяем стрелки и WASD
            # Влево: LEFT или A
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:            
                moved = self.player.move(0, -1, self.maze)
                if not moved:
                    interaction = self.check_wall_interaction(0, -1)
                self.player.direction = 'left'
            # Вправо: RIGHT или D
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                moved = self.player.move(0, 1, self.maze)
                if not moved:
                    interaction = self.check_wall_interaction(0, 1)
                self.player.direction = 'right'
            # Вверх: UP или W
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                moved = self.player.move(-1, 0, self.maze)
                if not moved:
                    interaction = self.check_wall_interaction(-1, 0)
            # Вниз: DOWN или S
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                moved = self.player.move(1, 0, self.maze)
                if not moved:
                    interaction = self.check_wall_interaction(1, 0)
            
            self.player.is_moving = moved or interaction
            
            if (moved or interaction) and self.resource_manager.sounds.get('move') and self.sound_enabled:
                move_channel = pygame.mixer.Channel(1)
                if not move_channel.get_busy():
                    move_channel.play(self.resource_manager.sounds['move'])
            
            self.last_move_time = current_time
        
        # Движение пауков (только в игровом режиме)
        self.spider_move_counter += 1
        if self.spider_move_counter % self.spider_speed == 0:
            self.move_spiders()
        
        # Проверка столкновений с пауками
        self.check_spider_collisions()

        # Проверка победы
        if self.player.has_treasure and self.player.x == self.config.HOUSE_X and self.player.y == self.config.HOUSE_Y:
            self.state.game_won = True
            self.start_win_animation()
            # НАЧИСЛЕНИЕ ОЧКОВ ЗА ДОСТАВКУ КЛАДА
            self.add_score(10, "Treasure In")
            self.state.maps_completed += 1  # УВЕЛИЧИВАЕМ СЧЕТЧИК КАРТ

            # ОБРАБОТКА КАМПАНИИ
            if self.state.campaign_mode and not self.state.campaign_completed:
                self.handle_campaign_win()
        
        if self.check_all_spiders_defeated():
            self.state.game_won = True
            self.start_win_animation()
            self.state.maps_completed += 1

            # ОБРАБОТКА КАМПАНИИ
            if self.state.campaign_mode and not self.state.campaign_completed:
                self.handle_campaign_win()
        
        # Обновление анимации победы (работает даже при паузе)
        if self.state.game_won:
            self.update_win_animation()

    def check_spider_collisions(self):
        """Проверка столкновений с пауками (работает в обоих режимах)"""
        for spider in self.maze.spiders:
            if not spider.defeated:
                spider_pos = (spider.x, spider.y)
                
                if ((self.player.x, self.player.y) == spider_pos or 
                    ((self.player.x, self.player.y) == spider.old_pos and 
                    (self.player.x, self.player.y) != (spider.x, spider.y))):
                    
                    if self.player.has_sword:
                        # Воспроизводим звук меча при убийстве паука
                        if self.sound_enabled and self.resource_manager.sounds.get('sword'):
                            sword_channel = pygame.mixer.Channel(2)
                            sword_channel.play(self.resource_manager.sounds['sword'])

                        spider.defeated = True
                        spider.defeated_time = time.time()
                        self.player.has_sword = False

                        # НАЧИСЛЕНИЕ ОЧКОВ ЗА УБИЙСТВО ПАУКА
                        self.add_score(1, "Spider kill")

                    else:
                        # === GOD MODE: бессмертие ===
                        if self.state.god_mode:
                            # Вместо смерти - убиваем паука без меча
                            self.set_editor_message("GOD MODE: Spider crushed!")
                            spider.defeated = True
                            spider.defeated_time = time.time()
                            self.add_score(1, "God mode kill")
                            continue  # Пропускаем остальную логику смерти
                        # === КОНЕЦ GOD MODE ===

                        # Воспроизводим звук проигрыша при смерти
                        if self.sound_enabled and self.resource_manager.sounds.get('game_over'):
                            game_over_channel = pygame.mixer.Channel(3)
                            game_over_channel.play(self.resource_manager.sounds['game_over'])

                        self.state.show_death_image = True
                        self.state.game_over = True
                        
                        self.reset_score() # СБРОС ОЧКОВ ПРИ ПРОИГРЫШЕ
                        self.state.maps_completed = 0  # СБРАСЫВАЕМ СЧЕТЧИК КАРТ

                        break

    # Метод Проверяет, все ли пауки побеждены
    def check_all_spiders_defeated(self):
        for spider in self.maze.spiders:
            if not spider.defeated:
                return False
        return True

    def find_path_to_follow(self):
        """Поиск пути для отображения"""
        path_to_follow = []
        
        if self.state.show_path:
            # В режиме редактора показываем путь как в игре
            if self.state.game_mode == 'editor':
                if self.player.has_treasure:
                    # Если в редакторе "игрок" с кладом - путь к дому
                    path_to_follow = self.find_path_bfs(
                        (self.player.x, self.player.y), 
                        lambda pos: pos == (self.config.HOUSE_X, self.config.HOUSE_Y)
                    )
                elif self.maze.treasure_position:
                    # Если в редакторе "игрок" без клада - путь к ближайшей проходимой клетке рядом с кладом
                    tx, ty = self.maze.treasure_position
                    possible_paths = []
                    
                    # Ищем все проходимые клетки вокруг клада
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = tx + dx, ty + dy
                        if (0 <= nx < len(self.maze.grid) and 
                            0 <= ny < len(self.maze.grid[0]) and 
                            self.maze.grid[nx][ny] == 0):
                            possible_paths.append((nx, ny))
                    
                    # Если есть проходимые клетки рядом с кладом, находим ближайшую к игроку
                    if possible_paths:
                        min_distance = float('inf')
                        closest_path = None
                        
                        for path_cell in possible_paths:
                            distance = abs(path_cell[0] - self.player.x) + abs(path_cell[1] - self.player.y)
                            if distance < min_distance:
                                min_distance = distance
                                closest_path = path_cell
                        
                        if closest_path:
                            path_to_follow = self.find_path_bfs(
                                (self.player.x, self.player.y), 
                                lambda pos: pos == closest_path
                            )
            
            # В игровом режиме используем обычную логику
            elif self.state.game_mode == 'game':
                if self.player.has_treasure:
                    # Если игрок с кладом - путь к дому
                    path_to_follow = self.find_path_bfs(
                        (self.player.x, self.player.y), 
                        lambda pos: pos == (self.config.HOUSE_X, self.config.HOUSE_Y)
                    )
                elif self.maze.treasure_position:
                    # Если игрок без клада - путь к ближайшей проходимой клетке рядом с кладом
                    tx, ty = self.maze.treasure_position
                    possible_paths = []
                    
                    # Ищем все проходимые клетки вокруг клада
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = tx + dx, ty + dy
                        if (0 <= nx < len(self.maze.grid) and 
                            0 <= ny < len(self.maze.grid[0]) and 
                            self.maze.grid[nx][ny] == 0):
                            possible_paths.append((nx, ny))
                    
                    # Если есть проходимые клетки рядом с кладом, находим ближайшую к игроку
                    if possible_paths:
                        min_distance = float('inf')
                        closest_path = None
                        
                        for path_cell in possible_paths:
                            distance = abs(path_cell[0] - self.player.x) + abs(path_cell[1] - self.player.y)
                            if distance < min_distance:
                                min_distance = distance
                                closest_path = path_cell
                        
                        if closest_path:
                            path_to_follow = self.find_path_bfs(
                                (self.player.x, self.player.y), 
                                lambda pos: pos == closest_path
                            )
        
        return path_to_follow
    
    def toggle_sound(self):
        """Переключение состояния звука"""
        self.sound_enabled = not self.sound_enabled
        
        # Применяем настройки звука
        if self.sound_enabled:
            # Включаем звук
            pygame.mixer.unpause()
        else:
            # Выключаем звук
            pygame.mixer.pause()
        
        # Сообщение о состоянии звука
        self.set_editor_message(f"Sound {'enabled' if self.sound_enabled else 'disabled'}")

    def toggle_time_timer(self):
        """Переключение режима таймера жизни !!! """
        self.state.time_timer_enabled = not self.state.time_timer_enabled
        
        # Сбрасываем таймер при включении/выключении
        if self.state.time_timer_enabled:
            self.state.time_timer = self.config.time_TIMER_MAX
            self.state.timer_active = True
        else:
            self.state.timer_active = False
        
        self.set_editor_message(f"Timer: {'ON' if self.state.time_timer_enabled else 'OFF'}")

    def calculate_submenu_width(self, submenu_options):
        """Расчет ширины подменю на основе опций"""
        max_width = 0
        for option in submenu_options:
            text_surf = self.fonts['info'].render(option["name"], True, self.config.WHITE)
            max_width = max(max_width, text_surf.get_width())
        
        min_width = int(150 * self.state.scale_factor)
        max_width = max(max_width, min_width)
        submenu_width = max_width + int(40 * self.state.scale_factor)
        
        return submenu_width

    def set_difficulty(self, level):
        """Установка уровня сложности"""
        if self.state.campaign_mode and not self.state.campaign_completed:
            self.show_exit_campaign_confirmation()
            self.pending_difficulty = level
            return
        
        self.current_difficulty = level
        
        # Обновляем конфигурацию
        self.config.MAZE_WIDTH = DIFFICULTY_LEVELS[level]['MAZE_WIDTH']
        self.config.MAZE_HEIGHT = DIFFICULTY_LEVELS[level]['MAZE_HEIGHT']
        self.config.time_TIMER_MAX = DIFFICULTY_LEVELS[level]['time_TIMER_MAX']
        self.config.time_BONUS_TIME = DIFFICULTY_LEVELS[level]['time_BONUS_TIME']
        
        # Сбрасываем скорость к стандартной для этого уровня, если не использовалась пользовательская
        if not self.state.spider_speed_custom:
            self.spider_speed = DIFFICULTY_LEVELS[level]['spider_SPEED']
        
        # ПЕРЕСОЗДАЕМ лабиринт с новыми размерами
        self.maze = Maze(self.config.MAZE_WIDTH, self.config.MAZE_HEIGHT)
        
        # Сбрасываем кэш размеров
        self.cached_maze_dimensions = None
        
        # СБРОС ПЕРЕМЕЩЕНИЯ МЫШЬЮ
        self.mouse_move_target = None
        self.mouse_move_path = []
        self.mouse_move_index = 0
        self.mouse_move_take_item = False
        self.mouse_move_item_to_take = None
        self.player.is_moving = False
        
        # === ПЕРЕЗАПУСКАЕМ ИГРУ С СОХРАНЕНИЕМ СТИЛЯ СТЕНЫ ===
        self.reset_game(keep_wall_style=True)  # <-- Сохраняем стиль стены
        
        speed_text = f" (custom: {self.spider_speed})" if self.state.spider_speed_custom else ""
        self.set_editor_message(f"Level: {DIFFICULTY_LEVELS[level]['NAME']}{speed_text}")

    def draw_menu_submenu(self):
        """Отрисовка подменю Menu и Level"""
        if self.active_menu_item not in ["Menu", "FREE PLAY"]:
            return
            
        if self.active_menu_item not in self.menu_rects:
            return

        menu_rect = self.menu_rects[self.active_menu_item]
        submenu_x = menu_rect.left
        submenu_y = self.info_panel_height
        submenu_item_height = int(30 * self.state.scale_factor)
        
        # Подменю для Menu
        if self.active_menu_item == "Menu":
            submenu_options = [
                {"name": "New Game", "action": lambda: self.reset_game(keep_wall_style=False)},
                {"name": "Save Game", "action": lambda: self.show_save_game_dialog()},
                {"name": "Load Game", "action": lambda: self.show_load_game_dialog()},
                {"name": "Edit Map", "action": lambda: self.toggle_editor_mode()},
                {"name": "Sound: ON" if self.sound_enabled else "Sound: OFF", "action": lambda: self.toggle_sound()},
                {"name": f"Game Speed: {self.FPS}", "action": lambda: self.toggle_fps()},
                {"name": f"Spiders Speed: {self.spider_speed}", "action": lambda: self.toggle_spider_speed()},
                {"name": f"Timer: {'ON' if self.state.time_timer_enabled else 'OFF'}", "action": lambda: self.toggle_time_timer()},  
                {"name": "Save Map", "action": lambda: self.show_save_dialog_handler()},
                {"name": "Load Map", "action": lambda: self.show_load_dialog_handler()},
                {"name": "Exit", "action": lambda: self.quit_game()}
            ]
        
        # Подменю для FREE PLAY
        elif self.active_menu_item == "FREE PLAY":
            submenu_options = [
                {"name": "Easy", "action": lambda: self.set_difficulty(1), "level": 1},
                {"name": "Normal", "action": lambda: self.set_difficulty(2), "level": 2},
                {"name": "Hard", "action": lambda: self.set_difficulty(3), "level": 3},
                {"name": "Challenging", "action": lambda: self.set_difficulty(4), "level": 4},
                {"name": "Difficult", "action": lambda: self.set_difficulty(5), "level": 5},
                {"name": "Extreme", "action": lambda: self.set_difficulty(6), "level": 6},
                {"name": "Nightmare", "action": lambda: self.set_difficulty(7), "level": 7}
            ]

        # Вычисляем ширину через общий метод
        submenu_width = self.calculate_submenu_width(submenu_options)
        submenu_height = len(submenu_options) * submenu_item_height
        submenu_rect = pygame.Rect(submenu_x, submenu_y, submenu_width, submenu_height)
        pygame.draw.rect(self.screen, self.config.MENU_BAR_COLOR, submenu_rect)
        pygame.draw.rect(self.screen, self.config.WHITE, submenu_rect, 1)
        
        # Рисуем пункты подменю
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(submenu_options):
            item_rect = pygame.Rect(submenu_x, submenu_y + (i * submenu_item_height), 
                                submenu_width, submenu_item_height)
            
            # Унифицированная логика подсветки для мыши и клавиатуры
            if self.active_menu_item == "Menu":
                is_selected_by_keyboard = (self.menu_open_with_keyboard and i == self.menu_navigation_index)
                is_current_item = False
            else:  # Level
                is_selected_by_keyboard = (self.menu_open_with_keyboard and i == self.level_navigation_index)
                is_current_item = (option.get("level") == self.current_difficulty)
            
            is_mouse_hover = item_rect.collidepoint(mouse_pos)
            
            # ОБНОВЛЯЕМ индекс навигации при наведении мыши
            if is_mouse_hover and self.menu_open_with_keyboard:
                if self.active_menu_item == "Menu":
                    self.menu_navigation_index = i
                else:  # Level
                    self.level_navigation_index = i
            
            # Подсветка для выбранного пункта или текущего уровня
            if is_selected_by_keyboard or is_mouse_hover or is_current_item:
                pygame.draw.rect(self.screen, self.config.BLUE, item_rect)
                pygame.draw.rect(self.screen, self.config.YELLOW, item_rect, 2)
            
            # Цвет текста
            if is_selected_by_keyboard or is_mouse_hover:
                text_color = self.config.YELLOW
            elif is_current_item:
                text_color = self.config.LIGHT_GREEN
            else:
                text_color = self.config.WHITE
            
            display_text = option["name"]
            if self.active_menu_item == "FREE PLAY" and is_current_item:
                display_text = "-> " + display_text
            
            text = self.fonts['info'].render(display_text, True, text_color)
            text_rect = text.get_rect(center=item_rect.center)
            self.screen.blit(text, text_rect)

    def draw_overlay_text(self):
        """Отрисовка текста поверх игры (инструкция, о программе)"""
        if not self.show_overlay_text:
            return
            
        # Определяем размеры окна на основе количества строк
        num_lines = len(self.show_overlay_text)
        overlay_width = int(600 * self.state.scale_factor)  # Фиксированная ширина
        overlay_height = int(40 * self.state.scale_factor) + (num_lines * int(30 * self.state.scale_factor))  # Высота зависит от количества строк
        
        overlay_x = (self.config.SCREEN_WIDTH - overlay_width) // 2
        overlay_y = (self.config.SCREEN_HEIGHT - overlay_height) // 2
        
        # Создаем полупрозрачный фон
        overlay = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Более темный фон для лучшей читаемости
        pygame.draw.rect(overlay, self.config.WHITE, (0, 0, overlay_width, overlay_height), 2)
        
        self.screen.blit(overlay, (overlay_x, overlay_y))
        
        # Рисуем текст внутри уменьшенного окна
        text_y = overlay_y + int(25 * self.state.scale_factor)
        for line in self.show_overlay_text:
            text_surface = self.fonts['info'].render(line, True, self.config.WHITE)
            text_rect = text_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, text_y))
            self.screen.blit(text_surface, text_rect)
            text_y += int(30 * self.state.scale_factor)
        
        # Рисуем кнопку закрытия внутри окна
        close_text = self.fonts['info'].render("Press ESC to return", True, self.config.YELLOW)
        close_rect = close_text.get_rect(center=(self.config.SCREEN_WIDTH // 2, 
                                            overlay_y + overlay_height - int(20 * self.state.scale_factor)))
        self.screen.blit(close_text, close_rect)

    def draw_score_display(self):
        """Отрисовка счета и информации о режиме игры в правом верхнем углу"""
        
        if self.state.campaign_mode and not self.state.campaign_completed:
            # === РЕЖИМ КАМПАНИИ ===
            level_names = {1: "Easy", 2: "Normal", 3: "Hard", 4: "Challenging", 
                        5: "Difficult", 6: "Extreme", 7: "Nightmare"}
            
            # Текст для кампании
            campaign_part = f"CAMPAIGN: {level_names[self.state.campaign_level]} ({self.state.campaign_wins}/3)"
            score_part = f" Score: {self.state.current_score}"
            high_part = f" High: {self.state.high_score}"
            
            # Создаем поверхности
            campaign_surface = self.fonts['menu'].render(campaign_part, True, self.config.LIGHT_GREEN)
            score_surface = self.fonts['menu'].render(score_part, True, self.config.YELLOW)
            high_surface = self.fonts['menu'].render(high_part, True, self.config.LIGHT_GREEN)
            
            # Вычисляем позиции
            total_width = campaign_surface.get_width() + score_surface.get_width() + high_surface.get_width()
            start_x = self.config.SCREEN_WIDTH - total_width - 10  # Отступ от правого края
            
            # РАСЧЕТ ВЫСОТЫ С УЧЕТОМ МАСШТАБА
            text_y = int(12 * self.state.scale_factor)
            
            # Отрисовываем
            self.screen.blit(campaign_surface, (start_x, text_y))
            self.screen.blit(score_surface, (start_x + campaign_surface.get_width(), text_y))
            self.screen.blit(high_surface, (start_x + campaign_surface.get_width() + score_surface.get_width(), text_y))
            
        elif self.state.campaign_mode and self.state.campaign_completed:
            # === КАМПАНИЯ ЗАВЕРШЕНА ===
            completed_part = "CAMPAIGN: COMPLETED!"
            score_part = f" Score: {self.state.current_score}"
            high_part = f" High: {self.state.high_score}"
            
            # Создаем поверхности
            completed_surface = self.fonts['menu'].render(completed_part, True, self.config.LIGHT_GREEN)
            score_surface = self.fonts['menu'].render(score_part, True, self.config.YELLOW)
            high_surface = self.fonts['menu'].render(high_part, True, self.config.LIGHT_GREEN)
            
            # Вычисляем позиции
            total_width = completed_surface.get_width() + score_surface.get_width() + high_surface.get_width()
            start_x = self.config.SCREEN_WIDTH - total_width - 10
            
            text_y = int(12 * self.state.scale_factor)
            
            # Отрисовываем
            self.screen.blit(completed_surface, (start_x, text_y))
            self.screen.blit(score_surface, (start_x + completed_surface.get_width(), text_y))
            self.screen.blit(high_surface, (start_x + completed_surface.get_width() + score_surface.get_width(), text_y))
            
        else:
            # === СВОБОДНАЯ ИГРА (FREE PLAY) ===
            level_name = DIFFICULTY_LEVELS[self.current_difficulty]['NAME']
            
            # Текст для свободной игры
            map_part = f"FREE PLAY: {level_name} Map: {self.state.maps_completed + 1}"
            score_part = f" Score: {self.state.current_score}"
            high_part = f" High: {self.state.high_score}"
            
            # Создаем поверхности
            map_surface = self.fonts['menu'].render(map_part, True, self.config.LIGHT_GREEN)
            score_surface = self.fonts['menu'].render(score_part, True, self.config.YELLOW)
            high_surface = self.fonts['menu'].render(high_part, True, self.config.LIGHT_GREEN)
            
            # Вычисляем позиции
            total_width = map_surface.get_width() + score_surface.get_width() + high_surface.get_width()
            start_x = self.config.SCREEN_WIDTH - total_width - 10
            
            text_y = int(12 * self.state.scale_factor)
            
            # Отрисовываем
            self.screen.blit(map_surface, (start_x, text_y))
            self.screen.blit(score_surface, (start_x + map_surface.get_width(), text_y))
            self.screen.blit(high_surface, (start_x + map_surface.get_width() + score_surface.get_width(), text_y))

    def set_editor_message(self, message):
        """Установка сообщения редактора с временной меткой"""
        self.editor_message = message
        self.editor_message_time = time.time()

    def draw_ui(self):
        """Отрисовка пользовательского интерфейса"""
        # Отрисовка комбинированного диалога файлов
        if self.state.show_combined_dialog:
            self.draw_combined_dialog()

        # Отрисовка диалога выхода из кампании
        if self.state.show_exit_campaign_dialog:
            self.draw_exit_campaign_dialog()
        
        # Отрисовка диалога входа в кампанию
        if self.state.show_enter_campaign_dialog:
            self.draw_enter_campaign_dialog()

        # Отрисовка информационной панели
        pygame.draw.rect(self.screen, self.config.MENU_BAR_COLOR, (0, 0, self.config.SCREEN_WIDTH, self.info_panel_height))

        # === ДОБАВИТЬ: Отрисовка сообщения с белой рамкой ===
        if self.editor_message and time.time() - self.editor_message_time < 3:
            message_text = self.fonts['info'].render(self.editor_message, True, self.config.YELLOW)
            message_x = (self.config.SCREEN_WIDTH - message_text.get_width()) // 2
            message_y = self.info_panel_height + int(5 * self.state.scale_factor)
            
            # Фон с белой рамкой (как в окне Instructions)
            bg_width = message_text.get_width() + 20
            bg_height = message_text.get_height() + 10
            bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            pygame.draw.rect(bg_surface, self.config.WHITE, (0, 0, bg_width, bg_height), 1)
            
            self.screen.blit(bg_surface, (message_x - 10, message_y - 5))
            self.screen.blit(message_text, (message_x, message_y))

        # ОТРИСОВКА ОЧКОВ В ПРАВОМ ВЕРХНЕМ УГЛУ
        self.draw_score_display()
        
        # Отрисовка меню
        menu_item_x = int(10 * self.state.scale_factor)
        self.menu_rects = {}
        
        for i, item in enumerate(self.menu_items):
            display_text = item
                
            # Определяем цвет текста в зависимости от активного элемента
            is_active_horizontally = (self.menu_open_with_keyboard and i == self.horizontal_nav_index)
            
            # Проверяем, находится ли мышь над пунктом меню
            mouse_pos = pygame.mouse.get_pos()
            text_surface = self.fonts['menu'].render(display_text, True, self.config.MENU_ITEM_COLOR)
            text_rect = text_surface.get_rect(topleft=(menu_item_x, (self.info_panel_height - text_surface.get_height()) // 2))
            
            # Подсветка при наведении мыши такая же как при клавиатурной навигации
            is_mouse_hover = text_rect.collidepoint(mouse_pos)
            
            # active_menu_item может быть только "Menu" или "FREE PLAY", поэтому проверяем строгое соответствие
            is_current_active_menu = False
            if self.active_menu_item == "Menu" and item == "Menu":
                is_current_active_menu = True
            elif self.active_menu_item == "FREE PLAY" and item == "FREE PLAY":
                is_current_active_menu = True
            
            # Подсвечиваем меню (открытое подменю)
            should_highlight = (
                (is_active_horizontally and not self.active_menu_item) or 
                is_mouse_hover or 
                is_current_active_menu
            )
            
            if should_highlight:
                # Подсвечиваем фон для активного элемента (клавиатура или мышь)
                text_surface = self.fonts['menu'].render(display_text, True, self.config.YELLOW)
                # Рисуем подсветку фона
                highlight_rect = pygame.Rect(
                    menu_item_x - int(5 * self.state.scale_factor),
                    int(2 * self.state.scale_factor),
                    text_surface.get_width() + int(10 * self.state.scale_factor),
                    self.info_panel_height - int(4 * self.state.scale_factor)
                )
                pygame.draw.rect(self.screen, self.config.BLUE, highlight_rect)
                pygame.draw.rect(self.screen, self.config.YELLOW, highlight_rect, 2)
            else:
                text_surface = self.fonts['menu'].render(display_text, True, self.config.MENU_ITEM_COLOR)
            
            text_rect = text_surface.get_rect(topleft=(menu_item_x, (self.info_panel_height - text_surface.get_height()) // 2))
            self.menu_rects[item] = text_rect
            self.screen.blit(text_surface, text_rect)
            menu_item_x += text_rect.width + int(20 * self.state.scale_factor)

        # Отрисовка подменю если активно
        if self.active_menu_item in ["Menu", "FREE PLAY"]:
            self.draw_menu_submenu()
        
        separator_x = self.visible_maze_width
        separator_width = int(2 * self.state.scale_factor)
        pygame.draw.rect(self.screen, self.config.SEPARATOR_COLOR, 
                        (separator_x, self.info_panel_height, separator_width, 
                        self.config.SCREEN_HEIGHT - self.info_panel_height))
        
        ui_panel_x = self.visible_maze_width + separator_width
        ui_panel_rect = pygame.Rect(ui_panel_x, self.info_panel_height, 
                                self.ui_panel_width - separator_width, 
                                self.config.SCREEN_HEIGHT - self.info_panel_height)
        pygame.draw.rect(self.screen, self.config.BAR_BACKGROUND, ui_panel_rect)
        
        self.draw_unified_ui(ui_panel_x, self.state.game_mode)

        # ========== GOD MODE В ЦЕНТРЕ ВЕРХНЕЙ ПАНЕЛИ ==========
        if self.state.god_mode:
            god_text = self.fonts['ui_header'].render("GOD MODE", True, self.config.GOLD)
            god_x = (self.config.SCREEN_WIDTH - god_text.get_width()) // 2
            god_y = (self.info_panel_height - god_text.get_height()) // 2
            
            # Полупрозрачный золотой фон
            bg_rect = pygame.Rect(
                god_x - 15,
                god_y - 5,
                god_text.get_width() + 30,
                god_text.get_height() + 10
            )
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((255, 215, 0, 40))
            pygame.draw.rect(bg_surface, self.config.GOLD, (0, 0, bg_rect.width, bg_rect.height), 1)
            self.screen.blit(bg_surface, bg_rect)
            
            self.screen.blit(god_text, (god_x, god_y))
        # =====================================================

        # Отрисовка сообщения о паузе по пробелу
        if (self.state.game_paused and 
            self.state.pause_type == 'space_pause' and 
            self.state.game_mode in ['game', 'editor']):
            self.draw_pause_message()
        
        # Отрисовка оверлеев (инструкция, о программе, описание кампании)
        if self.show_overlay_text:
            self.draw_overlay_text()

        # Отрисовка сообщений о состоянии игры
        if self.state.game_over:
            self.draw_game_over_message()
        elif self.state.game_won:
            self.draw_win_message()

    def draw_unified_ui(self, ui_panel_x, mode):
        """Универсальное боковое меню для игры и редактора - ОПТИМИЗИРОВАННАЯ ВЕРСИЯ"""
        # Обновляем кэш текстов UI
        self.update_ui_text_cache()
        
        # Локальные переменные для быстрого доступа
        screen = self.screen
        config = self.config
        fonts = self.fonts
        scale_factor = self.state.scale_factor
        
        # Предварительные вычисления размеров
        header_y = self.info_panel_height + int(25 * scale_factor)
        time_y = self.info_panel_height + int(55 * scale_factor)
        icons_start_y = self.info_panel_height + int(80 * scale_factor)
        
        # Кэширование заголовков
        header_key = f"header_{mode}"
        if header_key not in self.ui_text_cache:
            header_text = "MAP/EDITOR" if mode == 'editor' else "GAME"
            self.ui_text_cache[header_key] = fonts['ui_header'].render(header_text, True, config.WHITE)
        
        header_text_surface = self.ui_text_cache[header_key]
        header_rect = header_text_surface.get_rect(center=(ui_panel_x + (self.ui_panel_width - 2) // 2, header_y))
        screen.blit(header_text_surface, header_rect)
        
        # Кэширование текста времени жизни с проверкой изменений
        current_time_text = f"Time: {int(self.state.time_timer)}s" if self.state.time_timer_enabled else "Time: OFF"
        time_cache_key = f"time_{current_time_text}"
        
        if time_cache_key not in self.ui_text_cache:
            if self.state.time_timer_enabled:
                time_color = config.LIGHT_GREEN if self.state.time_timer > 180 else config.TOMATO
            else:
                time_color = config.GREY  # Серый цвет когда таймер выключен
            self.ui_text_cache[time_cache_key] = fonts['ui_header'].render(current_time_text, True, time_color)
            # Удаляем старые кэшированные версии таймера
            for key in list(self.ui_text_cache.keys()):
                if key.startswith('time_') and key != time_cache_key:
                    del self.ui_text_cache[key]
        
        time_text_surface = self.ui_text_cache[time_cache_key]
        time_rect = time_text_surface.get_rect(center=(ui_panel_x + (self.ui_panel_width - 2) // 2, time_y))
        screen.blit(time_text_surface, time_rect)
       
        # Предварительные вычисления размеров иконок
        base_icon_size = int(config.ORIGINAL_UI_PANEL_WIDTH * 0.8 * (1.0 / 3.0) * scale_factor)
        icon_size = int(base_icon_size * 1.5)
        padding = int(self.ui_panel_width * 0.095)
        text_padding = int(5 * scale_factor)
        
        # Предварительные вычисления счетчиков объектов
        object_counts = {
            'sword': len(self.maze.swords_positions),
            'time': len(self.maze.times_positions),
            'pointer': len(self.maze.path_pointers_positions),
            'spider': len([h for h in self.maze.spiders if not h.defeated]),
            'treasure': 1 if self.maze.treasure_position else 0,
            'house': 1,
            'wall': " ",
            'door': len(getattr(self.maze, 'extra_paths', set())),
            'path': " "
        }
        
        # Кэширование текстов счетчиков
        count_texts = {}
        for tool_name, count in object_counts.items():
            count_key = f"count_{tool_name}_{count}"
            if count_key not in self.ui_text_cache:
                count_texts[tool_name] = fonts['info'].render(f"{count}", True, config.LIGHT_YELLOW)
                self.ui_text_cache[count_key] = count_texts[tool_name]
            else:
                count_texts[tool_name] = self.ui_text_cache[count_key]
        
        # Сохраняем rect'ы для обработки кликов
        ui_rects = {}
        
        # Единый цикл отрисовки иконок с предварительными вычислениями
        for i, tool_name in enumerate(self.editor_tools):
            # Вычисление позиции иконки
            icon_y = icons_start_y + i * (icon_size + padding)
            icon_rect = pygame.Rect(ui_panel_x + padding, icon_y, icon_size, icon_size)
            ui_rects[tool_name] = icon_rect
            
            # Отрисовка рамки иконки
            border_color = config.DARK_GREEN if (mode == 'editor' and self.selected_tool == tool_name) else config.WHITE
            pygame.draw.rect(screen, border_color, icon_rect, 2)
            
            # Отрисовка иконки
            icon_image = self.resource_manager.editor_ui_icons.get(tool_name)
            if icon_image:
                # Кэширование масштабированных иконок
                icon_cache_key = f"icon_{tool_name}_{icon_size}"
                if icon_cache_key not in self.resource_manager.scaled_images:
                    self.resource_manager.scaled_images[icon_cache_key] = pygame.transform.scale(
                        icon_image, (icon_size - 8, icon_size - 8)
                    )
                scaled_icon = self.resource_manager.scaled_images[icon_cache_key]
                screen.blit(scaled_icon, (icon_rect.x + 4, icon_rect.y + 4))
            else:
                pygame.draw.rect(screen, config.GREY, icon_rect.inflate(-4, -4))
            
            # Позиции текста
            info_x = icon_rect.right + text_padding + 5
            name_y = icon_rect.y + icon_size // 4 + 2
            count_y = icon_rect.y + 2 * icon_size // 3 + 4
            
            # Название инструмента из кэша
            tool_cache_key = f"tool_{tool_name}"
            if tool_cache_key in self.ui_text_cache:
                name_text = self.ui_text_cache[tool_cache_key]
            else:
                tool_display_name = {"wall": "Wall", "door": "Door", "path": "Path", "sword": "Sword", 
                                "time": "Time", "pointer": "Pointer", "spider": "Spider",
                                "treasure": "Treasure", "house": "House"}.get(tool_name, tool_name)
                name_text = fonts['info'].render(tool_display_name, True, config.WHITE)
                self.ui_text_cache[tool_cache_key] = name_text
            
            name_rect = name_text.get_rect(midleft=(info_x, name_y))
            screen.blit(name_text, name_rect)
            
            # Количество объектов из кэша
            if tool_name in count_texts:
                count_text = count_texts[tool_name]
                count_rect = count_text.get_rect(midleft=(info_x, count_y))
                screen.blit(count_text, count_rect)
        
        # Предварительные вычисления позиций кнопок
        y_after_icons = icons_start_y + len(self.editor_tools) * (icon_size + padding)
        gap_after_icons = int(1 * scale_factor)
        button_height = int(30 * scale_factor)
        button_gap = int(10 * scale_factor)
        button_width = int(self.ui_panel_width - 20)
        
        # Универсальная функция отрисовки кнопок
        def draw_button(button_key, button_text, button_y, button_color, ui_rects_dict):
            button_rect = pygame.Rect(ui_panel_x + 10, button_y, button_width, button_height)
            pygame.draw.rect(screen, button_color, button_rect)
            pygame.draw.rect(screen, config.WHITE, button_rect, 2)
            
            # Текст кнопки из кэша
            if button_key in self.ui_text_cache:
                text_surface = self.ui_text_cache[button_key]
            else:
                text_surface = fonts['info'].render(button_text, True, config.WHITE)
                self.ui_text_cache[button_key] = text_surface
            
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)
            ui_rects_dict[button_key] = button_rect
            return button_y + button_height + button_gap
        
        # Отрисовка кнопок в зависимости от режима
        current_y = y_after_icons + gap_after_icons
        
        if mode == 'editor':
            current_y = draw_button('save_map', "Save Map", current_y, config.DARK_GREEN, ui_rects)
            current_y = draw_button('load_map', "Load Map", current_y, config.BLUE, ui_rects)
            draw_button('check_map', "Check Map", current_y, config.PURPLE, ui_rects)
        else:
            current_y = draw_button('save_game', "Save Game", current_y, config.DARK_GREEN, ui_rects)
            current_y = draw_button('load_game', "Load Game", current_y, config.BLUE, ui_rects)
            # === ДОБАВЛЯЕМ КНОПКУ Next Wall В РЕЖИМ ИГРЫ !!! ===
            draw_button('cycle_wall', "Next Wall", current_y, config.PURPLE, ui_rects)
        
        # Сохраняем rect'ы в соответствующий атрибут
        if mode == 'editor':
            self.editor_ui_rects = ui_rects
        else:
            self.game_ui_rects = ui_rects

    def draw_game_over_message(self):
        """Отрисовка сообщения о проигрыше"""
        # Тексты сообщений
        game_over_text = 'GAME OVER'
        reason_text = "Hero was killed by a spider or time expired!"
        restart_text = 'Press ENTER to start a new game'
        
        # Вычисляем размеры без создания поверхностей для отрисовки
        game_over_size = self.fonts['text'].size(game_over_text)
        reason_size = self.fonts['info'].size(reason_text)
        restart_size = self.fonts['info'].size(restart_text)
        
        # Вычисляем общую высоту текста с отступами
        text_height = (game_over_size[1] + 
                    reason_size[1] + 
                    restart_size[1] + 
                    int(60 * self.state.scale_factor))  # отступы между строками
        
        text_width = max(game_over_size[0], reason_size[0], restart_size[0])
        
        # Создаем адаптивный фон
        bg_width = text_width + int(80 * self.state.scale_factor)  # отступы по бокам
        bg_height = text_height + int(40 * self.state.scale_factor)  # отступы сверху и снизу
        
        text_background = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        text_background.fill((0, 0, 0, 180))  # черный с прозрачностью
        text_bg_rect = text_background.get_rect(center=(self.visible_maze_width / 2, self.config.SCREEN_HEIGHT / 2))
        
        # Рисуем ободок на поверхности фона
        border_rect = pygame.Rect(0, 0, bg_width, bg_height)
        pygame.draw.rect(text_background, self.config.RED, border_rect, int(3 * self.state.scale_factor))  # красный ободок
        
        self.screen.blit(text_background, text_bg_rect)

        # Мигающий текст "GAME OVER"
        blink_factor = (math.sin(time.time() * 5) + 1) / 2  # от 0 до 1
        color_intensity = int(155 + 100 * blink_factor)
        game_over_color = (255, color_intensity, color_intensity)  # мигающий красный
        
        # Основной текст (создаем поверхность только один раз для отрисовки)
        text_surface = self.fonts['text'].render(game_over_text, True, game_over_color)
        text_rect = text_surface.get_rect(center=(self.visible_maze_width / 2, text_bg_rect.top + int(70 * self.state.scale_factor)))
        self.screen.blit(text_surface, text_rect)
        
        # Дополнительный текст с причиной проигрыша (создаем поверхность только один раз)
        reason_surface = self.fonts['info'].render(reason_text, True, self.config.LIGHT_YELLOW)
        reason_rect = reason_surface.get_rect(center=(self.visible_maze_width / 2, text_rect.bottom + int(30 * self.state.scale_factor)))
        self.screen.blit(reason_surface, reason_rect)
        
        # Инструкция для продолжения (создаем поверхность только один раз)
        restart_surface = self.fonts['info'].render(restart_text, True, self.config.WHITE)
        restart_rect = restart_surface.get_rect(center=(self.visible_maze_width / 2, reason_rect.bottom + int(25 * self.state.scale_factor)))
        self.screen.blit(restart_surface, restart_rect)

    # Отображение варианта победы
    def draw_win_message(self):
        """Отрисовка сообщения о победе с анимацией"""
        # Рисуем частицы
        for particle in self.win_particles:
            pygame.draw.circle(
                self.screen, 
                particle['color'],
                (int(particle['x']), int(particle['y'])),
                int(particle['size'] * self.state.scale_factor)
            )
        
        # Создаем поверхности для текста чтобы вычислить общую высоту
        text_surface = self.fonts['text'].render('YOU WIN!', True, self.config.WHITE)
        if self.player.has_treasure:
            reason_text = "Treasure delivered safely!"
        else:
            reason_text = "All spiders defeated!"
        reason_surface = self.fonts['info'].render(reason_text, True, self.config.LIGHT_YELLOW)
        restart_surface = self.fonts['info'].render('Press ENTER to continue', True, self.config.WHITE)
        
        # Вычисляем общую высоту текста с отступами
        text_height = (text_surface.get_height() + 
                    reason_surface.get_height() + 
                    restart_surface.get_height() + 
                    int(60 * self.state.scale_factor))
        
        text_width = max(text_surface.get_width(), reason_surface.get_width(), restart_surface.get_width())
        
        # Создаем адаптивный фон
        bg_width = text_width + int(80 * self.state.scale_factor)
        bg_height = text_height + int(40 * self.state.scale_factor)
        
        text_background = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        text_background.fill((0, 0, 0, 180))
        text_bg_rect = text_background.get_rect(center=(self.visible_maze_width / 2, self.config.SCREEN_HEIGHT / 2))
        self.screen.blit(text_background, text_bg_rect)

        # Рисуем ободок на поверхности фона
        border_rect = pygame.Rect(0, 0, bg_width, bg_height)
        pygame.draw.rect(text_background, self.config.DARK_GREEN, border_rect, int(3 * self.state.scale_factor))
        
        text_bg_rect = text_background.get_rect(center=(self.visible_maze_width / 2, self.config.SCREEN_HEIGHT / 2))
        self.screen.blit(text_background, text_bg_rect)

        # Мигающий текст "You Win!"
        blink_factor = (math.sin(time.time() * 5) + 1) / 2
        color_intensity = int(100 + 155 * blink_factor)
        win_color = (255, 255, color_intensity)
        
        # Основной текст
        text_surface = self.fonts['text'].render('YOU WIN!', True, win_color)
        text_rect = text_surface.get_rect(center=(self.visible_maze_width / 2, text_bg_rect.top + int(70 * self.state.scale_factor)))
        self.screen.blit(text_surface, text_rect)
        
        # Дополнительный текст с причиной победы
        reason_surface = self.fonts['info'].render(reason_text, True, self.config.LIGHT_YELLOW)
        reason_rect = reason_surface.get_rect(center=(self.visible_maze_width / 2, text_rect.bottom + int(30 * self.state.scale_factor)))
        self.screen.blit(reason_surface, reason_rect)
        
        # Инструкция для продолжения
        restart_surface = self.fonts['info'].render('Press ENTER to continue', True, self.config.WHITE)
        restart_rect = restart_surface.get_rect(center=(self.visible_maze_width / 2, reason_rect.bottom + int(25 * self.state.scale_factor)))
        self.screen.blit(restart_surface, restart_rect)

    def draw_pause_message(self):
        """Отрисовка сообщения о паузе по пробелу"""
        if (self.state.game_paused and 
            self.state.pause_type == 'space_pause' and 
            self.state.game_mode in ['game', 'editor'] and
            not self.state.game_over and
            not self.state.game_won):
            
            # Создаем полупрозрачный фон
            pause_surface = pygame.Surface((self.visible_maze_width, self.visible_maze_height), pygame.SRCALPHA)
            pause_surface.fill((0, 0, 0, 128))  # Полупрозрачный черный
            
            # Текст паузы
            pause_text = self.fonts['text'].render('PAUSE', True, self.config.WHITE)
            text_rect = pause_text.get_rect(center=(self.visible_maze_width // 2, self.visible_maze_height // 2))
            pause_surface.blit(pause_text, text_rect)
            
            # Подсказка
            hint_text = self.fonts['info'].render('Press SPACE or ESC to continue', True, self.config.YELLOW)
            hint_rect = hint_text.get_rect(center=(self.visible_maze_width // 2, text_rect.bottom + 40))
            pause_surface.blit(hint_text, hint_rect)
            
            # Отображаем поверх игрового поля
            self.screen.blit(pause_surface, (0, self.info_panel_height))

    def start_campaign(self):
        """Запуск кампании"""
        self.state.campaign_mode = True
        self.state.campaign_level = 1  # начинаем с Easy
        self.state.campaign_wins = 0
        self.state.campaign_completed = False
        
        # Устанавливаем уровень сложности БЕЗ вызова set_difficulty
        self.current_difficulty = 1  # Easy
        
        # Обновляем конфигурацию напрямую
        self.config.MAZE_WIDTH = DIFFICULTY_LEVELS[1]['MAZE_WIDTH']
        self.config.MAZE_HEIGHT = DIFFICULTY_LEVELS[1]['MAZE_HEIGHT']
        self.config.time_TIMER_MAX = DIFFICULTY_LEVELS[1]['time_TIMER_MAX']
        self.config.time_BONUS_TIME = DIFFICULTY_LEVELS[1]['time_BONUS_TIME']
        
        self.spider_speed = DIFFICULTY_LEVELS[1]['spider_SPEED']

        # ПЕРЕСОЗДАЕМ лабиринт с новыми размерами
        self.maze = Maze(self.config.MAZE_WIDTH, self.config.MAZE_HEIGHT)
        
        # Перезапускаем игру с новыми параметрами
        self.reset_game(keep_wall_style=False)  # Меняем стену


    def handle_campaign_win(self):
        """Обработка победы в кампании"""
        self.state.campaign_wins += 1
        
        if self.state.campaign_wins >= 3:  # 3 победы на текущем уровне
            if self.state.campaign_level >= 7:  # Nightmare пройден
                # ПОЛНАЯ ПОБЕДА В КАМПАНИИ
                self.state.campaign_completed = True
                self.set_editor_message("CAMPAIGN COMPLETED! You are the champion!")

                # Автоматически перезапускаем игру для следующей попытки
                self.reset_game(keep_wall_style=False)  # Меняем стену
            else:
                # Переход на следующий уровень
                self.state.campaign_level += 1
                self.state.campaign_wins = 0
                self.current_difficulty = self.state.campaign_level
                
                # Обновляем конфигурацию напрямую (без вызова set_difficulty)
                self.config.MAZE_WIDTH = DIFFICULTY_LEVELS[self.state.campaign_level]['MAZE_WIDTH']
                self.config.MAZE_HEIGHT = DIFFICULTY_LEVELS[self.state.campaign_level]['MAZE_HEIGHT']
                self.config.time_TIMER_MAX = DIFFICULTY_LEVELS[self.state.campaign_level]['time_TIMER_MAX']
                self.config.time_BONUS_TIME = DIFFICULTY_LEVELS[self.state.campaign_level]['time_BONUS_TIME']

                self.spider_speed = DIFFICULTY_LEVELS[self.state.campaign_level]['spider_SPEED']

                # ПЕРЕСОЗДАЕМ лабиринт с новыми размерами
                self.maze = Maze(self.config.MAZE_WIDTH, self.config.MAZE_HEIGHT)
                
                level_names = {1: "Easy", 2: "Normal", 3: "Hard", 4: "Challenging", 
                            5: "Difficult", 6: "Extreme", 7: "Nightmare"}
                self.set_editor_message(f"CAMPAIGN: Advanced to {level_names[self.state.campaign_level]}! Win 3 times")

                # Автоматически перезапускаем игру для следующего уровня
                self.reset_game(keep_wall_style=False)  # Меняем стену
        else:
            # Еще не достигли 3 побед
            level_names = {1: "Easy", 2: "Normal", 3: "Hard", 4: "Challenging", 
                        5: "Difficult", 6: "Extreme", 7: "Nightmare"}
            wins_left = 3 - self.state.campaign_wins
            self.set_editor_message(f"CAMPAIGN: {level_names[self.state.campaign_level]} - {wins_left} wins left")

            # Автоматически перезапускаем игру для следующей попытки
            self.reset_game(keep_wall_style=False)  # Меняем стену 

    def show_exit_campaign_confirmation(self):
        """Показать диалог подтверждения выхода из кампании"""
        self.state.show_exit_campaign_dialog = True
        self.state.game_paused = True
        self.show_overlay_text = None
        self.exit_dialog_selected_button = 'cancel'  # Сброс кнопки по умолчанию

    def show_enter_campaign_confirmation(self):
        """Показать диалог подтверждения входа в кампанию"""
        self.state.show_enter_campaign_dialog = True
        self.state.game_paused = True
        self.show_overlay_text = None
        self.enter_dialog_selected_button = 'cancel'  # Сброс кнопки по умолчанию

    def handle_exit_campaign_dialog(self, confirmed):
        """Обработка результата диалога выхода из кампании"""
        self.state.show_exit_campaign_dialog = False
        
        if confirmed:
            # Пользователь нажал OK - выходим из кампании
            self.switch_to_free_play()
            self.state.game_paused = False
        else:
            # Пользователь нажал Cancel - остаемся в кампании
            self.state.game_paused = False

    def switch_to_free_play(self):
        """Переход из кампании в свободную игру"""
        # Полностью сбрасываем прогресс кампании
        self.state.campaign_mode = False
        self.state.campaign_level = 1
        self.state.campaign_wins = 0
        self.state.campaign_completed = False
        
        # Сбрасываем игру для свободного режима
        self.reset_game(keep_wall_style=False)  # Меняем стену 

    def draw_confirmation_dialog(self, title, title_color, messages, left_btn_data, right_btn_data):
            """
            Универсальная отрисовка диалога подтверждения
            left_btn_data / right_btn_data = {'text': str, 'active': bool, 'bg_color': color}
            """
            dialog_width = int(500 * self.state.scale_factor)
            # Высота зависит от количества строк
            dialog_height = int(200 * self.state.scale_factor) + (len(messages) * int(25 * self.state.scale_factor))
            
            dialog_x = (self.config.SCREEN_WIDTH - dialog_width) // 2
            dialog_y = (self.config.SCREEN_HEIGHT - dialog_height) // 2
            
            # Фон
            dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
            dialog_surface.fill((0, 0, 0, 230))
            pygame.draw.rect(dialog_surface, self.config.WHITE, (0, 0, dialog_width, dialog_height), 2)
            
            # Заголовок
            title_text = self.fonts['menu'].render(title, True, title_color)
            title_rect = title_text.get_rect(center=(dialog_width // 2, int(40 * self.state.scale_factor)))
            dialog_surface.blit(title_text, title_rect)
            
            # Сообщение
            msg_y = int(80 * self.state.scale_factor)
            for line in messages:
                text = self.fonts['info'].render(line, True, self.config.WHITE)
                rect = text.get_rect(center=(dialog_width // 2, msg_y))
                dialog_surface.blit(text, rect)
                msg_y += int(25 * self.state.scale_factor)
                
            # Кнопки
            btn_w = int(120 * self.state.scale_factor)
            btn_h = int(40 * self.state.scale_factor)
            btn_y = dialog_height - int(60 * self.state.scale_factor)
            
            # Вспомогательная функция отрисовки кнопки
            def draw_btn(text, x, active, default_color):
                rect = pygame.Rect(x, btn_y, btn_w, btn_h)
                
                if active:
                    # Подсветка
                    pygame.draw.rect(dialog_surface, self.config.YELLOW, rect)
                    pygame.draw.rect(dialog_surface, self.config.WHITE, rect, 3)
                    text_color = self.config.BLACK
                    # Стрелка
                    arrow = "->" if x < dialog_width // 2 else "<-"
                    arrow_surf = self.fonts['info'].render(arrow, True, self.config.YELLOW)
                    arrow_rect = arrow_surf.get_rect()
                    if x < dialog_width // 2: # Левая кнопка
                        arrow_rect.midright = (rect.left - 10, rect.centerY if hasattr(rect, 'centerY') else rect.y + rect.height//2)
                    else: # Правая кнопка
                        arrow_rect.midleft = (rect.right + 10, rect.centerY if hasattr(rect, 'centerY') else rect.y + rect.height//2)
                    dialog_surface.blit(arrow_surf, arrow_rect)
                else:
                    # Обычная
                    pygame.draw.rect(dialog_surface, default_color, rect)
                    pygame.draw.rect(dialog_surface, self.config.WHITE, rect, 2)
                    text_color = self.config.WHITE
                    
                txt_surf = self.fonts['info'].render(text, True, text_color)
                txt_rect = txt_surf.get_rect(center=rect.center)
                dialog_surface.blit(txt_surf, txt_rect)
                return rect # Возвращаем rect относительно диалога

            # Рисуем кнопки
            left_rect = draw_btn(left_btn_data['text'], dialog_width // 2 - btn_w - 20, 
                                left_btn_data['active'], left_btn_data['bg_color'])
            
            right_rect = draw_btn(right_btn_data['text'], dialog_width // 2 + 20, 
                                right_btn_data['active'], right_btn_data['bg_color'])
            
            self.screen.blit(dialog_surface, (dialog_x, dialog_y))
            
            # Возвращаем глобальные rect'ы для обработки кликов
            return {
                'left': pygame.Rect(dialog_x + left_rect.x, dialog_y + left_rect.y, btn_w, btn_h),
                'right': pygame.Rect(dialog_x + right_rect.x, dialog_y + right_rect.y, btn_w, btn_h)
            }

    def draw_exit_campaign_dialog(self):
        buttons = self.draw_confirmation_dialog(
            title="EXIT CAMPAIGN?",
            title_color=self.config.RED,
            messages=[
                "Are you sure you want to exit campaign?",
                " ",
                "All campaign progress will be lost!",
                " ",
                "Mouse, Arrow Keys or WASD Left/Right - Navigate",
                "ENTER - Select, ESC - Back"
            ],
            left_btn_data={
                'text': "EXIT", 
                'active': self.exit_dialog_selected_button == 'ok',
                'bg_color': self.config.RED
            },
            right_btn_data={
                'text': "CANCEL", 
                'active': self.exit_dialog_selected_button == 'cancel',
                'bg_color': self.config.DARK_GREEN
            }
        )
        # Сохраняем кнопки для обработки кликов (маппинг имен)
        self.exit_dialog_buttons = {'ok': buttons['left'], 'cancel': buttons['right']}

    def draw_enter_campaign_dialog(self):
        buttons = self.draw_confirmation_dialog(
            title="START CAMPAIGN?",
            title_color=self.config.LIGHT_GREEN,
            messages=[
                "OBJECTIVE: 21 Wins (3 per difficulty)",
                "",
                "PROGRESS TRACK:",
                "Easy -> Normal -> Hard -> Challenging",
                "-> Difficult -> Extreme -> Nightmare"
            ],
            left_btn_data={
                'text': "START", 
                'active': self.enter_dialog_selected_button == 'start',
                'bg_color': self.config.DARK_GREEN
            },
            right_btn_data={
                'text': "CANCEL", 
                'active': self.enter_dialog_selected_button == 'cancel',
                'bg_color': self.config.BLUE
            }
        )
        # Сохраняем кнопки для обработки кликов
        self.enter_dialog_buttons = {'start': buttons['left'], 'cancel': buttons['right']}

    def get_level_name(self, level):
        """Получить название уровня по номеру"""
        level_names = {
            1: "Easy", 2: "Normal", 3: "Hard", 4: "Challenging",
            5: "Difficult", 6: "Extreme", 7: "Nightmare"
        }
        return level_names.get(level, "Unknown")

    def run(self):
        """Основной игровой цикл (оптимизированная версия)"""
        running = True

        # Предварительные вычисления констант для оптимизации
        cell_size_half = self.cell_size // 2

        while running:
            # ОБНОВЛЯЕМ размеры каждый кадр
            self.visible_maze_width = self.config.SCREEN_WIDTH - self.ui_panel_width
            self.visible_maze_height = self.config.SCREEN_HEIGHT - self.info_panel_height

            # Расчет камеры - используем КЭШИРОВАННЫЕ размеры
            maze_width_px, maze_height_px = self.get_maze_dimensions()

            # Оптимизированные вычисления камеры
            visible_width_half = self.visible_maze_width // 2
            visible_height_half = self.visible_maze_height // 2

            cam_x = self.player.y * self.cell_size - visible_width_half + cell_size_half
            cam_y = self.player.x * self.cell_size - visible_height_half + cell_size_half

            cam_x = max(0, min(cam_x, maze_width_px - self.visible_maze_width))
            cam_y = max(0, min(cam_y, maze_height_px - self.visible_maze_height))

            # Обработка событий
            running = self.handle_events()
            if not running:
                break

            # Обновление состояния игры
            self.update_game_state()

            # Обновление анимации победы, если игра выиграна
            if self.state.game_won:
                self.update_win_animation()

            # ОТРИСОВКА ИГРЫ
            self.screen.fill(self.config.GREY)

            # Очищаем существующую поверхность
            self.labyrinth_surface.fill(self.config.BLACK)

            # Определение режима отрисовки
            mode = "editor" if self.state.game_mode == "editor" else "game"
            
            # Рисуем на предсозданной поверхности
            self.draw_map(self.labyrinth_surface, mode, self.cell_size, (-cam_x, -cam_y))

            # Копируем на экран
            self.screen.blit(self.labyrinth_surface, (0, self.info_panel_height))

            # Отрисовка UI
            self.draw_ui()

            pygame.display.flip()
            self.clock.tick(self.FPS)

            # --- Плавное применение нового размера окна ---
            if getattr(self, "pending_resize", None) and time.time() - self.last_resize_time > 0.15:
                w, h = self.pending_resize
                self.resize_window(w, h)
                self.pending_resize = None

        pygame.quit()


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.initialize()
    game.run()

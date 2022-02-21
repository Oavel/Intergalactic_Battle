import pygame.mixer
from os import path


class Settings:
    """Класс для хранения всех настроек игры Alien Invasion."""
    def __init__(self):
        """Инициализирует статистические настройки игры."""
        # Фоновый звук космоса
        sound = pygame.mixer.Sound('sound/cos.wav')
        sound.play()
        # Параметры экрана
        self.BLACK = (0, 0, 0)
        self.screen_width = 1280
        self.screen_height = 700
        self.background = pygame.image.load(path.join('images/cos.jpg'))
        self.background_rect = self.background.get_rect()
        # self.bg_color = (0, 0, 0)   # 29, 254, 176
        # Настройки скорости коробля
        self.ship_limit = 3
        # Настройка звука начала игры Play - (P)
        self.sound_play = pygame.mixer.Sound('sound/play.wav')
        # Настройка звука уничтожения всех пришельцев
        self.sound_metkost = pygame.mixer.Sound('sound/metkost.wav')
        # Настройка звука коробля
        self.sound_ship = pygame.mixer.Sound('sound/ship.wav')
        # Настройка звука завершения игры
        self.sound_end = pygame.mixer.Sound('sound/end.wav')
        # Настройка звука выстрела коробля
        self.sound_ship_fire = pygame.mixer.Sound('sound/fire.wav')
        # Настройка звука взрыва корабля
        self.sound_alien_kill = pygame.mixer.Sound('sound/vzryv.wav')
        # Параметры снаряда
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = (203, 95, 254)
        self.bullets_allowed = 100

        # Темп ускорения игры
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельца
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 0.3
        # Настройка пришельцев
        self.fleet_drop_speed_factor = 6
        self.alien_speed_factor = 0.5
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1

        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости  и стоимости пришельцев."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

import pygame
from pygame.sprite import Sprite


class Live (Sprite):
    """Класс для управления кораблем."""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/live.png')
        self.image.set_colorkey(self.settings.BLACK)
        self.rect = self.image.get_rect()

        # Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

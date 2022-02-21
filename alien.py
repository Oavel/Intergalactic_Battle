import pygame
from pygame.sprite import Sprite
import random


class Alien(Sprite):
    """Класс, представляющий одного пришельца."""

    def __init__(self, ai_game):
        """Инициализирует пришельца и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изображения пришельца и назначение атрибута rect.
        self.image = pygame.image.load('images/alien.png')
        self.image.set_colorkey(self.settings.BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(self.settings.screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 2)
        self.speedx = random.randrange(-1, 1)

        # Сохранение точной горизонтальной позиции пришельца.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Перемещает пришельца влево или вправо."""
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > self.settings.screen_height + 10 or self.rect.left < -25 or self.rect.right > self.settings.screen_width + 20:
            self.rect.x = random.randrange(self.settings.screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 2)

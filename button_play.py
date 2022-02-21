import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        """Инициализирует атрибут кнопки"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        # Назначение размеров и свойств кнопок
        self.width, self.height = 230, 80
        self.text_color = (203, 95, 254)
        self.font = pygame.font.SysFont('comicsansms', 48)

        # Построение объекта rect кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottomright = self.screen_rect.bottomright

        # Cообщение кнопки создается только один раз
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Отображение пустой кнопки и вывод сообщения
        self.screen.blit(self.msg_image, self.msg_image_rect)  # Выводит изображение текста на экран


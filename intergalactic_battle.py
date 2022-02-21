import sys

import time

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button_play import Button
from button_quit import ButtonQuit
from button_manual import ButtonManual
from button_game_over import ButtonGO
from ship import Ship
from bullet import Bullet
from alien import Alien


class IntergalacticBattle:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        # Звук начала игры Play - (P)
        self.sound_play = self.settings.sound_play
        # Звук движения корабля
        self.sound_ship = self.settings.sound_ship
        # Звук завешения игры
        self.sound_end = self.settings.sound_end
        # Звук уничтожения всех пришельцев
        self.sound_metkost = self.settings.sound_metkost
        # Звук выстрела корабля
        self.sound_ship_fire = self.settings.sound_ship_fire
        # Звук взрыва корабля
        self.sound_alien_kill = self.settings.sound_alien_kill
        pygame.display.set_caption("Intergalactic Battle")
        # Создание экземпляра для хранение игровой статистики
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()    # по флоту

        # Создание кнопки Play
        self.play_button = Button(self, "Play - (P)")
        # Создание кнопки Quit
        self.play_button_quit = ButtonQuit(self, "Quit - (Q)")
        # Создание кнопки инструкции
        self.play_button_manual = ButtonManual(self, "control keys / (space)-fire")
        # Создание кнопки Game Over
        self.play_button_game_over = ButtonGO(self, "Game Over")

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sound_end.play()  # Загружаем звук завершения игры
                time.sleep(1.7)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # Метод необ-им для реаг-ния только на щелчки мыши по кнопке Play
                self._check_play_button(mouse_pos)
                self._check_play_button_quit(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  # Метод collidepoint исп для проверки, находится
        if button_clicked and not self.stats.game_active:               # ли указатель мыши в пределах области
                                                                        # прямоугольника кнопки Play
            # Сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            # Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещ корабля в центре
            self._create_fleet()
            self.ship.centre_ship()
            self.sound_play.play()  # Звук начала игры Play - (P)
            # Указатель мыши скрывается
            pygame.mouse.set_visible(False)

    def _check_play_button_quit(self, mouse_pos):
        button_clicked_quit = self.play_button_quit.rect.collidepoint(mouse_pos)
        if button_clicked_quit and not self.stats.game_active:  # для того, чтобы область кнопки Quit не реагировала на
                                                                # щелчки мыши в этой области

            self.sound_end.play()  # Загружаем звук завершения игры
            time.sleep(1.7)
            sys.exit()

    def start_game(self):
        """Запускает новую игру при нажатии кнопки (P)"""
        button_clicked_0 = pygame.K_p
        if button_clicked_0 and not self.stats.game_active:
            # Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещ корабля в центре
            self._create_fleet()
            self.ship.centre_ship()
            self.sound_play.play()  # Звук начала игры Play - (P)
            # Указатель мыши скрывается
            pygame.mouse.set_visible(False)

    def _check_key_down_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT and self.stats.game_active:  # Переместить корабль вправо.
            self.ship.moving_right = True
            self.sound_ship.play()  # Загружаем звук корабля при движении
        elif event.key == pygame.K_LEFT and self.stats.game_active:  # Переместить корабль влево.
            self.ship.moving_left = True
            self.sound_ship.play()
        elif event.key == pygame.K_UP and self.stats.game_active:  # Переместить корабль вверх.
            self.ship.moving_up = True
            self.sound_ship.play()
        elif event.key == pygame.K_DOWN and self.stats.game_active:  # Переместить корабль вниз.
            self.ship.moving_down = True
            self.sound_ship.play()
        elif event.key == pygame.K_q:
            self.sound_end.play()  # Загружаем звук завершения игры
            time.sleep(1.7)
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_active:    # and self.stats_____: для того чтобы кнопка
            self._fire_bullet()                                         # space была не активна до нажатия Play
            self.sound_ship_fire.play()
        elif event.key == pygame.K_p:
            self.start_game()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Проверка попаданий в пришельцев.
        # При обнаружении попадания удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.check_high_score()
        # Воспроизведение звука взрыва корабля
            self.sound_alien_kill.play()
        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота
            self.sound_metkost.play()
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()
        self.sb.prep_score()

    def _update_screen(self):
        # При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.settings.BLACK)
        self.screen.blit(self.settings.background, self.settings.background_rect)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Выводит информацию о счете
        self.sb.show_score()

        # Кнопка Play отображается в том случае, если игра не активна
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Кнопка Quit отображается в том случае, если игра не активна
        if not self.stats.game_active:
            self.play_button_quit.draw_button()
        if not self.stats.game_active:
            self.play_button_manual.draw_button()
        if not self.stats.game_active:
            if self.stats.ships_left <= 0:
                self.play_button_game_over.draw_button()
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def _create_fleet(self):    # по флоту
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        self.aliens.add(alien)
    #     alien_width, alien_height = alien.rect.size
    #     alien_width = alien.rect.width
    #     available_space_x = self.settings.screen_width - (2 * alien_width)
    #     number_aliens_x = available_space_x // (2 * alien_width)
    #     """Определяет количество рядов, помещающихся на экране."""
    #     ship_height = self.ship.rect.height
    #     available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
    #     number_rows = available_space_y // (2 * alien_height)
    #
    #     # Создание флота вторжения.
    #
    #     for row_number in range(number_rows):
    #         for alien_number in range(number_aliens_x):
    #             self._create_alien(alien_number, row_number)
    #
    # def _create_alien(self, alien_number, row_number):
    #     """Создание пришельца и размещение его в ряду."""
    #     alien = Alien(self)
    #     alien_width, alien_height = alien.rect.size
    #     alien.x = alien_width + 2 * alien_width * alien_number
    #     alien.rect.x = alien.x
    #     alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    #     self.aliens.add(alien)

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()
        # Проверка коллизий "пришелец корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            sound_avaria = pygame.mixer.Sound('sound/avaria.wav')  # Звук столкновения корабля с пришельцем
            sound_avaria.play()
        # Проверяет, добрались ли пришельцы до нижнего края
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение пришельца с кораблем"""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_lives()
            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещ корабля в центре
            self._create_fleet()
            self.ship.centre_ship()
            time.sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed_factor
        self.settings.fleet_direction *= -1


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = IntergalacticBattle()
    ai.run_game()

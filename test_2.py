import pygame
import random
from statemachine import StateMachine, State
import sys


# машина состояний
class States(StateMachine):
    menu = State(initial=True)
    play = State()
    pause = State()
    won = State()
    init = State()
    game_over = State()
    after_end = State()

    menu_to_init = menu.to(init)
    init_to_game = init.to(play)
    end_pause = pause.to(play)
    pause_to_new_game = pause.to(init)
    play_to_pause = play.to(pause)
    play_to_menu = play.to(menu)
    play_to_won = play.to(won)
    play_to_game_over = play.to(game_over)
    game_over_to_init = game_over.to(init)
    won_to_play = won.to(play)
    won_to_init = won.to(init)
    won_to_inf = won.to(after_end)
    after_end_to_game_over = after_end.to(game_over)


# игровое поле
class Field_matrix:

    # конструктор
    def __init__(self, target_value):
        self.matrix = [[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]

        self.add_block()
        self.add_block()
        self.target_value = target_value

    # выдача матрицы
    def get_values(self):
        return self.matrix

    # сдвиг поля влево
    def left(self):
        returned_value = 0
        for i in range(len(self.matrix)):
            count = 0
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    self.matrix[i][count] = self.matrix[i][j]
                    count += 1

            while count < len(self.matrix[i]):
                self.matrix[i][count] = 0
                count += 1

            for j in range(1, len(self.matrix[i])):
                if self.matrix[i][j] == self.matrix[i][j - 1]:
                    self.matrix[i][j - 1] = self.matrix[i][j - 1] * 2
                    self.matrix[i][j] = 0
                    returned_value += self.matrix[i][j - 1]

            count = 0
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    self.matrix[i][count] = self.matrix[i][j]
                    count += 1

            while count < len(self.matrix[i]):
                self.matrix[i][count] = 0
                count += 1

        self.add_block()
        return returned_value

    # сдвиг поля вправо
    def right(self):
        returned_value = 0
        for i in range(len(self.matrix)):
            zero_indx = 3
            for j in range(len(self.matrix[i])-1, -1, -1):
                if self.matrix[i][j] != 0:
                    self.matrix[i][zero_indx] = self.matrix[i][j]
                    zero_indx -= 1

            while zero_indx != -1:
                self.matrix[i][zero_indx] = 0
                zero_indx -= 1

            for j in range(len(self.matrix[i])-1, 0, -1):
                if self.matrix[i][j] == self.matrix[i][j-1]:
                    self.matrix[i][j] = self.matrix[i][j-1]*2
                    self.matrix[i][j-1] = 0
                    returned_value += self.matrix[i][j]

            zero_indx = 3
            for j in range(len(self.matrix[i]) - 1, -1, -1):
                if self.matrix[i][j] != 0:
                    self.matrix[i][zero_indx] = self.matrix[i][j]
                    zero_indx -= 1

            while zero_indx != -1:
                self.matrix[i][zero_indx] = 0
                zero_indx -= 1

        self.add_block()
        return returned_value

    # сдвиг поля вверх
    def up(self):
        returned_value = 0

        for j in range(len(self.matrix)):
            count = 0

            for i in range(len(self.matrix)):
                if self.matrix[i][j] != 0:
                    self.matrix[count][j] = self.matrix[i][j]
                    count += 1

            while count < len(self.matrix):
                self.matrix[count][j] = 0
                count += 1

            for i in range(1, len(self.matrix[j])):
                if self.matrix[i][j] == self.matrix[i - 1][j]:
                    self.matrix[i - 1][j] = self.matrix[i - 1][j] * 2
                    self.matrix[i][j] = 0
                    returned_value += self.matrix[i - 1][j]

            count = 0

            for i in range(len(self.matrix)):
                if self.matrix[i][j] != 0:
                    self.matrix[count][j] = self.matrix[i][j]
                    count += 1

            while count < len(self.matrix):
                self.matrix[count][j] = 0
                count += 1

        self.add_block()
        return returned_value

    # сдвиг поля вниз
    def down(self):
        returned_value = 0
        for j in range(len(self.matrix)):

            count = 3

            for i in range(len(self.matrix) - 1, -1, -1):
                if self.matrix[i][j] != 0:
                    self.matrix[count][j] = self.matrix[i][j]
                    count -= 1

            while count > -1:
                self.matrix[count][j] = 0
                count -= 1

            for i in range(len(self.matrix) - 1, 0, -1):
                if self.matrix[i][j] == self.matrix[i - 1][j]:
                    self.matrix[i][j] = self.matrix[i - 1][j] * 2
                    self.matrix[i - 1][j] = 0
                    returned_value += self.matrix[i][j]

            count = 3

            for i in range(len(self.matrix) - 1, -1, -1):
                if self.matrix[i][j] != 0:
                    self.matrix[count][j] = self.matrix[i][j]
                    count -= 1

            while count > -1:
                self.matrix[count][j] = 0
                count -= 1

        self.add_block()
        return returned_value

    # проверка наличия целевого значения в матрице
    def won(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == self.target_value:
                    return True
        return False

    # добавление нового блока
    def add_block(self):
        if not self.check_free_space():
            return
        exists = True
        while exists:
            i = random.randint(0, 3)
            j = random.randint(0, 3)

            if self.matrix[i][j] == 0:
                exists = False

        self.matrix[i][j] = 4 if random.random() >= 0.9 else 2

    # проверка конца игры
    def game_over_check(self):
        if self.check_free_space():
            return False
        return self.check_vertical_game_over() and self.check_horizontal_game_over()

    # проверка наличия пустого места в матрице
    def check_free_space(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0:
                    return True
        return False

    # проверка возможности горизонтальных ходов
    def check_horizontal_game_over(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0]) - 1):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return False
        return True

    # проверка возможности вертикальных ходов
    def check_vertical_game_over(self):
        for i in range(len(self.matrix) - 1):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return False
        return True

    # выдача значения блока
    def get_block(self, i, j):
        return self.matrix[i][j]


# экран
class Screen:
    # конструктор
    def __init__(self, caption, size=[500, 500]):
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)

        self.font = pygame.font.SysFont('Arial', 40, bold=True)

        self.block_matrix = []

        for i in range(4):
            buffer = []
            for j in range(4):
                x = pygame.Rect(j * 120 + 15, i * 120 + 65, 110, 110)
                buffer.append(x)

            self.block_matrix.append(buffer)

        self.colors = {0: '#FB9902',
                       2: '#1f78b4',
                       4: '#7f21f3',
                       8: '#e821f3',
                       16: '#f32194',
                       32: '#f3212b',
                       64: '#f37f21',
                       128: '#f3e821',
                       256: '#94f321',
                       512: '#2bf321',
                       1024: '#21f380',
                       2048: '#21f3e8',
                       }

        self.buttons = {}

    # заполнение цветом
    def fill(self, color):
        self.screen.fill(color)

    # нарисовать кнопку
    def render_button(self, text, left=200, top=200):
        surf = self.font.render(text, True, 'white')
        button = pygame.Rect(left, top, 240, 60)

        a, b = pygame.mouse.get_pos()
        if button.x <= a <= button.x + 240 and button.y <= b <= button.y + 60:
            pygame.draw.rect(self.screen, (180, 180, 180), button)
        else:
            pygame.draw.rect(self.screen, (110, 110, 110), button)

        self.screen.blit(surf, (button.x + 5, button.y + 5))
        self.buttons[text] = button

    # отрисовка игрового поля
    def render_field(self, values):
        for i in range(len(values)):
            for j in range(len(values[i])):
                pygame.draw.rect(self.screen, self.colors[values[i][j]], self.block_matrix[i][j])
                surf = self.font.render(f'{values[i][j]}', True, 'white')
                self.screen.blit(surf, (self.block_matrix[i][j].x, self.block_matrix[i][j].y + 70))

    # проверка столкновения
    def check_collide(self, button_id, event):
        return self.buttons[button_id].collidepoint(event.pos)

    # нарисовать текст
    def render_text(self, text, x, y):
        surf = self.font.render(text, True, 'white')
        self.screen.blit(surf, (x, y))


# app
class Game:

    # инициализация
    def __init__(self):

        pygame.init()
        self.state = States()
        self.screen = Screen('2048', [500, 550])
        self.score = 0
        self.field_matrix = Field_matrix(128)

    # главный цикл
    def mainloop(self):

        while True:

            if self.state.current_state == self.state.init:
                self.field_matrix = Field_matrix(128)
                self.state.init_to_game()
                self.score = 0

            elif self.state.current_state == self.state.pause:

                # рендеринг
                self.screen.fill('#313552')

                self.screen.render_button('quit', 150, 400)
                self.screen.render_button('continue', 150, 200)
                self.screen.render_button('restart', 150, 300)

                self.screen.render_text('pause', 150, 100)

                # обработка событий
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if events.type == pygame.MOUSEBUTTONDOWN:
                        if self.screen.check_collide('quit', events):
                            pygame.quit()
                            sys.exit()
                        elif self.screen.check_collide('restart', events):
                            self.state.pause_to_new_game()
                        elif self.screen.check_collide('continue', events):
                            self.state.end_pause()

            elif self.state.current_state == self.state.menu:

                # рендеринг
                self.screen.fill('#313552')
                self.screen.render_button('quit', 150, 300)

                self.screen.render_button('start', 150, 200)

                self.screen.render_text('menu', 150, 100)

                # обработка событий
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if events.type == pygame.MOUSEBUTTONDOWN:
                        if self.screen.check_collide('quit', events):
                            pygame.quit()
                            sys.exit()
                        elif self.screen.check_collide('start', events):
                            self.state.menu_to_init()

            elif self.state.current_state == self.state.play:

                if self.field_matrix.won():
                    self.state.play_to_won()
                elif self.field_matrix.game_over_check():
                    self.state.play_to_game_over()

                # обработка событий
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif events.type == pygame.KEYDOWN:
                        if events.key == pygame.K_UP:
                            self.score += self.field_matrix.up()
                        elif events.key == pygame.K_DOWN:
                            self.score += self.field_matrix.down()
                        elif events.key == pygame.K_LEFT:
                            self.score += self.field_matrix.left()
                        elif events.key == pygame.K_RIGHT:
                            self.score += self.field_matrix.right()
                        elif events.key == pygame.K_ESCAPE:
                            self.state.play_to_pause()

                # рендеринг
                self.screen.fill('#313552')
                self.screen.render_field(self.field_matrix.get_values())
                self.screen.render_text(f'score:{self.score}', 15, 15)

            elif self.state.current_state == self.state.won:

                # рендеринг
                self.screen.fill('#313552')
                self.screen.render_text('you have won the game', 150, 100)
                self.screen.render_button('continue', 150, 200)
                self.screen.render_button('restart', 150, 300)
                self.screen.render_button('quit', 150, 400)

                # обработка событий
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if events.type == pygame.MOUSEBUTTONDOWN:
                        if self.screen.check_collide('quit', events):
                            pygame.quit()
                            sys.exit()
                        elif self.screen.check_collide('restart', events):
                            self.state.won_to_init()
                        elif self.screen.check_collide('continue', events):
                            self.state.won_to_inf()

            elif self.state.current_state == self.state.game_over:

                # рендеринг
                self.screen.fill('pink')
                self.screen.render_button('restart', 150, 200)
                self.screen.render_button('quit', 150, 300)
                self.screen.render_text('game over', 150, 100)

                # обработка событий
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if events.type == pygame.MOUSEBUTTONDOWN:
                        if self.screen.check_collide('quit', events):
                            pygame.quit()
                            sys.exit()
                        elif self.screen.check_collide('restart', events):
                            self.state.game_over_to_init()

            elif self.state.current_state == self.state.after_end:

                if self.field_matrix.game_over_check():
                    self.state.after_end_to_game_over()

                # обработка событий
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif events.type == pygame.KEYDOWN:

                        if events.key == pygame.K_UP:
                            self.score += self.field_matrix.up()
                        elif events.key == pygame.K_DOWN:
                            self.score += self.field_matrix.down()
                        elif events.key == pygame.K_LEFT:
                            self.score += self.field_matrix.left()
                        elif events.key == pygame.K_RIGHT:
                            self.score += self.field_matrix.right()
                        elif events.key == pygame.K_ESCAPE:
                            self.state.play_to_pause()

                self.screen.fill('#313552')
                self.screen.render_field(self.field_matrix.get_values())
                self.screen.render_text(f'score:{self.score}', 15, 15)

            pygame.display.update()


if __name__ == '__main__':
    app = Game()
    app.mainloop()

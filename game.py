import os
import pickle
import random as rand
from collections import deque

from config import *


class Minefield:
    def __init__(self, size, bombs):
        """
        Инициализация минного поля

        :param size: list or tuple содержат размеры поля по вертикали и горизонтали
        :param bombs: int количество бомб на поле
        """
        self.size = size
        self.bombs = bombs
        self.minefield = [[' ' for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.playing_field = [['■' for _ in self.minefield[0]] for _ in self.minefield]
        self.queue_coord = deque()
        self.bombs_generated = False
        self.flags = 0

    def gen_neighbors(self, x, y):
        """
        Generating a list containing the values of neighboring cells

        :param x: int координата ячейки по вертикали
        :param y: int координата ячейки по горизонтали
        :return: list значения соседних ячеек
        """
        neighbors = []
        for delta_1 in [-1, 0, 1]:
            for delta_2 in [-1, 0, 1]:
                x_new, y_new = x + delta_1, y + delta_2
                if 0 <= x_new <= self.size[0] - 1 and 0 <= y_new <= self.size[1] - 1 and (not delta_1 == delta_2 == 0):
                    neighbors.append(self.minefield[x_new][y_new])
        return neighbors

    def gen_coord_neighbors(self, x, y):
        """
        Генерация списка списков координат соседних ячеек

        :param x: int координата ячейки по вертикали
        :param y: int координата ячейки по горизонтали
        :return: list списки координат соседних ячеек
        """
        coord_neighbors = []
        for delta_1 in [-1, 0, 1]:
            for delta_2 in [-1, 0, 1]:
                x_new = x + delta_1
                y_new = y + delta_2
                if 0 <= x_new <= self.size[0] - 1 and 0 <= y_new <= self.size[1] - 1 and (not delta_1 == delta_2 == 0):
                    coord_neighbors.append([x_new, y_new])
        return coord_neighbors

    def check_neighbors(self, x, y):
        """
        Проверка ячеек на наличие мин в них и соседних. Если в соседней ячейке есть мина, в ячейку записывается
        количество мин вокруг нее, ее соседи в данной итерации не проверяются.

        :param x: int координата ячейки по вертикали
        :param y: int координата ячейки по горизонтали
        :return: None
        """
        neighbors = self.gen_neighbors(x, y)
        if '💣' in neighbors:
            self.playing_field[x][y] = neighbors.count('💣')
        else:
            self.playing_field[x][y] = ' '
            coord_neighbors = self.gen_coord_neighbors(x, y)
            self.queue_coord += deque(coord_neighbors)

    def set_bombs(self, x, y):
        """
        Инициализация мин на поле. Первым ходом проиграть невозможно, поэтому в выбранной ячейке и ее соседях мины
        не генерируются.

        :param x: int координата ячейки по вертикали
        :param y: int координата ячейки по горизонтали
        :return: None
        """
        for _ in range(self.bombs):
            while True:
                xb = rand.randint(0, self.size[0] - 1)
                yb = rand.randint(0, self.size[1] - 1)
                if self.minefield[xb][yb] == '💣' or (x == xb and y == yb) or [xb, yb] in self.gen_coord_neighbors(x, y):
                    continue
                self.minefield[xb][yb] = '💣'
                break

    def set_flags(self, x, y):
        """
        Устанавливает флаг 'F' в выбранную ячейку, если это возможно

        :param x: int координата ячейки по вертикали
        :param y: int координата ячейки по горизонтали
        :return: None
        """
        if self.playing_field[x][y] == 'F':
            self.playing_field[x][y] = '■'
            self.flags -= 1
        elif self.playing_field[x][y] == '■':
            self.playing_field[x][y] = 'F'
            self.flags += 1
        else:
            print(UserText.CANNOT_FLAG)

    def get_playing_field(self):
        """
        Красивый вывод поля в консоль

        :return: None
        """
        print(f'МИН НА ПОЛЕ: {self.bombs}', end='')
        for line in self.playing_field:
            print(f'\n-{"----" * len(line)}\n| ', end='')
            for cell in line:
                print(cell, sep=' | ', end=' | ')
        print(f'\n-{"----" * len(line)}')

    def get_minefield(self):
        """
        Вспомогательная функция, которая использовалась для отладки программы

        :return: None
        """
        print('МИННОЕ ПОЛЕ', end='')
        for line in self.minefield:
            print(f'\n-{"----" * len(line)}\n| ', end='')
            for cell in line:
                print(cell, sep=' | ', end=' | ')
        print(f'\n-{"----" * len(line)}')

    def do_act(self, x, y, action):
        """
        Вызывает функцию для проверки ячейки или функцию для установки флага в заданную ячейку. Может выбрасывать
        исключение при попытке открытия уже открытой ячейки или ячейки с флагом. Если выбранная ячейка содержит мину,
        вызывает функцию поражения.

        :param x: int координата ячейки по вертикали
        :param y: int координата ячейки по горизонтали
        :param action: str тип действия
        :return: func or ValueError or None
        """
        if action == Action.FLAG:
            self.set_flags(x, y)

        elif action == Action.OPEN and self.minefield[x][y] == '💣':
            return Game().lose_game()

        elif self.minefield[x][y].isdigit() or self.minefield[x][y] == Action.FLAG:
            raise ValueError

        elif action == Action.OPEN:
            self.queue_coord.append([x, y])
            while self.queue_coord:
                x, y = self.queue_coord.popleft()
                if self.playing_field[x][y] == '■':
                    self.check_neighbors(x, y)


class Game:
    def __init__(self):
        """
        Инициализация объекта игры
        """
        self.minefield = None
        self.isPlay = True

    def start(self):
        """
        Предлагает выбрать действие при запуске программы

        :return: func
        """
        print(UserText.WELCOME)

        command = self.handler_message(input(UserText.HOW_START_GAME), Context.START_MENU)
        if command == Start.START_NEW_GAME:
            return self.new_game()
        if command == Start.LOAD_GAME:
            return self.load_game()
        if command == Start.EXIT:
            return exit()

    def new_game(self):
        """
        Предлагает выбрать размер поля

        :return: func
        """
        command = self.handler_message(input(UserText.SELECT_FIELD), Context.SELECT_FIELD)

        if command == FieldSize.STANDARD:
            self.minefield = Minefield((5, 5), rand.randint(2, 5))
        elif command == FieldSize.CUSTOM:
            line, column, bombs = self.handler_message(input(UserText.CHOOSE_SIZES), Context.CHOOSE_SIZES)
            self.minefield = Minefield((line, column), bombs)
        elif command == FieldSize.BACK:
            return self.start()

        print(UserText.START_GAME)
        return self.first_action()

    def load_game(self):
        """
        Функция для загрузки сохранения из файла с расширением .pkl, реализованная с помощью стандартной библиотеки pickle

        :return: func
        """
        if not list(filter(lambda x: x[:4] == "save", os.listdir())):
            print(UserText.NO_SAVE)
            if self.minefield is None:
                print(UserText.WILL_BE_CREATED)
                self.new_game()
            else:
                self.action()
        print(UserText.SELECT_SAVE)
        for save in filter(lambda x: x[:4] == "save", os.listdir()):
            print(save)
        with open(f'save{self.handler_message(input(), Context.SELECT_SAVE)}.pkl', 'rb') as save:
            try:
                self.minefield = pickle.load(save)
                self.minefield.get_playing_field()
                return self.action()
            except:
                print(UserText.ERROR)
                return self.load_game()

    def save_game(self):
        """
        Функция для сохранения игры в файл с расширением .pkl, реализованная с помощью стандартной библиотеки pickle.
        Открытие файла с помощью текстового редактора не позволяет узнать положение мин на поле.

        :return: func
        """
        if len(list(filter(lambda x: x[:4] == "save", os.listdir()))):
            number_of_save = max([int(save[4]) for save in filter(lambda x: x[:4] == "save", os.listdir())]) + 1
        else:
            number_of_save = 1
        with open(f'save{number_of_save}.pkl', 'wb') as save:
            pickle.dump(self.minefield, save)
            print(UserText.GAME_SAVED)
            return self.menu()

    def first_action(self):
        """
        Предлагает сделать первый ход, а также запускает функцию, инициализирующую мины на поле

        :return: func
        """
        self.minefield.get_playing_field()

        action = self.handler_message(input(UserText.ENTER_MOVE), Context.PLAYER_TURN)
        if action == 'Меню':
            return self.menu()
        X, Y, Action = action

        self.minefield.set_bombs(X - 1, Y - 1)
        self.minefield.bombs_generated = True
        self.minefield.do_act(X - 1, Y - 1, Action)
        self.minefield.get_playing_field()

        return self.action()

    def action(self):
        """
        Функция для совершения ходов, проверяет партию на победу и возвращает функцию победы при выполненных условиях

        :return: func
        """
        try:
            while self.is_win(self.minefield.playing_field) != 0:

                action = self.handler_message(input(UserText.ENTER_MOVE), Context.PLAYER_TURN)
                if action == Menu.MENU:
                    return self.menu()
                X, Y, Action = action
                self.minefield.do_act(X - 1, Y - 1, Action)
                self.minefield.get_playing_field()

            return self.win_game()

        except ValueError:
            print(UserText.ERROR)
            return self.action()

    def menu(self):
        """
        Меню, позволяющее сохранить, загрузить, начать новую игру или выйти из программы, прямо во время партии

        :return: func
        """
        command = input(UserText.MENU)
        if command == Menu.CONTINUE:
            return self.action()
        if command == Menu.SAVE_GAME:
            if not self.minefield.bombs_generated:
                print(UserText.CANNOT_BE_SAVED)
                return self.menu()
            return self.save_game()
        if command == Menu.LOAD_GAME:
            return self.load_game()
        if command == Menu.START_NEW_GAME:
            return self.new_game()
        if command == Menu.EXIT:
            return exit()

    def is_win(self, field):
        """
        Проверяет поле на условие победы

        :param field: list of lists игровое поле
        :return: int количество не открытых ячеек
        """
        return sum([line.count('■') for line in field]) - self.minefield.bombs + self.minefield.flags

    def win_game(self):
        """
        Поздравляет с победой

        :return: func
        """
        print(UserText.CONGRATULATIONS)
        return self.start()

    def lose_game(self):
        """
        Сообщает о поражении

        :return: func
        """
        print(UserText.DEFEAT)
        return self.start()

    def handler_message(self, string, context):
        """
        Обработчик сообщений пользователя

        :param string: str строка, введенная пользователем
        :param context: str положение, из которого вызван обработчик сообщений
        :return: str
        """
        if context in (Context.START_MENU, Context.SELECT_FIELD):
            while True:
                if string in ['1', '2', '3']:
                    return string
                else:
                    string = input(UserText.ERROR)

        if context == Context.CHOOSE_SIZES:
            while True:
                try:
                    sizes = [int(size) for size in string.split()]
                    if 5 <= sizes[0] <= 30 and 5 <= sizes[1] <= 30 and 0 < sizes[2] < sizes[0] * sizes[1]:
                        return sizes
                    else:
                        string = input(UserText.ERROR)
                except ValueError or IndexError:
                    string = input(UserText.ERROR)

        if context == Context.PLAYER_TURN:
            while True:
                try:
                    if string == 'Меню':
                        return string
                    turn = string.replace(' ', '').split(',')
                    turn[0], turn[1], turn[2] = int(turn[0]), int(turn[1]), turn[2].upper()
                    if 1 <= turn[0] <= self.minefield.size[0] and 1 <= turn[1] <= self.minefield.size[1]\
                            and turn[2] in ['F', 'O']:
                        return turn
                    else:
                        string = input(UserText.ERROR)
                except ValueError or IndexError:
                    string = input(UserText.ERROR)

        if context == Context.SELECT_SAVE:
            while True:
                try:
                    saves = list(filter(lambda x: x[:4] == "save", os.listdir()))
                    number_of_saves = [save[4] for save in saves]
                    if string in number_of_saves:
                        return string
                    else:
                        string = input(UserText.ERROR)

                except ValueError:
                    string = input(UserText.ERROR)

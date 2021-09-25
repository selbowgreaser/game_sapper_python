import os
import pickle
import random as rand
from collections import deque

from config import *


class Minefield:
    def __init__(self, size, bombs):
        self.size = size
        self.bombs = bombs
        self.minefield = [[' ' for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.playing_field = [['■' for _ in self.minefield[0]] for _ in self.minefield]
        self.queue_coord = deque()
        self.bombs_generated = False
        self.flags = 0

    def gen_neighbors(self, x, y):
        neighbors = []
        for delta_1 in [-1, 0, 1]:
            for delta_2 in [-1, 0, 1]:
                x_new, y_new = x + delta_1, y + delta_2
                if 0 <= x_new <= self.size[0] - 1 and 0 <= y_new <= self.size[1] - 1 and (not delta_1 == delta_2 == 0):
                    neighbors.append(self.minefield[x_new][y_new])
        return neighbors

    def gen_coord_neighbors(self, x, y):
        coord_neighbors = []
        for delta_1 in [-1, 0, 1]:
            for delta_2 in [-1, 0, 1]:
                x_new = x + delta_1
                y_new = y + delta_2
                if 0 <= x_new <= self.size[0] - 1 and 0 <= y_new <= self.size[1] - 1 and (not delta_1 == delta_2 == 0):
                    coord_neighbors.append([x_new, y_new])
        return coord_neighbors

    def check_neighbors(self, x, y):
        neighbors = self.gen_neighbors(x, y)
        if '💣' in neighbors:
            self.playing_field[x][y] = neighbors.count('💣')
        else:
            self.playing_field[x][y] = ' '
            coord_neighbors = self.gen_coord_neighbors(x, y)
            self.queue_coord += deque(coord_neighbors)

    def set_bombs(self, X, Y):
        for _ in range(self.bombs):
            while True:
                x = rand.randint(0, self.size[0] - 1)
                y = rand.randint(0, self.size[1] - 1)
                if self.minefield[x][y] == '💣' or (x == X and y == Y) or [x, y] in self.gen_coord_neighbors(X, Y):
                    continue
                self.minefield[x][y] = '💣'
                break
        self.get_minefield()

    def set_flags(self, x, y):
        if self.playing_field[x][y] == 'F':
            self.playing_field[x][y] = '■'
            self.flags -= 1
        elif self.playing_field[x][y] == '■':
            self.playing_field[x][y] = 'F'
            self.flags += 1
        else:
            print(UserText.CANNOT_FLAG)

    def get_playing_field(self):
        print(f'МИН НА ПОЛЕ: {self.bombs}', end='')
        for line in self.playing_field:
            print(f'\n-{"----" * len(line)}\n| ', end='')
            for cell in line:
                print(cell, sep=' | ', end=' | ')
        print(f'\n-{"----" * len(line)}')

    def get_minefield(self):
        print('МИННОЕ ПОЛЕ', end='')
        for line in self.minefield:
            print(f'\n-{"----" * len(line)}\n| ', end='')
            for cell in line:
                print(cell, sep=' | ', end=' | ')
        print(f'\n-{"----" * len(line)}')

    def do_act(self, x, y, action):
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
        self.minefield = None
        self.isPlay = True

    def start(self):
        print(UserText.WELCOME)

        command = self.handler_message(input(UserText.HOW_START_GAME), Context.START_MENU)
        if command == Start.START_NEW_GAME:
            return self.new_game()
        if command == Start.LOAD_GAME:
            return self.load_game()
        if command == Start.EXIT:
            return exit()

    def new_game(self):
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
                return self.action()
            except:
                print(UserText.ERROR)
                return self.load_game()

    def save_game(self):
        if len(list(filter(lambda x: x[:4] == "save", os.listdir()))):
            number_of_save = max([int(save[4]) for save in filter(lambda x: x[:4] == "save", os.listdir())]) + 1
        else:
            number_of_save = 1
        with open(f'save{number_of_save}.pkl', 'wb') as save:
            pickle.dump(self.minefield, save)
            print(UserText.GAME_SAVED)
            return self.menu()

    def first_action(self):
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
        return sum([line.count('■') for line in field]) - self.minefield.bombs + self.minefield.flags

    def win_game(self):
        print(UserText.CONGRATULATIONS)
        return self.start()

    def lose_game(self):
        print(UserText.DEFEAT)
        return self.start()

    def handler_message(self, string, context):
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

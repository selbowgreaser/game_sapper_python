import random as rand
from collections import deque
import pickle


class Minefield:
    def __init__(self, size, bombs):
        self.size = size
        self.bombs = bombs
        self.minefield = [[' ' for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.playing_field = [[' ' for _ in self.minefield[0]] for _ in self.minefield]
        self.flags = bombs
        self.queue_coord = deque()
        print('Поле успешно сгенерировано!')

    def gen_neighbors(self, x, y):
        neighbors = []
        if x == 0 and y == 0:
            neighbors.append(self.minefield[x + 1][y])
            neighbors.append(self.minefield[x][y + 1])
            neighbors.append(self.minefield[x + 1][y + 1])
        elif x == 0 and y == self.size[1] - 1:
            neighbors.append(self.minefield[x + 1][y])
            neighbors.append(self.minefield[x + 1][y - 1])
            neighbors.append(self.minefield[x][y - 1])
        elif x == self.size[0] - 1 and y == 0:
            neighbors.append(self.minefield[x - 1][y])
            neighbors.append(self.minefield[x][y + 1])
            neighbors.append(self.minefield[x - 1][y + 1])
        elif x == self.size[0] - 1 and y == self.size[1] - 1:
            neighbors.append(self.minefield[x - 1][y])
            neighbors.append(self.minefield[x - 1][y - 1])
            neighbors.append(self.minefield[x][y - 1])

        elif x == 0:
            neighbors.append(self.minefield[x][y - 1])
            neighbors.append(self.minefield[x + 1][y - 1])
            neighbors.append(self.minefield[x + 1][y])
            neighbors.append(self.minefield[x + 1][y + 1])
            neighbors.append(self.minefield[x][y + 1])
        elif x == self.size[0] - 1:
            neighbors.append(self.minefield[x][y - 1])
            neighbors.append(self.minefield[x - 1][y - 1])
            neighbors.append(self.minefield[x - 1][y])
            neighbors.append(self.minefield[x - 1][y + 1])
            neighbors.append(self.minefield[x][y + 1])
        elif y == 0:
            neighbors.append(self.minefield[x - 1][y])
            neighbors.append(self.minefield[x - 1][y + 1])
            neighbors.append(self.minefield[x][y + 1])
            neighbors.append(self.minefield[x + 1][y + 1])
            neighbors.append(self.minefield[x + 1][y])
        elif y == self.size[1] - 1:
            neighbors.append(self.minefield[x - 1][y])
            neighbors.append(self.minefield[x - 1][y - 1])
            neighbors.append(self.minefield[x][y - 1])
            neighbors.append(self.minefield[x + 1][y - 1])
            neighbors.append(self.minefield[x + 1][y])

        else:
            neighbors.append(self.minefield[x - 1][y - 1])
            neighbors.append(self.minefield[x - 1][y])
            neighbors.append(self.minefield[x - 1][y + 1])
            neighbors.append(self.minefield[x][y + 1])
            neighbors.append(self.minefield[x + 1][y + 1])
            neighbors.append(self.minefield[x + 1][y])
            neighbors.append(self.minefield[x + 1][y - 1])
            neighbors.append(self.minefield[x][y - 1])

        return neighbors

    def gen_coord_neighbors(self, x, y):
        coord_neighbors = []
        if x == 0 and y == 0:
            coord_neighbors.append([x + 1, y])
            coord_neighbors.append([x, y + 1])
            coord_neighbors.append([x + 1, y + 1])
        elif x == 0 and y == self.size[1] - 1:
            coord_neighbors.append([x + 1, y])
            coord_neighbors.append([x + 1, y - 1])
            coord_neighbors.append([x, y - 1])
        elif x == self.size[0] - 1 and y == 0:
            coord_neighbors.append([x - 1, y])
            coord_neighbors.append([x, y + 1])
            coord_neighbors.append([x - 1, y + 1])
        elif x == self.size[0] - 1 and y == self.size[1] - 1:
            coord_neighbors.append([x - 1, y])
            coord_neighbors.append([x - 1, y - 1])
            coord_neighbors.append([x, y - 1])

        elif x == 0:
            coord_neighbors.append([x, y - 1])
            coord_neighbors.append([x + 1, y - 1])
            coord_neighbors.append([x + 1, y])
            coord_neighbors.append([x + 1, y + 1])
            coord_neighbors.append([x, y + 1])
        elif x == self.size[0] - 1:
            coord_neighbors.append([x, y - 1])
            coord_neighbors.append([x - 1, y - 1])
            coord_neighbors.append([x - 1, y])
            coord_neighbors.append([x - 1, y + 1])
            coord_neighbors.append([x, y + 1])
        elif y == 0:
            coord_neighbors.append([x - 1, y])
            coord_neighbors.append([x - 1, y + 1])
            coord_neighbors.append([x, y + 1])
            coord_neighbors.append([x + 1, y + 1])
            coord_neighbors.append([x + 1, y])
        elif y == self.size[1] - 1:
            coord_neighbors.append([x - 1, y])
            coord_neighbors.append([x - 1, y - 1])
            coord_neighbors.append([x, y - 1])
            coord_neighbors.append([x + 1, y - 1])
            coord_neighbors.append([x + 1, y])

        else:
            coord_neighbors.append([x - 1, y - 1])
            coord_neighbors.append([x - 1, y])
            coord_neighbors.append([x - 1, y + 1])
            coord_neighbors.append([x, y + 1])
            coord_neighbors.append([x + 1, y + 1])
            coord_neighbors.append([x + 1, y])
            coord_neighbors.append([x + 1, y - 1])
            coord_neighbors.append([x, y - 1])

        return coord_neighbors

    def check_neighbors(self, x, y):
        neighbors = self.gen_neighbors(x, y)
        if '*' in neighbors:
            self.playing_field[x][y] = neighbors.count('*')
        else:
            self.playing_field[x][y] = 0
            coord_neighbors = self.gen_coord_neighbors(x, y)
            self.queue_coord += deque(coord_neighbors)

    def set_bombs(self, X, Y):
        for _ in range(self.bombs):
            while True:
                x = rand.randint(0, self.size[0] - 1)
                y = rand.randint(0, self.size[1] - 1)
                if self.minefield[x][y] == '*' or (x == X and y == Y) or [x, y] in self.gen_coord_neighbors(X, Y):
                    continue
                self.minefield[x][y] = '*'
                break
        print('Бомбы установлены!')
        self.get_minefield()

    def set_flags(self, x, y):
        if self.playing_field[x][y] == 'F':
            self.playing_field[x][y] = ' '
        elif self.playing_field[x][y] == ' ':
            self.playing_field[x][y] = 'F'
        else:
            print('Нельзя поставить флаг в эту клетку')

    def get_playing_field(self):
        print('ПОЛЕ ИГРОКА', end='')
        for line in self.playing_field:
            print(f'\n-{"----" * len(line)}\n| ', end='')
            for cell in line:
                print(cell, sep=' | ', end=' | ')
        print()

    def get_minefield(self):
        print('МИННОЕ ПОЛЕ')
        for i in self.minefield:
            print(i)

    def do_act(self, x, y, action):
        if action == 'F':
            self.set_flags(x, y)

        elif action == 'O' and self.minefield[x][y] == '*':
            return Game().lose_game()

        elif self.minefield[x][y].isdigit() or self.minefield[x][y] == 'F':
            raise ValueError

        elif action == 'O':
            self.queue_coord.append([x, y])
            print(self.queue_coord)
            while self.queue_coord:
                x, y = self.queue_coord.popleft()
                if self.playing_field[x][y] == ' ':
                    self.check_neighbors(x, y)
                    print(self.queue_coord)
                    print(self.get_playing_field())

        else:
            raise ValueError


class Game:
    def __init__(self):
        self.minefield = None
        self.isPlay = True

    def start(self):
        print('Добро пожаловать в консольную игру "Сапер"!')
        command = input('Выберите действие: \n1. Новая игра \n2. Загрузить игру \n')

        if command == '1':
            return self.new_game()
        elif command == '2':
            return self.load_game()

    def new_game(self):
        command = input('Выберите размер поля: \n1. Стандарт \n2. Задать свои размеры '
                        'и количество бомб \n')

        if command == '1':
            self.minefield = Minefield((5, 5), rand.randint(2, 5))
        elif command == '2':
            line = int(input('Введите размер поля по вертикали: '))
            column = int(input('Введите размер поля по горизонтали: '))
            bombs = int(input('Введите количество бомб: '))

            self.minefield = Minefield((line, column), bombs)
        print('Игра началась! Вводите свои ходы в формате "X,Y,F/O", \n'
              'где X - строка, Y - столбец, F - поставить флаг в ячейку или убрать его, \n'
              'O - открыть ячейку. В любой момент можно написать "Меню", где можно \n'
              'сохранить, загрузить или начать новую игру! Удачи!')
        return self.first_step()

    def load_game(self):
        pass

    def save_game(self):
        pass

    def first_step(self):
        try:
            self.minefield.get_playing_field()

            action = input('Ваш ход: ')
            if action == 'Меню':
                return self.menu()
            X, Y, Action = action.split(',')
            X, Y = int(X), int(Y)
            if 1 <= X <= self.minefield.size[0] and 1 <= Y <= self.minefield.size[1]:
                self.minefield.set_bombs(X - 1, Y - 1)
                self.minefield.do_act(X - 1, Y - 1, Action)
            else:
                print('Вы ввели не корректное значение. Попробуйте снова.')
                return self.first_step()
            return self.action()

        except ValueError:
            print('Вы ввели не корректное значение. Попробуйте снова.')
            return self.first_step()

    def action(self):
        try:
            while self.is_win(self.minefield.playing_field) != 0:
                self.minefield.get_playing_field()
                print()
                self.minefield.get_minefield()

                action = input('Ваш ход: ')
                if action == 'Меню':
                    return self.menu()
                X, Y, Action = action.split(',')
                X, Y = int(X), int(Y)
                if 1 <= X <= self.minefield.size[0] and 1 <= Y <= self.minefield.size[1]:
                    self.minefield.do_act(X - 1, Y - 1, Action)
                else:
                    print('Вы ввели не корректное значение. Попробуйте снова.')
                    return self.action()
            return self.win_game()

        except ValueError:
            print('Вы ввели не корректное значение. Попробуйте снова.')
            return self.action()

    def menu(self):
        command = input('Выберите действие: \n1. Сохранить игру '
                        '\n2. Загрузить игру \n3. Начать новую игру \n')

    def is_win(self, field):
        return sum([line.count('O') for line in field]) - self.minefield.bombs

    def win_game(self):
        command = input('Поздравляем! Вы не подорвались на мине и успешно закончили игру! '
                        'Чтобы начать новую игру, введите 1,'
                        'чтобы загрузить игру, введите 2')
        if command == '1':
            return self.new_game()
        elif command == '2':
            return self.load_game()

    def lose_game(self):
        command = input('К сожалению, вы подорвались на мине :('
                        'Чтобы начать новую игру, введите 1,'
                        'чтобы загрузить игру, введите 2')
        if command == '1':
            return self.new_game()
        elif command == '2':
            return self.load_game()


Game().start()

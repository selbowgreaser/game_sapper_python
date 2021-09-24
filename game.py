import random as rand
import pickle


class Minefield:
    def __init__(self, size, bombs):
        self.size = size
        self.bombs = bombs
        self.minefield = [['O' for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.playerfield = [['O' for _ in self.minefield[0]] for _ in self.minefield]
        self.flags = bombs
        print('Поле успешно сгенерировано!')

    def set_bombs(self):
        for _ in range(self.bombs):
            while True:
                x = rand.randint(0, 4)
                y = rand.randint(0, 4)
                if self.minefield[x][y] == '*':
                    continue
                self.minefield[x][y] = '*'
                break
        print('Бомбы установлены!')

    def set_flags(self, x, y):
        if self.playerfield[x][y] == 'F':
            self.playerfield[x][y] = 'O'
        elif self.playerfield[x][y] == 'O':
            self.playerfield[x][y] = 'F'
        else:
            print('Нельзя поставить флаг в эту клетку')

    def get_playerfield(self):
        for i in self.playerfield:
            print(i)

    def do_act(self, x, y, action):
        if action == 'F':
            self.set_flags(x, y)

        elif action == 'O' and self.minefield[x][y] == '*':
            return Game().lose_game()

        elif self.minefield[x][y].isdigit() or self.minefield[x][y] == 'F':
            raise ValueError

        elif action == 'O' and self.playerfield[x][y] == 'O':
            print(x, y)
            return self.check_cell(x, y)

        else:
            raise ValueError

    def check_cell(self, x, y):
        if self.playerfield[x][y].isdigit() == False and self.minefield[x][y] != 'C':
            if x == 0 and y == 0:
                return self.check_corner_ul(x, y)
            if x == 0 and y == self.size[1] - 1:
                return self.check_corner_ur(x, y)
            if x == self.size[0] - 1 and y == 0:
                return self.check_corner_bl(x, y)
            if x == self.size[0] - 1 and y == self.size[1] - 1:
                return self.check_corner_br(x, y)

            if x == 0:
                return self.check_up(x, y)
            if x == self.size[0]:
                return self.check_bottom(x, y)
            if y == 0:
                return self.check_left(x, y)
            if y == self.size[1]:
                return self.check_right(x, y)

            return self.check_any(x, y)

    def check_corner_ul(self, x, y):
        bombs_near = 0

        if self.minefield[x + 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y] == 'O':
            self.minefield[x + 1][y] = 'C'
            self.check_cell(x + 1, y)

        if self.minefield[x][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y + 1] == 'O':
            self.minefield[x][y + 1] = 'C'
            self.check_cell(x, y + 1)

        if self.minefield[x + 1][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y + 1] == 'O':
            self.minefield[x + 1][y + 1] = 'C'
            self.check_cell(x + 1, y + 1)

            self.playerfield[x][y] = bombs_near

    def check_corner_ur(self, x, y):
        bombs_near = 0

        if self.minefield[x + 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y] == 'O':
            self.minefield[x + 1][y] = 'C'
            self.check_cell(x + 1, y)

        if self.minefield[x][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y - 1] == 'O':
            self.minefield[x][y - 1] = 'C'
            self.check_cell(x, y - 1)

        if self.minefield[x + 1][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y - 1] == 'O':
            self.minefield[x + 1][y - 1] = 'C'
            self.check_cell(x + 1, y - 1)

        self.playerfield[x][y] = bombs_near

    def check_corner_bl(self, x, y):
        bombs_near = 0

        if self.minefield[x - 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y] == 'O':
            self.minefield[x - 1][y] = 'C'
            self.check_cell(x - 1, y)

        if self.minefield[x][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y + 1] == 'O':
            self.minefield[x][y + 1] = 'C'
            self.check_cell(x, y + 1)

        if self.minefield[x - 1][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y + 1] == 'O':
            self.minefield[x - 1][y + 1] = 'C'
            self.check_cell(x - 1, y + 1)

        self.playerfield[x][y] = bombs_near

    def check_corner_br(self, x, y):
        bombs_near = 0

        if self.minefield[x - 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y] == 'O':
            self.minefield[x - 1][y] = 'C'
            self.check_cell(x - 1, y)

        if self.minefield[x][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y - 1] == 'O':
            self.minefield[x][y - 1] = 'C'
            self.check_cell(x, y - 1)

        if self.minefield[x - 1][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y - 1] == 'O':
            self.minefield[x - 1][y - 1] = 'C'
            self.check_cell(x - 1, y - 1)

        self.playerfield[x][y] = bombs_near

    def check_up(self, x, y):
        bombs_near = 0

        if self.minefield[x][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y - 1] == 'O':
            self.minefield[x][y - 1] = 'C'
            self.check_cell(x, y - 1)

        if self.minefield[x + 1][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y - 1] == 'O':
            self.minefield[x + 1][y - 1] = 'C'
            self.check_cell(x + 1, y - 1)

        if self.minefield[x + 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y] == 'O':
            self.minefield[x + 1][y] = 'C'
            self.check_cell(x + 1, y)

        if self.minefield[x + 1][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y + 1] == 'O':
            self.minefield[x + 1][y + 1] = 'C'
            self.check_cell(x + 1, y + 1)

        if self.minefield[x][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y + 1] == 'O':
            self.minefield[x][y + 1] = 'C'
            self.check_cell(x, y + 1)

        self.playerfield[x][y] = bombs_near

    def check_bottom(self, x, y):
        bombs_near = 0

        if self.minefield[x][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y - 1] == 'O':
            self.minefield[x][y - 1] = 'C'
            self.check_cell(x, y - 1)

        if self.minefield[x - 1][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y - 1] == 'O':
            self.minefield[x - 1][y - 1] = 'C'
            self.check_cell(x - 1, y - 1)

        if self.minefield[x - 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y] == 'O':
            self.minefield[x - 1][y] = 'C'
            self.check_cell(x - 1, y)

        if self.minefield[x - 1][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y + 1] == 'O':
            self.minefield[x - 1][y + 1] = 'C'
            self.check_cell(x - 1, y + 1)

        if self.minefield[x][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y + 1] == 'O':
            self.minefield[x][y + 1] = 'C'
            self.check_cell(x, y + 1)

        self.playerfield[x][y] = bombs_near

    def check_left(self, x, y):
        bombs_near = 0

        if self.minefield[x + 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y] == 'O':
            self.minefield[x + 1][y] = 'C'
            self.check_cell(x + 1, y)

        if self.minefield[x + 1][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y + 1] == 'O':
            self.minefield[x + 1][y + 1] = 'C'
            self.check_cell(x + 1, y + 1)

        if self.minefield[x][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y + 1] == 'O':
            self.minefield[x][y + 1] = 'C'
            self.check_cell(x, y + 1)

        if self.minefield[x + 1][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y + 1] == 'O':
            self.minefield[x + 1][y + 1] = 'C'
            self.check_cell(x + 1, y + 1)

        if self.minefield[x - 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y] == 'O':
            self.minefield[x - 1][y] = 'C'
            self.check_cell(x - 1, y)

        self.playerfield[x][y] = bombs_near

    def check_right(self, x, y):
        bombs_near = 0

        if self.minefield[x + 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y] == 'O':
            self.minefield[x + 1][y] = 'C'
            self.check_cell(x + 1, y)

        if self.minefield[x + 1][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y - 1] == 'O':
            self.minefield[x + 1][y - 1] = 'C'
            self.check_cell(x + 1, y - 1)

        if self.minefield[x][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y - 1] == 'O':
            self.minefield[x][y - 1] = 'C'
            self.check_cell(x, y - 1)

        if self.minefield[x + 1][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y - 1] == 'O':
            self.minefield[x + 1][y - 1] = 'C'
            self.check_cell(x + 1, y - 1)

        if self.minefield[x - 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y] == 'O':
            self.minefield[x - 1][y] = 'C'
            self.check_cell(x - 1, y)

        self.playerfield[x][y] = bombs_near

    def check_any(self, x, y):
        bombs_near = 0

        if self.minefield[x - 1][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y - 1] == 'O':
            self.minefield[x - 1][y - 1] = 'C'
            self.check_cell(x - 1, y - 1)

        if self.minefield[x - 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y] == 'O':
            self.minefield[x - 1][y] = 'C'
            self.check_cell(x - 1, y)

        if self.minefield[x - 1][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x - 1][y + 1] == 'O':
            self.minefield[x - 1][y + 1] = 'C'
            self.check_cell(x - 1, y + 1)

        if self.minefield[x][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y + 1] == 'O':
            self.minefield[x][y + 1] = 'C'
            self.check_cell(x, y + 1)

        if self.minefield[x + 1][y + 1] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y + 1] == 'O':
            self.minefield[x + 1][y + 1] = 'C'
            self.check_cell(x + 1, y + 1)

        if self.minefield[x + 1][y] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y] == 'O':
            self.minefield[x + 1][y] = 'C'
            self.check_cell(x + 1, y)

        if self.minefield[x + 1][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x + 1][y - 1] == 'O':
            self.minefield[x + 1][y - 1] = 'C'
            self.check_cell(x + 1, y - 1)

        if self.minefield[x][y - 1] == '*':
            bombs_near += 1
        elif self.minefield[x][y - 1] == 'O':
            self.minefield[x][y - 1] = 'C'
            self.check_cell(x, y - 1)

        self.playerfield[x][y] = bombs_near


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
        command = input('Выберите размер поля: \n1. Стандарт \n2. Задать свои размеры ' \
                        'и количество бомб \n')

        if command == '1':
            self.minefield = Minefield((5, 5), rand.randint(2, 5))
            self.minefield.set_bombs()
        elif command == '2':
            line = int(input('Введите размер поля по вертикали: '))
            column = int(input('Введите размер поля по горизонтали: '))
            bombs = int(input('Введите количество бомб: '))

            self.minefield = Minefield((line, column), bombs)
            self.minefield.set_bombs()
        print('Игра началась! Вводите свои ходы в формате "X,Y,F/O", \n' \
              'где X - строка, Y - столбец, F - поставить флаг в ячейку или убрать его, \n' \
              'O - открыть ячейку. В любой момент можно написать "Меню", где можно \n' \
              'сохранить, загрузить или начать новую игру! Удачи!')
        print(self.minefield.minefield)
        return self.action()

    def load_game(self):
        pass

    def save_game(self):
        pass

    def action(self):
        try:
            while self.is_win(self.minefield.minefield) != 0:
                self.minefield.get_playerfield()
                action = input('Ваш ход: ')
                if action == 'Меню':
                    return self.menu()
                X, Y, Action = action.split(',')
                X, Y = int(X), int(Y)
                if 0 <= X <= self.minefield.size[0] and 0 <= Y <= self.minefield.size[1]:
                    self.minefield.do_act(X, Y, Action)
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
        return sum([line.count('O') for line in field])

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

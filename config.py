from typing import NamedTuple

class Start(NamedTuple):
    START_NEW_GAME = '1'
    LOAD_GAME = '2'
    EXIT = '3'


class FieldSize(NamedTuple):
    STANDARD = '1'
    CUSTOM = '2'
    BACK = '3'


class Action(NamedTuple):
    OPEN = 'O'
    FLAG = 'F'


class Menu(NamedTuple):
    MENU = 'Меню'
    CONTINUE = '1'
    SAVE_GAME = '2'
    LOAD_GAME = '3'
    START_NEW_GAME = '4'
    EXIT = '5'


class Context(NamedTuple):
    START_MENU = 'START MENU'
    SELECT_FIELD = 'SELECT FIELD'
    CHOOSE_SIZES = 'CHOOSE SIZES'
    PLAYER_TURN = 'PLAYER TURN'
    MENU = 'MENU'
    SELECT_SAVE = 'SELECT SAVE'


class UserText(NamedTuple):
    WELCOME = 'Добро пожаловать в консольную игру "Сапер"!'
    SELECT_FIELD = 'Выберите размер поля: \n1. Стандарт \n2. Задать свои размеры ' \
                   'и количество бомб \n3. Назад\n'
    CHOOSE_SIZES = 'Введите через пробел размеры нового поля и количество бомб на нём...' \
                   'Максимальный размер поля ограничен 30 × 30!\n'
    HOW_START_GAME = 'Что вам нужно? \n1. Новая игра \n2. Загрузить игру \n3. Выход\n'
    ERROR = 'Что-то пошло не так... Попробуйте ещё раз!\n'
    SELECT_SAVE = 'Выберите номер сохранения:'
    NO_SAVE = 'Доступные сохранения отсутствуют'
    WILL_BE_CREATED = 'Будет создана новая игра'
    START_GAME = 'Игра началась! Вводите свои ходы в формате "X,Y,F/O", \n' \
                 'где X - строка, Y - столбец, F - поставить флаг в ячейку или убрать его, \n' \
                 'O - открыть ячейку. В любой момент после первого хода можно написать "Меню", где можно \n' \
                 'сохранить, загрузить или начать новую игру! Удачи!'
    GAME_SAVED = 'Игра успешно сохранена!'
    MENU = 'Выберите действие: \n1. Продолжить ' \
           '\n2. Сохранить игру \n3. Загрузить игру \n4. Начать новую игру \n5. Выход\n'
    CONGRATULATIONS = 'ПОЗДРАВЛЯЕМ! Вы не подорвались на мине и успешно разминировали поле!'
    DEFEAT = 'К сожалению, вы подорвались на мине :('
    ENTER_MOVE = 'Введите ход:\n'
    CANNOT_BE_SAVED = 'Нельзя сохраняться до генерации мин!'
    CANNOT_FLAG = 'Нельзя поставить флаг в эту клетку'

from random import randint                              # Метод randint () в Python возвращает
                                                        # случайное целочисленное значение между
                                                        #двумя нижними и верхними пределами
                                                        #(включая оба ограничения), предоставленными
                                                        # как два параметра.

class Dot:                                              # Собственный тип данных "Точка"
                                                        # class'ы обеспечивают возможность объединения данных
                                                        # и функциональности. Создание нового класса создает
                                                        # новый тип объекта. Экземпляры класса также могут
                                                        # иметь методы (определяемые его классом) для изменения
                                                        # его состояния.

    def __init__(self, x, y):                           # Метод __init__ используются для
                                                        # инициализации состояния объекта.
                                                        # Задача конструкторов - инициализировать
                                                        # (присвоить значения) членам данных класса при
                                                        # создании объекта класса.

        self.x = x                                      # Имя для аргумента, представляющего текущий
                                                        # объект класса.
                                                        # self — это стандартное имя первого аргумента
                                                        # для методов объекта
        self.y = y

    def __eq__(self, other):                            # Метод __eq__ вызывается при использовании
                                                        # оператора == для сравнения экземпляров класса.
        return self.x == other.x and self.y == other.y

    def __repr__(self):                                 # Метод __repr__ - используется для представления
                                                        # объектов класса в виде строки.
                                                        # Цель - быть однозначным.

        return f"({self.x}, {self.y})"                  # f означает форматированные строковые литералы,
                                                        # и это нововведение в Python 3.6.
                                                        # Форматированный строковый литерал или f-строка -
                                                        # это строковый литерал с префиксом «f» или «F».
                                                        # Эти строки могут содержать замещающие поля,
                                                        # которые представляют собой выражения,
                                                        # разделенные фигурными скобками {}.

class BoardException(Exception):                        # Собственный класс исключений
    pass

class BoardOutException(BoardException):
    def __str__(self):                                  # Метод __str__ в Python представляет объекты
                                                        # класса в виде строки - его можно использовать
                                                        # для классов. Метод __str__ должен быть определен
                                                        # таким образом, чтобы его было легко читать,
                                                        # и он должен выводить все члены класса.
                                                        # Этот метод также используется в качестве
                                                        # инструмента отладки, когда необходимо проверить
                                                        # члены класса.
                                                        # Цель - быть читаемым.
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

class BoardWrongShipException(BoardException):
    pass


class Ship:                                             # Класс "Корабль"
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property                                           # @property декоратор может быть использован для
                                                        # определения методов в классе,
                                                        # которые действуют как атрибуты.
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))         # Добавление элемента в конец списка.

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:                                            # Класс "Игровое поле"
    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"]*size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)


    def contour(self, ship, verb = False):              # Контур корабля и добавление его на доску"

        near =[                                         # Список с контуром вокруг одиночного корабля.
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for d in ship.dots:                                             # Запуск цикла for для определение размера
                                                                        # корабля и контура вокруг него.
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):                                                  # Отображение игрового поля
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))


    def shot(self, d):                                      # Стрельба по доске
        if self.out(d):
            raise BoardOutException()                       # raise - вывод (поднятие) исключения.

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:                             # Запуск цикла перебора попаданий по
                                                            # караблю и вывода отображения попадания
                                                            # и соответствующего сообщения.
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:                                               # Класс "Игрок"
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):                                           # Класс "Игрок - компьютер"
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d

class User(Player):                                         # Класс "Игрок - пользователь"
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите две координаты!")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:                                                 # Класс "Игра" и генерация досок

    def __init__(self, size = 6):                           # Конструктор и приветствие
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):                                 # Доска со случайной расстановкой кораблей.
        board = None
        while board is None:
            board = self.random_plase()
        return board

    def random_plase(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:                                      # Генерация случайной расстановки караблей.
            while True:
                attempts += 1
                if attempts > 2000:                         # Не более 2000 попыток.
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):                                        # Приветствие
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):                                         # Игровой цикл
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь")
                repeat = self.us.move()
            else:
                print("Ходит компьютер:")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):                                        # Метод "Start"
        self.greet()
        self.loop()

g = Game()                                                  # Запуск игры
g.start()

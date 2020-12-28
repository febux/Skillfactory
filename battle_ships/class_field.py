import random


# класс поля принимает в себя либо весь набор кораблей, либо только несколько,
# а также атрибут скрытности для поля ИИ
class BattleField:
    def __init__(self, size=6, hidden=False):
        ships = []
        self.size = size
        self.ships = ships
        self.hidden = hidden

        field = [["o" for j in range(size + 2)] for i in range(size + 2)]
        field[0][0] = "\\"

        for i in range(size):
            field[0][i + 1] = str(i + 1)
            field[i + 1][0] = str(i + 1)

        for i in range(size + 1):
            field[size + 1][i] = ""
            field[i][size + 1] = ""

        my_damage_count = 0
        ai_damage_count = 0
        used_coordinates = [[0, 0]]

        if hidden:
            self.damage = ai_damage_count
        else:
            self.damage = my_damage_count

        self.used_coordinates = used_coordinates
        self.field = field

    # добаляем корабль на поле
    def add_ship(self, ship):
        if not self.hidden:
            if ship.length == 3:
                self.field[ship.x][ship.y] = "▇"
                self.field[ship.x1][ship.y1] = "▇"
                self.field[ship.x2][ship.y2] = "▇"
            elif ship.length == 2:
                self.field[ship.x][ship.y] = "▇"
                self.field[ship.x1][ship.y1] = "▇"
            elif ship.length == 1:
                self.field[ship.x][ship.y] = "▇"

        self.ships.append(ship)

    # печатаем всё поле
    def print_field(self):
        for i in range(7):
            print(" ".join(self.field[i]) + "\n")

    # получаем значение урона
    @property
    def get_damage_count(self):
        return self.damage

    # получаем значения всего поля
    @property
    def get_values_field(self):
        return self.field

    # получаем значения всех кораблей
    @property
    def get_ships(self):
        return self.ships

    # получаем значение корабля с определёнными координатами
    def get_value_field(self, coordinates):
        return self.field[coordinates[0]][coordinates[1]]

    # устанавливаем значение с определёнными координатами
    def set_value_field(self, coordinates, value):
        self.field[coordinates[0]][coordinates[1]] = value

    # функция выстрелов для ИИ и игрока, с обработкой исключений и проверкой длины координат,
    # а также с проверкой занятости клеток поля
    def shot(self, player):
        # global my_damage_count, ai_damage_count
        shot_flag = 0

        while shot_flag == 0:

            if player == 2:
                temp = input("Enter coordinates of shot in row-column format, for example 32 or 65: ").lower()

                if temp == "exit":
                    return True

                try:
                    coordinates = list(map(int, temp))

                    if len(coordinates) != 2:
                        raise LengthException()
                except ValueError:
                    print("You entered wrong type of coordinates.")
                except LengthException:
                    print("You entered wrong length of coordinates.")
                else:

                    for ship in self.ships:
                        # print(ship)
                        if ship.length == 3:
                            if ((coordinates[0] == ship.x and coordinates[1] == ship.y)
                                    or (coordinates[0] == ship.x1 and coordinates[1] == ship.y1)
                                    or (coordinates[0] == ship.x2 and coordinates[1] == ship.y2)):
                                shot_flag = 1
                        if ship.length == 2:
                            if ((coordinates[0] == ship.x and coordinates[1] == ship.y)
                                    or (coordinates[0] == ship.x1 and coordinates[1] == ship.y1)):
                                shot_flag = 1
                        if ship.length == 1:
                            if coordinates[0] == ship.x and coordinates[1] == ship.y:
                                shot_flag = 1

                    if self.get_value_field(coordinates) == "o":
                        if shot_flag == 1:
                            self.set_value_field(coordinates, "X")
                            self.damage += 1
                        else:
                            self.set_value_field(coordinates, "T")
                            shot_flag = 1

                        print(f"Your shot is {coordinates[0]}:{coordinates[1]}")
                    else:
                        print("This cell is busy already, try again.")
                        shot_flag = 0

            if player == 1:
                coordinates = []
                flag_gen = 0

                while flag_gen == 0:
                    coordinates = [random.randint(1, 6), random.randint(1, 6)]
                    if coordinates not in self.used_coordinates:
                        self.used_coordinates.append(coordinates)
                        flag_gen = 1

                for ship in self.ships:
                    # print(ship)
                    if ship.length == 3:
                        if ((coordinates[0] == ship.x and coordinates[1] == ship.y)
                                or (coordinates[0] == ship.x1 and coordinates[1] == ship.y1)
                                or (coordinates[0] == ship.x2 and coordinates[1] == ship.y2)):
                            shot_flag = 1
                    if ship.length == 2:
                        if ((coordinates[0] == ship.x and coordinates[1] == ship.y)
                                or (coordinates[0] == ship.x1 and coordinates[1] == ship.y1)):
                            shot_flag = 1
                    if ship.length == 1:
                        if coordinates[0] == ship.x and coordinates[1] == ship.y:
                            shot_flag = 1

                if self.get_value_field(coordinates) == "o" or self.get_value_field(coordinates) == "▇":
                    if shot_flag == 1:
                        self.set_value_field(coordinates, "X")
                        self.damage += 1
                    else:
                        self.set_value_field(coordinates, "T")
                        shot_flag = 1
                    print(f"AI's shot is {coordinates[0]}:{coordinates[1]}")

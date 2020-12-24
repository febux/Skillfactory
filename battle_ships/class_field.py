import random


# класс поля принимает в себя либо весь набор кораблей, либо только несколько,
# а также атрибут скрытности для поля ИИ
class BattleField:
    def __init__(self, ships, hidden=False):
        self.ships = ships
        self.hidden = hidden

        field = [["o" for j in range(8)] for i in range(8)]
        field[0][0] = "\\"

        for i in range(6):
            field[0][i + 1] = str(i + 1)
            field[i + 1][0] = str(i + 1)

        for i in range(7):
            field[7][i] = ""
            field[i][7] = ""

        if ships != "" and not hidden:
            for i in range(len(ships)):
                if len(ships[i]) == 6:
                    for j in (0, 2, 4):
                        field[ships[i][j]][ships[i][j + 1]] = "▇"
                elif len(ships[i]) == 4:
                    for j in (0, 2):
                        field[ships[i][j]][ships[i][j + 1]] = "▇"
                elif len(ships[i]) == 2:
                    field[ships[i][0]][ships[i][0 + 1]] = "▇"

        my_damage_count = 0
        ai_damage_count = 0
        used_coordinates = [[0, 0]]

        if hidden:
            self.damage = ai_damage_count
        else:
            self.damage = my_damage_count

        self.used_coordinates = used_coordinates
        self.field = field

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
                    temp_ships = self.ships

                    if len(coordinates) == 2:
                        for i in range(7):
                            if len(temp_ships[i]) == 6:
                                for j in (0, 2, 4):
                                    if coordinates == temp_ships[i][j:j + 2]:
                                        shot_flag = 1
                            if len(temp_ships[i]) == 4:
                                for j in (0, 2):
                                    if coordinates == temp_ships[i][j:j + 2]:
                                        shot_flag = 1
                            if len(temp_ships[i]) == 2:
                                if coordinates == temp_ships[i][0:2]:
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

                temp_ships = self.ships

                for i in range(7):
                    if len(temp_ships[i]) == 6:
                        for j in (0, 2, 4):
                            if coordinates == temp_ships[i][j:j + 2]:
                                shot_flag = 1
                    if len(temp_ships[i]) == 4:
                        for j in (0, 2):
                            if coordinates == temp_ships[i][j:j + 2]:
                                shot_flag = 1
                    if len(temp_ships[i]) == 2:
                        if coordinates == temp_ships[i][0:2]:
                            shot_flag = 1

                if self.get_value_field(coordinates) == "o" or self.get_value_field(coordinates) == "▇":
                    if shot_flag == 1:
                        self.set_value_field(coordinates, "X")
                        self.damage += 1
                    else:
                        self.set_value_field(coordinates, "T")
                        shot_flag = 1
                    print(f"AI's shot is {coordinates[0]}:{coordinates[1]}")
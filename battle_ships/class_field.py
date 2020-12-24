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

        self.field = field

    # печатаем всё поле
    def print_field(self):
        for i in range(7):
            print(" ".join(self.field[i]) + "\n")

    # получаем значения всего поля
    def get_values_field(self):
        return self.field

    # получаем значения всех кораблей
    def get_ships(self):
        return self.ships

    # получаем значение корабля с определёнными координатами
    def get_value_field(self, coordinates):
        return self.field[coordinates[0]][coordinates[1]]

    # устанавливаем значение с определёнными координатами
    def set_value_field(self, coordinates, value):
        self.field[coordinates[0]][coordinates[1]] = value

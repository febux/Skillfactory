from class_field import BattleField
from class_ship import BattleShip
from class_exception import LengthException
import random

ships_patterns = [
    [[1, 1, 1, 2, 1, 3], [2, 5, 2, 6], [3, 1, 3, 2], [4, 4], [5, 2], [5, 6], [6, 4]],
    [[1, 3, 1, 4, 1, 5], [3, 1, 3, 2], [4, 5, 4, 6], [5, 1], [1, 1], [6, 6], [6, 3]],
    [[2, 3, 2, 4, 2, 5], [4, 1, 4, 2], [4, 5, 4, 6], [1, 1], [6, 1], [6, 3], [6, 6]],
    [[4, 2, 4, 3, 4, 4], [1, 1, 1, 2], [6, 5, 6, 6], [1, 6], [2, 4], [6, 1], [3, 6]],
    [[5, 2, 5, 3, 5, 4], [1, 5, 1, 6], [3, 5, 3, 6], [1, 1], [2, 3], [3, 1], [6, 6]],
    [[2, 2, 3, 2, 4, 2], [1, 5, 1, 6], [5, 6, 6, 6], [3, 6], [6, 1], [5, 4], [3, 4]],
    [[1, 2, 2, 2, 3, 2], [1, 6, 2, 6], [6, 1, 6, 2], [6, 6], [1, 4], [4, 4], [4, 6]],
    [[4, 6, 5, 6, 6, 6], [1, 1, 1, 2], [3, 1, 4, 1], [1, 6], [2, 4], [4, 3], [6, 1]]
]


# функция ввода значений кораблей для игрока с проверкой на длину кораблей и обработкой исключений
def enter_value(field, number_ship):

    length = 0
    text = ''

    if number_ship == 0:
        text = "Enter coordinates 3-cells ship in row-column format, for example 232425: "
        length = 6
    if number_ship == 1 or number_ship == 2:
        text = "Enter coordinates 2-cells ship in row-column format, for example 3334: "
        length = 4
    if number_ship == 3 or number_ship == 4 or number_ship == 5 or number_ship == 6:
        text = "Enter coordinates 1-cells ship in row-column format, for example 61: "
        length = 2

    while True:
        temp = input(text).lower()

        if temp == "exit":
            return True

        try:
            final_value = list(map(int, temp))

            if len(final_value) != length:
                raise LengthException()
        except ValueError:
            print("You entered wrong type of coordinates.")
        except LengthException:
            print("You entered wrong length of coordinates.")
        else:
            if len(final_value) == length:
                ship = BattleShip(final_value)

                if ship.check_dist(field.get_values_field, field.size):
                    print()
                    print(f"Amount of ships: {number_ship + 1}/7")
                    print()
                    return ship


# функция проверки выигрыша по количеству урона
def check_win(field):

    if field.get_damage_count == 11:
        return True
    else:
        return False


# функция игры
def new_game():

    my_field = BattleField()
    my_field.print_field()
    print("OKAY, We have a field and we need to fill it by ships.\n")
    print("If you enter \"Exit\" instead of coordinates, you are going to main menu. Remember it! \n")

    for i in range(7):
        if i == 0:
            ship = enter_value(my_field, i)
            if ship is True:
                return True
            else:
                my_field.add_ship(ship)
                my_field.print_field()
        elif i == 1 or i == 2:
            ship = enter_value(my_field, i)
            if ship is True:
                return True
            else:
                my_field.add_ship(ship)
                my_field.print_field()
        elif i == 3 or i == 4 or i == 5 or i == 6:
            ship = enter_value(my_field, i)
            if ship is True:
                return True
            else:
                my_field.add_ship(ship)
                my_field.print_field()

    # print(my_field.get_ships)
    print()
    print("Now the field is filled with ships.\n")

    rand = random.randint(0, 7)
    ai_field = BattleField(hidden=True)
    for i in range(7):
        ship = BattleShip(ships_patterns[rand][i])
        ai_field.add_ship(ship)

    print()
    print("The field of AI (Artificial Intelligence) is filled with ships too.\n")
    print("Now start to shoot! You are the first.")
    while True:
        print("You shoot!")
        print()
        ai_field.print_field()
        if ai_field.shot(2):
            return True

        print()
        ai_field.print_field()
        print()

        if check_win(ai_field):
            print("You win!")
            return True

        print("Now AI shoot!")
        print()
        my_field.shot(1)

        print()
        my_field.print_field()
        print()

        if check_win(my_field):
            print("AI wins!")
            return True


# функция главного меню, где можно начать игру или закончить
# также игрок сюда возвращается вводом "exit" вместо координат
def main_menu():
    print("Welcome to The BattleShips!")
    start_flag = input("For starting game enter Start, for closing - any other key: ").lower()
    print()

    if start_flag == "start":
        if new_game():
            main_menu()
    else:
        input("Press any key for closing...")


print("Hello someone!")
main_menu()

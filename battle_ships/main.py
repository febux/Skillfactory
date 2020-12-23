from class_field import BattleField
from class_ship import BattleShip
import random

my_damage_count = 0
ai_damage_count = 0
ships = []
used_coordinates = [[0, 0]]
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


def enter_value(my_field, number_ship):
    global ships, ships_patterns
    final_value_flag = 0
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

    while final_value_flag == 0:
        temp = input(text).lower()

        if temp == "exit":
            return True

        try:
            final_value = list(map(int, temp))
        except ValueError:
            print("You entered wrong type of coordinates.")
        except IndexError:
            print("You entered wrong length of coordinates.")
        else:
            if len(final_value) == length:
                ship = BattleShip(final_value)

                if ship.check_dist(my_field.get_values_field()):
                    ships.append(list(ship.get_coordinates()))
                    # print(ships)
                    print()
                    print(f"Amount of ships: {number_ship + 1}/7")
                    print()
                    final_value_flag = 1
            else:
                print("You entered wrong length of coordinates.")


def shot(field, field_ind):
    global my_damage_count, ai_damage_count
    shot_flag = 0

    while shot_flag == 0:

        if field_ind == 2:
            temp = input("Enter coordinates of shot in row-column format, for example 32 or 65: ").lower()

            if temp == "exit":
                return True

            try:
                coordinates = list(map(int, temp))
            except ValueError:
                print("You entered wrong type of coordinates.")
            except IndexError:
                print("You entered wrong length of coordinates.")
            else:
                temp_ships = field.get_ships()

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

                    if field.get_value_field(coordinates) == "o":
                        if shot_flag == 1:
                            field.set_value_field(coordinates, "X")
                            ai_damage_count += 1
                            # print(ai_damage_count)
                        else:
                            field.set_value_field(coordinates, "T")
                            shot_flag = 1
                    else:
                        print("This cell is busy already, try again.")
                        shot_flag = 0
                else:
                    print("You entered wrong length of coordinates.")

        if field_ind == 1:
            coordinates = []
            flag_gen = 0

            while flag_gen == 0:
                coordinates = [random.randint(1, 6), random.randint(1, 6)]
                if coordinates not in used_coordinates:
                    used_coordinates.append(coordinates)
                    # print(used_coordinates)
                    flag_gen = 1

            temp_ships = field.get_ships()

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

            if field.get_value_field(coordinates) == "o" or field.get_value_field(coordinates) == "▇":
                if shot_flag == 1:
                    field.set_value_field(coordinates, "X")
                    my_damage_count += 1
                    # print(my_damage_count)
                else:
                    field.set_value_field(coordinates, "T")
                    shot_flag = 1


def check_win():
    global my_damage_count, ai_damage_count

    if my_damage_count == 11:
        return 2
    elif ai_damage_count == 11:
        return 1
    else:
        return False


def new_game():
    global ships
    my_field = BattleField("")
    my_field.print_field()
    print("OKAY, We have a field and we need to fill it by ships.\n")
    print("If you enter \"Exit\" instead of coordinates, you are going to main menu. Remember it! \n")

    for i in range(7):
        if i == 0:
            if enter_value(my_field, i):
                return True
            else:
                my_field = BattleField(ships)
                my_field.print_field()
        elif i == 1 or i == 2:
            if enter_value(my_field, i):
                return True
            else:
                my_field = BattleField(ships)
                my_field.print_field()
        elif i == 3 or i == 4 or i == 5 or i == 6:
            if enter_value(my_field, i):
                return True
            else:
                my_field = BattleField(ships)
                my_field.print_field()

    print()
    print("Now the field is filled with ships.\n")

    rand = random.randint(0, 7)
    ai_field = BattleField(ships_patterns[rand], True)
    print(".......")
    print("The field of AI (Artificial Intelligence) is filled with ships too.\n")
    # ai_field.print_field()
    # print(ai_field.get_ships())
    print("Now start to shoot! You are the first.")
    while check_win() != 1 or check_win() != 2:
        print("You shoot!")
        print()
        ai_field.print_field()
        if shot(ai_field, 2):
            return True
        # print(check_win())
        # print(ai_field.get_ships())
        print()
        ai_field.print_field()
        print()
        if check_win() == 1:
            print("You win!")
            return True
        if check_win() == 2:
            print("AI wins!")
            return True

        print("Now AI shoot!")
        print()
        # my_field.print_field()
        shot(my_field, 1)
        # print(check_win())
        # print(my_field.get_ships())
        print()
        my_field.print_field()
        print()

        if check_win() == 1:
            print("You win!")
            return True
        if check_win() == 2:
            print("AI wins!")
            return True


def main_menu():
    global ships
    print("Welcome to The BattleShips!")
    start_flag = input("For starting game enter Start, for closing - any other key: ").lower()
    print()

    if start_flag == "start":
        if new_game():
            ships = []
            main_menu()
    else:
        input("Press any key for closing...")


print("Hello someone!")
main_menu()

# класс корабля принимает в себя набор координат с определённой длинной
class BattleShip:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        if len(coordinates) == 6:
            self.x = coordinates[0]
            self.y = coordinates[1]
            self.x1 = coordinates[2]
            self.y1 = coordinates[3]
            self.x2 = coordinates[4]
            self.y2 = coordinates[5]
        elif len(coordinates) == 4:
            self.x = coordinates[0]
            self.y = coordinates[1]
            self.x1 = coordinates[2]
            self.y1 = coordinates[3]
        elif len(coordinates) == 2:
            self.x = coordinates[0]
            self.y = coordinates[1]

    # проверка расстояния в одну клетку при выставлении кораблей на поле,
    # также проверка связанности координат
    def check_dist(self, massive):
        if len(self.coordinates) == 6:
            if (self.x == 0 or self.y == 0 or self.x1 == 0 or self.y1 == 0 or self.x2 == 0 or self.y2 == 0
                    or self.x >= 7 or self.x1 >= 7 or self.y >= 7 or self.y1 >= 7 or self.x2 >= 7 or self.y2 >= 7):
                print("Error 0: the coordinates have 0 value or value over than 7!")
                return False

            if ((self.x == self.x1 and self.y == self.y1) or (self.x == self.x2 and self.y == self.y2)
                    or (self.x1 == self.x2 and self.y1 == self.y2)):
                print("Error 1: some or all of the coordinates are the same!")
                return False

            if ((massive[self.x][self.y] == "▇")
                    or (massive[self.x + 1][self.y] == "▇")
                    or (massive[self.x - 1][self.y] == "▇")
                    or (massive[self.x][self.y + 1] == "▇")
                    or (massive[self.x][self.y - 1] == "▇")
                    or (massive[self.x + 1][self.y + 1] == "▇")
                    or (massive[self.x - 1][self.y - 1] == "▇")
                    or (massive[self.x + 1][self.y - 1] == "▇")
                    or (massive[self.x - 1][self.y + 1] == "▇")):
                print("Error 2: there is another ship nearby!")
                return False

            if not ((self.x1 == self.x + 1 and self.y1 == self.y)
                    or (self.x1 == self.x - 1 and self.y1 == self.y)
                    or (self.x1 == self.x and self.y1 == self.y + 1)
                    or (self.x1 == self.x and self.y1 == self.y - 1)):
                print("Error 3: the coordinates are too far from each other!")
                return False

            if self.x1 == self.x + 1 and self.y1 == self.y:
                if (massive[self.x1 + 1][self.y1] == "▇"
                        or massive[self.x1 + 1][self.y1 + 1] == "▇"
                        or massive[self.x1 + 1][self.y1 - 1] == "▇"
                        or massive[self.x1][self.y1 + 1] == "▇"
                        or massive[self.x1][self.y1 - 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if self.x1 == self.x - 1 and self.y1 == self.y:
                if (massive[self.x1 - 1][self.y1] == "▇"
                        or massive[self.x1 - 1][self.y1 + 1] == "▇"
                        or massive[self.x1 - 1][self.y1 - 1] == "▇"
                        or massive[self.x1][self.y1 + 1] == "▇"
                        or massive[self.x1][self.y1 - 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if self.x1 == self.x and self.y1 == self.y + 1:
                if (massive[self.x1 + 1][self.y1] == "▇"
                        or massive[self.x1 - 1][self.y1] == "▇"
                        or massive[self.x1][self.y1 + 1] == "▇"
                        or massive[self.x1 + 1][self.y1 + 1] == "▇"
                        or massive[self.x1 - 1][self.y1 + 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if self.x1 == self.x and self.y1 == self.y - 1:
                if (massive[self.x1 + 1][self.y1] == "▇"
                        or massive[self.x1 + 1][self.y1 - 1] == "▇"
                        or massive[self.x1 - 1][self.y1] == "▇"
                        or massive[self.x1 - 1][self.y1 - 1] == "▇"
                        or massive[self.x1][self.y1 - 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if ((massive[self.x1][self.y1] == "▇")
                    or (massive[self.x1 + 1][self.y1] == "▇")
                    or (massive[self.x1 - 1][self.y1] == "▇")
                    or (massive[self.x1][self.y1 + 1] == "▇")
                    or (massive[self.x1][self.y1 - 1] == "▇")):
                print("Error 5: there is another ship nearby!")
                return False

            if self.x1 == self.x + 1 and self.y1 == self.y:
                if not ((self.x2 == self.x1 + 1 and self.y2 == self.y1)
                        or (self.x2 == self.x - 1 and self.y2 == self.y)):
                    print("Error 6: one of the coordinates has wrong place!")
                    return False

            if self.x1 == self.x - 1 and self.y1 == self.y:
                if not ((self.x2 == self.x1 - 1 and self.y2 == self.y1)
                        or (self.x2 == self.x + 1 and self.y2 == self.y)):
                    print("Error 6: one of the coordinates has wrong place!")
                    return False

            if self.x1 == self.x and self.y1 == self.y + 1:
                if not ((self.x2 == self.x1 and self.y2 == self.y1 + 1)
                        or (self.x2 == self.x and self.y2 == self.y - 1)):
                    print("Error 6: one of the coordinates has wrong place!")
                    return False

            if self.x1 == self.x and self.y1 == self.y - 1:
                if not ((self.x2 == self.x1 + 1 and self.y2 == self.y1 - 1)
                        or (self.x2 == self.x - 1 and self.y2 == self.y + 1)):
                    print("Error 6: one of the coordinates has wrong place!")
                    return False

            if not ((self.x2 == self.x1 + 1 and self.y2 == self.y1)
                    or (self.x2 == self.x1 - 1 and self.y2 == self.y1)
                    or (self.x2 == self.x1 and self.y2 == self.y1 + 1)
                    or (self.x2 == self.x1 and self.y2 == self.y1 - 1)):
                print("Error 3: the coordinates are too far from each other!")
                return False

            if self.x2 == self.x1 + 1 and self.y2 == self.y1:
                if (massive[self.x2 + 1][self.y2] == "▇"
                        or massive[self.x2 + 1][self.y2 + 1] == "▇"
                        or massive[self.x2 + 1][self.y2 - 1] == "▇"
                        or massive[self.x2][self.y2 + 1] == "▇"
                        or massive[self.x2][self.y2 - 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if self.x2 == self.x1 - 1 and self.y2 == self.y:
                if (massive[self.x2 - 1][self.y2] == "▇"
                        or massive[self.x2 - 1][self.y2 + 1] == "▇"
                        or massive[self.x2 - 1][self.y2 - 1] == "▇"
                        or massive[self.x2][self.y2 + 1] == "▇"
                        or massive[self.x2][self.y2 - 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if self.x2 == self.x1 and self.y2 == self.y1 + 1:
                if (massive[self.x2 + 1][self.y2] == "▇"
                        or massive[self.x2 - 1][self.y2] == "▇"
                        or massive[self.x2][self.y2 + 1] == "▇"
                        or massive[self.x2 + 1][self.y2 + 1] == "▇"
                        or massive[self.x2 - 1][self.y2 + 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if self.x2 == self.x1 and self.y2 == self.y1 - 1:
                if (massive[self.x2 + 1][self.y2] == "▇"
                        or massive[self.x2 + 1][self.y2 - 1] == "▇"
                        or massive[self.x2 - 1][self.y2] == "▇"
                        or massive[self.x2 - 1][self.y2 - 1] == "▇"
                        or massive[self.x2][self.y2 - 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if ((massive[self.x2][self.y2] == "▇")
                    or (massive[self.x2 + 1][self.y2] == "▇")
                    or (massive[self.x2 - 1][self.y2] == "▇")
                    or (massive[self.x2][self.y2 + 1] == "▇")
                    or (massive[self.x2][self.y2 - 1] == "▇")):
                print("Error 5: there is another ship nearby!")
                return False

            else:
                return True
        elif len(self.coordinates) == 4:

            if (self.x == 0 or self.y == 0 or self.x1 == 0 or self.y1 == 0
                    or self.x >= 7 or self.x1 >= 7 or self.y >= 7 or self.y1 >= 7):
                print("Error 0: the coordinates have 0 value or value over than 7!")
                return False

            if self.x == self.x1 and self.y == self.y1:
                print("Error 1: some or all of the coordinates are the same!")
                return False

            if ((massive[self.x][self.y] == "▇")
                    or (massive[self.x + 1][self.y] == "▇")
                    or (massive[self.x - 1][self.y] == "▇")
                    or (massive[self.x][self.y + 1] == "▇")
                    or (massive[self.x][self.y - 1] == "▇")
                    or (massive[self.x + 1][self.y + 1] == "▇")
                    or (massive[self.x - 1][self.y - 1] == "▇")
                    or (massive[self.x + 1][self.y - 1] == "▇")
                    or (massive[self.x - 1][self.y + 1] == "▇")):
                print("Error 2: there is another ship nearby!")
                return False

            if not ((self.x1 == self.x + 1 and self.y1 == self.y)
                    or (self.x1 == self.x - 1 and self.y1 == self.y)
                    or (self.x1 == self.x and self.y1 == self.y + 1)
                    or (self.x1 == self.x and self.y1 == self.y - 1)):
                print("Error 3: the coordinates are too far from each other!")
                return False

            if self.x1 == self.x + 1 and self.y1 == self.y:
                if (massive[self.x1 + 1][self.y1] == "▇"
                        or massive[self.x1 + 1][self.y1 + 1] == "▇"
                        or massive[self.x1 + 1][self.y1 - 1] == "▇"
                        or massive[self.x1][self.y1 + 1] == "▇"
                        or massive[self.x1][self.y1 - 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if self.x1 == self.x - 1 and self.y1 == self.y:
                if (massive[self.x1 - 1][self.y1] == "▇"
                        or massive[self.x1 - 1][self.y1 + 1] == "▇"
                        or massive[self.x1 - 1][self.y1 - 1] == "▇"
                        or massive[self.x1][self.y1 + 1] == "▇"
                        or massive[self.x1][self.y1 - 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if self.x1 == self.x and self.y1 == self.y + 1:
                if (massive[self.x1 + 1][self.y1] == "▇"
                        or massive[self.x1 - 1][self.y1] == "▇"
                        or massive[self.x1][self.y1 + 1] == "▇"
                        or massive[self.x1 + 1][self.y1 + 1] == "▇"
                        or massive[self.x1 - 1][self.y1 + 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if self.x1 == self.x and self.y1 == self.y - 1:
                if (massive[self.x1 + 1][self.y1] == "▇"
                        or massive[self.x1 + 1][self.y1 - 1] == "▇"
                        or massive[self.x1 - 1][self.y1] == "▇"
                        or massive[self.x1 - 1][self.y1 - 1] == "▇"
                        or massive[self.x1][self.y1 - 1] == "▇"):
                    print("Error 4: there is another ship nearby!")
                    return False

            if ((massive[self.x1][self.y1] == "▇")
                    or (massive[self.x1 + 1][self.y1] == "▇")
                    or (massive[self.x1 - 1][self.y1] == "▇")
                    or (massive[self.x1][self.y1 + 1] == "▇")
                    or (massive[self.x1][self.y1 - 1] == "▇")):
                print("Error 5: there is another ship nearby!")
                return False

            else:
                return True

        elif len(self.coordinates) == 2:

            if self.x == 0 or self.y == 0 or self.x >= 7 or self.y >= 7:
                print("Error 0: the coordinates have 0 value or value over than 7!")
                return False

            if ((massive[self.x][self.y] == "▇")
                    or (massive[self.x + 1][self.y] == "▇")
                    or (massive[self.x - 1][self.y] == "▇")
                    or (massive[self.x][self.y + 1] == "▇")
                    or (massive[self.x][self.y - 1] == "▇")
                    or (massive[self.x + 1][self.y + 1] == "▇")
                    or (massive[self.x - 1][self.y - 1] == "▇")
                    or (massive[self.x + 1][self.y - 1] == "▇")
                    or (massive[self.x - 1][self.y + 1] == "▇")):
                print("Error 2: there is another ship nearby!")
                return False
            else:
                return True

    # получить координаты корабля
    def get_coordinates(self):
        if len(self.coordinates) == 6:
            return self.x, self.y, self.x1, self.y1, self.x2, self.y2
        elif len(self.coordinates) == 4:
            return self.x, self.y, self.x1, self.y1
        elif len(self.coordinates) == 2:
            return self.x, self.y

class Rectangle:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def get_area(self):
        return self.width * self.height

    def get_info(self):
        list_ = (self.x, self.y, self.width, self.height)
        print("Rectangle " + str(list_))

class Square:

    def __init__(self, x, y, l):
        self.x = x
        self.y = y
        self.lenght = l

    def get_area(self):
        return self.lenght ** 2

    def get_info(self):
        list_ = (self.x, self.y, self.lenght)
        print("Square " + str(list_))

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r

    def get_area(self):
        return (self.radius ** 2) * 3.14

    def get_info(self):
        list_ = (self.x, self.y, self.radius)
        print("Circle " + str(list_))

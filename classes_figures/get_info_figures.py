from classes import Rectangle, Square, Circle

type_of_figure = 0
figure = 0
figures = ["rectangle", "square", "circle"]

def enter_values():
    global type_of_figure
    type_of_figure = str(input("Enter type of figure (rectangle, square, circle): ")).lower()
    if type_of_figure in figures:
        return True
    else:
        return False

while enter_values() != True:
    print("You entered wrong type of figure, please, try again.\n")

if type_of_figure == "rectangle":
    type_of_figure = "Rectangle"
    x = int(input("Enter value x: "))
    y = int(input("Enter value y: "))
    width = int(input("Enter value width: "))
    height = int(input("Enter value height: "))
    figure = Rectangle(x, y, width, height)
elif type_of_figure == "square":
    type_of_figure = "Square"
    x = int(input("Enter value x: "))
    y = int(input("Enter value y: "))
    lenght = int(input("Enter value lenght: "))
    figure = Square(x, y, lenght)
elif type_of_figure == "circle":
    type_of_figure = "Circle"
    x = int(input("Enter value x: "))
    y = int(input("Enter value y: "))
    radius = int(input("Enter value radius: "))
    figure = Circle(x, y, radius)
else:
    print("You entered wrong type of figure, please, try again.\n")

figure.get_info()

input("Press to close...")

class Pet:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

class Cat(Pet):
    kind = "Cat"
    def get_info(self):
        return self.kind, self.name, self.gender, self.age

    def get_kind(self):
        return self.kind

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_age(self):
        return self.age

class Dog(Pet):
    kind = "Dog"

    def get_info(self):
        return self.kind, self.name, self.gender, self.age

    def get_kind(self):
        return self.kind

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_age(self):
        return self.age

class Parrot(Pet):
    kind = "Parrot"

    def get_info(self):
        return self.kind, self.name, self.gender, self.age

    def get_kind(self):
        return self.kind

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_age(self):
        return self.age

class Pet:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age


class Cat(Pet):
    kind = "Cat"

#    def __repr__(self):
#        return '({kind}; {name}; {gender}; {age})'.format(kind=self.kind, name=self.name,
#                                                          gender=self.gender, age=self.age)

    def get_info(self):
        print("Kind of pet:", self.kind)
        print("Name:", self.name)
        print("Gender:", self.gender)
        print("Age:", self.age)
        print()

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
        print("Kind of pet:", self.kind)
        print("Name:", self.name)
        print("Gender:", self.gender)
        print("Age:", self.age)
        print()

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
        print("Kind of pet:", self.kind)
        print("Name:", self.name)
        print("Gender:", self.gender)
        print("Age:", self.age)
        print()

    def get_kind(self):
        return self.kind

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_age(self):
        return self.age

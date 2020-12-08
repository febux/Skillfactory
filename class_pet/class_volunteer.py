class Volunteer:
    part = False

    def __init__(self, name, city, status):
        self.name = name
        self.city = city
        self.status = status

    def get_part_info(self):
        return self.name, self.city, self.status, self.part

    def get_info(self):
        print("Volunteer: " + str(self.name) + "\nCity: " + str(self.city)
              + "\nStatus: " + str(self.status))


class Participant(Volunteer):
    part = "Corporate Participant"

    def get_part_info(self):
        return self.name, self.city, self.status, self.part

    def get_info(self):
        print("Volunteer: " + str(self.name) + "\nCity: " + str(self.city)
              + "\nStatus: " + str(self.status) + "\n" + str(self.part))


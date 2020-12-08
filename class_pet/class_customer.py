history = {}
count = 0


class Customer:
    def __init__(self, name, account=0):
        self.name = name
        self.account = account

    def get_info(self):
        print("Customer: " + str(self.name) + "\nAccount: " + str(self.account))

    def refill(self, amount):
        self.account += amount
        global history
        global count
        temp = "+" + str(amount)
        history[count] = temp
        count += 1

    def payment(self, amount):
        self.account -= amount
        global history
        global count
        temp = "-" + str(amount)
        history[count] = temp
        count += 1

    def get_info_account_operations(self):
        global history
        global count
        print()
        print("Name: ", self.name)
        print("Operations: ")
        for i in range(0, count):
            print(history[i])
        print("Current amount: ", self.account)
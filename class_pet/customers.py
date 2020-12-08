from class_customer import Customer

customer1 = Customer("Иван Петров", 150)

customer1.get_info()
customer1.refill(50)
customer1.get_info()
customer1.refill(50)
customer1.get_info()
customer1.payment(25)
customer1.get_info()

customer1.get_info_account_operations()
import class_pet

pet = {0: class_pet.Cat(name="Baron", gender="male", age=2), 1: class_pet.Cat(name="Sam", gender="male", age=2),
       2: class_pet.Dog(name="Felix", gender="male", age=2), 3: class_pet.Dog(name="Linda", gender="female", age=2),
       4: class_pet.Dog(name="Mouhtar", gender="male", age=0), 5: class_pet.Parrot(name="Gosha", gender="male", age=1)}

for i in range(0, len(pet)):
    print("ID: ", i+1)
    pet[i].get_info()
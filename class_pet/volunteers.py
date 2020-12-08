import class_volunteer

volunteer = {0: class_volunteer.Volunteer("Иван Петров", "Москва", "Наставник"),
             1: class_volunteer.Volunteer("Галя Петренко", "Москва", "Волонтёр"),
             2: class_volunteer.Participant("Иоанн Богослов", "Москва", "Волонтёр"),
             3: class_volunteer.Participant("Зина Пулемёт", "Москва", "Наставник"),
             4: class_volunteer.Participant("Аксиния Радионова", "Санкт-Петербург", "Волонтёр"),
             5: class_volunteer.Participant("Кирилл Дорохов", "Уфа", "Волонтёр")}

for i in range(0, len(volunteer)):
    temp_list = volunteer[i].get_part_info()
    if temp_list[3] == "Corporate Participant":
        print()
        print(temp_list)
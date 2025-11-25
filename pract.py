import datetime

weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

def func(date):


    weekday = date.weekday()
    return weekdays[weekday]

print(func(datetime.date(2025, 11, 26)))
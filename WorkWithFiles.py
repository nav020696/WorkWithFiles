"""
Создать телефонный справочник с возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в текстовом файле
3. Пользователь может ввести одну из характеристик для поиска определенной
записи(Например имя или фамилию человека)
4. Использование функций. Ваша программа не должна быть линейной

ДЗ "Дополнить справочник возможностью копирования данных из одного файла в другой. 
Пользователь вводит номер строки, которую необходимо перенести из одного файла в другой."
*Дополнить валидацию по фамилии и по наличию чисел в имени и фамилии
**шапку для нового файла собираем из ключей из словаря из записи

"""

from os.path import exists
from csv import DictReader, DictWriter

class LenNumberError(Exception):
    def __init__(self, text):
        self.txt = text

class NameError(Exception):
    def __init__(self, text):
        self.txt = text

def get_info():
    is_valid_name = False
    while not is_valid_name:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Некорректное имя")
            else:
                is_valid_name = True
        except NameError as err:
            print(err)
            continue
    
    last_name = input("Введите фамилию: ")

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер телефона: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер")
            continue
        except LenNumberError as err: 
            print(err)
            continue

    return [first_name, last_name, phone_number]

def create_file(file_name):
    #менеджер контекста
    with open(file_name, "w", encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()

def read_file(file_name):
    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)
    
def write_file(file_name, lst):
    res = read_file(file_name)
    for el in res:
        if el['Телефон'] == str(lst[2]):
            print("Такой телефон уже существует")
            return     
    obj = {'Имя' : lst[0], 'Фамилия' : lst[1], 'Телефон' : lst[2]}
    res.append(obj)
    with open(file_name, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)

file_name = 'phone.csv'

def main():
    while True:
        command = input("Введите команду: ")
        if command == 'q':
            print("До свидания :)")
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print("Файл отсутствует. Создайте файл")
                continue 
            print(*read_file(file_name))

main()
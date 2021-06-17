from collections import UserDict
import datetime
import re
import copy

pattern_phone = '\d{3,}'


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __eq__(self, other):
        return self.value == other.value


class Name(Field):

    pass


class Phone(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):

        # проверка данных на корректность.
        # паттерн  pattern_phone указан в начале программы
        # if re.fullmatch(pattern_phone, new_value):
        # нужна более продвинутая проверка!!!!!
        # если количество цифр меньше шести телефон не записывается
        new_value = re.sub(r'[^\d]', '', new_value)
        if len(new_value) > 6:
            self.__value = new_value

        else:
            print('Phone number so short')
            self.__value = None


class Birthday(Field):

    def __init__(self, value):
        self.value = value

    '''
    def __init__(self. value):
        self.__value = 0
        self.value = value
    '''

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        # предполагаю, что new_value  может быть записан с любыми разделителями
        # извлекаю оттуда только числа
        numbers_date = re.findall(r'\d+', str(new_value))

        # если передали None , или там не три числа
        # значит создаем объект с value = None
        if len(numbers_date) != 3:
            self.__value = None

        # преобразую в кортеж чисел
        numbers_date = tuple(map(int, numbers_date))

        try:
            # если из этих чисел получается дата
            date_birthday = datetime.datetime(*numbers_date).date()

            # и эта дата не из будущего
            if date_birthday >= datetime.datetime.today().date():
                print('Date from future')
                self.__value = None
                return

            # присваиваем новое значение даты
            self.__value = date_birthday

        except:
            print('Date is wrong')
            self.__value = None


class Record():

    def __init__(self, name, phone='', birthday=Birthday(None)):
        self.name = name
        self.phones = [phone]
        self.birthday = birthday

    def __str__(self):
        result = ''
        result += f"name - {self.name.value} "
        if self.birthday:
            result += f"birthday - {str(self.birthday.value)} "
        result += f"phones - {', '.join([phone.value for phone in self.phones])}"
        return result

    def add_phone(self, phone):
        self.phones.append(phone)

    def change_phone(self, phone, new_phone):
        #  поиск по объекту Phone  не работает, потому что   ищет вхождение,
        '''
        try:
            idx = self.phones.index(phone)
            self.phones[idx] = new_phone
        except:
            raise Exception("Phone is not found")
        '''
        # а это is . Объект созданный с теми же данными будет новым объектом
        # Поэтому будем искать value объекта  .

        for i, el in enumerate(self.phones):
            if phone.value == el.value:
                self.phones[i] = new_phone
                break
        else:
            raise Exception("Phone is not found")

    def change_birthday(self,  new_birthday):
        if new_birthday.value != None:
            self.birthday = new_birthday
        else:
            raise Exception("New birthday is not correct")


    def days_to_birthday(self):
        if self.birthday:
            now_date = datetime.now()
            birthday_date = datetime.strptime(self.birthday, '%d.%m.%Y')
            delta1 = datetime(now_date.year, birthday_date.month, birthday_date.day)
            delta2 = datetime(now_date.year + 1, birthday_date.month, birthday_date.day)
            days = (max(delta1, delta2) - now_date).days + 1
            if days >= 365:
                return days - 365
            else:
                return days


class AddressBook(UserDict):

    # два следующих метода  - инструкции для сериализации
    # и десериализации  экземпляра класса  AddressBook
    # ----------------------------------
    def __getstate__(self):
        # deepcopy  для перестраховки.
        atr = copy.deepcopy(self.__dict__)
        return atr

    def __setstate__(self, atr):
        self.__dict__ = atr
    # -----------------------------------

    def add_record(self, record):
        '''
        метод для добавления одного элемента
        в словарь экземпляра
        record -  объект   класса Record, содержащий поля - 
        name - объект класса Name
        phones -   список объектов класса Phone
        birthday - объект класса  Birthday
        '''
        self[record.name.value] = record

    def full_search(self, user_or_phone):
        result = ''

        for rec in self.data.values():
            #  сначала ищу среди имен
            if user_or_phone in rec.name.value:
                result += '\n' + str(rec)

            # потом ищу в телефонах
            # для этого удаляю все символы кроме цифр
            dig_user_or_phone = re.sub(r'[\D]', '', user_or_phone)
            #  если там есть хотя бы 4 цифры, будем считать это частью телефона
            if len(dig_user_or_phone) > 3:
                for phone in rec.phones:
                    if dig_user_or_phone in phone.value:
                        result += '\n' + str(rec)

        return result

    def iterable(self, n):
        self.i = 0
        length = len(self)
        users_list = list(self)
        while self.i < length:
            result = []
            next_iter = length if len(users_list[self.i:]) < int(n) else self.i + int(n)
            for j in range(self.i, next_iter):
                user = f'\n{users_list[j]}\n{self[users_list[j]]}\n'
                result.append(user)
                self.i += 1
            yield result
            
    def __str__(self):
        return '\n'.join(list(self.data.items()))
    '''


if __name__ == "__main__":
    pass

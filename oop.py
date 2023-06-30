from collections import UserDict
from datetime import datetime

class Field:

    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
     
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not value.isdigit():
            raise ValueError("Phone must be a number!")
        self._value = value


class Birthday(Field):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Format birthday must be dd.mm.YYYY")


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.optional_fields = []
        self.birthday = birthday

        if phone:
            self.optional_fields.append(phone)

    def add_phone(self, phone: Phone):

        self.optional_fields.append(phone)

    def remove_phone(self, phone: Phone):
        for field in self.optional_fields:
            if not isinstance(field, Phone):
                continue
            if field.value == phone.value:
                self.optional_fields.remove(field)

    def edit_phone(self, phone: Phone, new_phone_number):
        for field in self.optional_fields:
            if not isinstance(field, Phone):
                continue
            if field.value == phone.value:
                field.value = new_phone_number

    def add_birthday(self, birthday: Birthday):
        if not self.birthday:
            self.birthday = birthday
        else:
            print("Birthday already exists")

    def days_to_birthday(self):
        if self.birthday:
            birthday = self.birthday.value
            day_now = datetime.now()
            if day_now > datetime(day_now.year, birthday.month, birthday.day):
                time_to_birthday = datetime(
                    day_now.year + 1, birthday.month, birthday.day) - day_now
            else:
                time_to_birthday = datetime(
                    day_now.year, birthday.month, birthday.day) - day_now
            return f"{time_to_birthday.days} days to {self.name.value} birthday"
        else:
            return "This contact does not have a birthday"

class AdressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, n: int):
        start = 0
        end = n
        keys = list(self.data.keys())
        while start < len(keys):
            chunk_keys = keys[start:end]
            chunk = [self.data[key] for key in chunk_keys]
            yield chunk
            start = end
            end = start + n

    

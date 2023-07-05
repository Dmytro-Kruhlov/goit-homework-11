from collections import UserDict
from datetime import datetime
import pickle
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

    def __eq__(self, other):
        if  not isinstance(other, Phone):
            return False
        return self.value == other.value


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
            
            if field == phone:
                self.optional_fields.remove(field)

    def edit_phone(self, phone: Phone, new_phone_number):
        for field in self.optional_fields:
            
            if field == phone:
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
        
    def __str__(self):
        output = ""
        fields = [field.value for field in self.optional_fields if isinstance(field, Phone)]
        phones = ", ".join(fields) if fields else "N/A"
        birthday = self.birthday.value.date() if self.birthday else "N/A"
        output += f"{self.name.value}: Phones:{phones}, Birthday: {birthday}\n"
        return output
    
    
    
class AdressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def save_data(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)
        return "Data saved successfully."

    def load_data(self, filename):
        try:
            with open(filename, "rb") as file:
                self.data = pickle.load(file)
            return "Data loaded successfully"
        except FileNotFoundError:
            return "File not found."
        except pickle.UnpicklingError:
            return "Error while loading data from the file."
            
            
class AddressBookIterator:

    def __init__(self, address_book: AdressBook, n):
        self.address_book = address_book
        self.n = n
        self.start = 0
        self.keys = list(self.address_book.data.keys())

    def __iter__(self):
        return self
    
    def __next__(self):
        end = self.start + self.n
        if self.start < len(self.keys):
            chunk_keys = self.keys[self.start:end]
            chunk = [self.address_book.data[key] for key in chunk_keys]
            self.start = end
            return chunk
        raise StopIteration     
        

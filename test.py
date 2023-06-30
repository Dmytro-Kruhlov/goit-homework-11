from oop import Record
from oop import Name
from oop import AdressBook
from oop import Phone
from oop import Birthday

adress_book = AdressBook()
name = Name()
name.value = "Dima"
phone = Phone()
phone.value = "1234"
birthday = Birthday()
birthday.value = "10.04.1990"
record = Record(name, phone, birthday)
phone1 = Phone()
phone1.value = "123456"
record.add_phone(phone1)
record.days_to_birthday
print(record.days_to_birthday())
adress_book.add_record(record)

# print(adress_book.data)
# print(record.optional_fields)
# for name, record in adress_book.data.items():
#     print(f"{name}: {[r.value for r in record.optional_fields]}, {record.birthday.value.date()}")

from oop import AdressBook, Record, Name, Phone, Birthday, AddressBookIterator


adress_book = AdressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Invalid command. Please try again."
        except ValueError:
            return "Error: Invalid input format. Please try again."
        except IndexError:
            return "Error: Contact not found. Please try again."
    return wrapper


def load(args):
    filename = args
    return adress_book.load_data(filename)


def save(args):
    filename = args
    return adress_book.save_data(filename)


def spliting(args):
    return args.split()


def hello(args):
    return "How can I help you?"


def add_record(args):

    args = spliting(args)

    if len(args) < 1 or len(args) > 3:
        raise ValueError
    name = args[0]
    phone = args[1] if len(args) > 1 else ""
    birthday = args[2] if len(args) > 2 else ""
    
    if name in adress_book.data:
        return "You already have a contact with this name"
    else:

        r_name = Name()
        r_name.value = name
        record = Record(r_name)
        if phone:
            r_phone = Phone()
            r_phone.value = phone
            record.add_phone(r_phone)
        if birthday:
            r_birthday = Birthday()
            r_birthday.value = birthday
            record.add_birthday(r_birthday)
        adress_book.add_record(record)
        
        return f"Contact {name} has been added."
    

def add_birthday(args):

    args = spliting(args)

    if len(args) < 2:
        raise ValueError
    
    name, birthday = args
    record = adress_book[name]
    a_birthday = Birthday()
    a_birthday.value = birthday
    record.add_birthday(a_birthday)

    return f"Birthday to contact {name} has been added"


def show_day_to_birthday(args):

    name = args

    if name in adress_book.data and adress_book.data[name].birthday:
        day_birthday = adress_book.data[name].days_to_birthday()
        return day_birthday
    else:
        return f"This contact doesn't have birthday"

    
def add_phone(args):

    args = spliting(args)

    if len(args) != 2:
        raise ValueError
    name, phone = args
    record = adress_book[name]
    if name in adress_book.data:
        a_phone = Phone()
        a_phone.value = phone
        record.add_phone(a_phone)

    return f"A number {phone} has been added to a contact {name}"


def change(args):

    args = spliting(args)

    if len(args) != 3:
        raise ValueError
    name, old_phone, new_phone = args
    if name not in adress_book.data:
        return f"You dont have contact with name {name}"
    record = adress_book[name]
    phone = Phone()
    phone.value = old_phone
    record.edit_phone(phone, new_phone)
        
    return f"The phone number {old_phone} for contact {name} has been changed to {new_phone}."


def get_phone_number(args):

    args = spliting(args)

    if len(args) != 1:
        raise ValueError
    name = args[0]
    if name in adress_book.data:
        record = adress_book[name]
        phones = []
        for field in record.optional_fields:
            phones.append(field.value)
        return f"The phone numbers for contact {name} is {', '.join(phones)}."
    else:
        raise IndexError


def show_all_contacts(args):

    if len(args) > 1:
        raise ValueError
    if not args:
        output = ""
        for record in adress_book.data.values():
            output += str(record)
        return output
    else:
        n = int(args[0])
        page = 1
        page_iterator = AddressBookIterator(adress_book, n)
        output = ""
        for pages in page_iterator:
            output += f"Page {page} Contacts:\n"
            for record in pages:
                output += str(record)
            page += 1

        return output


def search_contacts(args):
    results = []
    search_term = args

    for record in adress_book.data.values():
        name = record.name.value
        phones = [phone.value for phone in record.optional_fields if isinstance(phone, Phone)]
        if search_term in name or any(search_term in phone for phone in phones):
            results.append(record)

    if not results:
        return "No matching contacts found."

    output = ""
    for record in results:
        output += str(record)

    return output


COMMANDS = {
    add_record: ["add record"],
    hello: ["hello"],
    change: ["change"],
    get_phone_number: ["phone"],
    show_all_contacts: ["show all"],
    add_phone: ["add phone"],
    add_birthday: ["add birthday"],
    show_day_to_birthday: ["show birthday"],
    load: ["load"],
    save: ["save"],
    search_contacts: ["search"]
}


@input_error
def get_func(user_input):
    succesfull_run = False
    user_input_lower = user_input.lower()
    for func, key_words in COMMANDS.items():
        for key in key_words:
            if user_input_lower.startswith(key):
                args = user_input[len(key):].strip()
                result = func(args)
                succesfull_run = True
                break
    if not succesfull_run:
        raise KeyError
    return result


def main_loop():

    while True:

        user_input = input(">>> ")

        if user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        result = get_func(user_input)
        print(result)


if __name__ == "__main__":
    main_loop()

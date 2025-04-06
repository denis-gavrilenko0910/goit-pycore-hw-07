from collections import UserDict
from datetime import datetime, timedelta


class Field:
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)
  

class Name(Field):
  pass


class Phone(Field):
  def __init__(self, value: str):
    if value.isdigit() and len(value) == 10:
      super().__init__(value)
    else:
      raise ValueError('Incorrect phone number')
    

class Birthday(Field):
    def __init__(self, value):
      try:
        brth_date = datetime.strptime(value, '%d.%m.%Y')
        super().__init__(brth_date)
      except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
  def __init__(self, name):
    self.name = Name(name)
    self.phones = []
    self.birthday = None
  
  def add_birthday(self, birthday):
    self.birthday = Birthday(birthday)

  def add_phone(self, phone):
    self.phones.append(Phone(phone))
  
  def find_phone(self, phone):
    for phone_obj in self.phones:
      if phone_obj.value == phone:
        return phone_obj
      
  def remove_phone(self, phone):
    rem_phone = self.find_phone(phone)
    if rem_phone:
      self.phones.remove(rem_phone)

  def edit_phone(self, old_phone, new_phone):
    phone_obj = self.find_phone(old_phone)
    if phone_obj:
      phone_obj.value = new_phone

  def __str__(self):
    birthday = self.birthday.value.strftime('%d.%m.%Y') if self.birthday else '-'
    return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones),}, birthday: {birthday}"


class AddressBook(UserDict):
  def add_record(self, record: Record):
    self.data[record.name.value] = record

  def find(self, name) -> Record:
    if name in self.data:
      return self.data[name]
    
  def get_upcoming_birthdays(self):
    result = []
    date_now = datetime.today().date()
    for name, record in self.data.items():
      if record.birthday:    
        user_brthday = record.birthday.value.date()
        user_brthday = user_brthday.replace(year=date_now.year)
        if user_brthday < date_now:
          user_brthday = user_brthday.replace(year=date_now.year + 1)

        if user_brthday >= date_now and user_brthday < date_now + timedelta(days=7):
          user_brthday = user_brthday.strftime('%d.%m.%Y')
          result.append({'name': name, 'congratulation_date':  user_brthday})
      
    return result  
  
  def delete(self, name):
    del_contact = self.find(name)
    if del_contact:
      self.data.pop(name, None)


if __name__ == '__main__':
  book = AddressBook()
  
  john_record = Record("John")
  john_record.add_phone("1234567890")
  john_record.add_phone("5555555555")
  john_record.add_birthday("07.04.1985")
  # john_record.add_phone("3333")
  
  book.add_record(john_record)
  
  jane_record = Record("Jane")  
  jane_record.add_phone("9876543210")
  # jane_record.add_birthday("34.13.")

  book.add_record(jane_record)

  for name, record in book.data.items():
    print(record)
  
  john = book.find("John")
  john.edit_phone("1234567890", "11122233")
  # john.remove_phone('3333')
  print(john)

  found_phone = john.find_phone("5555555555")
  print(f"{john.name}: {found_phone}")  
  
  # book.delete("Jane")
  # for name, record in book.data.items():
  #   print(record)

  print(book.get_upcoming_birthdays())
        
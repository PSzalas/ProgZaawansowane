from datetime import date


class Library:
    def __init__(self, city, street, zip_code, open_hours, phone):
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.open_hours = open_hours
        self.phone = phone

    def __str__(self):
        return (f"Adres biblioteki: {self.city}, {self.street}, {self.zip_code}\n"
                f"Godziny otwarcia: {self.open_hours}\nNumer kontaktowy: {self.phone}")


class Employee:
    def __init__(self, first_name, last_name, hire_date, birth_date, city, street, zip_code, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.birth_date = birth_date
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.phone = phone

    def __str__(self):
        return (f"Pracownik: {self.first_name} {self.last_name}\n"
                f"Data zatrudnienia: {self.hire_date}\nData urodzenia: {self.birth_date}\n"
                f"Adres zamieszkania: {self.city}, {self.street}, {self.zip_code}\nNumer kontaktowy: {self.phone}")


class Book:
    def __init__(self, library, publication_date, author_name, author_surname, number_of_pages):
        self.library = library
        self.publication_date = publication_date
        self.author_name = author_name
        self.author_surname = author_surname
        self.number_of_pages = number_of_pages

    def __str__(self):
        return (f"Autor {self.author_name} {self.author_surname}, Data publikacji: {self.publication_date}\n"
                f"Liczba stron: {self.number_of_pages}\nBiblioteka: {self.library}")


class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def is_passed(self):
        average = sum(self.marks) / len(self.marks)
        return average > 50

    def __str__(self):
        return f"Student: {self.name}, Oceny: {self.marks}"


class Order:
    def __init__(self, employee, student, books, order_date):
        self.employee = employee
        self.student = student
        self.books = books
        self.order_date = order_date

    def __str__(self):
        book_list = "\n".join([str(book) for book in self.books])
        return (f"Data zamówienia: {self.order_date}\n"
                f"Pracownik: {self.employee}\n"
                f"Student: {self.student}\n"
                f"Książki:\n{book_list}")


# Tworzenie obiektów
library1 = Library("Warszawa", "Śródmieście 3", "00-001", "9-17", "123-456-789")
library2 = Library("Kraków", "Stare miasto 5", "30-002", "10-18", "987-654-321")

employee1 = Employee("Patryk", "Nowak", date(2021, 1, 15), date(1990, 5, 20), "Warszawa", "Poniatowskiego 5", "00-003",
                     "111-222-333")
employee2 = Employee("Anna", "Kowalska", date(2020, 6, 30), date(1985, 8, 15), "Kraków", "Piłsudskiego 2", "30-004",
                     "444-555-666")
employee3 = Employee("Piotr", "Wiśniewski", date(2022, 9, 10), date(1995, 12, 10), "Warszawa", "Mickiewicza 10", "00-005",
                     "777-888-999")

book1 = Book(library1, date(2010, 6, 15), "Adam", "Mickiewicz", 300)
book2 = Book(library2, date(2005, 3, 22), "Henryk", "Sienkiewicz", 250)
book3 = Book(library1, date(2018, 11, 10), "Bolesław", "Prus", 400)
book4 = Book(library2, date(1999, 4, 5), "Eliza", "Orzeszkowa", 220)
book5 = Book(library1, date(2022, 7, 18), "Juliusz", "Słowacki", 150)

student1 = Student("Zofia", [55, 65, 75])
student2 = Student("Marcin", [45, 55, 60])
student3 = Student("Agnieszka", [30, 40, 45])

order1 = Order(employee1, student1, [book1, book3], date(2023, 10, 1))
order2 = Order(employee2, student2, [book2, book4, book5], date(2023, 11, 5))

print(order1)
print()
print(order2)
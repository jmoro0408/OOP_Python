class Employee:
    def __init__(self, first, last, pay) -> None:
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + "." + last + "@company.com"

    def fullname(self):
        return self.first, self.last


emp_1 = Employee("James", "Moro", 50000)
emp_2 = Employee("test", "name", 60000)


print(emp_2.fullname())

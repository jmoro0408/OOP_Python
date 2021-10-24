class Employee:

    raise_amount = 1.04
    num_of_employees = 0

    def __init__(self, first, last, pay) -> None:
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + "." + last + "@company.com"

        Employee.num_of_employees += 1  # increase the number of employees by one each time an employee is created

    def fullname(self):
        return self.first, self.last

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)  # 4% raise

    @classmethod
    def set_raise_amount(cls, amount):
        cls.raise_amount = amount

    @classmethod
    def from_string(cls, emp_str):  # alternative constructors start from_
        first, last, pay = emp_str.split("-")
        return cls(
            first, last, pay
        )  # creates a new employee object from string. This is an alternative constructor

    @staticmethod  # static methods are logically linked to the class but doesnt access the class or instance
    def is_workday(day):
        if day.weekday() > 4:  # Mon = 0, Sat/Sun = 5/6.
            return False
        return True


class Developer(Employee):  # Inherit from employee class
    raise_amount = 1.10

    def __init__(self, first, last, pay, prog_lang):
        super().__init__(
            first, last, pay
        )  # This lets the Employee class handle the first 3 arguments
        self.prog_lang = prog_lang


class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        for emp in self.employees:
            print(emp.fullname())


dev_1 = Developer("James", "Moro", 50000, "Python")
dev_2 = Developer("test", "name", 60000, "Java")
mgr_1 = Manager("Sue", "Smith", 90000, employees=[dev_1])

print(mgr_1.email)
mgr_1.add_emp(dev_2)
mgr_1.print_emps()

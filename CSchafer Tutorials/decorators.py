class Employee:

    raise_amount = 1.04
    num_of_employees = 0

    def __init__(self, first, last, pay) -> None:
        self.first = first
        self.last = last
        self.pay = pay
        # self.email = first + "." + last + "@company.com"

        Employee.num_of_employees += 1  # increase the number of employees by one each time an employee is created

    def __repr__(self):  # used for debugging, should recreate the object
        return f"Employee({self.first}, {self.last}, {self.pay})"

    def __str__(self):  # for end user
        return f"{self.fullname()}, {self.email}"

    @property
    def fullname(self):
        return self.first, self.last

    @fullname.setter
    def fullname(self, name):
        first, last = name.split(" ")
        self.first = first
        self.last = last

    @fullname.deleter
    def fullname(self):
        print("delete name")
        self.first = None
        self.last = None

    @property
    def email(self):
        return f"{self.first}.{self.last}@email.com"

    def __add__(self, other):  # return the total pay when adding two employees together
        return self.pay + other.pay

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


emp_1 = Employee("James", "Moro", 50000)
dev_1 = Developer("James", "Moro", 50000, "Python")
dev_2 = Developer("test", "name", 60000, "Java")
mgr_1 = Manager("Sue", "Smith", 90000, employees=[dev_1])

emp_1.fullname = "Jane Doe"
print(emp_1.email)

del emp_1.fullname

print(emp_1.email)

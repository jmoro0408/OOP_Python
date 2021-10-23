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


dev_1 = Employee("James", "Moro", 50000)
dev_2 = Employee("test", "name", 60000)


print(dev_1.email)
print(dev_2.email)

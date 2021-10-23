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


emp_1 = Employee("James", "Moro", 50000)
emp_2 = Employee("test", "name", 60000)

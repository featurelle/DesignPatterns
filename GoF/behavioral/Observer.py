from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self, observable, *args):
        pass


class Observable:

    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def delete_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, *args):
        for observer in self._observers:
            observer.update(self, *args)


class Employee(Observable):

    def __init__(self, name, salary):
        super().__init__()
        self._name = name
        self._salary = salary

    @property
    def name(self):
        return self._name

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, new_salary):
        self._salary = new_salary
        self.notify_observers(new_salary)


class Payroll(Observer):

    def update(self, employee, salary):
        print(f'Payroll: Cut a new check for {employee.name}!\n'
              f'Her/his/its new salary is {salary}!\n')


class TaxMan(Observer):

    def update(self, employee, salary):
        print(f'TaxMan: Send {employee.name} a new tax bill!\n')

# hello
def promote_employee():
    e = Employee('John Doe', 12000)
    p = Payroll()
    t = TaxMan()

    e.add_observer(p)
    e.add_observer(t)

    print('JD has just gotten promoted!\n')
    e.salary = 15000

    e.delete_observer(t)

    print('Wow! He\'s really nailing it!\n')
    e.salary = 18000


if __name__ == "__main__":
    promote_employee()

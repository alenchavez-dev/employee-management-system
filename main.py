# ============================================================
# Program: Employee Management System
# Author: Alen Chavez
# Description:
#   Console app that models Employees and Managers (inheritance +
#   composition). Prompts for input, supports managers with
#   subordinates, and formats zero-padded employee IDs. Output is
#   printed fully left-aligned for clarity.
# ============================================================

class Employee:
    def __init__(self, name, eid):
        # Initialize the Employee with a name and eid
        self.__name = name
        self.__eid = eid

    @property
    def name(self):
        # Return the capitalized name
        return self.__name.capitalize()

    @name.setter
    def name(self, name):
        # Set the name if it is alphabetic, otherwise set to 'Unknown'
        if name.isalpha():
            self.__name = name
        else:
            self.__name = 'Unknown'

    @property
    def eid(self):
        # Return the eid zero-filled up to 4 spaces
        return str(self.__eid).zfill(4)

    @eid.setter
    def eid(self, eid):
        # Set the eid if it is provided, otherwise set to '9999'
        if eid:
            self.__eid = eid
        else:
            self.__eid = '9999'

    def __str__(self):
        # Return the formatted string for the Employee
        return f'{self.eid}: {self.name}'


class Manager(Employee):
    def __init__(self, name, eid):
        # Initialize the Manager with a name and eid, and an empty subordinates list
        super().__init__(name, eid)
        self.subordinates = []

    def add_subordinate(self, name, eid):
        # Create a new Employee and add to the subordinates list
        subordinate = Employee(name, eid)
        self.subordinates.append(subordinate)

    def print_subordinates(self):
        # Print subordinates fully left-aligned (no indentation)
        print(f"{self.name}'s Employees")
        for subordinate in self.subordinates:
            print(f"{subordinate}")


def add_employee():
    # Prompt the user to enter employee details and create an Employee or Manager
    name = input("Enter name: ")
    eid = input("Enter id: ")
    is_manager = input("Is the employee a manager? (Y/N) ").strip().lower()

    if is_manager == 'y':
        # If the employee is a manager, create a Manager and add subordinates
        manager = Manager(name, eid)
        num_subordinates = int(input("How many subordinates? "))
        for _ in range(num_subordinates):
            sub_name = input("Enter subordinate name: ").strip()
            sub_id = input("Enter subordinate id: ").strip()
            if not sub_name:
                sub_name = "Unknown"
            if not sub_id:
                sub_id = "9999"
            manager.add_subordinate(sub_name, sub_id)
        return manager
    else:
        # If the employee is not a manager, create a regular Employee
        return Employee(name, eid)


def main():
    # Print the title and introductory messages
    print("Employee Management System\n")
    print("Adding Employees...\n")

    employees = []

    while True:
        # Add an employee to the list
        employees.append(add_employee())
        more = input("Do you want to enter more? (Y/N) ").strip().lower()
        if more != 'y':
            break
        print()  # Skip a line

    # Print the list of employees and their subordinates if any (all left-aligned)
    print("\nPrinting Employee List")
    for emp in employees:
        print(f"{emp}")
        if isinstance(emp, Manager):
            emp.print_subordinates()


if __name__ == "__main__":
    # Run the main function
    main()

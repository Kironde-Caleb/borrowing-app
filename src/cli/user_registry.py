from src.models.administrator import Administrator
from src.models.student import Student


class UserRegistry:
    """In-memory list of the people who can log in to the command-line app."""

    def __init__(self):
        self.__users = {}

    def register_student(self, student_id, full_name, email, hostel):
        student = Student(
            self.__normalise(student_id),
            full_name.strip(),
            email.strip(),
            hostel.strip(),
        )
        self.__add(student)
        return student

    def register_administrator(self, admin_id, full_name, email, role):
        admin = Administrator(
            self.__normalise(admin_id),
            full_name.strip(),
            email.strip(),
            role.strip(),
        )
        self.__add(admin)
        return admin

    def find(self, person_id):
        user = self.__users.get(self.__normalise(person_id))
        if user is None:
            raise ValueError("No user found with that ID.")
        return user

    def all_users(self):
        return list(self.__users.values())

    def __add(self, person):
        if person.person_id in self.__users:
            raise ValueError("A user with this ID already exists.")
        self.__users[person.person_id] = person

    @staticmethod
    def __normalise(value):
        return str(value).strip().upper()

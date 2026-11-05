from src.models.person import Person


class Student(Person):
    def __init__(self, student_id, full_name, email, hostel):
        super().__init__(student_id, full_name, email)
        self.__hostel = hostel

    @property
    def student_id(self):
        return self.person_id

    @property
    def hostel(self):
        return self.__hostel

    def display_details(self):
        return (
            f"Student ID: {self.student_id}\n"
            f"Name: {self.full_name}\n"
            f"Email: {self.email}\n"
            f"Hostel: {self.hostel}"
        )
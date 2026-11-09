from src.models.person import Person


class Student(Person):
    def __init__(self, student_id, full_name, email, hostel):
        if not student_id or not student_id.strip():
            raise ValueError("Student ID cannot be empty.")

        if not full_name or not full_name.strip():
            raise ValueError("Full name cannot be empty.")

        if not email or "@" not in email:
            raise ValueError("A valid email address is required.")

        if not hostel or not hostel.strip():
            raise ValueError("Hostel cannot be empty.")

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
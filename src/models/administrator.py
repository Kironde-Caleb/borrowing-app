from src.models.person import Person


class Administrator(Person):
    def __init__(self, admin_id, full_name, email, role):
        super().__init__(admin_id, full_name, email)
        self.__role = role

    @property
    def role(self):
        return self.__role

    def display_details(self):
        return (
            f"Administrator ID: {self.person_id}\n"
            f"Name: {self.full_name}\n"
            f"Email: {self.email}\n"
            f"Role: {self.role}"
        )
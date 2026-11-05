from src.models.person import Person


class Administrator(Person):
    def __init__(self, admin_id, full_name, email, role):
        if not admin_id or not admin_id.strip():
            raise ValueError("Administrator ID cannot be empty.")

        if not full_name or not full_name.strip():
            raise ValueError("Full name cannot be empty.")

        if not email or "@" not in email:
            raise ValueError("A valid email address is required.")

        if not role or not role.strip():
            raise ValueError("Administrator role cannot be empty.")

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
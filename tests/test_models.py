import unittest
from datetime import datetime, timedelta

from src.models.person import Person
from src.models.student import Student
from src.models.administrator import Administrator
from src.models.item import Item
from src.models.item_category import ItemCategory
from src.models.item_status import ItemStatus
from src.models.borrow_request import BorrowRequest
from src.models.borrow_record import BorrowRecord
from src.models.request_status import RequestStatus


class TestBorrowingModels(unittest.TestCase):

    def setUp(self):
        self.student = Student(
            "ST001", "John Doe", "john@example.com", "Hostel A"
        )

        self.item = Item(
            "IT001",
            "Laptop",
            "HP laptop",
            ItemCategory.ELECTRONICS,
            self.student
        )

    def test_student_inherits_person(self):
        self.assertIsInstance(self.student, Person)

    def test_administrator_inherits_person(self):
        admin = Administrator(
            "AD001", "Admin User", "admin@example.com", "Manager"
        )
        self.assertIsInstance(admin, Person)

    def test_item_starts_available(self):
        self.assertEqual(self.item.status, ItemStatus.AVAILABLE)

    def test_borrow_request_starts_pending(self):
        request = BorrowRequest("BR001", self.item, self.student)
        self.assertEqual(request.status, RequestStatus.PENDING)

    def test_borrow_record_return(self):
        request = BorrowRequest("BR002", self.item, self.student)
        record = BorrowRecord(
            "REC001", request, datetime.now() + timedelta(days=7)
        )
        record.mark_as_returned()
        self.assertIsNotNone(record.return_date)
    def test_person_is_abstract(self):
        with self.assertRaises(TypeError):
            Person("P001", "Test Person", "test@example.com")
    

if __name__ == "__main__":
    unittest.main()
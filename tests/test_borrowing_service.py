import unittest

from src.models.student import Student
from src.models.item import Item
from src.models.item_category import ItemCategory
from src.models.item_status import ItemStatus
from src.models.request_status import RequestStatus
from src.services.borrowing_service import BorrowingService


class TestBorrowingService(unittest.TestCase):

    def setUp(self):
        self.service = BorrowingService()

        self.owner = Student(
            "ST001", "John Doe", "john@example.com", "Hostel A"
        )
        self.borrower = Student(
            "ST002", "Mary Jane", "mary@example.com", "Hostel B"
        )

        self.item = Item(
            "IT001",
            "Laptop",
            "HP laptop",
            ItemCategory.ELECTRONICS,
            self.owner
        )

    # submit_request tests

    def test_submit_request_creates_pending_request(self):
        request = self.service.submit_request(self.item, self.borrower)
        self.assertEqual(request.status, RequestStatus.PENDING)
        self.assertEqual(request.request_id, "REQ001")

    def test_submit_request_keeps_item_available(self):
        self.service.submit_request(self.item, self.borrower)
        self.assertEqual(self.item.status, ItemStatus.AVAILABLE)

    def test_submit_request_rejects_unavailable_item(self):
        self.item.update_status(ItemStatus.BORROWED)

        with self.assertRaises(ValueError):
            self.service.submit_request(self.item, self.borrower)

    def test_submit_request_rejects_own_item(self):
        with self.assertRaises(ValueError):
            self.service.submit_request(self.item, self.owner)

    def test_submit_request_rejects_duplicate_pending_request(self):
        self.service.submit_request(self.item, self.borrower)

        with self.assertRaises(ValueError):
            self.service.submit_request(self.item, self.borrower)

    def test_submit_request_rejects_invalid_item(self):
        with self.assertRaises(ValueError):
            self.service.submit_request("Laptop", self.borrower)

    def test_submit_request_rejects_invalid_borrower(self):
        with self.assertRaises(ValueError):
            self.service.submit_request(self.item, "Mary")


if __name__ == "__main__":
    unittest.main()


    
import unittest
from datetime import datetime, timedelta

from src.models.administrator import Administrator
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
        self.stranger = Student(
            "ST003", "Peter Okello", "peter@example.com", "Hostel C"
        )
        self.admin = Administrator(
            "AD001", "Admin User", "admin@example.com", "Manager"
        )

        self.item = Item(
            "IT001",
            "Laptop",
            "HP laptop",
            ItemCategory.ELECTRONICS,
            self.owner
        )

        self.due_date = datetime.now() + timedelta(days=7)

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

    # approve_request tests

    def test_owner_can_approve_request(self):
        request = self.service.submit_request(self.item, self.borrower)
        record = self.service.approve_request(
            request.request_id, self.owner, self.due_date
        )

        self.assertEqual(request.status, RequestStatus.APPROVED)
        self.assertEqual(self.item.status, ItemStatus.BORROWED)
        self.assertEqual(record.record_id, "REC001")
        self.assertEqual(record.due_date, self.due_date)

    def test_administrator_can_approve_request(self):
        request = self.service.submit_request(self.item, self.borrower)
        self.service.approve_request(
            request.request_id, self.admin, self.due_date
        )

        self.assertEqual(request.status, RequestStatus.APPROVED)

    def test_stranger_cannot_approve_request(self):
        request = self.service.submit_request(self.item, self.borrower)

        with self.assertRaises(ValueError):
            self.service.approve_request(
                request.request_id, self.stranger, self.due_date
            )

        self.assertEqual(request.status, RequestStatus.PENDING)
        self.assertEqual(self.item.status, ItemStatus.AVAILABLE)

    def test_approve_rejects_unknown_request_id(self):
        with self.assertRaises(ValueError):
            self.service.approve_request("REQ999", self.owner, self.due_date)

    def test_approve_rejects_past_due_date(self):
        request = self.service.submit_request(self.item, self.borrower)
        past_date = datetime.now() - timedelta(days=1)

        with self.assertRaises(ValueError):
            self.service.approve_request(
                request.request_id, self.owner, past_date
            )

    def test_approve_rejects_invalid_due_date(self):
        request = self.service.submit_request(self.item, self.borrower)

        with self.assertRaises(ValueError):
            self.service.approve_request(
                request.request_id, self.owner, "Next week"
            )

    def test_approve_same_request_twice_is_refused(self):
        request = self.service.submit_request(self.item, self.borrower)
        self.service.approve_request(
            request.request_id, self.owner, self.due_date
        )

        with self.assertRaises(ValueError):
            self.service.approve_request(
                request.request_id, self.owner, self.due_date
            )

    # reject_request tests

    def test_owner_can_reject_request(self):
        request = self.service.submit_request(self.item, self.borrower)
        self.service.reject_request(request.request_id, self.owner)

        self.assertEqual(request.status, RequestStatus.REJECTED)
        self.assertEqual(self.item.status, ItemStatus.AVAILABLE)

    def test_stranger_cannot_reject_request(self):
        request = self.service.submit_request(self.item, self.borrower)

        with self.assertRaises(ValueError):
            self.service.reject_request(request.request_id, self.stranger)

        self.assertEqual(request.status, RequestStatus.PENDING)

    # return_item tests

    def test_return_item_updates_record_request_and_item(self):
        request = self.service.submit_request(self.item, self.borrower)
        record = self.service.approve_request(
            request.request_id, self.owner, self.due_date
        )

        self.service.return_item(record.record_id)

        self.assertIsNotNone(record.return_date)
        self.assertEqual(request.status, RequestStatus.RETURNED)
        self.assertEqual(self.item.status, ItemStatus.AVAILABLE)

    def test_return_item_rejects_unknown_record_id(self):
        with self.assertRaises(ValueError):
            self.service.return_item("REC999")

    def test_return_item_twice_is_refused(self):
        request = self.service.submit_request(self.item, self.borrower)
        record = self.service.approve_request(
            request.request_id, self.owner, self.due_date
        )
        self.service.return_item(record.record_id)

        with self.assertRaises(ValueError):
            self.service.return_item(record.record_id)

    def test_returned_item_can_be_requested_again(self):
        request = self.service.submit_request(self.item, self.borrower)
        record = self.service.approve_request(
            request.request_id, self.owner, self.due_date
        )
        self.service.return_item(record.record_id)

        new_request = self.service.submit_request(self.item, self.borrower)
        self.assertEqual(new_request.request_id, "REQ002")
        self.assertEqual(new_request.status, RequestStatus.PENDING)


if __name__ == "__main__":
    unittest.main()
import unittest
from datetime import datetime, timedelta

from src.models.student import Student
from src.models.item import Item
from src.models.item_category import ItemCategory
from src.models.request_status import RequestStatus
from src.services.borrowing_service import BorrowingService


class TestBorrowingViews(unittest.TestCase):

    def setUp(self):
        self.service = BorrowingService()

        self.owner = Student(
            "ST001", "John Doe", "john@example.com", "Hostel A"
        )
        self.borrower = Student(
            "ST002", "Mary Jane", "mary@example.com", "Hostel B"
        )

        self.laptop = Item(
            "IT001",
            "Laptop",
            "HP laptop",
            ItemCategory.ELECTRONICS,
            self.owner
        )
        self.book = Item(
            "IT002",
            "Textbook",
            "Networking textbook",
            ItemCategory.BOOKS,
            self.owner
        )

        self.due_date = datetime.now() + timedelta(days=7)

    def test_pending_requests_lists_only_pending(self):
        first = self.service.submit_request(self.laptop, self.borrower)
        second = self.service.submit_request(self.book, self.borrower)
        self.service.approve_request(
            first.request_id, self.owner, self.due_date
        )

        pending = self.service.get_pending_requests()

        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].request_id, second.request_id)
        self.assertEqual(pending[0].status, RequestStatus.PENDING)

    def test_all_requests_lists_every_request(self):
        self.service.submit_request(self.laptop, self.borrower)
        self.service.submit_request(self.book, self.borrower)

        self.assertEqual(len(self.service.get_all_requests()), 2)

    def test_all_records_lists_every_record(self):
        request = self.service.submit_request(self.laptop, self.borrower)
        self.service.approve_request(
            request.request_id, self.owner, self.due_date
        )

        self.assertEqual(len(self.service.get_all_records()), 1)

    def test_active_records_excludes_returned_items(self):
        first = self.service.submit_request(self.laptop, self.borrower)
        second = self.service.submit_request(self.book, self.borrower)
        record_one = self.service.approve_request(
            first.request_id, self.owner, self.due_date
        )
        record_two = self.service.approve_request(
            second.request_id, self.owner, self.due_date
        )

        self.service.return_item(record_one.record_id)
        active = self.service.get_active_records()

        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].record_id, record_two.record_id)
        self.assertEqual(len(self.service.get_all_records()), 2)

    def test_returned_list_is_a_copy(self):
        self.service.submit_request(self.laptop, self.borrower)

        requests = self.service.get_all_requests()
        requests.clear()

        self.assertEqual(len(self.service.get_all_requests()), 1)


if __name__ == "__main__":
    unittest.main()
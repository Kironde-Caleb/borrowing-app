from datetime import datetime

from src.models.borrow_request import BorrowRequest


class BorrowRecord:
    def __init__(self, record_id, borrow_request, due_date):

        if not isinstance(record_id, str) or not record_id.strip():
            raise ValueError("Record ID cannot be empty.")

        if not isinstance(borrow_request, BorrowRequest):
            raise ValueError("A valid borrow request is required.")

        if not isinstance(due_date, datetime):
            raise ValueError("Due date must be a valid date and time.")

        self.__record_id = record_id
        self.__borrow_request = borrow_request
        self.__borrow_date = datetime.now()
        self.__due_date = due_date
        self.__return_date = None

    @property
    def record_id(self):
        return self.__record_id

    @property
    def borrow_request(self):
        return self.__borrow_request

    @property
    def borrow_date(self):
        return self.__borrow_date

    @property
    def due_date(self):
        return self.__due_date

    @property
    def return_date(self):
        return self.__return_date

    def mark_as_returned(self):
        if self.__return_date is None:
            self.__return_date = datetime.now()
        else:
            raise ValueError("This item has already been returned.")

    def display_record(self):
        return (
            f"Record ID: {self.__record_id}\n"
            f"Item: {self.__borrow_request.item.name}\n"
            f"Borrower: {self.__borrow_request.borrower.full_name}\n"
            f"Borrow Date: {self.__borrow_date}\n"
            f"Due Date: {self.__due_date}\n"
            f"Return Date: {self.__return_date or 'Not yet returned'}"
        )
from datetime import datetime
from src.models.request_status import RequestStatus


class BorrowRequest:
    def __init__(self, request_id, item, borrower):
        self.__request_id = request_id
        self.__item = item
        self.__borrower = borrower
        self.__status = RequestStatus.PENDING
        self.__request_date = datetime.now()

    @property
    def request_id(self):
        return self.__request_id

    @property
    def item(self):
        return self.__item

    @property
    def borrower(self):
        return self.__borrower

    @property
    def status(self):
        return self.__status

    @property
    def request_date(self):
        return self.__request_date

    def update_status(self, new_status):
        if isinstance(new_status, RequestStatus):
            self.__status = new_status
        else:
            raise ValueError("Invalid request status.")

    def display_request(self):
        return (
            f"Request ID: {self.__request_id}\n"
            f"Item: {self.__item.name}\n"
            f"Borrower: {self.__borrower.full_name}\n"
            f"Status: {self.__status.value}\n"
            f"Request Date: {self.__request_date}"
        )
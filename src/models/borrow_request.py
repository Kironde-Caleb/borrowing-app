
from datetime import datetime

from src.models.request_status import RequestStatus
from src.models.item import Item
from src.models.person import Person


class BorrowRequest:
    def __init__(self, request_id, item, borrower):

        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("Request ID cannot be empty.")

        if not isinstance(item, Item):
            raise ValueError("Item must be a valid item.")

        if not isinstance(borrower, Person):
            raise ValueError("Borrower must be a valid person.")

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
        allowed_transitions = {
            RequestStatus.PENDING: [
                RequestStatus.APPROVED,
                RequestStatus.REJECTED,
                RequestStatus.CANCELLED
            ],
            RequestStatus.APPROVED: [
                RequestStatus.RETURNED
            ],
            RequestStatus.REJECTED: [],
            RequestStatus.CANCELLED: [],
            RequestStatus.RETURNED: []
        }

        if not isinstance(new_status, RequestStatus):
            raise ValueError("Invalid request status.")

        if new_status not in allowed_transitions[self.__status]:
            raise ValueError(
                f"Cannot change status from "
                f"{self.__status.value} to {new_status.value}."
            )

        self.__status = new_status

    def display_request(self):
        return (
            f"Request ID: {self.__request_id}\n"
            f"Item: {self.__item.name}\n"
            f"Borrower: {self.__borrower.full_name}\n"
            f"Status: {self.__status.value}\n"
            f"Request Date: {self.__request_date}"
        )

from datetime import datetime
from src.models.administrator import Administrator
from src.models.borrow_record import BorrowRecord
from src.models.borrow_request import BorrowRequest
from src.models.item import Item
from src.models.item_status import ItemStatus
from src.models.person import Person
from src.models.request_status import RequestStatus


class BorrowingService:
    def __init__(self):
        self.__requests = []
        self.__records = []
        self.__request_counter = 0
        self.__record_counter = 0

    def submit_request(self, item, borrower):
        if not isinstance(item, Item):
            raise ValueError("A valid item is required.")

        if not isinstance(borrower, Person):
            raise ValueError("A valid borrower is required.")

        if item.status != ItemStatus.AVAILABLE:
            raise ValueError("This item is not available for borrowing.")

        if item.owner.person_id == borrower.person_id:
            raise ValueError("You cannot borrow your own item.")

        for request in self.__requests:
            if (
                request.item.item_id == item.item_id
                and request.borrower.person_id == borrower.person_id
                and request.status == RequestStatus.PENDING
            ):
                raise ValueError(
                    "You already have a pending request for this item."
                )

        self.__request_counter += 1
        request_id = f"REQ{self.__request_counter:03d}"

        request = BorrowRequest(request_id, item, borrower)
        self.__requests.append(request)
        return request

    def approve_request(self, request_id, approver, due_date):
        request = self.__find_request(request_id)
        self.__check_approver(request, approver)

        if not isinstance(due_date, datetime):
            raise ValueError("Due date must be a valid date and time.")

        if due_date <= datetime.now():
            raise ValueError("Due date must be in the future.")

        if request.item.status != ItemStatus.AVAILABLE:
            raise ValueError("This item is not available for borrowing.")

        request.update_status(RequestStatus.APPROVED)
        request.item.update_status(ItemStatus.BORROWED)

        self.__record_counter += 1
        record_id = f"REC{self.__record_counter:03d}"

        record = BorrowRecord(record_id, request, due_date)
        self.__records.append(record)
        return record

    def reject_request(self, request_id, approver):
        request = self.__find_request(request_id)
        self.__check_approver(request, approver)

        request.update_status(RequestStatus.REJECTED)
        return request

    def __find_request(self, request_id):
        for request in self.__requests:
            if request.request_id == request_id:
                return request

        raise ValueError("Borrow request not found.")

    def __check_approver(self, request, approver):
        if not isinstance(approver, Person):
            raise ValueError("A valid approver is required.")

        is_owner = request.item.owner.person_id == approver.person_id
        is_admin = isinstance(approver, Administrator)

        if not (is_owner or is_admin):
            raise ValueError(
                "Only the item owner or an administrator can do this."
            )
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
    
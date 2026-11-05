from enum import Enum


class RequestStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    RETURNED = "Returned"
    CANCELLED = "Cancelled"
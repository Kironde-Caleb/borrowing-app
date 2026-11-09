from enum import Enum


class ItemStatus(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    UNAVAILABLE = "Unavailable"

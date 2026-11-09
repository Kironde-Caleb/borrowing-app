
from src.models.item_category import ItemCategory
from src.models.item_status import ItemStatus
from src.models.person import Person


class Item:
    def __init__(self, item_id, name, description, category, owner):

        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError("Item ID cannot be empty.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Item name cannot be empty.")

        if not isinstance(description, str) or not description.strip():
            raise ValueError("Item description cannot be empty.")

        if not isinstance(category, ItemCategory):
            raise ValueError("Invalid item category.")

        if not isinstance(owner, Person):
            raise ValueError("Owner must be a valid person.")

        self.__item_id = item_id
        self.__name = name
        self.__description = description
        self.__category = category
        self.__owner = owner
        self.__status = ItemStatus.AVAILABLE

    @property
    def item_id(self):
        return self.__item_id

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def category(self):
        return self.__category

    @property
    def owner(self):
        return self.__owner

    @property
    def status(self):
        return self.__status

    def update_status(self, new_status):
        if isinstance(new_status, ItemStatus):
            self.__status = new_status
        else:
            raise ValueError("Invalid item status.")

    def display_item(self):
        return (
            f"Item ID: {self.__item_id}\n"
            f"Name: {self.__name}\n"
            f"Description: {self.__description}\n"
            f"Category: {self.__category.value}\n"
            f"Owner: {self.__owner.full_name}\n"
            f"Status: {self.__status.value}"
        )


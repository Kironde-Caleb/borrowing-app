from src.models.item import Item
from src.models.item_category import ItemCategory
from src.models.item_status import ItemStatus


class ItemService:
	"""Handles listing, viewing, searching and updating items."""

	def __init__(self):
		self.__items = {}

	def add_item(self, item_id, name, description, category, owner):
		# Item validates all fields and raises ValueError if invalid
		item = Item(item_id, name, description, category, owner)
		if item.item_id in self.__items:
			raise ValueError("An item with this ID already exists.")
		self.__items[item.item_id] = item
		return item

	def get_item(self, item_id):
		item = self.__items.get(item_id)
		if item is None:
			raise ValueError("Item not found.")
		return item

	def view_all_items(self):
		return list(self.__items.values())

	def view_available_items(self):
		return self.search_by_availability(ItemStatus.AVAILABLE)

	def search_by_name(self, keyword):
		if not isinstance(keyword, str) or not keyword.strip():
			raise ValueError("Search keyword cannot be empty.")
		keyword = keyword.strip().lower()
		return [i for i in self.__items.values() if keyword in i.name.lower()]

	def search_by_category(self, category):
		if not isinstance(category, ItemCategory):
			raise ValueError("Invalid item category.")
		return [i for i in self.__items.values() if i.category == category]

	def search_by_availability(self, status):
		if not isinstance(status, ItemStatus):
			raise ValueError("Invalid item status.")
		return [i for i in self.__items.values() if i.status == status]

	def update_item(self, item_id, name=None, description=None, category=None):
		old = self.get_item(item_id)
		new_item = Item(
			old.item_id,
			name if name is not None else old.name,
			description if description is not None else old.description,
			category if category is not None else old.category,
			old.owner,
		)
		new_item.update_status(old.status)
		self.__items[item_id] = new_item
		return new_item

	def set_availability(self, item_id, available):
		item = self.get_item(item_id)
		if item.status == ItemStatus.BORROWED:
			raise ValueError("Cannot change availability of a borrowed item.")
		if available:
			item.update_status(ItemStatus.AVAILABLE)
		else:
			item.update_status(ItemStatus.UNAVAILABLE)
		return item

from datetime import datetime, timedelta

from src.models.administrator import Administrator
from src.models.item_category import ItemCategory
from src.models.item_status import ItemStatus


class BorrowingCLI:
    """Command-line interface. It only talks to the services and the
    registry; all business rules stay in the services and models."""

    def __init__(self, item_service, borrowing_service, registry,
                 input_func=input, output_func=print):
        self.__items = item_service
        self.__borrowing = borrowing_service
        self.__registry = registry
        self.__input = input_func
        self.__output = output_func
        self.__user = None

    # ------------------------------------------------------------------
    # Entry point and menus
    # ------------------------------------------------------------------
    def run(self):
        self.__say("Welcome to the UCU Hostel Borrowing System")
        try:
            self.__start_menu()
        except (EOFError, KeyboardInterrupt):
            self.__say("\nGoodbye!")

    def __start_menu(self):
        actions = [
            ("Register as a student", self.__register_student),
            ("Log in", self.__log_in),
        ]
        while True:
            choice = self.__menu(
                "START MENU", [label for label, _ in actions], "Exit"
            )
            if choice == 0:
                self.__say("Goodbye!")
                return
            self.__safely(actions[choice - 1][1])
            if self.__user is not None:
                self.__user_menu()

    def __user_menu(self):
        actions = [
            ("View all items", self.__view_all_items),
            ("View available items", self.__view_available_items),
            ("Search for items", self.__search_items),
            ("List an item for lending", self.__list_item),
            ("Update one of my items", self.__update_item),
            ("Mark my item available / unavailable", self.__set_availability),
            ("Request to borrow an item", self.__request_borrow),
            ("View my borrow requests", self.__view_my_requests),
            ("Approve or reject requests for my items", self.__review_requests),
            ("View my borrowing records", self.__view_my_records),
            ("Return an item", self.__return_item),
        ]
        if self.__is_admin():
            actions += [
                ("[Admin] View all requests", self.__admin_all_requests),
                ("[Admin] View all borrowing records", self.__admin_all_records),
                ("[Admin] View all users", self.__admin_all_users),
            ]

        while self.__user is not None:
            role = "Administrator" if self.__is_admin() else "Student"
            choice = self.__menu(
                f"MAIN MENU - {self.__user.full_name} ({role})",
                [label for label, _ in actions],
                "Log out",
            )
            if choice == 0:
                self.__say(f"Logged out. Goodbye, {self.__user.full_name}!")
                self.__user = None
                return
            self.__safely(actions[choice - 1][1])

    # ------------------------------------------------------------------
    # Account actions
    # ------------------------------------------------------------------
    def __register_student(self):
        self.__say("\n--- Register as a student ---")
        student_id = self.__ask("Student ID: ")
        full_name = self.__ask("Full name: ")
        email = self.__ask("Email: ")
        hostel = self.__ask("Hostel: ")
        self.__user = self.__registry.register_student(
            student_id, full_name, email, hostel
        )
        self.__say(f"Registered and logged in as {self.__user.full_name}.")

    def __log_in(self):
        self.__say("\n--- Log in ---")
        person_id = self.__ask("Your ID: ")
        self.__user = self.__registry.find(person_id)
        self.__say(f"Welcome, {self.__user.full_name}!")

    # ------------------------------------------------------------------
    # Item actions
    # ------------------------------------------------------------------
    def __view_all_items(self):
        self.__show_all(
            self.__items.view_all_items(),
            lambda item: item.display_item(),
            "No items have been listed yet.",
        )

    def __view_available_items(self):
        self.__show_all(
            self.__items.view_available_items(),
            lambda item: item.display_item(),
            "No items are available right now.",
        )

    def __search_items(self):
        choice = self.__menu(
            "SEARCH ITEMS",
            ["By name", "By category", "By availability"],
            "Back",
        )
        if choice == 0:
            return
        if choice == 1:
            results = self.__items.search_by_name(self.__ask("Keyword: "))
        elif choice == 2:
            results = self.__items.search_by_category(self.__ask_category())
        else:
            results = self.__items.search_by_availability(self.__ask_status())
        self.__show_all(
            results, lambda item: item.display_item(), "No matching items found."
        )

    def __list_item(self):
        self.__say("\n--- List an item for lending ---")
        name = self.__ask("Item name: ")
        description = self.__ask("Description: ")
        category = self.__ask_category()
        item = self.__items.add_item(
            self.__next_item_id(), name, description, category, self.__user
        )
        self.__say("\nItem listed successfully:")
        self.__say(item.display_item())

    def __update_item(self):
        mine = self.__my_items()
        if not mine:
            self.__say("You have no items to update.")
            return
        self.__show_all(mine, lambda item: item.display_item(), "")
        item_id = self.__pick_from(
            mine, lambda item: item.item_id, "Item ID to update: "
        )
        self.__say("Press Enter to keep the current value.")
        name = self.__ask("New name: ") or None
        description = self.__ask("New description: ") or None
        category = self.__ask_category(allow_blank=True)
        item = self.__items.update_item(item_id, name, description, category)
        self.__say("\nItem updated:")
        self.__say(item.display_item())

    def __set_availability(self):
        mine = self.__my_items()
        if not mine:
            self.__say("You have no items to change.")
            return
        self.__show_all(mine, lambda item: item.display_item(), "")
        item_id = self.__pick_from(
            mine, lambda item: item.item_id, "Item ID: "
        )
        answer = self.__ask("Make it available for borrowing? (y/n): ").lower()
        if answer not in ("y", "n"):
            raise ValueError("Please answer y or n.")
        item = self.__items.set_availability(item_id, answer == "y")
        self.__say(f"{item.name} is now {item.status.value}.")

    # ------------------------------------------------------------------
    # Borrowing actions
    # ------------------------------------------------------------------
    def __request_borrow(self):
        candidates = [
            item for item in self.__items.view_available_items()
            if item.owner.person_id != self.__user.person_id
        ]
        if not candidates:
            self.__say("There are no items you can request right now.")
            return
        self.__show_all(candidates, lambda item: item.display_item(), "")
        item_id = self.__ask_id("Item ID to request: ")
        item = self.__items.get_item(item_id)
        request = self.__borrowing.submit_request(item, self.__user)
        self.__say("\nRequest submitted. The owner or an administrator must approve it.")
        self.__say(request.display_request())

    def __view_my_requests(self):
        mine = [
            request for request in self.__borrowing.get_all_requests()
            if request.borrower.person_id == self.__user.person_id
        ]
        self.__show_all(
            mine, lambda r: r.display_request(), "You have not made any requests."
        )

    def __review_requests(self):
        pending = [
            request for request in self.__borrowing.get_pending_requests()
            if self.__is_admin()
            or request.item.owner.person_id == self.__user.person_id
        ]
        if not pending:
            self.__say("There are no pending requests for you to review.")
            return
        self.__show_all(pending, lambda r: r.display_request(), "")
        request_id = self.__ask_id("Request ID to review (Enter to go back): ")
        if not request_id:
            return
        choice = self.__menu("REVIEW REQUEST", ["Approve", "Reject"], "Back")
        if choice == 0:
            return
        if choice == 1:
            days = self.__ask_int("Lend for how many days (1-90)? ", 1, 90)
            due_date = datetime.now() + timedelta(days=days)
            record = self.__borrowing.approve_request(
                request_id, self.__user, due_date
            )
            self.__say("\nRequest approved:")
            self.__say(record.display_record())
        else:
            request = self.__borrowing.reject_request(request_id, self.__user)
            self.__say(f"\nRequest {request.request_id} rejected.")

    def __view_my_records(self):
        me = self.__user.person_id
        records = self.__borrowing.get_all_records()
        borrowed = [r for r in records if r.borrow_request.borrower.person_id == me]
        lent = [r for r in records if r.borrow_request.item.owner.person_id == me]
        self.__say("\n=== Items I borrowed ===")
        self.__show_all(
            borrowed, self.__format_record, "You have not borrowed anything."
        )
        self.__say("\n=== Items I lent out ===")
        self.__show_all(
            lent, self.__format_record, "You have not lent anything out."
        )

    def __return_item(self):
        me = self.__user.person_id
        returnable = [
            r for r in self.__borrowing.get_active_records()
            if self.__is_admin()
            or r.borrow_request.borrower.person_id == me
            or r.borrow_request.item.owner.person_id == me
        ]
        if not returnable:
            self.__say("There are no items waiting to be returned.")
            return
        self.__show_all(returnable, self.__format_record, "")
        record_id = self.__pick_from(
            returnable, lambda r: r.record_id, "Record ID to return: "
        )
        record = self.__borrowing.return_item(record_id)
        self.__say("\nItem returned:")
        self.__say(record.display_record())

    # ------------------------------------------------------------------
    # Administrator actions
    # ------------------------------------------------------------------
    def __admin_all_requests(self):
        self.__show_all(
            self.__borrowing.get_all_requests(),
            lambda r: r.display_request(),
            "No borrow requests yet.",
        )

    def __admin_all_records(self):
        self.__show_all(
            self.__borrowing.get_all_records(),
            self.__format_record,
            "No borrowing records yet.",
        )

    def __admin_all_users(self):
        self.__show_all(
            self.__registry.all_users(),
            lambda person: person.display_details(),
            "No users registered.",
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def __is_admin(self):
        return isinstance(self.__user, Administrator)

    def __my_items(self):
        return [
            item for item in self.__items.view_all_items()
            if self.__is_admin()
            or item.owner.person_id == self.__user.person_id
        ]

    def __next_item_id(self):
        number = len(self.__items.view_all_items()) + 1
        while True:
            item_id = f"IT{number:03d}"
            try:
                self.__items.get_item(item_id)
            except ValueError:
                return item_id
            number += 1

    @staticmethod
    def __format_record(record):
        text = record.display_record()
        if record.return_date is None and record.due_date < datetime.now():
            text += "\n** OVERDUE **"
        return text

    def __say(self, text=""):
        self.__output(text)

    def __ask(self, prompt):
        return self.__input(prompt).strip()

    def __ask_id(self, prompt):
        return self.__ask(prompt).upper()

    def __ask_int(self, prompt, minimum, maximum):
        answer = self.__ask(prompt)
        if not answer.isdecimal() or not minimum <= int(answer) <= maximum:
            raise ValueError(
                f"Please enter a whole number from {minimum} to {maximum}."
            )
        return int(answer)

    def __ask_category(self, allow_blank=False):
        categories = list(ItemCategory)
        for number, category in enumerate(categories, start=1):
            self.__say(f"  {number}. {category.value}")
        suffix = " (Enter to keep current)" if allow_blank else ""
        answer = self.__ask(f"Category number{suffix}: ")
        if allow_blank and answer == "":
            return None
        if not answer.isdecimal() or not 1 <= int(answer) <= len(categories):
            raise ValueError("Please choose a valid category number.")
        return categories[int(answer) - 1]

    def __ask_status(self):
        statuses = list(ItemStatus)
        for number, status in enumerate(statuses, start=1):
            self.__say(f"  {number}. {status.value}")
        number = self.__ask_int("Status number: ", 1, len(statuses))
        return statuses[number - 1]

    def __pick_from(self, candidates, id_getter, prompt):
        chosen = self.__ask_id(prompt)
        if chosen not in [id_getter(c) for c in candidates]:
            raise ValueError("That ID is not in the list shown above.")
        return chosen

    def __menu(self, title, options, exit_label):
        while True:
            self.__say(f"\n=== {title} ===")
            for number, label in enumerate(options, start=1):
                self.__say(f"  {number}. {label}")
            self.__say(f"  0. {exit_label}")
            answer = self.__ask("Choose an option: ")
            if answer.isdecimal() and 0 <= int(answer) <= len(options):
                return int(answer)
            self.__say(f"Invalid choice. Enter a number from 0 to {len(options)}.")

    def __show_all(self, objects, formatter, empty_message):
        if not objects:
            if empty_message:
                self.__say(empty_message)
            return
        for obj in objects:
            self.__say("-" * 40)
            self.__say(formatter(obj))
        self.__say("-" * 40)
        self.__say(f"{len(objects)} shown.")

    def __safely(self, action):
        try:
            action()
        except ValueError as error:
            self.__say(f"Error: {error}")

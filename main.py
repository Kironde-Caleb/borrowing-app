from src.cli.menu import BorrowingCLI
from src.cli.user_registry import UserRegistry
from src.services.borrowing_service import BorrowingService
from src.services.item_service import ItemService


def main():
    registry = UserRegistry()
    # Default administrator so admin options can be used straight away.
    registry.register_administrator(
        "AD001", "Hostel Admin", "admin@ucu.ac.ug", "Hostel Manager"
    )

    cli = BorrowingCLI(ItemService(), BorrowingService(), registry)
    cli.run()


if __name__ == "__main__":
    main()

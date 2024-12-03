import reflex as rx
from typing import Union, List
import csv


class Item(rx.Base):
    """The item class."""

    name: str
    payment: float
    date: str
    status: str


class TableState(rx.State):
    """The state class."""

    items: List[Item] = []

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page

    def validate_item(self, item: Item) -> bool:
        """Validate an item before adding it to the list."""
        try:
            # Verify that payment is a positive number
            assert item.payment >= 0, "Payment must be positive."
            # Verify that status is valid
            assert item.status in ["Pending", "Completed", "In Progress"], "Invalid status."
            return True
        except AssertionError as e:
            print(f"Validation error: {e}")
            return False

    def load_entries(self):
        """Load items from a CSV file."""
        try:
            with open("items.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.items = [
                    Item(
                        name=row["name"],
                        payment=float(row["payment"]),
                        date=row["date"],
                        status=row["status"],
                    )
                    for row in reader
                    if self.validate_item(
                        Item(
                            name=row["name"],
                            payment=float(row["payment"]),
                            date=row["date"],
                            status=row["status"],
                        )
                    )
                ]
                self.total_items = len(self.items)
        except FileNotFoundError:
            print("The file 'items.csv' was not found.")
            self.items = []
            self.total_items = 0
        except KeyError as e:
            print(f"Missing column in CSV: {e}")
            self.items = []
            self.total_items = 0

    def toggle_sort(self, column: str):
        """Toggle the sort order for a specific column."""
        if self.sort_value == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_value = column
            self.sort_reverse = False

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[Item]:
        """Get filtered and sorted items."""
        items = self.items

        # Sort items based on selected column
        if self.sort_value:
            if self.sort_value in ["payment"]:
                items = sorted(
                    items,
                    key=lambda item: float(getattr(item, self.sort_value)),
                    reverse=self.sort_reverse,
                )
            else:
                items = sorted(
                    items,
                    key=lambda item: str(getattr(item, self.sort_value)).lower(),
                    reverse=self.sort_reverse,
                )

        # Filter items based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in ["name", "payment", "date", "status"]
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        """Get the current page number."""
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        """Get the total number of pages."""
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 0
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[Item]:
        """Get the items for the current page."""
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def prev_page(self):
        """Navigate to the previous page."""
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        """Navigate to the next page."""
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        """Navigate to the first page."""
        self.offset = 0

    def last_page(self):
        """Navigate to the last page."""
        self.offset = (self.total_pages - 1) * self.limit

    def paginate(self) -> List[Item]:
        """Get the items for the current page."""
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def export_to_csv(self, filename="exported_items.csv"):
        """Export the current items to a CSV file."""
        with open(filename, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "payment", "date", "status"])
            writer.writeheader()
            for item in self.filtered_sorted_items:
                writer.writerow(
                    {
                        "name": item.name,
                        "payment": item.payment,
                        "date": item.date,
                        "status": item.status,
                    }
                )
        print(f"Items exported to {filename}")

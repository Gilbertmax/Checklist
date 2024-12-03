import reflex as rx
from ..backend.table_state import TableState, Item


def _header_cell(text: str, icon: str) -> rx.Component:
    """Create a styled header cell."""
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def _show_item(item: Item, index: int) -> rx.Component:
    """Display a single checklist item in the table."""
    return rx.table.row(
        rx.table.row_header_cell(item.name),
        rx.table.cell(f"${item.payment}"),
        rx.table.cell(item.date),
        rx.table.cell(item.status),
        rx.table.cell(
            rx.input(
                type="file",
                on_change=lambda e: TableState.upload_evidence(item.name, e),
                size="sm",
            ),
            justify="center",
        ),
        style={
            "_hover": {"bg": rx.cond(index % 2 == 0, "gray.100", "gray.200")},
            "bg": rx.cond(index % 2 == 0, "white", "gray.50"),
        },
    )


def _pagination_view() -> rx.Component:
    """Pagination controls for the checklist table."""
    return rx.hstack(
        rx.text(
            "Page ",
            rx.code(TableState.page_number),
            f" of {TableState.total_pages}",
        ),
        rx.icon_button(
            rx.icon("chevron-left", size=18),
            on_click=TableState.prev_page,
            disabled=TableState.page_number == 1,
        ),
        rx.icon_button(
            rx.icon("chevron-right", size=18),
            on_click=TableState.next_page,
            disabled=TableState.page_number == TableState.total_pages,
        ),
        spacing="4",
        justify="end",
        margin_top="1rem",
    )


def checklist_table() -> rx.Component:
    """Render the checklist table."""
    return rx.box(
        rx.flex(
            rx.input(
                placeholder="Search project...",
                value=TableState.search_value,
                on_change=TableState.set_search_value,
                size="sm",
                max_width="250px",
            ),
            rx.button(
                "Export to Excel",
                on_click=TableState.export_to_excel,
                color="white",
                background_color="green",
                hover={"background_color": "darkgreen"},
            ),
            justify="space-between",
            wrap="wrap",
            width="100%",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Task Name", "task"),
                    _header_cell("Payment", "dollar-sign"),
                    _header_cell("Date", "calendar"),
                    _header_cell("Status", "check-circle"),
                    _header_cell("Evidence", "upload"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    TableState.get_current_page,
                    lambda item, index: _show_item(item, index),
                )
            ),
        ),
        _pagination_view(),
        width="100%",
    )

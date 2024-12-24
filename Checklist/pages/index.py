import reflex as rx
from ..templates import template
from .. import styles
from ..views.checklist_state import ChecklistState


def checklist_table(data: list) -> rx.Component:
    """Generate a table for the checklist.

    Args:
        data (list): The list of checklist items.

    Returns:
        A Reflex table component.
    """
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Name"),
                rx.table.column_header_cell("Owner"),
                rx.table.column_header_cell("Status"),
                rx.table.column_header_cell("Progress"),
            )
        ),
        rx.table.body(
            rx.foreach(
                data,
                lambda item: rx.table.row(
                    rx.table.cell(item["Name"]),
                    rx.table.cell(item["Owner"]),
                    rx.table.cell(item["Status"]),
                    rx.table.cell(f"{item['Progress']}%"),
                )
            )
        ),
        style=styles.base_style,  # Usar base_style en lugar de table_style
    )


@template(route="/", title="Checklist Overview")
def index() -> rx.Component:
    """The overview page for checklists.

    Returns:
        The UI for the checklist overview page.
    """
    return rx.vstack(
        rx.heading("Checklist Overview", size="5"),
        rx.flex(
            rx.input(
                placeholder="Search checklist...",
                value=ChecklistState.search_term,
                on_change=ChecklistState.set_search_term,
                size="3",
                width="100%",
                max_width="400px",
                radius="large",
                style=styles.ghost_input_style,
            ),
            rx.select(
                ["All", "Completed", "Pending", "In Progress"],
                default_value="All",
                value=ChecklistState.status_filter,
                on_change=ChecklistState.set_status_filter,
                width="200px",
            ),
            rx.button(
                "Create New Checklist",
                on_click=ChecklistState.go_to_create_page,
                color="white",
                background_color=styles.accent_color,
                hover={"background_color": styles.accent_text_color},
            ),
            justify="between",  # Corregido
            align="center",
            width="100%",
        ),
        checklist_table(ChecklistState.filtered_checklists),  # Correcta llamada
        rx.button(
            "Download as Excel",
            on_click=ChecklistState.download_checklists,
            color="white",
            background_color="green",
            hover={"background_color": "darkgreen"},
            margin_top="1rem",
        ),
        spacing="8",
        width="100%",
    )

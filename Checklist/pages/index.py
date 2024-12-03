"""The checklist overview page of the app."""

import reflex as rx
from ..templates import template
from .. import styles
from reflex.components.table import Table
from reflex.components.radix.forms import Select
from .checklist_state import ChecklistState


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
                hover={
                    "background_color": styles.accent_text_color,
                },
            ),
            justify="space-between",
            align="center",
            width="100%",
        ),
        Table(
            columns=["Name", "Owner", "Status", "Progress"],
            rows=ChecklistState.filtered_checklists,
            width="100%",
            style=styles.table_style,
        ),
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

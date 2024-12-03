"""The about page for the Checklist App."""

from .. import styles
from ..templates import template
import reflex as rx


@template(route="/about", title="About Checklist App")
def about() -> rx.Component:
    """The about page.

    Returns:
        The UI for the about page.
    """
    return rx.vstack(
        rx.heading("About the Checklist App", size="4", margin_bottom="1rem"),
        rx.text(
            "This app allows users to manage checklists efficiently. "
            "It provides features such as filtering, sorting, pagination, "
            "and exporting checklists to Excel. Users can also create new checklists, "
            "assign owners by area, and track progress in real-time.",
            size="3",
            margin_bottom="1rem",
        ),
        rx.text(
            "Key Features:",
            size="3",
            weight="bold",
            margin_bottom="0.5rem",
        ),
        rx.unordered_list(
            rx.list_item("Filter and sort checklists by name or status."),
            rx.list_item("Track progress of each checklist."),
            rx.list_item("Assign ownership to specific areas."),
            rx.list_item("Create, edit, and export checklists to Excel."),
            margin_bottom="1rem",
        ),
        rx.button(
            "Back to Dashboard",
            on_click=lambda: rx.redirect("/"),
            color="white",
            background_color=styles.accent_color,
            hover={"background_color": styles.accent_text_color},
            size="md",
        ),
        spacing="4",
        padding="2rem",
        width="100%",
        align_items="center",
    )

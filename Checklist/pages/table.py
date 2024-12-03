"""The checklist page."""

from ..templates import template
from ..backend.table_state import TableState
from ..views.table import checklist_table

import reflex as rx


@template(route="/checklist", title="Checklist", on_load=TableState.load_entries)
def table() -> rx.Component:
    """The checklist page.

    Returns:
        The UI for the checklist page.
    """
    return rx.vstack(
        rx.heading("Checklist Management", size="5"),
        checklist_table(),
        spacing="8",
        width="100%",
    )

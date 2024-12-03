"""Page for creating and editing checklists."""

import reflex as rx
from ..templates import template
from .. import styles
from .checklist_state import ChecklistState


@template(route="/create-checklist", title="Create/Edit Checklist")
def create_checklist() -> rx.Component:
    """Page to create or edit checklists.

    Returns:
        The UI for creating/editing checklists.
    """
    return rx.vstack(
        rx.heading("Create/Edit Checklist", size="5"),
        rx.input(
            placeholder="Project Name",
            value=ChecklistState.new_project_name,
            on_change=ChecklistState.set_new_project_name,
            size="3",
            width="100%",
            max_width="400px",
            radius="large",
            style=styles.ghost_input_style,
        ),
        rx.text_area(
            placeholder="Checklist Items (one per line)",
            value=ChecklistState.new_checklist_items,
            on_change=ChecklistState.set_new_checklist_items,
            rows=10,
            width="100%",
        ),
        rx.select(
            ["Area 1", "Area 2", "Area 3"],
            value=ChecklistState.new_owner,
            on_change=ChecklistState.set_new_owner,
            width="100%",
        ),
        rx.button(
            "Save Checklist",
            on_click=ChecklistState.save_checklist,
            color="white",
            background_color=styles.accent_color,
            hover={"background_color": styles.accent_text_color},
        ),
        spacing="8",
        width="100%",
    )

import reflex as rx
import pandas as pd


class ChecklistState(rx.State):
    """State to manage the checklist view."""

    checklists = [
        {"Name": "Checklist 1", "Owner": "Area 1", "Status": "Completed", "Progress": "100%"},
        {"Name": "Checklist 2", "Owner": "Area 2", "Status": "In Progress", "Progress": "50%"},
        {"Name": "Checklist 3", "Owner": "Area 3", "Status": "Pending", "Progress": "0%"},
    ]
    search_term: str = ""
    status_filter: str = "All"

    def set_search_term(self, value: str):
        self.search_term = value

    def set_status_filter(self, value: str):
        self.status_filter = value

    @property
    def filtered_checklists(self):
        filtered = self.checklists
        if self.search_term:
            filtered = [
                c for c in filtered if self.search_term.lower() in c["Name"].lower()
            ]
        if self.status_filter != "All":
            filtered = [c for c in filtered if c["Status"] == self.status_filter]
        return filtered

    def go_to_create_page(self):
        rx.redirect("/create-checklist")

    def download_checklists(self):
        df = pd.DataFrame(self.checklists)
        df.to_excel("checklists.xlsx", index=False)
        rx.download("checklists.xlsx")

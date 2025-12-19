class StudentTreeviewRenderer:
    def __init__(self, treeview, styles):
        self.treeview = treeview
        self.styles = styles

    def clear(self):
        self.treeview.delete(*self.treeview.get_children())

    def render(self, rows, selected_ids):
        self.clear()

        if not rows:
            self.treeview.insert(
                "", "end",
                values=("", "Aucun élève trouvé", "", "", "", "")
            )
            return

        for index, row in enumerate(rows):
            tag = "even" if index % 2 == 0 else "odd"
            if row["id"] in selected_ids:
                tag = "selected"

            self.treeview.insert(
                "",
                "end",
                iid=f"student_{row['id']}",
                values=(
                    "☑️" if row["id"] in selected_ids else "☐",
                    row["nom"],
                    row["prenom"],
                    row["classe"],
                    row["annee"],
                    row["events"]
                ),
                tags=(tag,)
            )

    def configure_tags(self):
        self.treeview.tag_configure(
            "selected",
            background=self.styles.colors["selected"],
            foreground=self.styles.colors["dark_blue"]
        )
        self.treeview.tag_configure(
            "even",
            background=self.styles.colors["white"]
        )
        self.treeview.tag_configure(
            "odd",
            background=self.styles.colors["off_white"]
        )
# ====================================================
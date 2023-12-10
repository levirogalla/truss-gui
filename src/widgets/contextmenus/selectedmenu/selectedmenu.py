from PyQt6.QtWidgets import QMenu


class SelectedMenu(QMenu):
    """Right click menu for selected items."""

    def __init__(self, parent: "TrussWidget"):
        super().__init__(parent)
        # change track grad
        self.delete_items = self.addAction("Delete Item(s)")

        self.delete_items.triggered.connect(self.handle_delete)

    def handle_delete(self) -> None:
        """Delete the joint."""

        for item in self.parent().scene().selectedItems():
            # make sure the item wasn't already deleted
            try:
                self.parent().deleteItem(item)
            except KeyError:
                # the item was already deleted
                continue

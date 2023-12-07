import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMenu, QDialog, QWidget
from pytruss import Support, Joint, Mesh, Force, Member

# from .trusswidget2 import JointItem, TrussWidget
from dialogs.manageitems.manageitems import JointConnections
from dialogs.editcoordinates.editcoordinates import EditCoordinatesDialog


class SelectedMenu(QMenu):
    """Joint right-click menu."""

    def __init__(self, parent: "TrussWidget"):
        super().__init__(parent)
        # change track grad
        self.delete_items = self.addAction("Delete Item(s)")

        self.delete_items.triggered.connect(self.handle_delete)

    def handle_delete(self):
        print(self.parent().connections)

        for item in self.parent().scene().selectedItems():
            # make sure the item wasn't already deleted
            try:
                self.parent().deleteItem(item)
            except KeyError:
                # the item was already deleted
                continue

import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMenu, QDialog, QWidget
from pytruss import Support, Joint, Mesh, Force, Member

# from .trusswidget2 import JointItem, TrussWidget
from .editCoordinates_ui import Ui_EditCoordinatesDialog


class EditCoordinates(QDialog):
    """Class for edit joint coordinates dialog."""

    def __init__(self, parent, joint: Joint) -> None:
        super().__init__(parent)

        self.ui = Ui_EditCoordinatesDialog()
        self.ui.setupUi(self)
        self.x_coord: float = None
        self.y_coord: float = None

        self.ui.doneButton.pressed.connect(self.handleDone)
        self.ui.cancelButton.pressed.connect(self.close)

        self.ui.xCoordinate.setText(str(joint.x_coordinate.item()))
        self.ui.yCoordinate.setText(str(joint.y_coordinate.item()))

    def handleDone(self):
        self.x_coord = float(self.ui.xCoordinate.text())
        self.y_coord = float(self.ui.yCoordinate.text())
        self.close()

    @staticmethod
    def getCoordinates(parent, joint: Joint) -> tuple[float, float]:
        dialog = EditCoordinates(parent, joint)
        dialog.exec()
        return (dialog.x_coord, dialog.y_coord)

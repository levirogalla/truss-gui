import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMenu, QDialog, QWidget
from pytruss import Support, Joint, Mesh, Force, Member

# from .trusswidget2 import JointItem, TrussWidget
from .editcoordinates_ui import Ui_EditCoordinatesDialog


class EditCoordinatesDialog(QDialog):
    """Class for edit joint coordinates dialog."""

    def __init__(self, parent, joint: Joint) -> None:
        super().__init__(parent)

        self.ui = Ui_EditCoordinatesDialog()
        self.ui.setupUi(self)
        self.x_coord: float = None
        self.y_coord: float = None

        self.ui.doneButton.pressed.connect(self.handleDone)
        self.ui.cancelButton.pressed.connect(self.cancel)

        self.ui.xCoordinate.setText(str(joint.x_coordinate.item()))
        self.ui.yCoordinate.setText(str(joint.y_coordinate.item()))
        self.ui.trackGrad.setCurrentText(str(joint.track_grad))

    def cancel(self):
        self.close()
        return None, None, None

    def handleDone(self):
        self.x_coord = float(self.ui.xCoordinate.text())
        self.y_coord = float(self.ui.yCoordinate.text())
        self.track_grad = True if self.ui.trackGrad.currentText() == "True" else False
        self.close()

    @staticmethod
    def getCoordinates(parent, joint: Joint) -> tuple[float, float]:
        dialog = EditCoordinatesDialog(parent, joint)
        dialog.exec()
        return (dialog.x_coord, dialog.y_coord, dialog.track_grad)

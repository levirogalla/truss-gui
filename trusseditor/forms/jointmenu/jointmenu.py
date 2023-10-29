import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMenu, QDialog, QWidget
from pytruss import Support, Joint, Mesh, Force, Member

# from .trusswidget2 import JointItem, TrussWidget
from ..jointconnections.jointconnection import JointConnections
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


class JointMenu(QMenu):
    """Joint right-click menu."""

    def __init__(self, parent: "TrussWidget", joint_item: "JointItem"):
        super().__init__(parent)
        # change track grad
        self.joint_item = joint_item
        self.track_grad_menu = QMenu("Track Grad")
        self.set_track_grad_true = self.track_grad_menu.addAction("True")
        self.set_track_grad_true.setCheckable(True)

        self.set_track_grad_false = self.track_grad_menu.addAction("False")
        self.set_track_grad_false.setCheckable(True)
        self.addAction(self.track_grad_menu.menuAction())
        if joint_item.joint.track_grad:
            self.set_track_grad_true.setChecked(True)
        else:
            self.set_track_grad_false.setChecked(True)

        self.edit_coordinate_action = self.addAction("Edit Coordinates")
        self.addSeparator()
        self.supports_action = self.addAction("Supports...")
        self.forces_action = self.addAction("Forces...")
        self.members_action = self.addAction("Members...")
        self.addSeparator()
        self.delete_joint_action = self.addAction("Delete Joint")

        self.set_track_grad_true.triggered.connect(
            lambda: self.update_track_grad(True))
        self.set_track_grad_false.triggered.connect(
            lambda: self.update_track_grad(False))

        self.supports_action.triggered.connect(self.show_supports)
        self.forces_action.triggered.connect(self.show_forces)
        self.members_action.triggered.connect(self.show_members)
        self.delete_joint_action.triggered.connect(self.delete_joint)
        self.edit_coordinate_action.triggered.connect(self.edit_coordinates)

    def update_track_grad(self, track_grad):
        self.joint_item.joint.set_track_grad(track_grad)
        self.joint_item.updateSceneLocation()

    def show_supports(self):
        dialog = JointConnections(self.parent(), self.joint_item, Support)
        dialog.exec()

    def show_forces(self):
        dialog = JointConnections(self.parent(), self.joint_item, Force)
        dialog.exec()

    def show_members(self):
        dialog = JointConnections(self.parent(), self.joint_item, Member)
        dialog.exec()

    def delete_joint(self):
        self.parent().deleteJoint(self.joint_item.joint)

    def edit_coordinates(self):
        x_coord, y_coord = EditCoordinates.getCoordinates(
            self.parent(), self.joint_item.joint)
        if x_coord is None or y_coord is None:
            return
        self.joint_item.joint.set_cordinates([x_coord, y_coord])
        self.joint_item.updateSceneLocation()

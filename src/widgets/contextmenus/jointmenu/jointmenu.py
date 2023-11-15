import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMenu, QDialog, QWidget
from pytruss import Support, Joint, Mesh, Force, Member

# from .trusswidget2 import JointItem, TrussWidget
from dialogs.manageitems.manageitems import JointConnections
from dialogs.editcoordinates.editcoordinates import EditCoordinatesDialog


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

        self.dialogs = set()

    def update_track_grad(self, track_grad):
        self.joint_item.joint.set_track_grad(track_grad)
        self.joint_item.updateSceneLocation()

    def show_supports(self):
        dialog = JointConnections(self.parent(), self.joint_item, Support)
        dialog.open()
        self.dialogs.add(dialog)
        dialog.finished.connect(lambda: self.deleteDialog(dialog))

    def show_forces(self):
        dialog = JointConnections(self.parent(), self.joint_item, Force)
        dialog.open()
        self.dialogs.add(dialog)
        dialog.finished.connect(lambda: self.deleteDialog(dialog))

    def show_members(self):
        dialog = JointConnections(self.parent(), self.joint_item, Member)
        dialog.open()
        self.dialogs.add(dialog)
        dialog.finished.connect(lambda: self.deleteDialog(dialog))

    def delete_joint(self):
        self.parent().deleteJoint(self.joint_item.joint)

    def deleteDialog(self, dialog: QDialog) -> None:
        dialog.deleteLater()
        self.dialogs.remove(dialog)

    def edit_coordinates(self):
        x_coord, y_coord = EditCoordinatesDialog.getCoordinates(
            self.parent(), self.joint_item.joint)
        if x_coord is None or y_coord is None:
            return
        self.joint_item.joint.set_cordinates([x_coord, y_coord])
        self.joint_item.updateSceneLocation()

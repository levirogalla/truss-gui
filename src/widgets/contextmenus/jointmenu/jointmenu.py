from PySide6.QtWidgets import QMenu, QDialog
from trussty import Support, Force, Member

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

    def update_track_grad(self, track_grad) -> None:
        "Update joints track grad based on menu selection."
        self.joint_item.joint.set_track_grad(track_grad)
        self.joint_item.updateSceneLocation()

    def show_supports(self) -> None:
        """Open the support table for the connected support."""
        dialog = JointConnections(self.parent(), self.joint_item, Support)
        dialog.open()
        self.dialogs.add(dialog)
        dialog.finished.connect(lambda: self.deleteDialog(dialog))

    def show_forces(self) -> None:
        """Open the forces table for the connected forces."""
        dialog = JointConnections(self.parent(), self.joint_item, Force)
        dialog.open()
        self.dialogs.add(dialog)
        dialog.finished.connect(lambda: self.deleteDialog(dialog))

    def show_members(self) -> None:
        """Open members table for connected members."""
        dialog = JointConnections(self.parent(), self.joint_item, Member)
        dialog.open()
        self.dialogs.add(dialog)
        dialog.finished.connect(lambda: self.deleteDialog(dialog))

    def delete_joint(self) -> None:
        """Delete a joint via the table."""
        self.parent().deleteJoint(self.joint_item.joint)

    def deleteDialog(self, dialog: QDialog) -> None:
        """Delete the dialog."""
        dialog.deleteLater()
        self.dialogs.remove(dialog)

    def edit_coordinates(self) -> None:
        """Edit the coordinate of a joint."""
        x_coord, y_coord, track_grad = EditCoordinatesDialog.getCoordinates(
            self.parent(), self.joint_item.joint)
        if x_coord is None or y_coord is None:
            return
        self.joint_item.joint.set_cordinates([x_coord, y_coord])
        self.joint_item.joint.set_track_grad(track_grad)
        self.joint_item.updateSceneLocation()

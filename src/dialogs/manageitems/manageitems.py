import typing

from PySide6.QtWidgets import QDialog,  QTableWidgetItem, QTableWidget, QMessageBox

from trussty import Mesh, Joint, Member, Support, Force

from .manageitems_ui import Ui_Dialog
from ..addforcequick.addforcequick import AddForceQuickDialog
from ..addsupportquick.addsupportquick import AddSupportQuickDialog
from ..addforce.addforce import AddForceDialog
from ..addsupport.addsupport import AddSupportDialog
from ..editcoordinates.editcoordinates import EditCoordinatesDialog


class JointConnections(QDialog):
    """Class for optimization window dialog."""

    def __init__(self, truss_widget: "TrussWidget", joint_item: "JointItem", show_type: typing.Type[Member | Force | Support]) -> None:
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.truss_widget = truss_widget
        self.joint_item = joint_item
        self.ui.connectedItems.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.ui.connectedItems.setSelectionMode(
            QTableWidget.SelectionMode.MultiSelection
        )

        if show_type == Force:
            self.__loadForces()
            self.ui.addButton.pressed.connect(self.addForce)
            self.ui.deleteButton.pressed.connect(self.deleteForce)
        elif show_type == Member:
            self.__loadMembers()
            self.ui.addButton.pressed.connect(self.addMember)
            self.ui.deleteButton.pressed.connect(self.deleteMember)
        elif show_type == Support:
            self.__loadSupport()
            self.ui.addButton.pressed.connect(self.addSupport)
            self.ui.deleteButton.pressed.connect(self.deleteSupport)

    def __loadMembers(self) -> None:
        """Populate the table with connected members."""
        self.ui.connectedItems.setRowCount(
            len(self.joint_item.joint.members))

        self.ui.connectedItems.setColumnCount(5)
        self.ui.connectedItems.setHorizontalHeaderItem(
            0, QTableWidgetItem("Member ID"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            1, QTableWidgetItem("Joint A"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            2, QTableWidgetItem("Joint B"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            3, QTableWidgetItem("Internal Force"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            4, QTableWidgetItem("Force Type"))

        for r, member in enumerate(self.joint_item.joint.members):
            self.ui.connectedItems.setItem(
                r, 0, QTableWidgetItem(str(id(member))))
            self.ui.connectedItems.setItem(
                r, 1, QTableWidgetItem(str(member.joint_a))
            )
            self.ui.connectedItems.setItem(
                r, 2, QTableWidgetItem(str(member.joint_b))
            )
            self.ui.connectedItems.setItem(
                r, 3, QTableWidgetItem(str(member.force.item()))
            )
            self.ui.connectedItems.setItem(
                r, 4, QTableWidgetItem(str(member.force_type))
            )

        self.ui.connectedItems.resizeColumnsToContents()

        # deactive add and delete button because idk how to implement those in a nice way
        self.ui.addButton.setEnabled(False)

    def __loadSupport(self) -> None:
        """Populate the table with connected support."""
        support = self.joint_item.joint.support
        self.ui.connectedItems.clear()
        self.ui.connectedItems.setColumnCount(6)
        self.ui.connectedItems.setHorizontalHeaderItem(
            0, QTableWidgetItem("Support ID"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            1, QTableWidgetItem("Joint"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            2, QTableWidgetItem("Type"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            3, QTableWidgetItem("X Support Reaction"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            4, QTableWidgetItem("Y Support Reaction"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            5, QTableWidgetItem("Moment Support Reaction"))

        if support is not None:
            self.ui.connectedItems.setRowCount(1)
            self.ui.connectedItems.setItem(
                0, 0, QTableWidgetItem(str(id(support))))
            self.ui.connectedItems.setItem(
                0, 1, QTableWidgetItem(str(support.joint)))
            self.ui.connectedItems.setItem(
                0, 2, QTableWidgetItem(str(support.base.base_to_code(support.base))))
            self.ui.connectedItems.setItem(
                0, 3, QTableWidgetItem(str(float(support.x_reaction)))
            )
            self.ui.connectedItems.setItem(
                0, 4, QTableWidgetItem(str(float(support.y_reaction)))
            )
            self.ui.connectedItems.setItem(
                0, 5, QTableWidgetItem(str(float(support.moment_reaction)))
            )

        self.ui.connectedItems.resizeColumnsToContents()

    def __loadForces(self) -> None:
        """Populate the table with connected forces."""
        self.ui.connectedItems.setRowCount(
            len(self.joint_item.joint.forces))

        self.ui.connectedItems.setColumnCount(5)
        self.ui.connectedItems.setHorizontalHeaderItem(
            0, QTableWidgetItem("Force ID"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            1, QTableWidgetItem("Joint"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            2, QTableWidgetItem("X Component"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            3, QTableWidgetItem("Y Component"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            4, QTableWidgetItem("Type"))

        for r, force in enumerate(self.joint_item.joint.forces):
            self.ui.connectedItems.setItem(
                r, 0, QTableWidgetItem(str(id(force))))
            self.ui.connectedItems.setItem(
                r, 1, QTableWidgetItem(str(force.joint)))
            self.ui.connectedItems.setItem(
                r, 2, QTableWidgetItem(str(float(force.x_component)))
            )
            self.ui.connectedItems.setItem(
                r, 3, QTableWidgetItem(str(float(force.y_component)))
            )
            self.ui.connectedItems.setItem(
                r, 4, QTableWidgetItem(str(force.type))
            )

        self.ui.connectedItems.resizeColumnsToContents()

    def addForce(self) -> None:
        "Add force."
        x_comp, y_comp = AddForceQuickDialog.get_components(self)
        if x_comp is None or y_comp is None:
            return
        self.truss_widget.addForce(
            Force(self.joint_item.joint, x_comp, y_comp))
        self.__loadForces()

    def addMember(self) -> None:
        "Add member."
        pass

    def addSupport(self) -> None:
        "Add support."
        support_type = AddSupportQuickDialog.get_type(self)
        if support_type is None:
            return
        self.truss_widget.addSupport(self.joint_item.joint, support_type)
        self.__loadSupport()

    def get_selected_items(self) -> typing.Generator:
        "Gets items selected on the table."
        selected_items = self.ui.connectedItems.selectedItems()

        rows_visted = set()
        for item_cell in selected_items:
            row = item_cell.row()
            if row not in rows_visted:
                item_id = int(self.ui.connectedItems.item(row, 0).text())
                item = self.truss_widget.connections[item_id]
                rows_visted.add(row)
                yield item

    def deleteForce(self) -> None:
        "Delete forces from truss."
        for force in self.get_selected_items():
            self.truss_widget.deleteForce(force.force)

        self.__loadForces()

    def deleteMember(self) -> None:
        "Delete members from truss."
        for member in self.get_selected_items():
            self.truss_widget.deleteMember(member.member)
        self.__loadMembers()

    def deleteSupport(self) -> None:
        "Delete supports from truss."
        for support in self.get_selected_items():
            self.truss_widget.deleteSupport(support.support)

        self.__loadSupport()


class TrussItems(QDialog):
    """Class for optimization window dialog."""

    def __init__(self, truss_widget: "TrussWidget", show_type: typing.Type[Member | Force | Support | Joint]) -> None:
        super().__init__()
        self.truss_widget = truss_widget

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.truss: Mesh = truss_widget.truss

        self.ui.connectedItems.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.ui.connectedItems.setSelectionMode(
            QTableWidget.SelectionMode.MultiSelection
        )
        if show_type == Force:
            self.__loadForces()
            self.ui.addButton.pressed.connect(self.addForce)
            self.ui.deleteButton.pressed.connect(self.deleteForce)
            truss_widget.interacted.connect(self.__loadForces)
        elif show_type == Member:
            self.__loadMembers()
            self.ui.addButton.pressed.connect(self.addMember)
            self.ui.deleteButton.pressed.connect(self.deleteMember)
            truss_widget.interacted.connect(self.__loadMembers)
        elif show_type == Support:
            self.__loadSupports()
            self.ui.addButton.pressed.connect(self.addSupport)
            self.ui.deleteButton.pressed.connect(self.deleteSupport)
            truss_widget.interacted.connect(self.__loadSupports)
        elif show_type == Joint:
            self.__loadJoints()
            self.ui.addButton.pressed.connect(self.addJoint)
            self.ui.deleteButton.pressed.connect(self.deleteJoint)
            truss_widget.interacted.connect(self.__loadJoints)

    def __loadMembers(self) -> None:
        """Populate the table with connected members."""
        self.ui.connectedItems.setRowCount(
            len(self.truss.members))
        self.ui.connectedItems.setColumnCount(5)
        self.ui.connectedItems.setHorizontalHeaderItem(
            0, QTableWidgetItem("Member ID"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            1, QTableWidgetItem("Joint A"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            2, QTableWidgetItem("Joint B"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            3, QTableWidgetItem("Internal Force"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            4, QTableWidgetItem("Force Type"))

        for r, member in enumerate(self.truss.members):
            member: Member
            self.ui.connectedItems.setItem(
                r, 0, QTableWidgetItem(str(id(member))))
            self.ui.connectedItems.setItem(
                r, 1, QTableWidgetItem(str(member.joint_a))
            )
            self.ui.connectedItems.setItem(
                r, 2, QTableWidgetItem(str(member.joint_b))
            )
            self.ui.connectedItems.setItem(
                r, 3, QTableWidgetItem(str(member.force.item()))
            )
            self.ui.connectedItems.setItem(
                r, 4, QTableWidgetItem(str(member.force_type))
            )

        self.ui.connectedItems.resizeColumnsToContents()

        # deactive add and delete button because idk how to implement those in a nice way
        self.ui.addButton.setEnabled(False)

    def __loadSupports(self) -> None:
        """Populate the table with connected support."""
        self.ui.connectedItems.setRowCount(
            len(self.truss.supports))
        self.ui.connectedItems.setColumnCount(6)
        self.ui.connectedItems.setHorizontalHeaderItem(
            0, QTableWidgetItem("Support ID"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            1, QTableWidgetItem("Joint"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            2, QTableWidgetItem("Type"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            3, QTableWidgetItem("X Support Reaction"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            4, QTableWidgetItem("Y Support Reaction"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            5, QTableWidgetItem("Moment Support Reaction"))

        for r, support in enumerate(self.truss.supports):
            if support is not None:
                support: Support
                self.ui.connectedItems.setItem(
                    r, 0, QTableWidgetItem(str(id(support))))
                self.ui.connectedItems.setItem(
                    r, 1, QTableWidgetItem(str(support.joint)))
                self.ui.connectedItems.setItem(
                    r, 2, QTableWidgetItem(str(support.base.base_to_code(support.base))))
                self.ui.connectedItems.setItem(
                    r, 3, QTableWidgetItem(str(float(support.x_reaction)))
                )
                self.ui.connectedItems.setItem(
                    r, 4, QTableWidgetItem(str(float(support.y_reaction)))
                )
                self.ui.connectedItems.setItem(
                    r, 5, QTableWidgetItem(str(float(support.moment_reaction)))
                )

        self.ui.connectedItems.resizeColumnsToContents()

    def __loadForces(self) -> None:
        """Populate the table with connected forces."""
        self.ui.connectedItems.setRowCount(
            len(self.truss.forces))

        self.ui.connectedItems.setColumnCount(5)
        self.ui.connectedItems.setHorizontalHeaderItem(
            0, QTableWidgetItem("Force ID"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            1, QTableWidgetItem("Joint"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            2, QTableWidgetItem("X Component"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            3, QTableWidgetItem("Y Component"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            4, QTableWidgetItem("Type"))

        for r, force in enumerate(self.truss.forces):
            force: Force
            self.ui.connectedItems.setItem(
                r, 0, QTableWidgetItem(str(id(force))))
            self.ui.connectedItems.setItem(
                r, 1, QTableWidgetItem(str(force.joint)))
            self.ui.connectedItems.setItem(
                r, 2, QTableWidgetItem(str(float(force.x_component)))
            )
            self.ui.connectedItems.setItem(
                r, 3, QTableWidgetItem(str(float(force.y_component)))
            )
            self.ui.connectedItems.setItem(
                r, 4, QTableWidgetItem(str(force.type))
            )

        self.ui.connectedItems.resizeColumnsToContents()

    def __loadJoints(self) -> None:
        """Populate the table with connected forces."""
        self.ui.connectedItems.setRowCount(
            len(self.truss.joints))

        self.ui.connectedItems.setColumnCount(4)
        self.ui.connectedItems.setHorizontalHeaderItem(
            0, QTableWidgetItem("Joint ID"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            1, QTableWidgetItem("X Coordinate"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            2, QTableWidgetItem("Y Coordinate"))
        self.ui.connectedItems.setHorizontalHeaderItem(
            3, QTableWidgetItem("Track Grad"))

        for r, joint in enumerate(self.truss.joints):
            joint: Joint
            self.ui.connectedItems.setItem(
                r, 0, QTableWidgetItem(str(id(joint))))
            self.ui.connectedItems.setItem(
                r, 1, QTableWidgetItem(str(joint.x_coordinate.item()))
            )
            self.ui.connectedItems.setItem(
                r, 2, QTableWidgetItem(str(joint.y_coordinate.item()))
            )
            self.ui.connectedItems.setItem(
                r, 3, QTableWidgetItem(str(joint.track_grad))
            )

    def addForce(self) -> None:
        "Add force via table."
        force = AddForceDialog.get_force(self.truss.joints, None)
        if force is None:
            QMessageBox.warning(
                self, "Error", "Could not add force, missing fields.")
            return
        self.truss_widget.addForce(force)
        self.__loadForces()

    def addMember(self) -> None:
        "Not Implemented"
        raise NotImplementedError

    def addSupport(self) -> None:
        "Add support via table."
        joint, support_type = AddSupportDialog.get_support(
            self.truss.joints, None)
        self.truss_widget.addSupport(joint, support_type)
        self.__loadSupports()

    def addJoint(self) -> None:
        "Add joint via table."
        joint = Joint(0, 0, False)
        x_cord, y_cord, track_grad = EditCoordinatesDialog.getCoordinates(
            self, joint)
        self.truss_widget.addJoint(
            Joint(float(x_cord),  float(y_cord), track_grad))

    def get_selected_items(self) -> typing.Generator:
        """Get selected items on table."""
        selected_items = self.ui.connectedItems.selectedItems()

        rows_visted = set()
        for item_cell in selected_items:
            try:
                row = item_cell.row()
            except RuntimeError:
                # means the cell was deleted from memory so skip it
                continue
            if row not in rows_visted:
                item_id = int(self.ui.connectedItems.item(row, 0).text())
                item = self.truss_widget.connections[item_id]
                rows_visted.add(row)
                yield item

    def deleteForce(self) -> None:
        "Delete a force via table."
        for force in self.get_selected_items():
            self.truss_widget.deleteForce(force.force)

        self.__loadForces()

    def deleteMember(self) -> None:
        "Delete a member via table."
        for member in self.get_selected_items():
            self.truss_widget.deleteMember(member.member)
        self.__loadMembers()

    def deleteSupport(self) -> None:
        "Delete a support via table."
        for support in self.get_selected_items():
            self.truss_widget.deleteSupport(support.support)
        self.__loadSupports()

    def deleteJoint(self) -> None:
        "Delete joints via table."
        for joint in self.get_selected_items():
            self.truss_widget.deleteJoint(joint.joint)

        self.__loadJoints()

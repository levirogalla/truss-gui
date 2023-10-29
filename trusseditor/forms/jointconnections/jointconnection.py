import copy
import typing

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QDialog, QFileDialog, QWidget, QTableWidgetItem, QTableWidgetSelectionRange, QTableWidget

from pytruss import Mesh, Joint, Member, Support, Force

from .jointconnections_ui import Ui_Dialog
from .addforce import AddForce
from .addsupport import AddSupport


class JointConnections(QDialog):
    """Class for optimization window dialog."""

    def __init__(self, parent: "TrussWidget", joint_item: "JointItem", show_type: typing.Type[Member | Force | Support]) -> None:
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.joint_item = joint_item
        self.ui.connectedItems.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.ui.connectedItems.setSelectionMode(
            QTableWidget.SelectionMode.MultiSelection
        )
        if show_type == Force:
            self.loadForces()
            self.ui.addButton.pressed.connect(self.addForce)
            self.ui.deleteButton.pressed.connect(self.deleteForce)
        elif show_type == Member:
            self.loadMembers()
            self.ui.addButton.pressed.connect(self.addMember)
            self.ui.deleteButton.pressed.connect(self.deleteMember)
        elif show_type == Support:
            self.loadSupport()
            self.ui.addButton.pressed.connect(self.addSupport)
            self.ui.deleteButton.pressed.connect(self.deleteSupport)

    def loadMembers(self):
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

    def loadSupport(self):
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

    def loadForces(self):
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

    def addForce(self):
        x_comp, y_comp = AddForce.getComponents(self)
        if x_comp is None or y_comp is None:
            return
        self.parent().addForce(self.joint_item.joint, x_comp, y_comp)
        self.loadForces()

    def addMember(self):
        pass

    def addSupport(self):
        support_type = AddSupport.getType(self)
        if support_type is None:
            return
        self.parent().addSupport(self.joint_item.joint, support_type)
        self.loadSupport()

    def get_selected_items(self):
        selected_items = self.ui.connectedItems.selectedItems()

        rows_visted = set()
        for item_cell in selected_items:
            row = item_cell.row()
            if row not in rows_visted:
                item_id = int(self.ui.connectedItems.item(row, 0).text())
                print(self.parent().connections)
                item = self.parent(
                ).connections[item_id]
                rows_visted.add(row)
                yield item

    def deleteForce(self):
        for force in self.get_selected_items():
            self.parent().deleteForce(force.force)

        self.loadForces()

    def deleteMember(self):
        for member in self.get_selected_items():
            self.parent().deleteMember(member.member)
        self.loadMembers()

    def deleteSupport(self):
        for support in self.get_selected_items():
            self.parent().deleteSupport(support.support)

        self.loadSupport()

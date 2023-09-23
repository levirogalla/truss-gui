"""Gui for pytruss."""

import sys
import typing
from PyQt6 import QtGui
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidgetSelectionRange, QAbstractItemView
from trusseditor.trusswidget import TrussWidget
from trusseditor.circle import JointWidget
from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.addJointButton.clicked.connect(self.ui.build.previewJoint)
        self.ui.addMemberButton.clicked.connect(self.ui.build.addMember)
        # self.ui.addSupportButton.clicked.connect(self.ui.build.supportForm)
        # self.ui.addForceButton.clicked.connect(self.ui.build.forceForm)

        self.ui.jointInfo.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )
        self.ui.build.interacted.connect(self.updateInfo)
        self.ui.jointInfo.itemSelectionChanged.connect(self.setJointSelection)
        self.ui.jointInfo.cellChanged.connect(self.updateJointLocation)

        self.ui.build.member_added.connect(self.loadMembers)
        self.ui.build.joint_added.connect(self.loadJoints)
        self.ui.build.support_added.connect(self.loadSupports)
        self.ui.build.force_added.connect(self.loadForces)

    def setJointSelection(self):
        selectedIds = set()

        self.ui.build.clearMoves()

        for item in self.ui.jointInfo.selectedItems():
            if item.column() == 0:
                selectedIds.add(item.text())

        for jointWidget in self.findChildren(JointWidget):
            jointWidget: JointWidget
            if str(id(jointWidget.joint)) in selectedIds:
                jointWidget.selectJoint()

    def updateJointLocation(self, row, col):
        for jointWidget in self.findChildren(JointWidget):
            if str(id(jointWidget.joint)) == self.ui.jointInfo.item(row, 0).text():
                x = self.ui.jointInfo.item(row, 1).text()
                y = self.ui.jointInfo.item(row, 2).text()
                jointWidget.joint.set_cordinates([float(x), float(y)])
                jointWidget.updateLocation()
        self.ui.build.update()

    def updateInfo(self):
        self.ui.jointInfo.itemSelectionChanged.disconnect(
            self.setJointSelection
        )

        self.ui.jointInfo.clearSelection()
        self.ui.memberInfo.clearSelection()
        self.loadJoints()
        self.loadMembers()
        self.loadSupports()
        self.loadForces()

        self.ui.jointInfo.itemSelectionChanged.connect(
            self.setJointSelection
        )

    def loadSupports(self):
        self.ui.jointInfo.cellChanged.disconnect(self.updateJointLocation)
        self.ui.supportInfo.setRowCount(len(self.ui.build.truss.supports))
        for r, support in enumerate(self.ui.build.truss.supports):
            self.ui.supportInfo.setItem(
                r, 0, QTableWidgetItem(str(id(support))))
            self.ui.supportInfo.setItem(
                r, 1, QTableWidgetItem(str(support.joint)))
            self.ui.supportInfo.setItem(
                r, 2, QTableWidgetItem(str(support.base.base_to_code(support.base))))
        self.ui.jointInfo.cellChanged.connect(self.updateJointLocation)

    def loadJoints(self):
        self.ui.jointInfo.cellChanged.disconnect(self.updateJointLocation)
        self.ui.jointInfo.setRowCount(len(self.ui.build.truss.joints))
        for r, joint in enumerate(self.ui.build.truss.joints):
            self.ui.jointInfo.setItem(r, 0, QTableWidgetItem(str(id(joint))))
            self.ui.jointInfo.setItem(
                r, 1, QTableWidgetItem(str(joint.x_coordinate.item()))
            )
            self.ui.jointInfo.setItem(
                r, 2, QTableWidgetItem(str(joint.y_coordinate.item()))
            )

            if joint in self.ui.build.highlighted_joints:
                self.ui.jointInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 0, r, 2), True)
        self.ui.jointInfo.cellChanged.connect(self.updateJointLocation)

    def loadMembers(self):
        self.ui.memberInfo.setRowCount(len(self.ui.build.truss.members))
        for r, member in enumerate(self.ui.build.truss.members):
            self.ui.memberInfo.setItem(r, 0, QTableWidgetItem(str(id(member))))
            self.ui.memberInfo.setItem(
                r, 1, QTableWidgetItem(str(member.joint_a))
            )
            self.ui.memberInfo.setItem(
                r, 2, QTableWidgetItem(str(member.joint_b))
            )

            if member.joint_a in self.ui.build.highlighted_joints:
                self.ui.memberInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 1, r, 1), True)
            if member.joint_b in self.ui.build.highlighted_joints:
                self.ui.memberInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 2, r, 2), True)

    def loadForces(self):
        self.ui.forceInfo.setRowCount(len(self.ui.build.truss.forces))
        for r, force in enumerate(self.ui.build.truss.forces):
            self.ui.forceInfo.setItem(r, 0, QTableWidgetItem(str(id(force))))
            self.ui.forceInfo.setItem(r, 1, QTableWidgetItem(str(force.joint)))
            self.ui.forceInfo.setItem(
                r, 2, QTableWidgetItem(str(force.x_component))
            )
            self.ui.forceInfo.setItem(
                r, 3, QTableWidgetItem(str(force.y_component))
            )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Truss Maker")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

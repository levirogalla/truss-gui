"""Gui for pytruss."""

import sys
import typing
from PyQt6 import QtGui
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidgetSelectionRange, QAbstractItemView
from trusseditor.trusswidget import TrussWidget

from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.addJointButton.clicked.connect(self.handleJointClick)
        self.ui.addMemberButton.clicked.connect(self.handleMemberClick)
        self.ui.jointInfo.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )
        self.ui.build.interacted.connect(self.updateInfo)

    def updateInfo(self):
        self.ui.jointInfo.clearSelection()
        self.ui.memberInfo.clearSelection()
        self.loadJoints()
        self.loadMembers()

    def handleMemberClick(self):
        self.ui.build.addMember()
        self.loadMembers()

    def handleJointClick(self):
        self.ui.build.addJoint()
        self.loadJoints()

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        super().mouseMoveEvent(a0)
        pos = a0.globalPosition()
        relative_pos = self.ui.tabWidget.mapFromGlobal(pos)
        x = relative_pos.x()
        y = relative_pos.y()

    def loadJoints(self):
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


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

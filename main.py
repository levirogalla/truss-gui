"""Gui for pytruss."""

import sys
import typing
from PyQt6 import QtGui
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QFileDialog, QApplication, QMainWindow, QTableWidgetItem, QTableWidgetSelectionRange, QAbstractItemView
from trusseditor.trusswidget2 import JointItem, TrussWidget, SavedTruss
from mainwindow_ui import Ui_MainWindow
from pytruss import Mesh
from trusseditor.forms.checksave.checksave import CheckSaveForm
from trusseditor.forms.optimizer.optimize import OptimizeDialog
from trusseditor.forms.trusspreferences.trussprefences import TrussPreferences


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.forms = set()

        # flags
        self.ui.jointInfo.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )

        # file actions
        self.ui.actionNew.triggered.connect(self.handleCreateNewTab)
        self.ui.actionOpen.triggered.connect(self.handleOpenTruss)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionSave.triggered.connect(self.handleSave)

        # solve actions
        self.ui.actionSolve_Members.triggered.connect(
            self.handleSolveMembers)
        self.ui.actionSolve_Reactions.triggered.connect(
            self.handleSolveReactions)
        self.ui.actionOpen_Optimizer.triggered.connect(
            self.handleOptimize
        )

        # view actions
        self.ui.actionView_in_MPL.triggered.connect(self.openTrussInMPL)
        self.ui.actionTruss_Preferences.triggered.connect(
            self.openTrussPreferences)

        # info selection stuff
        self.connectInfoSignals()

        self.ui.jointInfo.cellChanged.connect(self.updateJointLocation)

        # tab stuff
        self.ui.tabWidget.currentChanged.connect(self.setUpButtonSignals)
        self.current_tab: TrussWidget = self.ui.tabWidget.currentWidget()
        self.setUpButtonSignals()
        self.ui.tabWidget.tabCloseRequested.connect(self.handleTabClose)

    def openTrussPreferences(self):
        dialog = TrussPreferences(self.current_tab)
        dialog.exec()

    def destroyForm(self, form):
        self.forms.remove(form)

    def handleOptimize(self):
        # block current truss widget when this form is opened
        form = OptimizeDialog(self.ui.tabWidget.currentWidget())
        form.exec()

    def handleSolveReactions(self):
        truss_widget: TrussWidget = self.ui.tabWidget.currentWidget()
        truss_widget.truss.solve_supports()
        truss_widget.loadTrussWidgetFromMesh(False)
        self.updateInfo()

    def handleSolveMembers(self):
        truss_widget: TrussWidget = self.ui.tabWidget.currentWidget()
        truss_widget.truss.solve_members()
        truss_widget.loadTrussWidgetFromMesh(False)
        self.updateInfo()

    def saveAs(self, optional_suffix=""):
        current_truss: TrussWidget = self.ui.tabWidget.currentWidget()
        current_truss.file = None
        self.handleSave()

    def handleSave(self, optional_suffix=""):
        current_truss: TrussWidget = self.ui.tabWidget.currentWidget()

        if current_truss.file is None:
            saveAsDialog = QFileDialog(self)
            saveAsDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            saveAsDialog.setFileMode(QFileDialog.FileMode.Directory)
            file, _ = saveAsDialog.getSaveFileName(
                self, "Save As", None, "Truss File (.trss)")
            if file == "":
                return
            current_truss.file = file

        current_truss.saveTruss()

    def handleOpenTruss(self):
        # this is a callback function that opens the truss on the gui
        openFileDialog = QFileDialog()
        openFileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        openFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        openFileDialog.setNameFilter("Truss Files (*.trss);; All Files (*)")
        openFileDialog.show()

        files = []
        if openFileDialog.exec():
            files = openFileDialog.selectedFiles()

        for file in files:
            truss_widget = TrussWidget(file)
            self.handleCreateNewTab(truss_widget)
            self.ui.tabWidget.setCurrentWidget(truss_widget)

    def openTrussInMPL(self):
        self.current_tab.truss.show(show=True)

    def handleCreateNewTab(self, truss: TrussWidget = None):

        # weird bug where truss is passed as false?
        if not isinstance(truss, TrussWidget):
            self.ui.tabWidget.addTab(TrussWidget(), "Truss New")
        else:
            self.ui.tabWidget.addTab(truss, truss.file.split("/")[-1])

    def handleTabClose(self, index):
        # add pop up to save truss if its not saved
        truss_widget: TrussWidget = self.ui.tabWidget.widget(index)

        if len(truss_widget.edits) != 0:
            form = CheckSaveForm(
                self, self.handleSave, lambda: self.ui.tabWidget.removeTab(index), lambda: None)
            form.exec()
        else:
            self.ui.tabWidget.removeTab(index)

    def connectInfoSignals(self):
        self.ui.jointInfo.itemSelectionChanged.connect(
            self.updateTrussSelections)
        self.ui.memberInfo.itemSelectionChanged.connect(
            self.updateTrussSelections)
        self.ui.forceInfo.itemSelectionChanged.connect(
            self.updateTrussSelections)
        self.ui.supportInfo.itemSelectionChanged.connect(
            self.updateTrussSelections)

    def disconnectInfoSignals(self):
        self.ui.jointInfo.itemSelectionChanged.disconnect(
            self.updateTrussSelections)
        self.ui.memberInfo.itemSelectionChanged.disconnect(
            self.updateTrussSelections)
        self.ui.forceInfo.itemSelectionChanged.disconnect(
            self.updateTrussSelections)
        self.ui.supportInfo.itemSelectionChanged.disconnect(
            self.updateTrussSelections)

    def setUpButtonSignals(self):
        last_tab = self.current_tab
        new_tab: TrussWidget = self.ui.tabWidget.currentWidget()

        # disconnect old signals
        # checks to make sure signals are connected before attempting to disconnect
        if last_tab != new_tab:
            last_tab.interacted.disconnect(self.updateInfo)
            last_tab.member_added.disconnect(self.loadMembers)
            last_tab.joint_added.disconnect(self.loadJoints)
            last_tab.support_added.disconnect(self.loadSupports)
            last_tab.force_added.disconnect(self.loadForces)
            self.ui.addJointButton.clicked.disconnect(last_tab.previewJoint)
            self.ui.addMemberButton.clicked.disconnect(last_tab.addMember)
            self.ui.addSupportButton.clicked.disconnect(last_tab.supportForm)
            self.ui.addForceButton.clicked.disconnect(last_tab.forceForm)

        # connect new signals
        new_tab.interacted.connect(self.updateInfo)
        new_tab.member_added.connect(self.loadMembers)
        new_tab.joint_added.connect(self.loadJoints)
        new_tab.support_added.connect(self.loadSupports)
        new_tab.force_added.connect(self.loadForces)
        self.ui.addJointButton.clicked.connect(new_tab.previewJoint)
        self.ui.addMemberButton.clicked.connect(new_tab.addMember)
        self.ui.addSupportButton.clicked.connect(new_tab.supportForm)
        self.ui.addForceButton.clicked.connect(new_tab.forceForm)

        self.current_tab = new_tab

    def updateTrussSelections(self):
        self.disconnectInfoSignals()
        self.current_tab.scene().clearSelection()

        for item in self.ui.jointInfo.selectedItems():
            if item.column() == 0:
                truss_graphics_item = self.current_tab.connections[int(
                    item.text())]
                truss_graphics_item.setSelected(True)

        for item in self.ui.memberInfo.selectedItems():
            if item.column() == 0:
                truss_graphics_item = self.current_tab.connections[int(
                    item.text())]

                print(self.current_tab.connections, item.text())
                truss_graphics_item.setSelected(True)

        for item in self.ui.supportInfo.selectedItems():
            if item.column() == 0:
                truss_graphics_item = self.current_tab.connections[int(
                    item.text())]
                truss_graphics_item.setSelected(True)

        for item in self.ui.forceInfo.selectedItems():
            if item.column() == 0:
                truss_graphics_item = self.current_tab.connections[int(
                    item.text())]
                truss_graphics_item.setSelected(True)

        self.connectInfoSignals()

    def updateJointLocation(self, row, col):
        try:
            joint_id = self.ui.jointInfo.item(row, 0).text()
            joint_item: JointItem = self.current_tab.connections[int(joint_id)]
            joint = joint_item.joint

            # changed x val
            if col == 1:
                joint.set_x(float(self.ui.jointInfo.item(row, col).text()))

            # changed y val
            elif col == 2:
                joint.set_y(float(self.ui.jointInfo.item(row, col).text()))

            # changed movable
            elif col == 3:
                new_val = self.ui.jointInfo.item(row, col).text()
                if new_val == "True":
                    joint.set_track_grad(True)
                elif new_val == "False":
                    joint.set_track_grad(False)

            joint_item.updateSceneLocation()
            self.current_tab.scene().update()
        except Exception as e:
            print(e)

    def updateInfo(self):
        self.disconnectInfoSignals()

        self.ui.jointInfo.clearSelection()
        self.ui.memberInfo.clearSelection()
        self.ui.forceInfo.clearSelection()
        self.ui.supportInfo.clearSelection()
        self.loadJoints()
        self.loadMembers()
        self.loadSupports()
        self.loadForces()

        self.connectInfoSignals()

    def loadSupports(self):
        self.ui.jointInfo.cellChanged.disconnect(self.updateJointLocation)
        self.ui.supportInfo.setRowCount(
            len(self.ui.tabWidget.currentWidget().truss.supports))
        for r, support in enumerate(self.ui.tabWidget.currentWidget().truss.supports):
            self.ui.supportInfo.setItem(
                r, 0, QTableWidgetItem(str(id(support))))
            self.ui.supportInfo.setItem(
                r, 1, QTableWidgetItem(str(support.joint)))
            self.ui.supportInfo.setItem(
                r, 2, QTableWidgetItem(str(support.base.base_to_code(support.base))))
            self.ui.supportInfo.setItem(
                r, 3, QTableWidgetItem(str(float(support.x_reaction)))
            )
            self.ui.supportInfo.setItem(
                r, 4, QTableWidgetItem(str(float(support.y_reaction)))
            )
            self.ui.supportInfo.setItem(
                r, 5, QTableWidgetItem(str(float(support.moment_reaction)))
            )

            if self.itemIsSelected(support):
                self.ui.supportInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 0, r, 5), True)

            if self.itemIsSelected(support.joint):
                self.ui.memberInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 1, r, 1), True)

        self.ui.jointInfo.cellChanged.connect(self.updateJointLocation)

    def loadJoints(self):
        self.ui.jointInfo.cellChanged.disconnect(self.updateJointLocation)
        self.ui.jointInfo.setRowCount(
            len(self.ui.tabWidget.currentWidget().truss.joints))
        for r, joint in enumerate(self.ui.tabWidget.currentWidget().truss.joints):
            self.ui.jointInfo.setItem(r, 0, QTableWidgetItem(str(id(joint))))
            self.ui.jointInfo.setItem(
                r, 1, QTableWidgetItem(str(joint.x_coordinate.item()))
            )
            self.ui.jointInfo.setItem(
                r, 2, QTableWidgetItem(str(joint.y_coordinate.item()))
            )
            self.ui.jointInfo.setItem(
                r, 3, QTableWidgetItem(str(joint.track_grad))
            )

            if self.itemIsSelected(joint):
                self.ui.jointInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 0, r, 3), True)

        self.ui.jointInfo.cellChanged.connect(self.updateJointLocation)

    def loadMembers(self):
        self.ui.memberInfo.setRowCount(
            len(self.ui.tabWidget.currentWidget().truss.members))
        for r, member in enumerate(self.ui.tabWidget.currentWidget().truss.members):
            self.ui.memberInfo.setItem(r, 0, QTableWidgetItem(str(id(member))))
            self.ui.memberInfo.setItem(
                r, 1, QTableWidgetItem(str(member.joint_a))
            )
            self.ui.memberInfo.setItem(
                r, 2, QTableWidgetItem(str(member.joint_b))
            )
            self.ui.memberInfo.setItem(
                r, 3, QTableWidgetItem(str(member.force.item()))
            )
            self.ui.memberInfo.setItem(
                r, 4, QTableWidgetItem(str(member.force_type))
            )

            if self.itemIsSelected(member):
                self.ui.memberInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 0, r, 4), True)

            if self.itemIsSelected(member.joint_a):
                self.ui.memberInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 1, r, 1), True)

            if self.itemIsSelected(member.joint_b):
                self.ui.memberInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 2, r, 2), True)

    def loadForces(self):
        self.ui.forceInfo.setRowCount(
            len(self.ui.tabWidget.currentWidget().truss.forces))
        for r, force in enumerate(self.ui.tabWidget.currentWidget().truss.forces):
            self.ui.forceInfo.setItem(r, 0, QTableWidgetItem(str(id(force))))
            self.ui.forceInfo.setItem(r, 1, QTableWidgetItem(str(force.joint)))
            self.ui.forceInfo.setItem(
                r, 2, QTableWidgetItem(str(float(force.x_component)))
            )
            self.ui.forceInfo.setItem(
                r, 3, QTableWidgetItem(str(float(force.y_component)))
            )
            self.ui.forceInfo.setItem(
                r, 4, QTableWidgetItem(str(force.type))
            )

            if self.itemIsSelected(force):
                self.ui.forceInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 0, r, 4), True)

            if self.itemIsSelected(force.joint):
                self.ui.forceInfo.setRangeSelected(
                    QTableWidgetSelectionRange(r, 1, r, 1), True)

    def itemIsSelected(self, truss_item):
        if self.ui.tabWidget.currentWidget().connections[id(truss_item)] is not None:
            return self.ui.tabWidget.currentWidget().connections[id(truss_item)].isSelected()
        return False

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        print(self.ui.tabWidget.currentWidget())
        return super().mousePressEvent(a0)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Truss Maker")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

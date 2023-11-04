"""Gui for pytruss."""

import sys

from PyQt6.QtWidgets import QFileDialog, QDialog, QApplication, QMainWindow, QTableWidgetItem, QTableWidgetSelectionRange, QAbstractItemView
from PyQt6.QtCore import Qt
from pytruss import Force, Member, Joint, Support

from mainwindow_ui import Ui_MainWindow
from trusseditor.trusswidget2 import JointItem, TrussWidget
from trusseditor.forms.checksave.checksave import CheckSaveForm
from trusseditor.forms.optimizer.optimize import OptimizeDialog
from trusseditor.forms.trusspreferences.trussprefences import TrussPreferences
from trusseditor.forms.manageitems.manageitems import TrussItems


class MainWindow(QMainWindow):
    """Creates the main window."""

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # flags
        self.ui.jointInfo.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )

        # file actions
        self.ui.actionNew.triggered.connect(self.handleCreateNewTab)
        self.ui.actionOpen.triggered.connect(self.handleOpenTruss)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionSave.triggered.connect(self.handleSave)

        # edit actions
        self.ui.actionForce.triggered.connect(self.openForcesTable)
        self.ui.actionMember.triggered.connect(self.openMembersTable)
        self.ui.actionSupport.triggered.connect(self.openSupportsTable)
        self.ui.actionJoint.triggered.connect(self.openJointsTable)

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

        self.dialogs = set()

    def openTrussPreferences(self) -> None:
        """Opens the view preferences dialog."""
        dialog = TrussPreferences(self.current_tab)
        dialog.exec()

    def handleOptimize(self) -> None:
        """Opens the optimization dialog."""
        # block current truss widget when this form is opened
        form = OptimizeDialog(self.current_tab)
        form.exec()

    def handleSolveReactions(self) -> None:
        """Solves and displayes support reaction forces."""
        truss_widget: TrussWidget = self.current_tab
        truss_widget.truss.solve_supports()
        truss_widget.loadTrussWidgetFromMesh(False)

    def handleSolveMembers(self) -> None:
        """Solves and displays internal member forces."""
        truss_widget: TrussWidget = self.current_tab
        truss_widget.truss.solve_members()
        truss_widget.loadTrussWidgetFromMesh(False)
        self.updateInfo()

    def saveAs(self, optional_suffix: str = "") -> None:
        """Handles the save as request and open save dialog always."""
        current_truss: TrussWidget = self.current_tab
        current_truss.file = None
        self.handleSave()

    def handleSave(self, optional_suffix: str = "") -> None:
        """Handles save request and only open save dialog if the truss has never been saved before."""
        current_truss: TrussWidget = self.current_tab

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

    def handleOpenTruss(self) -> None:
        """Handles open file request. Loads the truss onto the GUI."""

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

        self.updateInfo()

    def openTrussInMPL(self) -> None:
        """Opens the truss in Matplotlib."""
        self.current_tab.truss.show(show=True)

    def handleCreateNewTab(self, truss: TrussWidget = None) -> None:
        """Creates a new tab either with an existing truss or new truss."""
        if not isinstance(truss, TrussWidget):
            self.ui.tabWidget.addTab(TrussWidget(), "Truss New")
        else:
            self.ui.tabWidget.addTab(truss, truss.file.split("/")[-1])

    def handleTabClose(self, index: int) -> None:
        """Handles close tab request. Opens dialog to save recent changes if not saved."""
        truss_widget: TrussWidget = self.ui.tabWidget.widget(index)

        if len(truss_widget.edits) != 0:
            form = CheckSaveForm(
                self, self.handleSave, lambda: self.ui.tabWidget.removeTab(index), lambda: None)
            form.exec()
        else:
            self.ui.tabWidget.removeTab(index)

    def connectInfoSignals(self) -> None:
        """Connects info table signals to handlers."""
        self.ui.jointInfo.itemSelectionChanged.connect(
            self.updateTrussSelections)
        self.ui.memberInfo.itemSelectionChanged.connect(
            self.updateTrussSelections)
        self.ui.forceInfo.itemSelectionChanged.connect(
            self.updateTrussSelections)
        self.ui.supportInfo.itemSelectionChanged.connect(
            self.updateTrussSelections)

    def disconnectInfoSignals(self) -> None:
        """Disconnects info table signals to handlers."""
        self.ui.jointInfo.itemSelectionChanged.disconnect(
            self.updateTrussSelections)
        self.ui.memberInfo.itemSelectionChanged.disconnect(
            self.updateTrussSelections)
        self.ui.forceInfo.itemSelectionChanged.disconnect(
            self.updateTrussSelections)
        self.ui.supportInfo.itemSelectionChanged.disconnect(
            self.updateTrussSelections)

    def setUpButtonSignals(self) -> None:
        """Connects button signals to handler functions."""
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

    def updateTrussSelections(self) -> None:
        """Updates selected items on truss scene if item is selected on info tables."""
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

    def updateJointLocation(self, row: int, col: int) -> None:
        """Updates the joint data when info table is edited."""
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

    def updateInfo(self) -> None:
        """
        Updates the info tables with truss items data.
        Clears all current tables and re-populates them.
        """
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

    def loadSupports(self) -> None:
        """Populates the support info table."""
        self.ui.jointInfo.cellChanged.disconnect(self.updateJointLocation)
        self.ui.supportInfo.setRowCount(
            len(self.current_tab.truss.supports))
        for r, support in enumerate(self.current_tab.truss.supports):
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

    def loadJoints(self) -> None:
        """Populates the joints info table."""

        self.ui.jointInfo.cellChanged.disconnect(self.updateJointLocation)
        self.ui.jointInfo.setRowCount(
            len(self.current_tab.truss.joints))
        for r, joint in enumerate(self.current_tab.truss.joints):
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

    def loadMembers(self) -> None:
        """Populates the members info table."""
        self.ui.memberInfo.setRowCount(
            len(self.current_tab.truss.members))
        for r, member in enumerate(self.current_tab.truss.members):
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

    def loadForces(self) -> None:
        """Populates the forces info table."""
        self.ui.forceInfo.setRowCount(
            len(self.current_tab.truss.forces))
        for r, force in enumerate(self.current_tab.truss.forces):
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

    def itemIsSelected(self, truss_item) -> bool:
        """Returns wether a truss item is selected on the scene."""
        if self.current_tab.connections[id(truss_item)] is not None:
            return self.current_tab.connections[id(truss_item)].isSelected()
        return False

    def deleteDialog(self, dialog: QDialog):
        dialog.deleteLater()
        self.dialogs.remove(dialog)

    def openForcesTable(self):
        dialog = TrussItems(self.current_tab, Force)
        dialog.open()
        self.dialogs.add(dialog)
        dialog.finished.connect(lambda: self.deleteDialog(dialog))

    def openJointsTable(self):
        dialog = TrussItems(self.current_tab, Joint)
        dialog.open()
        self.dialogs.add(dialog)
        dialog.finished.connect(lambda: self.deleteDialog(dialog))

    def openMembersTable(self):
        dialog = TrussItems(self.current_tab, Member)
        dialog.open()
        self.dialogs.add(dialog)
        dialog.finished.connect(lambda: self.deleteDialog(dialog))

    def openSupportsTable(self):
        dialog = TrussItems(self.current_tab, Support)
        dialog.open()
        self.dialogs.add(dialog)
        dialog.finished.connect(lambda: self.deleteDialog(dialog))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Truss Maker")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

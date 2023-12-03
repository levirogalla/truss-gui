"""Gui for pytruss."""

import sys
import functools

from PyQt6.QtWidgets import QFileDialog, QDialog, QApplication, QMainWindow, QTableWidgetItem, QTableWidgetSelectionRange, QAbstractItemView
from PyQt6.QtCore import Qt
from pytruss import Force, Member, Joint, Support

from .mainwindow_ui import Ui_MainWindow
from widgets.trussview.graphicsitems import JointItem, MemberItem, ForceItem, JointItem
from widgets.trussview.graphicsview import TrussWidget
from widgets.contextmenus.startmenu.startpage import StartPage
from dialogs.checksave.checksave import CheckSaveDialog
from dialogs.optimize.optimize import OptimizeDialog
from dialogs.trusspreferences.trussprefences import TrussPreferences
from dialogs.manageitems.manageitems import TrussItems
from dialogs.generalsettings.generalsettings import GeneralSettings
from utils.saveopen import SavedTruss


class MainWindow(QMainWindow):
    """Creates the main window."""

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # give start page reference to main window
        self.ui.start.set_main_window(self)

        # flags
        self.ui.jointInfo.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )

        # tab stuff
        self.ui.tabWidget.currentChanged.connect(self.handleTabChange)
        self.current_tab: TrussWidget | StartPage = self.ui.tabWidget.currentWidget()
        self.connectFileActions()
        self.handleTabChange()
        self.ui.tabWidget.tabCloseRequested.connect(self.handleTabClose)

        # info selection stuff
        self.connectInfoSignals()

        self.ui.jointInfo.cellChanged.connect(self.updateJointLocation)
        self.ui.actionStart.triggered.connect(
            lambda: self.ui.tabWidget.addTab(StartPage(), "Start"))

        self.dialogs = set()

        # for the open recent action
        self.showRecentFiles()

    def showRecentFiles(self):
        recent_files = SavedTruss.recent()

        for file in recent_files:
            self.ui.menuOpen_Recent.addAction(
                file, functools.partial(self.handleCreateNewTab, truss=TrussWidget(file)))

    def disconnectActions(self) -> None:
        try:
            # file actions
            self.disconnectFileActions()

            # edit actions
            self.disconnectEditActions()

            # solve actions
            self.disconnectSolveActions()

            # view actions
            self.disconnectViewActions()
        except TypeError as e:
            print("Some or all actions aren't connected.", e)

    def connectActions(self) -> None:
        # file actions
        self.connectFileActions()

        # edit actions
        self.connectEditActions()

        # solve actions
        self.connectSolveActions()

        # view actions
        self.connectViewActions()

    def connectViewActions(self):
        self.ui.actionView_in_MPL.triggered.connect(self.openTrussInMPL)
        self.ui.actionTruss_Preferences.triggered.connect(
            self.openTrussPreferences)
        self.ui.actionGeneral_Settings.triggered.connect(
            self.openGeneralSettings
        )

        self.ui.actionZoom_In.triggered.connect(self.handleZoomIn)
        self.ui.actionZoom_Out.triggered.connect(self.handleZoomOut)

    def disconnectViewActions(self):
        self.ui.actionView_in_MPL.triggered.disconnect(self.openTrussInMPL)
        self.ui.actionTruss_Preferences.triggered.disconnect(
            self.openTrussPreferences)
        self.ui.actionGeneral_Settings.triggered.disconnect(
            self.openGeneralSettings
        )
        self.ui.actionZoom_In.triggered.disconnect(self.handleZoomIn)
        self.ui.actionZoom_Out.triggered.disconnect(self.handleZoomOut)

    def handleZoomIn(self) -> None:
        self.current_tab.resizeViewport(
            -self.current_tab.general_settings["zoom_step"])

    def handleZoomOut(self) -> None:
        self.current_tab.resizeViewport(
            self.current_tab.general_settings["zoom_step"])

    def connectSolveActions(self):
        self.ui.actionSolve_Members.triggered.connect(
            self.handleSolveMembers)
        self.ui.actionSolve_Reactions.triggered.connect(
            self.handleSolveReactions)
        self.ui.actionOpen_Optimizer.triggered.connect(
            self.handleOptimize
        )

    def disconnectSolveActions(self):
        self.ui.actionSolve_Members.triggered.disconnect(
            self.handleSolveMembers)
        self.ui.actionSolve_Reactions.triggered.disconnect(
            self.handleSolveReactions)
        self.ui.actionOpen_Optimizer.triggered.disconnect(
            self.handleOptimize
        )

    def connectEditActions(self):
        self.ui.actionForce.triggered.connect(self.openForcesTable)
        self.ui.actionMember.triggered.connect(self.openMembersTable)
        self.ui.actionSupport.triggered.connect(self.openSupportsTable)
        self.ui.actionJoint.triggered.connect(self.openJointsTable)

        self.ui.actionAddJointDrop.triggered.connect(
            self.current_tab.previewJoint)
        self.ui.actionAddJointDialog.triggered.connect(
            self.current_tab.handleAddJoint)
        self.ui.actionAddMember.triggered.connect(self.current_tab.addMember)
        self.ui.actionAddForce.triggered.connect(self.current_tab.forceForm)
        self.ui.actionAddSupport.triggered.connect(
            self.current_tab.supportForm)

    def disconnectEditActions(self):
        self.ui.actionForce.triggered.disconnect(self.openForcesTable)
        self.ui.actionMember.triggered.disconnect(self.openMembersTable)
        self.ui.actionSupport.triggered.disconnect(self.openSupportsTable)
        self.ui.actionJoint.triggered.disconnect(self.openJointsTable)

        self.ui.actionAddJointDrop.triggered.disconnect(
            self.current_tab.previewJoint)
        self.ui.actionAddJointDialog.triggered.disconnect(
            self.current_tab.handleAddJoint)
        self.ui.actionAddMember.triggered.disconnect(
            self.current_tab.addMember)
        self.ui.actionAddForce.triggered.disconnect(self.current_tab.forceForm)
        self.ui.actionAddSupport.triggered.disconnect(
            self.current_tab.supportForm)

    def connectFileActions(self):
        self.ui.actionNew.triggered.connect(self.handleCreateNewTab)
        self.ui.actionOpen.triggered.connect(self.handleOpenTruss)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionSave.triggered.connect(self.handleSave)

    def disconnectFileActions(self):
        self.ui.actionNew.triggered.disconnect(self.handleCreateNewTab)
        self.ui.actionOpen.triggered.disconnect(self.handleOpenTruss)
        self.ui.actionSave_As.triggered.disconnect(self.saveAs)
        self.ui.actionSave.triggered.disconnect(self.handleSave)

    def openTrussPreferences(self) -> None:
        """Opens the view preferences dialog."""
        dialog = TrussPreferences(self.current_tab)
        dialog.exec()

    def openGeneralSettings(self) -> None:
        dialog = GeneralSettings(self.current_tab)
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
        # file actions are connected on start page so add check
        if not isinstance(current_truss, StartPage):
            current_truss.file = None
            self.handleSave()

    def handleSave(self, optional_suffix: str = "") -> None:
        """Handles save request and only open save dialog if the truss has never been saved before."""
        current_truss: TrussWidget = self.current_tab

        # file actions are connected on start page so add check
        if isinstance(current_truss, StartPage):
            return

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
        truss_widget: TrussWidget | StartPage = self.ui.tabWidget.widget(index)

        if isinstance(truss_widget, StartPage):
            self.ui.tabWidget.removeTab(index)
            return

        if len(truss_widget.edits) != 0:
            form = CheckSaveDialog(
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

    def connectTrussSignals(self) -> None:
        self.current_tab.interacted.connect(self.updateInfo)
        self.current_tab.member_added.connect(self.loadMembers)
        self.current_tab.joint_added.connect(self.loadJoints)
        self.current_tab.support_added.connect(self.loadSupports)
        self.current_tab.force_added.connect(self.loadForces)

    def disconnectTrussSignals(self) -> None:
        self.current_tab.interacted.disconnect(self.updateInfo)
        self.current_tab.member_added.disconnect(self.loadMembers)
        self.current_tab.joint_added.disconnect(self.loadJoints)
        self.current_tab.support_added.disconnect(self.loadSupports)
        self.current_tab.force_added.disconnect(self.loadForces)

    def connectTrussButtons(self) -> None:
        self.ui.addJointButton.clicked.connect(self.current_tab.previewJoint)
        self.ui.addMemberButton.clicked.connect(self.current_tab.addMember)
        self.ui.addSupportButton.clicked.connect(self.current_tab.supportForm)
        self.ui.addForceButton.clicked.connect(self.current_tab.forceForm)

        self.ui.zoomInButton.clicked.connect(self.handleZoomIn)
        self.ui.zoomOutButton.clicked.connect(self.handleZoomOut)

    def disconnectTrussButtons(self) -> None:
        self.ui.addJointButton.clicked.disconnect(
            self.current_tab.previewJoint)
        self.ui.addMemberButton.clicked.disconnect(self.current_tab.addMember)
        self.ui.addSupportButton.clicked.disconnect(
            self.current_tab.supportForm)
        self.ui.addForceButton.clicked.disconnect(self.current_tab.forceForm)

        self.ui.zoomInButton.clicked.disconnect(self.handleZoomIn)
        self.ui.zoomOutButton.clicked.disconnect(self.handleZoomOut)

    def handleTabChange(self) -> None:
        """Connects button signals to handler functions."""
        last_tab = self.current_tab
        new_tab: TrussWidget = self.ui.tabWidget.currentWidget()

        if isinstance(last_tab, StartPage):
            self.disconnectFileActions()
        if isinstance(last_tab, TrussWidget):
            self.disconnectActions()
            self.disconnectTrussButtons()
            self.disconnectTrussSignals()

        self.current_tab = new_tab

        if isinstance(new_tab, StartPage):
            self.connectFileActions()
            self.ui.jointInfo.clear()
            self.ui.memberInfo.clear()
            self.ui.forceInfo.clear()
            self.ui.supportInfo.clear()
        if isinstance(new_tab, TrussWidget):
            self.connectActions()
            self.connectTrussButtons()
            self.connectTrussSignals()
            self.updateInfo()

    def updateTrussSelections(self) -> None:
        """Updates selected items on truss scene if item is selected on info tables."""
        self.disconnectInfoSignals()
        self.current_tab.scene().clearSelection()

        for item in self.ui.jointInfo.selectedItems():
            if item.column() == 0:
                truss_graphics_item: JointItem = self.current_tab.connections[int(
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

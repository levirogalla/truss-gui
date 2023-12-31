# Form implementation generated from reading ui file '/Users/levirogalla/Dev/Practice/Projects/truss-gui/src/mainwindow/mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from widgets.contextmenus.startmenu.startpage import StartPage
from PySide6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 611)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.controls = QtWidgets.QWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.controls.sizePolicy().hasHeightForWidth())
        self.controls.setSizePolicy(sizePolicy)
        self.controls.setObjectName("controls")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.controls)
        self.verticalLayout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        self.verticalLayout.setContentsMargins(10, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.editMeshOptions = QtWidgets.QGroupBox(parent=self.controls)
        self.editMeshOptions.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.editMeshOptions.sizePolicy().hasHeightForWidth())
        self.editMeshOptions.setSizePolicy(sizePolicy)
        self.editMeshOptions.setObjectName("editMeshOptions")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.editMeshOptions)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.addJointButton = QtWidgets.QPushButton(
            parent=self.editMeshOptions)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.addJointButton.sizePolicy().hasHeightForWidth())
        self.addJointButton.setSizePolicy(sizePolicy)
        self.addJointButton.setObjectName("addJointButton")
        self.verticalLayout_2.addWidget(self.addJointButton)
        self.addMemberButton = QtWidgets.QPushButton(
            parent=self.editMeshOptions)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.addMemberButton.sizePolicy().hasHeightForWidth())
        self.addMemberButton.setSizePolicy(sizePolicy)
        self.addMemberButton.setMinimumSize(QtCore.QSize(0, 0))
        self.addMemberButton.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight)
        self.addMemberButton.setAutoFillBackground(False)
        self.addMemberButton.setObjectName("addMemberButton")
        self.verticalLayout_2.addWidget(self.addMemberButton)
        self.addForceButton = QtWidgets.QPushButton(
            parent=self.editMeshOptions)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.addForceButton.sizePolicy().hasHeightForWidth())
        self.addForceButton.setSizePolicy(sizePolicy)
        self.addForceButton.setObjectName("addForceButton")
        self.verticalLayout_2.addWidget(self.addForceButton)
        self.addSupportButton = QtWidgets.QPushButton(
            parent=self.editMeshOptions)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.addSupportButton.sizePolicy().hasHeightForWidth())
        self.addSupportButton.setSizePolicy(sizePolicy)
        self.addSupportButton.setObjectName("addSupportButton")
        self.verticalLayout_2.addWidget(self.addSupportButton)
        self.verticalLayout.addWidget(self.editMeshOptions)
        self.horizontalLayout.addWidget(self.controls)
        self.widget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(parent=self.widget_2)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.verticalLayoutWidget)
        self.tabWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.tabWidget.setMouseTracking(True)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.TextElideMode.ElideLeft)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.start = StartPage()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy)
        self.start.setObjectName("start")
        self.tabWidget.addTab(self.start, "")
        self.verticalLayout_5.addWidget(self.tabWidget)
        self.quickData = QtWidgets.QFrame(parent=self.verticalLayoutWidget)
        self.quickData.setAutoFillBackground(False)
        self.quickData.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.quickData.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.quickData.setMidLineWidth(0)
        self.quickData.setObjectName("quickData")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.quickData)
        self.horizontalLayout_2.setContentsMargins(10, 2, 10, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.quickData)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.widget = QtWidgets.QWidget(parent=self.quickData)
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.zoomOutButton = QtWidgets.QPushButton(parent=self.widget)
        self.zoomOutButton.setObjectName("zoomOutButton")
        self.horizontalLayout_3.addWidget(self.zoomOutButton)
        self.zoomInButton = QtWidgets.QPushButton(parent=self.widget)
        self.zoomInButton.setCheckable(False)
        self.zoomInButton.setAutoDefault(False)
        self.zoomInButton.setDefault(False)
        self.zoomInButton.setFlat(False)
        self.zoomInButton.setObjectName("zoomInButton")
        self.horizontalLayout_3.addWidget(self.zoomInButton)
        self.horizontalLayout_2.addWidget(self.widget)
        self.horizontalLayout_2.setStretch(0, 1)
        self.verticalLayout_5.addWidget(self.quickData)
        self.infoWidget = QtWidgets.QWidget(parent=self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.infoWidget.sizePolicy().hasHeightForWidth())
        self.infoWidget.setSizePolicy(sizePolicy)
        self.infoWidget.setObjectName("infoWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.infoWidget)
        self.verticalLayout_4.setContentsMargins(10, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.jointInfo = QtWidgets.QTableWidget(parent=self.infoWidget)
        self.jointInfo.setObjectName("jointInfo")
        self.jointInfo.setColumnCount(4)
        self.jointInfo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(3, item)
        self.verticalLayout_4.addWidget(self.jointInfo)
        self.memberInfo = QtWidgets.QTableWidget(parent=self.infoWidget)
        self.memberInfo.setObjectName("memberInfo")
        self.memberInfo.setColumnCount(5)
        self.memberInfo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(4, item)
        self.verticalLayout_4.addWidget(self.memberInfo)
        self.forceInfo = QtWidgets.QTableWidget(parent=self.infoWidget)
        self.forceInfo.setObjectName("forceInfo")
        self.forceInfo.setColumnCount(5)
        self.forceInfo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(4, item)
        self.verticalLayout_4.addWidget(self.forceInfo)
        self.supportInfo = QtWidgets.QTableWidget(parent=self.infoWidget)
        self.supportInfo.setObjectName("supportInfo")
        self.supportInfo.setColumnCount(6)
        self.supportInfo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(5, item)
        self.verticalLayout_4.addWidget(self.supportInfo)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 37))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOpen_Recent = QtWidgets.QMenu(parent=self.menuFile)
        self.menuOpen_Recent.setObjectName("menuOpen_Recent")
        self.menuEdit = QtWidgets.QMenu(parent=self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuDelete = QtWidgets.QMenu(parent=self.menuEdit)
        self.menuDelete.setObjectName("menuDelete")
        self.menuAdd = QtWidgets.QMenu(parent=self.menuEdit)
        self.menuAdd.setObjectName("menuAdd")
        self.menuJoint = QtWidgets.QMenu(parent=self.menuAdd)
        self.menuJoint.setObjectName("menuJoint")
        self.menuSolve = QtWidgets.QMenu(parent=self.menubar)
        self.menuSolve.setObjectName("menuSolve")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(parent=MainWindow)
        self.actionSave.setEnabled(True)
        self.actionSave.setShortcutVisibleInContextMenu(True)
        self.actionSave.setObjectName("actionSave")
        self.actionedit = QtGui.QAction(parent=MainWindow)
        self.actionedit.setObjectName("actionedit")
        self.actionOpen_Optimizer = QtGui.QAction(parent=MainWindow)
        self.actionOpen_Optimizer.setObjectName("actionOpen_Optimizer")
        self.actionView_in_MPL = QtGui.QAction(parent=MainWindow)
        self.actionView_in_MPL.setObjectName("actionView_in_MPL")
        self.actionNew = QtGui.QAction(parent=MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtGui.QAction(parent=MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_As = QtGui.QAction(parent=MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionSolve_Reactions = QtGui.QAction(parent=MainWindow)
        self.actionSolve_Reactions.setObjectName("actionSolve_Reactions")
        self.actionSolve_Members = QtGui.QAction(parent=MainWindow)
        self.actionSolve_Members.setObjectName("actionSolve_Members")
        self.actionOptimize = QtGui.QAction(parent=MainWindow)
        self.actionOptimize.setObjectName("actionOptimize")
        self.actionTruss_Preferences = QtGui.QAction(parent=MainWindow)
        self.actionTruss_Preferences.setObjectName("actionTruss_Preferences")
        self.actionRedo = QtGui.QAction(parent=MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.actionOpen_Change_Log = QtGui.QAction(parent=MainWindow)
        self.actionOpen_Change_Log.setObjectName("actionOpen_Change_Log")
        self.actionClear_Reactions = QtGui.QAction(parent=MainWindow)
        self.actionClear_Reactions.setObjectName("actionClear_Reactions")
        self.actionClear_Members = QtGui.QAction(parent=MainWindow)
        self.actionClear_Members.setObjectName("actionClear_Members")
        self.actionDelete_Member = QtGui.QAction(parent=MainWindow)
        self.actionDelete_Member.setObjectName("actionDelete_Member")
        self.actionDelete_Force = QtGui.QAction(parent=MainWindow)
        self.actionDelete_Force.setObjectName("actionDelete_Force")
        self.actionJoint = QtGui.QAction(parent=MainWindow)
        self.actionJoint.setObjectName("actionJoint")
        self.actionMember = QtGui.QAction(parent=MainWindow)
        self.actionMember.setObjectName("actionMember")
        self.actionForce = QtGui.QAction(parent=MainWindow)
        self.actionForce.setObjectName("actionForce")
        self.actionSupport = QtGui.QAction(parent=MainWindow)
        self.actionSupport.setObjectName("actionSupport")
        self.actionDelete = QtGui.QAction(parent=MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionStart = QtGui.QAction(parent=MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionGeneral_Settings = QtGui.QAction(parent=MainWindow)
        self.actionGeneral_Settings.setObjectName("actionGeneral_Settings")
        self.actionAddJointDrop = QtGui.QAction(parent=MainWindow)
        self.actionAddJointDrop.setObjectName("actionAddJointDrop")
        self.actionAddJointDialog = QtGui.QAction(parent=MainWindow)
        self.actionAddJointDialog.setObjectName("actionAddJointDialog")
        self.actionAddMember = QtGui.QAction(parent=MainWindow)
        self.actionAddMember.setObjectName("actionAddMember")
        self.actionAddSupport = QtGui.QAction(parent=MainWindow)
        self.actionAddSupport.setObjectName("actionAddSupport")
        self.actionAddForce = QtGui.QAction(parent=MainWindow)
        self.actionAddForce.setObjectName("actionAddForce")
        self.actionZoom_In = QtGui.QAction(parent=MainWindow)
        self.actionZoom_In.setObjectName("actionZoom_In")
        self.actionZoom_Out = QtGui.QAction(parent=MainWindow)
        self.actionZoom_Out.setObjectName("actionZoom_Out")
        self.menuOpen_Recent.addAction(self.actionStart)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuOpen_Recent.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuDelete.addAction(self.actionJoint)
        self.menuDelete.addAction(self.actionMember)
        self.menuDelete.addAction(self.actionForce)
        self.menuDelete.addAction(self.actionSupport)
        self.menuJoint.addAction(self.actionAddJointDrop)
        self.menuJoint.addAction(self.actionAddJointDialog)
        self.menuAdd.addAction(self.menuJoint.menuAction())
        self.menuAdd.addAction(self.actionAddMember)
        self.menuAdd.addAction(self.actionAddSupport)
        self.menuAdd.addAction(self.actionAddForce)
        self.menuEdit.addAction(self.actionedit)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.menuDelete.menuAction())
        self.menuEdit.addAction(self.menuAdd.menuAction())
        self.menuSolve.addAction(self.actionSolve_Reactions)
        self.menuSolve.addAction(self.actionSolve_Members)
        self.menuSolve.addSeparator()
        self.menuSolve.addAction(self.actionClear_Reactions)
        self.menuSolve.addAction(self.actionClear_Members)
        self.menuSolve.addSeparator()
        self.menuSolve.addAction(self.actionOpen_Optimizer)
        self.menuView.addAction(self.actionView_in_MPL)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionTruss_Preferences)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionZoom_In)
        self.menuView.addAction(self.actionZoom_Out)
        self.menuSettings.addAction(self.actionGeneral_Settings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSolve.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.editMeshOptions.setTitle(_translate("MainWindow", "Edit Mesh"))
        self.addJointButton.setText(_translate("MainWindow", "Add Joint"))
        self.addMemberButton.setText(_translate("MainWindow", "Add Member"))
        self.addForceButton.setText(_translate("MainWindow", "Add Force"))
        self.addSupportButton.setText(_translate("MainWindow", "Add Support"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.start), _translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "Truss Maker v0.0.0"))
        self.zoomOutButton.setText(_translate("MainWindow", "-"))
        self.zoomInButton.setText(_translate("MainWindow", "+"))
        item = self.jointInfo.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Joint"))
        item = self.jointInfo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "X"))
        item = self.jointInfo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Y"))
        item = self.jointInfo.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Movable"))
        item = self.memberInfo.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Member"))
        item = self.memberInfo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Joint A"))
        item = self.memberInfo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Joint B"))
        item = self.memberInfo.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Internal Force"))
        item = self.memberInfo.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Force Type"))
        item = self.forceInfo.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Force"))
        item = self.forceInfo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Joint"))
        item = self.forceInfo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "X Component"))
        item = self.forceInfo.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Y Component"))
        item = self.forceInfo.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Type"))
        item = self.supportInfo.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Support"))
        item = self.supportInfo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Joint"))
        item = self.supportInfo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Base"))
        item = self.supportInfo.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "X Reaction"))
        item = self.supportInfo.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Y  Reaction"))
        item = self.supportInfo.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Moment Reaction"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOpen_Recent.setTitle(_translate("MainWindow", "Open Recent"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuDelete.setTitle(_translate("MainWindow", "Manage"))
        self.menuAdd.setTitle(_translate("MainWindow", "Add"))
        self.menuJoint.setTitle(_translate("MainWindow", "Joint"))
        self.menuSolve.setTitle(_translate("MainWindow", "Solve"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionedit.setText(_translate("MainWindow", "Undo"))
        self.actionOpen_Optimizer.setText(
            _translate("MainWindow", "Open Optimizer..."))
        self.actionView_in_MPL.setText(_translate("MainWindow", "View in MPL"))
        self.actionNew.setText(_translate("MainWindow", "New Truss"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..."))
        self.actionSave_As.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+S"))
        self.actionSolve_Reactions.setText(
            _translate("MainWindow", "Solve Reactions"))
        self.actionSolve_Members.setText(
            _translate("MainWindow", "Solve Members"))
        self.actionOptimize.setText(_translate("MainWindow", "Optimize"))
        self.actionTruss_Preferences.setText(
            _translate("MainWindow", "Truss Preferences"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionOpen_Change_Log.setText(
            _translate("MainWindow", "Open Change Log"))
        self.actionClear_Reactions.setText(
            _translate("MainWindow", "Clear Reactions"))
        self.actionClear_Members.setText(
            _translate("MainWindow", "Clear Members"))
        self.actionDelete_Member.setText(
            _translate("MainWindow", "Delete Member..."))
        self.actionDelete_Force.setText(
            _translate("MainWindow", "Delete Force..."))
        self.actionJoint.setText(_translate("MainWindow", "Joints..."))
        self.actionMember.setText(_translate("MainWindow", "Members..."))
        self.actionForce.setText(_translate("MainWindow", "Forces..."))
        self.actionSupport.setText(_translate("MainWindow", "Supports..."))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionGeneral_Settings.setText(
            _translate("MainWindow", "General Settings..."))
        self.actionAddJointDrop.setText(_translate("MainWindow", "Drop"))
        self.actionAddJointDrop.setShortcut(_translate("MainWindow", "Alt+J"))
        self.actionAddJointDialog.setText(
            _translate("MainWindow", "Dialog..."))
        self.actionAddJointDialog.setShortcut(
            _translate("MainWindow", "Alt+Shift+J"))
        self.actionAddMember.setText(_translate("MainWindow", "Member"))
        self.actionAddMember.setShortcut(_translate("MainWindow", "Alt+M"))
        self.actionAddSupport.setText(_translate("MainWindow", "Support"))
        self.actionAddSupport.setShortcut(_translate("MainWindow", "Alt+S"))
        self.actionAddForce.setText(_translate("MainWindow", "Force"))
        self.actionAddForce.setShortcut(_translate("MainWindow", "Alt+F"))
        self.actionZoom_In.setText(_translate("MainWindow", "Zoom In"))
        self.actionZoom_In.setShortcut(_translate("MainWindow", "Ctrl+="))
        self.actionZoom_Out.setText(_translate("MainWindow", "Zoom Out"))
        self.actionZoom_Out.setShortcut(_translate("MainWindow", "Ctrl+-"))

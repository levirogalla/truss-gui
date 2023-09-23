# Form implementation generated from reading ui file '/Users/levirogalla/Dev/Practice/Projects/truss-gui/mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(983, 589)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.controls = QtWidgets.QWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controls.sizePolicy().hasHeightForWidth())
        self.controls.setSizePolicy(sizePolicy)
        self.controls.setObjectName("controls")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.controls)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        self.verticalLayout.setContentsMargins(10, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.editMeshOptions = QtWidgets.QGroupBox(parent=self.controls)
        self.editMeshOptions.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editMeshOptions.sizePolicy().hasHeightForWidth())
        self.editMeshOptions.setSizePolicy(sizePolicy)
        self.editMeshOptions.setObjectName("editMeshOptions")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.editMeshOptions)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.addJointButton = QtWidgets.QPushButton(parent=self.editMeshOptions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addJointButton.sizePolicy().hasHeightForWidth())
        self.addJointButton.setSizePolicy(sizePolicy)
        self.addJointButton.setObjectName("addJointButton")
        self.verticalLayout_2.addWidget(self.addJointButton)
        self.addMemberButton = QtWidgets.QPushButton(parent=self.editMeshOptions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addMemberButton.sizePolicy().hasHeightForWidth())
        self.addMemberButton.setSizePolicy(sizePolicy)
        self.addMemberButton.setMinimumSize(QtCore.QSize(0, 0))
        self.addMemberButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.addMemberButton.setAutoFillBackground(False)
        self.addMemberButton.setObjectName("addMemberButton")
        self.verticalLayout_2.addWidget(self.addMemberButton)
        self.addForceButton = QtWidgets.QPushButton(parent=self.editMeshOptions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addForceButton.sizePolicy().hasHeightForWidth())
        self.addForceButton.setSizePolicy(sizePolicy)
        self.addForceButton.setObjectName("addForceButton")
        self.verticalLayout_2.addWidget(self.addForceButton)
        self.addSupportButton = QtWidgets.QPushButton(parent=self.editMeshOptions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addSupportButton.sizePolicy().hasHeightForWidth())
        self.addSupportButton.setSizePolicy(sizePolicy)
        self.addSupportButton.setObjectName("addSupportButton")
        self.verticalLayout_2.addWidget(self.addSupportButton)
        self.verticalLayout.addWidget(self.editMeshOptions)
        self.horizontalLayout.addWidget(self.controls)
        self.splitter = QtWidgets.QSplitter(parent=self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.splitter)
        self.tabWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.tabWidget.setMouseTracking(True)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.TextElideMode.ElideRight)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.build = TrussWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.build.sizePolicy().hasHeightForWidth())
        self.build.setSizePolicy(sizePolicy)
        self.build.setObjectName("build")
        self.tabWidget.addTab(self.build, "")
        self.optimize = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.optimize.sizePolicy().hasHeightForWidth())
        self.optimize.setSizePolicy(sizePolicy)
        self.optimize.setObjectName("optimize")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.optimize)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget.addTab(self.optimize, "")
        self.infoWidget = QtWidgets.QWidget(parent=self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoWidget.sizePolicy().hasHeightForWidth())
        self.infoWidget.setSizePolicy(sizePolicy)
        self.infoWidget.setObjectName("infoWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.infoWidget)
        self.verticalLayout_4.setContentsMargins(10, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.jointInfo = QtWidgets.QTableWidget(parent=self.infoWidget)
        self.jointInfo.setObjectName("jointInfo")
        self.jointInfo.setColumnCount(3)
        self.jointInfo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(2, item)
        self.verticalLayout_4.addWidget(self.jointInfo)
        self.memberInfo = QtWidgets.QTableWidget(parent=self.infoWidget)
        self.memberInfo.setObjectName("memberInfo")
        self.memberInfo.setColumnCount(3)
        self.memberInfo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(2, item)
        self.verticalLayout_4.addWidget(self.memberInfo)
        self.forceInfo = QtWidgets.QTableWidget(parent=self.infoWidget)
        self.forceInfo.setObjectName("forceInfo")
        self.forceInfo.setColumnCount(4)
        self.forceInfo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(3, item)
        self.verticalLayout_4.addWidget(self.forceInfo)
        self.supportInfo = QtWidgets.QTableWidget(parent=self.infoWidget)
        self.supportInfo.setObjectName("supportInfo")
        self.supportInfo.setColumnCount(3)
        self.supportInfo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(2, item)
        self.verticalLayout_4.addWidget(self.supportInfo)
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 983, 37))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(parent=self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuSolve = QtWidgets.QMenu(parent=self.menubar)
        self.menuSolve.setObjectName("menuSolve")
        self.menuOptimize = QtWidgets.QMenu(parent=self.menubar)
        self.menuOptimize.setObjectName("menuOptimize")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(parent=MainWindow)
        self.actionSave.setEnabled(False)
        self.actionSave.setObjectName("actionSave")
        self.actionedit = QtGui.QAction(parent=MainWindow)
        self.actionedit.setObjectName("actionedit")
        self.actionOpen_setting = QtGui.QAction(parent=MainWindow)
        self.actionOpen_setting.setObjectName("actionOpen_setting")
        self.actionView_in_MPL = QtGui.QAction(parent=MainWindow)
        self.actionView_in_MPL.setObjectName("actionView_in_MPL")
        self.menuFile.addAction(self.actionSave)
        self.menuEdit.addAction(self.actionedit)
        self.menuSolve.addAction(self.actionOpen_setting)
        self.menuView.addAction(self.actionView_in_MPL)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSolve.menuAction())
        self.menubar.addAction(self.menuOptimize.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.build), _translate("MainWindow", "Build"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optimize), _translate("MainWindow", "Metrics"))
        item = self.jointInfo.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Joint"))
        item = self.jointInfo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "X"))
        item = self.jointInfo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Y"))
        item = self.memberInfo.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Member"))
        item = self.memberInfo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Joint A"))
        item = self.memberInfo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Joint B"))
        item = self.forceInfo.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Force"))
        item = self.forceInfo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Joint"))
        item = self.forceInfo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "X Component"))
        item = self.forceInfo.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Y Component"))
        item = self.supportInfo.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Support"))
        item = self.supportInfo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Joint"))
        item = self.supportInfo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Base"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuSolve.setTitle(_translate("MainWindow", "Solve"))
        self.menuOptimize.setTitle(_translate("MainWindow", "Optimize"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionedit.setText(_translate("MainWindow", "edit"))
        self.actionOpen_setting.setText(_translate("MainWindow", "Open setting"))
        self.actionView_in_MPL.setText(_translate("MainWindow", "View in MPL"))
from trusseditor.trusswidget2 import TrussWidget

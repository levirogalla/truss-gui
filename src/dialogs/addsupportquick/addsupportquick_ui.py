# Form implementation generated from reading ui file '/Users/levirogalla/Dev/Practice/Projects/truss-gui/src/dialogs/addsupportquick/addsupportquick.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_AddSupportDialog(object):
    def setupUi(self, AddSupportDialog):
        AddSupportDialog.setObjectName("AddSupportDialog")
        AddSupportDialog.setWindowModality(
            QtCore.Qt.WindowModality.WindowModal)
        AddSupportDialog.resize(202, 92)
        AddSupportDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddSupportDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.supportType = QtWidgets.QComboBox(parent=AddSupportDialog)
        self.supportType.setObjectName("supportType")
        self.supportType.addItem("")
        self.supportType.addItem("")
        self.supportType.addItem("")
        self.verticalLayout.addWidget(self.supportType)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.doneButton = QtWidgets.QPushButton(parent=AddSupportDialog)
        self.doneButton.setObjectName("doneButton")
        self.horizontalLayout.addWidget(self.doneButton)
        self.cancelButton = QtWidgets.QPushButton(parent=AddSupportDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AddSupportDialog)
        QtCore.QMetaObject.connectSlotsByName(AddSupportDialog)

    def retranslateUi(self, AddSupportDialog):
        _translate = QtCore.QCoreApplication.translate
        AddSupportDialog.setWindowTitle(
            _translate("AddSupportDialog", "Add Support"))
        self.supportType.setItemText(
            0, _translate("AddSupportDialog", "Fixed Pin"))
        self.supportType.setItemText(
            1, _translate("AddSupportDialog", "Roller Pin"))
        self.supportType.setItemText(
            2, _translate("AddSupportDialog", "Fixed"))
        self.doneButton.setText(_translate("AddSupportDialog", "Done"))
        self.cancelButton.setText(_translate("AddSupportDialog", "Cancel"))

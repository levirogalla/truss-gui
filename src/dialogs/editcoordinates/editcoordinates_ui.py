# Form implementation generated from reading ui file '/Users/levirogalla/Dev/Practice/Projects/truss-gui/src/dialogs/editcoordinates/editcoordinates.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_EditCoordinatesDialog(object):
    def setupUi(self, EditCoordinatesDialog):
        EditCoordinatesDialog.setObjectName("EditCoordinatesDialog")
        EditCoordinatesDialog.setWindowModality(
            QtCore.Qt.WindowModality.WindowModal)
        EditCoordinatesDialog.resize(204, 164)
        EditCoordinatesDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditCoordinatesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(parent=EditCoordinatesDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.xCoordinate = QtWidgets.QLineEdit(parent=EditCoordinatesDialog)
        self.xCoordinate.setObjectName("xCoordinate")
        self.horizontalLayout_4.addWidget(self.xCoordinate)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=EditCoordinatesDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.yCoordinate = QtWidgets.QLineEdit(parent=EditCoordinatesDialog)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        self.yCoordinate.setFont(font)
        self.yCoordinate.setObjectName("yCoordinate")
        self.horizontalLayout_2.addWidget(self.yCoordinate)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(parent=EditCoordinatesDialog)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.trackGrad = QtWidgets.QComboBox(parent=EditCoordinatesDialog)
        self.trackGrad.setObjectName("trackGrad")
        self.trackGrad.addItem("")
        self.trackGrad.addItem("")
        self.horizontalLayout_3.addWidget(self.trackGrad)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.doneButton = QtWidgets.QPushButton(parent=EditCoordinatesDialog)
        self.doneButton.setObjectName("doneButton")
        self.horizontalLayout.addWidget(self.doneButton)
        self.cancelButton = QtWidgets.QPushButton(parent=EditCoordinatesDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(EditCoordinatesDialog)
        QtCore.QMetaObject.connectSlotsByName(EditCoordinatesDialog)

    def retranslateUi(self, EditCoordinatesDialog):
        _translate = QtCore.QCoreApplication.translate
        EditCoordinatesDialog.setWindowTitle(_translate(
            "EditCoordinatesDialog", "Edit Coordinates"))
        self.label_3.setText(_translate("EditCoordinatesDialog", "X:"))
        self.xCoordinate.setPlaceholderText(
            _translate("EditCoordinatesDialog", "X Coordinate"))
        self.label_2.setText(_translate("EditCoordinatesDialog", "Y:"))
        self.yCoordinate.setPlaceholderText(
            _translate("EditCoordinatesDialog", "Y Coordinate"))
        self.label.setText(_translate("EditCoordinatesDialog", "Track Grad:"))
        self.trackGrad.setItemText(
            0, _translate("EditCoordinatesDialog", "True"))
        self.trackGrad.setItemText(1, _translate(
            "EditCoordinatesDialog", "False"))
        self.doneButton.setText(_translate("EditCoordinatesDialog", "Done"))
        self.cancelButton.setText(_translate(
            "EditCoordinatesDialog", "Cancel"))

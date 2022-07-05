from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_commandScriptGenerator(object):
    def setupUi(self, commandScriptGenerator):
        commandScriptGenerator.setObjectName("commandScriptGenerator")
        commandScriptGenerator.resize(802, 227)
        self.labelStatus = QtWidgets.QLabel(commandScriptGenerator)
        self.labelStatus.setGeometry(QtCore.QRect(20, 160, 761, 61))
        self.labelStatus.setText("")
        self.labelStatus.setObjectName("labelStatus")
        self.pushButtonGenerateScript = QtWidgets.QPushButton(commandScriptGenerator)
        self.pushButtonGenerateScript.setGeometry(QtCore.QRect(320, 110, 161, 31))
        self.pushButtonGenerateScript.setObjectName("pushButtonGenerateScript")
        self.groupBox = QtWidgets.QGroupBox(commandScriptGenerator)
        self.groupBox.setGeometry(QtCore.QRect(9, 20, 781, 71))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.lineEditFilePath = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditFilePath.setGeometry(QtCore.QRect(110, 20, 571, 31))
        self.lineEditFilePath.setObjectName("lineEditFilePath")
        self.pushButtonBrowse = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonBrowse.setGeometry(QtCore.QRect(700, 20, 75, 31))
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 31))
        self.label.setObjectName("label")
        self.groupBox.raise_()
        self.labelStatus.raise_()
        self.pushButtonGenerateScript.raise_()

        self.retranslateUi(commandScriptGenerator)
        QtCore.QMetaObject.connectSlotsByName(commandScriptGenerator)

    def retranslateUi(self, commandScriptGenerator):
        _translate = QtCore.QCoreApplication.translate
        commandScriptGenerator.setWindowTitle(_translate("commandScriptGenerator", "Command Script Generator"))
        self.pushButtonGenerateScript.setText(_translate("commandScriptGenerator", "Generate Script"))
        self.pushButtonBrowse.setText(_translate("commandScriptGenerator", "Browse"))
        self.label.setText(_translate("commandScriptGenerator", "Select Master File"))

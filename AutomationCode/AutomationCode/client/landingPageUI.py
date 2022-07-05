from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_landingPage(object):
    def setupUi(self, landingPage):
        landingPage.setObjectName("landingPage")
        landingPage.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(landingPage)
        self.centralwidget.setObjectName("centralwidget")
        landingPage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(landingPage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuTool = QtWidgets.QMenu(self.menubar)
        self.menuTool.setObjectName("menuTool")
        landingPage.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(landingPage)
        self.statusbar.setObjectName("statusbar")
        landingPage.setStatusBar(self.statusbar)
        self.actionCommand_Script_Generator = QtWidgets.QAction(landingPage)
        self.actionCommand_Script_Generator.setObjectName("actionCommand_Script_Generator")
        self.actionKPI_Alert_Test = QtWidgets.QAction(landingPage)
        self.actionKPI_Alert_Test.setObjectName("actionKPI_Alert_Test")
        self.menuTool.addAction(self.actionCommand_Script_Generator)
        self.menubar.addAction(self.menuTool.menuAction())

        self.retranslateUi(landingPage)
        QtCore.QMetaObject.connectSlotsByName(landingPage)

    def retranslateUi(self, landingPage):
        _translate = QtCore.QCoreApplication.translate
        landingPage.setWindowTitle(_translate("landingPage", "Test Automation"))
        self.menuTool.setTitle(_translate("landingPage", "Tool"))
        self.actionCommand_Script_Generator.setText(_translate("landingPage", "Command Script Generator"))

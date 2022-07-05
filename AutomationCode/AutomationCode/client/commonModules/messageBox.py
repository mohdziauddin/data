from PyQt5 import QtWidgets
class messageBox:
    def __init__(self):
        pass

    def showMessageBox(self, text, title):
        msg = QtWidgets.QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

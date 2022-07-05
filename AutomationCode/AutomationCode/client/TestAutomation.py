import sys
from PyQt5 import QtWidgets
from client import landingPageUI
import traceback
from client.commonModules import messageBox
from client.commandScriptGenerator import commandScriptGeneratorController
try:
    import pyi_splash
except:
    pass

class controller:
    def __init__(self):
        self.messageBox = messageBox.messageBox()        
        self.commandScriptGenerator = commandScriptGeneratorController.commandScriptGenerator()        

    def landingPage(self):
        try:
            self.landingPageWindow = QtWidgets.QMainWindow()
            self.landingPageWindowScreen = landingPageUI.Ui_landingPage()
            self.landingPageWindowScreen.setupUi(self.landingPageWindow)
            self.landingPageWindowScreen.actionCommand_Script_Generator.triggered.connect(
                self.commandScriptGenerator.commandScriptGeneratorWindow)           
            try:
                pyi_splash.update_text('Almost Done...')
                pyi_splash.close()
            except:
                pass
            self.landingPageWindow.show()
        except:
            print(traceback.format_exc())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Controller = controller()
    Controller.landingPage()
    sys.exit(app.exec_())

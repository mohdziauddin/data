import json
import threading
import traceback
from PyQt5 import QtWidgets
from client.commandScriptGenerator import commandScriptGeneratorUI
from client.commonModules.fileHandler import fileHandler
from client.commonModules.messageBox import messageBox
from client.commonModules.genericModule import genericModule
import os
import shutil
import time


class commandScriptGenerator:
    def __init__(self):
        self.fileHandler = fileHandler()
        self.selectedFile = None
        self.messageBox = messageBox()
        self.config = None
        self.path = os.getcwd()
        self.genericModule = genericModule()

    def uiController(self, widget, state):
        try:
            if widget == "all":
                self.commandScriptGeneratorUIScreen.groupBox.setEnabled(state)
                self.commandScriptGeneratorUIScreen.pushButtonGenerateScript.setEnabled(state)
            if widget == "groupBox":
                self.commandScriptGeneratorUIScreen.groupBox.setEnabled(state)
                self.commandScriptGeneratorUIScreen.pushButtonGenerateScript.setEnabled(state)
        except:
            print(traceback.format_exc())

    def changeStatus(self, text):
        try:
            self.commandScriptGeneratorUIScreen.labelStatus.setText(text)
        except:
            print(traceback.format_exc())

    def raiseFileErrors(self, message):
        try:
            self.uiController("all", False)
            self.changeStatus(message)
            self.messageBox.showMessageBox(message, "Error")
        except:
            print(traceback.format_exc())

    def readConfigFile(self):
        try:
            self.path = str(os.getcwd())
            with open(self.path + "/config/commandScriptGenerator.json", encoding="utf-8") as f:
                self.config = json.loads(f.read())

            if "projectNames" not in self.config.keys():
                self.raiseFileErrors(
                    'Project Name Details is missing in "Command Script Generator" config file, Please check '
                    'and try again...')


        except json.decoder.JSONDecodeError:
            self.raiseFileErrors(
                'Project Name Details is missing in "Command Script Generator" config file, Please check '
                'and try again...')

        except FileNotFoundError:
            self.raiseFileErrors(
                '"Command Script Generator" config file is missing, Please check and try again...')
        except:
            print(traceback.format_exc())

    def startGeneratingScript(self):
        try:
            startThread = threading.Thread(target=self.GenerateScript)
            startThread.start()
        except:
            print(traceback.format_exc())

    def validateContent(self, masterContent):
        try:
            self.changeStatus("Validating command master content...")
            configKeys = self.config["projectNames"].keys()
            missingContent = ""
            keys = masterContent[0].keys()
            if "Key" not in keys:
                missingContent += "Key" + ", "
            if "Data Type" not in keys:
                missingContent += "Data Type" + ", "
            if "Type" not in keys:
                missingContent += "Type" + ", "
            for key in configKeys:
                for keyTypes in [key, str(key) + "D", str(key) + "R"]:
                    if keyTypes not in keys:
                        missingContent += keyTypes + ", "
            self.changeStatus("Validating command master content completed...")
            return missingContent
        except:
            return traceback.format_exc()

    def createDirectory(self, path):
        try:
            os.mkdir(path=self.path + path)
        except:
            pass

    def createPreDirectories(self):
        try:
            if os.path.isdir(self.path + "/outputFiles/commadScripts") == True:
                shutil.rmtree(self.path + "/outputFiles/commadScripts", ignore_errors=True)
            self.createDirectory("/outputFiles")
            self.createDirectory("/outputFiles/commadScripts")
            projectNames = self.config["projectNames"]
            for project in projectNames.keys():
                if projectNames[project] == True:
                    self.createDirectory("/outputFiles/commadScripts/" + str(project))
        except:
            print(traceback.format_exc())

    def generateErrors(self, slNO, key, project, result):
        try:
            return {
                "slNo": slNO,
                "key": key,
                "project": project,
                "result": result
            }

        except:
            print(traceback.format_exc())

    def checkDataType(self, dataType):
        try:
            result = None
            dataType = str(dataType).lower()
            if "float" in dataType:
                result = "float"

            elif "int" in dataType:
                result = "int"
            elif "str" in dataType:
                result = "str"

            elif "hex" in dataType:
                result = "hex"
            return result

        except:
            print(traceback.format_exc())
            return None

    def validateRange(self, rangeValues, value):
        try:
            result = []
            state = True
            rangeType = None
            rangeValues = str(rangeValues)
            if "to" in rangeValues.lower():
                result = rangeValues.lower().split("to")
                if len(result) != 2:
                    state = False
                else:
                    rangeType = "range"
            elif "-" in rangeValues:
                result = rangeValues.split("-")
                if len(result) != 2:
                    state = False
                else:
                    rangeType = "range"
            elif "," in rangeValues:
                result = rangeValues.split(",")
                rangeType = "single"
            else:
                try:
                    int(rangeValues)
                    rangeType = "single"
                    result = [rangeValues]
                except:
                    state = False
            # this is for range case with values
            value = str(value).strip()
            if value != "" and value.lower() != "na" and value is not None and value != 'None':
                rangeType += "WithValue"
            return state, result, rangeType
        except:
            return False, [], None

    def validateType(self, rangeValues, dataType):
        try:
            result = True
            for value in rangeValues:
                if dataType == "int" or dataType == "str":
                    int(value)
                elif dataType == "float":
                    float(value)
            return result
        except:
            return False

    def scriptJsonFormatter(self, InputKey, InputValue, ExpectedOutput, DefaultValue):
        try:
            return {"Dependency": None,
                    "TestCases": {"InputKey": InputKey, "InputValue": InputValue,
                                  "ExpectedOutput": ExpectedOutput, "DefaultValue": DefaultValue,
                                  }}
        except:
            print(traceback.format_exc())
            return {}

    def intTypeRangeLogic(self, min, max):
        try:
            mid = int(max / 2)
            preCheck = [min - 1, min, min + 1]
            logic = [
                {"value": min, "ExpectedOutput": "1"},
                {"value": min + 1, "ExpectedOutput": "1"}, ]
            if mid not in preCheck:
                logic.append({"value": mid, "ExpectedOutput": "1"})
            if max - 1 not in preCheck:
                logic.append({"value": max - 1, "ExpectedOutput": "1"})
            if max not in preCheck:
                logic.append({"value": max, "ExpectedOutput": "1"})
            if max + 1 not in preCheck:
                logic.append({"value": max + 1, "ExpectedOutput": "-2"})
            logic.append({"value": min - 1, "ExpectedOutput": "-2"})

            return logic
        except:
            print(traceback.format_exc())
            return []

    def floatTypeRangeLogic(self, min, max):
        try:
            mid = round(float(max / 2), 1)
            preCheck = [round(float(min - 1), 1), round(float(min), 1), round(float(min + 1), 1)]
            logic = [
                {"value": round(float(min), 1), "ExpectedOutput": "1"},
                {"value": round(float(min + 1), 1), "ExpectedOutput": "1"}, ]
            if mid not in preCheck:
                preCheck.append(round(float(mid), 1))
                logic.append({"value": round(float(mid), 1), "ExpectedOutput": "1"})
            if max - 1 not in preCheck:
                preCheck.append(round(float(max - 1), 1))
                logic.append({"value": round(float(max - 1), 1), "ExpectedOutput": "1"})
            if max not in preCheck:
                preCheck.append(round(float(max), 1))
                logic.append({"value": round(float(max), 1), "ExpectedOutput": "1"})
            if max + 1 not in preCheck:
                preCheck.append(round(float(max + 1), 1))
                logic.append({"value": round(float(max + 1), 1), "ExpectedOutput": "-2"})
            logic.append({"value": round(float(min - 1), 1), "ExpectedOutput": "-2"})

            return logic
        except:
            print(traceback.format_exc())
            return []

    def intTypeRangeValueLogic(self, min, max, projectMin, projectMax):
        try:
            # print(min, max, projectMin, projectMax)
            logic = []
            for i in range(min, max + 1):
                logic.append({"value": i, "ExpectedOutput": "1"})
            logic.append({"value": projectMin - 1, "ExpectedOutput": "-2"})
            logic.append({"value": projectMax + 1, "ExpectedOutput": "-2"})
            return logic
        except:
            print(traceback.format_exc())
            return []

    def getporjectValues(self, index, mainKey, masterContent):
        try:
            projectMin = None
            projectMax = None
            for i in range(index, len(masterContent) + 1):
                masterKey = str(masterContent[i]["Key"]).strip()

                if i == index:
                    projectMin = int(str(masterContent[i]["Value"]))
                    print("projectMin:",projectMin)
                if masterKey != mainKey and masterKey != "" and masterKey != 'None' and masterKey != None:
                    if i - 1 == index:
                        projectMin = None
                        projectMax = None
                        break
                    else:
                        projectMax = int(str(masterContent[i - 1]["Value"]))

                if i == len(masterContent) - 1:
                    projectMax = int(str(masterContent[i]["Value"]))
                if projectMax != None:
                    break
            return projectMin, projectMax
        except:
            print(traceback.format_exc())
            return None, None

    def createJsonFile(self, project, mainKey, value, jsonData):
        try:
            folderPath = "/outputFiles/commadScripts/" + str(project) + "/" + str(mainKey)
            self.createDirectory(folderPath)
            rand = self.genericModule.generateRandomNumber()
            fileName = self.path + folderPath + "/" + mainKey + "_" + value + "_" + str(rand) + ".json"
            self.fileHandler.generateJsonFile(jsonData, fileName)
        except:
            print(traceback.format_exc())

    def strTypeRangeLogic(self, min, max):
        try:
            logic = []
            preCheck = []
            mid = int(max / 2)
            if min > 0 and min not in preCheck:
                preCheck.append(min)
                strValue = self.genericModule.generateString(min)
                logic.append({"value": str(strValue), "ExpectedOutput": "1"})
            if min + 1 > 0 and min + 1 not in preCheck:
                preCheck.append(min + 1)
                strValue = self.genericModule.generateString(min + 1)
                logic.append({"value": str(strValue), "ExpectedOutput": "1"})
            if mid > 0 and mid not in preCheck:
                preCheck.append(mid)
                strValue = self.genericModule.generateString(mid)
                logic.append({"value": str(strValue), "ExpectedOutput": "1"})
            if max > 0 and max not in preCheck:
                preCheck.append(max)
                strValue = self.genericModule.generateString(max)
                logic.append({"value": str(strValue), "ExpectedOutput": "1"})
            if max - 1 > 0 and max - 1 not in preCheck:
                preCheck.append(max - 1)
                strValue = self.genericModule.generateString(max - 1)
                logic.append({"value": str(strValue), "ExpectedOutput": "1"})
            if min - 1 > 0 and min - 1 not in preCheck:
                preCheck.append(min - 1)
                strValue = self.genericModule.generateString(min - 1)
                logic.append({"value": str(strValue), "ExpectedOutput": "-2"})
            if max + 1 > 0 and max + 1 not in preCheck:
                preCheck.append(max + 1)
                strValue = self.genericModule.generateString(max + 1)
                logic.append({"value": str(strValue), "ExpectedOutput": "-2"})
            return logic
        except:
            print(traceback.format_exc())
            return []

    def loopScriptGeneration(self, slNo, project, mainKey, default, rangeValues, rangeType, dataType, index,
                             masterContent):
        try:
            error = None
            if dataType == "int":
                if "range" in rangeType:
                    min = int(rangeValues[0])
                    max = int(rangeValues[1])
                    logic = []
                    if rangeType == "rangeWithValue":
                        projectMin, projectMax = self.getporjectValues(index, mainKey, masterContent)
                        if projectMin == None and projectMax == None:
                            error = self.generateErrors(slNo, mainKey, project,
                                                        'Invalid "Range" Value - check value column')
                        else:
                            logic = self.intTypeRangeValueLogic(min, max, projectMin, projectMax)
                    if rangeType == "range":
                        logic = self.intTypeRangeLogic(min, max)
                    for valueOutput in logic:
                        script = self.scriptJsonFormatter(mainKey, str(valueOutput["value"]),
                                                          valueOutput["ExpectedOutput"], default)
                        self.createJsonFile(project, mainKey, str(valueOutput["value"]), script)
                if "single" in rangeType:
                    for value in rangeValues:
                        script = self.scriptJsonFormatter(mainKey, str(value),
                                                          "1", default)
                        self.createJsonFile(project, mainKey, str(value), script)

                    min = int(rangeValues[0])
                    max = int(rangeValues[-1])
                    if rangeType == "singleWithValue":
                        projectMin, projectMax = self.getporjectValues(index, mainKey, masterContent)
                        if projectMin == None and projectMax == None:
                            error = self.generateErrors(slNo, mainKey, project,
                                                        'Invalid "Range" Value - check value column')
                        else:
                            min = projectMin
                            max = projectMax

                    for value in [min - 1, max + 1]:
                        script = self.scriptJsonFormatter(mainKey, str(value),
                                                          "-2", default)
                        self.createJsonFile(project, mainKey, str(value), script)

            elif dataType == "str":
                if "range" in rangeType:
                    min = int(rangeValues[0])
                    max = int(rangeValues[1])
                    logic = []
                    if rangeType == "range":
                        logic = self.strTypeRangeLogic(min, max)
                    for valueOutput in logic:
                        script = self.scriptJsonFormatter(mainKey, str(len(str(valueOutput["value"]))),
                                                          valueOutput["ExpectedOutput"], default)
                        # print(project, script)
                        self.createJsonFile(project, mainKey,str(len(str(valueOutput["value"]))), script)
                if "single" in rangeType:
                    for value in rangeValues:
                        if int(value) > 0:
                            strValue = self.genericModule.generateString(int(value))
                            script = self.scriptJsonFormatter(mainKey, strValue,
                                                              "1", default)
                            self.createJsonFile(project, mainKey, str(len(str(value))), script)

                    min = int(rangeValues[0])
                    max = int(rangeValues[-1])
                    for value in [min - 1, max + 1]:
                        if int(value) > 0:
                            strValue = self.genericModule.generateString(int(value))
                            script = self.scriptJsonFormatter(mainKey, strValue,
                                                              "-2", default)
                            self.createJsonFile(project, mainKey, str(len(str(value))), script)

            elif dataType == "float":
                try:
                    default = str(round(float(default), 1)) + "00000"
                    if "range" in rangeType:
                        min = float(rangeValues[0])
                        max = float(rangeValues[1])
                        logic = []
                        # if rangeType == "rangeWithValue":
                        #     projectMin, projectMax = self.getporjectValues(index, mainKey, masterContent)
                        #     if projectMin == None and projectMax == None:
                        #         error = self.generateErrors(slNo, mainKey, project,
                        #                                     'Invalid "Range" Value - check value column')
                        #     else:
                        #         logic = self.floatTypeRangeValueLogic(min, max, projectMin, projectMax)
                        # if rangeType == "range":
                        logic = self.floatTypeRangeLogic(min, max)
                        for valueOutput in logic:
                            script = self.scriptJsonFormatter(mainKey, str(valueOutput["value"]) + "00000",
                                                              valueOutput["ExpectedOutput"], default)
                            self.createJsonFile(project, mainKey, str(valueOutput["value"]), script)
                    if "single" in rangeType:
                        for value in rangeValues:
                            floatValue = str(round(float(value), 1)) + "00000"
                            script = self.scriptJsonFormatter(mainKey, floatValue,
                                                              "1", default)
                            self.createJsonFile(project, mainKey, str(value), script)

                        min = float(rangeValues[0])
                        max = float(rangeValues[-1])
                        # if rangeType == "singleWithValue":
                        #     projectMin, projectMax = self.getporjectValues(index, mainKey, masterContent)
                        #     if projectMin == None and projectMax == None:
                        #         error = self.generateErrors(slNo, mainKey, project,
                        #                                     'Invalid "Range" Value - check value column')
                        #     else:
                        #         min = projectMin
                        #         max = projectMax
                        for value in [min - 1, max + 1]:
                            floatValue = str(round(float(value), 1)) + "00000"
                            script = self.scriptJsonFormatter(mainKey, floatValue,
                                                              "-2", default)
                            self.createJsonFile(project, mainKey, str(value), script)
                except:
                    error = self.generateErrors(slNo, mainKey, project,
                                                'Invalid Default Value')

            return error
        except:
            print(traceback.format_exc())

    def ruleEngin(self, masterContent):
        try:
            self.createPreDirectories()
            errorLog = []
            for index, content in enumerate(masterContent):
                slNo = content["Sl No"]
                mainKey = content["Key"]
                if mainKey != None:
                    if "config" in str(content["Type"]).lower():
                        dataType = self.checkDataType(content["Data Type"])
                        if dataType != None:
                            projectNames = self.config["projectNames"]
                            for project in projectNames.keys():
                                if projectNames[project] == True:
                                    projectR = str(content[project + "R"]).strip()
                                    projectD = str(content[project + "D"]).strip()
                                    if projectR != "" and projectR.lower() != "na" and projectD != "" and projectD.lower() != "na" and projectR is not None and projectR.lower() != "none" and projectD is not None and projectD.lower() != "none":
                                        state, rangeValues, rangeType = self.validateRange(projectR, content["Value"])
                                        if state == True:
                                            validateType = self.validateType(rangeValues, dataType)
                                            if validateType == True:
                                                self.changeStatus("Generating Script for project - " + str(
                                                    project) + " and Key - " + str(mainKey))
                                                error = self.loopScriptGeneration(slNo, project, mainKey, projectD,
                                                                                  rangeValues,
                                                                                  rangeType, dataType, index,
                                                                                  masterContent)
                                                if error != None:
                                                    errorLog.append(error)
                                            else:
                                                error = self.generateErrors(slNo, mainKey, project,
                                                                            'Invalid "Range" Value')
                                                errorLog.append(error)
                                        else:
                                            error = self.generateErrors(slNo, mainKey, project, 'Invalid "Range" Value')
                                            errorLog.append(error)


                        else:
                            error = self.generateErrors(slNo, mainKey, None, 'Invalid "Data Type"')
                            errorLog.append(error)
                    else:
                        error = self.generateErrors(slNo, mainKey, None, 'Invalid "Type"')
                        errorLog.append(error)
            time.sleep(3)
            self.changeStatus("Almost Done...")
            time.sleep(2)
            self.changeStatus("Completed")
            self.fileHcounterandler.generateExcelFile(errorLog, self.path + "/outputFiles/commadScripts/Failure_Log_" + str(
                self.genericModule.generateRandomNumber()) + ".xlsx")
            self.uiController("groupBox", True)
        except:
            print(traceback.format_exc())

    def GenerateScript(self):
        try:
            if self.selectedFile != None:
                self.uiController("groupBox", False)
                self.changeStatus("Reading command master file...")
                masterContent = self.fileHandler.readExcelFile(self.selectedFile)
                self.changeStatus("Reading command master file completed...")
                missingContent = self.validateContent(masterContent)
                if len(missingContent) > 0:
                    self.uiController("grourepBox", True)
                    self.changeStatus('Following fields missing in command master file - "' + missingContent[
                                                                                              :-2] + '", do correction and try again')
                else:
                    self.ruleEngin(masterContent)

            else:
                self.uiController("groupBox", True)
                self.messageBox.showMessageBox("Select command master file to continue...", "Error")

        except:
            self.uiController("groupBox", True)
            print(traceback.format_exc())

    def browseMasterFile(self):
        try:
            self.selectedFile = self.fileHandler.browseExcelFile()
            self.commandScriptGeneratorUIScreen.lineEditFilePath.setText(self.selectedFile)
        except:
            print(traceback.format_exc())

    def commandScriptGeneratorWindow(self):
        self.commandScriptGeneratorUI = QtWidgets.QDialog()
        self.commandScriptGeneratorUIScreen = commandScriptGeneratorUI.Ui_commandScriptGenerator()
        self.commandScriptGeneratorUIScreen.setupUi(self.commandScriptGeneratorUI)
        self.readConfigFile()
        self.commandScriptGeneratorUIScreen.pushButtonBrowse.clicked.connect(self.browseMasterFile)
        self.commandScriptGeneratorUIScreen.pushButtonGenerateScript.clicked.connect(self.startGeneratingScript)
        self.commandScriptGeneratorUI.exec_()


# cl = commandScriptGenerator()
# # state, result, rangeType = cl.validateRange("1r")
# # print(state, result, rangeType)
#
# result = cl.validateType(["13", "0.1."], "float")
# # print(result)
# re = cl.floatTypeRangeLogic(0.1, 5)
# print(re)

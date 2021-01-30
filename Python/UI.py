# -*- coding: utf-8 -*-

import argparse
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Project import Project
from pythonosc import udp_client


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="10.1.52.82",
                        help="The ip of the OSC server")
    parser.add_argument("--port2", default=12000,
                        help="The port the OSC server is listening on")
    parser.add_argument("--port", type=int, default=7004,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)
client = udp_client.SimpleUDPClient(args.ip, args.port)
global output_text
output_text = ""


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1353, 899)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(460, 40, 91, 61))
        self.pushButton.setStyleSheet("selection-color: rgb(0, 255, 0);\n"
                                      "font: 15pt \"Fixedsys\";\n"
                                      "background-color: rgb(0, 0, 0);\n"
                                      "color: rgb(0, 255, 0);\n"
                                      "border-color: rgb(0, 255, 0);\n"
                                      "selection-background-color: rgb(0, 255, 0);")
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.printButtonPressed)

        self.input = QtWidgets.QLineEdit(self.centralwidget)
        self.input.setGeometry(QtCore.QRect(60, 40, 361, 61))
        self.input.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                 "selection-color: rgb(0, 255, 0);\n"
                                 "color: rgb(0, 255, 0);\n"
                                 "border-color: rgb(0, 255, 0);\n"
                                 "selection-background-color: rgb(0, 255, 0);\n"
                                 "font: 11pt \"Fixedsys\";")
        self.input.setObjectName("input")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(60, 140, 1231, 691))
        self.plainTextEdit.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                         "selection-color: rgb(0, 255, 0);\n"
                                         "color: rgb(0, 255, 0);\n"
                                         "border-color: rgb(0, 255, 0);\n"
                                         "selection-background-color: rgb(0, 255, 0);\n"
                                         "font: 13pt \"Fixedsys\";")
        self.plainTextEdit.setTabChangesFocus(False)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1353, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Generate"))

    def printButtonPressed(self):
        global output_text
        # Generate Haiku
        if (self.input.text() == "") or (self.input.text() is None):
            return

        #output_text += "\n Generating Haiku - please be patient... \n"
        output_text += "\n"
        self.plainTextEdit.setPlainText(output_text)
        client.send_message("/HA/Jackfreesound", self.input.text())

        newProject = Project(self.input.text(), 4, 30)
        output_text = newProject.Haiku.display_haiku() + "\n\n" + output_text
        self.plainTextEdit.setPlainText(output_text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
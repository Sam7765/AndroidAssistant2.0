# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AndroiBot.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_game(object):
    def setupUi(self, Androidio):
        Androidio.setObjectName("Androidio")
        Androidio.resize(692, 498)
        self.centralwidget = QtWidgets.QWidget(Androidio)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 691, 481))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:\\Users\\Shubham\\Desktop\\pics\\backgrunds.gif"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 75, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(74, 0, 71, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 180, 571, 301))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("C:\\Users\\Shubham\\Desktop\\andro00\\robot.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(680, 0, 16, 16))
        self.textBrowser.setAutoFillBackground(True)
        self.textBrowser.setStyleSheet("background-color: rgb(38, 0, 58);")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(680, 0, 16, 16))
        self.textBrowser_2.setAutoFillBackground(True)
        self.textBrowser_2.setStyleSheet("background-color: rgb(44, 10, 62);")
        self.textBrowser_2.setObjectName("textBrowser_2")
        Androidio.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Androidio)
        self.statusbar.setObjectName("statusbar")
        Androidio.setStatusBar(self.statusbar)

        self.retranslateUi(Androidio)
        QtCore.QMetaObject.connectSlotsByName(Androidio)

    def retranslateUi(self, Androidio):
        _translate = QtCore.QCoreApplication.translate
        Androidio.setWindowTitle(_translate("Androidio", "MainWindow"))
        self.pushButton.setText(_translate("Androidio", "Start"))
        self.pushButton_2.setText(_translate("Androidio", "Exist"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Androidio = QtWidgets.QMainWindow()
    ui = Ui_game()
    ui.setupUi(Androidio)
    Androidio.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(633, 351)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.movieNameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.movieNameLineEdit.setGeometry(QtCore.QRect(80, 20, 411, 27))
        self.movieNameLineEdit.setObjectName("movieNameLineEdit")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.nameLabel.setObjectName("nameLabel")
        self.searchPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchPushButton.setGeometry(QtCore.QRect(499, 20, 91, 27))
        self.searchPushButton.setObjectName("searchPushButton")
        self.detailWidget = QtWidgets.QWidget(self.centralwidget)
        self.detailWidget.setGeometry(QtCore.QRect(80, 70, 411, 80))
        self.detailWidget.setObjectName("detailWidget")
        self.imageLabel = QtWidgets.QLabel(self.detailWidget)
        self.imageLabel.setGeometry(QtCore.QRect(10, 10, 61, 61))
        self.imageLabel.setObjectName("imageLabel")
        self.nameLabel_2 = QtWidgets.QLabel(self.detailWidget)
        self.nameLabel_2.setGeometry(QtCore.QRect(90, 30, 311, 19))
        self.nameLabel_2.setObjectName("nameLabel_2")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(610, 0, 16, 351))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.movieNameLineEdit.returnPressed.connect(self.movieNameLineEdit.undo)
        self.searchPushButton.clicked.connect(self.searchPushButton.update)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.nameLabel.setText(_translate("MainWindow", "Name:"))
        self.searchPushButton.setText(_translate("MainWindow", "&Search"))
        self.imageLabel.setText(_translate("MainWindow", "TextLabel"))
        self.nameLabel_2.setText(_translate("MainWindow", "TextLabel"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ali/projects/Series/series.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(656, 434)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.seriesTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.seriesTableWidget.setGeometry(QtCore.QRect(0, 0, 511, 411))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.seriesTableWidget.sizePolicy().hasHeightForWidth())
        self.seriesTableWidget.setSizePolicy(sizePolicy)
        self.seriesTableWidget.setObjectName("seriesTableWidget")
        self.seriesTableWidget.setColumnCount(5)
        self.seriesTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.seriesTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.seriesTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.seriesTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.seriesTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.seriesTableWidget.setHorizontalHeaderItem(4, item)
        self.seriesTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.seriesTableWidget.horizontalHeader().setStretchLastSection(True)
        self.seriesTableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.checkPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkPushButton.setGeometry(QtCore.QRect(540, 80, 93, 29))
        self.checkPushButton.setObjectName("checkPushButton")
        self.editPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.editPushButton.setGeometry(QtCore.QRect(540, 130, 93, 29))
        self.editPushButton.setObjectName("editPushButton")
        self.addPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.addPushButton.setGeometry(QtCore.QRect(540, 180, 93, 29))
        self.addPushButton.setObjectName("addPushButton")
        self.setPhotoPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.setPhotoPushButton.setGeometry(QtCore.QRect(540, 230, 93, 29))
        self.setPhotoPushButton.setObjectName("setPhotoPushButton")
        self.loadPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadPushButton.setGeometry(QtCore.QRect(540, 30, 93, 29))
        self.loadPushButton.setObjectName("loadPushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.addPushButton.clicked.connect(self.addPushButton.hide)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.seriesTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.seriesTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Season"))
        item = self.seriesTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Episode"))
        item = self.seriesTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))
        item = self.seriesTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "result"))
        self.checkPushButton.setText(_translate("MainWindow", "&Check"))
        self.editPushButton.setText(_translate("MainWindow", "&Edit"))
        self.addPushButton.setText(_translate("MainWindow", "&Add"))
        self.setPhotoPushButton.setText(_translate("MainWindow", "&Set Photo"))
        self.loadPushButton.setText(_translate("MainWindow", "&Load"))

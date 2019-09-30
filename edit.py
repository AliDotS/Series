from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(719, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(40, 30, 79, 19))
        self.nameLabel.setObjectName("nameLabel")
        self.directoryLabel = QtWidgets.QLabel(self.centralwidget)
        self.directoryLabel.setGeometry(QtCore.QRect(40, 70, 91, 19))
        self.directoryLabel.setObjectName("directoryLabel")
        self.imdbLabel = QtWidgets.QLabel(self.centralwidget)
        self.imdbLabel.setGeometry(QtCore.QRect(40, 110, 91, 19))
        self.imdbLabel.setObjectName("imdbLabel")
        self.photoLabel = QtWidgets.QLabel(self.centralwidget)
        self.photoLabel.setGeometry(QtCore.QRect(70, 163, 101, 19))
        self.photoLabel.setObjectName("photoLabel")
        self.photoCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.photoCheckBox.setGeometry(QtCore.QRect(40, 159, 16, 25))
        self.photoCheckBox.setText("")
        self.photoCheckBox.setObjectName("photoCheckBox")
        self.photoCheckBox.setChecked(True)
        self.nameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.nameLineEdit.setGeometry(QtCore.QRect(160, 27, 221, 27))
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.directoryLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.directoryLineEdit.setGeometry(QtCore.QRect(160, 67, 481, 27))
        self.directoryLineEdit.setObjectName("directoryLineEdit")
        self.imdbLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.imdbLineEdit.setGeometry(QtCore.QRect(160, 108, 481, 27))
        self.imdbLineEdit.setObjectName("imdbLineEdit")
        self.photoLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.photoLineEdit.setGeometry(QtCore.QRect(170, 157, 471, 27))
        self.photoLineEdit.setObjectName("photoLineEdit")
        self.urlTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.urlTableWidget.setGeometry(QtCore.QRect(40, 200, 641, 192))
        self.urlTableWidget.setObjectName("urlTableWidget")
        self.urlTableWidget.setColumnCount(1)
        self.urlTableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.urlTableWidget.setHorizontalHeaderItem(0, item)
        self.urlTableWidget.horizontalHeader().setStretchLastSection(True)
        self.urlTableWidget.verticalHeader().setStretchLastSection(False)
        self.directoryPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.directoryPushButton.setGeometry(QtCore.QRect(660, 69, 31, 27))
        self.directoryPushButton.setObjectName("directoryPushButton")
        self.imdbPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.imdbPushButton.setGeometry(QtCore.QRect(660, 109, 31, 27))
        self.imdbPushButton.setObjectName("imdbPushButton")
        self.photoPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.photoPushButton.setGeometry(QtCore.QRect(660, 158, 31, 27))
        self.photoPushButton.setObjectName("photoPushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Edit"))
        self.nameLabel.setText(_translate("MainWindow", "Name:"))
        self.directoryLabel.setText(_translate("MainWindow", "Direcotory:"))
        self.imdbLabel.setText(_translate("MainWindow", "Imdb Url:"))
        self.photoLabel.setText(_translate("MainWindow", "Photo Path:"))
        item = self.urlTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Urls"))
        self.directoryPushButton.setText(_translate("MainWindow", "..."))
        self.imdbPushButton.setText(_translate("MainWindow", "..."))
        self.photoPushButton.setText(_translate("MainWindow", "..."))

        self.directoryPushButton.clicked.connect(self.on_directory)
        self.photoPushButton.clicked.connect(self.on_photo)
        self.photoCheckBox.stateChanged['int'].connect(self.on_check_box_changed)
        self.urlTableWidget.itemChanged.connect(self.on_table_item_changed)

    def on_directory(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory()
        if folder != '':
            self.directoryLineEdit.setText(folder)

    def on_photo(self):
        photo = QtWidgets.QFileDialog.getOpenFileName(
            filter="Image files (*.jpg *.png)")
        if photo[0] != 0:
            self.photoLineEdit.setText(photo[0])

    def on_check_box_changed(self):
        self.photoLineEdit.setEnabled(self.photoCheckBox.isChecked())
        self.photoPushButton.setEnabled(self.photoCheckBox.isChecked())

    def on_table_item_changed(self, test):
        rowNum = self.urlTableWidget.rowCount()
        temp_item = self.urlTableWidget.item(rowNum - 1, 0)
        if not temp_item or not temp_item.text().strip():
            return
        self.urlTableWidget.insertRow(rowNum)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

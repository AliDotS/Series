from PyQt5 import QtCore, QtGui, QtWidgets
from urllib.parse import urlparse
from os.path import isdir, isfile
from re import search as reSearch

import seriesServices


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class Ui_MainWindow(object):
    imdb_url = ''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(668, 467)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(20, 60, 65, 21))
        self.nameLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.nameLabel.setObjectName("nameLabel")
        self.directoryLabel = QtWidgets.QLabel(self.centralwidget)
        self.directoryLabel.setGeometry(QtCore.QRect(20, 100, 81, 21))
        self.directoryLabel.setObjectName("directoryLabel")
        self.photoLabel = QtWidgets.QLabel(self.centralwidget)
        self.photoLabel.setGeometry(QtCore.QRect(50, 140, 91, 31))
        self.photoLabel.setObjectName("photoLabel")
        self.photoCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.photoCheckBox.setGeometry(QtCore.QRect(20, 140, 16, 27))
        self.photoCheckBox.setText("")
        self.photoCheckBox.setObjectName("photoCheckBox")
        self.photoCheckBox.setChecked(True)
        self.nameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.nameLineEdit.setGeometry(QtCore.QRect(110, 50, 221, 31))
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.directoryLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.directoryLineEdit.setGeometry(QtCore.QRect(110, 90, 491, 31))
        self.directoryLineEdit.setObjectName("directoryLineEdit")
        self.photoPathLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.photoPathLineEdit.setGeometry(QtCore.QRect(150, 140, 451, 31))
        self.photoPathLineEdit.setObjectName("photoPathLineEdit")
        self.directoryPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.directoryPushButton.setGeometry(QtCore.QRect(620, 90, 31, 29))
        self.directoryPushButton.setObjectName("directoryPushButton")
        self.photoPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.photoPushButton.setGeometry(QtCore.QRect(620, 140, 31, 29))
        self.photoPushButton.setObjectName("photoPushButton")
        self.urlsTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.urlsTableWidget.setGeometry(QtCore.QRect(25, 241, 621, 151))
        self.urlsTableWidget.setObjectName("urlsTableWidget")
        self.urlsTableWidget.setColumnCount(1)
        self.urlsTableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.urlsTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.urlsTableWidget.setHorizontalHeaderItem(0, item)
        self.urlsTableWidget.horizontalHeader().setStretchLastSection(True)
        self.addPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.addPushButton.setGeometry(QtCore.QRect(300, 410, 86, 29))
        self.addPushButton.setObjectName("addPushButton")
        self.searchPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchPushButton.setGeometry(QtCore.QRect(550, 190, 100, 31))
        self.searchPushButton.setObjectName("searchPushButton")
        self.imdbLabel = QtWidgets.QLabel(self.centralwidget)
        self.imdbLabel.setGeometry(QtCore.QRect(28, 190, 71, 31))
        self.imdbLabel.setObjectName("imdbLabel")
        self.imdbLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.imdbLineEdit.setGeometry(QtCore.QRect(110, 190, 421, 31))
        self.imdbLineEdit.setObjectName("imdbLineEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.photoCheckBox.stateChanged['int'].connect(self.on_check_box_changed)
        self.addPushButton.clicked.connect(self.on_add_button)
        self.directoryPushButton.clicked.connect(self.on_directory)
        self.photoPushButton.clicked.connect(self.on_photo)
        self.urlsTableWidget.itemChanged.connect(self.on_table_item_changed)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.nameLineEdit, self.directoryLineEdit)
        MainWindow.setTabOrder(self.directoryLineEdit, self.directoryPushButton)
        MainWindow.setTabOrder(self.directoryPushButton, self.photoCheckBox)
        MainWindow.setTabOrder(self.photoCheckBox, self.photoPathLineEdit)
        MainWindow.setTabOrder(self.photoPathLineEdit, self.photoPushButton)
        MainWindow.setTabOrder(self.photoPushButton, self.urlsTableWidget)
        MainWindow.setTabOrder(self.urlsTableWidget, self.addPushButton)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Add"))
        self.nameLabel.setText(_translate("MainWindow", "Name:"))
        self.directoryLabel.setText(_translate("MainWindow", "Directory:"))
        self.photoLabel.setText(_translate("MainWindow", "Photo Path:"))
        self.directoryPushButton.setText(_translate("MainWindow", "..."))
        self.photoPushButton.setText(_translate("MainWindow", "..."))
        item = self.urlsTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Url"))
        self.addPushButton.setText(_translate("MainWindow", "&Add"))
        self.searchPushButton.setText(_translate("MainWindow", "&Search"))
        self.imdbLabel.setText(_translate("MainWindow", "Imdb Url:"))

    def on_table_item_changed(self, test):
        rowNum = self.urlsTableWidget.rowCount()
        temp_item = self.urlsTableWidget.item(rowNum - 1, 0)
        if not temp_item or not temp_item.text().strip():
            return
        self.urlsTableWidget.insertRow(rowNum)

    def on_check_box_changed(self):
        self.photoPathLineEdit.setEnabled(self.photoCheckBox.isChecked())
        self.photoPushButton.setEnabled(self.photoCheckBox.isChecked())

    def on_add_button(self):
        if self.validate_form():
            self.create_series()

    def on_directory(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory()
        if folder != '':
            self.directoryLineEdit.setText(folder)

    def on_photo(self):
        photo = QtWidgets.QFileDialog.getOpenFileName(
            filter="Image files (*.jpg *.png)")
        if photo[0] != 0:
            self.photoPathLineEdit.setText(photo[0])

    def validate_form(self):
        directory = self.directoryLineEdit.text()
        photo = self.photoPathLineEdit.text()
        name = self.nameLineEdit.text()
        imdb_url = ''
        urls = []
        for row in range(self.urlsTableWidget.rowCount() - 1):
            urls.append(self.urlsTableWidget.item(row, 0).text())

        error = ""
        if not isdir(directory):
            error += "Unvalid directory\n"
        if self.photoCheckBox.isChecked() and not isfile(photo):
            error += "Unvalid photo\n"
        if not name or name == "":
            error += "Unvalid name\n"
        if not is_url(imdb_url) or\
                not reSearch("^(http[s]?://)?(www.)?imdb.com", imdb_url):
            error += "Unvalid imdb url\n"
        for index, url in enumerate(urls):
            if not is_url(url):
                error += f"Unvalid url {index + 1}\n"
        if error:
            print(error)
            return False
        return True

    def validate_urls(self):
        for url in range(self.urlsTableWidget.rowCount() - 1):
            if not is_url(url):
                return False
        return True

    def create_series(self):
        name = self.nameLineEdit.text()
        directory = self.directoryLineEdit.text()
        imdb_url = ''
        photo = self.photoPathLineEdit.text()
        urls = []
        for row in range(self.urlsTableWidget.rowCount() - 1):
            urls.append(self.urlsTableWidget.item(row, 0).text())

        seriesServices.createSeries(name, imdb_url, directory, urls)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

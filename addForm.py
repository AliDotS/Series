from PyQt5 import QtCore, QtGui, QtWidgets
from urllib.parse import urlparse
from os.path import isdir, isfile
from re import search as reSearch

from search import Ui_MainWindow as searchUI
import seriesServices


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class Ui_MainWindow(object):
    imdb_id = ''
    adding = True
    oldName = ''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(668, 467)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(20, 60, 65, 21))
        self.nameLabel.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
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
        self.photoCheckBox.setChecked(False)
        self.nameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.nameLineEdit.setGeometry(QtCore.QRect(110, 50, 221, 31))
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.directoryLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.directoryLineEdit.setGeometry(QtCore.QRect(110, 90, 491, 31))
        self.directoryLineEdit.setObjectName("directoryLineEdit")
        self.photoPathLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.photoPathLineEdit.setGeometry(QtCore.QRect(150, 140, 451, 31))
        self.photoPathLineEdit.setObjectName("photoPathLineEdit")
        self.photoPathLineEdit.setEnabled(False)
        self.directoryPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.directoryPushButton.setGeometry(QtCore.QRect(620, 90, 31, 29))
        self.directoryPushButton.setObjectName("directoryPushButton")
        self.photoPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.photoPushButton.setGeometry(QtCore.QRect(620, 140, 31, 29))
        self.photoPushButton.setObjectName("photoPushButton")
        self.photoPushButton.setEnabled(False)
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
        self.searchPushButton.setGeometry(QtCore.QRect(480, 191, 100, 31))
        self.searchPushButton.setObjectName("searchPushButton")
        self.imdbLabel = QtWidgets.QLabel(self.centralwidget)
        self.imdbLabel.setGeometry(QtCore.QRect(28, 190, 71, 31))
        self.imdbLabel.setObjectName("imdbLabel")
        self.imdbLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.imdbLineEdit.setGeometry(QtCore.QRect(110, 190, 141, 31))
        self.imdbLineEdit.setObjectName("imdbLineEdit")
        self.seasonLabel = QtWidgets.QLabel(self.centralwidget)
        self.seasonLabel.setGeometry(QtCore.QRect(270, 198, 79, 19))
        self.seasonLabel.setObjectName("seasonLabel")
        self.seasonSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.seasonSpinBox.setGeometry(QtCore.QRect(350, 193, 53, 28))
        self.seasonSpinBox.setMinimum(1)
        self.seasonSpinBox.setObjectName("seasonSpinBox")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.photoCheckBox.stateChanged['int'].connect(
            self.on_check_box_changed)
        self.addPushButton.clicked.connect(self.on_add_button)
        self.directoryPushButton.clicked.connect(self.on_directory)
        self.photoPushButton.clicked.connect(self.on_photo)
        self.urlsTableWidget.itemChanged.connect(self.on_table_item_changed)
        self.searchPushButton.clicked.connect(self.on_search)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.nameLineEdit, self.directoryLineEdit)
        MainWindow.setTabOrder(self.directoryLineEdit,
                               self.directoryPushButton)
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
        self.imdbLabel.setText(_translate("MainWindow", "Imdb Id:"))
        self.seasonLabel.setText(_translate("MainWindow", "Season:"))

    def on_table_item_changed(self, test):
        rowNum = self.urlsTableWidget.rowCount()
        temp_item = self.urlsTableWidget.item(rowNum - 1, 0)

        if rowNum == 1 and (temp_item is None or not temp_item.text().strip()):
            return

        for index in reversed(range(rowNum - 1)):
            temp_row = self.urlsTableWidget.item(index, 0)
            if temp_row is None or not temp_row.text().strip():
                self.urlsTableWidget.removeRow(index)

        rowNum = self.urlsTableWidget.rowCount()
        temp_item = self.urlsTableWidget.item(rowNum - 1, 0)

        if temp_item and temp_item.text().strip():
            self.urlsTableWidget.insertRow(rowNum)

    def on_check_box_changed(self):
        self.photoPathLineEdit.setEnabled(self.photoCheckBox.isChecked())
        self.photoPushButton.setEnabled(self.photoCheckBox.isChecked())

    def on_add_button(self):
        if self.validate_form():
            if self.adding:
                self.create_series()
            else:
                urls = []
                for num in range(self.urlsTableWidget.rowCount() - 1):
                    urls.append(self.urlsTableWidget.item(num, 0).text())
                seriesServices.updateSeries(self.oldName, self.nameLineEdit.text(), self.imdbLineEdit.text(
                ), self.seasonSpinBox.value(), self.directoryLineEdit.text(), self.photoPathLineEdit.text(), urls)
        self.centralwidget.parent().close()

    def on_directory(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory()
        if folder != '':
            self.directoryLineEdit.setText(folder)

    def on_photo(self):
        photo = QtWidgets.QFileDialog.getOpenFileName(
            filter="Image files (*.jpg *.png)")
        if photo[0] != 0:
            self.photoPathLineEdit.setText(photo[0])

    def on_search(self):
        self.sMain = QtWidgets.QMainWindow()
        self.sUI = searchUI()
        self.sUI.perName = self.nameLineEdit.text()
        self.sUI.setupUi(self.sMain)
        self.sUI.set_imdb = self.set_imdb_url
        self.sMain.show()

    def set_imdb_url(self, imdb_id: str, season: int):
        self.seasonSpinBox.setValue(season)
        self.imdbLineEdit.setText(imdb_id)

    def validate_form(self):
        directory = self.directoryLineEdit.text()
        photo = self.photoPathLineEdit.text()
        name = self.nameLineEdit.text()
        imdb_id = self.imdbLineEdit.text()
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
        if not reSearch(r'tt\d+', imdb_id):
            error += "Unvalid imdb id\n"
        for index, url in enumerate(urls):
            if not is_url(url):
                error += f"Unvalid url {index + 1}\n"
        if error:
            print(error)
            return False
        return True

    def create_series(self):
        name = self.nameLineEdit.text()
        directory = self.directoryLineEdit.text()
        imdb_id = self.imdbLineEdit.text()
        season = self.seasonSpinBox.value()
        photo = self.photoPathLineEdit.text()
        urls = []
        for row in range(self.urlsTableWidget.rowCount() - 1):
            urls.append(self.urlsTableWidget.item(row, 0).text())

        seriesServices.createSeries(name, imdb_id, season, directory, urls, photo)
        self.centralwidget.parent().close()

    def setup_edit(self, name, directory, imdb_id, season, photo, urls):
        self.nameLineEdit.setText(name)
        self.oldName = name
        self.directoryLineEdit.setText(directory)
        self.imdbLineEdit.setText(imdb_id)
        self.seasonSpinBox.setValue(season)
        if photo:
            self.photoPathLineEdit.setText(photo)
            self.addPushButton.setEnabled(True)
            self.photoCheckBox.setChecked(True)
            self.photoPathLineEdit.setEnabled(True)
        for index, url in enumerate(urls):
            if index != 0:
                self.urlsTableWidget.insertRow(index)
            item = QtWidgets.QTableWidgetItem(url)
            self.urlsTableWidget.setItem(index, 0, item)
        self.addPushButton.setText("&Edit")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.setup_edit('titans', 'testd', 'testi', 'testp', ['hello1', 'hello2'])
    sys.exit(app.exec_())

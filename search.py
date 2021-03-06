from urllib.request import urlopen, Request
from tempfile import NamedTemporaryFile

from PyQt5 import QtCore, QtGui, QtWidgets

import seriesServices


class myLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.mousePressEvent = self.on_clicked
        self.set_imdb = lambda self, x : x+'hello'

    def enterEvent(self, QEvent):
        self.setStyleSheet("background-color : #fff")

    def leaveEvent(self, QEvent):
        self.setStyleSheet("background-color : transparent")

    def on_clicked(self, event):
        self.parent().imdb_id = self.imdb_id
        self.parent().on_close()


class Ui_MainWindow(object):
    rownum = 0
    imdb_id = ''
    perName = ''
    set_imdb = lambda x: x
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 361)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.nameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.nameLineEdit.setText(self.perName)
        self.gridLayout.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.searchPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchPushButton.setObjectName("searchPpushButton")
        self.gridLayout.addWidget(self.searchPushButton, 0, 2, 1, 1)
        self.groupBox = QtWidgets.QGroupBox()
        self.groupBox.on_close = self.on_close
        self.groupLayout = QtWidgets.QFormLayout()
        self.groupBox.setLayout(self.groupLayout)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidget(self.groupBox)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Search"))
        self.label.setText(_translate("MainWindow", "name:"))
        self.searchPushButton.setText(_translate("MainWindow", "&Search"))
        self.nameLineEdit.returnPressed.connect(self.search_name)
        self.searchPushButton.clicked.connect(self.search_name)

    def search_name(self):
        self.searchPushButton.setEnabled(False)
        self.nameLineEdit.setEnabled(False)
        self.searchPushButton.setText('searching...')
        QtWidgets.QApplication.processEvents()
        self.clear_results()
        print(f'getting {self.nameLineEdit.text()}')
        results = seriesServices.search(self.nameLineEdit.text())
        print(results)
        for result in results:
            image = QtWidgets.QLabel()
            image.setScaledContents(True)
            self.downloadfile(image, result.img)
            name = myLabel(result.name)
            name.imdb_id = result.imdb_id
            name.set_imdb = self.set_imdb
            self.groupLayout.addRow(image, name)
            QtWidgets.QApplication.processEvents()
        self.searchPushButton.setEnabled(True)
        self.nameLineEdit.setEnabled(True)
        self.searchPushButton.setText('&Search')

    def downloadfile(self, label, link, retry=0):
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            request = urlopen(req, timeout=10)

            with NamedTemporaryFile() as f:
                f.write(request.read())
                f.flush()
                label.setPixmap(QtGui.QPixmap(f.name))
        except:
            if retry > 15:
                return 1
            return self.downloadfile(label, link, retry + 1)

        return 0

    def clear_results(self):
        if self.groupLayout.count() == 0:
            return
        for index in reversed(range(self.groupLayout.count())):
            self.groupLayout.itemAt(index).widget().setParent(None)

    def on_close(self):
        self.centralwidget.parent().hide()
        self.set_imdb(self.groupBox.imdb_id, seriesServices.get_season(self.groupBox.imdb_id))
        self.centralwidget.parent().close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

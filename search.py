from urllib.request import urlopen, Request
from tempfile import NamedTemporaryFile

from PyQt5 import QtCore, QtGui, QtWidgets

import seriesServices


class Ui_MainWindow(object):
    rownum = 0

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
        self.gridLayout.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.searchPpushButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchPpushButton.setObjectName("searchPpushButton")
        self.gridLayout.addWidget(self.searchPpushButton, 0, 2, 1, 1)
        self.groupBox = QtWidgets.QGroupBox()
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
        self.searchPpushButton.setText(_translate("MainWindow", "&Search"))
        self.nameLineEdit.returnPressed.connect(self.search_name)

    def search_name(self):
        print(f'getting {self.nameLineEdit.text()}')
        results = seriesServices.search(self.nameLineEdit.text())
        print(results)
        for result in results:
            image = QtWidgets.QLabel()
            image.setFixedHeight(120)
            self.downloadfile(image, result.img)
            name = QtWidgets.QLabel(result.name)
            self.groupLayout.addRow(image, name)
            QtWidgets.QApplication.processEvents()

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

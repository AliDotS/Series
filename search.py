from urllib.request import urlopen, Request
from tempfile import NamedTemporaryFile

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.imgHeight = 70
        self.nameHeight = 90
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(601, 351)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks |
                                  QtWidgets.QMainWindow.AllowTabbedDocks | QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QScrollArea(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.centralwidget.setWidgetResizable(True)
        self.movieNameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.movieNameLineEdit.setGeometry(QtCore.QRect(80, 20, 411, 27))
        self.movieNameLineEdit.setObjectName("movieNameLineEdit")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.nameLabel.setObjectName("nameLabel")
        self.searchPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchPushButton.setGeometry(QtCore.QRect(499, 20, 91, 27))
        self.searchPushButton.setObjectName("searchPushButton")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(80, 70, 61, 61))
        self.imageLabel.setObjectName("imageLabel")
        self.nameLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel_2.setGeometry(QtCore.QRect(160, 90, 311, 19))
        self.nameLabel_2.setObjectName("nameLabel_2")
        # self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.resize(601, 351)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.movieNameLineEdit.returnPressed.connect(self.search_name)
        self.searchPushButton.clicked.connect(self.search_name)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.nameLabel.setText(_translate("MainWindow", "Name:"))
        self.searchPushButton.setText(_translate("MainWindow", "&Search"))
        self.imageLabel.setText(_translate("MainWindow", "TextLabel"))
        self.nameLabel_2.setText(_translate("MainWindow", "TextLabel"))

    def search_name(self):
        self.imgHeight += 65
        tempw = QtWidgets.QLabel(self.centralwidget)
        tempw.setGeometry(80, self.imgHeight, 61, 61)
        tempw.setText('tempw')
        tempw.show()

        self.nameHeight += 65
        tempw2 = QtWidgets.QLabel(self.centralwidget)
        tempw2.setGeometry(160, self.nameHeight, 311, 19)
        tempw2.setText('tempw2')
        tempw2.show()

    def downloadfile(self, link, retry=0):
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            request = urlopen(req, timeout=10)

            with NamedTemporaryFile() as f:
                f.write(request.read())
                self.imageLabel.setPixmap(QtGui.QPixmap(f.name))
        except:
            if retry > 15:
                return 1
            return self.downloadfile(link, retry + 1)

        return 0


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

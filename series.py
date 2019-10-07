from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QColor
import addForm
import seriesServices

class Ui_MainWindow(object):
    status = ''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(602, 423)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.seriesTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.seriesTableWidget.setGeometry(QtCore.QRect(0, 0, 441, 401))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.seriesTableWidget.sizePolicy().hasHeightForWidth())
        self.seriesTableWidget.setSizePolicy(sizePolicy)
        self.seriesTableWidget.setObjectName("seriesTableWidget")
        self.seriesTableWidget.setColumnCount(4)
        self.seriesTableWidget.setRowCount(0)
        self.seriesTableWidget.setSelectionMode(Qt.QAbstractItemView.SingleSelection)
        self.seriesTableWidget.setSelectionBehavior(Qt.QAbstractItemView.SelectRows)
        item = QtWidgets.QTableWidgetItem()
        self.seriesTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.seriesTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.seriesTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.seriesTableWidget.setHorizontalHeaderItem(3, item)
        self.seriesTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.seriesTableWidget.horizontalHeader().setStretchLastSection(True)
        self.seriesTableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.checkPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkPushButton.setGeometry(QtCore.QRect(470, 70, 93, 29))
        self.checkPushButton.setObjectName("checkPushButton")
        self.editPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.editPushButton.setGeometry(QtCore.QRect(470, 120, 93, 29))
        self.editPushButton.setObjectName("editPushButton")
        self.addPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.addPushButton.setGeometry(QtCore.QRect(470, 170, 93, 29))
        self.addPushButton.setObjectName("addPushButton")
        self.updatePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.updatePushButton.setGeometry(QtCore.QRect(470, 220, 93, 29))
        self.updatePushButton.setObjectName("updatePushButton")
        self.loadPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadPushButton.setGeometry(QtCore.QRect(470, 20, 93, 29))
        self.loadPushButton.setObjectName("loadPushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.checkPushButton.clicked.connect(self.checkSeries)
        self.addPushButton.clicked.connect(self.addWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.on_load()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tv Series"))
        item = self.seriesTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.seriesTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Season"))
        item = self.seriesTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Episode"))
        item = self.seriesTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))
        self.checkPushButton.setText(_translate("MainWindow", "&Check"))
        self.editPushButton.setText(_translate("MainWindow", "&Edit"))
        self.addPushButton.setText(_translate("MainWindow", "&Add"))
        self.updatePushButton.setText(_translate("MainWindow", "&Update"))
        self.loadPushButton.setText(_translate("MainWindow", "&Load"))


        self.editPushButton.clicked.connect(self.on_edit)
        self.updatePushButton.clicked.connect(self.on_update)
        self.loadPushButton.clicked.connect(self.on_load)

    def on_load(self):
        self.status = 'loading'
        try:
            self.seriesTableWidget.setRowCount(0)
            for series in seriesServices.getSeries():
                position = self.seriesTableWidget.rowCount()
                self.seriesTableWidget.insertRow(position)
                self.seriesTableWidget.setItem(position, 0, QtWidgets.QTableWidgetItem(series['name']))
                self.seriesTableWidget.setItem(position, 1, QtWidgets.QTableWidgetItem(series['season']))
                self.seriesTableWidget.setItem(position, 2, QtWidgets.QTableWidgetItem(series['episode']))
        except Exception:
            self.loadPushButton.setStyleSheet('background-color: red')
            return False
        self.loadPushButton.setStyleSheet('background-color: normal')
        return True

    def checkSeries(self):
        print("Checking...")
        for index, series in enumerate(seriesServices.getSeries()):
            results = seriesServices.checkOut(series['name'])
            brush = Qt.QBrush()
            if results:
                item = QtWidgets.QTableWidgetItem('OUT')
                brush.setColor(QColor(0, 255, 0))
            else:
                item = QtWidgets.QTableWidgetItem('not out')
                brush.setColor(QColor(255, 0, 0))
            item.setForeground(brush)
            self.seriesTableWidget.setItem(index, 3, item)
            QtWidgets.QApplication.processEvents()
        print('finished')

    def addWindow(self):
        self.addf = QtWidgets.QMainWindow()
        self.add = addForm.Ui_MainWindow()
        self.add.setupUi(self.addf)
        self.addf.show()

    def editWindow(self, data):
        self.eMain = QtWidgets.QMainWindow()
        self.eUI = addForm.Ui_MainWindow()
        self.eUI.setupUi(self.eMain)
        self.eUI.adding = False
        self.eUI.setup_edit(data['name'], data['directory'], data['imdbUrl'], data['photo'], data['urls'])
        self.eMain.show()

    def on_edit(self):
        item = self.seriesTableWidget.selectedItems()
        if not item:
            return
        seriesData = seriesServices.getSeriesSingle(item[0].text())
        if seriesData is None:
            return
        self.editWindow(seriesData)

    def on_update(self):
        self.updatePushButton.setText('updating...')
        self.updatePushButton.setEnabled(False)
        Qt.QApplication.processEvents()
        for index, series in enumerate(seriesServices.getSeries()):
            result = seriesServices.getData(series['name'])
            brush = Qt.QBrush()
            if result:
                item = QtWidgets.QTableWidgetItem("updated")
                brush.setColor(QColor(0, 200, 0))
            else:
                item = QtWidgets.QTableWidgetItem("update failed")
                brush.setColor(QColor(200, 0, 0))
            item.setForeground(brush)
            self.seriesTableWidget.setItem(index, 3, item)
        self.updatePushButton.setText('&Update')
        self.updatePushButton.setEnabled(True)
        Qt.QApplication.processEvents()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

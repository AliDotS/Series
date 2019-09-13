import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets, Qt
from PyQt5.QtGui import QColor

import seriesServices
import addForm

qtCreatorFile = "series.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.checkPushButton.clicked.connect(self.checkSeries)
        self.addPushButton.clicked.connect(self.addWindow)

        for series in seriesServices.getSeries():
            position = self.seriesTableWidget.rowCount()
            self.seriesTableWidget.insertRow(position)
            self.seriesTableWidget.setItem(
                position, 0, QtWidgets.QTableWidgetItem(series['name']))
            self.seriesTableWidget.setItem(
                position, 1, QtWidgets.QTableWidgetItem(series['season']))
            self.seriesTableWidget.setItem(
                position, 2, QtWidgets.QTableWidgetItem(series['episode']))

    def checkSeries(self):
        print("Checking...")
        for index, series in enumerate(seriesServices.getSeries()):
            brush = Qt.QBrush()
            item = QtWidgets.QTableWidgetItem('checking')
            brush.setColor(QColor(200, 200, 0))
            item.setForeground(brush)
            self.seriesTableWidget.setItem(index, 3, item)
            QtWidgets.QApplication.processEvents()

            results = seriesServices.checkOut(series['name'])
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
        self.add_from_window = QtWidgets.QMainWindow()
        self.add_from_ui = addForm.Ui_MainWindow()
        self.add_from_ui.setupUi(self.add_from_window)
        self.add_from_window.show()



def window_generator(filename):
    pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

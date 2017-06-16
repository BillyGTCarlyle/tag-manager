import sys
import pandas as pd
import csv
from PyQt4 import QtCore, QtGui

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("SheepScan")
        #exit action
        extractAction = QtGui.QAction("&Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Exit the app')
        extractAction.triggered.connect(QtCore.QCoreApplication.instance().quit)
        #new action
        newAction = QtGui.QAction("&New", self)
        newAction.setShortcut("Ctrl+N")
        newAction.setStatusTip('Create a new spreadsheet') 
        #save action
        saveAction = QtGui.QAction("&Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip('Save current spreadsheet')
        #open action
        openAction = QtGui.QAction("&Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip('Open an existing spreadsheet') 
        #import action
        importAction = QtGui.QAction("&Import", self)
        importAction.setShortcut("Ctrl+I")
        importAction.setStatusTip('Import from I-Read device')
        importAction.triggered.connect(self.pushImportAction)
        #search action
        searchAction = QtGui.QAction("&Search", self)
        searchAction.setShortcut("Ctrl+F")
        searchAction.setStatusTip('Search for a tag number')
        #change rowCounr action
        rowCountAction = QtGui.QAction("&Change row count", self)
        rowCountAction.setShortcut("Ctrl+R")
        rowCountAction.setStatusTip('Change number of rows in table')
        #build menu
        self.statusBar()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File') 
        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(importAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(extractAction)
        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(searchAction)
        editMenu.addAction(rowCountAction)
        self.Table()

    def loadCsv(self, fileName):
        data = dataFormatter(fileName)
        n = 0
        for entry in data:
            print(entry)
            newItem = QtGui.QTableWidgetItem(entry)
            self.table.setItem(n, 0, newItem)
            n += 1
            

    @QtCore.pyqtSlot()
    def pushImportAction(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '/home/')
        self.loadCsv(fileName)

    def Table(self):
        
        self.rowCount = 2048
        self.table = QtGui.QTableWidget()
        self.setCentralWidget(self.table)
        self.headers = ['Type', 'Number']
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setRowCount(self.rowCount)
        self.table.setColumnCount(2)
        self.show()

class dataFormatter(object):
    def __init__(self, filename):
        self._filename = filename
        self._handle = None

    def _open(self):
        if not self._handle:
            self._handle = open(self._filename, 'r')

    def __iter__(self): 
        self._open()
        return self

    def __next__(self):
        self._open()
        data = self._handle.readline().strip()
        if data == '':
            raise StopIteration
        else:
            data = data.split()
            return data[4]

def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

main()

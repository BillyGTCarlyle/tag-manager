import sys
import csv
import webbrowser
from PyQt4 import QtCore, QtGui

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("SheepScan")
        #undo stack
        # self.undoStack = QUndoStack(self)
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
        saveAction.triggered.connect(self.pushSaveAction)
        #open action
        openAction = QtGui.QAction("&Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip('Open an existing spreadsheet') 
        openAction.triggered.connect(self.pushOpenAction)
        #import action
        importAction = QtGui.QAction("&Import", self)
        importAction.setShortcut("Ctrl+I")
        importAction.setStatusTip('Import from I-Read device')
        importAction.triggered.connect(self.pushImportAction)
        #search action
        searchAction = QtGui.QAction("&Search", self)
        searchAction.setShortcut("Ctrl+F")
        searchAction.setStatusTip('Search for a tag number')
        # #undo action
        # undoAction = QtGui.QAction("&Undo", self)
        # undoAction.setShortcut("Ctrl+Z")
        # undoAction.setStatusTip("Undo last change")
        # undoAction.triggered.connect(self.undoStack.undo())
        # #redo action
        # redoAction = QtGui.QAction("&Redo", self)
        # redoAction.setStatusTip("Redo last undo")
        # redoAction.triggered.connect(self.undoStack.redo())
        #report issue action
        issueAction = QtGui.QAction("&Report an issue", self)
        issueAction.setStatusTip("Report an issue to the developer")
        issueAction.triggered.connect(self.reportIssue)
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
        # editMenu.addAction(undoAction)
        # editMenu.addAction(redoAction)
        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(issueAction)
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

    def pushSaveAction(self):
        path = QtGui.QFileDialog.getSaveFileName(
                self, 'Save File', '', '.csv')
        if path:
            with open(path, 'w') as stream:
                writer = csv.writer(stream)
                for row in range(self.table.rowCount()):
                    rowdata = []
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        if item is not None:
                            rowdata.append(
                                item.text())
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
    
    def pushOpenAction(self):
        path = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '/home')
        if path:
            with open(path, 'r') as stream:
                self.table.setRowCount(0)
                self.table.setColumnCount(0)
                for rowdata in csv.reader(stream):
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    self.table.setColumnCount(len(rowdata))
                    for column, data in enumerate(rowdata):
                        item = QtGui.QTableWidgetItem(data)
                        self.table.setItem(row, column, item)
                
    def reportIssue(self):
        webbrowser.open('https://github.com/BillyGTCarlyle/tag-manager/issues')

    def Table(self):        
        self.rowCount = 2048
        self.table = QtGui.QTableWidget()
        self.setCentralWidget(self.table)
        self.table.setHorizontalHeaderLabels(['Number', 'Comments'])
        self.table.setRowCount(self.rowCount)
        self.table.setColumnCount(2)
        self.show()

   #def initSearch(self):
   #     self.le = QtGui.QLineEdit(self)
   #     self.le.move(130,22)

        
   # def search(self):
   #     text, ok = QtGui.QInputDialog.getText(self, 'Search Tag',
   #         'Enter tag number:')
   #     if ok:
   #         self.le.setText(str(text))
   

#credit to Justin Hendryx for writing and explaining this class to me
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

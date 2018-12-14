from PyQt5 import *
from PyQt5.QtCore import QThread
import sys
import server
from PyQt5 import QtCore, QtGui, QtWidgets
from client.clientView import Ui_Client

class ClientController():
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.view = Ui_Client()

class RestHelper(QThread):
    def __init__(self):
        QThread.__init__(self)

    def show(self):
        self.dialog.show()

    def getAllStudents(self):
        students = server.UserList.get()
        rowPosition = Ui_Client.allStudentsTable.rowCount()
        Ui_Client.allStudentsTable.insertRow(rowPosition)

    def getOneStudent(self, id):
        pass

    def deleteStudent(self, id):
        pass

    def addStudent(self, username, email, picture):
        pass

    def editStudent(self, id, username = None, email = None, picture = None):
        pass

    def run(self):
        self.getAllStudents()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
from PyQt5 import *
from PyQt5.QtCore import QThread
import sys
import server
from PyQt5 import QtCore, QtGui, QtWidgets
from client.clientView import Ui_Client

class ClientController(object):
    def __init__(self):
        self.view = Ui_Client()

        self.window = QtWidgets.QMainWindow()
        self.view.setupUi(self.window,self)

        self.clientThread = ThreadHandeler(self)

        self.view.loadStudent_button.clicked.connect(lambda: self.clientThread.getAllStudents())

    def show(self):
        self.window.show()

    def close(self):
        self.clientThread.close()

class ThreadHandeler():

    def __init__(self, Controller):
        self.workerThread = RestHelper(Controller)
        self.workerThread.start()

    def close(self):
        self.workerThread.quit()

    def getAllStudents(self):
        self.workerThread.getAllStudents()

    def testMethod(self):
        self.workerThread.testMethod()

class RestHelper(QThread):
    def __init__(self, Controller):
        QThread.__init__(self)
        self.controller = Controller

    def testMethod(self):
        print("Hallo Welt")

    def getAllStudents(self):
        #students = server.UserList.get()
        rowPosition = self.controller.view.allStudentsTable.rowCount()
        print(rowPosition)
        self.controller.view.allStudentsTable.insertRow(rowPosition)

    def getOneStudent(self, id):
        pass

    def deleteStudent(self, id):
        pass

    def addStudent(self, username, email, picture):
        pass

    def editStudent(self, id, username = None, email = None, picture = None):
        pass

    def run(self):
        pass
        #self.getAllStudents()

from PyQt5 import *
from PyQt5.QtCore import QThread
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QWidget
from client.clientView import Ui_Client
from client.clientModel import Model
from server import server
import requests

class ClientController(object):
    def __init__(self):
        self.view = Ui_Client()

        self.window = QtWidgets.QMainWindow()
        self.view.setupUi(self.window,self)

        self.view.loadStudent_button.clicked.connect(lambda: self.getAllStudents())

        self.table = self.view.allStudentsTable
        self.model = Model()

    def show(self):
        self.window.show()

    def close(self):
        pass
        #self.clientThread.close()

    def getAllStudents(self):
        self.view.loadStudent_button.setEnabled(False)
        self.workerThread = RestHelper(self)
        self.workerThread.start()

    def editStudent(self):
        pass

    def deleteStudent(self):
        pass

    def updateStudentList(self):

        btn = QPushButton('Update', self.view.allStudentsTable)
        btn2 = QPushButton('Delete', self.view.allStudentsTable)

        self.view.allStudentsTable.setRowCount(0)

        for student in self.model.students.json():
            rowPosition = self.view.allStudentsTable.rowCount()
            self.view.allStudentsTable.insertRow(rowPosition)

            self.view.allStudentsTable.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(student['username']))
            self.view.allStudentsTable.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(student['email']))
            self.view.allStudentsTable.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(student['picture']))

            self.view.allStudentsTable.setCellWidget(rowPosition, 3, btn)
            self.view.allStudentsTable.setCellWidget(rowPosition, 4, btn2)

        self.view.loadStudent_button.setEnabled(True)


class RestHelper(QThread):
    def __init__(self, Controller):
        QThread.__init__(self)
        self.controller = Controller
        self.table = self.controller.view.allStudentsTable

    def testMethod(self):
        print("Hallo Welt")

    def getAllStudents(self):
        pass
    def getOneStudent(self, id):
        pass

    def deleteStudent(self, id):
        pass

    def addStudent(self, username, email, picture):
        pass

    def editStudent(self, id, username = None, email = None, picture = None):
        pass

    def __del__(self):
        self.wait()

    def run(self):
        self.sleep(2)
        #self.table.setRowCount(0)

        self.controller.model.students = requests.get("http://127.0.0.1:5000/user")
        self.controller.updateStudentList()


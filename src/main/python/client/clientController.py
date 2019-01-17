from PyQt5 import *
from PyQt5.QtCore import QThread
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QWidget
from client.clientView import Ui_Client
#from client.clientView import Ui_Client
from client.clientModel import Model
#from client.clientModel import Model
import requests, json
from functools import partial

class ClientController(object):
    def __init__(self):
        self.view = Ui_Client()

        self.window = QtWidgets.QMainWindow()
        self.view.setupUi(self.window,self)

        self.model = Model()

    def returnWindow(self):
        return self.window

    def show(self):
        self.window.show()
        self.getAllStudents()

    def getAllStudents(self):
        self.view.loadStudent_button.setEnabled(False)

        self.updateStudentList()

    def addNewStudent(self, username, email, picture=None):
        self.username = username.text()
        self.email = email.text()
        self.picture = ""
        if(picture):
            self.picture = picture.text()
        if((self.username != "") & (self.email != "")):
            url = "http://localhost:5000/user"
            json_dict = {'username': self.username, 'email': self.email, 'picture': self.picture}
            requests.post(url, json = json_dict)
        self.updateStudentList()

    def editStudent(self, current_row):
        if (current_row is not None):
            id = self.view.allStudentsTable.item(current_row, 0).text()
            username = self.view.allStudentsTable.item(current_row, 1).text()
            email = self.view.allStudentsTable.item(current_row, 2).text()
            picture = self.view.allStudentsTable.item(current_row, 3).text()

            url = "http://localhost:5000/user/" + str(id)

            # Checks if username and email are not null and not empty
            if ((username != "") & (email != "") & (picture != "")):
                json_dict = {'username': username, 'email': email, 'picture': picture}
                requests.put(url, json=json_dict)
            elif ((username != "") & (email != "")):
                json_dict = {'username': username, 'email': email}
                requests.put(url, json=json_dict)
            else:
                # TODO: Show error on GUI
                print("Errorrrr")
            self.updateStudentList()

    def deleteStudent(self, current_row):
        if (current_row is not None):
            id = self.view.allStudentsTable.item(current_row, 0).text()

            url = "http://localhost:5000/user/" + str(id)
            response = requests.delete(url)
            self.updateStudentList()

    def updateStudentList(self):

        self.model.students = requests.get("http://127.0.0.1:5000/user")

        self.view.allStudentsTable.setRowCount(0)

        for student in self.model.students.json():
            rowPosition = self.view.allStudentsTable.rowCount()
            self.view.allStudentsTable.insertRow(rowPosition)

            id = student['id']

            item = QtWidgets.QTableWidgetItem(str(student['id']))
            item.setFlags(Qt.ItemIsEditable)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.view.allStudentsTable.setItem(rowPosition, 0, item)
            self.view.allStudentsTable.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(student['username']))
            self.view.allStudentsTable.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(student['email']))
            self.view.allStudentsTable.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(student['picture']))

            btn = QPushButton('Update', self.view.allStudentsTable)
            self.view.allStudentsTable.setCellWidget(rowPosition, 4, btn)
            #Source: http://discourse.techart.online/t/pyqt-maya-how-to-pass-arguments-to-a-function-when-connecting-it-to-pyqt-button/2953/2
            btn.clicked.connect(partial(self.editStudent, current_row = rowPosition))

            btn2 = QPushButton('Delete', self.view.allStudentsTable)
            self.view.allStudentsTable.setCellWidget(rowPosition, 5, btn2)
            btn2.clicked.connect(partial(self.deleteStudent, current_row = rowPosition))

        self.view.loadStudent_button.setEnabled(True)

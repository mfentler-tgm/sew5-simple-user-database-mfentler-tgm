import pytest
from pytestqt import qtbot
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from client.clientController import *
import requests, json, time

@pytest.fixture
def setUp(qtbot):
    #app = QtWidgets.QApplication([])

    #app.exec_()

    url = "http://localhost:5000/user"

    json_dict1 = {'username': 'Mr Testuser', 'email': 'mrtestuser@gmx.at'}
    json_dict2 = {'username': 'Fr Testfrau', 'email': 'testfrau@gmail.com'}

    requests.post(url, json=json_dict1)
    requests.post(url, json=json_dict2)

    controller = ClientController()
    controller.show()
    qtbot.add_widget(controller.returnWindow())
    #qtbot.waitForWindowShown(controller.window)

    yield (controller, qtbot)

    response = requests.get(url)
    for user in response.json():
        requests.delete("http://localhost:5000/user/" + str(user['id']))

def test_getUser_onStartup(setUp):
    controller, qtbot = setUp
    assert(controller.view.allStudentsTable.rowCount() > 0)

def test_addingUser_allArgs(setUp):
    controller, qtbot = setUp

    rows = controller.view.allStudentsTable.rowCount()

    qtbot.keyClicks(controller.view.addStudent_username, "Mario Fentler")
    qtbot.keyClicks(controller.view.addStudent_email, "mfentler@student.tgm.ac.at")
    qtbot.keyClicks(controller.view.addStudent_picture, "http://cdn.ebaumsworld.com/mediaFiles/picture/2453506/85677232.jpg")
    qtbot.mouseClick(controller.view.addStudent_button, QtCore.Qt.LeftButton)

    #time.sleep(1)

    assert(controller.view.allStudentsTable.rowCount() == rows+1)

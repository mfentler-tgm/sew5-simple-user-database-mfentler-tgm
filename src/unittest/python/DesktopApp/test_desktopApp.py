import pytest
from pytestqt import qtbot
from PyQt5 import QtWidgets
from client.clientController import *
import requests

@pytest.fixture
def setUp(qtbot):
    app = QtWidgets.QApplication([])
    controller = ClientController()
    controller.show()
    app.exec_()

    url = 'http://localhost:5000/user'

    json_dict1 = {'username': 'Mr Testuser', 'email': 'mrtestuser@gmx.at'}
    json_dict2 = {'username': 'Fr Testfrau', 'email': 'testfrau@gmail.com'}

    requests.post(url, json=json_dict1)
    requests.post(url, json=json_dict2)

    yield (controller, qtbot)

    response = requests.get(url)
    for user in response:
        requests.delete('http://localhost:5000/user/' + str(user['id']))

def test_getUser_onStartup(bot):
    controller, qtbot = bot
    assert(controller.view.allStudentsTable.rowCount() > 0)

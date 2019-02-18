from clientController import ClientController
#from client.clientController import ClientController
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

def main():
    try:
        app = QtWidgets.QApplication([])
        controller = ClientController()
        controller.show()
        app.exec_()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
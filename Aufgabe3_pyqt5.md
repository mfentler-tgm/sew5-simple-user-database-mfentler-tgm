# Aufgabe 3 - PyQt5 Python Client

## Aufgabenstellung
Die detaillierte Aufgabenstellung zu der Übung befindet sich [hier](TODO3.md)  
## Deploying
- Server starten (server.py)
- PythonClient starten
- Tox starten - für die Testcases
## Implementierung
### Vorarbeit
Als erstes muss PyQt5 installiert werden.  
```bash
pip install pyqt5
pip install pyqt5-tools
```
Mit den PyQt5 Tools installiert man sich unteranderem den PyQt5-Designer. Der kann verwendet werden um einfach GUIs zu erstellen. 
Er befindet sich hier: __C:\Python\Python37\Lib\site-packages\pyqt5_tools__  

Nachdem man dann mit dem Tool die GUI erstellt hat und sie abgespeichert hat muss man diese auch noch in ein Python File umwandeln. Das geht mit folgendem Befehl: 
```bash
pyuic5 -x input.ui -o output.py
```
## Client starten
Um die Desktop App zu starten, wurde eine eigene Klasse erstellt. In der Klasse wird eine neue __QApplication__ erstellt, ein __Controller__ und schließlich die __show()__ Methode des Controllers aufgerufen. Natürlich wird hier auch ein try catch eingebaut, da der __Server laufen__ muss damit die GUI funktioniert. -> Dazu server.py starten.  
```python
def main():
    try:
        app = QtWidgets.QApplication([])
        controller = ClientController()
        controller.show()
        app.exec_()
    except:
        print("Start server first")
```

## MVC
Als Design Pattern wird MVC verwendet. Die __View__ ist das umgewandelte ui File (vorheriger Schritt). In der Methode __setpUi()__ wird noch ein Parameter __Controller__ hinzugefügt, 
damit man die Buttons mit den Methoden verknüpfen kann.  
Die __Model__ Klasse beinhaltet einzig und allein einen Konstruktor und darin eine student Liste. 
Im __Controller__ ist die Logik hinter der Desktop App.  

Dort sind die Methoden für das Löschen, Adden, Editieren und Abrufen. Dort gibt es auch die Methode show(). Diese ist dafür zuständig, dass das Window angezeigt wird 
und ruft auch gleichzeitig noch die Methode zum Abrufen aller User aus der Datenbank beim Öffnen des Fensters auf.  
```python
def show(self):
	self.window.show()
	self.getAllStudents()
```

Für die CRUD Methoden werden weiterhin die Methoden des Servers verwendet. Um diese zu erreichen arbeiten wir mit __requests__. Die Methoden im Controller holen sich lediglich die Werte aus der GUI, überprüfen diese und senden sie weiter.  

Zur __Anzeige__ der Daten wird eine Tabelle verwendet. Pro user gibt es eine Zeile mit seiner ID(nicht editierbar), Username, Email, Picture und zwei Buttons. Einen zum Speichern der Änderungen und einen zum Löschen.  
Wenn man Daten von einem bestehenden User ändern will muss man einfach nur in die Zelle klicken, den Wert ändern und auf den Button klicken. Der sendet die Argumente dann an den Server und lädt die Seite und die User der Tabelle neu.  

Wenn man neue Rows an die Tabelle anhängt, dann werden die Werte in einer Tabellenreihe mit "__setItem()__" hinzugefügt. Wenn man allerdings Buttons hinzufügen will, dann muss man die Methode "__setCellWidget(<row>,<column>,<QtWidget>)__" verwenden.  
Den Buttons muss man dann auch noch eine OnClick Methode zuweisen. Dabei ist zu beachten, dass man allerdings nur einen Verweis anstatt einem Methodenaufruf machen muss - also ohne die "__()__".  
Wenn die Methode allerdings Parameter benötigt, dann kann man die mit __partial()__ zuweisen.
```python
self.view.allStudentsTable.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(student['username']))
```
```python
btn = QPushButton('Update', self.view.allStudentsTable)
self.view.allStudentsTable.setCellWidget(rowPosition, 4, btn)
#Source: http://discourse.techart.online/t/pyqt-maya-how-to-pass-arguments-to-a-function-when-connecting-it-to-pyqt-button/2953/2
btn.clicked.connect(partial(self.editStudent, current_row = rowPosition))
self.editButtons.append(btn)
```

## Testing
Für das Testen wird __pytest-qt__ verwendet. Dieses Package enthält einen __qtBot__ mit dem man Mausklicks und Tastatureingaben auf der GUI simulieren und testen kann.  

Im neuen Testfile wird wieder eine __pytest.fixture__ verwendet, die immer vor jedem Testcase aufgerufen wird. Darin werden die Klassen immer neu aufgerufen, zwei Testuser eingefügt und am Ende wieder gelöscht.  
Mit __yield(controller,qtbot)__ definiert man die return values der Methode. Alles was danach in der Methode steht wird erst beim Beenden aufgerufen (User wieder löschen).

Bei den Testcases wird einfach überprüft ob sie die GUI bei gewissen Aktionen ändert und ob sich die Daten in der Datenbank ändern, falls man einen User löscht über den Button zum Beispiel.  
Bei diesem Testcase wird überprüft ob eine neue Row in die Tabelle eingefügt wurde nachdem, ein neuer User geaddet wurde.  
```python
def test_addingUser_allArgs(setUp):
    controller, qtbot = setUp

    rows = controller.view.allStudentsTable.rowCount()

    qtbot.keyClicks(controller.view.addStudent_username, "Mario Fentler")
    qtbot.keyClicks(controller.view.addStudent_email, "mfentler@student.tgm.ac.at")
    qtbot.keyClicks(controller.view.addStudent_picture, "http://cdn.ebaumsworld.com/mediaFiles/picture/2453506/85677232.jpg")
    qtbot.mouseClick(controller.view.addStudent_button, QtCore.Qt.LeftButton)

    time.sleep(0.5)

    assert(controller.view.allStudentsTable.rowCount() == rows+1)
```

Damit der __Innvocation Error__ nicht kommt beim Ausführen der Pytests auf Travis, muss man das Package __pytest-xvfb__ installieren und auch in das requirements.txt File hinzufügen. ([Source](https://pypi.org/project/pytest-xvfb/))
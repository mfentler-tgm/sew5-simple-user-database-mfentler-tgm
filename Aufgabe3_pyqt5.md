# Aufgabe 3 - PyQt5 Python Client

## Aufgabenstellung
Die detaillierte Aufgabenstellung zu der Übung befindet sich [hier](TODO3.md)  

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

## MVC
Als Design Pattern wird MVC verwendet. Die View ist das umgewandelte ui File (vorheriger Schritt). In der Methode setUpUi wird noch ein Parameter __Controller__ hinzugefügt, 
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
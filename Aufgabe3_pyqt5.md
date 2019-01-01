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
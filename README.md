# "Restful User-Service"

## Aufgabenstellung
Die detaillierte [Aufgabenstellung](TASK.md) beschreibt die notwendigen Schritte zur Realisierung.

## Implementierung
### Vorarbeit
Als erster Schritt wird Tox installiert:

    pip install tox
Im tox.ini File added man noch folgende dependencies:

    flask
    flask-restful
    request
    json
### SQLite3
Um SQLite herunter zu laden, holt man sich die Binarys von der offiziellen Webseite[3], erstellt einen neuen Ordner und fügt den heruntergeladenen Inhalt in diesen Ordner ein. Um die Installation zu verifizieren, folgender Befehl:

    sqlite3
Zusätzlich kann man sqlite noch zum Pfad hinzufügen (recommended).
#### Datenbank erstellen
Aus einem JSON-File wird eine SQLite Datenbank erstellt. Dazu wird sqlitebitter verwendet.

    pip install sqlitebiter
    
## Quellen
[1] https://medium.com/python-pandemonium/build-simple-restful-api-with-python-and-flask-part-2-724ebf04d12  
[2] https://stackoverflow.com/questions/34202755/how-to-run-python-scripts-within-tox-created-virtual-environment-without-specify  

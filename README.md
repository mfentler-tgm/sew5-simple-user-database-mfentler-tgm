# "Restful User-Service"

## Aufgabenstellung
Die detaillierte [Aufgabenstellung](TASK.md) beschreibt die notwendigen Schritte zur Realisierung.

## Implementierung
### Vorarbeit
Als erster Schritt wird Tox installiert:

    pip install tox
Im tox.ini File added man noch folgende Dependencies, die im "requirements.txt" File zu finden sind:

### SQLite3
Um SQLite herunter zu laden, holt man sich die Binarys von der offiziellen Webseite[3], erstellt einen neuen Ordner und fügt den heruntergeladenen Inhalt in diesen Ordner ein. Um die Installation zu verifizieren, folgender Befehl:

    sqlite3
Zusätzlich kann man sqlite noch zum Pfad hinzufügen (recommended).
### Datenbank erstellen
Die Datenbank, auf die im Code referenziert wird muss zuerst erstellt werden. Das geht folgendermaßen.  
Man öffnet die CMD und wechselt in das Verzeichnis in dem die Datei liegt.

    python
    #from <filename> import db
    from client import db
    db.create_all()
Dieser Command erstellt einem die SQLite Datenbank.
### API Testing tool
Um die Api zu testen gibt es zwei verschiedene Tools:
- Postman  
- Insomnia  
(Hat meiner Ansicht nach ein einfacheres, besser gestaltetes Design)
    
## Quellen
[1] https://medium.com/python-pandemonium/build-simple-restful-api-with-python-and-flask-part-2-724ebf04d12  
[2] https://stackoverflow.com/questions/34202755/how-to-run-python-scripts-within-tox-created-virtual-environment-without-specify  
[3] https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3  


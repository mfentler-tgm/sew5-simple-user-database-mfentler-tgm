# Aufgabe 4 - Authentication mit HTTP-Digest

## Aufgabenstellung
- [X]: __CRUD Authentifizieren__  
GK: mit HTTP-Digest aus UserDB mit mindestens SHA256 Hash (Hashlib) authentifizieren  
EK: OAuthV2 Authentifizierung wenn kein Hash vorhanden  
-> Erstellen, Updaten, Löschen nur Admins  
-> Lesen nur auth. Username w/o Hash
 
- [X]: Deployment (Kein werkzeug von Python verwenden!)  
GK: lokal
EK: Heroku -> Zertifikat HTTPS (letsencrypt)

## Vorarbeit
Es gibt 2 Methoden für die Authentifizierung.  
HTTP-Basic Auth und HTTP-Digest Auth. Hier in diesem Beispiel wird Digest verwendet. Dazu muss folgendes Package installiert werden:  
```bash
pip3 install flask-httpauth
```

Die Authentifizierung erfolgt am Server. Dort brauchen wir folgende Imports:  
Md5 ist die Standardverschlüsselungsmethode für HTTP-Digest.  
```python
from flask_httpauth import HTTPDigestAuth
from hashlib import md5 as basic_md5
```

Weiters muss noch eine weitere Spalte in der Tabelle angefügt werden.  
```python
password = db.Column(db.String(255))
```

## Authentifizierung

## Deployment
Lokal kann man mit __GUnicorn__ deployen. Dieses Package ist allerdings ein UNIX Package, was bedeutet dass es nur auf Linux Maschinen funktioniert.

```bash
pip3 install gunicorn
//gunicorn filename:methodname
gunicorn server:main
```

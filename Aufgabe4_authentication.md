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
Md5 ist die Standardverschlüsselungsmethode für HTTP-Digest. Im Konstruktor von HTTPDigestAuth geben
wir an, dass das Passwort verschlüsselt ist und daher bei der Abfrage die Input-Daten auch verschlüsselt werden müssen. 
```python
from flask_httpauth import HTTPDigestAuth
from hashlib import md5 as basic_md5

auth = HTTPDigestAuth(use_ha1_pw=True)
```

Weiters muss noch eine weitere Spalte in der Tabelle angefügt werden.  
```python
password = db.Column(db.String(255))
```
Da es nun eine weitere Spalte gibt, muss diese auch im Konstruktor behandelt werden. Dabei wird das Passwort im
Konstruktor manuell verschlüsselt.
```python
self.password = get_ha1(username,password,auth.realm)
```

### Verschlüsselung
Das Passwort wird nach einem speziellen Muster verschlüsselt. Dabei wird das verschlüsselte
Passwort aus dem Usernamen, dem Passwort und einem realm zusammengesetzt. (Ist von Digest so vorgegeben)

```python
def md5(str):
    str = str.encode('utf-8')
    return basic_md5(str)

def get_ha1(user, pw, realm):
    a1 = user + ":" + realm + ":" + pw
    return md5(a1).hexdigest()
```

## Authentifizierung
Für die Authentifizierung wird wie bereits erwähnt __HTTPDigestAuth__ verwendet. Dabei wird der User aufgefordert seine Credentials
in ein Formular einzugeben um die Methoden aufrufen zu können. Nachdem er seine Daten eingegeben hat bleibt er für die ganze Session angemeldet.

Um Methoden zu sichern muss man sie mit der Annotation __@auth.login_required__ markieren.

Man muss Digest auch eine Methode bereitstellen mit der das Passwort eines User angefragt werden können. Diese ist mit der Annotation __@auth.get_passwort__ zu markieren.
```python
@auth.get_password
def get_password(username):
    all_users = User_DB.query.all()
    result = users_schema.dump(all_users)
    for user in result.data:
        if user["username"] == username:
            return user["password"]
    return None
```

## Testing
Da man nun authentifiziert sein muss um die Methoden benutzen zu können, funktionieren die geschriebenen Tests nicht mehr.  
Um die Tests wieder lauffähig zu machen muss man HTTP-Header mitgeben.  

Konkret funktioniert das so:  
__(1.)__ Wird eine get-Anfrage an den Server geschickt und die Response in einem Objekt gespeichert.
```python
response = client.get('/user')
assert (response.status_code == 401)
```  
__(2.)__ Aus diesem Response werden dann alle notwendigen Informationen abgerufen um damit und mit Username/Passwort eines Users das verschlüsselte Passwort zu erstellen.  
```python
auth_type, auth_info = header.split(None, 1)
d = parse_dict_header(auth_info)

a1 = 'admin:' + d['realm'] + ':1234'
ha1 = md5(a1).hexdigest()
```
__(3.)__ (Beispiel User adden), in diesem Fall wird nun der HTTP-Header mit der gewünschten Methode erweitert und dann mit dem vorher erstellten Hash zusammengefügt.
```python
a2 = 'POST:/user'
ha2 = md5(a2).hexdigest()
a3 = ha1 + ':' + d['nonce'] + ':' + ha2
auth_response = md5(a3).hexdigest()
```  
__(4.)__ Dieser Header wird nun beim Aufruf der Methode mitgeben.
```python
response = client.post('/user', data=json.dumps(json_dict), content_type='application/json', headers={
            'Authorization': 'Digest username="admin",realm="{0}",'
                             'nonce="{1}",uri="/user",response="{2}",'
                             'opaque="{3}"'.format(d['realm'],
                                                   d['nonce'],
                                                   auth_response,
                                                   d['opaque'])})
```

Jetzt nochmal die Methode __im Ganzen:__
```Python
def login(client, method, json_dict=None, url=None):

    response = client.get('/user')
    assert (response.status_code == 401)
    header = response.headers.get('WWW-Authenticate')

    auth_type, auth_info = header.split(None, 1)
    d = parse_dict_header(auth_info)

    a1 = 'admin:' + d['realm'] + ':1234'
    ha1 = md5(a1).hexdigest()

    if((method == "post") and (json_dict != None)):

        a2 = 'POST:/user'
        ha2 = md5(a2).hexdigest()
        a3 = ha1 + ':' + d['nonce'] + ':' + ha2
        auth_response = md5(a3).hexdigest()

        response = client.post('/user', data=json.dumps(json_dict), content_type='application/json', headers={
            'Authorization': 'Digest username="admin",realm="{0}",'
                             'nonce="{1}",uri="/user",response="{2}",'
                             'opaque="{3}"'.format(d['realm'],
                                                   d['nonce'],
                                                   auth_response,
                                                   d['opaque'])})
```

## Deployment
Lokal kann man mit __GUnicorn__ deployen. Dieses Package ist allerdings ein UNIX Package, was bedeutet dass es nur auf Linux Maschinen funktioniert.
  
Davor muss man sicherstellen, dass die Datenbank auch erstellt wurde. Dazu
führt man folgenden Befehl aus:   
```python
python src/main/python/server/databaseHandler.py
```
```bash
pip3 install gunicorn
//gunicorn filename:methodname
gunicorn server:app
```

# "Restful User-Service"

## Aufgabenstellung
Die detaillierte [Aufgabenstellung](TASK.md) beschreibt die notwendigen Schritte zur Realisierung für die erste Aufgabe.  

Die Task der zweiten Aufgabe befinden sich [hier](TODO2.md).

## Implementierung
1. [Zur Implementierung](Aufgabe1_flaskServer.md) der ersten Aufgabe  
2. [Zur Implementierung](Aufgabe2_restApi.md) der zweiten Aufgabe, Web-Api  
3. [Zur Implementierung](Aufgabe3_pyqt5.md) der dritten Aufgabe, PyQT5 Desktop App    
4. [Zur Implementierung](Aufgabe4_authentication.md) der vierten Aufgabe, Authentication  
- [ ]: CRUD Authentifizieren  
GK: mit HTTP-Digest aus UserDB mit mindestens SHA256 Hash (Hashlib) authentifizieren  
EK: OAuthV2 Authentifizierung wenn kein Hash vorhanden  
-> Erstellen, Updaten, Löschen nur Admins  
-> Lesen nur auth. Username w/o Hash
 
- [ ]: Deployment (Kein werkzeug von Python verwenden!)  
GK: lokal
EK: Heroku -> Zertifikat HTTPS (letsencrypt)
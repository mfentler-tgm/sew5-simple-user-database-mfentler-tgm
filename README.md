# "Restful User-Service"

## Aufgabenstellung
Die detaillierte [Aufgabenstellung](TASK.md) beschreibt die notwendigen Schritte zur Realisierung.

## Implementierung
### Vorarbeit
Als erster Schritt wird Tox installiert:

    pip install tox
Im tox.ini File added man noch folgende Dependencies, die im "requirements.txt" File zu finden sind:

    pytest
    pytest-cov
    pytest-html
    flask
    flask-restful
    flask-sqlalchemy
    flask-marshmallow
    requests

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

## Konfiguration
Folgende Zeilen werden ganz oben nach den Inputs eingefügt. Das sind die Konfigurationen für die Datenbank und für Flask:

    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'C:\\Users\\mario\\git\\sew5-simple-user-database-mfentler-tgm\\usercrud.sqlite')
    db = SQLAlchemy(app)
    ma = Marshmallow(app)
    api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user')
### DB-Model
Da es sich um eine SQLite Datenbank handelt, braucht man auch folgende Klassen (DB.Model und Schema):

    class User_DB(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        email = db.Column(db.String(120), unique=True)
        picture = db.Column(db.String(400))

        def __init__(self, username, email,picture):
            self.username = username
            self.email = email
            self.picture = picture

    class UserSchema(ma.Schema):
        class Meta:
            # Fields to expose
            fields = ('id','username', 'email','picture')
    
    user_schema = UserSchema()
    users_schema = UserSchema(many=True)

## Rest-Methods
Die REST Methoden (get, post, put, delete) werden von dem Python File abgefangen und entsprechend bearbeitet.  
Die Post-Methode könnte folgendermaßen aussehen:

    def post(self):
        username = request.json['username']
        email = request.json['email']
        picture = request.json['picture']

        new_user = User_DB(username, email, picture)

        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user)

Für die Rest-Methoden verwende ich zwei Klassen.
- Class User:  
Hier sind alle meine Methoden drinnen, bei denen ich als Parameter die __user_id__ benötige. Also __get(u_id), put(u_id) und delete(u_id)__.  
- Class User.List:  
Hier sind die Methoden drinnen, für die ich die __user_id__ nicht als Parameter benötige. __post(), get()__  

Diese Aufteilung gibt es aus einem bestimmten Grund. Und zwar muss man der Api die Resourcen zuteilen. In dem Fall muss die Adresse auf die Klassen gemapt werden:

    ##
    ## Actually setup the Api resource routing here
    ##
    api.add_resource(UserList, '/user')
    api.add_resource(User, '/user/<user_id>')

## Quellen
[1] https://medium.com/python-pandemonium/build-simple-restful-api-with-python-and-flask-part-2-724ebf04d12  
[2] https://stackoverflow.com/questions/34202755/how-to-run-python-scripts-within-tox-created-virtual-environment-without-specify  
[3] https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3  


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

## Testing
Zum automatischen Testen der Api werden die Module pytest und pytest-flask verwendet.  
Dabei benützt man einen pytest-client um auf die Api zuzugreifen.  
In den Tests werden die Methoden post, get, put und delete überprüft.  

Genauso wie bei Unittests gibt es auch hier Methoden, die vor jeder Methode ausgeführt werden. In dem Fall sieht die verwendete Methode so aus:  

    @pytest.fixture
    def client():
        print('\n----- CREATE FLASK APPLICATION\n')
        test_client = app.test_client()
        return test_client

Damit die tests vom pytest Command gefunden werden muss das File __"test\_*"__ und die Methoden darin auch __"test\_*"__ heißen.  

Man kann über json Dictionaries Objekte der Api mitgeben. Im Fall von der Mehode Post kann der Test so aussehen:  

    def test_post_user(client):
        print('\n----- TESTING POST USER\n')
        json_dict = {"email":"testuser@student.tgm.ac.at","username":"testuser","picture":"linkZumBild"}
        response = client.post('/user', data=json.dumps(json_dict), content_type='application/json')
        assert response.status_code == 200

Über __client.REST-MethodenName__ kann man die Methoden der Api ansprechen.

### Globale Variable userCounter
Mit der globalen Variable wird der hardgecodete Teil aus den Tests herausgenommen. Die Variable wird mit der Länge der Objekte im json File beschrieben. Somit wissen die Methoden welche id der Testuser haben muss. 

Um auf eine globale Variable zuzugreifen, wenn man sie überschreiben will, muss man sie zuerst als global in dieser Methode deklarieren. Wenn man nur den Inhalt der Variable abfragen möchte reicht es sie über den Variablennamen aufzurufen.    

    result = client.get('/user')
    json_data = json.loads(result.data)
    global userCounter
    for item in json_data:
        userCounter += 1
    url = '/user/' + str(userCounter)

## Quellen
[1] https://medium.com/python-pandemonium/build-simple-restful-api-with-python-and-flask-part-2-724ebf04d12  
[2] https://stackoverflow.com/questions/34202755/how-to-run-python-scripts-within-tox-created-virtual-environment-without-specify  
[3] https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3  
[4] https://stackoverflow.com/questions/423379/using-global-variables-in-a-function   
[5] https://stackoverflow.com/questions/24898797/check-if-key-exists-and-iterate-the-json-array-using-python  

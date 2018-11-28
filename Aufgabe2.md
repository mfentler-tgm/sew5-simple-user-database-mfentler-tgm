# Aufgabe 2 - VUE.js
Hier in der Übung geht es darum der Api ein Userinterface zu geben, welches man über eine IP-Adresse erreichen können soll.

## Aufgabenstellung
Die detaillierte Aufgabenstellung zu dieser Übung befindet sich [hier](TODO2.md).

## Implementierung
### Vorarbeit
Als erstes wird das Package Vue/cli herunter geladen, dieses wird für den nächsten Schritt benötigt.  

    npm install -g @vue/cli
Mit diesem Package kann man jetzt ein neues VUE Projekt aufsetzen. [3]

    cd src/main/vue
    vue create client
Nach der Installation kann man Vue testhalber mit folgendem Befehl starten uns sollte auf 'localhost:8080' das Bild von VUE sehen.  

    npm run dev
    oder
    npm start

#### Benötigte Packages
Für die Aufgabe braucht man noch zusätzlich folgende Packages:  

    Python:
    pip install flask-cors

    JavaScript:
    npm install axios@0.18.0 --save
    npm install bootstrap@4.1.1 --save
    npm install cypress --save-dev

### VUE.js

### Cypress.io Tests
Mit folgendem Command kann man Cypress ausführen  

	npm run cypress:open
Dazu muss vorher in das package.json folgende Lines zu den Scripts hinzufügen:  

	"cypress:open": "cypress open"
Anschließend kann man die Tests in JS-Files schreiben, die sich in folgenem Ordner befinden müssen. (src/main/vue/client/cypress/integration)
### Travis

## Quellen
[1] - [https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs](https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs)  
[2] - [https://flask-cors.corydolphin.com/en/latest/index.html](https://flask-cors.corydolphin.com/en/latest/index.html)  
[3] - [https://vue-loader-v14.vuejs.org/en/start/setup.html](https://vue-loader-v14.vuejs.org/en/start/setup.html)  
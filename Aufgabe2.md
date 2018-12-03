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
Für VUE wird als erstes ein neuer Ordner angelegt. Das geht mit folgendem Befehl. Dabei 'entered' man sich einfach durch.  

    vue init webpack <name>
Nachdem man das gemacht hat bekommt man direkt eine vordefinierte Projektstruktur.  
Als nächster Schritt wird ein neues .vue File im components Ordner angelegt. In dieses File kommt der HTML und JavaScript Code -> das __eigentlich wesentliche File__!

Im __main.js__ File wird Bootstrap importiert.  

    import Vue from 'vue'
    import App from './App'
    import router from './router'
    import 'bootstrap/dist/css/bootstrap.css'
    import BootstrapVue from 'bootstrap-vue'
    import { Modal } from 'bootstrap-vue/es/components'
    
    Vue.config.productionTip = false
    Vue.use(BootstrapVue)
    Vue.use(Modal)
    
    /* eslint-disable no-new */
    new Vue({
      el: '#app',
      router,
      components: { App },
      template: '<App/>'
    })
In das File im __route__ Ordner werden die Files den Routen zugewiesen. (In unserem Fall wird das User File der Route '/' zugewiesen)  

    import Vue from 'vue'
    import Router from 'vue-router'
    import User from '@/components/User'
    import 'bootstrap/dist/css/bootstrap.css'
    
    Vue.use(Router)
    
    export default new Router({
      routes: [
        {
          path: '/',
          name: 'User',
          component: User
        }
      ],
      mode: 'history'
    })

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
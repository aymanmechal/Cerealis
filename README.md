# Cerealis

Projet web simple qui utilise une intelligence artificielle pour prédire le cours de plusieurs produits agricoles dans le futur.

## Fonctionnement du projet

Le projet est compose de deux parties :

- une interface web en `Vue 3` pour afficher les donnees
- un serveur backend en `FastAPI` qui fournit les donnees et les predictions

Le frontend appelle le backend via l'API `http://localhost:8000`.
Si besoin, l'URL du serveur peut aussi etre definie avec la variable `VITE_API_URL`.

Le serveur peut etre lancé sur une machine et joint par un client depuis une autre machine 

## Infos à connaître avant de lancer le serveur

Le backend se trouve dans `Docker-server-deployement`.
Le projet peut maintenant etre lance avec `Docker Compose` depuis la racine.

## Pour télécharger le serveur: 

git clone https://github.com/aymanmechal/Cerealis

## Lancer le serveur Avec Docker Compose

Depuis la racine du projet :

```bash
docker compose up --build
```

Si tu veux lancer seulement le backend, depuis `Docker-server-deployement` :

```bash
docker run -p 8000:8000 cerealis-server
```

Les données seront consultables sous la forme d'un dictionnaire à l'URL : `http://localhost:8000/api/data?months=120`

## Se connecter au serveur

Une fois le serveur lancé :

- documentation API : `http://localhost:8000/docs`
- donnees du projet : `http://localhost:8000/api/data?months=120`
- ajout manuel de donnees : `http://localhost:8000/docs` puis endpoint `POST /api/add_month`
- interface web : `http://localhost:8080`   

Pour chacune de ces commandes il est possible de remplacer localhost par l'ip du serveur distant

Si le serveur tourne sur une autre machine, remplace `localhost` par l'adresse IP du serveur.

## Ajouter des donnees

Le serveur stocke les donnees dans une base SQLite, puis synchronise aussi un fichier CSV.

Pour ajouter un mois :

1. Ouvre `http://localhost:8000/docs` (ou l'IP du serveur distant)
2. Choisis `POST /api/add_month`
3. Clique sur `Try it out`
4. Renseigne les champs demandes
5. Clique sur `Execute`

Les donnees sont ensuite enregistrees dans la base et exportees dans `Server/agricol_datas.csv`.

## De facon générale, à chaque modification du code, on doit recréer une image docker; à la racine du projet:
```bash
docker compose down
docker compose up --build #cela va lancer Cerealis par la suite
```

## Structure globale du projet

- `src/` : code de l'interface web
- `src/screens/` : ecrans principaux de l'application
- `src/components/` : composants reutilisables
- `src/services/api.js` : appels vers le backend
- `src/data/mock.ts` : donnees de secours pour l'interface
- `public/` : fichiers statiques
- `Docker-server-deployement/` : serveur FastAPI, base SQLite et CSV
- `Docker-server-deployement/Server/Server.py` : code principal du backend
- `Docker-server-deployement/Server/agricol_datas.csv` : backup de la base de données
- `Docker-server-deployement/Server/database.db` : base de donnees SQLite

## Technologies utilisees

- `Vue JS 3`
- `TypeScript`
- `Tailwind CSS`
- `FastAPI`
- `SQLite`
- `Docker`
- `Sickit-Learn`

## Autres

- Le frontend utilise l'API du backend pour charger les donnees.
- Le dossier `Docker-server-deployement` contient tout ce qui concerne le serveur.
- Les données doivent être inscrites manuellement

- A chaque modification du serveur, un nouveau conteneur docker doit etre créé: 
docker rm -f $(docker ps -aq) # Va supprimer les images docker déjà présentes
docker build -t mon-api-agricole . # Pour recréer un image docker

# Concernant les données présentes dans la base de données:

Les données correspondent à des moyennes mensuelles en France.
Les mois sont exprimés sous forme numérique (janvier = 1, février = 2, etc.).
La pression atmosphérique est exprimée en hectopascals (hPa).
La pluviométrie est exprimée en millimètres (mm).
Le prix du baril de pétrole est en dollars américains ($).
Le taux de change correspond à la conversion euro / dollar (EUR/USD).
Le taux d’inflation est exprimé en pourcentage (%) d’évolution annuelle.
Données suivies

Le projet inclut notamment des séries historiques (1996–2025) pour les indicateurs suivants :

Prix de l’eau (€/m³)
Prix du gaz naturel (€/MWh)
Prix de l’électricité (€/MWh)
Prix du blé tendre (€/t)
Prix du maïs (€/t)
Prix de l’orge (€/t)
Prix du sarrasin (€/t)
Prix du seigle (€/t)
Prix des graines de tournesol (€/t)
Prix des graines de moutarde (€/t)



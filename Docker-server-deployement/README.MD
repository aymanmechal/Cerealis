Pour lancer le conteneur:
docker run -p 8000:8000 mon-api-agricole

Sources:
Météo (Open-Meteo, sans clé) — moyenne mensuelle de température, pression et cumul de pluie sur Paris. Toujours disponible, données archivées.
Pétrole Brent (EIA DEMO_KEY) — prix mensuel en $/baril. La clé DEMO_KEY suffit pour 30 requêtes/heure. Tu peux obtenir une clé gratuite sur eia.gov si tu veux plus de quota.
EUR/USD (Frankfurter, sans clé) — moyenne des taux journaliers sur le mois.
Inflation (INSEE API BDM) — IPC France mensuel, variation annuelle en %.
Prix eau/gaz/électricité (INSEE séries tarifaires) — rebasés sur ta dernière valeur réelle en DB grâce à _get_last_insee_index_and_value(), pour conserver des valeurs cohérentes avec ton historique.
Céréales (FranceAgriMer export CSV public) — blé, maïs, orge, seigle, tournesol. Sarrasin et moutarde n'ont pas de cotation publique standardisée → leur dernière valeur DB est reconduite automatiquement.
Fallback universel — si n'importe quelle source tombe en erreur, _fallback_db() reprend silencieusement la dernière valeur connue en base, sans jamais bloquer le scheduler.


Pour actualiser les datas: Lance ton serveur avec python Server.py dans ton terminal
Ouvre ton navigateur sur http://localhost:8000/docs
Clique sur POST /api/add_month
Clique sur "Try it out"
Remplis les 18 champs (Annee, Mois, Prix_Ble, etc.)
Clique sur "Execute"

# Matrice des températures moyennes mensuelles en France (1996-2025)
# Chaque sous-liste représente une année (de Janvier à Décembre)

# Matrice de la pression atmosphérique moyenne mensuelle en France (1996-2025)
# Unité : Hectopascals (hPa)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice de la pluviométrie mensuelle moyenne en France (1996-2025)
# Unité : Millimètres (mm)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du prix moyen mensuel du baril de pétrole Brent (1996-2025)
# Unité : Dollars US ($)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du taux de change moyen mensuel Euro / Dollar (EUR/USD)
# Unité : 1 Euro = X Dollars
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du taux d'inflation annuel en France (1996-2025)
# Unité : Pourcentage (%) d'évolution par rapport à N-1
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]


# Matrice du prix moyen du mètre cube d'eau en France (1996-2025)
# Unité : Euros par m³ (€/m3) - TTC (incluant distribution et assainissement)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du prix moyen du gaz naturel en France (1996-2025)
# Unité : Euros par Mégawattheure (€/MWh)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du prix moyen de l'électricité sur le marché de gros en France (1996-2025)
# Unité : Euros par Mégawattheure (€/MWh)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du prix du Blé Tendre sur Euronext Paris (MATIF)
# Unité : Euros par Tonne (€/t) - Échéance rapprochée
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du prix du Maïs Grain sur Euronext Paris (MATIF)
# Unité : Euros par Tonne (€/t)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du prix de l'Orge Fourragère (Base France/Europe)
# Unité : Euros par Tonne (€/t)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du prix moyen du Sarrasin en France (Prix payé au producteur)
# Unité : Euros par Tonne (€/t)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du prix moyen du Seigle en France (Prix payé au producteur)
# Unité : Euros par Tonne (€/t)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du prix moyen des Graines de Tournesol (Départ Organisme Stockeur France)
# Unité : Euros par Tonne (€/t)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

# Matrice du prix des Graines de Moutarde (Base France/Bourgogne)
# Unité : Euros par Tonne (€/t)
# Structure : [Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sept, Oct, Nov, Déc]

pip install pandas
pip install scikit-learn
pip install fastapi uvicorn

Installation de docker desktop

2. Côté Vue.js (Le Client)
Dans votre projet Vue, vous allez utiliser fetch (natif) ou la bibliothèque axios pour appeler cette URL.

Voici un exemple de composant simple (Predictions.vue) :

HTML
<template>
  <div>
    <h1>Prédictions Agricoles</h1>
    <button @click="loadData">Charger les données</button>

    <div v-if="loading">Chargement des calculs...</div>

    <div v-if="results">
      <h3>Prédictions pour le Blé (Prix_Ble)</h3>
      <ul>
        <li v-for="(item, index) in results.Prix_Ble.donnees_predites" :key="index">
          Date: {{ item[0] }} - Prix estimé: {{ item[1] }} €
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const results = ref(null);
const loading = ref(false);

const loadData = async () => {
  loading.value = true;
  try {
    // On appelle l'URL de notre serveur Python
    const response = await fetch('http://localhost:8000/api/data?months=120');
    results.value = await response.json();
  } catch (error) {
    console.error("Erreur de connexion au serveur Python:", error);
  } finally {
    loading.value = false;
  }
};
</script>

1. Lancer le serveur :
Dans ton terminal, exécute :

python Server.py
2. Tester dans ton navigateur :
Ouvre http://localhost:8000/api/data?months=120. Tu devrais voir une structure JSON avec tes données passées et tes prédictions.

3. Dans ton code Vue.js (Frontend) :
Voici à quoi devrait ressembler ton appel pour récupérer les données du blé, par exemple :

JavaScript
axios.get('http://localhost:8000/api/data?months=24')
  .then(response => {
    const blePasse = response.data.Prix_Ble.donnees_passees;
    const bleFutur = response.data.Prix_Ble.donnees_predites;
    console.log("Prédiction dans 2 ans :", bleFutur[bleFutur.length - 1]);
  })
  .catch(error => console.error("Erreur API :", error));


  docker rm -f $(docker ps -aq) pour supprimer le conteneur
  docker build -t mon-api-agricole . pour le recréer
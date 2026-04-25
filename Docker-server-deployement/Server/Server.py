import sqlite3
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

#Pour la régression: 
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

def DB_init():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prix_agricoles (
        Annee INTEGER,
        Mois INTEGER,
        Prix_Ble FLOAT,
        Prix_Mais FLOAT,
        Prix_Orge FLOAT,
        Prix_Sarrasin FLOAT,
        Prix_Seigle FLOAT,
        Prix_Tournesol FLOAT,
        Prix_Moutarde FLOAT,
        Temperature FLOAT,
        Pression FLOAT,
        Pluviometrie FLOAT,
        Prix_Petrole FLOAT,
        Valeur_Euro FLOAT,
        Inflation FLOAT,
        Prix_Eau FLOAT,
        Prix_Gaz FLOAT,
        Prix_Electricite FLOAT
    )
    ''')

    conn.commit()
    conn.close()
    print("Base de données et table créées avec succès !")

def import_datas_from_csv(nom_fichier_csv='agricol_datas.csv', nom_fichier_db='database.db'):
    conn = sqlite3.connect(nom_fichier_db)
    
    try:
        # Lecture du CSV
        df = pd.read_csv(nom_fichier_csv, sep=';', decimal=',', encoding='utf-8-sig')

        # REMPLACEMENT CRITIQUE : 'replace' au lieu de 'append'
        # Cela vide la table avant d'insérer, garantissant 0 doublon.
        df.to_sql('prix_agricoles', conn, if_exists='replace', index=False)

        conn.commit()
        print(f"Synchronisation réussie : {len(df)} lignes uniques importées.")

    except FileNotFoundError:
        print(f"Erreur : fichier '{nom_fichier_csv}' introuvable.")
    except Exception as e:
        print(f"Erreur lors de l'import : {e}")
    finally:
        conn.close()

def Show_database(nom_fichier_db='database.db'):
    # 1. Connexion à la base
    conn = sqlite3.connect(nom_fichier_db)
    
    try:
        # 2. Lecture de la table vers un DataFrame Pandas
        # On utilise une requête SQL simple
        df = pd.read_sql_query("SELECT * FROM prix_agricoles", conn)
        
        # 3. Configuration de l'affichage pour voir toutes les colonnes
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        
        # 4. Affichage
        if df.empty:
            print("La base de données est vide.")
        else:
            print(f"\n--- CONTENU DE LA BASE ({len(df)} lignes) ---")
            # .head(30) permet d'afficher les 30 premières lignes
            # .round(3) applique ta limite de 3 chiffres après la virgule
            print(df.head(30).round(3))
            
    except Exception as e:
        print(f"Erreur lors de l'affichage : {e}")
    finally:
        # 5. Fermeture de la connexion
        conn.close()

def predict_future_environnemment_datas(element: str, nbr_months: int):
    conn = sqlite3.connect('database.db')
    query = f"SELECT Annee, Mois, {element} FROM prix_agricoles ORDER BY Annee, Mois"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return None

    # 1. Préparation avec Mois (Saison) et Time_Index (Tendance)
    df['Time_Index'] = np.arange(len(df)) 
    X = df[['Mois', 'Time_Index']].values
    Y = df[element].values

    # 2. Préparation du futur (strictement déterministe)
    last_month = df['Mois'].iloc[-1]
    last_time = df['Time_Index'].iloc[-1]
    
    future_X = []
    current_month = last_month
    current_time = last_time
    
    for _ in range(nbr_months):
        current_month = 1 if current_month >= 12 else current_month + 1
        current_time += 1
        future_X.append([current_month, current_time])
    
    future_X = np.array(future_X)

    # 3. On privilégie la Polynomiale pour l'évolution temporelle
    # Même si le Random Forest a un meilleur R² sur le passé, 
    # la Polynomiale est plus "honnête" pour l'extrapolation future.
    poly_feat = PolynomialFeatures(degree=2)
    X_poly = poly_feat.fit_transform(X)
    model_poly = LinearRegression()
    model_poly.fit(X_poly, Y)

    # 4. Calcul des prédictions (Sans ajout de bruit)
    future_X_poly = poly_feat.transform(future_X)
    future_preds = model_poly.predict(future_X_poly)

    return np.round(future_preds, 2)

def export_to_csv(nom_fichier_csv='export_prix_agricoles.csv', nom_fichier_db='database.db'):
    conn = sqlite3.connect(nom_fichier_db)
    
    try:
        df = pd.read_sql_query("SELECT * FROM prix_agricoles ORDER BY Annee, Mois", conn)
        
        if df.empty:
            print("La base de données est vide, rien à exporter.")
            return
        
        df.to_csv(nom_fichier_csv, index=False, sep=';', decimal=',', encoding='utf-8-sig')
        print(f"Export réussi : {len(df)} lignes exportées dans '{nom_fichier_csv}'")
        
    except Exception as e:
        print(f"Erreur lors de l'export : {e}")
    finally:
        conn.close()

def fetch_new_month_data() -> dict | None:
    now = datetime.now()
    if now.month == 1:
        mois_cible  = 12
        annee_cible = now.year - 1
    else:
        mois_cible  = now.month - 1
        annee_cible = now.year

    print(f"[Scheduler] Récupération des données pour {annee_cible}-{mois_cible:02d}...")

    # 👉 TON APPEL API ICI — en attendant :
    return None

def insert_new_month_row(data: dict, nom_fichier_db='database.db'):
    """Insère une ligne dans la DB si elle n'existe pas déjà."""
    conn = sqlite3.connect(nom_fichier_db)
    try:
        cursor = conn.cursor()
        # Vérification doublon
        cursor.execute(
            "SELECT COUNT(*) FROM prix_agricoles WHERE Annee=? AND Mois=?",
            (data["Annee"], data["Mois"])
        )
        if cursor.fetchone()[0] > 0:
            print(f"[Scheduler] Données {data['Annee']}-{data['Mois']:02d} déjà présentes, insertion ignorée.")
            return False

        colonnes = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        cursor.execute(
            f"INSERT INTO prix_agricoles ({colonnes}) VALUES ({placeholders})",
            list(data.values())
        )
        conn.commit()
        print(f"[Scheduler] ✅ Ligne {data['Annee']}-{data['Mois']:02d} insérée avec succès.")
        return True
    except Exception as e:
        print(f"[Scheduler] Erreur insertion : {e}")
        return False
    finally:
        conn.close()

async def monthly_data_refresh():
    """
    Exécutée automatiquement le 1er de chaque mois.
    1. Récupère les données du mois écoulé
    2. Les insère en base
    3. Met à jour le CSV source
    """
    print(f"\n[Scheduler] 🕕 Tâche mensuelle déclenchée le {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    new_data = fetch_new_month_data()
    
    if new_data is None:
        print("[Scheduler] Aucune donnée à insérer ce mois-ci.")
        return
    
    inserted = insert_new_month_row(new_data)
    
    if inserted:
        # On réécrit le CSV pour qu'il reste synchronisé avec la DB
        export_to_csv('Server/agricol_datas.csv')
        print("[Scheduler] 🔄 CSV mis à jour.")
    
    print("[Scheduler] Tâche mensuelle terminée.\n")

def predict_future_product_datas(environnement_datas_predictions, product_to_predict: str):
    
    # 1. Récupérer les données historiques de la base
    conn = sqlite3.connect('database.db')
    cols_env = ["Temperature", "Pression", "Pluviometrie", "Prix_Petrole",
                "Valeur_Euro", "Inflation", "Prix_Eau", "Prix_Gaz", "Prix_Electricite"]
    
    query = f"SELECT {', '.join(cols_env)}, {product_to_predict} FROM prix_agricoles ORDER BY Annee, Mois"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print("Aucune donnée trouvée.")
        return None

    # 2. Préparer X (environnement historique) et Y (produit à prédire)
    X_hist = df[cols_env].values
    Y_hist = df[product_to_predict].values

    # 3. Tester plusieurs modèles de régression et garder le meilleur
    modeles = {
        "LinearRegression"      : LinearRegression(),
        "Ridge"                 : Ridge(alpha=1.0),
        "RandomForest"          : RandomForestRegressor(n_estimators=100, random_state=42),
        "GradientBoosting"      : GradientBoostingRegressor(n_estimators=100, random_state=42),
    }

    meilleur_nom   = None
    meilleur_score = -np.inf
    meilleur_model = None
    for nom, modele in modeles.items():
        modele.fit(X_hist, Y_hist)
        score = r2_score(Y_hist, modele.predict(X_hist))
        if score > meilleur_score:
            meilleur_score = score
            meilleur_nom   = nom
            meilleur_model = modele


    # 4. Construire la matrice des données futures d'environnement
    X_future = np.column_stack(environnement_datas_predictions)

    # 5. Prédire avec le meilleur modèle
    predictions = meilleur_model.predict(X_future)

    return np.round(predictions, 2)

def Get_predictions_all_product_datas (number_of_months=120):
    Temperature_prediction = predict_future_environnemment_datas("Temperature",number_of_months)
    Pression_prediction = predict_future_environnemment_datas("Pression",number_of_months)
    Pluviometrie_prediction = predict_future_environnemment_datas("Pluviometrie",number_of_months)
    Prix_Petrole_prediction = predict_future_environnemment_datas("Prix_Petrole",number_of_months)
    Valeur_Euro_prediction = predict_future_environnemment_datas("Valeur_Euro",number_of_months)
    Inflation_prediction = predict_future_environnemment_datas("Inflation", number_of_months)
    Prix_Eau_prediction = predict_future_environnemment_datas("Prix_Eau",number_of_months)
    Prix_Gaz_prediction = predict_future_environnemment_datas("Prix_Gaz",number_of_months)
    Prix_Electricite_prediction = predict_future_environnemment_datas("Prix_Electricite",number_of_months)

    Environnement_datas_predictions=[Temperature_prediction,Pression_prediction,Pluviometrie_prediction,Prix_Petrole_prediction ,Valeur_Euro_prediction ,Inflation_prediction,Prix_Eau_prediction ,Prix_Gaz_prediction ,Prix_Electricite_prediction]

    produits = ["Prix_Ble", "Prix_Mais", "Prix_Orge", "Prix_Sarrasin", 
                "Prix_Seigle", "Prix_Tournesol", "Prix_Moutarde"]

    predictions_produits = {
        produit: predict_future_product_datas(Environnement_datas_predictions, produit)
        for produit in produits
    }
    return predictions_produits

def Get_prediction_datas(Predictions_duree=120):
    
    # 1. Récupérer toutes les données historiques de la base
    conn = sqlite3.connect('database.db')
    query = """
        SELECT Annee, Mois, Prix_Ble, Prix_Mais, Prix_Orge, Prix_Sarrasin,
               Prix_Seigle, Prix_Tournesol, Prix_Moutarde
        FROM prix_agricoles 
        ORDER BY Annee, Mois
    """
    df_hist = pd.read_sql_query(query, conn)
    conn.close()

    produits = ["Prix_Ble", "Prix_Mais", "Prix_Orge", "Prix_Sarrasin",
                "Prix_Seigle", "Prix_Tournesol", "Prix_Moutarde"]

    # 2. Récupérer les prédictions futures
    predictions_produits = Get_predictions_all_product_datas(Predictions_duree)

    # 3. Générer les labels futurs à partir du dernier mois connu
    derniere_annee = int(df_hist['Annee'].iloc[-1])
    dernier_mois   = int(df_hist['Mois'].iloc[-1])
    labels_futurs  = []
    annee_courante = derniere_annee
    mois_courant   = dernier_mois

    for _ in range(Predictions_duree):
        mois_courant += 1
        if mois_courant > 12:
            mois_courant   = 1
            annee_courante += 1
        labels_futurs.append(f"{annee_courante}-{mois_courant:02d}")

    # 4. Construire le dictionnaire final avec tuples
    result = {}
    for produit in produits:
        result[produit] = {
            "donnees_passees": [
                (f"{int(row['Annee'])}-{int(row['Mois']):02d}", float(row[produit]))
                for _, row in df_hist.iterrows()
            ],
            "donnees_predites": [
                (label, float(valeur))
                for label, valeur in zip(labels_futurs, predictions_produits[produit])
            ],
        }
    return result


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    print("Initialisation de la base de données...")
    DB_init()

    # Vérification : la DB est-elle déjà peuplée ?
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM prix_agricoles")
    row_count = cursor.fetchone()[0]
    conn.close()

    if row_count == 0:
        print("Base de données vide — chargement depuis le CSV de backup...")
        import_datas_from_csv('Server/agricol_datas.csv')
        print("Import CSV terminé.")
    else:
        print(f"Base de données déjà peuplée ({row_count} lignes) — import CSV ignoré.")

    print("Base de données prête !")

    # ✅ Lancement du scheduler : exécution le 1er de chaque mois à 06h00
    scheduler.add_job(
        monthly_data_refresh,
        trigger=CronTrigger(day=1, hour=6, minute=0),
        id="monthly_refresh",
        replace_existing=True,
    )
    scheduler.start()
    print("[Scheduler] ✅ Planificateur démarré — tâche prévue le 1er de chaque mois à 06h00.")


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    print("[Scheduler] Planificateur arrêté.")


# ✅ BONUS : Route manuelle pour déclencher la tâche sans attendre
@app.post("/api/refresh")
async def manual_refresh():
    """Permet de déclencher la mise à jour manuellement (utile pour les tests)."""
    await monthly_data_refresh()
    return {"status": "ok", "message": "Mise à jour manuelle effectuée."}

@app.post("/api/add_month")
def add_month_data(
    Annee: int,
    Mois: int,
    Prix_Ble: float,
    Prix_Mais: float,
    Prix_Orge: float,
    Prix_Sarrasin: float,
    Prix_Seigle: float,
    Prix_Tournesol: float,
    Prix_Moutarde: float,
    Temperature: float,
    Pression: float,
    Pluviometrie: float,
    Prix_Petrole: float,
    Valeur_Euro: float,
    Inflation: float,
    Prix_Eau: float,
    Prix_Gaz: float,
    Prix_Electricite: float
):
    data = {
        "Annee": Annee,
        "Mois": Mois,
        "Prix_Ble": Prix_Ble,
        "Prix_Mais": Prix_Mais,
        "Prix_Orge": Prix_Orge,
        "Prix_Sarrasin": Prix_Sarrasin,
        "Prix_Seigle": Prix_Seigle,
        "Prix_Tournesol": Prix_Tournesol,
        "Prix_Moutarde": Prix_Moutarde,
        "Temperature": Temperature,
        "Pression": Pression,
        "Pluviometrie": Pluviometrie,
        "Prix_Petrole": Prix_Petrole,
        "Valeur_Euro": Valeur_Euro,
        "Inflation": Inflation,
        "Prix_Eau": Prix_Eau,
        "Prix_Gaz": Prix_Gaz,
        "Prix_Electricite": Prix_Electricite
    }

    # 1. Insertion en base (réutilise ta fonction existante)
    inserted = insert_new_month_row(data)

    if not inserted:
        return {
            "status": "skipped",
            "message": f"Les données pour {Annee}-{Mois:02d} existent déjà en base."
        }

    # 2. Sync CSV depuis la DB (réutilise ta fonction existante)
    export_to_csv('Server/agricol_datas.csv')

    return {
        "status": "ok",
        "message": f"Données {Annee}-{Mois:02d} ajoutées en base et CSV mis à jour."
    }

@app.get("/api/data")
def provide_data(months: int = 120):
    try:
        data = Get_prediction_datas(months)
        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    DB_init()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM prix_agricoles")
    row_count = cursor.fetchone()[0]
    conn.close()
    if row_count == 0:
        import_datas_from_csv('Server/agricol_datas.csv')
    print("\n--- SERVEUR PRÊT ---")          
    uvicorn.run(app, host="0.0.0.0", port=8000)
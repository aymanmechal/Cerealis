import sqlite3
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

def init_db():
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

def load_csv(csv_file='agricol_datas.csv', db_file='database.db'):
    conn = sqlite3.connect(db_file)
    try:
        df = pd.read_csv(csv_file, sep=';', decimal=',', encoding='utf-8-sig')
        df.to_sql('prix_agricoles', conn, if_exists='replace', index=False)
        conn.commit()
        print(f"Synchronisation réussie : {len(df)} lignes uniques importées.")
    except FileNotFoundError:
        print(f"Erreur : fichier '{csv_file}' introuvable.")
    except Exception as e:
        print(f"Erreur lors de l'import : {e}")
    finally:
        conn.close()

def show_db(db_file='database.db'):
    conn = sqlite3.connect(db_file)
    try:
        df = pd.read_sql_query("SELECT * FROM prix_agricoles", conn)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        if df.empty:
            print("La base de données est vide.")
        else:
            print(f"\n--- CONTENU DE LA BASE ({len(df)} lignes) ---")
            print(df.head(30).round(3))
    except Exception as e:
        print(f"Erreur lors de l'affichage : {e}")
    finally:
        conn.close()

def predict_env(col: str, n: int):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query(f"SELECT Annee, Mois, {col} FROM prix_agricoles ORDER BY Annee, Mois", conn)
    conn.close()

    if df.empty:
        return None

    df['t'] = np.arange(len(df))
    X = df[['Mois', 't']].values
    Y = df[col].values

    last_mo = df['Mois'].iloc[-1]
    last_t = df['t'].iloc[-1]

    X_fut = []
    mo, t = last_mo, last_t
    for _ in range(n):
        mo = 1 if mo >= 12 else mo + 1
        t += 1
        X_fut.append([mo, t])
    X_fut = np.array(X_fut)

    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, Y)

    return np.round(model.predict(poly.transform(X_fut)), 2)

def export_csv(csv_file='export_prix_agricoles.csv', db_file='database.db'):
    conn = sqlite3.connect(db_file)
    try:
        df = pd.read_sql_query("SELECT * FROM prix_agricoles ORDER BY Annee, Mois", conn)
        if df.empty:
            print("La base de données est vide, rien à exporter.")
            return
        df.to_csv(csv_file, index=False, sep=';', decimal=',', encoding='utf-8-sig')
        print(f"Export réussi : {len(df)} lignes exportées dans '{csv_file}'")
    except Exception as e:
        print(f"Erreur lors de l'export : {e}")
    finally:
        conn.close()

def fetch_month() -> dict | None:
    now = datetime.now()
    mo = 12 if now.month == 1 else now.month - 1
    yr = now.year - 1 if now.month == 1 else now.year
    print(f"[Scheduler] Récupération des données pour {yr}-{mo:02d}...")
    return None

def insert_row(data: dict, db_file='database.db'):
    conn = sqlite3.connect(db_file)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM prix_agricoles WHERE Annee=? AND Mois=?",
            (data["Annee"], data["Mois"])
        )
        if cursor.fetchone()[0] > 0:
            print(f"[Scheduler] Données {data['Annee']}-{data['Mois']:02d} déjà présentes, insertion ignorée.")
            return False
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        cursor.execute(f"INSERT INTO prix_agricoles ({cols}) VALUES ({placeholders})", list(data.values()))
        conn.commit()
        print(f"[Scheduler] ✅ Ligne {data['Annee']}-{data['Mois']:02d} insérée avec succès.")
        return True
    except Exception as e:
        print(f"[Scheduler] Erreur insertion : {e}")
        return False
    finally:
        conn.close()

async def monthly_refresh():
    print(f"\n[Scheduler] 🕕 Tâche mensuelle déclenchée le {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    new_data = fetch_month()
    if new_data is None:
        print("[Scheduler] Aucune donnée à insérer ce mois-ci.")
        return
    inserted = insert_row(new_data)
    if inserted:
        export_csv('Server/agricol_datas.csv')
        print("[Scheduler] 🔄 CSV mis à jour.")
    print("[Scheduler] Tâche mensuelle terminée.\n")

def predict_crop(env_preds, crop: str):
    conn = sqlite3.connect('database.db')
    env_cols = ["Temperature", "Pression", "Pluviometrie", "Prix_Petrole",
                "Valeur_Euro", "Inflation", "Prix_Eau", "Prix_Gaz", "Prix_Electricite"]
    df = pd.read_sql_query(
        f"SELECT {', '.join(env_cols)}, {crop} FROM prix_agricoles ORDER BY Annee, Mois", conn
    )
    conn.close()

    if df.empty:
        print("Aucune donnée trouvée.")
        return None

    X = df[env_cols].values
    Y = df[crop].values

    models = {
        "linear": LinearRegression(),
        "ridge":  Ridge(alpha=1.0),
        "rf":     RandomForestRegressor(n_estimators=100, random_state=42),
        "gb":     GradientBoostingRegressor(n_estimators=100, random_state=42),
    }

    best_score = -np.inf
    best_model = None
    for m in models.values():
        m.fit(X, Y)
        s = r2_score(Y, m.predict(X))
        if s > best_score:
            best_score = s
            best_model = m

    X_fut = np.column_stack(env_preds)
    return np.round(best_model.predict(X_fut), 2)

def predict_all(n=120):
    env_preds = [
        predict_env("Temperature", n),
        predict_env("Pression", n),
        predict_env("Pluviometrie", n),
        predict_env("Prix_Petrole", n),
        predict_env("Valeur_Euro", n),
        predict_env("Inflation", n),
        predict_env("Prix_Eau", n),
        predict_env("Prix_Gaz", n),
        predict_env("Prix_Electricite", n),
    ]
    crops = ["Prix_Ble", "Prix_Mais", "Prix_Orge", "Prix_Sarrasin",
             "Prix_Seigle", "Prix_Tournesol", "Prix_Moutarde"]
    return {c: predict_crop(env_preds, c) for c in crops}

def smooth_preds(raw, last_price: float):
    if len(raw) == 0:
        return raw
    smoothed = (
        pd.Series(raw.astype(float))
        .rolling(window=3, center=True, min_periods=1)
        .mean()
        .values
    )
    result = np.empty_like(smoothed)
    prev = float(last_price)
    for i, val in enumerate(smoothed):
        clamped = float(np.clip(val, prev * 0.95, prev * 1.05))
        result[i] = clamped
        prev = clamped
    return np.round(result, 2)

def get_data(n_months=120):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query(
        "SELECT Annee, Mois, Prix_Ble, Prix_Mais, Prix_Orge, Prix_Sarrasin, Prix_Seigle, Prix_Tournesol, Prix_Moutarde FROM prix_agricoles ORDER BY Annee, Mois",
        conn
    )
    conn.close()

    crops = ["Prix_Ble", "Prix_Mais", "Prix_Orge", "Prix_Sarrasin",
             "Prix_Seigle", "Prix_Tournesol", "Prix_Moutarde"]
    preds = predict_all(n_months)

    last_yr = int(df['Annee'].iloc[-1])
    last_mo = int(df['Mois'].iloc[-1])
    labels = []
    yr, mo = last_yr, last_mo
    for _ in range(n_months):
        mo += 1
        if mo > 12:
            mo = 1
            yr += 1
        labels.append(f"{yr}-{mo:02d}")

    result = {}
    for c in crops:
        last_price = float(df[c].iloc[-1])
        smoothed   = smooth_preds(preds[c], last_price)
        result[c] = {
            "donnees_passees":  [(f"{int(r['Annee'])}-{int(r['Mois']):02d}", float(r[c])) for _, r in df.iterrows()],
            "donnees_predites": [(lbl, float(v)) for lbl, v in zip(labels, smoothed)],
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
    init_db()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM prix_agricoles")
    row_count = cursor.fetchone()[0]
    conn.close()

    if row_count == 0:
        print("Base de données vide — chargement depuis le CSV de backup...")
        load_csv('Server/agricol_datas.csv')
        print("Import CSV terminé.")
    else:
        print(f"Base de données déjà peuplée ({row_count} lignes) — import CSV ignoré.")

    print("Base de données prête !")

    scheduler.add_job(
        monthly_refresh,
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


@app.post("/api/refresh")
async def manual_refresh():
    await monthly_refresh()
    return {"status": "ok", "message": "Mise à jour manuelle effectuée."}

@app.post("/api/add_month")
def add_month_data(
    Annee: int, Mois: int,
    Prix_Ble: float, Prix_Mais: float, Prix_Orge: float,
    Prix_Sarrasin: float, Prix_Seigle: float, Prix_Tournesol: float,
    Prix_Moutarde: float, Temperature: float, Pression: float,
    Pluviometrie: float, Prix_Petrole: float, Valeur_Euro: float,
    Inflation: float, Prix_Eau: float, Prix_Gaz: float, Prix_Electricite: float
):
    data = {
        "Annee": Annee, "Mois": Mois,
        "Prix_Ble": Prix_Ble, "Prix_Mais": Prix_Mais, "Prix_Orge": Prix_Orge,
        "Prix_Sarrasin": Prix_Sarrasin, "Prix_Seigle": Prix_Seigle,
        "Prix_Tournesol": Prix_Tournesol, "Prix_Moutarde": Prix_Moutarde,
        "Temperature": Temperature, "Pression": Pression, "Pluviometrie": Pluviometrie,
        "Prix_Petrole": Prix_Petrole, "Valeur_Euro": Valeur_Euro, "Inflation": Inflation,
        "Prix_Eau": Prix_Eau, "Prix_Gaz": Prix_Gaz, "Prix_Electricite": Prix_Electricite,
    }

    inserted = insert_row(data)
    if not inserted:
        return {"status": "skipped", "message": f"Les données pour {Annee}-{Mois:02d} existent déjà en base."}

    export_csv('Server/agricol_datas.csv')
    return {"status": "ok", "message": f"Données {Annee}-{Mois:02d} ajoutées en base et CSV mis à jour."}

@app.get("/api/data")
def provide_data(months: int = 120):
    try:
        data = get_data(months)

        conn = sqlite3.connect('database.db')
        env_df = pd.read_sql_query(
            "SELECT Prix_Petrole, Valeur_Euro, Inflation, Temperature FROM prix_agricoles ORDER BY Annee DESC, Mois DESC LIMIT 1",
            conn
        )
        conn.close()

        if not env_df.empty:
            row = env_df.iloc[0]
            data["market_stats"] = {
                "Prix_Petrole": round(float(row["Prix_Petrole"]), 2),
                "Valeur_Euro":  round(float(row["Valeur_Euro"]),  4),
                "Inflation":    round(float(row["Inflation"]),    1),
                "Temperature":  round(float(row["Temperature"]),  1),
            }

        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    init_db()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM prix_agricoles")
    row_count = cursor.fetchone()[0]
    conn.close()
    if row_count == 0:
        load_csv('Server/agricol_datas.csv')
    print("\n--- SERVEUR PRÊT ---")
    uvicorn.run(app, host="0.0.0.0", port=8000)

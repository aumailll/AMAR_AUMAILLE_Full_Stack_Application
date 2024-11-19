from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import pandas as pd
import psycopg2

# Définir les colonnes correspondant à la table
CUSTOM_COLUMNS = [
    "Rang", "Titre", "Score", "Episodes", "Statut",
    "Studio", "Producteurs", "Type", "Genres_ET_Themes", "Lien"
]

def get_anime_data(db: Session):
    """
    Récupère les données des animes depuis la base de données.

    Args:
        db (Session): La session SQLAlchemy pour interroger la base de données.

    Returns:
        list[dict]: Une liste de dictionnaires contenant les informations des animes.
    """
    try:
        # Exécuter la requête SQL pour récupérer les données
        animes = db.execute(text("SELECT * FROM anime")).fetchall()
        
        # Transformer les résultats en liste de dictionnaires
        anime_list = [dict(zip(CUSTOM_COLUMNS, anime)) for anime in animes]

        return anime_list
    except Exception as e:
        # En cas d'erreur, loguer ou gérer l'exception
        print(f"Erreur lors de la récupération des animes : {e}")
        return []


# URL de connexion à PostgreSQL (depuis Docker)
DATABASE_URL = "postgresql://user:password@postgres:5432/db_projet"

COLUMN_MAPPING = {
    0: "rank",
    1: "titre",
    2: "score",
    3: "episodes",
    4: "statut",
    5: "studio",
    6: "producteurs",
    7: "type",
    8: "genres_themes",
    9: "lien"
}


def fetch_anime_data():
    """
    Récupère les données des animes depuis la base de données PostgreSQL.

    Returns:
        pandas.DataFrame: Les données des animes sous forme de DataFrame.
    """
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        query = "SELECT * FROM anime;"  # Requête SQL
        df = pd.read_sql(query, conn)  # Charger les données dans un DataFrame
        conn.close()

        # Renommer les colonnes selon le mapping
        if not df.empty:
            df.columns = [COLUMN_MAPPING.get(i, col) for i, col in enumerate(df.columns)]
        return df
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return pd.DataFrame()
    

    
def get_unique_genres(db: Session):
    """
    Récupère la liste des genres uniques des animes.

    Args:
        db (Session): La session SQLAlchemy pour interroger la base de données.

    Returns:
        list: Liste triée des genres uniques.
    """
    try:
        # Exécuter la requête SQL pour récupérer les genres des animes
        query = text("SELECT genres_themes FROM anime")  # Récupère la colonne genres_themes
        result = db.execute(query).fetchall()

        # Extraire les genres et les diviser en une liste
        all_genres = []
        for row in result:
            genres = row[0]
            if genres:  # S'il y a des genres
                all_genres.extend(genres.split(','))  # Séparer les genres par une virgule et ajouter à la liste

        # Retirer les doublons et trier les genres
        unique_genres = sorted(set(all_genres))

        return unique_genres
    except Exception as e:
        print(f"Erreur lors de la récupération des genres : {e}")
        return []


# avant Giulia
# ---

def fetch_data(db: Session):
    """
    Récupère les données des animes en utilisant une session SQLAlchemy.

    Args:
        db (Session): La session SQLAlchemy pour interroger la base de données.

    Returns:
        pandas.DataFrame: Les données des animes sous forme de DataFrame.
    """
    try:
        # Requête pour récupérer les données des animes
        query = text("SELECT * FROM anime;")
        result = db.execute(query).fetchall()

        # Vérifier si des résultats existent
        if result:
            # Colonnes correspondant à la table "anime"
            columns = [
                "rank", "titre", "score", "episodes", "statut",
                "studio", "producteurs", "type", "genres_themes", "lien"
            ]
            df = pd.DataFrame(result, columns=columns)
            return df
        else:
            return pd.DataFrame()  # Retourner un DataFrame vide si aucun résultat
    except Exception as e:
        print(f"Erreur lors de la récupération des données des animes : {e}")
        return pd.DataFrame()
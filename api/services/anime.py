from sqlalchemy.orm import Session
from sqlalchemy.sql import text

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

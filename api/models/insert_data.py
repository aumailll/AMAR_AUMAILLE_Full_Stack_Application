import pandas as pd
import uuid
from api.models import create_db
from sqlalchemy.orm import Session
from api.models.getdb import SessionLocal  # Assurez-vous que SessionLocal est importé depuis le bon fichier

# Chargement du fichier CSV avec un encodage explicite
anime_df = pd.read_csv('v7/Data/anime.csv', encoding='utf-8', quotechar='"')


# Fonction d'insertion des données dans la base
def insert_anime(session: Session, anime_df: pd.DataFrame):
    try:
        for _, row in anime_df.iterrows():
            anime = create_db.Anime(
                id=uuid.uuid4(),
                rank=row['Rank'],
                titre=row['Title'],
                score=row.get('Score', None),
                episodes=row.get('Episodes', None),
                statut=row.get('Status', None),
                studio=row.get('Studio', None),
                producteurs=row.get('Producers', None),
                type=row.get('Type', None),
                genres_et_themes=row.get('Genres & Themes', None),
                lien=row['Link']
            )
            session.add(anime)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erreur d'insertion : {e}")

    
    session.commit()

# Définition de la session
session = SessionLocal()

# Appel de la fonction d'insertion
insert_anime(session, anime_df)

# Fermeture de la session
session.close()

import pandas as pd
from api.models import create_db
from api.models.database import SessionLocal, engine, BaseSQL

session = SessionLocal()

anime_df = pd.read_csv('D:\E5\Full_stack\anime_fullStack\Data\anime.csv')


def insert_anime(session, anime_df):
    for _, row in anime_df.iterrows():
        anime = create_db.Anime(
            # Adjust column names if necessary to match model
            rank=row['rank'],
            titre=row['titre'],
            lien=row['lien'],
            score=row['score'],  # Ensure this matches your model's field name
            episodes=row['episodes'],
            statut=row['statut'],
            studio=row.get('studio', None),
            producteurs=row.get('producteurs', None),
            type=row.get('type', None),
            genres_ET_themes=row['genres_ET_themes']
        )
        session.add(anime)
    session.commit()

try:
    # Create tables if they don’t exist
    BaseSQL.metadata.create_all(bind=engine)
    # Insert data
    insert_anime(session, anime_df)
except Exception as e:
    print("Il y a eu une erreur:", e)
finally:
    # Close the session to release database resources
    session.close()

print("Les données ont été ajoutées à la base de données avec succès.")
import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models.create_db import Anime 
from api.models.getdb import DATABASE_URL  

# Création d'un engine pour enregistrer les données au tout début 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# Fonction d'insertion des données depuis le CSV
def insert_data(csv_file_path):
    session = SessionLocal()
    try:
       
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # On parcourt chaque tuple du csv et on créep pour chacun une instance dans la table anime
                anime = Anime(
                    rank=row['rank'],
                    titre=row['titre'],
                    score=row['score'],
                    episodes=row['episodes'],
                    statut=row['statut'],
                    studio=row['studio'],
                    producteurs=row['producteurs'],
                    type=row['type'],
                    genres_themes=row['genres_themes'],
                    lien=row['lien']
                )
                session.add(anime)

            # Commit les changements dans la base de données
            session.commit()
        print("Données insérées avec succès dans la table Anime.")

    except Exception as e:
        session.rollback()  # En cas d'erreur, on annule
        print(f"Erreur lors de l'insertion des données : {e}")

    finally:
        session.close()

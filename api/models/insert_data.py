import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models.create_db import Anime # Assure-toi d'importer ton modèle Anime
from api.models.getdb import DATABASE_URL  # Importation de l'URL de connexion

# Créer l'engine de connexion à la base de données
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# Fonction d'insertion des données depuis le CSV
def insert_data_from_csv(csv_file_path):
    session = SessionLocal()
    try:
        # Ouvrir et lire le fichier CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Créer une instance de l'objet Anime avec les données du CSV
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
        session.rollback()  # En cas d'erreur, annuler la transaction
        print(f"Erreur lors de l'insertion des données : {e}")

    finally:
        session.close()

# Appel de la fonction pour insérer les données
csv_file_path = r'Data/anime.csv'  # Modifie le chemin selon où ton fichier CSV est stocké
insert_data_from_csv(csv_file_path)

import streamlit as st
from api.models import SessionLocal
from api.services.anime import get_unique_genres, L_fetch_data
import requests
from bs4 import BeautifulSoup

# Fonction pour récupérer l'image de couverture depuis une page MyAnimeList
def get_cover_image_url(page_url):
    """
    Récupère l'URL de l'image de couverture d'une page MyAnimeList.

    Args:
        page_url (str): URL de la page MyAnimeList.

    Returns:
        str: URL de l'image de couverture, ou None si non trouvée.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(page_url, headers=headers)
        response.raise_for_status()  # Vérifie que la requête a réussi
        
        # Parser le contenu HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Rechercher la balise <meta property="og:image"> qui contient l'image
        image_tag = soup.find('meta', property='og:image')
        if image_tag and 'content' in image_tag.attrs:
            return image_tag['content']  # Retourne l'URL de l'image
    except Exception as e:
        print(f"Erreur lors de la récupération de l'image depuis {page_url}: {e}")
        return None

# Initialisation de la session SQLAlchemy
db = SessionLocal()

try:
    # Récupérer les genres uniques depuis la base de données
    genres = get_unique_genres(db)

    # Titre de l'application
    st.title("Sélectionner des Genres et Thèmes d'Anime")

    # Barre de recherche multiselect pour sélectionner plusieurs genres/thèmes
    selected_genres = st.multiselect("Choisissez un ou plusieurs genres/thèmes", genres)

    if selected_genres:
        st.subheader(f"Animes contenant tous les genres/thèmes sélectionnés : {', '.join(selected_genres)}")

        # Récupérer les données des animes depuis la base de données
        data = L_fetch_data(db)

        # Filtrer les données pour inclure uniquement les animes correspondant à tous les genres sélectionnés
        filtered_data = data[data['genres_themes'].apply(
            lambda x: all(genre.lower() in x.lower() for genre in selected_genres)
        )]

        if not filtered_data.empty:
            for _, row in filtered_data.iterrows():
                st.markdown("---")  # Ligne de séparation entre les éléments
                st.write(f"### {row['titre']}")
                # Utiliser des colonnes pour une disposition en ligne
                col1, col2 = st.columns([1, 2])  # col1 pour l'image (1 part), col2 pour la description (2 parts)
                with col1:
                    # Récupérer l'image de couverture depuis la page MyAnimeList
                    if row['lien']:
                        image_url = get_cover_image_url(row['lien'])
                        if image_url:
                            st.image(image_url, width=200)  # Image réduite pour s'adapter à la mise en page
                        else:
                            st.warning("Image non disponible.")
                    else:
                        st.warning("Aucune image disponible.")

                with col2:
                    # Afficher les informations à droite de l'image
                    
                    st.write(f"- **Score**: {row['score']}")
                    st.write(f"- **Studio**: {row['studio']}")
                    st.write(f"- **Genres et Thèmes**: {row['genres_themes']}")
                    st.write(f"- **Statut**: {row['statut']}")
                    st.write(f"- **Nombre d'épisodes**: {row['episodes']}")
                    st.write(f"- [Plus d'informations ici]({row['lien']})")

        else:
            st.warning("Aucun anime trouvé pour ces genres/thèmes.")
finally:
    # Fermez la session pour éviter les fuites
    db.close()

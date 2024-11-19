import streamlit as st
from api.models import SessionLocal
from api.services.anime import get_unique_genres, fetch_data
import requests
from bs4 import BeautifulSoup


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
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')

        image_tag = soup.find('meta', property='og:image')
        if image_tag and 'content' in image_tag.attrs:
            return image_tag['content'] 
    except Exception as e:
        st.warning(f"Erreur lors de la récupération de l'image depuis {page_url}: {e}")
        return None


def dashboard_preferences_utilisateur():
    """
    Affiche le tableau des préférences utilisateur.
    Permet de sélectionner des genres/thèmes et d'afficher les animes correspondants.
    """
    db = SessionLocal()

    try:
        genres = get_unique_genres(db)

        st.title("Rechercher avec le genre ou le thème")

        selected_genres = st.multiselect("Choisissez un ou plusieurs genres/thèmes", genres)

        if selected_genres:
            data = fetch_data(db)

            filtered_data = data[data['genres_themes'].apply(
                lambda x: all(genre.lower() in x.lower() for genre in selected_genres)
            )]

            if not filtered_data.empty:
                for _, row in filtered_data.iterrows():
                    st.markdown("---")
                    st.write(f"### {row['titre']}")
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        if row['lien']:
                            image_url = get_cover_image_url(row['lien'])
                            if image_url:
                                st.image(image_url, width=200)
                            else:
                                st.warning("Image non disponible.")
                        else:
                            st.warning("Aucune image disponible.")

                    with col2:                        
                        st.write(f"- **Score**: {row['score']}")
                        st.write(f"- **Studio**: {row['studio']}")
                        st.write(f"- **Genres et Thèmes**: {row['genres_themes']}")
                        st.write(f"- **Statut**: {row['statut']}")
                        st.write(f"- **Nombre d'épisodes**: {row['episodes']}")
                        st.write(f"- [Plus d'informations ici]({row['lien']})")

            else:
                st.warning("Aucun anime trouvé pour ces genres/thèmes.")

    except Exception as e:
        st.error(f"Erreur lors de l'accès aux données : {e}")

    finally:
        db.close()

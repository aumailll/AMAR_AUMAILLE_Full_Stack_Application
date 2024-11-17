import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px

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
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        query = "SELECT * FROM anime;"  # Requête SQL
        df = pd.read_sql(query, conn)  # Charger les données dans un DataFrame
        conn.close()
        
        if not df.empty:
            df.columns = [COLUMN_MAPPING.get(i, col) for i, col in enumerate(df.columns)]
        return df
    except Exception as e:
        st.error(f"Erreur lors de la connexion à la base de données : {e}")
        return pd.DataFrame()

data = fetch_anime_data()

# Titre de l'application
st.title("Étude du classement des animes")

if not data.empty:
    # Barre de recherche pour afficher les détails d'un anime
    st.subheader("Recherche d'un Anime")
    search_input = st.text_input("Entrez le nom d'un anime :")
    if st.button("Rechercher"):
        if search_input:
            search_result = data[data['titre'].str.contains(search_input, case=False, na=False)]
            if not search_result.empty:
                for _, row in search_result.iterrows():
                    st.write(f"**{row['titre']}**")
                    st.write(f"- Score: {row['score']}")
                    st.write(f"- Studios: {row['studio']}")
                    st.write(f"- Genres et thèmes: {row['genres_themes']}")
                    st.write(f"- Statut: {row['statut']}")
                    st.write(f"- Nombre d'épisodes: {row['episodes']}")
            else:
                st.error("Aucun anime trouvé.")

    # Afficher les liens vers les animes les mieux notés
    st.subheader("Liens vers les Animes les mieux notés")
    top_animes_links = [
        f"{i+1}. [{row['titre']}]({row['lien']}) - Score: {row['score']}"
        for i, row in data.head(10).iterrows()
    ]
    st.markdown("\n".join(top_animes_links))

    # Filtrer les données en fonction du rang sélectionné
    st.header("Sélectionnez une tranche d'animes")
    selected_range = st.slider(
        "Tranche de rang :",
        int(data['rank'].min()),
        int(data['rank'].max()),
        (1, 30)
    )
    filtered_data = data[(data['rank'] >= selected_range[0]) & (data['rank'] <= selected_range[1])]

    # Histogramme des studios les plus productifs
    st.subheader("Studios les plus productifs")
    if 'studio' in filtered_data.columns:
        studios_count = filtered_data['studio'].str.split(',').explode().value_counts()
        studio_fig = px.bar(
            studios_count,
            x=studios_count.index,
            y=studios_count.values,
            labels={'x': 'Studio', 'y': "Nombre d'animes produits"},
            title="Studios les plus productifs"
        )
        st.plotly_chart(studio_fig)

    # Histogramme du statut des animes
    st.subheader("Distribution des Animes en fonction du Statut")
    if 'statut' in filtered_data.columns:
        status_count = filtered_data['statut'].value_counts()
        status_fig = px.bar(
            status_count,
            x=status_count.index,
            y=status_count.values,
            labels={'x': 'Statut', 'y': "Nombre d'animes"},
            title="Distribution des Animes en fonction du Statut"
        )
        st.plotly_chart(status_fig)

    # Diagramme circulaire des genres les plus populaires
    st.subheader("Genres les plus populaires")
    if 'genres_themes' in filtered_data.columns:
        genres_count = filtered_data['genres_themes'].str.split(',').explode().value_counts()
        genres_fig = px.pie(
            names=genres_count.index,
            values=genres_count.values,
            title="Genres les plus populaires"
        )
        st.plotly_chart(genres_fig)

    # Histogramme du nombre d'épisodes
    st.subheader("Nombre d'épisodes")
    if 'episodes' in filtered_data.columns:
        episode_fig = px.bar(
            filtered_data,
            x='titre',
            y='episodes',
            labels={'x': 'Anime', 'y': "Nombre d'épisodes"},
            title="Histogramme du Nombre d'Épisodes"
        )
        st.plotly_chart(episode_fig)

else:
    st.warning("Aucune donnée disponible dans la base de données.")

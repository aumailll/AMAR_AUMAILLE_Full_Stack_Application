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

    # Filtrer les données en fonction du rang sélectionné
    st.header("Sélectionnez une tranche d'animes")
    selected_range = st.slider(
        "Tranche de rang :",
        int(data['rank'].min()),
        int(data['rank'].max()),
        (1, 30)
    )
    filtered_data = data[(data['rank'] >= selected_range[0]) & (data['rank'] <= selected_range[1])]

    # Afficher les liens vers les animes les mieux notés
    ITEMS_PER_VIEW = 10

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

    total_items = len(filtered_data)
    total_pages = (total_items // ITEMS_PER_VIEW) + (1 if total_items % ITEMS_PER_VIEW != 0 else 0)
    start_idx = (st.session_state.current_page - 1) * ITEMS_PER_VIEW
    end_idx = min(start_idx + ITEMS_PER_VIEW, total_items)

    paged_data = filtered_data.iloc[start_idx:end_idx]

    st.subheader(f"Classement des Animes ({start_idx+1} à {end_idx}/{total_items})")
    if not paged_data.empty:
        for i, row in enumerate(paged_data.iterrows(), start=start_idx + 1):
            idx, row_data = row
            st.markdown(f"**{i}. [{row_data['titre']}]({row_data['lien']})** - Score: {row_data['score']}")
    else:
        st.warning("Aucun anime à afficher dans cette plage.")

    col1, col2, col3 = st.columns([2, 6, 2])

    with col1:
        if st.button("⬅️", key="prev") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1

    with col2:
        page_circles = []
        for page in range(1, total_pages + 1):
            if page == st.session_state.current_page:
                page_circles.append(
                    f"<span style='color: #007BFF; font-size: 20px;'>●</span>"
                )
            else:
                page_circles.append(
                    f"<span style='color: lightgray; font-size: 20px;'>○</span>"
                )
        st.markdown(
            f"<div style='text-align: center;'>{' '.join(page_circles)}</div>",
            unsafe_allow_html=True,
        )

    with col3:
        if st.button("➡️", key="next") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1

    st.markdown("---")

    # Histogramme des studios les plus productifs
    st.subheader("Studios les plus productifs")
    if 'studio' in filtered_data.columns:
        studios_count = filtered_data['studio'].str.split(',').explode().value_counts()
        studio_fig = px.bar(
            studios_count,
            x=studios_count.index,
            y=studios_count.values,
            labels={'x': 'Studio', 'y': "Nombre d'animes produits"},
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
        sorted_data = filtered_data.sort_values(by='episodes', ascending=True)
        
        episode_fig = px.bar(
            sorted_data,
            x='episodes',
            y='titre',
            orientation='h',  
            labels={'x': "Nombre d'épisodes", 'y': 'Anime'},
            title="Histogramme du nombre d'épisodes"
        )
        st.plotly_chart(episode_fig)

    # Scatter plot sur les producteurs
    st.subheader("Etude sur les producteurs")
    data_exploded = data.assign(producteurs=data['producteurs'].str.split(',')).explode('producteurs')
    data_exploded['producteurs'] = data_exploded['producteurs'].str.strip()
    producteurs_count = data_exploded['producteurs'].value_counts().reset_index()
    producteurs_count.columns = ['producteur', 'nombre_productions']

    merged_data = pd.merge(
        data_exploded,
        producteurs_count,
        left_on='producteurs',
        right_on='producteur',
        how='left'
    )

    scatter_fig = px.scatter(
        merged_data,
        x='rank',
        y='nombre_productions',
        color='producteurs',
        size='score',
        hover_name='titre',
        labels={'rank': 'Rang', 'nombre_productions': 'Nombre de Productions'},
        title="Rang des animes et producteurs les plus actifs"
    )
    st.plotly_chart(scatter_fig)


else:
    st.warning("Aucune donnée disponible dans la base de données.")

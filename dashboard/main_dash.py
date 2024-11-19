import streamlit as st
from tab_classement import dashboard_anime_classement
from tab_recherche import dashboard_preferences_utilisateur

# Créez les onglets
st.set_page_config(page_title="Dashboard Anime")

tab1, tab2 = st.tabs(["Classement des Animes", "Recherche en fonction du genre et du thème"])

with tab1:
    dashboard_anime_classement()

with tab2:
    dashboard_preferences_utilisateur()

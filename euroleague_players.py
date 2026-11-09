import streamlit as st
import pandas as pd
import plotly.express as px
import nbformat

data = pd.read_csv("./euroleague_players.csv")
data["season"] = data["season_code"].str.replace('E', '', regex=False).astype(int)
data = data[["player", "season", "team_id", "games_started", "games_played", "minutes", "points", "assists", "total_rebounds", "steals"]]


# configuration de base de la page: première commande du fichier
st.set_page_config(
    page_title="EuroLeague players",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ajout du menu
page = st.sidebar.selectbox(
    "Navigation",
    ["Homepage", "Stats", "Graphs"]
)

# définition de la page d'accueil
if page == "Homepage":

    # Ajouter une image depuis une URL publique (version moderne)
    
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/9/90/EuroLeague_logo.svg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original",
        caption="Every game matters.",
        use_container_width=True
    )

    st.title("Welcome to the EuroLeague players Dashboard ")

    # Texte introductif
    st.write(
        "Dive in for more insights!"
    )

    # Lien vers les sources officielles
    st.markdown(
        "To know more about the Euroleague championship, visit [Euroleague's official website](https://www.euroleaguebasketball.net/en/euroleague/)."
    )

    st.markdown(
        "To download the datased, visit [Kaggle](https://www.kaggle.com/datasets/babissamothrakis/euroleague-datasets)."
    )

# définition de la page analyse
elif page == "Stats":

    col1, col2, col3 = st.columns(3)
    col1.image("./decolo.png", caption = "Nando De Colo")
    col2.image("./francisco.png", caption = "Sylvain Francisco")
    col3.image("./strazel.png", caption = "Matthew Strazel")



    st.title("Player stats")
    st.write("A quick overview of great players' achievments")
    
    # Widgets interactifs
    option = st.selectbox(
        "Pick a player",
        ["DE COLO, NANDO", "FRANCISCO, SYLVAIN", "STRAZEL, MATTHEW"]
    )
    valeur = st.slider(
        "How many seasons would you like to analyze?", 0, 20, 3
    )
    
    st.write(f"Player : {option}")
    st.write(f"Seasons under review - backwards analysis (2026 = year 0) : {valeur}")

    data_filtered = data[(data["player"]== option) & (data["season"] >= (2026 - valeur))]

    st.table(data_filtered)
    
    # Bouton pour télécharger le tableau
    st.download_button(
        label="Download player stats",
        data=data_filtered.to_csv(index=False).encode('utf-8'),
        file_name='player_stats.csv',
        mime='text/csv'
    )


# page graphique
elif page == "Graphs":

    st.image(
            "./french_co.jpg",
            caption="Panathinaikos' French connection"
        )

    st.title("Compare stats of the French players that are currently playing for Panathinaikos")

    selected_players = st.multiselect(
    "Pick your player(s)", 
    ["FRANCISCO, SYLVAIN", "LESSORT, MATHIAS", "YABUSELE, GUERSCHON", "FALL, MOUSTAPHA"]
    )

    stat = st.selectbox(
    "Which stat are you interested in?", 
    ["games_started", "games_played", "minutes", "points", "assists", "total_rebounds", "steals"]
    )


        # Graphique Plotly interactif
    st.subheader(f"Evolution of {stat} over the seasons")
    
    chart_filter = data[data["player"].isin(selected_players)]

    fig = px.line(
        chart_filter,
        x="season",
        y=stat,
        color = "player"
    )

    fig.update_xaxes(dtick=1)
    
    st.plotly_chart(fig)
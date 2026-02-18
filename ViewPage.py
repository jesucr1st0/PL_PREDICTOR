import streamlit as st
import base64
import joblib
import pandas as pd
from FunctionsModel import predict_match

# Cargar CSV
df1 = pd.read_csv("data/pl_23_24.csv")
df2 = pd.read_csv("data/pl_24_25.csv")
df3 = pd.read_csv("data/pl_25_26.csv")

df = pd.concat([df1, df2, df3], ignore_index=True)

# Convertir fecha
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

st.set_page_config(layout="wide")

def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
model = joblib.load("model/model.pkl")
team_encoder = joblib.load("model/team_encoder.pkl")
result_encoder = joblib.load("model/result_encoder.pkl")

# -------- CSS PRO --------
st.markdown("""
<style>
body {
    background-color: #0f2f1f;
}

h1 {
    text-align: center;
    color: #00ff88;
    font-weight: 800;
}

.team-card {
    text-align: center;
    padding: 10px;
}

.team-card img {
    border-radius: 20px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.team-card img:hover {
    transform: scale(1.1);
    box-shadow: 0px 0px 25px rgba(0,255,120,0.9);
    cursor: pointer;
}

.selected img {
    box-shadow: 0px 0px 35px rgba(0,255,120,1);
    transform: scale(1.1);
}
            
/* 🔥 CENTRADO REAL DEL BOTÓN */
div[data-testid="stButton"] {
    text-align: center;
}

div[data-testid="stButton"] > button {
    width: 130px;        /* mismo ancho que la imagen */
    padding: 10px;
    margin: 0 auto;      
}
</style>
""", unsafe_allow_html=True)



st.markdown("<h1>⚽ Premier League Predictor</h1>", unsafe_allow_html=True)

# -------- EQUIPOS --------
teams = {
    "Arsenal": "assets/arsenal.png",
    "Chelsea": "assets/chelsea.png",
    "Liverpool": "assets/liverpool.png",
    "Man. City": "assets/manchestercity.png",
    "Man. United": "assets/manchesterunited.png",
    "Tottenham": "assets/tottenham.png",
    "Newcastle": "assets/newcastle.png",
    "Brighton": "assets/brighton.png",
    "Aston Villa": "assets/astonvilla.png",
    "West Ham": "assets/westham.png",
    "Brentford": "assets/brentford.png",
    "Crystal Palace": "assets/crystalpalace.png",
    "Everton": "assets/everton.png",
    "Fulham": "assets/fulham.png",
    "Bournemouth": "assets/bournemouth.png",
    "Wolves": "assets/wolves.png",
    "Burnley": "assets/burnley.png",
    "Nottingham": "assets/nottingham_forest.png",
    "Leeds United": "assets/leeds.png",
    "Sunderland": "assets/sunderland.png",
}

# -------- SESSION STATE --------
if "home_team" not in st.session_state:
    st.session_state.home_team = None

if "away_team" not in st.session_state:
    st.session_state.away_team = None

if "selection_mode" not in st.session_state:
    st.session_state.selection_mode = "home"

# -------- MENSAJE SUPERIOR --------
if st.session_state.selection_mode == "home":
    msg = "Selecciona el equipo LOCAL"
elif st.session_state.selection_mode == "away":
    msg = "Selecciona el equipo VISITANTE"
else:
    msg = "Equipos seleccionados"

st.markdown(
    f"""
    <div style="
        text-align:center;
        background:#0f2f1f;
        border:2px solid #00ff88;
        color:#00ff88;
        padding:15px;
        border-radius:15px;
        width:400px;
        margin:0 auto 30px auto;
        font-weight:bold;
        font-size:18px;
    ">
        {msg}
    </div>
    """,
    unsafe_allow_html=True
)
# -------- GRID 5x4 --------
cols_per_row = 5
teams_list = list(teams.items())

for i in range(0, len(teams_list), cols_per_row):
    cols = st.columns(cols_per_row)
    for col, (team, logo) in zip(cols, teams_list[i:i+cols_per_row]):
        with col:
            img_base64 = get_base64_image(logo)


            selected_class = ""
            if team == st.session_state.home_team or team == st.session_state.away_team:
                selected_class = "selected"

            # BOTÓN REAL (visible)
            if st.button(team, key=f"btn_{team}",  use_container_width=True):

                if st.session_state.selection_mode == "home":
                    st.session_state.home_team = team
                    st.session_state.selection_mode = "away"

                elif st.session_state.selection_mode == "away":
                    if team != st.session_state.home_team:
                        st.session_state.away_team = team
                        st.session_state.selection_mode = "done"

            # IMAGEN
            st.markdown(
                f"""
                <div class="team-card {selected_class}">
                    <img src="data:image/png;base64,{img_base64}" width="130">
                </div>
                """,
                unsafe_allow_html=True
            )

# -------- MOSTRAR VS --------
if st.session_state.home_team and st.session_state.away_team:

    st.markdown("---")

    col1, col2, col3 = st.columns([2,1,2])
    home_logo = get_base64_image(teams[st.session_state.home_team])
    away_logo = get_base64_image(teams[st.session_state.away_team])

    with col1:
     if st.session_state.home_team:
        st.markdown(
             f"""
             <div style="text-align:center">
                 <img src="data:image/png;base64,{home_logo}" width="130">
                 <h3>{st.session_state.home_team}</h3>
             </div>
             """,
             unsafe_allow_html=True
        )

    with col2:
     st.markdown(
        "<h2 style='text-align:center'>VS</h2>",
        unsafe_allow_html=True
     )

    with col3:
     if st.session_state.away_team:
        st.markdown(
             f"""
             <div style="text-align:center">
                 <img src="data:image/png;base64,{away_logo}" width="130">
                 <h3>{st.session_state.away_team}</h3>
             </div>
             """,
             unsafe_allow_html=True
        )
    

    with col2:

     st.markdown("###  Selecciona la fecha ")

     match_date = st.date_input("Fecha del partido")

     st.markdown("<br>", unsafe_allow_html=True)

     if st.button("🔮 Predecir ", use_container_width=True):
         result = predict_match(
            st.session_state.home_team,
            st.session_state.away_team,
            st.session_state.match_date,
            df
         )

         st.success(f"Predicción: {result}")

     st.markdown("<br>", unsafe_allow_html=True)

     if st.button("🔄 Reiniciar ", use_container_width=True):
        st.session_state.home_team = None
        st.session_state.away_team = None
        st.session_state.selection_mode = "home"
        st.rerun()
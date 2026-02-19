import streamlit as st
import base64
import joblib
import pandas as pd
from FunctionsModel import predict_match

# Cargar CSV
df = pd.read_csv("data/clean_matches.csv")



# Convertir fecha
df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True)

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
    transition: box-shadow 0.25s ease;
}

.selected img {
    box-shadow: 0px 0px 35px rgba(0,255,120,1);
    border: 2px solid #00ff88;
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
    "Man City": "assets/manchestercity.png",
    "Man United": "assets/manchesterunited.png",
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
    "Nott'm Forest": "assets/nottingham_forest.png",
    "Leeds": "assets/leeds.png",
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
            selected_class = "selected" if team in [st.session_state.home_team, st.session_state.away_team] else ""

            # 1. Mostramos la imagen con el estilo CSS que ya tienes
            st.markdown(
                f"""
                <div class="team-card {selected_class}">
                    <img src="data:image/png;base64,{img_base64}" width="130">
                </div>
                """,
                unsafe_allow_html=True
            )

            # 2. El botón justo debajo (es el que captura el evento)
            if st.button(f"Seleccionar", key=f"btn_{team}", use_container_width=True):
                if st.session_state.selection_mode == "home":
                    st.session_state.home_team = team
                    st.session_state.selection_mode = "away"
                    st.rerun()
                elif st.session_state.selection_mode == "away" and team != st.session_state.home_team:
                    st.session_state.away_team = team
                    st.session_state.selection_mode = "done"
                    st.rerun()

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

     st.session_state.match_date = st.date_input("Fecha del partido")

     st.markdown("<br>", unsafe_allow_html=True)

     if st.button(" Predecir ", use_container_width=True):
        result = predict_match(
            st.session_state.home_team,
            st.session_state.away_team,
            st.session_state.match_date,
            df
        )

        st.success(
            f"""
            RESULTADO SIMULADO

            {st.session_state.home_team} {result["home_goals"]} - {result["away_goals"]} {st.session_state.away_team}

            Probabilidades:
            Local: {result['probs'][0]:.2%}
            Empate: {result['probs'][1]:.2%}
            Visitante: {result['probs'][2]:.2%}
            """
        )

     st.markdown("<br>", unsafe_allow_html=True)

     if st.button(" Reiniciar ", use_container_width=True):
        st.session_state.home_team = None
        st.session_state.away_team = None
        st.session_state.selection_mode = "home"
        st.rerun()
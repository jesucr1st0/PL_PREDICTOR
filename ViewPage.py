import streamlit as st
import base64

st.set_page_config(layout="wide")
def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

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
    padding: 15px;
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
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚽ Premier League Predictor</h1>", unsafe_allow_html=True)

# -------- EQUIPOS --------
teams = {
    "Arsenal": "assets/arsenal.png",
    "Chelsea": "assets/chelsea.png",
    "Liverpool": "assets/liverpool.png",
    "Manchester City": "assets/manchestercity.png",
    "Manchester United": "assets/manchesterunited.png",
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
    "Nottingham Forest": "assets/nottingham_forest.png",
    "Leeds United": "assets/leeds.png",
    "Sunderland": "assets/sunderland.png",
}

# -------- SESSION STATE --------
if "selected_team" not in st.session_state:
    st.session_state.selected_team = None

# -------- GRID 5x4 --------
cols_per_row = 5
teams_list = list(teams.items())

for i in range(0, len(teams_list), cols_per_row):
    cols = st.columns(cols_per_row)
    for col, (team, logo) in zip(cols, teams_list[i:i+cols_per_row]):
        with col:
            img_base64 = get_base64_image(logo)

            selected_class = "selected" if st.session_state.selected_team == team else ""

            # Imagen clickeable real
            clicked = st.markdown(
                f"""
                <div class="team-card {selected_class}">
                    <a href="?team={team}">
                        <img src="data:image/png;base64,{img_base64}" width="130">
                    </a>
                    <p style="color:white;">{team}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# -------- CAPTURAR CLICK --------
query_params = st.query_params
if "team" in query_params:
    st.session_state.selected_team = query_params["team"]

# -------- RESULTADO --------
if st.session_state.selected_team:
    st.success(f"Equipo seleccionado: {st.session_state.selected_team}")

# -------- CAPTURAR CLICK --------
query_params = st.query_params
if "team" in query_params:
    st.session_state.selected_team = query_params["team"]

# -------- RESULTADO --------
if st.session_state.selected_team:
    st.success(f"Equipo seleccionado: {st.session_state.selected_team}") 
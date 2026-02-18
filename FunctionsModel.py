import joblib
import pandas as pd

model = joblib.load("model/model.pkl")
team_encoder = joblib.load("model/team_encoder.pkl")
result_encoder = joblib.load("model/result_encoder.pkl")

# Función auxiliar que procesa las estadísticas de los últimos 5
# partidos para pasar las features al modelo.
def get_team_stats(team, date, df, n=5):

    date = pd.to_datetime(date, dayfirst=True)

    past = df[df["Date"] < date]

    # últimos partidos como LOCAL
    home = past[past["HomeTeam"] == team].tail(n)

    # últimos partidos como VISITANTE
    away = past[past["AwayTeam"] == team].tail(n)

    stats = {}

    # columnas que dependen de local
    home_cols = ["HS","HST","HC","HY","HR"]

    # columnas que dependen de visitante
    away_cols = ["AS","AST","AC","AY","AR"]

    # odds (usamos solo cuando fue local)
    odds_cols = ["AvgH","AvgD","AvgA"]

    for col in home_cols:
        stats[col] = home[col].mean() if len(home) > 0 else df[col].mean()

    for col in away_cols:
        stats[col] = away[col].mean() if len(away) > 0 else df[col].mean()

    for col in odds_cols:
        stats[col] = home[col].mean() if len(home) > 0 else df[col].mean()

    return stats

# Función que predice en sí el partido
def predict_match(home_team, away_team, date, df):

    date = pd.to_datetime(date, dayfirst=True)

    home_stats = get_team_stats(home_team, date, df, 10)
    away_stats = get_team_stats(away_team, date, df, 10)

    input_dict = {

        "HomeTeam_enc": team_encoder.transform([home_team])[0],
        "AwayTeam_enc": team_encoder.transform([away_team])[0],

        "HS": home_stats["HS"] - away_stats["AS"],
        "AS": away_stats["AS"] - home_stats["HS"],

        "HST": home_stats["HST"],
        "AST": away_stats["AST"],

        "HC": home_stats["HC"],
        "AC": away_stats["AC"],

        "HY": home_stats["HY"],
        "AY": away_stats["AY"],

        "HR": home_stats["HR"],
        "AR": away_stats["AR"],

        "AvgH": home_stats["AvgH"] / 10,
        "AvgD": home_stats["AvgD"] / 10,
        "AvgA": home_stats["AvgA"] / 10,
    }

    input_df = pd.DataFrame([input_dict])

    input_df = input_df[model.feature_names_in]

    pred = model.predict(input_df)[0]

    probs = model.predict_proba(input_df)[0]

    print("Probabilidades:")
    print(f"Home win: {probs[ result_encoder.transform(['H'])[0] ]:.3f}")
    print(f"Draw: {probs[ result_encoder.transform(['D'])[0] ]:.3f}")
    print(f"Away win: {probs[ result_encoder.transform(['A'])[0] ]:.3f}")

    return result_encoder.inverse_transform([pred])[0]



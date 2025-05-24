from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib

app = Flask(__name__, static_folder="static")
CORS(app)

# Load the trained goalie model
goalie_model = joblib.load("goalie_model.pkl")

@app.route("/")
def serve_estimator():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/estimate", methods=["POST"])
def estimate():
    data = request.json
    player_type = data.get("PlayerType")

    # Shared fields
    age = data.get("Age", 0)
    is_rfa = data.get("IsRFA", 0)
    cap_norm = data.get("CapSpaceNormalized", 0)

    if player_type == "Goalie":
        # Use trained goalie model
        games = data.get("GamesStarted", 0)
        xg = data.get("xG", 0)
        yl = data.get("YL", 1)
        length = data.get("Length", 2)

        features = [games, xg, age, is_rfa, yl, length]
        prediction = goalie_model.predict([features])[0]

        return jsonify({"EstimatedAAV": round(prediction / 1_000_000, 2)})

    elif player_type == "Defenseman":
        # Defenseman-specific fields
        goals = data.get("GoalsPerGame", 0)
        assists = data.get("AssistsPerGame", 0)
        toi = data.get("TOIPerGame", 0)
        plusminus = data.get("PlusMinus", 0)
        cf = data.get("CF_percent", 0)
        xg = data.get("xG", 0)
        hits = data.get("HitsPerGame", 0)
        blocks = data.get("BlockedShotsPerGame", 0)
        takeaways = data.get("TakeawaysPerGame", 0)
        turnovers = data.get("TurnoversPerGame", 0)
        missed = data.get("GamesMissed", 0)

        base = (
            (goals + assists) * 3 + (toi * 0.1) + plusminus +
            (cf - 50) * 0.2 + (xg * 0.5) +
            (hits + blocks + takeaways) * 0.3 -
            (turnovers * 0.3) -
            (missed * 0.1) +
            (1 if is_rfa else 0) +
            (1 - abs(age - 27) * 0.1) +
            (cap_norm * 2)
        )
        estimated_aav = round(max(base, 0), 2)
        return jsonify({"EstimatedAAV": estimated_aav})

    else:
        # Forward/general skater logic
        goals = data.get("GoalsPerGame", 0)
        assists = data.get("AssistsPerGame", 0)
        toi = data.get("TOIPerGame", 0)
        plusminus = data.get("PlusMinus", 0)
        cf = data.get("CF_percent", 0)
        xg = data.get("xG", 0)
        missed = data.get("GamesMissed", 0)

        base = (
            (goals + assists) * 4 + (toi * 0.1) + plusminus +
            (cf - 50) * 0.2 + (xg * 0.5) -
            (missed * 0.1) +
            (1 if is_rfa else 0) +
            (1 - abs(age - 27) * 0.1) +
            (cap_norm * 2)
        )
        estimated_aav = round(max(base, 0), 2)
        return jsonify({"EstimatedAAV": estimated_aav})

if __name__ == "__main__":
    app.run(debug=True)

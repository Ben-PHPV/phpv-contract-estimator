from flask import Flask, request, jsonify

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "NHL Contract Estimator is live!"

# Contract estimation route
@app.route('/estimate', methods=['POST'])
def estimate():
    data = request.json

    # Get input values from JSON request
    goals = data.get("GoalsPerGame", 0)
    assists = data.get("AssistsPerGame", 0)
    toi = data.get("TOIPerGame", 0)
    plus_minus = data.get("PlusMinus", 0)
    cf = data.get("CF_percent", 50)
    xg = data.get("xG", 0)
    age = data.get("Age", 0)
    is_rfa = int(data.get("IsRFA", 0))
    games_missed = data.get("GamesMissed", 0)
    cap_space = data.get("CapSpaceNormalized", 0)
    position = data.get("Position", "Center")

    # Encode position to numerical effect (example values)
    position_offset = {
        "Center": 0,
        "Winger": 0.2,
        "Defenseman": -0.3,
        "Goalie": -0.6
    }.get(position, 0)

    # Estimate AAV using linear model
    estimated_aav = (
        1.25 +                         # Intercept
        3.0 * goals +
        2.5 * assists +
        0.1 * toi +
        0.05 * plus_minus +
        0.2 * cf +
        0.12 * xg +
        -0.08 * age +
        0.9 * is_rfa +
        -0.05 * games_missed +
        4.0 * cap_space +
        position_offset
    )

    return jsonify({"EstimatedAAV": round(estimated_aav, 2)})



from flask_cors import CORS
from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the trained model
with open("goalie_model.pkl", "rb") as f:
    model = pickle.load(f)

# Define expected feature order (must match training)
FEATURE_ORDER = [
    "low_danger_pct", "medium_danger_pct", "high_danger_sv_pct", "sv_pct",
    "xGoals", "goals", "rebounds", "freeze", "ongoal", "saves",
    "games_played", "icetime",
    "Cap_hit_pct", "YL", "Length", "IsRFA"
]

@app.route("/")
def home():
    return "🏒 NHL Goalie Contract Estimator API is running."

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect inputs in the correct order
        input_data = []
        for feature in FEATURE_ORDER:
            val = request.form.get(feature)
            if val is None:
                return jsonify({"error": f"Missing value for: {feature}"}), 400
            input_data.append(float(val))

        # Convert to NumPy array
        input_array = np.array(input_data).reshape(1, -1)

        # Predict using the model
        prediction = model.predict(input_array)[0]
        prediction_rounded = round(prediction, 2)

        return jsonify({
            "estimated_AAV": prediction_rounded,
            "currency": "USD"
        })

    except Exception as e:
        return jsonify({"error": f"Error calculating estimate: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

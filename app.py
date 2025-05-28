from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for cross-origin requests (e.g., from WordPress)

# Load trained model
model_path = "goalie_model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Cannot find model at {model_path}")

with open(model_path, "rb") as f:
    model = pickle.load(f)

# Must match training feature order
FEATURE_ORDER = [
    "low_danger_pct", "medium_danger_pct", "high_danger_sv_pct", "sv_pct",
    "xGoals", "goals", "rebounds", "freeze", "ongoal", "saves",
    "games_played", "icetime",
    "Cap_hit_pct", "YL", "Length", "IsRFA"
]

@app.route("/")
def home():
    return "✅ Goalie contract estimator backend is running."

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = []
        for feature in FEATURE_ORDER:
            val = request.form.get(feature)
            if val is None:
                return jsonify({"error": f"Missing value: {feature}"}), 400
            input_data.append(float(val))

        # Predict and round result
        prediction = model.predict(np.array(input_data).reshape(1, -1))[0]
        return jsonify({"estimated_AAV": round(prediction, 2)})

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


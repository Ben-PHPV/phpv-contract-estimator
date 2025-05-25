from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# Load updated model
with open("goalie_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return "NHL Goalie Estimator API is running!"

@app.route("/predict-goalie", methods=["POST"])
def predict_goalie():
    try:
        data = request.json
        print("Received data:", data)

        features = np.array([[
            data["HighDangerSV%"],
            data["MediumDangerSV%"],
            data["LowDangerSV%"],
            data["SavePercentage"],
            data["GAA"],
            data["Rebounds"],
            data["Freeze"],
            data["OnGoalShots"]
        ]])

        prediction = model.predict(features)[0]
        return jsonify({"prediction": round(prediction, 3)})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

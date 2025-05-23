from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "PHPV Contract Estimator is live!"

@app.route('/estimate', methods=['POST'])
def estimate():
    return jsonify({"message": "POST to /estimate is working!"})

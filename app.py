"""
app.py - Flask web app for the Data Usage Advisor
Serves the frontend and exposes /analyze + /whatif API endpoints
"""

from flask import Flask, request, jsonify, render_template
from advisor import analyze, whatif_simulation

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_usage():
    """
    POST /analyze
    Body (JSON):
      {
        "daily_hours": 6,
        "streams_video": 1,
        "num_downloads": 5,
        "social_media_hours": 2
      }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required = ["daily_hours", "streams_video", "num_downloads", "social_media_hours"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        result = analyze(
            float(data["daily_hours"]),
            int(data["streams_video"]),
            int(data["num_downloads"]),
            float(data["social_media_hours"])
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/whatif", methods=["POST"])
def whatif():
    """
    POST /whatif
    Same body as /analyze — returns what-if scenarios only
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    try:
        scenarios = whatif_simulation(
            float(data["daily_hours"]),
            int(data["streams_video"]),
            int(data["num_downloads"]),
            float(data["social_media_hours"])
        )
        return jsonify({"whatif_scenarios": scenarios})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

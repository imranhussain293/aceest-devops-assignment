from flask import Flask, jsonify

app = Flask(__name__)

PROGRAMS = [
    {"name": "Fat Loss (FL)", "calorie_factor": 22},
    {"name": "Muscle Gain (MG)", "calorie_factor": 35},
    {"name": "Beginner (BG)", "calorie_factor": 26},
]

@app.get("/programs")
def get_programs():
    return jsonify({"programs": PROGRAMS})

@app.get("/health")
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

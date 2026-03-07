from flask import Flask, jsonify, request

app = Flask(__name__)

PROGRAMS = [
    {"name": "Fat Loss (FL)", "calorie_factor": 22},
    {"name": "Muscle Gain (MG)", "calorie_factor": 35},
    {"name": "Beginner (BG)", "calorie_factor": 26},
]

PROGRAM_FACTORS = {p["name"]: p["calorie_factor"] for p in PROGRAMS}

@app.post("/clients")
def create_client():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    weight = data.get("weight")
    program = data.get("program")

    if not all([name, age, weight, program]):
        return jsonify({"error": "Missing required fields"}), 400

    if program not in PROGRAM_FACTORS:
        return jsonify({"error": "Invalid program"}), 400

    calories = weight * PROGRAM_FACTORS[program]

    client = {
        "name": name,
        "age": age,
        "weight": weight,
        "program": program,
        "calories": calories
    }

    return jsonify({"client": client}), 201


@app.get("/programs")
def get_programs():
    return jsonify({"programs": PROGRAMS})

@app.get("/health")
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

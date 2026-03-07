import os
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_db_path():
    return os.environ.get("DATABASE_PATH", "aceest_fitness.db")

def get_db_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            age INTEGER,
            weight REAL NOT NULL,
            program TEXT NOT NULL,
            calories INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            week TEXT NOT NULL,
            adherence INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

PROGRAMS = [
    {"name": "Fat Loss (FL)", "calorie_factor": 22},
    {"name": "Muscle Gain (MG)", "calorie_factor": 35},
    {"name": "Beginner (BG)", "calorie_factor": 26},
]

PROGRAM_FACTORS = {p["name"]: p["calorie_factor"] for p in PROGRAMS}

@app.post("/clients")
def create_client():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    age = data.get("age")
    weight = data.get("weight")
    program = (data.get("program") or "").strip()

    #validate required fields

    if not name:
        return jsonify({"error": "name is required"}), 400
    if not program:
        return jsonify({"error": "program is required"}), 400
    if program not in PROGRAM_FACTORS:
        return jsonify({"error": "Invalid program"}), 400
        
    #validate numeric weight
    try:
        weight = float(weight)
    except (TypeError, ValueError):
        return jsonify({"error": "weight must be a number"}), 400

    if weight <= 0:
        return jsonify({"error": "weight must be greater than zero"}), 400

    #age is optional but if provided must be a positive integer
    if age is not None:
        try:
            age = int(age)
        except (TypeError, ValueError):
            return jsonify({"error": "age must be an integer"}), 400
        if age <= 0:
            return jsonify({"error": "age must be greater than zero"}), 400

    calories = int(weight * PROGRAM_FACTORS[program])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO clients (name, age, weight, program, calories)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, age, weight, program, calories),
    )
    conn.commit()
    conn.close()


    client = {
        "name": name,
        "age": age,
        "weight": weight,
        "program": program,
        "calories": calories
    }

    return jsonify({"client": client}), 201

@app.get("/clients/<string:name>")
def get_client(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, age, weight, program, calories FROM clients WHERE name=?",
        (name,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Client not found"}), 404
    
    return jsonify({"client": dict(row)}), 200

@app.get("/programs")
def get_programs():
    return jsonify({"programs": PROGRAMS})

@app.get("/health")
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

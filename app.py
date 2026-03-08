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

    # Clean up any existing duplicates (keeps the earliest row)
    cursor.execute("""
        DELETE FROM progress
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM progress
            GROUP BY client_name, week
        )
    """)

    # Enforce "one progress entry per client per week"
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS progress_unique_client_week
        ON progress (client_name, week)
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

    if row is None:
        conn.close()
        return jsonify({"error": "Client not found"}), 404

    cursor.execute(
        "SELECT week, adherence FROM progress WHERE client_name=? ORDER BY id DESC LIMIT 10",
        (name,),
    )
    progress_rows = cursor.fetchall()
    conn.close()

    return jsonify(
        {
            "client": {
                "name": row["name"],
                "age": row["age"],
                "weight": row["weight"],
                "program": row["program"],
                "calories": row["calories"],
            },
            "progress": [
                {"week": progress_row["week"], "adherence": progress_row["adherence"]}
                for progress_row in progress_rows
            ],
        }
    )


@app.post("/clients/<string:name>/progress")
def log_progress(name):
    data = request.get_json(silent=True) or {}
    adherence = data.get("adherence")
    week = (data.get("week") or "").strip()

    if not week:
        return jsonify({"error": "week is required"}), 400

    try:
        adherence = int(adherence)
    except (TypeError, ValueError):
        return jsonify({"error": "adherence must be an integer"}), 400

    if not (0 <= adherence <= 100):
        return jsonify({"error": "adherence must be between 0 and 100"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO progress (client_name, week, adherence) VALUES (?, ?, ?)",
        (name, week, adherence),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Progress logged successfully"}), 201

@app.get("/programs")
def get_programs():
    return jsonify({"programs": PROGRAMS})

@app.get("/health")
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

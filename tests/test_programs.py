from app import app


def test_programs_endpoint_returns_expected_programs():
    client = app.test_client()
    response = client.get("/programs")

    assert response.status_code == 200

    data = response.get_json()
    assert "programs" in data

    programs = data["programs"]
    names = {p["name"] for p in programs}

    assert {"Fat Loss (FL)", "Muscle Gain (MG)", "Beginner (BG)"}.issubset(names)

    factors = {p["name"]: p["calorie_factor"] for p in programs}
    assert factors["Fat Loss (FL)"] == 22
    assert factors["Muscle Gain (MG)"] == 35
    assert factors["Beginner (BG)"] == 26

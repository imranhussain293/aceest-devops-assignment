from app import app

def test_create_client_calculates_calories_and_persists():
    client = app.test_client()

    response = client.post(
        "/clients",
        json={
            "name": "JohnDoe",
            "age": 30,
            "weight": 70,
            "program": "Fat Loss (FL)",
        },
    )
    assert response.status_code == 201

    data = response.get_json()
    assert "client" in data

    created = data["client"]
    assert created["name"] == "JohnDoe"
    assert created["program"] == "Fat Loss (FL)"
    assert created["calories"] == 1540  # 70 * 22

    get_response = client.get("/clients/JohnDoe")
    assert get_response.status_code == 200

    stored = get_response.get_json()["client"]
    assert stored["calories"] == 1540
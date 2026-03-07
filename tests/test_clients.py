from app import app

def test_create_client_calculates_calories():
    client = app.test_client()

    response = client.post(
        "/clients",
        json={
            "name": "John Doe",
            "age": 30,
            "weight": 70,
            "program": "Fat Loss (FL)"
        },
    )

    assert response.status_code == 201

    data = response.get_json()
    assert "client" in data

    created = data["client"]
    assert created["name"] == "John Doe"
    assert created["program"] == "Fat Loss (FL)"
    assert created["calories"] == 1540  # 70 * 22
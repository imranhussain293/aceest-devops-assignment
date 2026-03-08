from app import app

def test_log_progress_for_client_and_read_back():
    client = app.test_client()

    # Create a client first
    client.post(
        "/clients",
        json={
            "name": "Alice",
            "age": 30,
            "weight": 70,
            "program": "Muscle Gain (MG)",
        },
    )

    # Log progress for the client
    response = client.post(
        "/clients/Alice/progress",
        json={"adherence": 90, "week": "Week 10 - 2026"}
    )
    assert response.status_code == 201

    # Read back the client's data
    get_response = client.get("/clients/Alice")
    assert get_response.status_code == 200

    data = get_response.get_json()
    assert "progress" in data
    progress = data["progress"]
    assert len(progress) == 1
    assert progress[0]["adherence"] == 90
    assert progress[0]["week"] == "Week 10 - 2026"
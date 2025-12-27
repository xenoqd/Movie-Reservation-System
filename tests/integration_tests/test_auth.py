def test_register_endpoint(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "Testuser0",
            "email": "TestEmail@gmail.com",
            "password": "TestPass",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == "Testuser0"


def test_login_endpoint(client):
    registration_response = client.post(
        "/auth/register",
        json={
            "username": "Testuser",
            "email": "TestEmail@gmail.com",
            "password": "TestPass",
        },
    )

    assert registration_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={
            "login": "Testuser",
            "password": "TestPass",
        },
    )

    assert login_response.status_code == 200

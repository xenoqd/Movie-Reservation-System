from backend.core.security.jwt import create_access_token


def test_create_movie_endpoint(client):
    token = create_access_token(
        data={
        "sub": "1", 
        "role": "admin"
        }
    )
    client.cookies.set("access_token", token)

    response = client.post(
        "/admin/movies/create_movie",
        json={
            "title": "string",
            "description": "string",
            "poster_url": "string",
            "genre": "action",
        },
    )

    assert response.status_code == 200


def test_edit_movie_endpoint(client):
    token = create_access_token(
        data={
        "sub": "1", 
        "role": "admin"
        }
    )

    client.cookies.set("access_token", token)

    response = client.post(
        "/admin/movies/create_movie",
        json={
            "title": "string",
            "description": "string",
            "poster_url": "string",
            "genre": "action",
        },
    )
    assert response.status_code == 200

    movie_id = response.json()["id"]

    resp_patch = client.patch(
        f"/admin/movies/{movie_id}",
        json={
            "title": "Patched title",
            "description": "string",
            "poster_url": "string",
            "genre": "action"
        },
    )

    assert resp_patch.status_code == 200


def test_delete_movie_endpoint(client):
    token = create_access_token(
        data={
        "sub": "1", 
        "role": "admin"
        }
    )

    client.cookies.set("access_token", token)

    response = client.post(
        "/admin/movies/create_movie",
        json={
            "title": "string",
            "description": "string",
            "poster_url": "string",
            "genre": "action",
        },
    )
    assert response.status_code == 200

    movie_id = response.json()["id"]

    resp_delete = client.delete(
        f"admin/movies/{movie_id}"
    )

    assert resp_delete.status_code == 200
from backend.core.security.jwt import create_access_token


def test_create_showtime_endpoint(client):
    token = create_access_token(
        data={
            "sub": "1",
            "role": "admin"
        }
    )
    client.cookies.set("access_token", token)

    response_movie = client.post(
        "/admin/movies/create_movie",
        json={
            "title": "string",
            "description": "string",
            "poster_url": "string",
            "genre": "action",
        },
    )

    assert response_movie.status_code == 200

    movie_id = response_movie.json()["id"]

    response = client.post(
        "/admin/showtime",
        json={
            "movie_id": movie_id,
            "starts_at": "2025-12-27T05:16:09.116095Z",
            "ends_at": "2025-12-27T05:16:09.116095Z",
            "hall_number": 0,
            "capacity": 60
        },
    )

    assert response.status_code == 200


def test_update_showtime_endpoint(client):
    token = create_access_token(
        data={
            "sub": "1",
            "role": "admin"
        }
    )
    client.cookies.set("access_token", token)

    response_movie = client.post(
        "/admin/movies/create_movie",
        json={
            "title": "string",
            "description": "string",
            "poster_url": "string",
            "genre": "action",
        },
    )

    assert response_movie.status_code == 200

    movie_id = response_movie.json()["id"]

    response = client.post(
        "/admin/showtime",
        json={
            "movie_id": movie_id,
            "starts_at": "2025-12-27T05:16:09.116095Z",
            "ends_at": "2025-12-27T05:16:09.116095Z",
            "hall_number": 0,
            "capacity": 60
        },
    )

    assert response.status_code == 200

    showtime_id = response_movie.json()["id"]

    response_showtime = client.patch(
        f"/admin/showtime/{showtime_id}",
        json={
            "movie_id": movie_id,
            "starts_at": "2025-12-27T06:22:16.328Z",
            "ends_at": "2025-12-27T06:22:16.328Z",
            "hall_number": 0,
            "capacity": 35
        }
    )

    assert response_showtime.status_code == 200


def test_delete_showtime_endpoint(client):
    token = create_access_token(
        data={
            "sub": "1",
            "role": "admin"
        }
    )
    client.cookies.set("access_token", token)

    response_movie = client.post(
        "/admin/movies/create_movie",
        json={
            "title": "string",
            "description": "string",
            "poster_url": "string",
            "genre": "action",
        },
    )

    assert response_movie.status_code == 200

    movie_id = response_movie.json()["id"]

    response = client.post(
        "/admin/showtime",
        json={
            "movie_id": movie_id,
            "starts_at": "2025-12-27T05:16:09.116095Z",
            "ends_at": "2025-12-27T05:16:09.116095Z",
            "hall_number": 0,
            "capacity": 60
        },
    )

    assert response.status_code == 200

    showtime_id = response_movie.json()["id"]

    response_showtime = client.patch(
        f"/admin/showtime/{showtime_id}",
        json={
            "movie_id": movie_id,
            "starts_at": "2025-12-27T06:22:16.328Z",
            "ends_at": "2025-12-27T06:22:16.328Z",
            "hall_number": 0,
            "capacity": 35
        }
    )

    assert response_showtime.status_code == 200

    response_delete = client.delete(
        f"/admin/showtime/{showtime_id}",
    )

    assert response_delete.status_code == 200

from urllib.parse import quote


def test_get_activities(client):
    # Arrange (fixture)
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "tester@example.com"
    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    get = client.get("/activities")
    assert email in get.json()[activity]["participants"]


def test_prevent_duplicate_signup(client):
    # Arrange
    activity = "Gym Class"
    email = "dup@example.com"
    # Act
    resp1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    resp2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    # Assert
    assert resp1.status_code == 200
    assert resp2.status_code == 400


def test_unregister_removes_participant(client):
    # Arrange
    activity = "Programming Class"
    email = "remove_me@example.com"
    # Act - signup then delete
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 200
    del_resp = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    # Assert
    assert del_resp.status_code == 200
    get = client.get("/activities")
    assert email not in get.json()[activity]["participants"]

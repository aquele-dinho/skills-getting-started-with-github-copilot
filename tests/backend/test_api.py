from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_the_default_catalog():
    response = client.get("/activities")

    assert response.status_code == 200

    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_adds_a_participant():
    email = "fresh.student@example.com"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_signup_for_activity_allows_the_same_email_in_a_fresh_test():
    email = "fresh.student@example.com"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_signup_for_activity_rejects_duplicate_participants():
    email = "duplicate.student@example.com"

    first_response = client.post(f"/activities/Chess Club/signup?email={email}")
    second_response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_a_student():
    email = "remove.me@example.com"

    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/Chess Club/participants/{email}")
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert email not in activities_response.json()["Chess Club"]["participants"]

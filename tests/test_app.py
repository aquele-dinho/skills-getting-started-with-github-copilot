from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "student@example.com"

    signup_response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{quote(email)}"
    )
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200

    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]

from urllib.parse import quote

import src.app as app_module


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "remove.me@mergington.edu"
    app_module.activities[activity_name]["participants"].append(email)
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    encoded_activity_name = quote(activity_name, safe="")
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_404_for_missing_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    encoded_activity_name = quote(activity_name, safe="")
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_404_when_student_not_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.signed.up@mergington.edu"
    assert email not in app_module.activities[activity_name]["participants"]

    # Act
    encoded_activity_name = quote(activity_name, safe="")
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
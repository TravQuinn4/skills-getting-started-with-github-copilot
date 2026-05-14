def test_get_activities_returns_activity_list(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200

    data = response.json()
    assert expected_activity in data
    assert "description" in data[expected_activity]
    assert "participants" in data[expected_activity]
    assert isinstance(data[expected_activity]["participants"], list)


def test_signup_for_activity_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "teststudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {new_email} for {activity_name}"
    }

    activities = client.get("/activities").json()
    assert new_email in activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={duplicate_email}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_invalid_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    test_email = "teststudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

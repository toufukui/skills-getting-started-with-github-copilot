import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestGetActivities:
    """Test suite for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        # Arrange: No setup needed, activities are pre-loaded
        
        # Act: Send GET request to /activities
        response = client.get("/activities")
        
        # Assert: Verify response and content
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert data["Chess Club"]["max_participants"] == 12
        assert "participants" in data["Chess Club"]


class TestSignupActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_participant_successfully(self, client):
        # Arrange: Prepare a new email that's not registered
        activity_name = "Chess Club"
        new_email = "newstudent123@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])
        
        # Act: Send POST request to signup endpoint
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert: Verify successful signup
        assert response.status_code == 200
        result = response.json()
        assert result["message"] == f"Signed up {new_email} for {activity_name}"
        assert new_email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count + 1
    
    def test_signup_duplicate_email_returns_error(self, client):
        # Arrange: Use an email that's already registered
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"
        
        # Act: Send POST request with existing email
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert: Verify error response for duplicate
        assert response.status_code == 400
        result = response.json()
        assert "already signed up" in result["detail"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange: Use an activity name that doesn't exist
        fake_activity = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act: Send POST request to nonexistent activity
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": email}
        )
        
        # Assert: Verify 404 not found error
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()


class TestUnregisterActivity:
    """Test suite for POST /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_participant_successfully(self, client):
        # Arrange: First signup a participant, then prepare to unregister
        activity_name = "Programming Class"
        temp_email = "tempstudent999@mergington.edu"
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": temp_email}
        )
        assert temp_email in activities[activity_name]["participants"]
        initial_count = len(activities[activity_name]["participants"])
        
        # Act: Send POST request to unregister
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": temp_email}
        )
        
        # Assert: Verify successful unregistration
        assert response.status_code == 200
        result = response.json()
        assert result["message"] == f"Removed {temp_email} from {activity_name}"
        assert temp_email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1
    
    def test_unregister_nonexistent_participant_returns_404(self, client):
        # Arrange: Use email that's not registered for this activity
        activity_name = "Chess Club"
        unregistered_email = "notregistered@mergington.edu"
        
        # Act: Send POST request to unregister non-participant
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": unregistered_email}
        )
        
        # Assert: Verify 404 error
        assert response.status_code == 404
        result = response.json()
        assert "not registered" in result["detail"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        # Arrange: Use activity that doesn't exist
        fake_activity = "Fake Activity"
        email = "test@mergington.edu"
        
        # Act: Send POST request to unregister from nonexistent activity
        response = client.post(
            f"/activities/{fake_activity}/unregister",
            params={"email": email}
        )
        
        # Assert: Verify 404 not found error
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()

"""Test suite for GET /activities endpoint"""
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for retrieving all activities"""

    def test_get_all_activities(self, client):
        """
        Test that GET /activities returns all 9 activities
        
        ARRANGE: Use client fixture
        ACT: Send GET request to /activities
        ASSERT: Verify response status and activity count
        """
        # ACT
        response = client.get("/activities")
        
        # ASSERT
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9

    def test_activities_have_correct_structure(self, client):
        """
        Test that each activity has required fields
        
        ARRANGE: Use client fixture
        ACT: Send GET request to /activities
        ASSERT: Verify each activity has expected structure
        """
        # ACT
        response = client.get("/activities")
        activities = response.json()
        
        # ASSERT
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)

    def test_activities_with_existing_participants(self, client):
        """
        Test that activities with existing participants display correctly
        
        ARRANGE: Use client fixture
        ACT: Send GET request to /activities
        ASSERT: Verify activities with participants show email list
        """
        # ACT
        response = client.get("/activities")
        activities = response.json()
        
        # ASSERT
        # Chess Club, Programming Class, and Gym Class have pre-populated participants
        assert len(activities["Chess Club"]["participants"]) == 2
        assert len(activities["Programming Class"]["participants"]) == 2
        assert len(activities["Gym Class"]["participants"]) == 2
        
        # Verify participants are email addresses
        for email in activities["Chess Club"]["participants"]:
            assert "@" in email

    def test_activities_with_no_participants(self, client):
        """
        Test that activities with no participants show empty list
        
        ARRANGE: Use client fixture
        ACT: Send GET request to /activities
        ASSERT: Verify empty participant lists
        """
        # ACT
        response = client.get("/activities")
        activities = response.json()
        
        # ASSERT
        # Basketball, Tennis, Drama, Art, Debate, Science clubs should be empty
        empty_activities = ["Basketball Club", "Tennis Club", "Drama Club", "Art Club", "Debate Club", "Science Club"]
        for activity_name in empty_activities:
            assert len(activities[activity_name]["participants"]) == 0

"""Test suite for POST /activities/{activity_name}/signup endpoint"""
import pytest


class TestSignup:
    """Tests for signing up students for activities"""

    def test_successful_signup(self, client):
        """
        Test that a student can successfully sign up for an activity
        
        ARRANGE: Prepare activity name and email
        ACT: Send POST request to signup endpoint
        ASSERT: Verify response and participant added
        """
        # ARRANGE
        activity_name = "Basketball Club"
        email = "new.student@mergington.edu"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # ASSERT: Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

    def test_duplicate_signup_returns_400(self, client):
        """
        Test that signing up twice for the same activity returns 400 error
        
        ARRANGE: Sign up a student first time, then attempt duplicate signup
        ACT: Send POST request for duplicate signup
        ASSERT: Verify 400 error with appropriate message
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 400
        assert "Already signed up" in response.json()["detail"]

    def test_activity_not_found_returns_404(self, client):
        """
        Test that signing up for non-existent activity returns 404 error
        
        ARRANGE: Prepare invalid activity name
        ACT: Send POST request to non-existent activity
        ASSERT: Verify 404 error with appropriate message
        """
        # ARRANGE
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_with_special_characters_in_email(self, client):
        """
        Test that email addresses with special characters are handled correctly
        
        ARRANGE: Prepare email with special characters
        ACT: Send POST request with special character email
        ASSERT: Verify successful signup
        """
        # ARRANGE
        activity_name = "Art Club"
        email = "student+tag@mergington.edu"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200
        
        # ASSERT: Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

    def test_signup_for_activity_at_capacity(self, client):
        """
        Test that a student can still sign up even if activity is at capacity
        (current implementation allows this)
        
        ARRANGE: Get an activity and sign up to its max capacity
        ACT: Continue signing up beyond capacity
        ASSERT: Verify signup is allowed (no capacity check in current implementation)
        """
        # ARRANGE
        activity_name = "Tennis Club"
        max_capacity = 12  # As defined in app.py
        
        # Sign up enough students to reach capacity
        for i in range(max_capacity + 1):
            email = f"student{i}@mergington.edu"
            
            # ACT
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            
            # ASSERT - current implementation allows signup beyond capacity
            assert response.status_code == 200
        
        # Verify all signed up
        activities = client.get("/activities").json()
        assert len(activities[activity_name]["participants"]) == max_capacity + 1

    def test_signup_case_sensitive_activity_name(self, client):
        """
        Test that activity names are case-sensitive
        
        ARRANGE: Prepare lowercase activity name (invalid)
        ACT: Send POST request with incorrect case
        ASSERT: Verify 404 error
        """
        # ARRANGE
        activity_name = "basketball club"  # Lowercase - incorrect
        email = "student@mergington.edu"
        
        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 404

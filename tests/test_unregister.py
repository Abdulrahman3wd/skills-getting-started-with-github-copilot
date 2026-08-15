"""Test suite for DELETE /activities/{activity_name}/unregister endpoint"""
import pytest


class TestUnregister:
    """Tests for unregistering students from activities"""

    def test_successful_unregister(self, client):
        """
        Test that a student can successfully unregister from an activity
        
        ARRANGE: Prepare activity and participant
        ACT: Send DELETE request to unregister endpoint
        ASSERT: Verify response and participant removed
        """
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        
        # ASSERT: Verify participant was removed
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]

    def test_not_registered_returns_400(self, client):
        """
        Test that unregistering a non-participant returns 400 error
        
        ARRANGE: Prepare activity and email not signed up
        ACT: Send DELETE request for non-participant
        ASSERT: Verify 400 error with appropriate message
        """
        # ARRANGE
        activity_name = "Basketball Club"
        email = "not.signed.up@mergington.edu"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 400
        assert "Not registered" in response.json()["detail"]

    def test_unregister_activity_not_found_returns_404(self, client):
        """
        Test that unregistering from non-existent activity returns 404 error
        
        ARRANGE: Prepare invalid activity name
        ACT: Send DELETE request to non-existent activity
        ASSERT: Verify 404 error with appropriate message
        """
        # ARRANGE
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # ACT
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_can_resignup_after_unregister(self, client):
        """
        Test that a student can re-sign up after unregistering
        
        ARRANGE: Sign up, unregister, then sign up again
        ACT: Execute signup -> unregister -> signup sequence
        ASSERT: Verify participant appears in final signup
        """
        # ARRANGE
        activity_name = "Drama Club"
        email = "actor@mergington.edu"
        
        # ACT: First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # ACT: Unregister
        response2 = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # ACT: Re-signup
        response3 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # ASSERT
        assert response3.status_code == 200
        
        # ASSERT: Verify participant appears in activity
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

    def test_unregister_multiple_participants(self, client):
        """
        Test that unregistering one participant doesn't affect others
        
        ARRANGE: Sign up multiple students, then unregister one
        ACT: Remove one student
        ASSERT: Verify other participants remain
        """
        # ARRANGE
        activity_name = "Science Club"
        email1 = "scientist1@mergington.edu"
        email2 = "scientist2@mergington.edu"
        
        # Sign up both students
        client.post(f"/activities/{activity_name}/signup", params={"email": email1})
        client.post(f"/activities/{activity_name}/signup", params={"email": email2})
        
        # ACT: Unregister first student
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email1}
        )
        
        # ASSERT
        assert response.status_code == 200
        
        # ASSERT: First student removed, second remains
        activities = client.get("/activities").json()
        assert email1 not in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]

    def test_unregister_with_url_encoding(self, client):
        """
        Test that email addresses with special characters are URL-encoded correctly
        
        ARRANGE: Sign up with special character email, then unregister
        ACT: Send DELETE with special character email
        ASSERT: Verify successful unregister
        """
        # ARRANGE
        activity_name = "Debate Club"
        email = "debater+tag@mergington.edu"
        
        # Sign up first
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        
        # ACT: Unregister with URL encoding
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # ASSERT
        assert response.status_code == 200
        
        # ASSERT: Verify removed
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]

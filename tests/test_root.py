"""Test suite for GET / endpoint"""


class TestRoot:
    """Tests for root endpoint redirect"""

    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html
        
        ARRANGE: Use client fixture
        ACT: Send GET request to root endpoint
        ASSERT: Verify redirect response and location
        """
        # ACT
        response = client.get("/", follow_redirects=False)
        
        # ASSERT
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_with_follow(self, client):
        """
        Test that following the redirect works correctly
        
        ARRANGE: Use client fixture with follow_redirects=True
        ACT: Send GET request to root endpoint
        ASSERT: Verify final response contains HTML content
        """
        # ACT
        response = client.get("/", follow_redirects=True)
        
        # ASSERT
        assert response.status_code == 200
        # Response body should contain HTML content from index.html
        assert "text/html" in response.headers.get("content-type", "")

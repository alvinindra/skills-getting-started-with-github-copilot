from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    # Test successful signup
    response = client.post(
        "/activities/Basketball Team/signup",
        params={"email": "test@example.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up test@example.com for Basketball Team"}

    # Test signup for non-existent activity
    response = client.post(
        "/activities/NonExistent/signup",
        params={"email": "test@example.com"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

    # Test signup for full activity (Chess Club has max 12, but let's use one with smaller max if possible, or just test the logic)
    # Chess Club has 2 participants, max 12.
    # Let's test "Student already signed up"
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}

def test_unregister_from_activity():
    # First sign up
    client.post(
        "/activities/Soccer Club/signup",
        params={"email": "unregister_test@example.com"}
    )
    
    # Then unregister
    response = client.delete(
        "/activities/Soccer Club/unregister",
        params={"email": "unregister_test@example.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered unregister_test@example.com from Soccer Club"}

    # Test unregistering non-existent student
    response = client.delete(
        "/activities/Soccer Club/unregister",
        params={"email": "not_there@example.com"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found in this activity"}

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_email_type():
    response = client.post("/create_email", json={
        "name": "Newsletter",
        "description": "Weekly newsletter"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Newsletter"
    assert response.json()["description"] == "Weekly newsletter"

def test_read_email_type():
    response = client.get("/get_email/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Newsletter"
    assert response.json()["description"] == "Weekly newsletter"

def test_read_email_types():
    response = client.get("/all_emails")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_email_type():
    response = client.put("/update_email/1", json={
        "name": "New Newsletter",
        "description": "Monthly newsletter"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "New Newsletter"
    assert response.json()["description"] == "Monthly newsletter"

def test_delete_email_type():
    response = client.delete("/delete_email/1")
    assert response.status_code == 200
    assert response.json() == {"Email type deleted successfully"}

def test_get_subscriptions_by_email_type():
    response = client.get("/get_email/1/subscriptions")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_run_function():
    response = client.get("/get_email/1/subscriptions")
    assert response.status_code == 200
    assert response.json() == {"Emails sent successfully"}
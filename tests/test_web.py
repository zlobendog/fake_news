from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Tests webserver being up
def test_home():
    response = client.get(
        "/", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Check any news and see if it's fake!" in response.content
    response = client.get("/static/styles.css")
    assert response.status_code == 200

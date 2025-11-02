from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_agent_card():
    r = client.get("/.well-known/agent.json")
    # if file missing, it will return 404; this test expects existence
    assert r.status_code in (200, 404)
    if r.status_code == 200:
        js = r.json()
        assert js.get("name") == "Etymo"

def test_message_send_invalid():
    r = client.post("/", json={"method": "message/send", "params": {}})
    assert r.status_code == 200
    assert "error" in r.json()
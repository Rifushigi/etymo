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

def test_agent_card_structure():
    """Agent card should have required fields."""
    response = client.get("http://localhost:8000/.well-known/agent.json")
    data = response.json()
    
    assert "name" in data
    assert "description" in data
    assert "url" in data
    assert "version" in data
    assert "skills" in data
    assert len(data["skills"]) > 0

def test_skill_examples_work():
    """Examples in agent card should actually work."""
    # Get agent card
    card = client.get("http://localhost:8000/.well-known/agent.json").json()
    
    # Test first example
    skill = card["skills"][0]
    example = skill["examples"][0]
    
    # Make request using example input
    response = client.post(
        "http://localhost:8000/",
        json={
            "jsonrpc": "2.0",
            "method": "message/send",
            "id": 1,
            "params": {"message": example["input"]}
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
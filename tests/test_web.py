from fastapi.testclient import TestClient

from kept.web.app import create_app

client = TestClient(create_app())


def test_healthz() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["ok"] == "true"


def test_pages_render() -> None:
    for path, needle in [
        ("/", "Nothing filed yet"),
        ("/inbox", "One-click confirm"),
        ("/decisions", "on the record"),
        ("/live", "bee stream --json"),
        ("/setup", "Phase 0 checkpoint"),
    ]:
        response = client.get(path)
        assert response.status_code == 200, path
        assert needle in response.text
        assert "Kept" in response.text

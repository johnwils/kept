from fastapi.testclient import TestClient

from kept.web.app import create_app


def test_healthz() -> None:
    client = TestClient(create_app())
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["ok"] == "true"


def test_pages_render() -> None:
    client = TestClient(create_app())
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
    home = client.get("/")
    assert "Phase 0 of 6" in home.text
    assert "Build phases" in home.text
    assert 'href="/setup"' in home.text
    assert "us.anthropic.claude-sonnet-4-6" not in home.text


def test_ship_mode_hides_build_chrome(monkeypatch) -> None:
    monkeypatch.setenv("KEPT_SHIP_MODE", "true")
    client = TestClient(create_app())
    home = client.get("/")
    assert home.status_code == 200
    assert "Phase 0 of 6" not in home.text
    assert "Build phases" not in home.text
    assert 'href="/setup"' not in home.text
    assert "Closed issues with a matching Bee todo." in home.text

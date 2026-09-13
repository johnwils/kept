from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from kept import __version__
from kept.config import load_settings

WEB_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(WEB_DIR / "templates"))

NAV = [
    ("/", "Ledger", "ledger"),
    ("/inbox", "Inbox", "inbox"),
    ("/decisions", "Decisions", "decisions"),
    ("/live", "Live", "live"),
    ("/setup", "Setup", "setup"),
]

PHASES = [
    {"id": 0, "name": "Scaffold", "status": "current"},
    {"id": 1, "name": "Daemon", "status": "next"},
    {"id": 2, "name": "Agent", "status": "queued"},
    {"id": 3, "name": "Write-back", "status": "queued"},
    {"id": 4, "name": "AgentCore", "status": "queued"},
    {"id": 5, "name": "Reminders", "status": "queued"},
    {"id": 6, "name": "Ship", "status": "queued"},
]


def create_app() -> FastAPI:
    app = FastAPI(title="Kept", version=__version__)
    app.mount("/static", StaticFiles(directory=str(WEB_DIR / "static")), name="static")

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"ok": "true", "version": __version__}

    @app.get("/", response_class=HTMLResponse)
    def ledger(request: Request) -> HTMLResponse:
        return _page(request, "ledger.html", "ledger", "Ledger")

    @app.get("/inbox", response_class=HTMLResponse)
    def inbox(request: Request) -> HTMLResponse:
        return _page(request, "inbox.html", "inbox", "Inbox")

    @app.get("/decisions", response_class=HTMLResponse)
    def decisions(request: Request) -> HTMLResponse:
        return _page(request, "decisions.html", "decisions", "Decisions")

    @app.get("/live", response_class=HTMLResponse)
    def live(request: Request) -> HTMLResponse:
        return _page(request, "live.html", "live", "Live")

    @app.get("/setup", response_class=HTMLResponse)
    def setup(request: Request) -> HTMLResponse:
        return _page(request, "setup.html", "setup", "Setup")

    return app


def _page(request: Request, template: str, active: str, title: str) -> HTMLResponse:
    settings = load_settings()
    nav = NAV if not settings.kept_ship_mode else [item for item in NAV if item[2] != "setup"]
    return templates.TemplateResponse(
        request=request,
        name=template,
        context={
            "title": title,
            "active": active,
            "nav": nav,
            "phases": PHASES,
            "version": __version__,
            "mode": settings.kept_mode,
            "ship_mode": settings.kept_ship_mode,
        },
    )


def run(host: str = "0.0.0.0", port: int = 8080) -> None:
    import uvicorn

    uvicorn.run(
        "kept.web.app:create_app",
        factory=True,
        host=host,
        port=port,
        log_level="info",
    )


app = create_app()

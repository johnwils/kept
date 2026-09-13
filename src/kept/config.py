from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

Mode = Literal["fixture", "live", "local-agent"]
ConsentDefault = Literal["self", "flagged", "allowlist"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    kept_mode: Mode = "fixture"
    kept_fixtures_dir: Path = Path("fixtures/sample")
    kept_web_host: str = "0.0.0.0"
    kept_web_port: int = 8080
    kept_db_path: Path = Path("data/kept.db")
    kept_ship_mode: bool = False

    bee_bin: str = "bee"
    bee_mcp_http_port: int = 8790
    bee_mcp_http_token: str = ""

    kept_me_identifiers: str = ""
    kept_redact: str = ""
    kept_consent_default: ConsentDefault = "self"
    kept_consent_allowlist: str = ""

    kept_auto_create_min: float = 0.75
    kept_inbox_min: float = 0.5

    aws_region: str = "us-west-2"
    aws_profile: str = ""
    bedrock_model_id: str = ""
    kept_agent_url: str = "http://127.0.0.1:8081"

    github_token: str = ""
    github_repo: str = ""
    github_adr_path: str = "docs/adr"

    def model_post_init(self, __context: object) -> None:
        if not 0.0 <= self.kept_auto_create_min <= 1.0:
            raise ValueError("KEPT_AUTO_CREATE_MIN must be between 0 and 1")
        if not 0.0 <= self.kept_inbox_min <= 1.0:
            raise ValueError("KEPT_INBOX_MIN must be between 0 and 1")

    @property
    def me_identifiers(self) -> list[str]:
        return _csv(self.kept_me_identifiers)

    @property
    def redact_terms(self) -> list[str]:
        return _csv(self.kept_redact)

    @property
    def consent_allowlist(self) -> list[str]:
        return _csv(self.kept_consent_allowlist)


def _csv(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def load_settings() -> Settings:
    return Settings()

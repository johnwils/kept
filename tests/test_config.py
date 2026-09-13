from kept import __version__
from kept.config import Settings


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_csv_identifiers() -> None:
    settings = Settings(kept_me_identifiers="me, John, speaker_1")
    assert settings.me_identifiers == ["me", "John", "speaker_1"]


def test_defaults_are_fixture_mode() -> None:
    settings = Settings()
    assert settings.kept_mode == "fixture"
    assert settings.aws_region == "us-west-2"
    assert settings.kept_auto_create_min == 0.75
    assert settings.kept_ship_mode is False
    assert settings.kept_consent_default == "self"
    assert settings.bedrock_model_id == ""


def test_consent_allowlist() -> None:
    settings = Settings(
        kept_consent_default="allowlist",
        kept_consent_allowlist="Jordan, Alex",
    )
    assert settings.consent_allowlist == ["Jordan", "Alex"]

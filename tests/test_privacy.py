from kept.privacy import redact


def test_redacts_case_insensitively() -> None:
    text = "Jordan asked me, and JORDAN followed up."
    assert redact(text, ["Jordan"]) == "[REDACTED] asked me, and [REDACTED] followed up."


def test_longer_terms_first() -> None:
    text = "Talked to Jordan Lee about billing."
    assert redact(text, ["Jordan", "Jordan Lee"]) == "Talked to [REDACTED] about billing."


def test_empty_terms_noop() -> None:
    assert redact("hello", []) == "hello"

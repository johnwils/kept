from __future__ import annotations

import json
from pathlib import Path

import pytest

from kept.models.events import classify_event, parse_stream_line


def test_classify_documented_payloads() -> None:
    assert (
        classify_event(
            {
                "utterance": {"text": "Hello there", "speaker": "speaker_1"},
                "conversation_uuid": "u",
            }
        )
        == "new-utterance"
    )
    assert (
        classify_event(
            {
                "conversation": {
                    "id": 123,
                    "uuid": "uuid-string",
                    "state": "processing",
                    "title": "Standup",
                }
            }
        )
        == "new-conversation"
    )
    assert (
        classify_event(
            {
                "conversation": {
                    "id": 123,
                    "state": "processed",
                    "title": "Standup",
                    "short_summary": "Auth bug by Thursday",
                }
            }
        )
        == "update-conversation"
    )
    assert (
        classify_event({"conversation_id": 123, "short_summary": "Summary text"})
        == "update-conversation-summary"
    )
    assert classify_event({"conversation": {"id": 123, "title": "Standup"}}) == (
        "delete-conversation"
    )
    assert (
        classify_event({"todo": {"id": 10, "text": "Call dentist", "completed": False}})
        == "todo-created"
    )
    assert classify_event({"todo": {"id": 10, "text": "Call dentist"}}) == "todo-deleted"


def test_parse_sample_stream(sample_dir: Path) -> None:
    lines = (sample_dir / "stream.jsonl").read_text().splitlines()
    events = [parse_stream_line(line) for line in lines]
    types = [e.type for e in events if e is not None]
    assert "new-utterance" in types
    assert "update-conversation" in types
    processed = next(e for e in events if e and e.type == "update-conversation")
    assert processed.conversation_id == 101
    assert processed.raw["conversation"]["state"] == "processed"


def test_blank_line_is_none() -> None:
    assert parse_stream_line("  \n") is None


def test_rejects_non_object() -> None:
    with pytest.raises(ValueError, match="not a JSON object"):
        parse_stream_line(json.dumps(["not", "an", "object"]))

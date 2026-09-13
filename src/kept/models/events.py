"""Bee `stream --json` payloads have no top-level `event` field.

Classify each line by structural keys, per
https://docs.bee.computer/docs/realtime (verified 2026-09-13).
"""

from __future__ import annotations

import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

EventType = Literal[
    "new-utterance",
    "new-conversation",
    "update-conversation",
    "update-conversation-summary",
    "delete-conversation",
    "update-location",
    "todo-created",
    "todo-updated",
    "todo-deleted",
    "journal-created",
    "journal-updated",
    "journal-deleted",
    "journal-text",
    "unknown",
]


class StreamEvent(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: EventType
    raw: dict[str, Any]
    conversation_id: int | None = None
    conversation_uuid: str | None = None


def classify_event(payload: dict[str, Any]) -> EventType:
    """Distinguish Bee stream events by structural keys.

    There is no `.event` field in `--json` output. Do not filter with
    `jq 'select(.event == "...")'` — that matches nothing.
    """
    if "utterance" in payload:
        return "new-utterance"

    if "todo" in payload:
        todo = payload["todo"] if isinstance(payload["todo"], dict) else {}
        if "completed" not in todo and "alarmAt" not in todo:
            return "todo-deleted"
        # created vs updated cannot be separated from the payload alone;
        # the daemon treats both as upserts. Honour a stamped event name.
        return "todo-updated" if _looks_like_update(payload) else "todo-created"

    if "journal" in payload:
        return "journal-updated" if _looks_like_update(payload) else "journal-created"

    if "journalId" in payload and "text" in payload:
        return "journal-text"
    if "journalId" in payload:
        return "journal-deleted"

    if "location" in payload and "conversation_id" in payload:
        return "update-location"

    if "conversation" in payload and isinstance(payload["conversation"], dict):
        conv = payload["conversation"]
        if conv.get("state") is None and conv.get("uuid") is None:
            return "delete-conversation"
        if conv.get("uuid") and conv.get("state") in {None, "processing", "preparing"}:
            return "new-conversation"
        if conv.get("state") == "processed" or conv.get("short_summary"):
            return "update-conversation"
        if conv.get("uuid"):
            return "new-conversation"
        return "update-conversation"

    if "short_summary" in payload and "conversation_id" in payload:
        return "update-conversation-summary"

    return "unknown"


def parse_stream_line(line: str) -> StreamEvent | None:
    text = line.strip()
    if not text:
        return None
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("stream line is not a JSON object")
    event_type = classify_event(payload)
    conversation_id, conversation_uuid = _conversation_ids(payload)
    return StreamEvent(
        type=event_type,
        raw=payload,
        conversation_id=conversation_id,
        conversation_uuid=conversation_uuid,
    )


def _conversation_ids(payload: dict[str, Any]) -> tuple[int | None, str | None]:
    conv = payload.get("conversation")
    if isinstance(conv, dict):
        cid = conv.get("id")
        uuid = conv.get("uuid")
        return (cid if isinstance(cid, int) else None, uuid if isinstance(uuid, str) else None)
    cid = payload.get("conversation_id")
    uuid = payload.get("conversation_uuid")
    return (
        cid if isinstance(cid, int) else None,
        uuid if isinstance(uuid, str) else None,
    )


def _looks_like_update(payload: dict[str, Any]) -> bool:
    # Webhook templates include {{event}}; the JSON stream does not. If a
    # producer (or our fixture recorder) stamped an event name, honour it.
    name = payload.get("event") or payload.get("_event")
    return isinstance(name, str) and name.endswith("-updated")

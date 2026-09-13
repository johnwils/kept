from __future__ import annotations

import re


def redact(text: str, terms: list[str]) -> str:
    """Scrub configured names/terms before any cloud call.

    Matching is case-insensitive. Longer terms are applied first so a full
    name is not partially overwritten by a first name.
    """
    if not text or not terms:
        return text
    redacted = text
    for term in sorted(terms, key=len, reverse=True):
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted

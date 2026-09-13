"""Strict extraction schema. The agent (Phase 2) must emit this JSON.

Confidence:
  ≥ 0.75  auto-create GitHub issue / ADR / Bee todo
  0.50–0.75  dashboard inbox, one-click confirm
  < 0.50  drop
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Commitment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(description="Normalized commitment in the owner's voice")
    quote: str = Field(description="Verbatim sentence from the transcript")
    made_to: str | None = Field(default=None, description="Person the promise was made to")
    due_date: date | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    conversation_id: int
    utterance_index: int | None = None


class Decision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    context: str
    decision: str
    consequences: str
    quote: str
    confidence: float = Field(ge=0.0, le=1.0)
    conversation_id: int


class AskOfMe(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    text: str
    asked_by: str = Field(alias="from", description="Who asked")
    quote: str
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator("asked_by")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("from must not be empty")
        return value


class ExtractionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    commitments: list[Commitment] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    asks_of_me: list[AskOfMe] = Field(default_factory=list)

    def actionable(self, auto_min: float = 0.75, inbox_min: float = 0.5) -> dict[str, list]:
        """Split items by confidence threshold. Never auto-create below auto_min."""

        def bucket(items: list) -> tuple[list, list]:
            auto, inbox = [], []
            for item in items:
                if item.confidence >= auto_min:
                    auto.append(item)
                elif item.confidence >= inbox_min:
                    inbox.append(item)
            return auto, inbox

        c_auto, c_inbox = bucket(self.commitments)
        d_auto, d_inbox = bucket(self.decisions)
        a_auto, a_inbox = bucket(self.asks_of_me)
        return {
            "auto": {"commitments": c_auto, "decisions": d_auto, "asks_of_me": a_auto},
            "inbox": {"commitments": c_inbox, "decisions": d_inbox, "asks_of_me": a_inbox},
        }

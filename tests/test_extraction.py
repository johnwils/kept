from datetime import date

from kept.models.extraction import AskOfMe, Commitment, Decision, ExtractionResult


def test_thresholds_split_auto_and_inbox() -> None:
    result = ExtractionResult(
        commitments=[
            Commitment(
                text="Fix auth",
                quote="I'll fix the auth bug by Thursday",
                made_to="Jordan",
                due_date=date(2026, 9, 17),
                confidence=0.91,
                conversation_id=101,
                utterance_index=4,
            ),
            Commitment(
                text="Look at logs",
                quote="I can look at the logs later",
                confidence=0.62,
                conversation_id=101,
            ),
            Commitment(
                text="Maybe rewrite",
                quote="we could rewrite the whole thing",
                confidence=0.31,
                conversation_id=101,
            ),
        ]
    )
    buckets = result.actionable()
    assert len(buckets["auto"]["commitments"]) == 1
    assert buckets["auto"]["commitments"][0].text == "Fix auth"
    assert len(buckets["inbox"]["commitments"]) == 1
    assert buckets["inbox"]["commitments"][0].confidence == 0.62


def test_from_alias() -> None:
    ask = AskOfMe.model_validate(
        {
            "text": "Can you take the on-call?",
            "from": "Priya",
            "quote": "Can you take the on-call this weekend?",
            "confidence": 0.8,
        }
    )
    assert ask.asked_by == "Priya"
    dumped = ask.model_dump(by_alias=True)
    assert dumped["from"] == "Priya"


def test_decision_roundtrip() -> None:
    decision = Decision(
        title="Postgres over Dynamo",
        context="Billing needs joins",
        decision="Use Postgres",
        consequences="Ops owns backups",
        quote="we're going with Postgres over Dynamo",
        confidence=0.88,
        conversation_id=101,
    )
    parsed = ExtractionResult.model_validate({"decisions": [decision.model_dump()]})
    assert parsed.decisions[0].title == "Postgres over Dynamo"

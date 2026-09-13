# Capturing Bee fixtures

Kept cannot be developed against live meetings every hour. We replay JSON
captured from the Bee CLI. **Real transcripts never go in git.**

Destination: `fixtures/real/` (gitignored). Synthetic stand-ins live in
`fixtures/sample/` and are the Phase 0 test corpus.

## Prerequisites

1. Bee iOS app, Developer Mode unlocked (tap **Version** five times).
2. `npm install -g @beeai/cli`
3. `bee login` then `bee status` / `bee ping`

## One-shot

```bash
chmod +x scripts/capture-fixtures.sh
./scripts/capture-fixtures.sh
```

## Manual (what the script runs)

```bash
mkdir -p fixtures/real
bee version
bee status
bee ping
bee me --json > fixtures/real/me.json
bee now --json > fixtures/real/now.json
bee conversations list --json --limit 50 > fixtures/real/conversations.json
bee todos list --json > fixtures/real/todos.json
bee facts list --json > fixtures/real/facts.json
bee sync --output fixtures/real/sync --recent-days 14
```

Sample the live stream for ~45 seconds (macOS has no `timeout(1)` by default):

```bash
bee stream --json --types new-conversation,update-conversation,update-conversation-summary,new-utterance,todo-created,todo-updated \
  > fixtures/real/stream.jsonl &
STREAM_PID=$!
sleep 45
kill $STREAM_PID
wait $STREAM_PID 2>/dev/null
wc -l fixtures/real/stream.jsonl
```

Then pick two conversation ids that look like engineering talk:

```bash
bee conversations transcript <id> --json > fixtures/real/transcript-<id>.json
bee conversations get <id> --json > fixtures/real/conversation-<id>.json
bee conversations related <id> --json > fixtures/real/related-<id>.json
```

## What to paste back into the Phase 0 checkpoint

- Output of `bee status` and `bee version`
- `bee me --json` (redact email if you want)
- Line count of `stream.jsonl` and whether `conversations.json` is a list or an object
- One transcript, names redacted, so we can lock the utterance schema

## Stream contract (verified 2026-09-13)

`bee stream --json` prints **one raw payload per line**. There is **no**
top-level `event` field. Classify by keys:

| Key present | Event |
| --- | --- |
| `.utterance` | `new-utterance` |
| `.conversation` with `.uuid` / `state=processing` | `new-conversation` |
| `.conversation` with `state=processed` | `update-conversation` |
| `.conversation_id` + `.short_summary` | `update-conversation-summary` |
| `.todo` | todo created/updated/deleted |
| `.conversation.id` | **number**, not a string |

Act on `update-conversation` when `conversation.state == "processed"`, then:

```bash
bee conversations transcript <id> --json
```

Delivery is at-most-once. No replay. `bee sync` is the reconciliation path.

Webhook mode *does* expose `{{event}}`. We stay on the JSON subprocess for the
daemon (simpler, local) and stamp `_event` onto fixture lines if needed.

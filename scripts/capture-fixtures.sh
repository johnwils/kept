#!/usr/bin/env bash
# Capture Bee fixtures for Kept. Run on the Mac that is logged into Bee.
# Real transcripts stay in fixtures/real/ (gitignored).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/fixtures/real"
mkdir -p "$OUT/sync"

need_bee() {
  if ! command -v bee >/dev/null 2>&1; then
    echo "bee not on PATH. Install with: npm install -g @beeai/cli" >&2
    exit 1
  fi
}

need_bee
echo "== bee version =="
bee version
echo
echo "== bee status =="
bee status
echo
echo "== bee ping =="
bee ping
echo
echo "== bee mcp --help =="
bee mcp --help
echo
echo "== bee sync --help =="
bee sync --help
echo
echo "== bee conversations --help =="
bee conversations --help || bee conversations list --help
echo

echo "== writing JSON snapshots =="
bee me --json > "$OUT/me.json"
bee now --json > "$OUT/now.json"
bee conversations list --json --limit 50 > "$OUT/conversations.json"
bee todos list --json > "$OUT/todos.json"
bee facts list --json > "$OUT/facts.json"

echo "== bee sync (14 days) =="
bee sync --output "$OUT/sync" --recent-days 14

echo
echo "== sampling bee stream for 45s =="
echo "(talk, or let a meeting run — empty files are still useful)"
bee stream --json --types new-conversation,update-conversation,update-conversation-summary,new-utterance,todo-created,todo-updated \
  > "$OUT/stream.jsonl" &
STREAM_PID=$!
sleep 45
kill "$STREAM_PID" 2>/dev/null || true
wait "$STREAM_PID" 2>/dev/null || true

echo
echo "Wrote:"
wc -l "$OUT"/*.json "$OUT/stream.jsonl" 2>/dev/null || true
echo
echo "Next: pick two conversation ids from fixtures/real/conversations.json and run:"
echo "  bee conversations transcript <id> --json > fixtures/real/transcript-<id>.json"
echo "  bee conversations get <id> --json > fixtures/real/conversation-<id>.json"
echo "  bee conversations related <id> --json > fixtures/real/related-<id>.json"
echo
echo "Paste bee status, bee me --json, line counts, and one redacted transcript back into the Kept thread."

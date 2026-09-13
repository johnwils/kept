# Friction log

Every real snag with Bee CLI, MCP, AgentCore, Strands, or Bedrock. Format is
fixed: task, steps, expected vs actual, severity, workaround, suggestion.

**Rule: no entry without a terminal transcript.** Desk-research notes belong
in PRODUCT_FEEDBACK.md or FEATURE_REQUESTS.md. From Phase 1 on, paste the
command run and the actual output or error.

Bonus: submissions with a friction log can earn up to 10% extra.

---

## 2026-09-13 — Stream JSON has no event name

- **Task attempted:** Confirm how `bee stream --json` identifies event types
  so the daemon can switch on them.
- **Steps taken:** Read [Realtime Sync](https://docs.bee.computer/docs/realtime)
  and the bee-computer/bee-cli README.
- **Expected:** a top-level `"event": "update-conversation"` field, matching
  SSE `event:` lines and webhook `{{event}}`.
- **Actual:** `--json` prints the raw payload only. Docs explicitly warn not
  to `jq 'select(.event == "...")'`. `new-utterance` vs `update-conversation`
  is distinguished by `.utterance` vs `.conversation`. Todo created vs updated
  share the same shape.
- **Severity:** medium
- **Workaround:** `kept.models.events.classify_event` uses structural keys.
  Webhook mode is available but we stay on the subprocess for locality. Fixture
  recorder may stamp `_event` if we later run with `--webhook-body`.
- **Actionable suggestion:** Add `"event"` to the JSON payload (keep it
  optional for back-compat) so clients do not reverse-engineer types. At
  minimum, document a recommended discriminator for todo created vs updated.

## 2026-09-13 — Conversation transcript schema is underspecified

- **Task attempted:** Write a Pydantic model for `bee conversations transcript <id> --json`.
- **Steps taken:** CLI README lists the command and `--since` / `--json`.
  Realtime docs show utterance `{text, speaker}` on the stream, not the
  transcript command.
- **Expected:** an example JSON document for the transcript command.
- **Actual:** no example. Stream utterances do not include an index; we still
  need `utterance_index` on commitments. Conversation has both numeric `id`
  and `uuid`.
- **Severity:** medium
- **Workaround:** synthetic `fixtures/sample/transcript.json` for tests.
  Phase 0 checkpoint captures two real transcripts and we lock the model
  to that shape.
- **Actionable suggestion:** Publish one redacted `transcript --json` example
  (utterance fields, id vs uuid, summary location) on the conversations page.

## 2026-09-13 — AgentCore CLI vs legacy starter toolkit

- **Task attempted:** Choose the deploy tool for Phase 4.
- **Steps taken:** AWS docs (updated 2026-09-04) and the starter-toolkit site,
  which now banners “use `@aws/agentcore`”.
- **Expected:** a single `agentcore` entry point.
- **Actual:** npm `@aws/agentcore` is current. The older Python
  `bedrock-agentcore-starter-toolkit` still ships an `agentcore` that can
  shadow the npm binary.
- **Severity:** medium (will bite on the Mac if the toolkit was ever installed)
- **Workaround:** `npm i -g @aws/agentcore` then `agentcore --version`. If it
  errors, `pip uninstall bedrock-agentcore-starter-toolkit`. Logged in
  `AWS_INTEGRATION.md`.
- **Actionable suggestion:** npm CLI should detect a shadowed binary and print
  the uninstall line. Docs already mention it — keep that warning at the top.

## 2026-09-13 — AgentCore cannot reach Bee MCP on localhost

- **Task attempted:** Decide how the extraction agent calls Bee MCP tools
  (related conversations, facts about people).
- **Steps taken:** MCP HTTP binds `127.0.0.1` only and rejects non-local
  Host/Origin. AgentCore Runtime is in AWS.
- **Expected:** a supported tunnel or Gateway path in the getting-started.
- **Actual:** none that we will take in Phase 2. A tunnel is extra moving
  parts for a hackathon demo.
- **Severity:** low (design choice, not a blocker)
- **Workaround:** daemon pre-fetches `conversations related`, `facts search`,
  and `bee me` and sends them in the extraction request. Agent stays a
  structured-output call. Revisit AgentCore Gateway in Phase 4 if it is free.
- **Actionable suggestion:** A first-class “MCP to AgentCore Gateway” recipe
  for CLIs that are localhost-only (Bee, native OS tools).

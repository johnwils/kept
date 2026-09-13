# Feature requests

Importance: `critical` / `important` / `nice-to-have`.

## Bee

| Request | Importance | Why |
| --- | --- | --- |
| Top-level `event` field on `bee stream --json` | important | Discriminating todo created vs updated, and delete vs update, is guesswork. Webhooks already have `{{event}}`. |
| Stream replay / durable cursor | critical | At-most-once + no replay means a daemon restart drops commitments. We paper over with `bee sync` every 15 minutes; a cursor would make Kept correct, not just eventually consistent. |
| Consent flag on the conversation object | important | Judges (and anyone recorded) will care. We store this ourselves; Bee is the source of the recording. |
| Documented transcript JSON | important | Extraction quality depends on speaker + index. Sample payload belongs in the docs. |
| `bee todos create` idempotency key | nice-to-have | Reconciliation can double-create wrist todos. |

## AgentCore / Strands / Bedrock

| Request | Importance | Why |
| --- | --- | --- |
| Localhost MCP → Gateway recipe | important | Bee MCP is 127.0.0.1 only; Runtime is in AWS. |
| `agentcore --version` warns on PATH shadow | nice-to-have | Legacy Python toolkit binary collides. |
| Structured-output examples with Bedrock inference profiles (`us.*`) | nice-to-have | Default model IDs in samples still show older Claude strings. |

## GitHub

| Request | Importance | Why |
| --- | --- | --- |
| None yet | — | Phase 3. |

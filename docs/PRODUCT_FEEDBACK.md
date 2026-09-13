# Product feedback

Required for the hackathon: what we used each tool for, what worked, what
needs work, onboarding, and whether we would build with it again. Updated
as we actually touch each surface.

## Bee CLI (`@beeai/cli`)

- **Used for:** ingestion contract (`stream`, `conversations`, `todos`, `sync`,
  `facts`). Phase 0 verified docs at docs.bee.computer (dated 2026-06-07)
  against the bee-computer/bee-cli README.
- **Worked:** stream payload shapes are documented with structural keys;
  `conversation.id` is a number; MCP HTTP is documented (`bee mcp serve-http`,
  token ≥32 chars, bind to 127.0.0.1).
- **Needs work:** JSON stream has no top-level `event` field, so created vs
  updated todos are ambiguous. Transcript JSON schema is not fully documented
  — we will lock it from captured fixtures.
- **Onboarding:** `npm i -g @beeai/cli` + Developer Mode (tap Version 5×) is
  clear. Prerequisite (physical Bee + iOS) is the right kind of friction for
  this track.
- **Build with it again:** yes, if the stream stays real-time. A REST-only
  export would kill the demo.

## Bee MCP

- **Used for (planned):** context enrichment (related conversations, facts
  about people). Phase 2 will pre-fetch via CLI rather than call MCP from
  AgentCore. Revisit if AgentCore Gateway makes localhost MCP trivial.
- **Build with it again:** TBD after Phase 2.

## Strands Agents SDK

- **Used for (planned):** extraction agent, `structured_output` into the
  Pydantic schema in `src/kept/models/extraction.py`.
- **Onboarding:** docs at strandsagents.com are current as of 2026-08;
  `BedrockModel` + `structured_output` match the plan.
- **Build with it again:** TBD after Phase 2.

## Amazon Bedrock AgentCore CLI (`@aws/agentcore`)

- **Used for (planned):** Phase 4 deploy of kept-agent. Confirmed 2026-09-04
  that this npm CLI replaced `bedrock-agentcore-starter-toolkit`.
- **Onboarding risk:** a leftover Python `agentcore` on PATH shadows the npm
  binary. We will document the uninstall.
- **Build with it again:** TBD after Phase 4.

## Amazon Bedrock (Claude Sonnet 4.6)

- **Used for (planned):** extraction. Recommended inference profile:
  `us.anthropic.claude-sonnet-4-6` in us-west-2.
- **Build with it again:** TBD after precision review on 10 real transcripts.

## FastAPI + HTMX + Tailwind-via-tokens

- **Used for:** dashboard (Ledger, Inbox, Decisions, Live, Setup). No JS build
  step. Custom CSS tokens rather than a CDN Tailwind compile, so the design
  system is one file.
- **Worked:** Phase 0 pages render without a bundler.
- **Build with it again:** yes for this shape of product.

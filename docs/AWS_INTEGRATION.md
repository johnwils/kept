# AWS integration

Kept uses Amazon Bedrock for extraction, and (from Phase 4) Amazon Bedrock
AgentCore for runtime, memory, and traces. Nothing is deployed yet — this
document is the plan the code will match. Update it the moment a service is
actually called.

Region: **us-west-2**.

## Services

| Service | When | What Kept uses it for |
| --- | --- | --- |
| Amazon Bedrock (model inference) | Phase 2 | Extraction agent via Strands `BedrockModel`. Model ID from `BEDROCK_MODEL_ID`. |
| Amazon Bedrock AgentCore Runtime | Phase 4 | Host the Strands agent. CLI: `npm i -g @aws/agentcore` (not the legacy `bedrock-agentcore-starter-toolkit`). |
| AgentCore Memory | Phase 4 | Remember people across conversations ("Jordan = PM on billing"). |
| AgentCore Observability | Phase 4 | Traces of extraction runs. Ships with `agentcore deploy` (CloudWatch). |
| IAM | Phase 4 | Execution role for Runtime + Bedrock invoke. |

No other AWS services are in scope. S3/Lambda/Dynamo would dilute the
AgentCore story.

## Model to enable (do this before Phase 2)

Console → Amazon Bedrock → **us-west-2** → Model access. Kept reads
`BEDROCK_MODEL_ID` from the environment and **does not hardcode** an ID.

| Role | Model | `BEDROCK_MODEL_ID` |
| --- | --- | --- |
| Default (precision) | Claude Sonnet 4.6 | `us.anthropic.claude-sonnet-4-6` |
| Cheap iteration | Claude Haiku 4.5 | `us.anthropic.claude-haiku-4-5-20251001-v1:0` |
| AWS-native fallback | Nova 2 Lite | `us.amazon.nova-2-lite-v1:0` |

Verified 2026-09-13 against the [Claude Sonnet 4.6 model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-sonnet-4-6.html).
The US geo inference profile `us.anthropic.claude-sonnet-4-6` routes from
us-west-2 to us-east-1 / us-east-2 / us-west-2.

## Phase 2 (local, no AgentCore)

```python
from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id=os.environ["BEDROCK_MODEL_ID"],
    region_name=os.environ.get("AWS_REGION", "us-west-2"),
)
agent = Agent(model=model)
result = agent.structured_output(ExtractionResult, prompt)
```

Daemon in `KEPT_MODE=local-agent` calls this in-process. That is the
prompt-engineering loop against real transcripts.

## Phase 4 (AgentCore Runtime)

```bash
npm install -g @aws/agentcore
agentcore --version
# If this hits a Python `agentcore` on PATH, that is the legacy starter toolkit.
# Uninstall: pip uninstall bedrock-agentcore-starter-toolkit

agentcore create \
  --project-name kept \
  --name kept-agent \
  --language Python \
  --framework Strands \
  --model-provider Bedrock \
  --memory long-term \
  --build CodeZip
```

`CodeZip` avoids Docker. Memory is long-term so people persist across
invocations. Observability is created by `agentcore deploy`.

The daemon POSTs an `ExtractionRequest` to the Runtime invoke URL
(`KEPT_AGENT_URL`). Local mode keeps the in-process path.

## What we will not do

- Tunnel Bee MCP from AgentCore (localhost-only HTTP) back to the Mac.
  The daemon pre-fetches related conversations and facts and sends them
  in the request. Tradeoff logged in `FRICTION_LOG.md`.
- Store raw transcripts in AgentCore Memory. Quotes + extracted items only.

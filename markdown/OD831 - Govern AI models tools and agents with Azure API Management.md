---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/api-management
  - topic/ai-gateway
  - topic/governance
  - topic/mcp
  - topic/agents
  - topic/azure
source: https://www.youtube.com/watch?v=EZLAjW0xPxM
session_code: OD831
event: Microsoft Build 2026
speakers: Anish (APIM team), Mike Bzinski (APIM team), Shriant (APIM team)
duration_min: 39
aliases:
  - Govern AI models, tools, and agents with Azure API Management
---

# OD831 — Govern AI models, tools, and agents with Azure API Management

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Anish, Mike Bzinski, and Shriant — all from the Azure API Management product team  
> **Duration:** ~39 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=EZLAjW0xPxM)

## 🎯 TL;DR
Azure API Management (APIM) is being repositioned from a traditional API gateway into a **universal gateway** that governs APIs, AI models, MCP tools, and agents through one consistent control plane. The session frames AI as no longer a pilot (Gartner: 95%+ of enterprises using LLMs/GenAI in production by 2028) and argues that the same governance, security, observability, and velocity problems enterprises solved for APIs are now magnified for AI. The **AI Gateway** capabilities inside APIM act as the bridge mediating client→model, client→tool, and client→agent access, layering token rate limiting, content safety, semantic caching, model routing/fallback, PII protection, and end-to-end tracing on top. **API Center** is the companion enterprise catalog (system of record) for all AI assets — REST APIs, MCP tools, skills, plugins, models, and agents — with Git-sync registration and LLM-as-a-judge quality scoring. Several launches landed: Anthropic + Vertex model policy support (this June), GA of expanded token metrics, the new **Unified Model API** (preview) with model aliases and cross-provider failover, GA of **Bring Your Own Model** in Microsoft Foundry, and **GA of Agent-to-Agent (A2A) governance** in APIM.

## 🔑 Key Takeaways
- APIM is evolving into a **universal gateway**: one governance lens for traditional APIs, model APIs, tools/MCP, and agents — so enterprises don't piecemeal multiple gateway/governance solutions.
- The **API Management platform = two products**: API Management (the managed + self-hosted gateway) and **API Center** (the catalog to track, discover, and govern assets regardless of type or location).
- "AI Gateway" is shorthand for the AI-specific capabilities inside APIM; it mediates all AI usage across five pillars: **governance, scalability, security & safety, observability, velocity**.
- **Token rate limits & quotas** let you cap consumption per user/agent, attribute usage, set alerts, and build cost dashboards — cost control is the headline concern for AI workloads.
- **Content safety policies** moderate prompts/completions and block harmful (e.g. hateful) requests *before* they reach the backend model; PII leakage prevention is built in.
- **Semantic caching** reduces token consumption (and therefore cost) by serving cached answers for semantically similar prompts.
- **Model routing & fallback**: prioritize provisioned (PTU) capacity for specific models and implement fallback strategies for reliability or cost.
- APIM supports **all major model providers**: Microsoft Foundry, OpenAI, Google Vertex AI, AWS Bedrock, Hugging Face, Anthropic, Mistral — plus clients like users, agents, and GitHub Copilot coding agents.
- **NEW (June this month):** Anthropic (Messages API) and Vertex models can now get the full policy set — token limits/metrics, content safety, semantic caching — plus logs/metrics import.
- **NEW (GA):** Expanded **token metrics** via the `llm-emit-token-metric` policy — captures *all* token types (completion, prompt, thinking/reasoning, cache) into Application Insights for accurate cost/usage dashboards.
- **NEW (Preview):** **Unified Model API** — a single APIM-fronted API that translates between Anthropic Messages API and OpenAI Chat Completions backends; includes **model aliases** to decouple client-facing names from backend models and **cross-provider failover**.
- **NEW (GA):** **Bring Your Own Model** in Microsoft Foundry — register any Chat-Completions-compatible model proxied by AI Gateway (APIM or third-party) for use in the Foundry agent service.
- **Tools = APIs or MCP servers** that turn LLM intelligence into action; more tools = exponentially more security/compliance/performance risk, so they need the same gateway governance.
- You can **convert existing REST APIs into MCP servers in a few clicks (no rewrites)** and **proxy first- or third-party MCP servers** (Stripe, Jira, Atlassian, Box, Neon, etc.) to apply unified governance and auth via Credential Manager.
- **NEW MCP capabilities:** MCP servers in the Products concept (bundling, subscriptions, quotas, approval workflows), **MCP versioning** (A/B test, blue-green, prod vs dev), finer OpenTelemetry metrics/traces/logs, and MCP as a first-class element in the management REST API; plus a **built-in test console** (no external MCP Inspector needed).
- **API Center** is the enterprise catalog/system of record for four+ asset types (REST APIs, MCP tools, skills/plugins, models, agents) with **Git-repo sync**, **LLM-as-a-judge quality scoring** (4 dimensions, 1–5 scale, default threshold 3), and a **marketplace endpoint** that surfaces skills/plugins/MCP to Claude Code and Copilot CLI.
- **NEW (GA):** **Agent-to-Agent (A2A) support in APIM** — bring A2A agents under the same enterprise-grade governance, security, and observability as REST APIs (agent cards, runtime operations, Gen AI semantic-convention OTel traces, throttling/IP-filtering/content-safety policies).

## 📚 Detailed Notes

### Why now — AI is in production, not a pilot
The session opens by reframing the AI conversation: although AI and AI workflows have been discussed since 2023, **AI is no longer a pilot**. Most enterprises are moving AI into production. Gartner is cited: **by 2028, more than 95% of enterprises will be using LLMs, GenAI APIs, and models in production applications.** That shift makes governance urgent — enterprises must decide how to govern diverse AI endpoints, ensure secure access, and observe what's actually happening (cost, security, troubleshooting).

The core argument: AI brings the *same* class of challenges enterprises already faced with APIs, but **magnified**:
- **Cost control & compliance** with organizational policies.
- **Agent proliferation** — preparing systems for hundreds → thousands → millions of agents as they scale.
- **Security & safety** of systems and applications.
- **Monitoring & troubleshooting** of AI systems.
- **Developer velocity** — empowering developers to build better AI systems faster.

These are exactly the problems APIM has solved for traditional APIs for over a decade, so the thesis is that APIM is the natural place to solve them for AI too.

### The API Management platform = two products
Before going deeper, the speakers set context on what "the platform" means:
1. **Azure API Management** — the gateway solution to securely **publish, manage, and analyze APIs** across all environments through a managed gateway. There is also a **self-hosted gateway** offering; together these are "API Management."
2. **Azure API Center** — the **catalog** to **track, discover, and govern** APIs within an organization, regardless of API type or where the APIs are located.

Together, these two products form the **Azure API Management platform**, which is the subject of the whole talk.

### From API gateway to universal gateway
APIM has supported the full API lifecycle — **design, develop, secure, publish, scale, monitor, analyze** — for traditional APIs for over a decade, with **40,000+ customers processing trillions of requests per month**. The strategic direction is to evolve it into a **universal gateway** that handles far more than REST:
- **Model APIs** — Azure AI Foundry, AWS Bedrock, Google Vertex AI, OpenAI, Anthropic, Mistral, or anywhere else models are hosted.
- **Tools** — MCP endpoints, OpenAPI specs, or custom connectors.
- **Agents** — agents built on protocols like **A2A** get the same governance lens as traditional APIs.

The value proposition: **one solution for governance across all API endpoint types**, so teams don't have to piecemeal effort across multiple gateway/governance products. APIM is positioned as simultaneously your **API gateway, AI gateway, model gateway, tools gateway, and agents gateway** — a single universal gateway for the entire product stack.

### What "AI Gateway" actually is
"AI Gateway" is the simplified name for the **AI-specific capabilities within APIM**. Conceptually it's a **bridge that mediates all AI usage**:
- **Left side (clients):** users, apps & services, agents, co-pilots.
- **Right side (backends):** AI models (from the many providers above), tools (MCP servers, APIs), and agents.

Every client→backend interaction is mediated by the AI Gateway, which applies five pillars: **governance, scalability, security, safety, observability, and velocity** — directly mapping to the AI challenges raised earlier.

### How the pillars are delivered (API gateway + AI gateway capabilities combined)
The approach combines **existing API gateway capabilities** with **new AI-purpose-built capabilities**, organized by problem:

**Governance**
- Existing: an extensive selection of **policies**, **federated API management with workspaces**, and **enterprise-wide catalogs**.
- Extended for AI: catalogs now cover **approved models, MCP servers, skills, plugins, and A2A agents**; **granular token rate limits and quotas** for cost management; policy enforcement for MCP and A2A endpoints (secured access, content safety, secret-leak prevention).

**Security & safety**
- Existing: **OWASP API Top 10** protections, client authn/authz, **keyless management**, **identity**, **Credential Manager**.
- Extended for AI: **moderate prompts and completions** and **prevent PII / private-information leakage**.

**Observability**
- Existing: robust **logs, metrics, and tracing**.
- Extended for AI: **track token consumption**, **log prompts and completions**, **log MCP tool interactions** (requests *and* responses), and **trace end-to-end agentic interactions**.

**Scalability**
- AI-specific: **saving tokens & improving latency via semantic caching**, **prioritizing routing to provisioned capacity** and specific models, **model fallback** for reliability or cost, and support for **both SSE and streaming HTTP** protocols (depending on how the tool is built).

**Velocity**
- **Developer portal**, **VS Code extensions**, **Copilot for policies**, and **test consoles for tools** built directly into the APIM portal (test MCP-protocol tools in place).
- Extended for AI: **import AI Foundry models / tools from other providers** (not just Foundry/APIM — import from anywhere), **wrap existing/external MCP servers** (Azure, off-Azure, or on-prem) and expose them as **private endpoints**, **convert existing REST APIs into MCP servers** (no duplicated work), and **discover/consume assets via the API Center MCP server**.

### Model governance (Mike Bzinski)
The **model gateway** capabilities recap and expand on the above:
- **Token rate & quotas** — monitor token consumption, attribute it to specific users or agents, set alerts, build dashboards.
- **Moderate prompts & completions** — log them for investigation/audit.
- **Semantic caching** — reduce token consumption / the actual cost of token consumption on models.
- **Routing** — prioritize **provisioned capacity** for certain models, implement **model fallback** strategies.
- **Backends supported** — Microsoft Foundry, OpenAI, Google Vertex AI, AWS Bedrock, Hugging Face, and any other provider; clients include users, agents, and **GitHub Copilot coding agents**.

**Model governance demo (AWS Bedrock):** A model deployed on AWS Bedrock (in Amazon's cloud) is imported as an API in APIM with two policies: (1) a **token limit of 10 tokens/minute per user**, and (2) a **content safety** policy. A sample app loops requests to demonstrate enforcement:
- First request ("explain Azure API Management in 10 words") **succeeds** with a proper answer.
- The **second request fails** — the token-limit policy throttles it because the quota is exceeded; the AI Gateway returns a throttle response.
- Changing the prompt to a hateful one ("I hate you") causes the AI Gateway to **block the request** under the content safety policy **before it ever reaches the backend model**.
The same capabilities already work for OpenAI models, Microsoft Foundry models, and other OpenAI-compatible models.

### Model governance launches (Mike Bzinski)
Mike walks through several model-gateway announcements:

**1. Anthropic + Vertex policy support (this June).** Starting June this month, the same policy set — **token limits, token metrics, content safety, semantic caching, etc.** — applies to **Anthropic models (via the Anthropic Messages API)** and **Vertex models deployed on Google Cloud**. Logs and metrics can be collected for those models, and cloud operations can be imported as part of the Microsoft import in APIM.

**2. GA: expanded token metrics.** The `llm-emit-token-metric` policy now collects metrics for **all token types** — not just completion and prompt tokens, but also **thinking/reasoning tokens, cache tokens**, and others. It forwards these metrics to **Application Insights**, where you can set alerts or build more complete and accurate dashboards for token usage and model consumption cost.

**3. Preview: Unified Model API.** A new API that creates **a single APIM API in front of multiple backend model providers**. Initially the supported backends are **Anthropic models (Messages API)** and **OpenAI-compatible models (Chat Completions API)**. A **client-facing Chat Completions interface automatically translates** calls to Anthropic and OpenAI backends, so clients can standardize on a single SDK / interface while many different backend models run behind it. Key sub-features:
- **Model aliases** — decouple backend and client model names. Example: create an alias `GPT` that forwards to the `GPT 5.3` backend; later swap the alias to `GPT 5.4` or even to a different provider (e.g. Anthropic) **without affecting any clients**. Clients only ever use the alias; you keep full control of the real backend.
- **Centralized governance** — apply a policy once and it works across all backend models from different providers.
- **Cross-provider failover** — fail over from, e.g., an OpenAI GPT model to an Anthropic Claude model even though they use different backend API formats; APIM handles the translation.

**4. GA: Bring Your Own Model in Microsoft Foundry.** Lets you add **any model proxied by an AI Gateway** (Azure APIM or a third-party gateway) that is **Chat Completions API compatible**, and use it for building prompt-based agents in the **Foundry agent service**. (More detail at the linked docs.)

### Tool governance (Anish)
**What is a "tool"?** Tools are **APIs or MCP servers** used within the enterprise. Models/LLMs supply *intelligence*; tools turn that intelligence into *action* by connecting agents/LLMs to APIs and services. The challenge: enterprises have built a huge sprawl of APIs and tools over the last couple of decades — how do they **repurpose that estate for the AI world**? And critically, **the more tools you add, the more risk you create** — security, compliance, and performance risk grows **exponentially** (per multiple surveys) with each added tool.

**AI Gateway as the tool bridge.** Just as it mediates model usage, the AI Gateway mediates **tool usage**, solving the same five issues (governance, security, observability, velocity, scalability) across tool backends:
- **API/cloud backends** — Logic Apps, Functions, Container Apps, etc.
- **Third-party MCP servers** — Atlassian, Stripe, Box, Neon, and others — mediated natively with the same governance policies as first-party APIs.

**What you can do with APIM tools today:**
1. **Create MCP servers** — convert your existing REST API portfolio into MCP servers **in a few clicks, no rewrites**; expose any HTTP backend as an MCP server **in under a minute**.
2. **Proxy existing MCP servers** — first-party (self-hosted) or third-party (Stripe, Jira, etc.) — to apply the same governance and security perimeter.
3. **Secure the endpoints** — ensure agents/LLMs are **authenticated** with the right access and scopes; streamline access to MCP servers that have their own auth (API keys or OAuth) using **Credential Manager** and policies.
4. **Apply organizational policies** — content safety (no PII leakage), throttling (prevent tool abuse by agents/LLMs), and more.
5. **Observability for every call** — clear logs, traces, and metrics on each tool invocation for root-causing and performance tuning.

The consistent theme: **same gateway, same policies** whether the caller is a REST client, an agent, or an MCP-aware coding tool.

### What's new for MCP / tools (Anish)
Recently shipped MCP/tool capabilities in APIM:
- **MCP in the Products concept** — bundle one or more MCP servers into APIM **products** with **subscriptions, quotas, and approval workflows**, creating curated rule sets per product.
- **MCP versioning** — create multiple versions of an MCP server to support **A/B testing, experimentation, blue-green deployments**, or running one version in prod and another in dev simultaneously.
- **Finer observability** — more fine-grained data and metrics for MCP tools via **OpenTelemetry**; track **end-to-end** from client → APIM gateway → MCP server, including which tool was invoked.
- **MCP as a first-class element in the management REST API** — create, secure, and apply policies to MCP servers programmatically via the APIM REST API, without going through the portal.

**MCP demo (APIM portal, V2 instance):**
- Under **MCP servers** in the AI Gateway section, the presenter creates a new MCP server pointing at a third-party server (`mcp.stripe.com`), gives it a display name and base path, and **assigns it to a product** during creation (then the product can be configured further).
- After creation, **policies and settings** can be applied — including **subscription keys** to authenticate access. A simple access policy is applied (a key, hardcoded for demo simplicity).
- A **built-in test console** is shown — **no external MCP Inspector needed**; it auto-lists the tools and lets you invoke them directly.
- **Versioning** is demoed by creating a **v2** of the "MCP test build 2026" server, resulting in two versions (original + v2) with separate private endpoints for experimentation / A/B testing / blue-green.

**Agent tool discovery at design time (demo by Mike):** A prototype shows the AI Gateway simplifying **tool discovery while building an agent**:
- Start with an intent: *"I want to build an agent that calculates shipping costs for online orders."*
- From that intent, **GitHub Copilot queries the AI Gateway's MCP server** to discover available tools, **automatically selecting relevant ones** (order lookup, US + international shipping cost) and **excluding irrelevant ones** (e.g. weather forecasting).
- After the developer confirms the selected tools, **Copilot generates the full agent code using the GitHub Copilot SDK** — not just a scaffold, but correct tool definitions and chaining logic derived from tool metadata/descriptions. The agent is then ready to run locally or **deploy to Foundry**.
- **How it works:** (1) a lightweight **custom skill** connects GitHub Copilot to the AI Gateway so Copilot can discover tools and generate code; (2) the **GitHub Copilot CLI** is configured with the AI Gateway's MCP server as the discovery endpoint for all exposed tools. For the prototype, the (future) AI Gateway — described as a *cloud-native, multi-tenant, always-on component that combines APIM + API Center* — is **mocked using standalone APIM + API Center resources**. API Center exposes the MCP server with tools auto-synced from APIM; irrelevant tools are filtered out by Copilot during discovery; APIM provides the tool runtime and the REST→MCP conversion.
- **Future prototyping:** dynamic tool selection at **agent runtime** (not just design time) and routing **all model calls through the AI Gateway** to enforce governance (e.g. token consumption limits).

### Enterprise catalog for AI assets — API Center (Shriant)
As enterprises scale AI investments, the recurring question is **"how do we manage all of it?"** — the agents, skills, MCP servers, and models. Teams need to **discover what exists, ensure quality, and prevent duplication**. **Azure API Center** is positioned as the answer: the **enterprise catalog and single system of record** where every tool an agent might call is **registered, tracked, and discoverable** across the org.

**Catalog scope — four+ asset types:** REST APIs, MCP tools, skills/plugins, models, and agents.

**Keeping it current is effortless:** register via the **portal, CLI, or direct GitHub repo sync** — **no manual drift**; assets ship as new commits are made.

**Quality assessment (LLM-as-a-judge):** all assets are evaluated for clarity, parameter design, and safety so developers *and* agents can trust what they consume.

**Marketplace for agents:** API Center exposes a **marketplace endpoint** that lets developer tools like **Claude Code and Copilot CLI** discover and load enterprise skills, plugins, and MCP servers **directly from the catalog**, with the same lifecycle and quality signals platform teams curate. It works across **Azure, other clouds, on-prem, and third-party SaaS** — *one catalog, every asset.*

**API Center demo — skills:**
- **Register a skill** from the Assets sidebar: provide capabilities, use cases, behavior, and the **Git repo URL** of the skill source (e.g. a new "code review" skill pointing at its skill-markdown file).
- **Git-sync at scale:** integrate a Git repo so any skill added/updated there **auto-syncs** to the API Center inventory. The demo integrates the **Azure skills Git repository**, which then auto-imports all Azure skills as discoverable assets.
- **Discovery:** the portal lets developers find skills (e.g. the **Azure cloud migrate** skill for assessing/migrating cross-cloud workloads); clicking a skill opens its **definition, reference docs, common tasks, and defined inputs/outputs**. Developers contribute new skills by committing to the integrated Git repo; pushes auto-sync to the catalog with no manual intervention.

**Skills assessment (LLM-as-a-judge detail):** A large language model evaluates AI outputs against defined quality criteria, scoring across dimensions like **accuracy, coherence, helpfulness**. The judge can use **rubrics, reference answers, or pair-wise comparisons** for scalable feedback at a fraction of human-annotation cost. API Center ships **default criteria** across **four dimensions, each scored 1–5 with a default threshold of 3**:
- **Documentation clarity** — how clearly the skill's purpose/behavior is communicated.
- **Help/completeness** — whether the output is a comprehensive standalone reference.
- **Discoverability** — how easily functionality can be navigated/found.
- **Safe usage** — whether sufficient guidance is provided for safe operation.
Platform admins can **extend with custom criteria** for org-specific standards, compliance, and governance. Developers then see a **detailed AI quality score report** per skill in the portal — an at-a-glance **pass/fail**, per-dimension scores, and actionable feedback — plus **structural checks** (valid front matter, skill name, body content) and **schema validation** (flags missing sections like examples or error handling). This lets developers judge a skill's quality/reliability **before adopting it**.

**API Center demo — MCP tools:** As the MCP ecosystem grows, orgs need scalable, automated registration. **Git-repo integration** keeps the MCP inventory in sync as tools evolve, giving a **single source of truth**. The demo imports the **Azure MCP server** into API Center via Git-repo sync, showing how fast a real-world MCP server goes from repo → fully registered, discoverable asset. The portal's **built-in MCP Inspector** lets developers explore tools, inspect inputs/outputs, and test them in real time **without writing any code**; the API Center **data-plane MCP server** lets developers list every MCP tool in the catalog and search for a specific server.

**API Center demo — plugins:** Plugins are **self-contained extensions** that supercharge supported AI dev tools, adding custom **commands, agents, hooks, and MCP integrations** to Copilot CLI, Claude Code, and beyond. Registration takes a **title, summary, description**, and a **version** (to track releases). The power move: **bundle skills and MCP servers directly inside the plugin**, so consumers get one self-contained, immediately actionable asset. The portal gives a single place to **browse, search, and discover plugins** alongside APIs, skills, and MCP servers — eliminating scattered repos and tribal knowledge — with each plugin surfacing its bundled skills/MCP servers in one view.

**API Center data plane brings it together:** API Center exposes a **marketplace endpoint via its data-plane API**, surfacing plugins directly to **Claude Code and Copilot CLI** so discovery happens **without leaving the dev environment**. Register the endpoint with Copilot CLI in **one step** and the full plugin catalog is instantly unlocked — browse, select, and plug in right from the CLI.

### Agent governance & A2A (Anish)
As agents proliferate, **raw unmediated access to backends doesn't scale**. Users, apps, agents, and co-pilots all make calls against A2A, REST, and HTTP backends spanning any cloud and on-prem. You need a **trusted thing in the middle — the AI Gateway** — delivering the same five pillars (governance, scalability, safety & security, observability, velocity): *one bridge for every agent, fully governed.*

**Announcement — A2A support is GA today.** Agent-to-Agent (A2A) is becoming the backbone of **multi-agent architectures**. You can now bring **A2A agents under the same enterprise-grade management** you rely on for REST APIs — **same governance, same security, same observability** — alongside all your other APIs:
- **Expose agent cards and runtime operations.**
- **Log OpenTelemetry traces using Gen AI semantic conventions** for deep, standardized visibility.
- **Apply policies** like **throttling, IP filtering, and content safety** to every agent call.
- **Inventory and publish** agent APIs.
Registering an A2A agent is simple, with **agent-specific metadata** (agent card, agent URL) surfaced natively alongside lifecycle and deployment details.

### Wrap-up
Everything shown is **available to use and build with today**. More details are promised at the **AKA.ms API blog** (`aka.ms` API blog).

## 🛠️ Products / Features / Technologies Mentioned
- **Azure API Management (APIM)** — the managed (and self-hosted) gateway to securely publish, manage, and analyze APIs; now the "universal gateway" for APIs, models, tools, and agents.
- **Azure API Center** — the enterprise catalog / system of record to track, discover, and govern AI assets (REST APIs, MCP tools, skills, plugins, models, agents).
- **AI Gateway** — shorthand for the AI-specific capabilities inside APIM that mediate client→model/tool/agent access across governance, scalability, security/safety, observability, velocity.
- **Self-hosted gateway** — APIM gateway you run in your own environment; part of "API Management."
- **Workspaces / federated API management** — governance construct for delegating management across teams.
- **Token rate limits & quotas** — cap and attribute token consumption per user/agent for cost control.
- **Content safety policy** — moderates prompts/completions, blocks harmful requests before reaching the backend model.
- **Semantic caching** — serves cached responses for semantically similar prompts to cut tokens/cost and latency.
- **`llm-emit-token-metric` policy** — emits all token-type metrics (prompt, completion, thinking/reasoning, cache) to Application Insights.
- **Unified Model API** — single APIM API fronting multiple model providers with translation, aliases, and failover.
- **Model aliases** — decouple client-facing model names from backend models for hot-swapping providers/versions.
- **Model routing / fallback** — prioritize provisioned (PTU) capacity and fail over across models/providers.
- **Credential Manager** — manages backend auth (API keys, OAuth) for tools/MCP servers and AI endpoints.
- **MCP (Model Context Protocol) servers** — tool endpoints; created from REST APIs or proxied (first/third-party) through APIM.
- **MCP versioning** — multiple versions of an MCP server for A/B testing, blue-green, prod vs dev.
- **MCP in Products** — bundle MCP servers into APIM products with subscriptions, quotas, approval workflows.
- **Built-in MCP test console / MCP Inspector** — test MCP tools in-portal without an external inspector.
- **APIM management REST API** — MCP now a first-class element for programmatic create/secure/policy.
- **OpenTelemetry + Gen AI semantic conventions** — standardized tracing/metrics/logs for tools and agents.
- **Application Insights** — destination for token metrics, dashboards, and alerts.
- **Microsoft Foundry (Azure AI Foundry)** — model host and agent service; target for Bring Your Own Model.
- **Foundry agent service** — builds prompt-based agents using models proxied by AI Gateway.
- **Bring Your Own Model (Foundry)** — register any Chat-Completions-compatible, gateway-proxied model in Foundry.
- **A2A (Agent-to-Agent) protocol** — multi-agent communication; now governed via APIM (agent cards, runtime ops).
- **GitHub Copilot (SDK + CLI)** — client/coding agent; discovers tools via AI Gateway MCP and generates agent code.
- **Claude Code** — developer tool that consumes the API Center marketplace endpoint for skills/plugins/MCP.
- **LLM-as-a-judge** — technique for automated quality scoring of skills/assets in API Center.
- **Skills & Plugins** — catalog asset types; plugins bundle skills + MCP servers + commands/agents/hooks.
- **Model providers supported** — Microsoft Foundry, OpenAI, Anthropic (Messages API), Google Vertex AI, AWS Bedrock, Hugging Face, Mistral.
- **Third-party MCP servers referenced** — Stripe, Jira, Atlassian, Box, Neon.
- **Azure compute backends referenced** — Logic Apps, Azure Functions, Container Apps.
- **Azure MCP server / Azure skills repo** — sample assets imported into API Center via Git-repo sync.
- **OWASP API Top 10** — baseline API security protections inherited by AI endpoints.
- **SSE & streaming HTTP** — both transport protocols supported for tools/agents.

## 🚀 Announcements / What's New
- **Anthropic + Vertex model policy support — launching June (this month).** Full policy set (token limits, token metrics, content safety, semantic caching) now applies to **Anthropic models via the Anthropic Messages API** and **Vertex models on Google Cloud**, including logs/metrics collection and cloud-operations import. *(Rolling out this month.)*
- **GA — Expanded token metrics.** The `llm-emit-token-metric` policy now captures **all token types** (prompt, completion, thinking/reasoning, cache, etc.) into Application Insights for accurate cost/usage dashboards. *(Generally Available.)*
- **Preview — Unified Model API.** Single APIM API fronting multiple backends (initially **Anthropic Messages API** + **OpenAI-compatible Chat Completions**), with automatic translation, **model aliases** (decouple client/backend names), **centralized cross-provider governance**, and **cross-provider failover**. *(Now in Preview.)*
- **GA — Bring Your Own Model in Microsoft Foundry.** Add any **Chat-Completions-compatible** model proxied by an AI Gateway (APIM or third-party) and use it to build prompt agents in the Foundry agent service. *(Generally Available.)*
- **GA — Agent-to-Agent (A2A) support in APIM.** Govern A2A agents with the same enterprise-grade governance, security, and observability as REST APIs — agent cards, runtime operations, OTel Gen-AI-semantic-convention traces, throttling/IP-filtering/content-safety policies, inventory/publish. *(Generally Available today.)*
- **Recently shipped (MCP/tools, status not explicitly labeled):** MCP in the Products concept (bundling/subscriptions/quotas/approval workflows), **MCP versioning**, finer OpenTelemetry observability for MCP tools, MCP as a first-class element in the management REST API, and the built-in MCP test console.

## 💡 Demos
- **Model governance (AWS Bedrock).** A Bedrock-hosted model imported into APIM with a 10-token/min/user limit + content safety policy. First request succeeds; second is **throttled** by the token policy; a hateful prompt is **blocked** by content safety **before reaching the backend** — proving policy enforcement at the gateway.
- **MCP server creation & management (APIM portal, V2 instance).** Create an MCP server from a third-party endpoint (`mcp.stripe.com`), assign it to a product during creation, apply an access policy with a subscription key, test tools in the **built-in test console** (no external inspector), and create a **v2 version** (two endpoints) for A/B testing / blue-green — proving the new MCP product/versioning/test-console features.
- **Agent tool discovery at design time (GitHub Copilot + AI Gateway).** From the intent "build an agent that calculates shipping costs," **GitHub Copilot queries the AI Gateway's MCP server**, auto-selects relevant tools (order lookup, US/intl shipping), excludes irrelevant ones (weather), and **generates full agent code via the Copilot SDK** ready to run locally or deploy to Foundry — proving gateway-driven, metadata-based tool discovery + code-gen (prototype; AI Gateway mocked with standalone APIM + API Center).
- **API Center — skills.** Register a "code review" skill with a Git repo URL, then integrate the **Azure skills Git repository** so all skills auto-sync and become discoverable (e.g. the Azure cloud-migrate skill, with full definition/docs/inputs/outputs) — proving Git-sync registration + discovery.
- **API Center — skills assessment.** Default LLM-as-a-judge scoring across 4 dimensions (documentation clarity, help/completeness, discoverability, safe usage; 1–5, threshold 3) plus structural + schema checks, surfaced as a pass/fail quality report — proving automated quality gating before adoption.
- **API Center — MCP tools.** Import the **Azure MCP server** via Git-repo sync; use the **built-in MCP Inspector** to explore/test tools with no code; list/search every MCP tool via the data-plane MCP server — proving automated MCP registration + discovery.
- **API Center — plugins & data-plane marketplace.** Register a plugin (title/summary/description/version) that **bundles skills + MCP servers**; surface it via the **marketplace endpoint** to Claude Code and Copilot CLI; register the endpoint with Copilot CLI in **one step** to unlock the full plugin catalog from the CLI — proving in-IDE discovery without leaving the dev environment.

## 📊 Notable Stats / Quotes
- **Gartner: by 2028, more than 95% of enterprises** will be using LLMs, GenAI APIs, and models in production applications.
- **40,000+ APIM customers** processing **trillions of requests per month**.
- **Token limit demo:** 10 tokens/minute per user (deliberately low to trigger throttling on the second call).
- **Skills assessment:** 4 default dimensions, scored on a **1–5 scale**, **default threshold of 3**.
- *"AI is no longer a pilot… most enterprises are starting to deploy AI in production."*
- *"The more tools you add, the more risk you create — the risk grows exponentially."*
- *"Same gateway, same policies whether it's a REST client or an agent or an MCP-aware coding tool."*
- *"One catalog, every asset."* (API Center positioning)
- *"One bridge for every agent, fully governed."* (Agent governance)

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up an APIM V2 instance and **convert an existing REST API into an MCP server** in the portal; test it in the built-in test console.
  - Apply a **token-rate-limit policy + content safety policy** to a model API and reproduce the throttle + block behavior.
  - Wire `llm-emit-token-metric` into **Application Insights** and build a token-cost dashboard covering reasoning + cache tokens.
  - Try the **Unified Model API** (preview): create a `GPT` alias over an OpenAI backend, then swap the alias to Anthropic and confirm clients are unaffected; test cross-provider failover.
  - Integrate a **Git repo with API Center** and watch skills/MCP auto-sync; review the LLM-as-a-judge quality report.
  - Register the **API Center marketplace endpoint with Copilot CLI** and load enterprise plugins from the CLI.
  - Register an **A2A agent** in APIM and confirm OTel Gen-AI-semantic-convention traces flow.
- [ ] Questions:
  - When does the standalone, multi-tenant, always-on **AI Gateway** (combined APIM + API Center) GA, vs today's mocked/standalone setup?
  - Will **runtime** (not just design-time) tool selection via AI Gateway reach preview/GA, and what's the latency overhead?
  - Which additional providers beyond Anthropic + OpenAI will the **Unified Model API** translate for next?
  - What are the exact **pricing implications** of token metrics + semantic caching at scale?
  - How do **content safety** policies on the gateway interact with model-native safety filters (double-filtering)?
- [ ] Relevant to:
  - Enterprise AI platform / landing-zone governance and FinOps (token cost control).
  - MCP tool/agent rollout where a single governance + security perimeter is required.
  - Multi-provider model strategies needing provider-agnostic SDKs and failover.

## 🔗 Related
- [[ODSP923 - Create enterprise apps with AI and MCP]] — enterprise apps built on MCP; complements APIM's MCP governance.
- [[Azure API Management]] — product hub note for APIM concepts, policies, and gateways.
- [[Model Context Protocol (MCP)]] — protocol background for tools/servers governed here.
- [[Azure AI Foundry]] — model host + agent service; target for Bring Your Own Model and agent deployment.
- [[AI Gateway]] — the gateway pattern for mediating model/tool/agent access.
- [[Agent-to-Agent (A2A)]] — multi-agent protocol now governable in APIM (GA).
- [[GitHub Copilot]] — client/coding agent used for tool discovery and agent code-gen in the demos.
- Source list: [[2026 Build Session List]]

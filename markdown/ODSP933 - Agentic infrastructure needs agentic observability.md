---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/observability
  - topic/agents
  - topic/ai
  - topic/monitoring
  - topic/sre
source: https://www.youtube.com/watch?v=rXd7KDBmU5A
session_code: ODSP933
event: Microsoft Build 2026
speakers: Jimmy (Solutions Engineering Lead, Groundcover)
duration_min: 14
aliases:
  - Agentic infrastructure needs agentic observability
---

# ODSP933 — Agentic infrastructure needs agentic observability

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Jimmy — Solutions Engineering Lead, Groundcover  
> **Duration:** ~14 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=rXd7KDBmU5A)

## 🎯 TL;DR
A vendor session from **Groundcover** framed not as a product pitch but as a **diagnosis**: observability as a category is breaking because its consumer is changing from humans to agents. For 15 years, logs, traces, dashboards, and alerts were all optimised around **human cognitive limits** — less data, simpler views, smaller cardinality, summaries. But agents now write code, operate systems, and debug failures without a human in the loop, and they *thrive on more context*, not less. Jimmy walks through three structural failures — **logs** (events vs. reasoning trails), **traces/sampling** (sampling misses the journey, "200 OK means nothing"), and **sensitivity/instrumentation** (telemetry now holds PII/prompts; manual instrumentation can't keep up with AI velocity) — then argues for an architecture built for **data abundance**: complete system state, bring-your-own-cloud, zero instrumentation, and a "move the LLM up, push the analysis down" investigation model where the agent orchestrates and a deterministic backend does the analytical work. The closing thesis: **observability is becoming the operating system for the agentic SDLC**, and "AI can't fix what AI can't see."

## 🔑 Key Takeaways
- **The consumer of observability has changed from humans to agents** — and once that happens, the assumptions underneath the entire category start to fail. This is a *systems* problem, not a "better dashboards / more AI features" problem.
- **Logs were built for events; agents produce decision breadcrumbs.** Traditional logging assumes discrete events, stable schemas, and human-readable meaning ("request started," "cache missed"). Agents emit a **reasoning trail**, not an event stream.
- The question shifts from *"what happened?"* to **"why did the agent make this decision?"** — why these documents, why block this output, why retry this tool five times. Reasoning spans long time horizons and wide context windows.
- **Agent systems don't fail cleanly.** The same input can produce different behaviours; the same workflow can make different decisions. Understanding the **reasoning path** matters more than the infrastructure path.
- **Sampling fundamentally breaks for agents.** Head-based sampling of a non-deterministic flow tells you almost nothing — the one trace you keep may miss the path that mattered. Tail-based sampling collapses too (holding ~50,000 spans per session in memory "falls apart pretty quickly").
- **"200 OK means nothing"** in agent systems — a success status only means *nothing crashed*. The infrastructure can succeed while the outcome is completely wrong (wrong context, wrong tool, hallucinated answer, misunderstood intent).
- **Agent failures are rare and non-deterministic**, so sampling *guarantees* you miss the exact journey you needed to debug.
- **The economics break.** Observability vendors historically charged for telemetry ingestion. Agents explode telemetry volume (thousands of spans, hundreds of tool calls per workflow), forcing a bad trade-off: keep the data and absorb cost, or cut visibility and hope key signals survive. Neither works.
- **Telemetry is now the most sensitive data in the company** — it contains prompts, customer conversations, PII, financial info, internal business logic. Shipping it to a SaaS vendor becomes a *liability* discussion, not just a cost one.
- **Manual instrumentation is collapsing under AI velocity.** AI generates services and workflows faster than humans can keep instrumentation current, so the observability layer itself must learn to **instrument automatically**.
- **We built the whole industry for the wrong consumer.** Old optimisations (summaries, simpler systems, reduced telemetry) become *constraints* for agents, which perform better with full context and complete system state.
- **Better models don't automatically fix observability** — smarter models on incomplete telemetry still make bad decisions. **Context quality matters as much as (or more than) model quality.** "The agent's reasoning is only as good as its data."
- **External agents are always "guests"** — they don't control the API surface, indexing, or correlation primitives, so they operate on **partial context**, which is exactly what creates **hallucinated diagnoses** (a pointed critique of MCP-style demos).
- **Observability is becoming active, not passive** — eventually instrumenting on the fly, raising fidelity dynamically, and supporting remediation during incidents. It becomes the **operating system for the agentic SDLC**, raising hard governance questions about autonomy, approval, and ownership of agent-driven actions.

## 📚 Detailed Notes

### The framing: a diagnosis, not a product pitch
Jimmy (Solutions Engineering Lead at **Groundcover**) opens with a historical setup: *"Once upon a time, humans wrote software, humans operated software, and humans debugged software. Observability was built around this."* Logs, traces, dashboards, and alerts all assumed **a human investigator sitting in front of the data trying to figure out what happened**.

That world is changing. Agents now **write code, operate systems, make decisions, debug failures, and interact with infrastructure without a human in the loop**. The core thesis: once the *consumer* of observability changes from humans to agents, **the assumptions underneath the category start to fail**.

He's explicit that this isn't a feature problem ("we need better dashboards or more AI features") — it's a **systems problem**. The operating assumptions underneath observability are changing. He calls the talk "a diagnosis" of something fundamental that stopped working once AI systems became part of the software lifecycle itself.

### Problem 1 — Logs: built for events, but agents produce decision breadcrumbs
Traditional logging assumes three things: **discrete events, stable schemas, and human-readable meaning.** Classic log lines are events: *request started, request completed, database failed, cache missed.*

Agents don't behave like that. A single agent **retrieves documents, scores relevance, applies policies, retries tool calls, rewrites outputs, and re-evaluates context.** What's produced is not an event stream — it's a **reasoning trail**.

This changes the fundamental question. It's no longer *"what happened?"* but:
- **Why did the agent make this decision?**
- Why did it choose these documents?
- Why did it block this output?
- Why did it retry this tool five times?

This reasoning happens **across long time horizons and wide context windows**, and Jimmy argues *no observability platform today was really designed for this.*

He contrasts determinism vs. non-determinism: traditional observability assumed systems were **mostly deterministic**, so you could usually reconstruct the story afterward (a request failed → a dependency timed out → a deployment introduced latency). **Agent systems don't fail that cleanly** — the same input can produce different behaviours, and the same workflow can make different decisions. Increasingly, **understanding the reasoning path matters more than understanding the infrastructure path.**

### Problem 2 — Traces & sampling: sampling breaks and status codes lie
*"APM was built for a world that no longer exists."*

**Head-based sampling:** A random sample of a non-deterministic agent flow **tells you almost nothing**. The one trace you happen to keep may completely miss the reasoning path that actually mattered.

**Tail-based sampling:** Not a real answer either, because you're trying to **hold tens of thousands of spans in memory** waiting to decide whether something failed. At **~50,000 spans per session**, that approach "falls apart pretty quickly."

**The "200 OK" problem (the standout line, repeated twice):** *"200 OK means absolutely nothing now."* In traditional systems, a successful status code usually meant the system behaved correctly. In agent systems, it only means **nothing crashed**. The infrastructure can succeed while the **outcome is completely wrong** — the agent may have used the wrong context, selected the wrong tool, hallucinated an answer, or misunderstood intent. **"No crash" no longer means "correct."**

These failures are **rare and non-deterministic**, which makes them incredibly difficult to capture — and **sampling guarantees you miss the exact journey you needed to debug.**

**The broken economics:** Observability vendors historically made money by charging you to **ingest more telemetry** — fine when telemetry growth was predictable. But agent systems **explode telemetry volume**: one workflow can generate thousands of spans, hundreds of tool calls, and massive amounts of contextual data. Teams are forced into a bad trade-off — **keep the data and absorb the cost, or reduce visibility and hope the important signals survive.** Neither option works.

### Problem 3 — Sensitivity & instrumentation: telemetry is now your most sensitive data
*"Your telemetry now contains things you never meant to store."* — prompts, customer conversations, PII, financial information, internal business logic.

Telemetry has stopped being just **technical metadata**; it's now potentially **the most sensitive data in the company.** That changes the **risk model** completely: shipping all of it to a SaaS vendor is **no longer just a cost discussion — it becomes a liability discussion.**

Simultaneously, **manual instrumentation is collapsing under AI velocity.** Humans used to maintain instrumentation pipelines manually because systems evolved at *human speed*. Now AI **generates services and workflows faster than teams can keep instrumentation current.** The obvious implication: **the observability layer itself has to learn to instrument automatically.**

### The unifying insight: we built the industry for the wrong consumer
Zooming out, all three problems point to the same root cause: **everything built in observability was optimised for the one thing agents don't have — human limits.**

The field optimised for:
- Less data
- Simpler dashboards
- Smaller cardinality
- Reduced telemetry
- Human-readable abstractions

But **agents don't need the simplifications humans need.** In fact, **agents improve with more context**, which means many old optimisations become **constraints**.

The contrast Jimmy draws:
| Humans | Agents |
|---|---|
| Can't process 50,000 spans in a session | Can |
| Need summaries | Need full context |
| Simplify systems to understand them | Often perform better with the **entire system state** |

The vivid framing: *"We're feeding agents a summary and expecting them to understand the entire book."* That's **not a model problem — it's a data completeness problem.**

### Context quality > model quality
One of the biggest misconceptions in AI infrastructure right now, per Jimmy: assuming **better models automatically solve observability.** They don't — *"smarter models operating on incomplete telemetry still make bad decisions."* **Context quality matters just as much as model quality, possibly more.**

This grounds a **slightly controversial point about MCP-style demos**: an external agent is **always a guest**. It doesn't control the API surface, doesn't control indexing, doesn't control correlation primitives. It operates on **partial context** — and *"partial context is exactly what creates hallucinated diagnosis."* The distinction that matters: **an agent confidently hallucinating a fix vs. an agent actually understanding what's wrong.**

### The proposed architecture: built for data abundance
What agents actually need is an architecture built for **data abundance**, where agents reason over **complete system state, not a curated slice.** Jimmy notes Groundcover "happens to align very naturally with this shift," and calls out three architectural bets that mattered:

1. **BYOC — Bring Your Own Cloud (transcribed as "DYOC").** Everything stays inside *your* cloud. This matters for **control, governance, and sensitive telemetry** (directly answering the Problem-3 liability concern).
2. **Zero instrumentation, zero friction.** You can't depend on humans to manually keep instrumentation current in AI-generated systems (answering Problem 3's instrumentation collapse).
3. **One platform regardless of authorship** — whether the code was written by a human or an agent, because increasingly **it's both.**

### A new investigation model: "Move the LLM up, push the analysis down"
This is the architectural heart of the talk. The model is **not the execution engine.** The division of labour:

- **The LLM's job:** understand intent, decide the investigation strategy, generate **deterministic operations**, and interpret the results. (Orchestration.)
- **The backend's job:** do the **actual analytical work** — close to the data, accurately, cheaply. (Execution.)

*"You don't want the model brute-forcing analysis over complete context. You want the model **orchestrating investigation** over a deterministic analytical system with complete telemetry."* This separation is a very different architecture from what most observability systems were originally designed for.

### Investigation starts from intent, not navigation
Once you accept that model, **investigation changes completely**:
- **Old world:** engineers **click through dashboards manually**, piecing together what happened.
- **New world:** you start with a **goal** — *Why did this fail? What changed? Which customers were impacted?* The agent **runs the investigation, gathers the right signals, materializes the right outputs, and returns an answer plus next actions — not a dashboard, an answer.**

This also changes **development workflows**. Jimmy calls out a current anti-pattern bluntly: *"Right now, teams literally screenshot dashboards and paste them into Claude. That should not exist."* Instead, **production telemetry should flow directly into coding agents and CI/CD systems as structured context.**

### From observe to act: observability as an active operational system
Eventually these systems **don't just observe — they start acting**: raising collection fidelity dynamically, **instrumenting on the fly**, and supporting **remediation during incidents.** This is where the category looks fundamentally different: **observability stops being a passive debugging interface and becomes an active operational system** — not just showing humans what happened, but helping systems **understand, respond, and eventually recover automatically.**

### The hard governance questions
Jimmy is candid that this raises questions the industry **still underestimates**:
- **How much autonomy** should your observability layer actually have?
- If an agent **fixes a production incident at 2 a.m., who approved that action?**
- What **guardrails** govern systems that can act directly in production?
- If the agent **remediates incorrectly, who owns that outcome?**
- How do you **validate that telemetry normalized correctly** when **no human explicitly defined the schema?**

These are framed not as edge cases but as **foundational operating questions for the next generation of infrastructure systems** — *"because ultimately, the agent's reasoning is only as good as its data"* (repeated for emphasis).

### Closing thesis
*"The companies that get observability right in the agent era will have a structural advantage — not just operationally, competitively."* The reasoning: **AI cannot fix what it cannot see, and it cannot build effectively without full context.** Groundcover doesn't claim to have every answer, but says it knows the direction and the questions teams need to start asking now.

The capstone idea: **"Observability is becoming the operating system for the agentic SDLC — the data layer everything else depends on."** And the repeated tagline that bookends the talk: **"AI can't fix what AI can't see."**

## 🛠️ Products / Features / Technologies Mentioned
- **Groundcover** — The presenter's company; an observability platform positioned for the agent era. Key claim: agents on Groundcover **reason over complete system state, not a curated slice.**
- **BYOC ("Bring Your Own Cloud," transcribed as "DYOC")** — Groundcover architectural bet: all telemetry/data stays inside the customer's own cloud, for control, governance, and sensitive-data handling.
- **Zero instrumentation / zero friction** — Groundcover capability: automatic instrumentation so humans don't have to manually maintain pipelines in fast-moving, AI-generated systems.
- **APM (Application Performance Monitoring)** — Cited as the legacy paradigm "built for a world that no longer exists."
- **Head-based sampling** — Trace sampling at ingest; criticised as near-useless for non-deterministic agent flows.
- **Tail-based sampling** — Trace sampling that buffers spans before deciding; criticised as unworkable at ~50,000 spans/session.
- **MCP (Model Context Protocol) — "MCP-style demos"** — Referenced critically: external agents acting as "guests" on partial context, which leads to hallucinated diagnoses.
- **Claude (Anthropic)** — Named in the anti-pattern of engineers screenshotting dashboards and pasting them into Claude.
- **CI/CD systems & coding agents** — Where production telemetry *should* flow directly as structured context, instead of via screenshots.
- **OpenTelemetry concepts (spans, traces, telemetry)** — The underlying observability primitives whose volume and semantics break under agentic workloads (referenced generically, not by name).

## 🚀 Announcements / What's New
None explicitly announced. This is a **thought-leadership / diagnosis talk** rather than a launch session. Groundcover's existing architectural pillars (BYOC, zero instrumentation, single platform for human- and agent-written code) are described as already aligning with the shift, but **no new product, preview, or GA release is announced.**

## 💡 Demos
No live demos were shown — this was a conceptual/keynote-style session. (Notably, Jimmy was *critical* of "MCP-style demos" as misleading, arguing they run on partial context and produce hallucinated diagnoses.)

## 📊 Notable Stats / Quotes
- **"200 OK means absolutely nothing now."** (said twice) — In agent systems a success code only means nothing crashed; the outcome can still be completely wrong.
- **~50,000 spans per session** — The scale at which tail-based sampling (holding spans in memory) "falls apart pretty quickly"; also the example of what agents *can* process but humans cannot.
- **One workflow can generate thousands of spans + hundreds of tool calls** — Why agent telemetry explodes and the ingest-pricing model breaks.
- **"We're feeding agents a summary and expecting them to understand the entire book."** — Reframes the core gap as **data completeness, not model capability.**
- **"The agent's reasoning is only as good as its data."** (said twice) — The talk's central governing constraint.
- **"AI can't fix what AI can't see."** — The closing tagline that bookends the session.
- **"We built the whole industry for the wrong consumer."** — On 15 years of observability tooling shaped around human cognition.
- **"Right now, teams literally screenshot dashboards and paste them into Claude. That should not exist."** — On broken current dev workflows.
- **"Observability is becoming the operating system for the agentic SDLC."** — The forward-looking positioning statement.
- **"15 years"** — How long observability tooling has been shaped around human cognition.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Audit our current observability stack against the three failure modes — (1) are we relying on head/tail sampling that would miss non-deterministic agent paths? (2) does telemetry already contain prompts/PII we're shipping to a SaaS vendor? (3) is instrumentation falling behind AI-generated services? Pilot a "start-from-intent" investigation flow (ask "why did this fail / who was impacted" and have an agent gather signals) vs. manual dashboard clicking.
- [ ] Things to try: Evaluate **BYOC / in-your-cloud** observability options for sensitive-telemetry workloads; stop the "screenshot dashboard → paste into Claude" anti-pattern by piping structured telemetry into coding agents / CI/CD.
- [ ] Questions: Is Groundcover genuinely architecturally different here, or is "reason over complete system state" achievable with OpenTelemetry + a data lake + an agent orchestrator? What's the *real* cost story when you stop sampling and keep everything? How do you define and enforce guardrails/approvals for an agent that can remediate production at 2 a.m.? Who owns a bad auto-remediation?
- [ ] Questions: How do you validate that auto-normalized telemetry schemas are correct when no human defined them? Does "move the LLM up, push analysis down" map cleanly onto existing query engines (e.g. ClickHouse / Kusto / Prometheus)?
- [ ] Relevant to: SRE / platform engineering, AI agent observability & evaluation, anyone building or operating agentic systems in production, security/compliance teams worried about PII in telemetry, and the broader "agentic SDLC" tooling conversation.

## 🔗 Related
- [[Observability for AI agents]]
- [[Agentic AI in production]]
- [[OpenTelemetry tracing and spans]]
- [[Model Context Protocol (MCP)]]
- [[Agentic SDLC]]
- [[SRE and incident remediation]]
- [[PII and telemetry data governance]]
- Source list: [[2026 Build Session List]]

---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/observability
  - topic/opentelemetry
  - topic/foundry
  - topic/agents
  - topic/tracing
  - topic/evaluation
source: https://www.youtube.com/watch?v=WprbDyANqy0
session_code: DEM341
event: Microsoft Build 2026
speakers: Hansi (Software Engineering Manager, Foundry Observability), Nikhil Kumar (Engineer, Foundry)
duration_min: 24
aliases:
  - Any agent any cloud Standardized tracing with Foundry OpenTelemetry
---

# DEM341 — Any agent, any cloud: Standardized tracing with Foundry+OpenTelemetry

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Hansi — Software Engineering Manager, Foundry Observability team; Nikhil Kumar ("Nikkumar") — Engineer, Foundry  
> **Duration:** ~24 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=WprbDyANqy0)

## 🎯 TL;DR
Enterprises rarely run all their agents on one cloud, one language, or one framework — the production reality is a heterogeneous mess of Foundry prompt agents, LangGraph on AWS, Google ADK on GCP, and Copilot SDK as a catch-all. When something goes wrong, teams can't easily answer "which agent did this, why, and how do we stop it?" This session shows how **Microsoft Foundry observability** unifies tracing across *any agent, any cloud* — not by rewriting agents into a single framework, but by adopting **OpenTelemetry GenAI semantic conventions** with just a few lines of initialization code. A live demo stitched together four agents (Foundry prompt agent, ADK on GCP, LangGraph on AWS, and a Microsoft Agent Framework orchestrator hosted on Foundry, plus a Copilot SDK fallback) into a single unified end-to-end trace, then walked through the full operational loop: **debug → monitor → evaluate → optimize → fleet-level control**, all on one observability plane backed by Azure Monitor / Application Insights.

## 🔑 Key Takeaways
- **The core problem is heterogeneity.** Real enterprises run agents across multiple clouds, languages, and frameworks (different teams pick FoundryPrompt agents, LangGraph/AWS, ADK/GCP, Copilot SDK) → different metrics, different dashboards, no single pane of glass.
- **Foundry observability is the unifying answer** — it lets you debug, monitor, and evaluate any agent regardless of framework or hosting location, in one place.
- **OpenTelemetry is the bridge.** You don't rewrite agents; you adopt **OpenTelemetry instrumentation** (a few lines of code) and keep your existing agent logic unchanged.
- **GenAI semantic conventions** are a *common telemetry schema* across frameworks — consistent span attributes for agent names, model calls, and key events. Microsoft heavily contributes to this standard.
- **The "Microsoft OpenTelemetry distro"** is a unified SDK that auto-instruments most agent frameworks across multiple programming languages. Foundry-native agents have it built in (zero code change); external agents need just a few lines of init code.
- **Unified traces "just work" across clouds** — because every sub-agent emits OpenTelemetry traces, Foundry stitches them into one end-to-end trace even when they run on GCP, AWS, and Foundry simultaneously.
- **Two agent flavors on Foundry:** *no-code* **Prompt Agents** (configure in the portal) and *pro-code* **Hosted Agents** (submit code/container; Foundry manages and runs it). Hosted agents shine for enterprise: VM isolation, Entra agent identity, long-running operations.
- **Orchestrator + specialists pattern.** A Foundry hosted orchestrator (built with Microsoft Agent Framework) routes questions by city to specialist sub-agents on different clouds, with a **Copilot SDK fallback** for cities with no specialist.
- **It's an operational loop, not just viewing traces.** The real value: answer production questions fast — *did routing pick the right sub-agent? did retrieval return weak context causing hallucination? where did latency come from (cold start / network / model)?*
- **Built-in monitoring** shows live traffic patterns, latency distribution, estimated cost, token usage, scheduled evals, scheduled red teams, error rate, and tool-call success — surfacing regressions (error rate up, tool-call success down).
- **Fleet-level "Operate" view** shows all agents in a project with active security alerts (malicious URLs, jailbreak attempts — on by default), evaluation-based alerts, agent success rate, and volume over time.
- **Evaluation closes the loop.** Set up evaluators (e.g., intent resolution, task adherence) on traces via the Foundry project client; failed evals link straight into the trace view to diagnose *why* (e.g., a "concise comparison" that didn't actually compare both cities).
- **Foundry powered by Azure Monitor & Application Insights** — traces stored in Azure Monitor, so existing Azure Monitor users keep their familiar features for non-agentic workloads too.
- **Meet customers where they are:** beyond OpenTelemetry GenAI conventions, Foundry also supports **OpenInference** and **OpenLLMetry** formats for trace viewing and evaluation.

## 📚 Detailed Notes

### The production reality: heterogeneous agent setups
The speaker (a software engineering manager on the Foundry observability team) opened with a show of hands: many in the room build or operate agents in production, but almost **no one** had *all* their agents running on the same cloud provider, same programming language, and same agent framework ("one lucky person"). This sets up the central thesis.

What Microsoft hears from customers repeatedly is that big enterprises have a **heterogeneous agent setup** that emerges organically:
- A **product team** picks **Foundry prompt agents** because they're easy to iterate on in the portal.
- A **backend team** picks **LangGraph on AWS** because that's the framework they know best.
- A **third team** adopts **ADK (Agent Development Kit) from Google** because they're already on GCP / Gemini.
- Then someone asks for **Copilot SDK** as a catch-all because it's the new thing they heard about.

Very quickly this becomes a mess: **different agent frameworks, different hosting stacks, different metrics, different dashboards.** When a bad response surfaces in production, leadership ("VP") starts asking scary questions:
- *Which agent is that?*
- *Why did the agent return this bad answer?*
- *How do we prevent bad behaviors in the future?*

The session's promise: **answer all these in one place — Foundry observability — without rewriting agents into a single framework.** The method is adopting **OpenTelemetry instrumentation with a few lines of code, no change to existing agent logic.** Everything demoed is live and reproducible from a repo shared at the end.

### Demo 1 — A simple Foundry Prompt Agent (the Xi'an travel expert)
The speaker grew up in **Xi'an**, a famous tourist destination in China, and often gets asked for travel recommendations — so they built a **travel expert agent** using Foundry's no-code offering, **Prompt Agent**, inside the **Microsoft Foundry portal** using the **Playground** view (lets you quickly configure and test agents).

How it was built:
- Picked a **model** for the agent.
- Gave it a **system prompt** (can be multi-language).
- **Secret sauce:** uploaded **travel notes as a PDF** (with pictures, links, etc.) into Foundry as an **index**, so the agent can retrieve from those notes when needed — a **classic RAG (Retrieval-Augmented Generation) pattern**.

Sample query: *"Plan a three-day trip in Xi'an for two people, focus on history and food."* The agent returned a detailed day-by-day itinerary — famous places to visit (in multiple languages) and restaurant recommendations. "We're in 2026, this shouldn't be a surprise" — the interesting part is **how** the agent got there.

### Foundry traces view — understanding agent behavior
Switching to the **Traces** view shows a list of all previous conversations with the agent, with dimensions like **token cost, tokens in, tokens out, estimated cost**, plus sort and filter. Drilling into a specific trace gives a clear behavioral view with key per-conversation metrics:
- **Number of spans**
- **Number of chat calls**
- **Number of tool calls**
- **Latency**
- **Token consumption**

The **tree view** structure:
- Everything is rooted under a single **`invoke agent` span** containing the **system message**, the **customer input**, and the **agent output**.
- Following it is an **`execute tool` span** the agent uses to look up the travel notes.
- The **metadata tab** on the tool span reveals the **query** the agent used to retrieve content from the PDF, and the **final answer/content** the tool returned to the agent.
- Everything is ultimately fed into the **LLM for the final answer.**

This is exactly where you'd start debugging **hallucination or groundedness problems** — inspect what the retrieval tool actually returned vs. what the agent claimed.

Extra UX features:
- **Replay button** with adjustable speed — watch how the agent actually executed, step by step.
- **User view** — experience exactly what an end user would see from the agent.

The takeaway from Demo 1: Foundry gives a very clear view to deeply understand agent behavior and debug issues — but the natural question is, *does this only work for Foundry-native agents? What about agents running elsewhere?*

### Demo 2 — External agents across clouds (the multi-cloud reveal)
To answer that, the speaker brought in colleague **Nikhil Kumar** ("Nikkumar"). Together they built parallel travel agents to prove Foundry observability works for *any* agent, *any* cloud:

- **Bangalore travel agent** (Kumar's hometown) — runs on **GCP using Google's ADK**, registered on Foundry as an **external agent**. After registration, it gets the *same rich trace experience*.
  - Proof it's real: Kumar sent a live request **via curl** to the agent running on **`run.app` (Google Cloud Run / GCP)**. The response came back (with the city in it) after a brief network delay — confirming a real agent on GCP, nothing faked, full HTTP request/response.
- **Seattle travel agent** (both presenters live in Seattle) — built with **LangGraph, running on AWS**. Kumar sent a curl request asking about Seattle.

The orchestration layer:
- A **fourth agent acts as an orchestrator**, built with **Microsoft Agent Framework**, **deployed on Foundry as a hosted agent**.
- It **routes intelligently based on the city** asked about.
- **All agents emit OpenTelemetry traces.**

The big multi-cloud demo: a single user message asked about **Seattle, Bangalore, and Lisbon**. Lisbon had no dedicated agent, so a **Copilot SDK fallback** handled cities without a specialized agent / without data. The orchestrator invoked multiple agents across multiple clouds in one flow.

In the **Traces** tab, an earlier example trace (asking about **Seattle and Berlin**) showed:
- The **`invoke agent` span** at the root.
- A **city router** deciding to route to the **Bangalore and Seattle** agents.
- The **Seattle specialist** invoked to get Seattle details.
- The **Copilot fallback** handling **Berlin** data.

### The bird's-eye view — how unified tracing actually works
Recap architecture (presented as a slide):
1. A **user asks a question** to the **orchestrator**.
2. The orchestrator runs as a **Foundry hosted agent** (pro-code).
3. It **routes the question to the right sub-agent** — the specialist for that specific city.
4. Each **sub-agent runs on a different cloud with a different agent framework** (Foundry / GCP+ADK / AWS+LangGraph).
5. **Because all of them emit OpenTelemetry traces, Foundry observability stitches together the end-to-end execution** into one **unified trace**.

Net effect: even though agents run across multiple clouds, **it feels like one system.**

### Key ingredient #1 — Microsoft's agent platform (Foundry)
Foundry offers two agent styles:
- **No-code: Foundry Prompt Agents** — configured in the portal (the Xi'an demo). Fast to iterate.
- **Pro-code: Foundry Hosted Agents** — you submit your **code or container** to Foundry; Foundry **manages and runs** it, giving you **full control of agent behavior** (the orchestrator was a hosted agent).

**Why hosted agents shine for enterprise:**
- **Enterprise-grade VM isolation**
- **Agent identity from Entra** (Entra ID) — guarantees security
- **Long-running operation routines** and other enterprise-friendly features

Pro-code or no-code is your choice — "Foundry's got you covered." The full lifecycle:
- **Build** your agent (code + prompts) and **check into GitHub**.
- **Run** it in Foundry with built-in **observability, evaluation, and optimization**.
- **Distribute** your agents to users (referenced as **M365 Copilot** — caption garbled as "M3C5").

### Key ingredient #2 — OpenTelemetry GenAI semantic conventions
Think of this as a **common telemetry schema across frameworks** — whether it's a Foundry prompt agent, a LangGraph app, or an ADK service, they all **emit spans with consistent attributes** for:
- **Agent names**
- **Model calls**
- **Key events**

This consistency gives **strong compatibility with downstream observability and evaluation features** on Foundry. **Microsoft heavily contributes to this standard** and actively adds new scenarios to support.

### Key ingredient #3 — The Microsoft OpenTelemetry distro (the code change)
The **Microsoft OpenTelemetry distro** is a **unified SDK that can instrument most agent frameworks across multiple programming languages.**
- **Foundry-native agents** have the distro instrumentation **built in → zero code changes.**
- **External agents** (outside Foundry) use the distro's **auto-instrumentation** — just a **few lines of initialization code.**

Code walkthrough (in **VS Code**) — to instrument an external agent you:
1. **Enable OpenTelemetry** and wire it up with **Azure Monitor**.
2. **Pass the Azure Monitor connection string.**
3. **Tell it which framework** you're using.
4. **Give it the agent ID** — *the same agent ID used to register the agent on Foundry*, so Foundry can **pull up the traces and correlate them.**

That's it — no changes to the agent's business logic.

### Storage & compatibility — Azure Monitor underneath
**Foundry observability is powered by Azure Monitor and Azure Application Insights.** All traces are **stored in Azure Monitor**. Practical benefit: if you're an **existing Azure Monitor user** (e.g., for non-agentic workflows/architecture), you can **keep using familiar Azure Monitor features** alongside agent traces.

### Why it matters in production — the operational loop
Seeing all traces is great, but the **real value is operational**: debug issues, monitor patterns, and evaluate quality **in one workflow**. Traces are only useful if they **answer questions quickly in production**, e.g.:
- Did the **routing agent route to the right sub-agents**?
- Did **retrieval return weak context** that might have caused a hallucination?
- Did **latency come from a cold start, slow network, or the model itself**?
- Over time, is there a **trend that agent behavior is shifting / drifting**?

### Monitor tab
The **Monitor** tab surfaces:
- **Live traffic patterns**
- **Latency distribution**
- A few **evaluation results**
- **Estimated cost** and **total token usage**
- **Types of evaluations** that ran on the agent
- **Scheduled evals** and **scheduled red teams**
- **Operational metrics** further down — including **error rate** (presenter noticed it *went up* and flagged it for follow-up)
- **Scheduled evaluation results** and **human-evaluator** input
- **Tool-call success rate** (noticed it *went down recently* — flagged to investigate)

This is the "monitor patterns / catch regressions" half of the loop.

### Operate tab — fleet-level visibility
The **Operate** tab (the "fleet view") lets you look at **all agents in a particular Foundry project**:
- **Active alerts** — if you have an agent on Foundry, a **security workflow runs by default**, alerting on things like **malicious URLs detected** or a **jailbreak attempt** on your prompt.
- **Custom evaluation alerts** — set alerts on evaluation results, so if an agent **stops working as intended**, you're notified.
- **Fleet metrics** — **agent success rate**, **agent volume**, **most-used agent over time**, etc.

### Evaluation — closing the loop on quality
Set up evaluations **on traces** using the **Foundry project client**, selecting which **evaluator** to add to the **testing criteria** (example used: **intent resolution evaluator**), then run on a specific **agent ID**. After creating an eval you get **eval results**.

Walkthrough of a real failure:
- A trace **didn't work well** → click it → taken **directly into the trace view** of that agent.
- The **user's intent**: compare **Bengaluru and Barcelona** for an after-work evening, keeping the plan **concise**.
- The failing metric was **task adherence** — the user asked for a **concise comparison**, but the response **did not cover both cities**.
- Inspecting the response: "there is no comparison… there is description about both of them." The presenter inferred the **evaluator was looking for a table.**

This demonstrates the diagnostic power: eval failure → jump to trace → see exactly what intent was, what failed, and why.

### The whole loop, summarized
The simple loop the presenters wanted to leave the audience with:
1. **Instrument** your code with OpenTelemetry.
2. **Debug** in production with live traffic.
3. **Evaluate** quality.
4. **Optimize** the agent.
5. Gain **fleet-level visibility** to manage and control agents.
…all on **one observability plane.**

### Bonus Foundry features (mentioned, not deep-dived due to time)
- **Rubric evaluators** — create a customized evaluation plan tailored to your agent, solving the **evaluation cold-start problem**.
- **Agent optimization** — improves your agent by **fine-tuning the system prompt**, **trying different models**, and **leveraging new tools**.
- **A65 / next-gen model opt-in** (caption garbled — likely a future Azure/Foundry model offering): for customers who want to leverage or opt in, **Foundry supports it natively**.
- **Alternative trace formats:** while Microsoft recommends OpenTelemetry GenAI semantic conventions, it **meets customers where they are** by also supporting **OpenInference** and **OpenLLMetry** for **trace viewing and trace evaluation** — for customers not ready to switch trace formats.

### Closing
The presenters pointed to **recordings of other Foundry sessions** and **Foundry's public documentation**, plus a **QR code linking to the demo repo** with all the agents showcased. Closing message: *"Build what you want, run it where you need, and observe it all in one place. **Any agent, any cloud, one observability plane.**"*

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — the AI agent platform / portal at the center of the talk.
- **Microsoft Foundry Observability** — unified tracing, monitoring, and evaluation plane.
- **Foundry Prompt Agents** — no-code agents configured in the portal.
- **Foundry Hosted Agents** — pro-code agents (submit code/container; Foundry runs them); enterprise VM isolation, Entra agent identity, long-running operations.
- **Foundry Playground** — quick configure-and-test view for agents.
- **Foundry Traces view** — per-conversation spans, metrics, tree view, replay, user view.
- **Foundry Monitor tab** — live traffic, latency distribution, cost, token usage, scheduled evals/red teams, error rate, tool-call success.
- **Foundry Operate tab (fleet view)** — all agents in a project, active alerts, fleet metrics.
- **OpenTelemetry** — open standard for telemetry/tracing.
- **OpenTelemetry GenAI semantic conventions** — common telemetry schema for agent names, model calls, key events.
- **Microsoft OpenTelemetry distro** — unified SDK auto-instrumenting most agent frameworks across multiple languages.
- **Microsoft Agent Framework** — used to build the orchestrator agent.
- **Google ADK (Agent Development Kit)** — used for the Bangalore agent on GCP.
- **LangGraph** — used for the Seattle agent on AWS.
- **Copilot SDK** — used as a fallback agent for cities with no specialist.
- **Azure Monitor** & **Azure Application Insights** — power Foundry observability; trace storage.
- **GitHub** — agent code + prompts checked in; build stage of the lifecycle.
- **M365 Copilot** — distribution target for agents (caption garbled as "M3C5").
- **GCP / Google Cloud Run (`run.app`)** — hosting for the ADK Bangalore agent.
- **AWS** — hosting for the LangGraph Seattle agent.
- **Entra ID (Entra)** — provides agent identity for hosted agents.
- **VS Code** — IDE used for the instrumentation code walkthrough.
- **Rubric evaluators** — customized evaluation plans (cold-start solution).
- **Agent optimization** — prompt fine-tuning, model swapping, new tools.
- **OpenInference** & **OpenLLMetry** — alternative trace formats supported for viewing/evaluation.
- **Evaluators** — intent resolution, task adherence (and others) for trace-based evaluation.
- **Scheduled red teams** — automated red-teaming runs surfaced in Monitor.
- **RAG (Retrieval-Augmented Generation)** — pattern used by the Xi'an agent with a PDF index.

## 🚀 Announcements / What's New
No major standalone product launches were announced in the keynote sense. The session was a capability **demo of currently live, reproducible features** (the presenters stressed "everything we show in this demo is live and available on Foundry"). Notable "this exists / is supported now" points worth tracking:
- **Cross-cloud unified tracing** via OpenTelemetry GenAI conventions is live in Foundry observability — stitching agents on GCP, AWS, and Foundry into one trace.
- **Microsoft OpenTelemetry distro** auto-instrumentation for external/non-Foundry agents (few lines of init code) is available across multiple languages and frameworks.
- **Support for OpenInference and OpenLLMetry** trace formats (in addition to OpenTelemetry GenAI conventions) for trace viewing and evaluation — meeting customers where they are.
- **Rubric evaluators** and **agent optimization** capabilities were called out as available Foundry features (covered briefly due to time).
- **A65 native support** (caption garbled — appears to be a forthcoming Azure/Foundry model that customers can opt into) is supported natively in Foundry.

> Note: This was a demo/enablement session (DEM track), so it focused on showing existing, reproducible capabilities rather than net-new launches. If you need a crisp "announcement" line: **None explicitly announced as a launch** — the emphasis was that all shown features are already live on Foundry.

## 💡 Demos
The session was essentially one continuous, escalating live demo built around **travel agents**, each tied to a presenter's hometown/city:

1. **Demo 1 — Foundry Prompt Agent (Xi'an travel expert).** No-code agent built in the Foundry Playground: pick a model, give a system prompt, upload a **travel-notes PDF as an index** (RAG). Queried *"Plan a three-day trip in Xi'an for two people, focus on history and food"* → returned a multi-language, day-by-day itinerary with places and restaurants. Then the **Traces** view was used to inspect spans (`invoke agent` → `execute tool` for PDF lookup → LLM), the metadata tab (retrieval query + returned content), the **replay** (step-through with speed control), and the **user view**.

2. **Demo 2 — Bangalore agent on GCP (Google ADK), registered as an external agent.** Kumar sent a **live curl request** to the agent on **`run.app` (GCP)**; after a network delay the response came back with the city — proving a real, unmodified cross-cloud agent surfaces the same rich trace experience in Foundry.

3. **Demo 3 — Seattle agent on AWS (LangGraph).** Kumar sent a **curl** with a Seattle question; the agent emitted OpenTelemetry traces like the others.

4. **Demo 4 — Multi-cloud orchestration (the headline demo).** A **Foundry hosted orchestrator** (Microsoft Agent Framework) was asked about **Seattle, Bangalore, and Lisbon** in one message. The **city router** routed to the right specialists; **Lisbon (and earlier, Berlin)** had no specialist, so the **Copilot SDK fallback** handled it. An earlier trace (Seattle + Berlin) was shown end-to-end: root `invoke agent` span → city router → Seattle specialist → Copilot fallback for Berlin — **all stitched into one unified trace despite spanning GCP, AWS, and Foundry.**

5. **Demo 5 — Instrumentation code (VS Code).** Showed the few lines needed to instrument an external agent: enable OpenTelemetry, wire to **Azure Monitor** with a **connection string**, specify the **framework**, and pass the **agent ID** (matching the Foundry registration) for trace correlation.

6. **Demo 6 — Monitor tab.** Live traffic patterns, latency distribution, estimated cost, token usage, scheduled evals, scheduled red teams; spotted **error rate up** and **tool-call success down** as live regressions to investigate.

7. **Demo 7 — Operate tab (fleet view).** All agents in a project, **active security alerts** (malicious URLs, jailbreak attempts — on by default), evaluation-based alerts, agent success rate, and most-used agent over time.

8. **Demo 8 — Evaluation.** Set up an **intent resolution evaluator** via the Foundry project client; a failing trace (compare **Bengaluru vs Barcelona**, concise) was opened directly from eval results — **task adherence failed** because the response described both cities but didn't actually compare them (evaluator likely expected a table).

## 📊 Notable Stats / Quotes
- **Show of hands:** roughly "one lucky person" in the room had *all* their agents on the same cloud + language + framework — vivid evidence that **heterogeneity is the norm**.
- **Per-conversation trace metrics** highlighted as "the key metrics": number of spans, number of chat calls, number of tool calls, latency, token consumption.
- **Trace list dimensions:** token cost, tokens in, tokens out, estimated cost (sortable/filterable).
- **"Adopt OpenTelemetry instrumentation with a few lines of code… without changing your existing agent logic."** — the central method.
- **"It's just a few lines of initialization code to set up the SDK."** (for external agents).
- **"Foundry observability is powered by Azure Monitor and Azure Application Insights… all of [the] traces are stored in Azure Monitor."**
- **"Because all of them are emitting OpenTelemetry traces, Foundry observability was able to stitch together the end-to-end execution… even though they are running across multiple clouds it feels like everything is in one system."**
- **Closing line:** *"Build what you want, run it where you need, and observe it all in one place. **Any agent, any cloud, one observability plane.**"*
- **Live regressions caught on stage:** error rate went up; a tool-call success rate went down — used to show the monitoring is real and actionable.

## 🧠 My Notes / Follow-ups
- [ ] **Things to try:**
  - Clone the **demo repo** (QR code at end of session) and reproduce the multi-cloud orchestrator + specialists locally.
  - Instrument a **non-Foundry agent** (e.g., a LangGraph or ADK service) with the **Microsoft OpenTelemetry distro** + Azure Monitor connection string + matching agent ID; confirm traces correlate in Foundry.
  - Stand up the **Foundry hosted orchestrator** pattern (Microsoft Agent Framework) with a **Copilot SDK fallback** for out-of-scope inputs.
  - Configure **scheduled evals** (intent resolution, task adherence) and **scheduled red teams**; wire **evaluation-based alerts** in the Operate tab.
  - Try **rubric evaluators** to bootstrap evaluation criteria from scratch (cold-start solution).
- [ ] **Questions:**
  - What exactly is **"A65"**? (Caption garble — likely a forthcoming Azure/Foundry model offering. Confirm name/availability.)
  - What are the **cost implications** of storing all agent traces in Azure Monitor at production scale (ingestion + retention)?
  - How granular is the **OpenTelemetry GenAI semantic convention** coverage today vs. proprietary spans for newer frameworks?
  - For **OpenInference / OpenLLMetry** formats — is evaluation feature-parity with native OpenTelemetry, or viewing-only for some features?
  - How does **agent identity from Entra** flow through to cross-cloud sub-agents (e.g., the AWS/GCP-hosted ones)?
- [ ] **Relevant to:**
  - Any org running a **heterogeneous / multi-cloud agent estate** wanting a single observability pane.
  - Teams already invested in **Azure Monitor / App Insights** who want agent traces in the same place.
  - Platform/SRE teams needing **fleet-level alerting** (security, jailbreak, eval-regression) across agents.
  - LLMOps/eval workstreams adopting **OpenTelemetry GenAI conventions** as a standard.

## 🔗 Related
- [[Microsoft Foundry]]
- [[OpenTelemetry]]
- [[Microsoft Agent Framework]]
- [[Azure Monitor]] / [[Application Insights]]
- [[Agent Observability]]
- [[LLM Evaluation]]
- Other Microsoft Build 2026 sessions — Foundry / observability / agents track

---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai-foundry
  - topic/open-source
  - topic/agents
  - topic/frameworks
source: https://www.youtube.com/watch?v=AmqjXd7v_x4
session_code: DEM333
event: Microsoft Build 2026
speakers: Facundo (Principal PM, Microsoft), Nakumar (Senior Software Engineer, Microsoft)
duration_min: 16
aliases:
  - How Foundry integrates with open-source frameworks and tools
---

# DEM333 — How Foundry integrates with open-source frameworks and tools

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Facundo (Principal Product Manager, Microsoft) & Nakumar (Senior Software Engineer, Microsoft — driving the demo)  
> **Duration:** ~16 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=AmqjXd7v_x4)

## 🎯 TL;DR
A live, build-it-from-scratch demo answering one practical question: **if you build an agent with open-source frameworks, how do you take it to production without rewriting it?** The presenters incrementally build a "OpenClaw-style" general-purpose agent using LangChain/LangGraph for the agent loop, then progressively layer on capabilities through **open standards** — MCP (Model Context Protocol) for tools, lightweight markdown **skills** for repeatable behavior, a Playwright CLI for browsing, and OpenTelemetry GenAI semantic conventions for observability. Finally they host the *same* LangGraph agent on **Microsoft Foundry**, which exposes it via an **OpenAI-compatible Responses API** and an **A2A (agent-to-agent) endpoint**, then have **Copilot CLI** discover and invoke it. The thesis: every component is composable, swappable, and connected through open interfaces — nothing is locked in, and "none of these components knew about each other."

## 🔑 Key Takeaways
- **The minimum viable agent = a model + an agent loop.** The loop asks the model for the next step, runs tools when needed, and uses each result to decide what happens next. That's the irreducible core — no platform required.
- **Foundry models expose OpenAI-compatible APIs**, so LangChain talks to a Foundry model with the same protocol it already understands. **Changing the model target is configuration, not a rewrite.**
- **Separation of concerns:** LangChain owns the agent loop (via `create_deep_agent`); Foundry provides the models (via the OpenAI-compatible protocol).
- **MCP (Model Context Protocol)** is the open pattern for giving agents tools. The agent connects to an MCP server, asks for tools, and receives tool schemas at runtime — it never needs to know every underlying HTTP endpoint.
- **Work IQ Mail MCP server** gives the agent Microsoft 365 capabilities (mail, calendar, Teams) through a clean tool interface (`search messages`, `get message details`, `draft replies`, etc.).
- **Tools are verbs; skills are playbooks.** A skill (e.g. "triage inbox") is just a **markdown document with a small formatting block** — no proprietary schema or special service.
- **Skills are mounted into a virtual skills path**; the agent lists and reads them only when the prompt is relevant — keeping the system prompt lean.
- **Skills make agent behavior repeatable** without turning every instruction into a massive system prompt — same model, same tools, completely different behavior.
- **Playwright CLI** brings web browsing to the agent. They chose a **CLI tool over an MCP server** because browser work creates a large tool surface; a command line is a simpler, more **token-efficient** utility (snapshots/details only enter the context window on demand).
- **Foundry hosts the same LangGraph agent as a hosted agent** and exposes it through an **OpenAI-compatible Responses API** via a thin adapter layer — the *same code* runs locally and in the cloud.
- **Order matters in the adapter:** initialize the Foundry server host *before* building the graph, so OpenTelemetry LangChain instrumentation can attach before graph construction.
- **Observability is open:** Foundry integrates with **Application Insights + OpenTelemetry** using the **Microsoft OpenTelemetry distro** and **GenAI semantic conventions** — you can inspect LangGraph spans, model calls, latencies, captured I/O, do trace replay, and review historical traces.
- **Because telemetry data is open**, you're not locked into Foundry's trace viewer — you could use Grafana or any other debugging tool. Traces also expose **per-section token spend**, so you see exactly where budget goes in production.
- **A2A (agent-to-agent):** hosting in Foundry yields an **A2A endpoint** where any A2A-compatible client can discover the **agent card** and send messages — enabling agents-calling-agents composition.
- **Copilot CLI consumed the hosted agent** by exposing a tiny **A2A directory as an MCP server** with two tools (`search agent`, `call agent`), discovering the right agent and invoking it over A2A.
- **The central thesis:** compose modules via open standards (LangGraph, MCP, skills, Playwright CLI, OpenTelemetry, Responses API, A2A); each piece works in isolation and stays freely swappable — no component knew about the others.

## 📚 Detailed Notes

### The framing question
The session opens with a deliberately simple premise: developers love building agents with open-source technology, but the hard part is **packaging and deploying to production without a rewrite.** To make it concrete, the presenters set out to **build their own "OpenClaw" live** — a general-purpose agent (the kind that browses the web, searches email, and gets things done) — using only open-source frameworks and tools, then deploy it to **Microsoft Foundry** for production. The whole talk is a progressive enhancement story: start with the smallest possible agent, then add one open-source capability at a time.

### Step 1 — The minimal agent: model + agent loop
Asked what the *minimum* code is to build an agent with "no magic platform, no Foundry," Nakumar reduces it to two essentials:
- **A model**
- **An agent loop** — the thing that "keeps the agent moving." It asks the model for the next step, runs tools when needed, and uses each result to decide what happens next.

In the demo, the file is intentionally tiny:
- The **model** comes from LangChain's `init_chat_model`.
- The **loop** is built with `create_deep_agent`.

This is plain **LangChain / LangGraph-style code**. The crucial enabler: **most Foundry models expose OpenAI-compatible APIs**, so LangChain can talk to a Foundry model using the same protocol it already understands. Swapping the model target is **configuration, not a rewrite**. Facundo summarizes the architecture cleanly: **LangChain owns the agent loop** (via `create_deep_agent`) and **Foundry provides the models** (via the OpenAI-compatible protocol). They run the small local agent, say "hello," and it replies — proving the core works.

### Step 2 — Giving the agent hands: MCP (Model Context Protocol)
A bare model "cannot do anything outside of what the model already knows." To let the agent *get things done*, they introduce **MCP — Model Context Protocol**, an **open protocol that lets an agent discover tools and call them**.

For this demo the MCP server is **Work IQ Mail**, which gives the agent access to **Microsoft 365 mail capabilities** through a tool interface. The key benefit: the agent **does not need to know every HTTP endpoint** Microsoft 365 exposes. Instead it:
1. Connects to the Work IQ MCP server,
2. Asks for tools,
3. Receives **tool schemas** like `search messages`, `get message details`, `draft replies`, etc.

In the code, the MCP server **URL is passed in**, and the tools are simply **added to the same agent loop** as additional tools — no change to the loop itself. Facundo confirms the generalization: you can point *any* existing LangGraph agent at this MCP server (over the open protocol) and instantly gain Work IQ mail, calendar, Teams, and other capabilities.

**Demo run:** With MCP enabled, Nakumar asks the agent to "check my email." Watching the **tool boundary**, the agent **discovers the mail tools at runtime** and chooses the right one. It comes back having found **five emails** via the Work IQ MCP server. The point stressed: the tool boundary is **inspectable**, and the agent is "just normal Python code."

### Step 3 — Teaching the agent *how* to use tools: Skills
Having "hands" isn't enough — knowing *which* emails are unread "is not that special." The real goal is to **triage the inbox**, which requires the agent to understand *how* to use each tool together. The open-source pattern for this is **skills**.

The mental model:
- **Tools are like verbs** (e.g. `search messages`).
- **A skill is a playbook** — e.g. "triaging inbox" — which can pull fields, **classify emails into categories**, **assign priority**, and **draft replies** when asked.

Critically, a **skill is just a markdown document with a small formatting block**. There is **no special service and no proprietary schema**. The agent **reads the skill when the prompt is relevant**. Mechanically, skills are **mounted into a virtual skills path**; the agent can **list them and read them** only when it needs guidance — so they don't bloat the system prompt.

**Demo run:** Nakumar asks the skills-enabled agent to "triage my inbox." Observations:
- The agent **picks up the triage skill**.
- Unlike the earlier single-tool email check, **multiple tools are now called** — including `get message` to fetch the **actual content** of emails (you can't triage without reading what's inside).
- It returns a **triage summary** with, for each item: the **category**, the **recommended action**, and the **reasons** for that action.

Same model, same tools — but **completely different behavior**, all from a reusable skill. Nakumar's "big point": **skills are a lightweight way to make agent behavior repeatable without turning every instruction into a massive system prompt.**

### Step 4 — Browsing the web: Playwright CLI (and why not MCP)
Another hallmark of OpenClaw-style agents is **web browsing**. The open-source story here is **Playwright** — an open-source framework that exposes a **CLI utility**. They again pair it with a **skill** that teaches the agent how to drive the Playwright CLI.

In `agent.py`, the Playwright tool is added to the `get_tools` method and passed in with the rest. The Python tool signature is minimal: **one arg string and an optional browser session.**

**Demo run:** The agent is asked to "open Amazon and tell me the price of the first Microsoft-branded coffee cup." It picks up a **different skill** (web browser) and uses the **Playwright CLI tool** (alongside the MCP server). It reports it couldn't find a Microsoft-branded cup, but the first non-Microsoft mug it found was **$16.19**.

**Why CLI instead of MCP?** This is a deliberate design contrast:
- Browser work usually creates a **large tool surface** (many endpoints/operations).
- A command line is a **simpler utility**.
- **Token efficiency:** with the CLI, **snapshots and command details only enter the context window when the agent asks for them.** With an MCP server you'd retrieve big JSON tool/instruction blobs, feed them back to the model on every turn, and burn tokens. Facundo underscores: the CLI is both **easier for the model to use** and **more token-efficient.**

### Step 5 — Taking it to production with Foundry (Responses API)
Everything so far runs in a terminal — but production users "don't want to be SSHing into your laptop." Foundry's answer: it **hosts the same LangGraph agent as a hosted agent** and exposes it through an **OpenAI-compatible Responses API.**

The mechanism is an **adapter layer** file that:
- Calls the **same `build_agent`** used earlier (no agent rewrite).
- Uses the **responses host server** to expose the LangGraph agent as a **Responses-compatible endpoint.**
- **Initializes the Foundry server host *before* building the graph**, so the **OpenTelemetry LangChain instrumentation can attach before the graph is constructed.** (Ordering is important.)

Facundo's read: the agent is **wrapped in the Responses API protocol**, so the **same code runs locally on your machine *and* in the cloud.** For the demo, the agent was pre-deployed, and Nakumar sends the "triage my inbox" prompt to the hosted version.

### Step 6 — Observability: Application Insights + OpenTelemetry
When you move to production you need to know *exactly* what the agent did. Foundry **integrates with Application Insights and OpenTelemetry.** The demo uses:
- The **Microsoft OpenTelemetry distro**, and
- **OpenTelemetry GenAI semantic conventions.**

This lets you inspect **LangGraph spans, model calls, latencies, and captured input/output.** In the **Traces tab** you can see all requests sent to the agent and how long each took. Specific capabilities shown:
- The **invoke agent span** and the **chat span** from a Foundry trace.
- **Trace replay.**
- A **historical trace** showing user input, user output, and **all tool actions** — including the agent **executing a tool to read the skill** it was told to use for triage.

Two strategic points:
1. **Open data → tool freedom.** Because OpenTelemetry with semantic conventions is a **widely industry-adopted open standard**, you can use Foundry *or* **Grafana or any other debugging tool** — the data is open, so you focus only on its content.
2. **Cost visibility.** Production is "when you get surprised about where the time and budget go." Traces expose the **token count per section**, so you can see **exactly where your money is going** and which parts need optimization.

### Step 7 — Composition: A2A (agent-to-agent) + Copilot CLI
The 2026 theme is **agents calling other agents, composing**. The question: can the deployed agent be **consumed by another agent**? Yes — hosting in Foundry yields an **A2A endpoint** that any **A2A-compatible client** can use to **discover the agent card** and **send messages** to the hosted agent.

**Demo with Copilot CLI:** Nakumar has **Copilot CLI** talk to the agent and asks it to "triage my inbox." Setup details:
- In the Copilot agent, they **expose a tiny A2A directory as an MCP server.**
- They add **two tools**: **`search agent`** and **`call agent`** (A2A tool).
- Copilot uses this to **search the directory** for an agent that can perform the task, then **invoke** it via A2A.

**The full composition chain (the payoff):**
1. **Copilot CLI** (a completely different runtime) searches for an agent via the **MCP server / A2A directory**.
2. It finds the matching agent (`search agent` line in the output).
3. It **invokes the agent over the A2A protocol.**
4. That agent is **hosted in Microsoft Foundry** and, under the hood, is **the very LangGraph agent they just built** — using LangGraph as the agent loop with Foundry models.
5. The Foundry agent calls **Work IQ** (hosted as an MCP server) to access the inbox, retrieve emails/content.
6. It applies the **triage skill** to classify and draft replies, then returns the answer.
7. The result flows back to **Copilot CLI**, which answers the original question.

**The beauty:** "**none of these components knew about each other.**" They were all built in isolation and simply **composed** through open interfaces.

### The closing thesis
The takeaway message: you **compose each module using open-source standards**, then build a bigger solution out of those **open interfaces** — which means you're **free to change any component at any time.** That is the open-source story: LangGraph + MCP + skills + Playwright CLI + OpenTelemetry + Responses API + A2A, all swappable, all composable, none locked in. The presenters point the audience to the **repo**, which contains every stage of the agent as it was built up through the demo.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — production hosting for the agent; provides OpenAI-compatible models, hosts the LangGraph agent, exposes Responses API + A2A endpoints, and integrates observability.
- **LangChain** — `init_chat_model` (model creation) and overall LangChain-style code.
- **LangGraph** — the agent loop / graph framework; `create_deep_agent` builds the loop.
- **OpenAI-compatible APIs / protocol** — how LangChain talks to Foundry models (and how the agent is exposed via the Responses API).
- **MCP (Model Context Protocol)** — open protocol for tool discovery and invocation.
- **Work IQ Mail (MCP server)** — Microsoft 365 mail/calendar/Teams capabilities exposed as tools (`search messages`, `get message details`, `draft replies`).
- **Skills** — markdown-based playbooks with a small formatting block, mounted into a virtual skills path.
- **Playwright** — open-source browser-automation framework exposed via a CLI utility for web browsing.
- **OpenAI-compatible Responses API** — the protocol wrapping the hosted agent (runs locally *and* in cloud).
- **Application Insights** — telemetry backend Foundry integrates with.
- **OpenTelemetry** — open observability standard; **Microsoft OpenTelemetry distro** + **GenAI semantic conventions**.
- **Grafana** — cited as an alternative trace/debug tool you can use because the telemetry data is open.
- **A2A (Agent-to-Agent) protocol** — endpoint + agent card discovery for agents invoking other agents.
- **Copilot CLI** — separate runtime that discovers and invokes the hosted agent via A2A (using `search agent` / `call agent` tools).
- **OpenClaw** — the general-purpose agent used as the conceptual reference ("let's build our own OpenClaw").

## 🚀 Announcements / What's New
None explicitly announced. This was a demo/architecture session showing how existing open-source frameworks and standards integrate with Microsoft Foundry, rather than a feature-launch talk. No GA vs. preview status was called out for any product. The notable capabilities demonstrated as available/working in the demo include Foundry hosting a LangGraph agent behind an **OpenAI-compatible Responses API**, an **A2A endpoint** with agent-card discovery, and OpenTelemetry/Application Insights tracing via the Microsoft OpenTelemetry distro and GenAI semantic conventions — but none were framed as new announcements.

## 💡 Demos
The entire session is a **single progressive live demo** ("driving the keyboard" = Nakumar), built up in stages — and the repo with each stage was shared:
1. **Minimal agent** — model (`init_chat_model`) + loop (`create_deep_agent`) pointed at a Foundry model via OpenAI-compatible API. Says "hello" → agent replies. ✅
2. **MCP-enabled agent** — Work IQ Mail MCP server added as tools. "Check my email" → discovers mail tools at runtime, returns **5 emails**. ✅
3. **Skills agent** — triage skill (markdown) mounted. "Triage my inbox" → multiple tools called (incl. `get message`), returns a triage summary with **category / recommended action / reasons**. ✅
4. **Browser agent** — Playwright CLI tool + web-browser skill. "Open Amazon, price the first Microsoft-branded coffee cup" → no Microsoft cup found; first non-Microsoft mug = **$16.19**. ✅ (showcases CLI vs. MCP token efficiency)
5. **Foundry-hosted agent** — same `build_agent` wrapped in Responses API adapter; pre-deployed; "triage my inbox" sent to the hosted endpoint. ✅
6. **Observability** — Traces tab in Foundry: invoke-agent span, chat span, latencies, trace replay, a historical trace showing tool actions (incl. reading the skill) and **per-section token usage**. ✅
7. **A2A composition** — Copilot CLI (separate runtime) exposes an A2A directory as an MCP server with `search agent` + `call agent`; discovers and invokes the Foundry-hosted LangGraph agent via A2A to triage the inbox. ✅

## 📊 Notable Stats / Quotes
- **5 emails** found via the Work IQ MCP server in the email-check demo.
- **$16.19** — price of the first non-Microsoft-branded coffee mug found on Amazon in the Playwright browsing demo.
- > "Changing the model target is configuration, not a rewrite." — on swapping Foundry models under LangChain.
- > "Tools are like verbs... A skill is a playbook." — the tools-vs-skills mental model.
- > "Skills are a lightweight way to make agent behavior repeatable without turning every instruction into a massive system prompt." — Nakumar.
- > "None of these components knew about each other... We're just composing all of them." — on the A2A/Copilot composition chain.
- > "You are free to change them at any time. So that's the story we want to tell with open source." — the closing thesis.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Build the minimal LangGraph agent with `init_chat_model` + `create_deep_agent` pointed at a Foundry model via the OpenAI-compatible endpoint, then verify "swap model = config change."
  - Stand up (or connect to) the **Work IQ Mail MCP server** and confirm runtime tool discovery (`search messages`, `get message details`, `draft replies`).
  - Author a **markdown skill** (small formatting block) for inbox triage; mount it into a virtual skills path and confirm the agent reads it only when relevant.
  - Wire up the **Playwright CLI** as a single-arg tool and compare context-window/token cost vs. an MCP browser server.
  - Wrap the agent in the **Responses API adapter** and host on Foundry; confirm the *same code* runs locally and cloud-side.
  - Enable the **Microsoft OpenTelemetry distro + GenAI semantic conventions**; inspect spans/latencies and **per-section token spend** in the Traces tab.
  - Export the same OpenTelemetry traces to **Grafana** to prove the "open data, any tool" claim.
  - Expose the Foundry **A2A endpoint** and consume it from **Copilot CLI** via `search agent` / `call agent`.
- [ ] Questions:
  - What exactly is `create_deep_agent` — is this a LangGraph/LangChain "deep agents" construct, and how does its loop differ from a standard ReAct loop?
  - Is the **Foundry hosted-agent + Responses API** path GA or preview? Pricing/limits for hosted agents?
  - How is the **A2A agent directory** populated and secured (auth, access control on agent cards)?
  - What's the exact ordering requirement for OTel instrumentation vs. graph construction, and what breaks if you get it wrong?
  - Is **Work IQ Mail** generally available as an MCP server, and what M365 scopes/permissions does it require?
  - For browser automation at scale, when does the CLI-vs-MCP trade-off flip back toward a server?
- [ ] Relevant to:
  - Any team building agents on **LangChain/LangGraph** that wants a no-rewrite path to production hosting.
  - Architects designing **multi-agent / A2A** systems where agents from different runtimes must discover and call each other.
  - Anyone standardizing on **open observability** (OpenTelemetry GenAI semantic conventions) for agent cost/latency tracking.
  - Building blocks for an internal **OpenClaw-style** assistant composed entirely from open standards (MCP + skills + Playwright + A2A).

## 🔗 Related
- [[DEM310 - Ship code faster with AI-powered NoSQL schema design]] — sibling Build 2026 demo using MCP + Copilot skills against an open ecosystem.
- [[Microsoft Agent Framework]]
- [[Microsoft Foundry]]
- [[Model Context Protocol (MCP)]]
- [[A2A - Agent-to-Agent Protocol]]
- [[OpenTelemetry GenAI Semantic Conventions]]
- [[LangGraph]]
- Source list: [[2026 Build Session List]]

---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/agents
  - topic/production
  - topic/foundry
  - topic/ai
source: https://www.youtube.com/watch?v=_8UKz197JuM
session_code: BRK241
event: Microsoft Build 2026
speakers: Tina Sharkey (CVP, Microsoft Foundry), Jeff Holland (Partner Director, Foundry Agent Platform)
duration_min: 43
aliases:
  - From prototype to production build and run agents at scale
---

# BRK241 — From prototype to production: build and run agents at scale

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Tina Sharkey (Corporate Vice President, Microsoft Foundry) · Jeff Holland (Partner Director, Foundry Agent Platform)  
> **Duration:** ~43 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=_8UKz197JuM)

## 🎯 TL;DR
A live, end-to-end demo of the full agent lifecycle on **Microsoft Foundry**: **build → deploy → operate**, run as one continuous learning-and-improvement loop. Using a real Microsoft scenario (an autonomous **fiber-outage response agent** for the Azure networking operations team), Jeff Holland builds an agent locally in **VS Code with GitHub Copilot** using the now-GA **Microsoft Agent Framework 1.0** (with its new secure **harness**), wires up tools via **Foundry Toolbox**, voice-enables it in seconds, deploys it as a **hosted agent** with per-session sandbox isolation, makes it proactive and long-running with **routines** + **durable task scheduler**, publishes it into **Teams/Microsoft 365 Copilot** as an **autopilot agent** (with its own identity/email), and finally **operates** it — using **trace replay**, auto-generated **eval datasets**, **custom rubrics**, and the **Agent Optimizer** to automatically tune prompts/tools/models for measurable gains (an 11% improvement on a voice-conciseness rubric). The throughline: AI systems are never "done" — they run on production learning loops, and Foundry is the operating system that lets enterprises continuously evolve production agents rather than rebuild from scratch, all with the developer in control of every change.

## 🔑 Key Takeaways
- **The hard part has shifted from "can I build it?" to "can I run it reliably at enterprise scale?"** Coding agents (GitHub Copilot, Copilot CLI, Claude Code) let any developer stand up a powerful agent in minutes; production operation is now the real challenge.
- **Agents are general-purpose systems, not static routers.** Modern agents can spawn sub-agents, get full access to their compute environment, create new skills, generate memory, and accomplish tasks they were never explicitly programmed for.
- **Agents are teammates, not tools.** They take on business outcomes and do whatever is needed — collaborating with both humans *and* other agents — across every business function (compliance, finance, supply chain, support).
- **Winning enterprises run a coordinated *system* of agents**, not one super-agent — long-running operators that continuously learn and improve. This demands an operating system for enterprise AI, which is what Foundry positions itself as.
- **"AI systems are never done" — they run on production learning loops.** Build → define evals → deploy → feed every action and cost signal back into evaluation/optimization → the system compounds the more it runs. You improve the whole system (model + harness + context + memory), not just fine-tune one model.
- **Microsoft Agent Framework 1.0 is production-ready (GA)** with a built-in secure **harness** (execute shell commands; read/write/execute code), integrated skills/memory/middleware, and pluggable harnesses (GitHub Copilot SDK, Claude Agent SDK).
- **Foundry Toolbox is *the* tool feature to remember:** one managed MCP-compatible endpoint for all tools, handling authentication, guardrails (e.g. PII leakage prevention), and **tool search** (returns only relevant tools per task to optimize context-window usage).
- **Voice enablement is nearly free:** flip "Voice mode" to wrap a Microsoft Agent Framework agent with industry-leading voice models over a streaming WebSocket connection — no rewrite.
- **Hosted agents give per-session sandbox isolation**, sub-second cold start, **zero idle-time cost**, framework-agnostic execution, durable state + file-system access — and now support long-running autonomous ("Claude-like") agents.
- **Routines turn agents from reactive to proactive and long-running** — developer-defined events (e.g. an hourly heartbeat) that Foundry queues, executes, and tracks, waking the agent to check logs/anomalies and act.
- **Security is solved by isolated sessions:** every conversation/routine gets its own dedicated, isolated workspace with durable persistent state, preventing cross-tenant context/code-execution leakage between (e.g.) subcontractor A and subcontractor B.
- **Durable Task scheduler** lets you monitor and resume long-running, serverless agent work across idle sessions — including human-in-the-loop approvals — without rehydrating/restarting state every time.
- **Agents can be published to Teams & Microsoft 365 Copilot**, including as **autopilot agents** with their own Azure identity, email address, and Teams presence — able to initiate conversations and follow up on action items, governed end-to-end in **Agent 365**.
- **Operate is the hardest phase and where the real work begins.** Foundry's **trace replay view** gives time- and token-level observability into each request's trajectory (reasoning steps, tool calls, inputs/outputs) and can replay a conversation at speed.
- **Optimization is automated and rubric-driven:** `azd ai agent eval init` can auto-generate an eval dataset from historic traces and a **custom rubric** of weighted, context-aware criteria; `azd ai agent optimize` runs a data-science optimization loop over prompts, tool descriptions, and models to produce ranked candidates compared on quality/cost/latency — developer chooses the winner, with full lineage and rollback.
- **Proof it's real:** 80,000+ customers run on Foundry today (Iberdrola, Twilio, KPMG cited), and the demo's optimizer found a candidate giving 11% better performance on the voice-conciseness rubric.

## 📚 Detailed Notes

### Framing: the new era of AI agents (Tina)
Tina Sharkey opens by grounding the audience in three truths about where AI agents are today:
1. **Building is no longer the hard part.** With coding agents like GitHub Copilot, GitHub Copilot CLI, and Claude Code, any developer can stand up a powerful agent within minutes. The central question has moved from *"can I build it?"* to *"can I run it reliably at enterprise scale?"*
2. **Agent capabilities have exploded.** Agents are no longer static routers shuffling requests between a fixed set of tools. Today's agents can spawn off new agents, have full access to their compute environments, create new skills, generate new memory, and accomplish things they were never originally programmed to do. They are **general-purpose systems**.
3. **Agents are teammates, not tools** (framed as possibly the biggest shift). We're no longer building chatbots — we're building agents that take on significant business outcomes and do whatever is needed to achieve them, by chatting not only with people but also with other agents.

Put in a whole-business context (compliance, finance, supply chain, support), the businesses that win **don't just build one super-powerful agent** — they put AI at the core of every function as a **coordinated system of agents** all carrying out business-critical, long-running, high-value tasks. The team of agents becomes a **team of operators**, continuously learning and improving. That demands not just a build, but an **entire operating system for enterprise AI transformation** — which is the positioning of Foundry.

### The systems advantage & production learning loops
Microsoft's claim is the **most complete system** for enterprises: **Foundry, Azure, GitHub, Microsoft 365, and Microsoft Security** all working as a holistic system rather than siloed tools. The core insight: **AI systems are never done; they run on production learning loops.**

The loop described:
- **Build** your agent in GitHub (e.g. with GitHub CLI).
- **Define the eval** to tell the system what "good" looks like.
- **Deploy** it into Foundry so it runs on production workloads.
- Every single **action** and **cost signal** is fed into the **evaluation and optimization service**, which continuously learns and improves.
- **The system compounds the more it runs.**

Crucially, this is *not* about fine-tuning a single model — it's about improving the **entire system**: tuning models, harness, context, and memory, **with the developer in control of every single change**. The enterprise continually evolves its production agents instead of rebuilding from scratch each time.

### The demo scenario: autonomous fiber-outage response agent
Microsoft runs the world's largest cloud infrastructure, and sometimes a **fiber cable gets cut near a data center**. The Azure networking operations team has built an agentic system that coordinates with both humans and other agents to respond, dispatch, and resolve such incidents fast. The session builds a simplified version: an **autonomous fiber-outage response agent**.

End-to-end flow of the target agent:
- A **sensor detects the fiber outage** and sends a signal that **triggers the agent**.
- The agent **wakes up** and looks up information via **Foundry Toolbox**:
  - **Site reliability + location info** via **Fabric IQ**.
  - **Supplier conversation info** via **Work IQ**.
  - **Specific work orders + supplier-agreement info** from relevant documents via **Document Intelligence** and **Content Understanding**.
- It **dispatches a field rep** to respond to the incident.
- It **files a ticket** to be tracked in **Dynamics 365 (D365)**.
- It **publishes the latest status into Teams** so everyone is aware.

The demo is structured into **three developer phases — build, deploy, operate — all inside a continuous learning/improvement loop.**

---

### PHASE 1 — BUILD (Jeff)

**The build-phase challenges:** how do I choose the right framework? the right model? how do I make sure the agent has access to the right organizational context/knowledge — integrated, secured with the right identity, and ready to run in natural interfaces (chat *and* voice)? The pitch: many of these pieces exist in the ecosystem, but Foundry brings them together as a **single platform** so you don't jump between tools.

**Tooling — use anything, but VS Code + GitHub Copilot is the showcase.** Foundry works with Claude Code, GitHub Copilot CLI, Cursor, Visual Studio, etc. Jeff's preferred combo is **VS Code + GitHub Copilot**, enabled by the **Foundry Tool Kit extension** (now GA). The extension surfaces the whole flow — not just agent creation, but **tracing, evaluations, and model management** — integrated in the editor.

**Creating the agent.** From a blank canvas, options include starting from a **sample** or **"generate with Copilot."** Jeff prompts Copilot to create an agent for the field operations team that, when someone is on site repairing a fiber line, has the right info from **Work IQ / Fabric IQ / Foundry IQ**.

**Baked-in best practices via skills.** A standout feature: the extension automatically integrates **Foundry best-practice skills** ("AI agent expert") into the workload. These skills can be installed standalone into a coding agent, but the extension auto-applies them so generated agents follow Foundry best practices out of the box.

**Framework: Microsoft Agent Framework (Python) + the new harness.** Jeff uses Microsoft's Agent Framework in Python, which is strong at **multi-step / multi-agent workflows**. The key new capability is the **harness** — a **secure environment** that lets the agent **execute shell commands and read/write/execute code**, all managed by the harness. You can plug in the **GitHub Copilot SDK** as an additional harness. The point: agents are no longer limited to predefined configured tools — they can **dynamically investigate, write, and author code** along the way.

**Tools — Foundry Toolbox (the one feature to remember).** Managed right inside VS Code, Toolbox provides:
- A **single place to configure and manage** a set of tools for one agent or a collection of agents.
- **Authentication handling** across tools like **Foundry IQ** (indexed documents — e.g. supplier contracts/agreements), **Web IQ / web search**, **Fabric IQ** (site reliability/uptime data surfaced through Fabric), and **Work IQ** (history + integration with Teams/Outlook via the Microsoft Graph).
- **Guardrails**, e.g. configuring that **PII doesn't leak** from any of these tools.
- **Tool search:** when enabled, talking to Toolbox through its **single MCP-compatible endpoint** returns only the tools relevant to the specific task — optimizing context utilization / context-window usage and keeping the agent focused on immediate needs.
- **Thousands of additional tools** available to add.

**Content Understanding (a notable tool).** Jeff highlights **Content Understanding**: given a PDF that contains tabular data (not natively agent-readable), it uses a **specialized model** to convert documents/contracts/specs into an **agent- and AI-ready format** — extracting tables, markdown, figures, or raw JSON. (He flags a dedicated Content Understanding session the next day.)

**Local debug — F5 the agent.** Echoing Satya's keynote theme of UI and code working together, Jeff **F5-debugs** the agent: it spins up locally, **connects to Toolbox** via a single MCP-compatible endpoint line, and runs on localhost. He sets a **breakpoint**, asks the agent an on-site connection-type question, the breakpoint hits, and he can inspect request/response and watch **events streaming in and out** — all without leaving VS Code. This demonstrates the build flow: pull the right tools from the right context (web/Foundry/Fabric/Microsoft Graph via Work IQ), connect them with a framework whose harness can look up the needed specification.

**Voice-enabling the agent.** For a field contractor wearing leather work gloves, a chat interface is a poor experience — so Jeff voice-enables the agent. He **deploys the agent into Foundry** (taking the code he wrote and pushing it to his Foundry account), switches to a pre-deployed version, and toggles **"Voice mode."** Foundry **automatically wraps industry-leading voice models** (configurable — choose the right voice model) onto what was built as a Microsoft Agent Framework agent. Over a **streaming WebSocket** voice connection, he asks it to pull the **fiber termination spec for the Quincy North Site** and which connector to use on the **B-side panel**; the agent streams progress updates ("Pulling that up now," "Getting the spec now") while iterating through Toolbox, then answers: **Connector family — LC/UPC duplex required on the B-side panel.**

---

### PHASE 1 RECAP — features shown (Tina)
- **Microsoft Agent Framework 1.0 — production ready (GA).** Built-in harness integrated with skills, memory, and middleware; plugin integrations with harnesses like the **GitHub Copilot SDK** and **Claude Agent SDK**.
- **Foundry Toolkit for VS Code — GA.** Purpose-built developer experience for building Foundry agents without leaving the editor.
- **Toolboxes in Foundry — GA soon.** One single managed endpoint for all the tools powering agents, with the right governance and policy. **Skills are now a first-class integration** with Toolboxes.
- **Voice Live integration with Foundry Agent Service** — **GA today** for prompt agents; **public preview** for hosted agents (speech/voice scenarios).
- **Hosted agents in Foundry Agent Service — GA soon.** Per-session sandbox isolation, sub-second cold start, zero idle-time cost, framework-agnostic; now supports long-running autonomous agents with durable state execution and file-system access.

---

### PHASE 2 — DEPLOY (Jeff)

**The deploy-phase challenges.** The transformative agents aren't reactive Q&A bots — they're **long-running**, maintaining and building context over time, accomplishing tasks that take **days or weeks**, securely. Because harness agents read/write code, **instances must be isolated** from each other. They must reach users through the **interfaces users care about** (don't make everyone bookmark 10 agents), and each agent increasingly behaves like a **proactive teammate** offering suggestions.

**Meet "Fiby" — a Claude-like agent.** Jeff introduces a different flavor of the agent called **Fiby** (the fiber agent), a **Claude-like agent** that **monitors telemetry and uptime** for the networking infrastructure over time.

**Routines — reactive → proactive.** A new Foundry feature, **routines** let you define events that proactively wake the agent. Jeff configures a simple **hourly heartbeat**: every hour, wake up, **check the investigation log**, look for **anomalies**, and if found, **follow the agent's skills** to alert the right person and issue the right subcontractor. (The real Azure networking team does this: on a networking incident, an agent can act automatically, wait for human approval as needed, and get someone on site.) The heartbeat is what makes the agent proactive — it checks for anomalies on its own, and the demo shows it has been firing routines over time.

**Security via isolated sessions.** People often dedicate a whole Windows box or Mac Mini to a Claude-like agent so its workspace stays secure. The risk: if **subcontractor A** and **subcontractor B** both interact with Fiby, and Fiby reads/writes files with subcontractor A's sensitive data saved locally, **subcontractor B's session could pull those files** — leaking context and code execution. Foundry's **hosted agent capability (GA soon)** solves this: **every conversation/routine can kick off its own dedicated, isolated workspace**, so everything one session does is separate from every other — yet with **durable persistent state**. Jeff opens a session idle since 11 a.m., views its **logs** and **inspects the file-system state** at idle: saved files for anomaly analysis, vendor contacts, investigation — "breadcrumbs" the agent writes just like a local Claude-like agent, **but securely in the cloud**.

**Zero idle cost + resume.** While idle (e.g. waiting for approval, or no event found), **you pay nothing**. When it needs to wake, Foundry **resumes the session**, restoring all state (investigation files) so the agent continues its work.

**Durable Task scheduler — monitor & resume across idle sessions.** Jeff extends the out-of-the-box sessions with the **durable task scheduler** (integrated via the **Microsoft Agent Framework extension for durable task**) to monitor state even when all sessions are idle. Example: Fiby woke, found something, and has been **waiting 2–3 hours for human approval**; all sessions are idle and serverless, but durable task tracks the pending-approval instance. Jeff clicks **Approve** → durable task records the approval and tells Foundry to **resume the session** → the Foundry session view shows the session **woke back up**, restored all prior investigation files, and **continued the work** — long-running, secure, with **human intervention but no manual rehydration/restart** of state.

**Publish to Teams & Microsoft 365 Copilot.** Any built agent can be made available to the whole team — not only via routines or custom apps (like the Fiby portal) but **published to Teams and Microsoft 365 Copilot**, with a guided deployment flow. The demo's agent is already deployed and **working as an autonomous agent in Teams** with **its own identity and even its own email address** (shown as `fiby@notareal.co`). Jeff asks it in Teams about **active incidents**; the same agent that ran inside Foundry **resumes or starts a session** and returns a status update — demonstrating Claude-like agents integrated into Teams with all the critical building blocks within Foundry.

---

### PHASE 2 RECAP — features shown (Tina)
- **Routines (Foundry Agent Service) — public preview.** Turn an agent from reactive to proactive and long-running. Developer decides what needs to happen and when; Foundry **queues, executes, and tracks** every run. Converts one-off reactive tasks into proactive, continuous agents.
- **Publish to Microsoft 365 Teams & Copilot — GA soon.** Publish Foundry agents into Teams/Copilot where teams already work; **identity, policy, and permissions flow through automatically**.
- **Autopilot agents in Teams — public preview.** Publish Foundry agents as **autopilot agents** that take on **Azure (Entra) IDs, email addresses, and Teams presence**; they can **initiate conversations** and **follow up on action items**, all governed end-to-end in **Agent 365**.

Progress so far: built locally → hosted in a sandbox → published as an autopilot agent in Teams. Next: the hard part — **operate**.

---

### PHASE 3 — OPERATE (Jeff)

Billed as "the last and maybe the best chapter." **This is where the real work begins:** building/prototyping cool agents takes hours/days, but making the agent **trusted in production** is the challenge — understanding how people use it, what signals occur, what succeeds/fails, and where to improve.

**The tuning dilemma.** When an agent misbehaves, *which variable do you tune?* The components include the **underlying model**, the **toolbox/tools**, **your own code**, and the **instructions in your code**. It's overwhelming and time-consuming — and this last mile is what Foundry aims to make robust.

**Visibility — Trace Replay view.** In the Fiby agent, Jeff sees all conversations across the agent and opens a request in the **new trace replay view**:
- See the **question asked** and **answer given**, plus the **full trajectory** the request took.
- Example trajectory: reasoning on the model (~20s) → call a tool → reason → call another tool. Click into any step for **exact inputs/outputs**.
- View it from a **time perspective** *and* a **token perspective** — where tokens are consumed throughout the request.
- **Replay** the whole conversation at speed (he runs it at **8× speed**) to watch each phase, what the agent was doing, and what the user saw throughout — observability at your fingertips.

**A real improvement target — voice conciseness.** Real feedback from building the demo: the voice-enabled agent answered the fiber-spec question in a **very "LLM" way — a bullet-point list**, which sounds robotic when read aloud by a voice. Jeff wants to optimize the agent to return a **more voice-natural response** — but *which variable* to tune?

**Eval init — `azd ai agent eval init`.** Jeff drops to the terminal and runs the **Azure Developer CLI (azd)** command `ai agent eval init` on the field-operations agent. It initializes the project for evaluations and benchmarks. Two problems it solves:
- **No eval dataset?** Many people talk about evals but don't have a dataset. Foundry can **auto-generate** one: it looks through **historic traces** and additional signals about your agent and uses an **LLM** to suggest an initial starting-point dataset based on how the agent is actually being interacted with.
- **The right evaluation logic/evaluator.** Out of the box Foundry has **built-in evaluators** — tool selection, tool output, tool input, retrieval evaluation, fluency evaluator, and more. Because picking the right combination is overwhelming, the tool can **generate the right combination of evaluators** (and even a custom rubric) for your specific agent.

**Custom rubric — context-aware, weighted, editable.** The generated **custom rubric** isn't a single dimension — an LLM suggested **multiple weighted dimensions** likely important for this agent, e.g.:
- **Correct tool use** (highest weight) — e.g. uptime questions should use **Fabric IQ**.
- **Safety warning** — a big, custom-to-this-agent concern.
- **Voice-optimized conciseness** — initially weighted **3**.

Acting on the real feedback, Jeff **bumps voice-optimized conciseness from 3 to 10** so the evaluator weights voice-friendliness much more heavily. The rubric is fully editable/customizable, yielding a **personalized evaluator** for the scenario.

**Optimize — `azd ai agent optimize` (favorite command).** With the dataset (questions + answers, pre-generated) and the custom evaluator, Jeff runs `azd ai agent optimize`. It detects the agent is already initialized for evaluations and considers, as **variables to tune**:
- the **system prompts / instructions** (both in-code instructions and configured behavior),
- any **skills** configured for the agent,
- the **tool configuration**,
- the **target model** (e.g. GPT-5.5 vs. Anthropic Opus 4.8 — model can be a variable too).

He picks a model to **drive the optimization process** (leaves it at **GPT-5**). This kicks off an **automatic optimization loop** (takes a couple dozen minutes) that adjusts the variables — "what if I modify your system prompts? your tool descriptions? use a different model?" — using **leading data-science techniques** to find better candidate versions of the agent against the custom rubric.

**Results — ranked candidates with measurable gains.** Jumping to a finished run, the optimizer reports it found a candidate that **boosts the evaluator by 11%** (11% better performance just from letting it run). It identified **four candidates**, each with different pros/cons. You can see exactly **what changed** (old system prompt vs. a new, better-behaving system prompt), **dive into score details** and the eval sets tested against, then **deploy the chosen candidate as the new default version** — getting the voice-conciseness improvement. The whole loop is **AI-powered/automated**, and that power is being put into developers' hands.

---

### PHASE 3 RECAP — features shown (Tina)
- **Tracing & evaluation for hosted agents.** Every invocation, tool call, sub-second hop, and handoff is logged in **one OpenTelemetry pipeline**.
- **Rubric for custom evaluation — public preview.** Auto-generates **context-aware criteria and weighted scoring** to define what "good" looks like for both evaluation and optimization, so developers don't start from scratch.
- **Agent Optimizer for Foundry Agent Service — private preview.** Turns **production traces and evals** into a set of **ranked candidates** by tweaking **skills, prompts, tool configuration, and even models**. Candidates are shown **side by side across quality, cost, and latency**; the **developer stays in control** to choose the winning variant to promote, with **full trace-back/lineage** and **rollback** available. ("The platform finds optimization; developers in control on every change.")
- **Procedural memory in Foundry Agent Service — public preview.** Lets the agent **learn the playbook across all sessions**, so it doesn't relearn from scratch each conversation — no manual rewrite of prompts or skills. The agent becomes **smarter, safer, and cheaper** the more it runs, with developer control over every change.

### Closing — proof, customers, and the through-line (Tina)
This is "not just a roadmap promise." **Over 80,000 customers** run on Foundry today, already using production agents to drive significant business outcomes:
- **Iberdrola** — scaling mission-critical energy operations across **14 countries**, leveraging identity, memory, governance, and observability from Foundry Agent Service with full control over **regulated operations**.
- **Twilio** — deployed **Twilio Agent Connect**, their open-source framework connecting AI agents with the Twilio platform, running on **hosted agents in Foundry**.
- **KPMG** — building their global **KPMG Workbench** platform on hosted agents, using tools and skills in **Foundry Toolbox** to supercharge client interactions worldwide.

**The 43-minute journey recapped:** started from a real scenario (fiber cut near a data center) → **built** an agent locally with **Microsoft Agent Framework** as orchestrator → connected **Foundry Toolbox, Foundry IQ, memory, voice, Document Intelligence, and Content Understanding** → ran it as a **hosted agent** in an isolated secure runtime → **published** it into **Teams as a Copilot agent** → **operated** it so it works autonomously, is traced end-to-end, governed in production, and **meaningfully improves through every run**. The promise: **"Build simply, deploy powerfully, operate with trust"** — seamless hosting, connected intelligence, enterprise trust and reach, all in one runtime, available to every developer.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — the end-to-end platform / "operating system" for building, deploying, and operating enterprise AI agents.
- **Foundry Agent Service** — the service hosting/running agents, with routines, hosted agents, tracing/eval, memory, and optimization.
- **Microsoft Agent Framework 1.0** — production-ready (GA) orchestration framework (used in Python here) with a built-in secure harness, skills, memory, middleware; strong at multi-step/multi-agent workflows.
- **Agent harness** — secure managed environment letting an agent execute shell commands and read/write/execute code dynamically.
- **Foundry Toolkit for VS Code** — GA editor extension for building Foundry agents (agent creation, tracing, evaluations, models) without leaving VS Code; auto-applies Foundry best-practice skills.
- **Foundry Toolbox** — single managed, MCP-compatible endpoint for all tools; handles auth, guardrails (e.g. PII), and **tool search** (returns only relevant tools per task).
- **Tool search** — Toolbox feature returning only task-relevant tools to optimize context-window usage.
- **Skills** — reusable best-practice capabilities; now a first-class integration with Toolboxes and installable into coding agents.
- **Foundry IQ** — indexed document knowledge (e.g. supplier contracts/agreements) surfaced as a tool.
- **Fabric IQ** — site reliability/uptime and location data surfaced through Microsoft Fabric.
- **Work IQ** — history + Microsoft Graph integration (Teams/Outlook) surfaced as a tool.
- **Web IQ / web search** — web knowledge as a tool.
- **Content Understanding** — specialized model converting PDFs/contracts/specs (incl. tabular data) into agent/AI-ready formats (tables, markdown, figures, raw JSON).
- **Document Intelligence** — document extraction service used alongside Content Understanding for work orders/agreements.
- **Voice Live** — Foundry integration that wraps agents with industry-leading streaming voice models over WebSocket ("Voice mode").
- **Hosted agents** — Foundry-managed agent runtime: per-session sandbox isolation, sub-second cold start, zero idle cost, framework-agnostic, durable state + file-system access.
- **Routines** — developer-defined proactive triggers/events (e.g. hourly heartbeat) that Foundry queues, executes, and tracks.
- **Durable Task scheduler** — serverless orchestration to monitor/resume long-running agent work across idle sessions, including human approvals; integrated via the **Microsoft Agent Framework extension for durable task**.
- **Procedural memory** — lets agents learn a playbook across all sessions (public preview).
- **Trace replay view** — observability UI showing a request's full trajectory by time and tokens, with step-level inputs/outputs and speed replay.
- **OpenTelemetry pipeline** — single pipeline logging every invocation/tool call/hop/handoff for hosted agents.
- **Custom rubric / evaluators** — auto-generated, context-aware, weighted evaluation criteria; built-in evaluators include tool selection, tool input, tool output, retrieval, and fluency.
- **Agent Optimizer** — turns production traces + evals into ranked candidate agents (tuning skills, prompts, tool config, models), compared on quality/cost/latency, with lineage and rollback (private preview).
- **Azure Developer CLI (azd)** — used via `azd ai agent eval init` and `azd ai agent optimize` to initialize evals and run the optimization loop.
- **GitHub Copilot / GitHub Copilot CLI / GitHub Copilot SDK** — coding agents and a pluggable harness/SDK for Agent Framework.
- **Claude Code / Claude Agent SDK** (rendered from caption "Cloud Code"/"Cloud Agent SDK") — Anthropic coding agent and a pluggable harness/SDK.
- **Microsoft 365 Copilot & Microsoft Teams** — publish targets for Foundry agents (identity/policy/permissions flow through).
- **Autopilot agents** — agents published to Teams with their own Entra/Azure ID, email address, and Teams presence; can initiate conversations/follow-ups.
- **Agent 365** — governance layer providing end-to-end control over autopilot agents.
- **Dynamics 365 (D365)** — ticketing/tracking system the target agent files incidents into.
- **VS Code, Visual Studio, Cursor** — supported editors; Claude Code/Copilot CLI also supported.
- **Models referenced** — GPT-5, GPT-5.5, Anthropic Opus 4.8 (as selectable target/optimization-driver models).
- **Customer platforms** — Twilio Agent Connect (Twilio), KPMG Workbench (KPMG).

## 🚀 Announcements / What's New
- **Microsoft Agent Framework 1.0 — GA / production-ready** (built-in harness; integrates skills, memory, middleware; plugins for GitHub Copilot SDK and Claude Agent SDK).
- **Foundry Toolkit for VS Code — GA.**
- **Toolboxes in Foundry — GA "soon";** Skills now a first-class integration with Toolboxes.
- **Voice Live integration with Foundry Agent Service — GA today** for prompt agents; **public preview** for hosted agents.
- **Hosted agents in Foundry Agent Service — GA "soon"** (per-session sandbox isolation, sub-second cold start, zero idle cost, framework-agnostic, durable state + file-system access; supports long-running autonomous agents).
- **Routines (Foundry Agent Service) — public preview.**
- **Publish to Microsoft 365 Teams & Copilot — GA "soon"** (identity/policy/permissions flow through automatically).
- **Autopilot agents in Teams — public preview** (own Entra ID, email, Teams presence; governed in Agent 365).
- **Rubric for custom evaluation — public preview.**
- **Agent Optimizer for Foundry Agent Service — private preview.**
- **Procedural memory in Foundry Agent Service — public preview.**

## 💡 Demos
- **Build an agent in VS Code (live):** Generate a fiber field-operations agent with GitHub Copilot in the Foundry Toolkit; auto-applied best-practice skills; built on Microsoft Agent Framework (Python) with the new harness.
- **Wire up tools via Foundry Toolbox:** Configure Foundry IQ, Fabric IQ, Work IQ, Web IQ, plus guardrails and tool search through one MCP-compatible endpoint; connect Content Understanding to make a tabular PDF spec agent-readable.
- **F5 local debug:** Run the agent on localhost, hit a breakpoint on an on-site connection-type question, inspect request/response and streaming events.
- **Voice enablement:** Toggle "Voice mode," then ask by voice for the **Quincy North Site** fiber-termination spec; agent streams progress and answers **LC/UPC duplex on the B-side panel** over a WebSocket voice connection.
- **"Fiby" — Claude-like long-running agent:** Configure an hourly **routine/heartbeat** to check the investigation log for anomalies and act.
- **Isolated sessions + file-system inspection:** Open a session idle since 11 a.m., view logs and the saved file-system state (anomaly analysis, vendor contacts, investigation breadcrumbs) — secure in the cloud, zero idle cost.
- **Durable Task human-in-the-loop:** A pending-approval instance waited 2–3 hours with all sessions idle; clicking **Approve** resumes the session, restores state, and continues work — shown live across the Durable Task and Foundry session views.
- **Publish to Teams as an autopilot agent:** Fiby running in Teams with its own identity/email (`fiby@notareal.co`); asked about active incidents, it resumes/starts a session and replies.
- **Trace replay (operate):** Inspect a request's trajectory by time and tokens, click into step inputs/outputs, and **replay the conversation at 8× speed**.
- **Eval + optimize loop:** `azd ai agent eval init` auto-generates an eval dataset and a custom weighted rubric (bumping voice-conciseness weight 3 → 10); `azd ai agent optimize` runs the optimization loop and surfaces ranked candidates — one giving **+11%** on the rubric — ready to deploy as the new default. (A few live-demo hiccups — a misplaced browser tab/URL — were handled on stage.)

## 📊 Notable Stats / Quotes
- **80,000+ customers** running on Foundry today.
- **Iberdrola** scaling mission-critical energy operations across **14 countries**.
- Optimizer found a candidate giving **~11% better performance** on the voice-conciseness rubric.
- Trace example: initial model reasoning took **~20 seconds** before the first tool call; replay shown at **8× speed**.
- Voice-conciseness rubric weight changed from **3 → 10**.
- Session framed as **~45 minutes** to go from a local laptop agent to one running across **thousands of conversations** in production.
- Fiber spec answer: **Connector family — LC/UPC duplex required on the B-side panel** (Quincy North Site).
- **"Building is no longer the hard part... The question has shifted from can I build it to can I run it reliably at enterprise scale?"** — Tina Sharkey.
- **"Agents are teammates, not tools."** — Tina Sharkey.
- **"AI systems are never done. They run on production learning loops."** — Tina Sharkey.
- **"Build simply, deploy powerfully, operate with trust."** — closing tagline.
- **"This is as live as it gets"** — Jeff Holland, on the unscripted demo.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install the **Foundry Toolkit for VS Code** (GA) and scaffold an agent with **Microsoft Agent Framework 1.0** + the new **harness**.
  - Stand up a **Foundry Toolbox** with **tool search** + PII guardrails over a single MCP endpoint; connect an IQ source (Foundry IQ / Fabric IQ / Work IQ).
  - Run **Content Understanding** on a tabular PDF to get agent-ready markdown/JSON.
  - Voice-enable an agent via **Voice Live** and test the streaming WebSocket experience.
  - Configure a **routine/heartbeat** on a **hosted agent** and verify per-session isolation + zero idle cost.
  - Wire up the **Durable Task scheduler** for a human-in-the-loop approval that resumes state.
  - Build the eval → optimize loop with `azd ai agent eval init` / `azd ai agent optimize`, generate a **custom rubric**, and review ranked candidates by quality/cost/latency.
- [ ] Questions:
  - What are the exact GA dates / regions behind the many "GA soon" items (hosted agents, Toolboxes, Publish to Teams)?
  - Pricing model for hosted agents (zero idle cost — but per-session/runtime billing details)?
  - How does **procedural memory** interact with isolated sessions and PII guardrails?
  - What's the model/eval cost of running `azd ai agent optimize` loops at scale?
  - How is **Agent 365** governance configured for autopilot-agent identities/emails?
- [ ] Relevant to:
  - Azure/AI platform teams building production, long-running, multi-agent systems.
  - Anyone moving an agent prototype to governed, observable, self-improving production.
  - Ops/SRE-style "agent as teammate" automation (incident response, dispatch).

## 🔗 Related
- [[2026 Build Session List]]
- Microsoft Build 2026 — Content Understanding session (referenced for the next day)
- Microsoft Build 2026 — Claude-like / autonomous agents session (referenced for next morning)
- Microsoft Build 2026 — Observability session (referenced as the following session)

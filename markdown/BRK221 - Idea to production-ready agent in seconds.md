---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/runtime
  - topic/azure
  - topic/containers
source: https://www.youtube.com/watch?v=4VPLRt25bec
session_code: BRK221
event: Microsoft Build 2026
speakers: Devanshi Joshi (PMM, Azure Container Apps), Simon (Microsoft Azure Container Apps product team), Gopi (Augur)
duration_min: 45
aliases:
  - Idea to production-ready agent in seconds
---

# BRK221 — Idea to production-ready agent in seconds on AI-native runtime

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Devanshi Joshi — Product Marketing Manager, Azure Container Apps · Simon — Microsoft Azure Container Apps product team · Gopi — Augur (customer)  
> **Duration:** ~45 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=4VPLRt25bec)

## 🎯 TL;DR
The session argues that most agentic-AI projects fail not because of the model but because of the **runtime** they run on — citing Gartner's prediction that **>40% of agentic AI projects will be cancelled by 2027**. The Azure Container Apps team lays out five non-negotiable runtime requirements (sub-second start/resume, native tool-calling/integration, persistent state, strong per-task isolation, and unified tooling) and unveils **Azure Container Apps Sandboxes** (now in **public preview**) — fast, isolated, stateful, scale-to-zero compute built for agents *to run on* and *for agents to use*. A live demo runs three voice-driven agents (Arya, Nova, SRE Agent) on serverless GPUs (Whisper + Kokoro speech models) and sandboxes, showing instant resume with memory state, snapshots, per-sandbox L7 firewall isolation, inherited connectors, and live port exposure. Customer **Augur** closes by showing how it built an autonomous supply-chain platform on ACA in ~14 months, running **40+ services and thousands of agents** for "agentic data integration" and a real-time simulation/what-if engine backed by its **OUSCO** supply-chain ontology.

## 🔑 Key Takeaways
- **Runtime, not model, is the failure point.** "It's not because of the models. It's because of what you're running, where you're running, how you're running." Gartner: **>40% of agentic AI projects cancelled by 2027**.
- **Five things a runtime MUST deliver** (treat as the spec you build to, not optimizations): fast startup & resume, native execution/tool-calling stitched to your other apps, persistent state, strong per-task isolation, unified tooling.
- **Cold start must be sub-second, every time** — "10-second startup was old-time technology. Now we're talking less than 100 milliseconds." Not a tuning exercise you nail on day five.
- **Agents are event-driven**: wake → do task → idle → wake. The runtime must support this loop with instant resume and not charge you for idle.
- **Don't run untrusted/agent-generated code on your dev laptop** — it already holds SSH keys, browser cookies, prod credentials. That's a liability; agents need a fresh sandbox per task.
- **Azure Container Apps Sandboxes** (NEW, **public preview**) = fast, isolated, stateful compute on demand; secure-by-default isolation for untrusted workloads; resume instantly preserving context; burst zero → thousands of instances and scale back to zero.
- **Resume captures memory state, not just disk** — a sandbox left running a script, slept ~20–25 min, woke in ~1–2 sec and continued exactly where it left off. Configurable: capture disk+memory or disk-only.
- **Sandbox groups** hold shared entities (connectors, volumes, snapshots, disk images); child sandboxes **inherit** those settings — e.g. create an agent with calendar/email/Teams connectors and it just has that access.
- **Isolation is more than process isolation** — each sandbox gets a **Layer-7 firewall**; you control allowed hosts and which routes are denied per host (network isolation), plus identity/data/access governance at the **runtime level**.
- **Snapshots** capture an entire disk so agent work (which is constantly undone/redone) can be replayed or branched from — "Git works great, but stuff gets missed when agents do work." Snapshot → create new sandbox = exact clone.
- **Serverless GPUs** on ACA: T4 and A100 GPUs, available in **15 regions**, scale-to-zero, pay only while running — "the easiest way to run your custom models" from Hugging Face via vLLM/Llama or any model container.
- **Pre-warm pools** address cold start for sandboxes; **Azure Container Apps Express** (launched ~1 month prior) is "fast Container Apps" — environment-less, no physical cluster, best for web apps/regular APIs (the deploy target, vs. sandboxes as the dev/iteration environment).
- **Microsoft dogfoods this runtime**: GitHub Copilot cloud/coding sandboxes, Foundry hosted agent service, and Container Apps Express all run on the same agent runtime.
- **Six adoption patterns** for sandboxes: multi-tenancy, platform-for-execution (e.g. EdTech student environments), agent workflows, AI code execution, platform building, and interactive user sessions.
- **Augur proof point**: built an enterprise autonomous supply-chain platform on ACA + Azure AI Foundry from first line of code (~March last year) to GA in ~14 months — 40+ services, thousands of agents/day.

## 📚 Detailed Notes

### Framing: why agents break between demo and production
Devanshi Joshi (PMM, Azure Container Apps) opens with audience polling: of those who deployed agents in the last 3 months, roughly **50–70% said their agents are no longer doing what they wanted at deploy time**. The thesis: this isn't a model problem. Gartner predicts **over 40% of agentic AI projects will be cancelled by 2027**, and the cause is the runtime — *what / where / how* you run.

The failure modes she enumerates:
- **One bad tool call brings down your workspace.** You restart, rebuild, and eat cold-start throttle in the agent loop — toil for the execution environment that can even lead to data leaks.
- **Budgets burn unattended.** Paraphrasing a news quote: "Agents are extremely good at burning through budgets and get even better when left unattended." A runaway overnight loop can torch a month of token spend before you notice.
- **Untrusted code on the dev laptop.** The agent has access to your machine — SSH keys, browser cookies, prod credentials. Running agent-generated code there (no sandbox) is a liability.
- **Cold-start throttle.** Startups exist purely to give sub-second provisioning. An agent sitting idle waiting on provisioning is unacceptable. 10s is "old-time tech"; the bar is **<100 ms**.
- **Workspaces dying on restart** lose context, cache, and intermediate state, paying the "environment setup tax" every time — long-running agents can't be long-running if their floor of context is removed.
- **Tooling stitched by hand.** Every runtime ships its own configs, packaging, rules; porting between runtimes as you move from dev to agents is a recurring headache.

### The five-requirement runtime spec
Joshi reframes the failure modes into five things a runtime must deliver **all the time, not sometimes** — "these aren't five optimizations, they're the spec you build with":
1. **Fast startup and resume.** Agents are event-driven (wake → act → idle → wake). Cold starts must be sub-second every time, not a tuning exercise. If resume is slow, the agent can't pick the user's thread back up.
2. **Execution stitched to the rest of your apps.** Agents are only useful when acting — calling APIs, running code, talking to other cloud services. That must live *inside the runtime*, not in fragile glue code.
3. **Persistent stored state.** Long-running agents reason across hours; persistence is required so the agent stays live without re-paying the setup tax. (Imagery: people walking around with laptop lids open so the agent keeps running.)
4. **Strong isolation per agent task.** Every execution lands in its own fresh sandbox while keeping security boundaries — preventing data/system/permission/access leaks. Governance covers not just identity/data but *which systems the tool-calling connects to*, enforced at the **runtime level** (not per-agent or per-project).

> Note: Joshi frames these as five, with persistent state and isolation tightly coupled; the deck/demo treats fast resume, integrated execution, persistence, and isolation as the pillars, plus unified tooling vs. the hand-stitched-tooling pain point.

### The demo architecture (Simon)
Simon (Microsoft ACA product team) — self-described as "the guy you call on stage when the high-wire act goes [wrong]" — walks the architecture, which spans two layers:

**Top layer — Container Apps environment with serverless GPUs:**
- Two speech models on **serverless GPU**: **Whisper** (speech-to-text) and **Kokoro** (text-to-speech).
- A **multi-agent broker** that intercepts every prompt in/out of every agent and translates text ↔ audio (the voice pipeline).

**Bottom layer — agent infrastructure on sandboxes:**
- Multiple **sandboxes** each running **GitHub Copilot CLI** (named agent areas, e.g. one called **Nova**).
- An **Azure SRE Agent** added as part of the demo.
- A series of **proxy bridges** that interface with the multi-agent broker so users talk to agents by voice.
- A **browser** front end for the conversation, plus — as "extra credit" — a **phone call gateway** built and run on ACA by **Twilio**.

The three demo agents:
- **Arya** — a regular Copilot / developer agent.
- **Nova** — a personal assistant with access to Simon's calendar, Teams meetings, and emails (via inherited connectors).
- **SRE Agent** — monitors the application and reports on infrastructure health.

### Live demo walkthrough
- **Mic check / voice**: agents greet the audience over the voice pipeline (slight delay noted as expected for the audio round-trip).
- **Give Arya a job**: "build a tic-tac-toe game and tell me the port it's listening on." Arya goes off to work (takes a couple of minutes) — demonstrating an agent doing real code execution inside a sandbox.
- **Ask Nova in parallel**: "what build-related meetings are on my calendar today?" Nova returns real calendar holds and sessions (mentions TECBRK 221 / BRK221). Then "what was my last Teams message?" — Nova reads a recent Teams message (referencing Twilio + Voice Live API + SRE agent chat, noting Simon is presenting live at BRK221). Simon stresses this was **not rehearsed** and that sandboxes natively connect to an endless number of endpoints via **sandbox connectors**.
- **Ask SRE Agent**: "what application are you watching?" It describes **Voice Connect** — a real-time multi-agent voice communication platform connecting users via **WebSocket audio sessions** to AI agents (Claude, an SRE agent, a sandboxed code-execution agent), with STT/TTS handling the audio pipeline, running on **Azure Container Apps, ACR, and Log Analytics**.
- **Arya finishes**: tic-tac-toe game is up on **port 80**.
- **Omni-channel point**: Simon notes voice/omni-channel feels more natural than constantly typing — you can keep agent "doors" open and converse back and forth.

### Infrastructure deep dive
- **ACA environment view**: shows all running apps and **workload profiles**. Two apps run the STT and TTS models on serverless GPU; both **scale to zero** when idle, so you pay only while running.
- **Serverless GPU plug**: easiest way to run custom models — Hugging Face via vLLM/Llama or any model-hosting container; T4 and A100 GPUs across 15 regions.
- **Azure SRE Agent**: a full-featured agent with many connectors — connect to a knowledge base, do code check-ins/checkouts, etc. Here it's wired to audio.

### ACA Sandboxes — the core feature
Simon spends most of the remaining demo on **ACA Sandboxes**, "a new offering being launched into public preview." Key framing: it's an **agent-first platform** in *two* senses — a platform to *run* agents **and** a platform *for agents to use*.

- **Sandbox groups**: hold entities — **connectors, volumes, snapshots, disk images**. Sandboxes run inside a group and **inherit** the group's settings (this is how Nova inherited calendar/Teams/email connectors).
- **Instant resume with memory state** (highlighted as the best part): a sandbox left running a background script slept for ~20–25 minutes; Simon woke it in roughly **1–2 seconds** and the script continued *exactly* where it left off. Configurable to capture **disk + memory** or **disk only** on sleep.
- **Fast create from templates**: a set of pre-configured templates ship; clicking "create" provisions a sandbox near-instantly. Connecting in and launching Copilot, the **GitHub token set on the sandbox group is auto-passed in**, so Copilot is authenticated immediately.
- **Network isolation (not just process isolation)**: each sandbox gets a **Layer-7 firewall**; you control exactly which hosts are allowed and which routes on which hosts are denied.
- **Port exposure**: Arya's tic-tac-toe game on port 80 is exposed live via a simple "add/expose this port" action, and Simon plays the game on stage.
- **Snapshots**: because agent work is constantly undone/redone and "stuff gets missed" even with Git, snapshotting the whole disk lets you replay or branch forward. Snapshot (e.g. "D91") → create a **new sandbox from snapshot** = an exact clone of the original agent's state/sessions.
- **Phone "extra credit"**: via the Twilio-built call gateway on ACA, Simon phones the agent trio ("Voice Connect agent — who would you like to talk to?") and asks about the last check-in (a real commit: "client phase 7 UI polish" with door-closed state, drop-mode banner, new Nova avatar). A request to Nova to email someone is correctly refused by the SRE agent ("I don't have the ability to send emails… focused on infrastructure"), illustrating per-agent capability scoping.

### Introducing Azure Container Apps Sandboxes (the engine) — back to Devanshi
After the demo, Joshi formally introduces the engine: **Azure Container Apps Sandboxes** — *fast, isolated, stateful compute infrastructure on demand, executing securely by default, isolated for untrusted workloads.* Not just AI-generated code but also **multi-tenant** scenarios. It resumes instantly preserving context end-to-end and bursts to **hyperscale — zero to thousands in seconds — then dies back to idle** so spend goes to tokens, not idle compute.

It's the **foundation layer already powering Microsoft's own experiences**: **GitHub Copilot's cloud/coding sandboxes** (also launched at Build), **Foundry hosted agent service**, and **Container Apps Express**.

- **Cold-start handling**: **pre-warm pools** for sandboxes; **Container Apps Express** is "fast Container Apps."
- **Container Apps Express** clarified: use it for everything that is *not* the agent itself — regular APIs/apps/web apps (the application layer / deploy target). Sandboxes are the fast iteration/dev environment agents run in and use.

### Customer adoption patterns
Joshi stresses sandbox value isn't industry-specific — net-tech, ISV services, startups all benefit, whether extending existing apps or building new experiences. Named examples:
- **EdTech / "Ed Chat" for the Department of Education, South Australia** — safe, sandboxed environments per student to build and test technology (democratized AI experience).
- **Sitecore AI** — runs long-lived agent executions safely/securely in production on its Sitecore AI platform, doing real production work end-to-end without losing control over its agents (multi-tenancy pattern).

**Six emerging patterns**: (1) multi-tenancy (Sitecore AI), (2) platform-for-execution of user/student environments (EdTech), (3) agent workflows (Simon's demo), (4) AI code execution (agent becomes "the user" asking a sandbox to spin up, act, and die down — so production data isn't at risk), (5) platform building (startups building AI/agent/copilot platforms on sandboxes, or multi-tenant ISV experiences), (6) interactive user sessions.

### Customer story: Augur (Gopi)
Gopi from **Augur** presents building **autonomous supply chains** with agents. Opening point: more people *write code today* than started their careers writing code, because agents now write code (his 15-year-old daughter included).

**The supply-chain problem**: even a simple pen has an insane supply chain — raw materials → processed manufacturing parts (ink, ball) → component assembly → shipping → warehousing → transport → retail → you. Combinatorial complexity explodes with variants ("a pink pen that writes in blue," "a pen-pencil"); now scale that to an iPhone or an NVIDIA GPU. Augur's mission: **autonomous supply chains using agents to coordinate across this gamut and eliminate the "coordination tax."**

Three pillars of Augur:
1. **Built on Augur's Universal Supply Chain Ontology (OUSCO)** — every layer of the stack shares the same terminology so agents can act comfortably.
2. **AI-native** — they don't reinvent foundational models; heavily **context-driven** because decades of operator/institutional knowledge in supply chains is undocumented and not in the public domain, yet essential to operate effectively.
3. (Implied throughout) **agents for reasoning, deterministic blocks for math/physics.**

**Problem 1 — data lives in silos; unstructured knowledge is lost.** Every deployment is bespoke and doesn't scale; "death by a thousand cuts" — solve the first 20% and the remaining 80% is edge cases. Augur's answer is **Agentic Data Integration (ADI)** on ACA: **thousands of agents** running concurrently. Example: a customer points Augur at a Snowflake account with **900 tables, 1,000+ columns each, millions of rows**. A human team would take **~12 months** just to start making progress on one customer. Instead an **agentic harness** figures out what each table means semantically, how tables/columns relate, and percolates that up to higher-level agents that reason about and join tables and predict interoperation. A **human-in-the-loop** layer lets long-running agents **sleep, then wake** via approval/information workflows to collect context and feed the next stage — compressing a ~1-year integration into **days**.

**Problem 2 — agents break without a world model.** Hyper-customizing every supply-chain problem into a bespoke solution doesn't scale. **OUSCO (Osco)** is richer than a data schema: it codifies common mathematical operations, common functions, and the *physics* of how a supply chain operates (how products move, processes, buffers). **Agents do decision-making/reasoning; deterministic work happens in strong deterministic blocks exposed as tools** to those agents. The world model scales across multiple customers.

**Connecting data ↔ world model — "the bus."** Because ADI is aware of the higher OUSCO layer it must report into, it **automatically builds ETL pipelines and ML notebooks** and connects incoming data into interoperable intelligence wired to the OUSCO layer. On top sits **context** — company-specific decision logic (e.g. tier-1 customers can never go hungry; tier-2 can starve a little) pulled in real time.

**Offline vs real-time.** The first two pillars are **offline workflows** using thousands of agents. The third is a **real-time** workflow: a what-if question ("what happens if I put a warehouse in this location?") runs through a modeling/simulation pipeline that must be **parameterized** with the right inputs in real time. This needs **very fast ACA agents that open sandboxes, run, hand off to other agents that make local decisions and pull data — all within ~10 seconds.** Back-end (long-running) work can take time; the **front-end experience must be fast**.

**Speed-to-market**: from the first line of code (~**March last year**) to **publicly closing with customers today** — an enterprise-grade, at-scale solution built in ~14 months, thanks to **ACA + Azure + Azure AI Foundry**. Augur runs **40+ services on Azure Container Apps** with **thousands of agents daily**.

### Closing three things (Devanshi)
1. **Container Apps already delivers a cohesive agent runtime for customers in action** (Augur as proof) — apps + sandboxes stitched together.
2. **Container Apps Sandboxes are now in public preview**, and Microsoft uses it itself — GitHub, Foundry, Container Apps and other Azure services run on the same agent-runtime experiences.
3. **Get started**: read the **Azure Container Apps all-up product blog**; Simon's **demo code is in the linked repo**; access the **sandboxes portal at `aka.ms/aca/sandboxes/portal`**; there's a blog with end-to-end samples; and check out **Express** too.

### Q&A
- **Express vs Sandboxes — when to use which?** Simon: **Sandboxes** are a *fast iteration environment* — built for agents to be run on *and* for agents to use during development; very transient ("think of them as your laptop you're finishing work on while running through the airport"). **Express** is what you *deploy to* — similarly speedy, **environment-less** (no physical cluster behind it), essentially just an app, **best for web apps**; launched ~a month ago. Rule of thumb: **develop with your agents on sandboxes, deploy on Express.**
- **Where does the OUSCO world model live / what format?** Gopi: it's **actual code — an object-oriented representation** inside their codebase (they want as much as possible to be deterministic). **Agents are registered with OUSCO**, every object is registered, the data schema is OUSCO, common functions are OUSCO — a world model not just of data but of *how supply chains operate*.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Container Apps (ACA)** — serverless container platform; the agent runtime backbone for this session.
- **Azure Container Apps Sandboxes** — NEW (public preview): fast, isolated, stateful on-demand compute; agent-first platform to run agents on and for agents to use; instant resume with memory state, snapshots, L7-firewall isolation, sandbox groups with inherited connectors.
- **Sandbox groups** — container for shared entities (connectors, volumes, snapshots, disk images) that child sandboxes inherit.
- **Sandbox connectors** — native connectivity from a sandbox to endless endpoints (calendar, email, Teams, etc.); inherited from the sandbox group.
- **Snapshots** — whole-disk capture of a sandbox to replay/branch/clone agent state.
- **Pre-warm pools** — keep sandboxes warm to eliminate cold start.
- **Azure Container Apps Express** — "fast Container Apps"; environment-less (no physical cluster), best for web apps/regular APIs; the deploy target (vs sandboxes for dev). Launched ~1 month prior.
- **Serverless GPUs (on ACA)** — T4 and A100 GPUs, 15 regions, scale-to-zero, pay-per-run; easiest way to host custom models.
- **Azure SRE Agent** — full-featured monitoring/troubleshooting agent with many connectors (knowledge base, code check-in/out); wired to audio in the demo.
- **GitHub Copilot CLI** — coding agent running inside the demo sandboxes (Arya, Nova).
- **GitHub Copilot cloud/coding sandboxes** — Microsoft's own Copilot sandboxes, also launched at Build, running on the same ACA sandbox engine.
- **Azure AI Foundry — hosted agent service** — Microsoft agent service built on the same runtime; used by Augur.
- **Whisper** — speech-to-text model running on serverless GPU in the demo.
- **Kokoro** — text-to-speech model running on serverless GPU in the demo (caption garbled it "Cocooro").
- **Multi-agent broker** — intercepts every agent prompt in/out and translates text ↔ audio (the voice pipeline).
- **Proxy bridges** — interface between the multi-agent broker and individual agents for voice in/out.
- **Voice Connect** — the demo app: real-time multi-agent voice platform over WebSocket audio sessions to AI agents, with STT/TTS pipeline, running on ACA + ACR + Log Analytics.
- **Twilio call gateway** — phone-call entry point to the agents, built and run on ACA by Twilio (the "extra credit" phone demo).
- **Azure Container Registry (ACR)** — image registry in the demo stack.
- **Azure Log Analytics** — observability backend in the demo stack.
- **vLLM / Llama / Hugging Face** — referenced as model sources/hosting paths for serverless GPU.
- **Claude** — named as one of the AI agents in the Voice Connect platform.
- **Augur OUSCO (Osco)** — Augur's Universal Supply Chain Ontology; object-oriented code world model codifying supply-chain physics, functions, schema; agents/objects register with it.
- **Augur Agentic Data Integration (ADI)** — thousands of concurrent agents that semantically map/join siloed data and auto-build ETL pipelines + ML notebooks.
- **Snowflake** — example customer data source (900 tables × 1,000+ columns) ingested by Augur's ADI.
- **Workload profiles (ACA)** — compute profile assignment shown in the environment view.

## 🚀 Announcements / What's New
- **Azure Container Apps Sandboxes — Public Preview** (the headline announcement): fast, isolated, stateful, scale-to-zero compute; instant resume with memory state; snapshots; L7-firewall network isolation; sandbox groups + inherited connectors; bursts zero → thousands of instances.
- **Pre-warm pools for sandboxes** — to address cold start (mentioned as available).
- **Azure Container Apps Express** — already GA-ish/launched ~1 month before this session; "fast Container Apps," environment-less, web-app-optimized deploy target.
- **Serverless GPUs** — T4 + A100 across 15 regions on ACA (promoted; recommend trying).
- **Microsoft dogfooding** — GitHub Copilot cloud sandboxes, Foundry hosted agent service, and Container Apps Express all run on the ACA agent runtime (GitHub Copilot cloud sandboxes also noted as launched at this Build).
- **Get-started resources**: ACA all-up product blog; Simon's demo **code repo**; sandboxes portal at **`aka.ms/aca/sandboxes/portal`**; blog with end-to-end samples.
- **Status note:** Container Apps Sandboxes = **public preview**. Express = launched (~1 month prior). Serverless GPU = generally available. (Exact GA dates for Express/GPU not stated in the talk.)

## 💡 Demos
- **Three voice agents on stage (Arya, Nova, SRE Agent)** — proved agents run on sandboxes + serverless-GPU voice pipeline and can be driven by natural voice (omni-channel) rather than typing.
- **Arya builds a tic-tac-toe game** — agent does real, autonomous code execution inside a sandbox and reports the listening port (80); proved in-runtime code execution + tool use.
- **Nova reads live calendar + Teams message** — unrehearsed; proved sandbox connectors reach real endpoints (calendar/email/Teams) inherited from the sandbox group.
- **SRE Agent describes the app it monitors** — proved an infrastructure-aware agent with its own connector set and scoped capabilities.
- **Instant resume with memory state** — a sandbox running a background script slept ~20–25 min and woke in ~1–2 sec, continuing exactly where it left off; proved stateful, sub-second resume (disk+memory).
- **Create sandbox from template** — clicking "create" provisions near-instantly; launching Copilot auto-uses the group's GitHub token (authenticated immediately); proved fast start + inherited credentials.
- **Network isolation per sandbox (Nova)** — showed the L7 firewall: allowed hosts and denied routes per host; proved isolation beyond process boundaries.
- **Expose port → play the game** — exposed Arya's port 80 live and played tic-tac-toe on stage; proved trivial service exposure from a sandbox.
- **Snapshot → clone** — snapshotted a sandbox ("D91") and created an exact new sandbox from it (same sessions); proved disk snapshot/replay/branching.
- **Phone call via Twilio gateway** — phoned the agent trio, asked about the last commit; Nova-email request correctly refused by the scoped SRE agent; proved omni-channel reach + per-agent capability scoping.
- **Augur (slides/architecture, not live)** — walked ADI (thousands of agents mapping a 900-table Snowflake DB), OUSCO world model, the "bus" auto-building ETL/ML pipelines, and a real-time ~10-second what-if simulation flow; proved production-scale agentic workloads on ACA.

## 📊 Notable Stats / Quotes
- **">40% of agentic AI projects will be cancelled by 2027"** — Gartner, cited as the central warning.
- **"It's not because of the models. It's because of what you're running, where you're running, how you're running."** — Devanshi Joshi.
- **"10-second startup was old-time technology. Now we're talking less than 100 milliseconds."** — on the cold-start bar.
- **"Agents are extremely good at burning through budgets and get even better when left unattended."** — paraphrased news quote on runaway loops/token spend.
- **"These aren't five optimizations. They are the spec that you build with."** — Joshi, on the runtime requirements.
- **"It is an agent-first platform for agents to use."** — Simon, reframing sandboxes.
- **50–70%** of audience hands dropped when asked if their deployed agents still do what they wanted.
- **Resume:** slept **~20–25 min**, woke in **~1–2 sec**, continued exactly as before.
- **Serverless GPU:** **T4 + A100**, **15 regions**, scale-to-zero.
- **Augur scale:** **40+ services** on ACA, **thousands of agents/day**; first line of code ~**March last year** → publicly live with customers in **~14 months**.
- **Augur Snowflake example:** **900 tables**, **1,000+ columns each**, **millions of rows**; human team ≈ **12 months** to even start → compressed to **days**.
- **Augur real-time loop:** open sandbox → run → hand off → pull data, all within **~10 seconds**.
- **Sandboxes portal:** `aka.ms/aca/sandboxes/portal`.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: spin up an **ACA Sandbox** from a template and verify sub-second create + Copilot auto-auth via sandbox-group GitHub token; test **resume with memory** (disk+memory vs disk-only) on a long-running script; create a **snapshot** and clone it; configure the **L7 firewall** (allowed hosts / denied routes); deploy a web app to **Container Apps Express** and contrast with a sandbox; try **serverless GPU** hosting a Hugging Face model (Whisper/Kokoro-style).
- [ ] Questions: What are sandbox limits (max concurrent, lifetime, size tiers, regions in preview)? Pricing model for sandboxes vs Express vs serverless GPU? How do connectors handle secrets/identity (managed identity?) vs the GitHub-token example? Is the L7 firewall egress-only or also ingress? How do snapshots interact with attached volumes? SLA/observability story for long-running sandboxes? Multi-tenant isolation guarantees for ISV scenarios (Sitecore-style)?
- [ ] Relevant to: agent runtime/platform decisions for any internal agentic projects; safe execution of AI-generated/untrusted code; demo/lab environments needing per-task isolation; cost control on idle agent loops (scale-to-zero); customer conversations on ACA sandboxes + Express + serverless GPU; supply-chain / data-integration agent patterns (Augur ADI + ontology approach).

## 🔗 Related
- [[BRK227 - Distributed systems to AI platforms]]
- [[BRK240 - Build context-aware agents]]
- [[DEMSP381 - Scale agentic AI on Azure with Arm Cobalt VMs]]
- ACA all-up product blog · Sandboxes portal: `aka.ms/aca/sandboxes/portal`
- 
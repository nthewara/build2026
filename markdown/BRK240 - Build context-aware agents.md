---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/azure
  - topic/data
source: https://www.youtube.com/watch?v=lekS6wuiHiM
session_code: BRK240
event: Microsoft Build 2026
speakers: Amanda Silver, Marco Casalaina
duration_min: 45
aliases:
  - Build context-aware agents
---

# BRK240 — Build context-aware agents: From data to decisions

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Amanda Silver (CVP, Developer Division / Microsoft Developer Tools & Platforms — 2+ decades at Microsoft) and Marco Casalaina (VP, AI Products — demos)  
> **Duration:** ~45 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=lekS6wuiHiM)

## 🎯 TL;DR
The central thesis: most agentic AI projects fail not because the models are weak, but because the agents lack **context** — a shared understanding of the people, data, policies, and business meaning around them. Microsoft's answer is **Microsoft IQ**, positioned as "the context layer for the agentic web," composed of four context sources: **Work IQ** (organizational/people context from M365), **Fabric IQ** (business knowledge — data, semantic models, ontologies), **Foundry IQ** (enterprise knowledge + governed agentic retrieval), and **Web IQ** (the world's real-time knowledge). Throughout, a single "refund processor" agent is built and grounded across all four IQs, demonstrating two recurring themes: **reuse** (define knowledge/context once, share across many agents) and **context delegation** (agents "phone a friend" sub-agent instead of cramming everything into a finite context window). The session closes on **agent identity** — turning the agent into an A365 template that any user can instantiate in Teams, giving it its own inbox, org-chart entry, and scoped permissions. Recurring message: intelligence (right context, not more context) makes agents *useful*; governance/trust makes them *deployable*.

## 🔑 Key Takeaways
- **>40% of agentic AI projects are expected to fail** — root cause is missing context, not model capability.
- The hard part isn't giving agents *access* to information; it's giving them a **shared understanding** of people, data, policies, and business context.
- **Microsoft IQ = the context layer for the agentic web**, unifying four sources: Work IQ, Fabric IQ, Foundry IQ, Web IQ.
- Analogy used throughout: infusing an agent with context is like onboarding a **seasoned employee** vs. a brand-new hire — you want every new agent to inherit institutional knowledge.
- **Web IQ** is a *grounding platform* (not a search API wrapped in AI) for real-time, citation-ready, multimodal (web/news/images/video) grounding, with **sub-200ms P95** latency and **passage-level ranking** to save tokens.
- **Foundry IQ** is a unified, governed **enterprise knowledge layer** that auto-ingests/enriches sources and does **agentic retrieval** (it's really a *sub-agent* that can retry and rerank), not just a static knowledge base.
- **Fabric IQ** brings real-time business understanding via three layers on **OneLake**: unified data → **semantic models** (often reused straight from Power BI) → **ontologies** (business entities + relationships expressed as *verbs*, not tables).
- **Ontologies** turn tables into business meaning ("a customer *sends/receives* a package"), support synonyms/metadata, and can be **bootstrapped from existing semantic models** or exposed directly as an **MCP server**.
- **Work IQ** is the *people layer* — the agent-facing, "headless" version of Outlook/Teams/SharePoint/Word — built **for agents, around organizational context, on top of (not a copy of) your existing M365 security model**. Data stays in your tenant.
- Work IQ bundles four capabilities: **Chat** (agent↔people/agent), **Context** (grounded org understanding), **Tools** (governed retrieve + act as the user), and **Workspaces** (persistent state for long-running agents).
- **Two unifying patterns**: **reuse** (don't redefine the same data sources/context for every agent) and **context delegation** (offload heavy structured-query context to a Fabric data agent so downstream agents stay lean).
- **Agent identity / A365**: an agent definition becomes a **blueprint → agent template**; users **instantiate** it in Teams, giving *their* agent its own identity, inbox, Teams presence, an **org-chart reporting line**, and a **scoped permission space** (e.g. draft-but-not-send).
- On-behalf-of vs. own-identity: Work IQ acting "as me" inherits all my permissions; an instantiated agent gets its **own, restrictable** rights — a key governance lever.
- Closing principle: don't just stuff agents with more info (that's expensive) — give them the **right** context for the highest-confidence decision with minimal information. **Intelligence makes agents useful; trust makes them deployable.**
- Every IQ layer is built on the **same foundation of identity, governance, and security**: agents are permission-aware by default, every action is traceable/explainable, policies applied consistently — because the real challenge is governing **thousands** of agents, not one.

## 📚 Detailed Notes

### The problem: software is shifting from apps to agents
Amanda Silver opens by framing this as the most profound shift she's seen in 20+ years on Microsoft developer tools/platforms: software is evolving **from people-driven applications to agents defined by intent and measured by outcomes**. Agents can reason, retrieve context, make decisions, and take action on a user's behalf — the long-promised "automated future."

But there's a hard statistic: **more than 40% of agentic AI projects are expected to fail** — *not* because models aren't capable, but because **agents lack the context they need to succeed**. To compensate, developers today stitch together fragmented data sources, custom retrieval systems, permissions models, and orchestration logic just to make agents useful. Everyone is figuring out best practices simultaneously, so experiences end up **brittle**: agents hallucinate, miss policy boundaries, and break in production.

**Reframing the challenge:** it's *not* about giving agents access to information — it's about giving them a **shared understanding** of the people, data, policies, and business context surrounding their work. When organizations get this right, agents stop acting like isolated apps and start operating with an understanding of the enterprise around them (people, data, workflows, policies). The payoff: better accuracy, more reliable actions, **dramatically less engineering**, and **no need to recreate context for every agent**.

**Core analogy (returns throughout the talk):** it's the difference between welcoming a brand-new employee vs. having a seasoned employee on your team. The question driving the whole session: *how do you take the knowledge a seasoned employee has and infuse every new agent with that context as it executes?*

### Microsoft IQ — the context layer for the agentic web
This is Microsoft's framing for the answer. **Microsoft IQ** is "the context layer for the agentic web," bringing together **four sources of context**:

- **Work IQ** → organizational context (the people layer; M365).
- **Fabric IQ** → business knowledge (data, metrics, semantic models, ontologies).
- **Foundry IQ** → enterprise knowledge and policies (governed retrieval).
- **Web IQ** → the world's knowledge (real-time, external).

Together these give agents a shared understanding of the world, the business, and the work happening on teams — enough context to make the right decisions, take the right actions, achieve intended outcomes, and ultimately **be trusted**.

### The running scenario: a refund agent from a single email
The demo's narrative device: a week earlier Amanda emailed Marco a "crazy idea" — **no spec, no design doc, just an email** — proposing an agent to handle an onerous refund process using all the IQs. Marco shows the journey from that email to a working agent.

He starts in **Copilot CLI** (which has a voice mode), with **Work IQ installed**, and asks it to find Amanda's email and draft a **spec/plan** for the agent. (Live, this hits a transient error / network issues — see Demos — but the intent: Work IQ logs in *on your behalf* to retrieve the email, exactly like the "Work IQ" indicator you see at the top of M365 Copilot when it looks up your mail.) From the resulting spec they built the actual agent. The polished UI is the "fancy front end," but in **Foundry** the agent is shown grounded in **all four IQs**.

### Web IQ — grounding agents in the real world
Amanda's deep dive. Agents don't just need to understand *your business* — often they need to understand the **real world your business operates in**. Example: someone delivering consumer goods needs to understand **micro/local events** to micro-target deliveries across markets.

**What Web IQ is:** it connects AI to **authoritative real-world information** — a **structured, multimodal index across web, news, images, and video** so agent responses are grounded in fresh, verifiable context. Crucially, it's **not a traditional search API wrapped in AI** — it's a **grounding platform built specifically for modern agentic systems**.

**Three things that matter when building agents at scale:**
1. **Quality** — structured, **citation-ready** results across web/news/images/video so users can verify and trust answers.
2. **Speed** — agent workflows are inherently multi-step (retrieval + reasoning + planning + action all add latency); **sub-200ms P95 grounding** keeps workflows responsive as agents chain operations.
3. **Efficiency** — context windows are valuable real estate; Web IQ uses **passage-level ranking** to surface highest-signal info and filter noise, **reducing token consumption and cost** at scale.

**Adoption:** already used by **frontier model providers** and enterprises; **available today to a few Azure customers**. Customer example: **NASDAQ** built a solution called **Board Vantage**, helping boards/executives make real-time decisions where accuracy, timeliness, and trust are critical. With Web IQ, NASDAQ combines enterprise information with external web signals **without compromising security or data boundaries**, grounding AI in fresh authoritative info → faster external context, higher-quality responses, simpler architecture.

### Foundry IQ — your enterprise knowledge, governed
"If Web IQ connects agents to the *world's* knowledge, Foundry IQ connects them to *your* knowledge." Enterprise knowledge is scattered across data platforms, content repositories, business systems, and custom apps. Today developers spend too much time stitching these together before an agent delivers value.

**What Foundry IQ does:** provides a **unified knowledge layer** that automatically **ingests, enriches, and connects** enterprise information, eliminating much of the retrieval logic/infrastructure you'd otherwise build. At runtime it **intelligently retrieves the right information from the right sources**, giving agents the context to answer accurately and act confidently → **less infrastructure to manage, more intelligence per agent**.

**Mental model (three layers):**
- **Foundation — knowledge sources:** enterprise data, documents, applications, and the live web. They *store* information.
- **Context layer:** memory, embeddings, and semantic models turn information into *understanding*.
- **Top — agents & applications:** what users interact with; they *retrieve, reason, and act*.

**Key idea — delegation:** every layer does one thing well. As a developer you **don't rebuild that machinery in every agent**; instead you define a **knowledge base** once and make it available to many agents, so you reach your solution faster.

**Trust is built in, not bolted on:** great grounding isn't only retrieval — **security, governance, and policy enforcement are built directly into the platform**.

**Important nuance (revealed in Marco's demo):** calling it a "knowledge base" is a bit of a **misnomer** — a Foundry IQ knowledge base is really a **separate sub-agent doing agentic retrieval**, meaning it can **try and try again** and **rerank results** before handing them to the downstream agent. This is what lets you **reuse the same grounded context across many agents**.

**Customer example:** **Sitecore** (digital experience / content management) uses Foundry IQ's reusable knowledge bases, agentic retrieval, and enterprise-grade security out of the box to make marketing/brand knowledge accessible to **every agent across the org, every time, with the right permissions**.

### Fabric IQ — understanding the business in real time
Where Foundry IQ unlocks what the org *knows*, **Fabric IQ helps agents understand what's happening in real time**. It connects agents to organizational data — metrics, semantic models, reports describing the current state of the business — so agents **reason with the same context people use to make decisions** daily.

**Three outcomes Fabric IQ delivers:** (1) a shared understanding of how the business operates, (2) insights turned into actions, (3) agents that reason over **business context, not just raw data**.

**The three layers (all live in Fabric, co-located with the data they describe — not stitched together):**

1. **OneLake — unified data.** A single unified data layer bringing together **analytical and operational** data across systems/clouds **without constantly moving or duplicating it**. Even non-Microsoft data can be brought into OneLake. Matters because **agents are only as good as the data they can access**; OneLake gives every team/app/agent the **same source of truth**, eliminating silos and re-authentication/auth errors → consistent, scalable, cost-effective AI.

2. **Semantic models — data ↔ business meaning.** Bridge the gap between raw data and business meaning, defining the **metrics and concepts** teams use to run the business. **Most are already defined in Power BI**, and Fabric IQ can **pick them up directly**. The win: when an agent asks "what happened?", it gets the **same answer your Power BI dashboards give**, what analysts see, and what you report to executives.

3. **Ontologies — a live model of the business.** Capture **entities, relationships, rules, processes** — so agents reason about **customers and orders, not tables/schemas/rows**. You can **bootstrap an ontology from existing semantic models** or build from scratch. This gives agents a **native understanding of how the organization operates**.

**Customer example:** **Q-Cells** (rendered "Guano Q cells" by captions) manages energy for **AI data centers**, a problem too dynamic/complex for humans to reason about alone. Using Fabric IQ they built an **operational model of the data center** understood by people, applications, *and* AI agents — letting agents reason about the business, recommend actions, and continuously optimize operations **while keeping human operators in control** (augmenting, not replacing, human judgment).

### Ontologies in depth (Marco's walkthrough)
Marco contrasts how *humans* vs. *agents* should consume Fabric data. Humans use **Power BI reports** built on a **semantic model** that defines table relationships (e.g. **packages ↔ drivers**, one-to-many). But you wouldn't hand Power BI reports to an agent — and a semantic model alone tells the agent the *relationships* but **not what the data *means***.

Enter the **"Generate ontology"** button in Fabric. The generated ontology *looks* like a semantic model but is fundamentally different:
- Its nodes are **business entities** (things that matter to the business), **not tables**.
- Its edges are **verbs / business relationships**, **not table joins** — e.g. *"a customer can **send** or **receive** a package; a package can be **sent to** a customer."*
- You can enrich entities with **metadata and additional semantics**, including **synonyms** — e.g. a "package" might be called a *box, case, or shipment*. The ontology **maps those natural-language words to the underlying query**, so an agent can translate human terms into correct queries.

**Consuming an ontology two ways:**
1. **Directly as an MCP server** — defining an ontology automatically exposes an **MCP server** your agents can connect to and use.
2. **Via Foundry IQ** — connect Foundry IQ to a Fabric ontology (which under the hood **also connects to that MCP server**, using the ontology as a data source).

### Context delegation & the Fabric data agent
A central design insight Marco names **"context delegation."** Every agent sits on a model with a **finite context window** — "only so much you can put in your agent's head." Querying any **structured data source** (e.g. a lakehouse) requires *tons* of context: what each data source is, its **data dictionary**, **example queries**, and **ancillary instructions** — including **tribal knowledge** in your head. His example: the acronym **SRC = "Shipping Refund Concession,"** specific to this business, that no model would know unless explicitly told.

Rather than connect the refund agent *directly* to the ontology, Marco connected it to a **Fabric data agent** — a separate agent that itself connects to **multiple data sources** (the ontology, a **lakehouse**, and others) and **holds all that heavy context** (descriptions, data dictionary, example queries, ancillary instructions like the SRC definition). The downstream agent then **doesn't keep that context in its head** — it **"phones a friend,"** calling the Fabric data agent to fetch structured data on demand. This **exports** specialized knowledge so it doesn't have to be redefined in every agent — the same **reuse** theme.

(In Marco's environment he noted ~**35 agents, 31 running**, many sharing the same grounded data sources — the concrete motivation for not redefining context per agent.)

### Work IQ — the people layer of Microsoft IQ
Back to Work IQ (which, in Act 1, was meant to turn Amanda's email into the plan that became the app). Think of it as the **people layer**: it captures **what your organization knows** — what people discuss over **email and Teams**, the data living in **M365** — and **imbues agents with that knowledge** so they understand business processes, collaboration, who's involved in a project, what's important, what decisions are already made, and what needs attention next. *The most valuable context isn't just data — it's the **people** collaborating to get work over the finish line.*

**What makes Work IQ different from the Graph / traditional APIs — three things:**
1. **Built for agents, not users.** Traditional API/Graph access was scaled to **human interactivity**; Work IQ is designed for the **speed an agentic process needs**.
2. **Built around organizational context, not raw data.**
3. **Built on top of your existing security model — not a copy of it.** Work IQ data **stays in your M365 tenant**. Developers **don't** build their own indexing systems, extract M365 data, build retrieval pipelines, or build a governance layer — Work IQ provides that foundation **out of the box**, so agents just get the work done.

**Four capabilities Work IQ unifies into a single intelligence layer:**
- **Chat** — agents interact with people *and other agents* (the conversational, agent-to-agent collaboration you'd get in Microsoft Copilot).
- **Context** — grounded understanding of what's happening across the org, drawn from **emails, meetings, Teams chats, documents, conversations, workflows** — without developers building their own retrieval/orchestration/index.
- **Tools** — a simplified, **governed** way for agents to **retrieve** information *and* **take action as the user would** in M365 (send an email, send a message), usable via any agent-friendly service.
- **Workspaces** — a **persistent place for agents to work** and store **intermediate work product**. As agents take on **longer-running tasks**, they must maintain **state** and share progress across phases with other agents or with humans.

Together these give agents the **same organizational context an employee has**.

**Partner example:** **Mural** (captions: "Maro") integrates Work IQ so M365 context flows **directly into its collaborative canvas** — no copy/paste, no disconnected tools, no stale snapshots; documents, conversations, people, and decisions are shared seamlessly **from M365 into Mural and back**.

### Agent identity & A365 — instantiating "my agent"
The finale (once the network returned). The standalone, anonymous refund agent from the start **isn't how it ended up**. The agent definition became a **blueprint in A365**, which in turn became an **agent template**.

**What an agent template is:** a template **by itself is not an agent**. Any user can go into **Teams** and **create an instance** of the template — and instantiation is what creates *an* agent. Marco emphasizes: he didn't just create *an* agent, he created **"my agent."** Each instance gets:
- Its **own identity**.
- An entry in the **org chart**, with a **reporting line** (Marco's refund-processor agent **reports to Marco**, who reports to Amanda Silver).
- Its **own Teams presence** and **own inbox**.

**It works end-to-end:** Marco had forwarded the agent an email from **"Maria Garcia"** about a package that hadn't arrived — delegating that work. The agent **checked its own inbox**, and **emailed Maria back (cc'ing Marco)** — apologizing it couldn't locate the package (network gremlins) but proving it could **read and send email under its own identity**. The mechanism: **Work IQ as the agent-facing, "headless" version of Outlook, Teams, SharePoint, and Word.**

**On-behalf-of vs. own-identity (a key governance point):**
- When Work IQ acts **"as me"** (e.g. Copilot CLI checking my email), it **inherits all my rights and permissions** — it can do anything I can.
- When you create an **agent instance** ("autopilot agent"), you give it its **own security/permission space** — e.g. *can send/receive email but can't write Word docs*, or *can only draft emails, not send them*. You can grant a **different, narrower** set of permissions than your own, **limiting what the agent can do**. Either way, it interacts with the world **via Work IQ**.

### Closing synthesis
Once back online, they replayed the highlights as a synopsis:
- **Web IQ** finally answered the **Sandy Fire** query (a real event burning ~400 miles south, near Simi Valley) in a couple of seconds — grounding the agent in **real-time world data**.
- **Foundry IQ** provided governed enterprise knowledge retrieval.
- **Fabric data agent** held all the structured-query context (data sources, descriptions, data dictionary, example queries, ancillary instructions, the **SRC** acronym) so downstream agents didn't have to.
- **Work IQ** let the agent **read and send its own email**.
- The agent was given an **addressable org-chart identity** so people could **email it and interact in Teams** — critical because end users live in M365/Teams, not technical UIs.

**The thesis restated:** the future isn't filling agents with *more* information (that makes them **expensive** to operate) — it's giving them the **right context** to make the **best decision with the minimum information at the highest confidence**. **Intelligence makes agents useful; trust makes them deployable.** Every layer of Microsoft IQ is built on the **same foundation of identity, governance, and security** — agents are **permission-aware by default**, every action is **traceable and explainable**, and policies are **applied consistently** across the ecosystem. The real challenge isn't one agent in a smart environment — it's **building and governing thousands**, in a unified (not bespoke) way, so you can trust and deploy them without monitoring each one individually.

### Getting started (call to action)
- Everything shown is **available to start building now**.
- **Hands-on lab** going deep on all the IQs.
- Visit the **booth**; join the discussion on **GitHub**.
- **Agents League hackathon** — a chance to build with everything shown, from creative applications to autonomous agents to enterprise-grade systems. ("Don't just imagine what's possible — go build it.")
- Both speakers stress they deliberately do **live demos** (not canned screenshots) for developers — and ask forgiveness for the rough network ride.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft IQ** — umbrella "context layer for the agentic web"; unifies four context sources (Work/Fabric/Foundry/Web IQ) on a shared identity/governance/security foundation.
- **Work IQ** — the *people layer*; agent-facing "headless" version of Outlook/Teams/SharePoint/Word that gives agents M365 organizational context and the ability to act as the user. Capabilities: Chat, Context, Tools, Workspaces.
- **Fabric IQ** — real-time *business knowledge* layer (OneLake + semantic models + ontologies) so agents reason over business context, not raw data.
- **Foundry IQ** — unified, governed *enterprise knowledge* layer doing **agentic retrieval** (really a retry/rerank sub-agent), reusable across agents.
- **Web IQ** — real-time, multimodal (web/news/images/video) **grounding platform** (not a search API) with citation-ready results, sub-200ms P95 latency, passage-level ranking.
- **Azure AI Foundry** ("Foundry") — where the refund agent is defined/inspected and grounded in all four IQs.
- **Copilot CLI** — command-line Copilot (with a voice mode) used with Work IQ installed to find the email and draft the agent spec; also referenced as "GitHub CLI" in the closing retry.
- **Microsoft 365 Copilot (M365 Copilot)** — shows a "Work IQ" indicator when looking up your email; the consumer-facing parallel to what the agent does.
- **OneLake** — single unified analytical + operational data layer (Fabric) across systems/clouds without moving/duplicating data; the source of truth for agents.
- **Semantic models** — define business metrics/relationships; reusable straight from **Power BI**; give agents the same answers as dashboards.
- **Ontologies** — live model of the business (entities + verb relationships + rules/synonyms/metadata); bootstrap-able from semantic models; map natural language to queries.
- **"Generate ontology"** — Fabric feature/button that scaffolds an ontology from a semantic model.
- **Fabric data agent** — a separate agent connecting to multiple sources (ontology, lakehouse, etc.) that holds heavy structured-query context for **context delegation**.
- **Lakehouse** — a structured data source the Fabric data agent connects to (requires data dictionary, example queries, etc.).
- **MCP (Model Context Protocol) server** — every defined ontology is automatically exposed as an MCP server agents can connect to; Foundry IQ connects to ontologies via this.
- **Power BI** — where most teams already define semantic models/reports; Fabric IQ picks these up directly.
- **A365 (Agent 365)** — platform where an agent definition becomes a **blueprint → agent template** that users instantiate in Teams with identity, inbox, org-chart entry, and scoped permissions.
- **Microsoft Teams** — where users instantiate agent templates and interact with their agent (each instance gets its own Teams presence).
- **Foundry IQ serverless developer tier** — new low-friction entry point to start building (see Announcements).
- **Agents League hackathon** — Build hackathon to build with the IQs.

## 🚀 Announcements / What's New
- **Foundry IQ serverless developer tier** — *introduced in this session* ("today we're actually introducing"); an easy, low-friction way for every developer to start building with Foundry IQ and **scale to production** when ready.
- **Web IQ availability** — described as **available today to a few Azure customers** (limited availability), already used by frontier model providers and enterprises (e.g. NASDAQ Board Vantage).
- **Microsoft IQ / Work IQ / Fabric IQ / Foundry IQ** — presented as the unified context layer; speakers state **"everything you saw today is available for you to start building now"** (specific GA/preview status per component not individually called out beyond Web IQ's limited availability and the new Foundry IQ serverless tier).
- **A365 agent identity / agent templates** — agents getting their own identity, inbox, org-chart reporting line, and scoped permissions, instantiable from Teams, shown as a current capability.
- **Agents League hackathon** — promoted as the venue to build everything shown.
- *(No explicit dated GA milestones or version numbers were stated beyond the above.)*

## 💡 Demos
The entire session is one continuous **"refund processor" agent** built from a single email, grounded across all four IQs. Notably, the **network failed catastrophically mid-session** (later traced to **GlobalProtect VPN** silently blocking traffic — "it was globally protecting you all from seeing my demos"; an audience member tipped Marco off). Marco had pre-loaded/cached fallbacks; most live pieces eventually worked once the VPN was disabled.

- **Email → spec in Copilot CLI (Work IQ).** Asked Copilot CLI (Work IQ installed, voice mode) to find Amanda's email and draft a plan/spec for the refund agent. *Point:* Work IQ logs in **on your behalf** to retrieve M365 content; an email with no spec/design doc can become a buildable plan. (Hit a transient/network error live; later **retried successfully** at the very end and *did* find the email.)
- **The built agent in Foundry.** Showed the polished front end and the same agent in **Azure AI Foundry**, grounded in **all four IQs**. *Point:* one agent, unified context.
- **Web IQ grounding (Sandy Fire).** Asked the package/refund agent about the **Sandy Fire** (real event ~400 mi south near Simi Valley). *Point:* ground agents in **real-time world data** in a couple of seconds (succeeded once the network returned).
- **Foundry IQ reuse.** Showed Foundry IQ connected to many data sources across ~**35 agents (31 running)**. *Point:* a Foundry IQ "knowledge base" is really an **agentic-retrieval sub-agent** (retry + rerank); define grounding once, **reuse across many agents** instead of redefining per agent.
- **Fabric: semantic model → ontology.** Showed packages↔drivers semantic model (one-to-many), the **"Generate ontology"** button, and a built ontology where nodes are **business entities** and edges are **verbs** (customer *sends/receives* package), plus **synonyms** (box/case/shipment). *Point:* ontologies give agents **meaning**, not just table relationships; expose as **MCP server**.
- **Fabric data agent / context delegation.** Showed (conceptually, network-permitting) a Fabric data agent connected to the ontology + a lakehouse holding rich context — data dictionary, example queries, ancillary instructions, and the business acronym **SRC = Shipping Refund Concession**. *Point:* **"phone a friend"** — offload heavy structured-query context to one data agent so downstream agents stay lean.
- **Agent identity (A365).** Fired up the **refund processor agent instance**: its **own identity**, **org-chart entry reporting to Marco** (→ Amanda), **own inbox + Teams box**. It had been forwarded an email from **Maria Garcia** (missing package), **checked its own inbox**, and **emailed Maria back, cc'ing Marco**. *Point:* agents become addressable "employees" with **scoped permissions** (e.g. draft-not-send), interacting with the world via **Work IQ**.

## 📊 Notable Stats / Quotes
- **">40% of agentic AI projects are expected to fail"** — and the cause is missing context, not model capability.
- **Sub-200ms P95 grounding** latency for Web IQ.
- **Passage-level ranking** in Web IQ to cut token consumption/cost.
- Marco's environment: **~35 agents, 31 currently running**, many sharing the same grounded data sources (the motivation for reuse).
- **SRC = "Shipping Refund Concession"** — example of business-specific tribal knowledge a model can't know unless told.
- **Sandy Fire** burning **~400 miles south**, near **Simi Valley** — the real-time Web IQ grounding example.
- *"The difference between welcoming a brand-new employee to the team versus somebody who's actually a seasoned employee."* — the recurring analogy for infusing agents with context.
- *"It's not a traditional search API … it's actually a grounding platform built specifically for the needs of modern agentic systems."* — on Web IQ.
- *"It calls the fabric data agent to get that data."* — on context delegation ("phones a friend").
- *"This intelligence is what makes the agents useful, and it's the trust that makes them deployable."* — the closing thesis.
- *"It was globally protecting you all from seeing my demos."* — Marco, on the GlobalProtect VPN that killed the live network (the catastrophic-demo moment).
- *"The challenge isn't really just building a single agent … it's actually building thousands of them"* — why governance/consistency matters.
- Customers named: **NASDAQ** (Board Vantage), **Sitecore**, **Q-Cells** (AI data-center energy management), **Mural** (Work IQ canvas integration).

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Spin up a **Foundry IQ serverless developer tier** knowledge base and connect it to a couple of agents to see the reuse/agentic-retrieval pattern firsthand.
- [ ] Things to try: In Fabric, take an existing **Power BI semantic model** and hit **"Generate ontology"** — inspect the entity/verb model and add synonyms/metadata; expose it as an **MCP server** and connect an agent.
- [ ] Things to try: Prototype **context delegation** — a single **Fabric data agent** fronting a lakehouse (with data dictionary + example queries + business acronyms) that downstream agents call, vs. cramming context into each agent.
- [ ] Things to try: Test **Work IQ** on-behalf-of vs. an **A365 agent instance** with **scoped permissions** (e.g. draft-but-not-send) and an org-chart identity.
- [ ] Questions: What's the actual GA/preview status and pricing of each IQ (esp. Web IQ limited availability and the Foundry IQ serverless tier)? Which regions?
- [ ] Questions: How does Work IQ's permission/identity model for autopilot agents map to existing Entra/M365 governance and audit?
- [ ] Questions: How do ontologies handle drift when underlying semantic models/schemas change? Re-generate, or incremental?
- [ ] Questions: What are the cost implications of agentic retrieval (retry/rerank sub-agents) at scale vs. plain RAG?
- [ ] Relevant to: Azure AI Foundry agent builds; Fabric/OneLake data-grounding work; any internal "agent that needs enterprise + real-time + people context" scenario; MCP-based tool/data integrations.

## 🔗 Related
- [[2026 Build Session List]]
- Microsoft Build 2026 — Azure AI Foundry / Microsoft IQ sessions
- Topics: Fabric IQ · Foundry IQ · Work IQ · Web IQ · OneLake · ontologies · MCP · A365 agent identity
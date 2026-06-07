---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/enterprise
  - topic/data
  - topic/case-study
source: https://www.youtube.com/watch?v=jlzlk_vh4r8
session_code: BRK224
event: Microsoft Build 2026
speakers: Bob Ward (Microsoft), Rishab Saha (Microsoft), Kunal Patel (PepsiCo)
duration_min: 42
aliases:
  - PepsiCo's blueprint for agentic AI
  - BRK224
  - CAM 360
---

# BRK224 — PepsiCo's blueprint for agentic AI

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:**  
> • **Bob Ward** — Principal Architect, Azure Data team, Microsoft (opening / data foundations)  
> • **Rishab Saha** — Chief Architect, Microsoft Office of the CTO  
> • **Kunal Patel** — Senior Manager, AI Solutions & Platforms team, PepsiCo  
> **Duration:** ~42 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=jlzlk_vh4r8)

## 🎯 TL;DR
PepsiCo and Microsoft walk through how they built **CAM 360**, a production multi-agent system that transforms a Key Account Manager's (KAM) meeting-prep workflow "from chaos to clarity." The core thesis: **you cannot build reliable agents on bad data** — everything rests on PepsiCo's pre-existing **Enterprise Data Foundation (EDF)**, evolving from "data for dashboards" to "data for agents." The solution uses six specialised agents (orchestrator + five specialists) built on Azure Databricks, Microsoft Fabric, Foundry IQ, Cosmos DB, LangGraph/LangSmith, and Databricks Genie (text-to-SQL). Two agents are deep-dived: a **Data Analyst agent** (Genie-powered NL→SQL with Unity Catalog governance and confidence-path routing) and a **Tracking agent** (a "compounding intelligence" learning loop that turns tribal knowledge into an institutional fact ledger). The payoff: a KAM named "Priya" goes from hours across 6–10 systems to a single question — *"Help me get prepared"* — and gets buyer signals, risks, talking points, and a draft strategy in minutes. The closing message: agents aren't to replace people, but to give time back so they can be human.

## 🔑 Key Takeaways
- **Data foundation is non-negotiable** — "Just like we cannot build a skyscraper on sand, it's very difficult to build agents if your data is inconsistent, not governed, or not meaningful." The hard, slow part was the foundation; once built, later agents came an order of magnitude faster.
- **Evolve "data for dashboards" → "data for agents."** Today's pipelines feed dashboards where humans interpret insights and apply manual rules; the target is a **connected knowledge graph / common knowledge layer** agents can reason and act on (insights → automation).
- **AI-ready data must solve 5 things simultaneously:** real-time, unified, meaningful, contextual, and trusted — individually hard, and "way harder" at PepsiCo scale.
- **EDF is a metadata-first foundation** built on common-sense principles: DevOps + governance, standardized industry data models (harmonized across functions/markets), reusable modules, and central observability.
- **CAM 360 is a multi-agent system of six:** an **Orchestrator** ("smart project manager") plus **Data Analyst** (the "nerd"), **Persona Intact**, **Tracking**, **Best Practices** (run-book enforcer), and **Debrief** (live conversational agent that fills knowledge gaps by asking the user questions).
- **Data Analyst agent = hybrid pipeline:** Authentication → Query (Genie) → Enrich/Persist. Auth converts **JWT → OIDC** via a Databricks federation policy; Genie does text-to-SQL; enrich layer stores knowledge + session memory.
- **Databricks Genie accuracy comes from configuration**, not luck — curated tables, full column/definition metadata, serverless warehouse for speed, formatting assistant, system instructions, one-shot examples, and a **golden dataset** of real user questions.
- **Confidence-path routing:** high-confidence queries map to **pre-validated static SQL** (instant); low-confidence queries generate SQL on the fly. The golden dataset / high-confidence paths were mined from **dev-cycle usage logs**.
- **Unity Catalog enforces row/table-level access** so agents never expose data the user isn't entitled to (e.g. user sees 2–3 of 10 configured tables).
- **Tracking agent delivers "compounding intelligence."** Three components: **Learning module** (configurable categories like pricing/escalation), **Enterprise Knowledge layer** (extracts tribal knowledge → shared memory), and a **Fact Builder agent** (turns signals + knowledge into factual statements with confidence scores).
- **Foundry IQ powers agentic RAG / agentic retrieval** — knowledge sources (indexes, federated remote MCP servers, remote SharePoint, etc.) plus tunable "knobs": retrieval instructions, planning model (chat completions), and reasoning effort. Solves a very hard problem with minimal implementation effort.
- **Agents share a Core Agent Runtime abstraction** built on the **Responses API** with tool-calling abstracted away — the Fact Builder and Tracking agents reuse the same runtime, just with different tools (e.g. `search facts`, `list retailers`).
- **Observability is first-class** — OpenTelemetry (OTLP) standards monitor everything the agents do; LangSmith provides node-by-node trace visibility.
- **Hard-won lessons:** *Don't boil the ocean* (start with one workflow / one person / one data source — "if you think you're starting small, start smaller"); they **underestimated data quality** because agents "confidently hallucinate," especially when answers are partly right; **involve domain experts from day one**.
- **The blueprint generalizes beyond Pepsi:** Secure infrastructure → unify & govern data → AI platform (models/agents) → user-experience layer. Agents, data, and UX vary by industry/role, but the building blocks stay consistent.
- **Purpose framing:** the goal is *not* to replace people — it's to give time back so KAMs can "think, strategize, and actually be human."

## 📚 Detailed Notes

### 1. Opening — Bob Ward on the data journey (the "foundation" pitch)
Bob Ward (Principal Architect, Azure Data team) frames the session around customer success rather than product announcements. His thesis, backed by Gartner research: **without the right data infrastructure — secure, quality, governed data — AI projects are "doomed to fail."** Many have started and failed for exactly this reason.

**The starting line (the "before" diagram):** a tangle of arrows and silos — data sprawl, many copies of data, manual file transfers, floating pipelines. Consequences:
- **Inefficiency** — no one actually knows where the data is.
- **Limited interoperability** — costly manual transfers and copies.
- **Exposure / security risk** — ungoverned, scattered data is hard to secure; the biggest pain.
- **Vendor sprawl** — data sprawl drags in multiple vendors with different subscriptions, versions, and policies to track.

**The finish line ("Nirvana"):** multiple organizations/teams working on different tasks but off a **centralized, unified data platform** — typically a **lakehouse / lake-based** approach. Many data sources may still exist, but they're well-integrated into the lake, yielding strong governance, security, and tighter AI-model integration. The two products called out for this: **Microsoft Fabric** and **Azure Databricks**.

**The journey checklist** (how to reach the finish line):
1. **Unify your data** — hard and slow historically, but easier with Fabric/Databricks.
2. **Make data AI-ready** — curated, secure, high quality. Unification alone isn't enough; un-ready data still blocks success.
3. **Bring in AI models** — use popular existing models or fine-tune; you need a platform that offers **choice of models per business need**.
4. **Build the right solution** — simple chat agents vs. complex agents, fit to the business (foreshadowing PepsiCo's choices).

**Developer tooling map** Bob lays out:
- **Low-code:** Copilot Studio.
- **Rich dev experience:** Visual Studio + VS Code + GitHub Copilot.
- **Model hosting:** **Foundry** — described from personal experience as superior for getting quality models with choice (small or large), vs. trying to deploy models on-prem.
- **App hosting:** Kubernetes, Azure Container Services, Static Web Apps.
- **Databases:** rich Azure database choice (below).
- **Unifying layer:** Databricks + Fabric, providing resiliency, governance, security.
- **Edge:** **Foundry Local** for edge-scenario AI models.

**Azure database lineup (several used by PepsiCo):** Azure SQL (incl. **Hyperscale**, based on SQL Server), Azure Database for PostgreSQL, **Cosmos DB** (NoSQL), the newly announced **Horizon DB** (PostgreSQL-compatible, cloud-scaled), and MySQL. Common traits: **scale** (Azure backbone), **transactions** (relational, plus Cosmos as transactional NoSQL → supports OLTP for AI systems), and **integrated vector support** for rich search tightly tied to Foundry, plus easy **mirroring into Fabric** for the lake approach.

**This week's database announcements (per Bob):** Cosmos DB **semantic re-ranking** (popular with the Cosmos community; PepsiCo uses Cosmos); Azure SQL / Hyperscale **deep GitHub Copilot integration in VS Code**; and the **public preview of Horizon DB** (announced "yesterday") for Postgres compatibility at cloud scale.

Bob hands off to **Rishab Saha (Microsoft)** and **Kunal Patel (PepsiCo)**.

### 2. The PepsiCo problem — scale creates complexity, complexity creates pain
Rishab reframes from "product story" to "**people story**" — specifically the **Key Account Manager (KAM)** and how the team took their Monday morning "from chaos to clarity."

**PepsiCo's scale:** 300,000+ employees, products enjoyed in 200+ countries, **23+ billion-dollar brands**. (Kunal's joke: the only "unlimited" thing at PepsiCo is *complexity and scale*.) This scale creates complexity, and complexity creates pain for the people closest to PepsiCo's largest customers.

**Who is a KAM?** A senior sales professional managing PepsiCo's largest retail customers ("the who's who of retailers") — relationships driving **multi-million-dollar revenue**.

**The "before" pain (Monday morning, meeting in 48 hours):**
- **Fragmented information** — multiple reports, multiple dashboards, context buried in emails.
- Constant uncertainty: *Do I have current data? The latest context?*
- The KAM's true competency is **strategizing the customer conversation**, but they burn hours on data-gathering hurdles before they can even start.

### 3. The vision — one workflow, one source of truth, a system that learns
Kunal describes the target state:
- Account plans and **account health in one singular workflow**.
- A **single trusted data source** — no hopping across silos, compiling, and validating with different people.
- A **learning system that compounds over time** — it doesn't need to be constantly fed; it learns on its own.

### 4. Foundation first — the Enterprise Data Foundation (EDF)
Rishab: in relationship businesses, learnings become **tribal knowledge** trapped in one person managing huge relationships and information. But before solving that, **the foundation comes first** ("can't build a skyscraper on sand").

**EDF design principles (common-sense, per Rishab):**
- **DevOps + governance** in place.
- **Standardized industry data models** so data is **harmonized** across business functions and markets.
- **Reusable modules** so every team isn't solving the same thing differently.
- **Central observability** — how the system learns, evolves, and adapts.

PepsiCo had already invested heavily and had the **EDF well baked in**.

### 5. From "data for dashboards" → "data for agents"
Kunal explains the evolution:
- **Today:** pipelines serve dashboards; **humans interpret insights**; **actions taken via manual rules**.
- **Target:** a **connected knowledge graph** forming a **common knowledge layer** that sits on top of multiple fragmented data sources; agents can **reason on it, decide, and take action** → **insights to automation**.
- EDF is the **metadata-first foundation**. On top: **data as knowledge** (disconnected entities brought together), **data as intelligence** (agents reason through / drill deeper), then the **agent layer**. The concept: make **AI-ready data** to generate more business value.

**The 5 requirements for AI-ready data** (all must hold simultaneously):
1. **Real-time** — agents are very latency-sensitive.
2. **Unified** — complex workflows touch many parts of the business.
3. **Meaningful** — business context, meanings, and processes captured.
4. **Contextual** — agents work best with the right context at the right time.
5. **Trusted** — everything above is meaningless without trust.

Enabled by Azure Databricks, Microsoft Fabric, and enterprise databases (SQL, Cosmos DB) — but still requiring **intentional architectural decisions**. Rishab's recurring point as chief architect: **the operating model must also evolve**.

### 6. Production-ready components
Rishab notes the full component slide (to be shared post-build). Key framing: individually the products aren't the headline — the highlight is that **every component was used in a production-ready way**, since this is a **multi-agent system** spanning different teams, developers, and components.

### 7. Meet Priya — the CAM 360 agent
A concrete persona: **Priya**, a KAM with a meeting in **48 hours** with one of her largest retail customers. Before: 6/7/10 systems, reports, emails, buried docs — hours of prep. After: she opens **CAM 360** and asks *"Help me get prepared."*

**Priya's "six superstars" (the agent team):**
1. **Orchestrator** — the "really smart project manager"; orchestrates everything across the board.
2. **Data Analyst agent** (the "nerd") — crunches data, goes through the numbers.
3. **Persona Intact agent** — ensures account personas are captured well and that strategies built on top are followed.
4. **Tracking agent** — manages the account lifecycle and keeps things on track.
5. **Best Practices agent** — enforces PepsiCo's success run-book at scale.
6. **Debrief agent** (Kunal's favorite) — a **live conversational agent**; when the knowledge layer has gaps, it generates a question, asks Priya, captures her answer into the knowledge layer → better account understanding next time.

So effectively **every KAM gets a team of six working with them all the time.**

### 8. Deep dive — Data Analyst agent (NL → SQL via Genie)
A **hybrid system** with layers: **Authentication → Query (Genie) → Enrich/Persist**.
- **Authentication:** enforces user access — if a user lacks access to specific data, the agent doesn't traverse or read it. Converts tokens **JWT → OIDC** using a **federation policy configured in the Databricks/Genie database**, tracked per session.
- **Genie ("the heart"):** performs **text-to-SQL** generation, executes, and returns responses. Conversation IDs and Genie request IDs are tracked through the session; the response provides a **summarized output and the SQL**.
- **Enrich & Persist:** stores the knowledge layer and session memories, making synthesis easy.

**LangGraph / LangSmith demo (see Demos):** a graph with the orchestrator (project manager) at the center. A query comes in → authentication & token conversion (JWT→OIDC) → Genie call (conversation tracking) → response (summary + SQL) → orchestrator **synthesizes**, checking against a **golden dataset** before answering. VS Code shows the **node-by-node graph** and each step.

**Databricks Genie configuration (why SQL is accurate):**
- All needed **tables created and configured** in Genie.
- A **serverless ("no-server") warehouse** for speed.
- Full **table definitions and column details** captured so Genie understands the data and generates more accurate SQL (vs. trial-and-error).
- A **formatting assistant** ensures correct output formatting.
- **Unity Catalog** governs access — even with 10 tables configured, a user may only access 2–3; agents must not answer from restricted data.
- **System instructions** and **one-shot examples** configured for the agent.
- **Confidence paths:** **high-confidence** queries → pre-configured **static SQL** (instant); **low-confidence** queries → SQL generated on the fly. High-confidence paths were mined from a **golden dataset** built from **dev-cycle usage logs** (capturing how users actually query and what common questions they ask).

**Three takeaways Rishab calls out from the walkthrough:**
1. Priya started with just an **intent** — she didn't need to know where the data/knowledge lived.
2. That intent translated into an accurate SQL query **because of the EDF** groundwork.
3. The system doesn't just summarize — it gives Priya the **variables she needs** to make her customer conversation meaningful.

### 9. Deep dive — Tracking agent ("compounding intelligence")
Story moves forward: Priya had a great meeting (Thursday). In the old cycle, Thursday evening she'd scribble notes in her car, send an email, or promise to update the account plan "later" — context easily lost, and even when captured it **never became institutional memory**. The Tracking agent extends prep work into a **learning system**.

**Three components:**
1. **Learning module** — lets you create **configurable categories** the system continuously learns about (e.g. **pricing**, **escalation**, any parameter). A **signal** example tracks pricing info with **hints** and an **extraction prompt** for downstream agents, plus optional **metadata fields** (for knowledge sources/bases) stored in **Cosmos DB**.
2. **Enterprise Knowledge layer** — extracts the **tribal knowledge** from Priya's memory and makes it available to the whole account team and successors. Powered by **Foundry IQ** (agentic RAG / agentic retrieval): **knowledge sources** = indexes or federated sources (remote **MCP servers**, remote **SharePoint**, etc.) constantly ingested and reasoned over. The **knowledge base** exposes tunable **knobs**: **retrieval instructions**, **planning mechanism** (configure a **chat-completions model** to plan), and **reasoning effort**. Rishab stresses this is simple to implement but would be very hard to hand-build at scale (cross-references **Pablo's earlier session** on Foundry IQ).
3. **Fact Builder agent** — converts **signals + knowledge sources/bases** into **facts / factual statements**. Built on a **Core Agent Runtime** (an abstracted agent reusable by multiple agents), uses the **Responses API** with **tool-calling abstracted away**, plus a configured **system prompt**. Output example (pricing): an email found in a knowledge source is summarized, yielding an **extraction summary** (e.g. *"this customer had requested a blanket 7% increase"*), a **confidence score**, **stakeholders**, **confidence reason**, and additional extracted data.

**The Tracking agent itself** is the **conversational interface** that only talks to the **fact ledger** — the only thing a CAM interacts with. The learning, enterprise-knowledge, and compounding-intelligence work all run **behind the scenes on a schedule**. Built on the **same Core Agent Runtime** as the Fact Builder, with extra tools like **`search facts`** and **`list retailers`**; it reads from **Cosmos DB** and returns the right facts based on question intent. **Observability** via **OpenTelemetry (OTLP)** monitors everything.

**User experience:** ask an intent (e.g. *"What was the last offer for ABC?"* — ABC being a dummy company) → in minutes Priya gets the answer pulled from learning configs, the enterprise knowledge layer, and generated facts.

**Compounding intelligence summary:** every past meeting (once stuck in memory) now makes the system smarter; every debrief improves planning for the next account cycle; every future CAM benefits from prior context — no reinventing the wheel.

### 10. Lessons learned (the honest part)
- **Don't boil the ocean** — keep scope small. "If you think you're starting small, start smaller." Start with **one workflow, one person, one data source**, then build on top.
- **Don't underestimate data quality** — even with strong foundations they underestimated it. Agents are good at **confidently hallucinating**, especially when answers are **partly right and partly wrong**, which non-domain-expert engineers struggle to catch. **Involve domain experts from day one.**
- **The EDF was the best part** — the data foundation played a pivotal role; agents not only worked but **compounded value** (e.g. debrief agents made subsequent sessions better). The first couple of agents were hard; the **next 3–5 were an order of magnitude faster** once foundations existed — "like climbing a hill."

### 11. The generalizable blueprint
Beyond PepsiCo, **enterprise AI at scale** looks like:
1. **Secure infrastructure** (start here).
2. **Unify & govern your data** on top.
3. **AI platform** ready — where models/agents reside, operate, and run.
4. **User-experience layer** — where agents interact with humans.

Agents change by industry, data evolves by company, UX changes by role — but the **building blocks stay consistent**.

**Resources mentioned:** free Azure resources for non-customers; **Azure Accelerate** (trusted experts — a program PepsiCo and Microsoft partnered on); **Cloud Accelerate Factory**; a post-session **survey**. All slides/resources available after the session.

### 12. Closing — give time back to people
Return to the opening image: a single CAM, Monday morning, meeting in 48 hours. **Before:** hours hunting for the right information across dashboards, reports, emails, and teammates. **Now:** open **CAM 360**, ask *"Help me get prepared,"* and within **minutes** (not hours/days/weeks) get **buyer signals, data, risks, talking points, even a draft strategy** — with time left to think and strategize. The purpose: **not to replace people** but to **give time back** so they can "think, strategize, and actually be human."

## 🛠️ Products / Features / Technologies Mentioned
- **CAM 360** — PepsiCo's multi-agent meeting-prep system for Key Account Managers (the central solution).
- **Microsoft Fabric** — unified analytics/lakehouse platform for unifying & governing data.
- **Azure Databricks** — lakehouse data platform; hosts Genie, Unity Catalog, serverless warehouses.
- **Databricks Genie** — natural-language-to-SQL engine; "the heart" of the Data Analyst agent.
- **Unity Catalog** — Databricks governance enforcing table/row-level access control for agents.
- **Azure AI Foundry** — model hosting platform offering broad model choice (small & large).
- **Foundry IQ** — agentic RAG / agentic retrieval service (knowledge sources + tunable retrieval/planning/reasoning knobs).
- **Foundry Local** — edge-scenario AI model hosting.
- **Azure Cosmos DB** — NoSQL database; stores signals, metadata, facts, and session/knowledge data; got semantic re-ranking this week.
- **Azure SQL Database / Hyperscale** — relational DB (SQL Server-based); deep GitHub Copilot/VS Code integration announced.
- **Azure Database for PostgreSQL** — managed Postgres option.
- **Horizon DB** — new PostgreSQL-compatible, cloud-scaled database (public preview).
- **Azure Database for MySQL** — managed MySQL option.
- **Responses API** — standardized agent API underpinning the Core Agent Runtime (tool-calling abstracted).
- **Core Agent Runtime** — PepsiCo's reusable agent abstraction shared across Fact Builder & Tracking agents.
- **LangGraph** — graph-based agent orchestration framework used for the agent flows.
- **LangSmith** — observability/tracing UI for inspecting the LangGraph flow node-by-node.
- **OpenTelemetry (OTLP)** — open-standard protocol used for agent observability/monitoring.
- **MCP servers (remote)** — federated knowledge sources for Foundry IQ.
- **Remote SharePoint** — another federated knowledge source for Foundry IQ.
- **Copilot Studio** — low-code agent-building tool (developer tooling option).
- **Visual Studio / VS Code / GitHub Copilot** — rich pro-developer toolchain.
- **Azure Kubernetes / Container Services / Static Web Apps** — application hosting options.
- **Enterprise Data Foundation (EDF)** — PepsiCo's metadata-first, governed, harmonized data foundation (the bedrock of the whole solution).
- **Azure Accelerate** — Microsoft program giving access to trusted experts (PepsiCo partnered on it).
- **Cloud Accelerate Factory** — Microsoft enablement program/resource.

## 🚀 Announcements / What's New
This is a customer case-study session; product news came mainly from Bob Ward's opening:
- **Horizon DB — Public Preview** *(announced this week / "yesterday")*: PostgreSQL-compatible, cloud-scaled Azure database for Postgres developers.
- **Cosmos DB — Semantic Re-ranking** *(announced this week)*: popular new retrieval capability with the Cosmos community.
- **Azure SQL / Hyperscale — deep GitHub Copilot integration in VS Code** *(announced this week)*: improved developer experience for Azure SQL.
- **Foundry IQ** *(referenced as current; deep-dived in "Pablo's" session)*: agentic RAG/retrieval with knowledge sources + tunable knobs — central to the Tracking agent.
- No CAM 360-specific product GA/preview was announced — the solution itself is a customer-built reference architecture, with the slides/components to be shared post-session.

## 💡 Demos
- **LangGraph flow in LangSmith (Data Analyst agent):** Showed a live graph with the **orchestrator/project-manager node** at the center. A demo query ("top accounts...") flows through **authentication & JWT→OIDC token conversion**, a **Genie call** (with conversation/Genie ID tracking), then **synthesis** validated against a **golden dataset** before output. **Point proved:** the end-to-end agentic NL→SQL pipeline with auth, tracing, and grounding actually works and is fully observable.
- **VS Code node-by-node graph view:** Drilled into the individual **nodes/steps** of the graph (token conversion, Genie call, response handling, orchestrator synthesis). **Point proved:** the system is transparent, debuggable, and built from inspectable, modular steps rather than a black box.
- **Databricks Genie configuration:** Showed the configured **tables, column definitions, serverless warehouse, formatting assistant, system instructions, one-shot examples, Unity Catalog access control, and high/low-confidence SQL paths** (static SQL for high-confidence; on-the-fly for low). **Point proved:** Genie's NL→SQL accuracy is engineered through rich metadata + a golden dataset — not luck — and respects per-user data governance.
- **Tracking agent — signal configuration & fact output:** Showed a **pricing signal** (hints + extraction prompt + Cosmos DB metadata fields) and the **Fact Builder output** — e.g. an extracted fact that *"this customer had requested a blanket 7% increase,"* with **confidence score, summary, stakeholders, confidence reason**. **Point proved:** tribal knowledge buried in emails/memory can be auto-converted into a queryable, trustworthy **fact ledger** (compounding intelligence).

## 📊 Notable Stats / Quotes
- **300,000+** PepsiCo employees; products in **200+** countries; **23+** billion-dollar brands.
- Customer prep window in the running example: **48 hours**; old process took **hours** across **6–10** systems → new process takes **minutes**.
- Extracted-fact example: a customer **"requested a blanket 7% increase."**
- *"The only unlimited thing we get is complexity and its scale."* — Kunal Patel (on working at PepsiCo).
- *"Just like we cannot build a skyscraper on sand, it's very difficult to build agents if your data is inconsistent... not governed properly, or... just not meaningful enough."* — Rishab Saha.
- *"Agents are very good with confidently hallucinating"* — especially when part of the answer is right and part is wrong (why domain experts are essential).
- *"If you think you're starting small, start smaller."* — on scoping agentic projects.
- *"It's not really to replace people... it's really to give time back to people so they can... think, strategize, and actually be human."* — closing message.
- Without the right data infrastructure, per Gartner, AI projects are *"kind of doomed to fail."* — Bob Ward.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Prototype a **Genie + LangGraph** NL→SQL agent with **Unity Catalog** governance and a **high/low-confidence SQL path** split driven by a golden dataset from usage logs.
  - Stand up a **Foundry IQ** knowledge base with federated **MCP / SharePoint** sources and experiment with the retrieval/planning/reasoning "knobs."
  - Build a minimal **Core Agent Runtime** on the **Responses API** and reuse it across two agents (a "fact builder" + a "conversational" agent) backed by **Cosmos DB**.
  - Wire **OpenTelemetry (OTLP)** tracing + **LangSmith** into an agent flow from day one.
- [ ] Questions:
  - What exactly is in PepsiCo's "golden dataset," and how do they keep high-confidence static SQL paths fresh as schemas/usage change?
  - How is the **connected knowledge graph / common knowledge layer** physically implemented (graph DB vs. metadata over the lakehouse)?
  - How do they evaluate/guard against the "confident hallucination" failure mode in production (eval harness, human-in-the-loop)?
  - What's the boundary between **Persona Intact** and **Best Practices** agents in practice?
- [ ] Relevant to:
  - Any enterprise pursuing **agentic AI on top of a governed data foundation** (the blueprint generalizes beyond CPG/retail).
  - Internal **NL-to-SQL / data-analyst agent** efforts and **agentic RAG** initiatives.
  - Architecture conversations about **"data for dashboards" → "data for agents"** and AI-ready data (real-time/unified/meaningful/contextual/trusted).

## 🔗 Related
- [[Build2026]] — Microsoft Build 2026 session index
- Foundry IQ deep-dive session ("Pablo's session" referenced in-talk) — find & link
- Notes on **Azure Databricks**, **Microsoft Fabric**, **Cosmos DB**, **Foundry**, **Responses API**, **LangGraph/LangSmith**
- Concept: **Enterprise Data Foundation (EDF)** / AI-ready data
- Concept: **Compounding intelligence** / agentic memory & fact ledgers

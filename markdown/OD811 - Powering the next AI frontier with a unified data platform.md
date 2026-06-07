---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/fabric
  - topic/onelake
  - topic/data-platform
  - topic/ai
source: https://www.youtube.com/watch?v=CfRuzCajbVA
session_code: OD811
event: Microsoft Build 2026
speakers: Amir Netz (Technical Fellow & CTO, Microsoft Fabric)
duration_min: 38
aliases:
  - Powering the next AI frontier with a unified data platform
---

# OD811 — Powering the next AI frontier with a unified data platform

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Amir Netz — Technical Fellow & CTO of Microsoft Fabric  
> **Duration:** ~38 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=CfRuzCajbVA)

## 🎯 TL;DR
Amir Netz frames Microsoft Fabric's Build 2026 story around a single mission: giving AI agents the same context, knowledge, and tools that human employees get, so the predicted **billion agents joining the workforce** over the next two years can be as trusted and productive as people. The vehicle is **Fabric IQ** — the "state of the business" pillar of **Microsoft IQ** (alongside Work IQ and Foundry IQ) — built via a four-step journey: **(1) unify the data estate in OneLake, (2) process & harmonize with analytical engines, (3) curate semantic knowledge with semantic models + ontologies + planning, and (4) empower AI agents** to build apps and act autonomously. The session is a dense announcement reel: GPU-accelerated Fabric Data Warehouse (8x→100x+ faster), Agent Skills for Fabric (now including Power BI report generation), Fabric Ontology + integrations, **GA of Planning in Fabric**, **public preview of Apps in Fabric** on the Rayfin SDK, and **GA of Operations Agents**. The throughline: collapse the gap between operational data, analytics, planning, and agents onto one governed foundation so AI sees the whole business instead of "looking at the world through a broken mirror."

## 🔑 Key Takeaways
- **Fabric is a >$2B ARR business (60% YoY growth)** with **35,000 customers** (excluding pure Power BI users) and **90%+ of the Fortune 500** — remarkable for a platform just over 2 years old.
- The big bet: **over a billion agents will join the workforce in the next 2 years**, shifting from chatbots/desktop apps to "real full-fledged employees" — they need the same people/process/real-time context humans get.
- **Microsoft IQ = Work IQ + Foundry IQ + Fabric IQ.** Work IQ = how each person works; Foundry IQ = institutional knowledge/SOPs; **Fabric IQ = the live state of the business** drawn from operational systems. Fabric's job is to create Fabric IQ.
- **Fabric IQ is built in 4 steps:** unify → process/harmonize → curate semantics → empower agents. The whole stack exists to build the AI's "IQ" — a full picture of what's happening in the org.
- **OneLake** is the single secure foundation: all data, open format, indexed, with lineage, sensitivity labels, and certification — plus **zero-ETL shortcuts** to bring in data already living elsewhere (Azure, AWS, GCP, Snowflake, Databricks, Postgres, Cosmos, Dataverse, on-prem, apps) "with zero effort and zero cost."
- **Newly GA shortcuts:** SAP and Oracle DB (recent), plus **SharePoint and OneDrive shortcuts announced GA today**. **Public preview:** Dremio, Azure DB for MySQL. **Coming soon:** Azure Monitor, AWS Glue (joins observability data with business data).
- **GPU-accelerated Fabric Data Warehouse (limited preview)** — query accelerator via GPUs delivering **~8x single-query**, **~25x at 16 concurrent queries**, and **>100x at 64 concurrent queries** vs today's CPU warehouse; one-click enable per workspace. Based on a **SIGMOD Best Paper**-winning technique.
- **Agent Skills for Fabric** moves development from manually crafting artifacts to agent-based "live coding" — skills encode Fabric best practices for analytical engines, and **now extend to generating Power BI reports** (built on the FabCon release from 3 months ago).
- **Semantics bridge data → meaning:** **Semantic models** (20M+ in daily use, ~90% of the world's are Power BI-based) carry business metrics + row/column-level security; **Ontologies** go further, modeling business *processes* (entities, properties, real-time feeds, actions, goals, policies) so agents can *participate* in operations.
- **Fabric Ontology** has new integrations across **Foundry, Palantir Studio, and Agent 365**; still pre-GA/preview, with **GA targeted later this year**.
- **Planning in Fabric is now Generally Available** (was public preview 3 months ago), rolling out to remaining regions over the next couple of weeks — a fully Fabric-native enterprise planning tool (budgets, forecasts, scenarios, targets) with write-back to Fabric SQL and OneLake integration.
- **Apps in Fabric (public preview, first time shown):** production-grade agentic line-of-business apps on your governed data estate, one managed backend (functions, storage, security/auth), built on the **Rayfin SDK** (type-safe, decorator-based code optimizer for agentic dev) — a safe home for vibe-coded apps.
- **Agent-driven BI apps** extend Rayfin: build custom web dashboards/reports against semantic models via a **Power BI skill**, without rebuilding the analytics foundation.
- **Operations Agents are now Generally Available** — autonomous "virtual team members" that monitor signals and act in the background (not Q&A chatbots). New at GA: **chat-based authoring, root cause analysis, and Microsoft Teams integration**; configured entirely in natural language and grounded in the operations ontology.
- The unifying message: **one governed foundation** for operational apps, analytics, planning, and agents — eliminating data silos so AI (and humans) see the whole business, all powered by Fabric IQ, which in turn powers many agents across many roles.

## 📚 Detailed Notes

### Setting the stage: what Fabric is, and the adoption numbers
Amir Netz (Technical Fellow at Microsoft, CTO of Microsoft Fabric) opens by recapping Fabric, released "just over 2 years ago," as the unification of all of Microsoft's data services under one roof:
- **Operational databases** — SQL database and Cosmos DB (NoSQL).
- **Data Factory** — data integration.
- **Analytics** — data warehousing, data engineering, data science.
- **Real-Time Intelligence** — live event streams analyzed via **Event Houses** and acted on via the **Activator**.
- **Power BI** — "the founding father of the entire stack."
- **Copilot** — a foundational capability across the whole stack.
- **Governance** — via a catalog.
- **OneLake** — "the one place we store all your data for the enterprise."

Adoption proof points he's "incredibly thrilled" to share:
- **35,000 customers** using Fabric today — and this explicitly **excludes** people who only use Power BI; these are customers using the *other* Fabric services.
- **Over 90% of the Fortune 500** are using Fabric.
- **Over $2 billion in ARR** with **60% year-over-year growth** — "remarkable for a platform that has been around for just over 2 years."

### The thesis: a billion agents joining the workforce
"The world is changing." Microsoft predicts **over a billion agents joining the workforce over the next 2 years**. Crucially, "joining the workforce" means agents move from being mere chatbots or desktop applications to **"real full-fledged employees."**

This reframes the central question of the talk: **how do we make agents as trusted and productive as human employees?** The answer: give them the same **tools, knowledge, understanding, and context** we give human employees.

### The three buckets of employee context
Netz categorizes the context every human employee relies on — and that agents therefore also need — into three buckets:
1. **People** — every employee works in a team and must understand their teammates, how the org works, and their manager.
2. **How the organization works** — each org has its own **standard operating procedures, institutional knowledge, and way of doing things**.
3. **What's going on right now** — the most dynamic context: which orders are in flight, which support cases need resolving, the latest cost-saving initiative. The live state of the business.

### Microsoft IQ: Work IQ, Foundry IQ, Fabric IQ
To deliver this context to agents, Microsoft introduced **Microsoft IQ**, composed of three sub-IQs that map onto the three buckets above:
- **Work IQ** — how employees work: understanding each individual person, their preferences, priorities, and even their personality.
- **Foundry IQ** — curating institutional knowledge: building **knowledge bases** that define what it means to be an employee, to fulfill a specific role, the SOPs, the regulations to abide by, etc.
- **Fabric IQ** — the **state of the business**: a real-time feed of how the organization is performing right now, sourced from the org's **operational systems**.

> When Microsoft talks about Fabric in this context, they are "really talking about bringing and creating that Fabric IQ." A whole new workload — literally **called Fabric IQ** — was introduced in the last few months to create this context layer.

Netz stresses that creating Fabric IQ "is not as trivial as one can imagine" — it requires thought, work, and planning. The entire Fabric stack is reframed as the machinery for creating that IQ/context so the AI has "a full picture of everything that is going on in the organization."

### The four-step Fabric IQ journey (the spine of the session)
Everything that follows is organized as a four-step pipeline to build Fabric IQ:
1. **Unify the data estate** — bring all the data together.
2. **Process & harmonize the data** — make it match up and fit together (consistency).
3. **Create semantic knowledge** — so the AI actually understands the data's meaning.
4. **Empower AI agents** — put agents on top of the semantics.

Each step is then walked through with announcements and demos.

### Step 1 — Unify the data estate with OneLake
**OneLake** is "a single secure foundation for every workload, for every piece of data." Properties Netz emphasizes:
- One place where **all data is stored, in open format, indexed, and managed**.
- Managed **lineage**, **sensitivity labels**, and **certification** of data.

But the bigger point is that OneLake isn't *just* storage — it's a place to **bring in all the data you already have stored elsewhere**, with **zero ETL, zero effort, and zero cost**, via **shortcuts**. Organizations have data everywhere: across multiple clouds (Azure, AWS, GCP), in many databases (Dataverse, SQL, Databricks, Snowflake, Postgres, Cosmos), on-premises, and in applications/files.

**Why this matters (the "broken mirror" argument):** Data has a "terrible quality" — left to itself it **silos**: stored in different containers, platforms, and technologies, then sharded and isolated. That makes the full picture hard for humans to grasp and even harder for AI — "for the AI, when the data is sharded, it's like looking at the world through a broken mirror." OneLake creates a **single pane of glass** spanning all your data regardless of where it physically lives.

**Shortcut/source announcements (Step 1):**
- **General Availability (recent):** SAP and Oracle DB.
- **Generally Available — announced today:** **SharePoint and OneDrive shortcuts**.
- **Public preview:** Dremio, Azure DB for MySQL.
- **Coming soon:** Azure Monitor, AWS Glue — notably to bring the **observability data estate** into OneLake to join with the business data estate.

### Step 2 — Process & harmonize with analytical engines (GPU-accelerated Data Warehouse)
Once data is unified, Fabric's **analytical engines** make it work together and stay consistent — chief among them the **data warehousing engine**. The headline announcement here is the **Query Accelerator for Fabric Data Warehouse via GPUs**, in **limited preview**.

**The benchmark story (TPC-H):** comparing competitors, today's CPU-powered Fabric Data Warehouse, and the new GPU-accelerated warehouse:
- Where the industry typically celebrates **10–15% annual** warehouse performance gains, the GPU warehouse delivers an **~8x improvement** on average single-query (higher vs some competitors).
- Counter-intuitively, **performance improves under concurrency**: at **16 concurrent queries**, acceleration reaches **~25x**; you "barely notice the additional load at this scale."
- At **64 concurrent queries**, acceleration is **over 100x**. "The more you load the data warehouse, the more gains you're seeing."
- Enabling it is **one click**. The underlying technique **won Best Paper at the SIGMOD conference**. Netz calls it "a revolution."

### Step 2 (cont.) — Agent Skills for Fabric
Building a Fabric application spans many technologies — data warehouse, Spark, functions, real-time event streams, and more. Netz argues we must **move away from manually crafting/curating each artifact** toward **agent-based development** — "just like we do live coding for code."

**Agent Skills for Fabric** give agents the **expertise to work with Fabric correctly, in an optimized way, with best practices baked in**. Timeline/announcement:
- Skills for the **analytical engines** were released at **FabCon, 3 months ago**.
- **New announcement:** the skill set now expands so the agent can also **create Power BI reports** for you.

### Step 3 — Curate semantic knowledge (semantic models, ontologies, planning)
Even with all data in OneLake, it's still hard for an AI agent to understand the *meaning* of the data. **Semantics are the bridge** that lets AI understand meaning and build the IQ layer into the agentic world. On top of OneLake's data (structured, unstructured, real-time, graph — "everything you want"), Fabric layers:

**Semantic models** (familiar from Power BI):
- Where you curate information about **tables, relationships, and measures** — the foundation under every Power BI report and dashboard.
- The **bridge between business concepts and how data is stored** in OneLake.
- Scale: **20 million semantic models** are used day in, day out worldwide; Netz estimates **~90% of the world's semantic models are Power BI-based**.
- They hold business data, cover corporate metrics, and enforce access via **row-level and column-level security**.
- Great for AI answering **business-intelligence** questions.

**Ontologies** (for moving beyond BI into operational intelligence):
- Ontologies **expand semantics from reporting/analytics into explaining how the business works** — giving AI an understanding of **business processes**.
- If the AI is aware of business processes — including the **real-time feed, policies, and actions** — it can **participate** in the business process, not just report on it.
- **Fabric Ontology** was announced a few months ago; **new integrations** now span **Foundry, Palantir Studio, and Agent 365**. Still **pre-GA (preview)**, "becoming bigger and deeper and more capable" toward **GA later this year**.

**What modeling an ontology means in practice** (retail example):
- Identify the **entities** participating in the business — suppliers, shipments, inventory, stores — and define each entity's **relationships, properties, and actions**.
- Example entity **Shipment**: properties like the **SKUs shipped** and **transit status**, plus **real-time feeds** such as **cargo temperature**; and **actions** like *pause the inbound*, *request inspection*, or *re-route to a different store*.
- The ontology also encodes **business goals, objectives, risk & compliance handling, profitability goals, customer satisfaction, and policies**.

**The three temporal layers an ontology can model:**
- **What happened** — history of all transactions from all systems of record (from **OneLake**).
- **What's happening now** — live telemetry/IoT/sensor reads (from **Real-Time Intelligence event streams**).
- **What should happen** — the organization's forward-looking goals in great detail — which is where **Fabric Planning** comes in.

**Planning in Fabric — now Generally Available:**
- Announced ~3 months ago in **public preview**; **now GA**, rolling out to remaining regions over the next couple of weeks. Netz calls it "one of the most exciting announcements" of the session.
- Positioned as "the best enterprise planning tool on the planet" — an end-to-end enterprise planning capability to **model budgets, forecasts, scenarios, and targets**.
- **Fully Fabric-native:** integrated into the experience, the **security model**, and **OneLake**, with **write-back** to Fabric SQL — "no gap between the planning software and the data."

### Step 4 — Empower AI agents (Apps in Fabric, agent-driven BI, Operations Agents)
With data unified, harmonized, semantically curated, and forward-looking planning added, the final step is **empowering AI agents** to build applications on top of the entire governed data estate.

**Apps in Fabric — public preview (shown for the first time):**
- Create **production-grade agentic apps** running on your **governed data estate**.
- Provides **one managed backend** with everything an app needs: **functions, storage, security, and authentication** — "designed from the ground up to be secured."
- Not just analytical apps — explicitly **line-of-business applications**, and a great environment to run **vibe-coded** applications.
- Built on the **Rayfin SDK**: a **type-safe, decorator-based code optimizer for agentic development**. (Caption rendered this as "Raefin/Raven"; it is the Fabric Backend-as-a-Service **Rayfin** — see sibling note [[BRK225 - Data apps and agents the future of app dev with Rayfin]].)

**Agent-driven BI apps (extending Rayfin):**
- Semantic models are the basis for Power BI, but if you want a **custom-code web app with embedded analytics**, the next phase of agentic apps lets you build **custom web pages that visualize data based on semantic models**.
- A **Power BI skill** lets the agent **generate interactive visuals directly against your semantic models** — without rebuilding the foundation the analytics team maintains.

**Operations Agents — now Generally Available:**
- Not Q&A chatbots — they are **"virtual team members that monitor signals and react autonomously in the background."** They don't wait to be asked; they're "constantly awake," watching and taking actions.
- **Natural-language setup** — no coding required to create one.
- New capabilities at GA: **chat-based authoring, root cause analysis, and Microsoft Teams integration**.
- Grounded in the **operations ontology**, which gives the agent a **common semantic context layer** across the business, letting it inherit existing actions or use custom ones.

### Closing: one foundation, many agents
Netz recaps the full journey — unify in OneLake → process/harmonize with the engines → curate semantics with semantic models + ontologies → empower agents to build apps and operate autonomously — "all powered by **Fabric IQ**." The key amplifier: Fabric IQ (and Microsoft IQ) isn't for one agent — a **shared foundation of knowledge and semantics can span many agents performing many different roles**, empowering both agents *and* employees.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Fabric** — unified data platform spanning operational DBs, integration, analytics, real-time, BI, and governance; the subject of the talk.
- **OneLake** — single secure storage foundation; all data in open format, indexed, with lineage/sensitivity/certification; supports zero-ETL shortcuts to external sources.
- **OneLake shortcuts** — bring external data in with zero ETL/effort/cost (SAP, Oracle DB, SharePoint, OneDrive, Dremio, Azure DB for MySQL, etc.).
- **OneLake Catalog** — governance/discovery surface where every governed asset (incl. new apps) appears alongside the rest of the estate.
- **Microsoft IQ** — umbrella context framework = Work IQ + Foundry IQ + Fabric IQ.
- **Work IQ** — understands how each individual employee works (preferences, priorities, personality).
- **Foundry IQ** — curates institutional knowledge / knowledge bases / SOPs / regulations.
- **Fabric IQ** — new Fabric workload capturing the live state of the business from operational systems; the focus of this session.
- **Fabric Data Warehouse** — the data-warehousing analytical engine; now with optional GPU query acceleration.
- **Query Accelerator (GPU)** — one-click GPU acceleration for the Fabric Data Warehouse (SIGMOD Best Paper tech).
- **Spark (4.0) / Delta (4.0)** — latest Fabric data-engineering runtime shown in the agent-skills demo.
- **Custom live pools** — pre-warmed Spark pools cutting cold-start from 3–5 minutes to 3–5 seconds.
- **Agent Skills for Fabric** — encode Fabric best practices so agents can build artifacts; now includes Power BI report generation.
- **GitHub Copilot / CLI** — the agentic interface driving Fabric development in the demos.
- **AI functions** — bring LLMs into Fabric (notebook or warehouse, PySpark or T-SQL) for categorization, sentiment, classification — no config.
- **Activator** — real-time alerting/trigger engine; fires actions (e.g. Teams notification) when matching data lands.
- **Real-Time Intelligence / Event Houses / event streams** — live telemetry and streaming signals feeding ontologies.
- **Semantic models** — curated tables/relationships/measures bridging business concepts to stored data; foundation of Power BI; enforce RLS/CLS.
- **Power BI** — BI layer; "founding father" of the stack; semantic models + reports.
- **Fabric Ontology** — models entities, properties, real-time feeds, actions, goals, and policies so agents understand business processes.
- **Planning in Fabric** — Fabric-native enterprise planning (budgets/forecasts/scenarios/targets) with write-back to Fabric SQL.
- **Apps in Fabric** — production-grade agentic line-of-business apps on the governed estate with one managed backend.
- **Rayfin SDK** — type-safe, decorator-based code optimizer for agentic app development (the Fabric BaaS); powers Apps in Fabric and agent-driven BI apps.
- **Fabric SQL database** — operational SQL store that Rayfin apps provision and write into; lands data straight into the workspace/OneLake.
- **Operations Agents** — autonomous virtual team members that monitor signals and act in the background; NL-configured, ontology-grounded.
- **Microsoft Teams** — channel where Activator alerts and Operations Agents post and collaborate.
- **Foundry / Palantir Studio / Agent 365** — platforms newly integrated with Fabric Ontology.
- **Cosmos DB, SQL database, Dataverse, Databricks, Snowflake, PostgreSQL** — named data sources/databases reachable via OneLake.

## 🚀 Announcements / What's New
- **OneLake shortcuts — SharePoint & OneDrive: Generally Available** (announced today).
- **OneLake shortcuts — SAP & Oracle DB: Generally Available** (recent).
- **OneLake shortcuts — Dremio & Azure DB for MySQL: Public Preview.**
- **OneLake shortcuts — Azure Monitor & AWS Glue: Coming soon** (brings observability data into OneLake).
- **GPU Query Accelerator for Fabric Data Warehouse: Limited Preview** (~8x → 25x → 100x+ as concurrency rises; one-click; SIGMOD Best Paper tech).
- **Agent Skills for Fabric: expanded** — now generate **Power BI reports** (extends the FabCon release from ~3 months ago covering analytical engines).
- **Fabric Ontology: new integrations** across **Foundry, Palantir Studio, and Agent 365**; still preview, **GA targeted later this year**.
- **Planning in Fabric: Generally Available** (was public preview ~3 months ago); rolling out to remaining regions over the next couple of weeks.
- **Apps in Fabric: Public Preview** — first public showing; agentic line-of-business apps on the Rayfin SDK with a managed backend.
- **Agent-driven BI apps:** custom web data apps on Rayfin with a **Power BI skill** generating visuals against semantic models (shown as the next phase of agentic apps).
- **Operations Agents: Generally Available** — new at GA: **chat-based authoring, root cause analysis, and Microsoft Teams integration**.

## 💡 Demos
- **GPU-accelerated Fabric Data Warehouse:** a developer enables **Query Acceleration** in workspace → data warehousing settings (applies to every SQL endpoint & warehouse in the workspace), runs ad-hoc queries, and watches them accelerate. Monitoring adds an "accelerated?" column and a per-query count; the bird's-eye view shows **~89% of queries were accelerated**. Proves the one-click, transparent speedup.
- **Agent Skills for Fabric (medallion architecture from scratch):** from the **GitHub Copilot CLI**, one prompt ("build an ingestion engine, clean my ticket data, prep a silver layer") provisions a **lakehouse + notebook** with best practices applied. Shows **Spark 4.0 / Delta 4.0**, **custom live pools** pre-warmed to start in **~5 seconds** (vs 3–5 min), **AI functions** for sentiment/classification on ticket data, and **Activator** firing a **Teams** alert on a product-quality issue — "from prompt engineering to operational intelligence to real-time alerting in minutes."
- **Planning in Fabric:** a beverage-company sales lead builds a **2026 revenue plan** from **2025 data in a OneLake semantic model**; applies growth rates that cascade to brands/quarters and roll up; **locks** figures so changes only redistribute to open categories; toggles **best-case vs base-case** scenarios with sliders; switches tabular ↔ tree views; adds custom columns, security/comment rules, and an **auditing view**; finishes with **write-back to a Fabric SQL database**, then feeds the plan into the **ontology** for a forward-looking business model.
- **Apps in Fabric / Rayfin (operational app):** a single **Rayfin CLI** command (blank template + name) scaffolds the whole project — Fabric provisions an **app artifact, a linked SQL database, and a static hosting URL**, live in seconds. GitHub Copilot then generates the schema, UI, pages, and flows for a **delivery app** (drivers log deliveries with photos; customers sign on tablets). The app artifact appears in the **governed workspace** beside its **Fabric SQL database** and in the **OneLake catalog** — an enterprise-ready app in minutes.
- **Agent-driven BI app (Rayfin + Power BI skill):** extends the delivery app — a new **data app** item in Fabric, scaffolded via the **Rayfin SDK** in VS Code, uses a **Power BI skill** to generate visuals against a **customer-satisfaction semantic model** joined to live delivery data. Result: an interactive dashboard with **monthly CSAT trends, regional breakdown, on-time delivery, complaint rate, and a delivery-impact correlation** — operational + analytical apps side by side on one governed foundation.
- **Operations Agent (customer churn):** create an agent to monitor churn 24/7; define **goals + instructions** in natural language; connect the **operations ontology** for shared semantic context; add a custom **action** (send a promo code with customer ID + discount params); generate a **playbook** of watch-conditions and allowed actions. In **Teams**, the agent first flags a weak signal (add-to-cart); the user tunes instructions, and the agent later flags a stronger signal (**abandoned cart**) and proposes the promo-code action for one-click confirmation — showing the agent *learning* and acting autonomously.

## 📊 Notable Stats / Quotes
- **35,000 customers** using Fabric (excluding Power BI-only users); **90%+ of the Fortune 500**.
- **$2B+ ARR, 60% YoY growth** — for a platform just over 2 years old.
- **Over a billion agents** predicted to join the workforce in the next 2 years.
- **20 million semantic models** used daily worldwide; **~90%** are Power BI-based.
- GPU Data Warehouse: **~8x** single-query, **~25x** at 16 concurrent, **>100x** at 64 concurrent (vs typical **10–15%/yr** gains); **~89%** of queries accelerated in the demo; **SIGMOD Best Paper**.
- Custom live pools: startup cut from **3–5 minutes** to **3–5 seconds**.
- *"For the AI, when the data is sharded, it's like looking at the world through a broken mirror."*
- *"Operations agents... are virtual team members that monitor signals and react autonomously in the background. They don't wait for you to ask them questions."*
- *"There's no gap between the planning software and the data. It lives in one place."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Enable the **GPU Query Accelerator** (limited preview) on a Fabric workspace and re-run a heavy TPC-H-style or concurrent workload to validate the 8x→100x claims.
  - Stand up a **medallion pipeline** end-to-end via **Agent Skills for Fabric** + GitHub Copilot CLI; test **custom live pools** pre-warming.
  - Spin up an **Apps in Fabric** project with the **Rayfin SDK** (operational LOB app) and an **agent-driven BI app** using the Power BI skill against an existing semantic model.
  - Build a small **Fabric Ontology** (entities + actions + real-time feed) and wire an **Operations Agent** to it; test chat-based authoring + Teams integration.
  - Migrate a planning workbook into **Planning in Fabric** (now GA) and test scenario locking + write-back to Fabric SQL.
- [ ] Questions:
  - What are the GPU Query Accelerator's **eligibility limits / cost model** beyond the one-click toggle (region availability, query types not accelerated)?
  - **GA timing** for Fabric Ontology and for Apps in Fabric (both still preview)? Which regions for Planning GA first?
  - How do **Operations Agents** govern autonomous actions (approval gates, guardrails, audit) at scale?
  - How does **Fabric IQ** surface to external agents (Foundry/Agent 365/Palantir) — protocol/permissions?
- [ ] Relevant to:
  - Any data-estate-unification, lakehouse, or agent-grounding initiative; teams standardizing analytics + operational data + planning on one governed foundation.
  - Architects evaluating OneLake shortcuts vs traditional ETL; BI teams extending semantic models into agentic apps.

## 🔗 Related
- [[OD812 - Fabric IQ Bringing enterprise intelligence into the developer workflow]] — sibling Fabric session diving into Fabric IQ in the developer workflow.
- [[OD818 - The AI-native Data Engineer]] — sibling Fabric session on the evolving data-engineer role with agents.
- [[BRK225 - Data apps and agents the future of app dev with Rayfin]] — deep dive on the **Rayfin SDK** that powers Apps in Fabric shown here.
- [[DEM362 - Building a Multi-Agent Workflow in Microsoft Fabric]] — hands-on multi-agent workflows on the same Fabric foundation.
- [[DEM331 - Turn APIs tools and data into real agent velocity]] — complementary take on grounding agents in real data/tools.
- Source list: [[2026 Build Session List]]

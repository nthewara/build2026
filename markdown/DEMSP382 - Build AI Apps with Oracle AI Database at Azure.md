---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/oracle
  - topic/database
  - topic/ai
  - topic/mcp
  - topic/github-copilot
  - topic/fabric
source: https://www.youtube.com/watch?v=44nyOX45Jn8
session_code: DEMSP382
event: Microsoft Build 2026
speakers: Partha (Oracle AI Database@Azure team), Rajalakshmi Elajosula (Oracle AI Database@Azure – Microsoft team)
duration_min: 26
aliases:
  - Build AI Apps with Oracle AI Database at Azure
---

# DEMSP382 — Build AI Apps with Oracle AI Database@Azure, MCP, and GitHub Copilot

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Partha (Oracle AI Database@Azure team) & Rajalakshmi "Raji" Elajosula (Oracle AI Database@Azure – Microsoft team)  
> **Duration:** ~26 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=44nyOX45Jn8)  
> **Type:** Oracle-sponsored partner demo session

## 🎯 TL;DR
A joint Oracle + Microsoft demo showing how **GitHub Copilot**, the **Oracle MCP server**, and the **Microsoft Fabric MCP server** let developers build end-to-end AI/data applications with natural-language prompts instead of manual wiring. Across two connected demos ("chapter one" and "chapter two"), the speakers provision an **Oracle AI Database@Azure** (Autonomous AI Database / ADB) from the Azure Marketplace, generate and validate synthetic fraud-detection data, replicate it into **Fabric OneLake**, then build ETL pipelines, an ML forecasting experiment (Prophet model), a semantic model, a Power BI dashboard, and a Fabric **data agent** — all driven through Copilot prompts. The closing message: Oracle transactional data + Microsoft Fabric's unified **IQ layer** (Fabric IQ, Foundry IQ, Work IQ) makes Oracle data far more actionable for agentic solutions.

## 🔑 Key Takeaways
- **Oracle AI Database@Azure** runs natively inside Azure data centers as a first-party offering, accessible via the **Azure Marketplace** — usable as if it were a native Azure database.
- The **Oracle MCP server** is generally available now: discoverable in the **OCI portal**, also published in the **Microsoft AI catalog**, and announced in a **blog released the day of the session**.
- The **Fabric MCP server** connects developers to Microsoft Fabric; both Oracle and Fabric MCP servers install as **VS Code extensions** (note: speaker said "Visual Studio," but the workflow shown is VS Code).
- MCP servers translate **natural-language prompts → SQL / API calls**. Under the hood the Oracle MCP server runs **SQLcl** (SQL Command Line) to execute queries against the database.
- GitHub Copilot collapses tasks that historically took **days/weeks** (creating accurate, performant synthetic data; building ETL pipelines; ML experiments) into **minutes/hours**.
- **Data never leaves Azure** during the workflow — IAM controls keep Oracle→Fabric movement secure and governed.
- Two enterprise-grade options exist to bring Oracle data into Fabric: **OCI GoldenGate** (real-time replication) and **Fabric mirroring** (native, near-real-time). The CSV export shown was just for demo simplicity.
- Oracle AI Database@Azure spans a **full spectrum of offerings**: Autonomous Database (ADB), **Base DB, Exadata, and Exascale** — giving enterprises a choice for their Oracle workloads.
- Demo 2 walks the full **medallion architecture** (bronze → gold) and multiple developer personas: app dev, **data engineer**, **ML engineer**, and **business user**.
- Copilot auto-generates **multi-step to-do plans** (e.g., 5 to-dos), creates notebooks (PySpark), deploys them to Fabric, builds pipelines, and validates runs — with the developer free to tweak anything.
- The **Prophet model** was used to forecast viewership; runs were split **by channel**, producing ML metrics for model comparison, and results written back to the lakehouse as a forecast **delta table**.
- A **Fabric data agent** lets business users converse with the data; it can be published to the **Microsoft store**, converted into a Fabric MCP server, and secured with **role-based access control (RBAC)**.
- Strategic framing (tied to **Satya's keynote** from the prior day): unifying Oracle transactional data with Fabric's **IQ layers** lets decisions draw on emails, Teams chats, calendars, and workflows — "Oracle and Microsoft are powerful together."
- Real-world authenticity note: even the presenter's own project initially failed on download; he used **Copilot to debug/troubleshoot** and fixed it in a few minutes.

## 📚 Detailed Notes

### The developer landscape & the problem
The session opens by framing **who** builds AI apps today and the friction they hit. The relevant personas:
- **Traditional app developers** — want to accelerate app development.
- **ML engineering developers** — build ML applications.
- **Data engineering developers** — build/maintain data pipelines.
- **Forward deployment engineers** — a newer class of developer.

A common thread across all of them: *"How do I access my data, and keep it where it resides today?"* The pain points called out:
- **Connectivity setup** requires heavy **manual wiring**, API access, and reading documentation.
- **Manual schema discovery** is needed before a database is usable in apps.
- **Data silos** between Oracle and Microsoft systems — disparate platforms that must be stitched together.
- **App scaffolding** is a major challenge — creating data for validation and templatizing apps takes real effort.

### Oracle AI Database@Azure — what it is
- A **native first-party database offering** running **inside Azure data centers**.
- Accessible through the **Azure Marketplace**; behaves like a native Azure database.
- The demo specifically provisions an **Autonomous AI Database (ADB)** — a "fully automated database solution."
- Broader portfolio (highlighted by Raji): **Autonomous Database, Base DB, Exadata, Exascale** — enterprises pick the best fit for their Oracle workloads. Navigation lives on the **Oracle AI Database@Azure page** in the Azure portal.

### The three enabling technologies
1. **Oracle MCP server** — available today via the **OCI portal** and the **Microsoft AI catalog**; blog published the day of the session.
2. **Fabric MCP server** — connects to **Microsoft Fabric**.
3. **Microsoft GitHub Copilot** — the orchestration layer that stitches the MCP servers together coherently.

> The two demos are deliberately sequential — "chapter one" (Oracle side: create + validate data) feeds "chapter two" (Fabric side: analytics, ML, BI).

### Demo 1 — Fraud detection data on Oracle (presented by Partha)
**Goal:** Build a customer/account database with **synthetic data** for a fraud-detection scenario, then transport it into Fabric for predictive analytics/forecasting — all while keeping the data inside Azure.

**Pre-setup (two manual steps before Copilot takes over):**
1. Create an **Oracle AI Database (ADB)** via the **Azure Marketplace** — provisioned empty (no data yet).
2. Create a **new empty workspace in Fabric**.

(Credit given to colleague **Daniel from Sweden** for the initial setup. Partha's app didn't work on first download — he used **Microsoft Copilot to debug and fix it in a few minutes**, a genuine "power of AI" moment.)

**MCP servers** were installed as **VS Code extensions**. The demo flow:
- **Connectivity check** — verify Copilot can reach both the **Oracle MCP server** and **Fabric MCP server**; it checks the schema and confirms connectivity.
- **Create tables + synthetic data** — Copilot creates **two tables** in the Oracle ADB, each with **~100 rows** of synthetic data. Key value: generating *accurate, performant* synthetic data normally takes a developer **days**; Copilot does it in **minutes**.
- **Under the hood:** the Oracle MCP server runs **SQLcl** (Oracle's SQL command-line utility), translating **natural-language commands into SQL queries** to create and fetch data.
- **Data validation** — Copilot confirms table/column names exist, **counts rows**, and **samples data** to verify the data is real (a routine step developers normally do by hand).
- **Performance/statistics checks** — runs the Oracle **statistics optimizer** (built into the Oracle database) to ensure SQL queries have no performance issues; if issues exist it can **auto-tune**. It also validates **indices and constraints** (again via SQLcl in the background).
- **Transition to chapter two — export to Fabric** — exports the Oracle data to Fabric. In the demo it exports as a **CSV file**, but the enterprise-grade method is the **Oracle GoldenGate connector** for replication/transport. Emphasis on **security + IAM control**: data does not leave Azure.
- **Verify landing in OneLake** — checks the **OneLake path structure** and confirms the data landed in **Fabric OneLake**; the **Fabric MCP server** verifies the data exists.
- **Final step** — create a **Fabric notebook** with **ML files and Spark Delta files**, setting up the data for analytics workloads (beyond simple querying).

### Demo 2 — Analytics, ML & BI on Fabric (presented by Raji)
Raji ( **Rajalakshmi Elajosula**, Oracle AI Database@Azure – Microsoft team) takes over to show **what you can do with the data once it's in Fabric**.

**Getting Oracle data into Fabric — two enterprise options:**
- **OCI GoldenGate** — replicate relevant Oracle data into Fabric in **real time**.
- **Fabric mirroring** — natively mirror Oracle data into Fabric in **near-real-time**.
- Choose whichever fits requirements best.

**Scenario / data estate — "Zava Media" (fictitious company):**
- Has a **mirror database** with Oracle data mirrored into Fabric.
- Also has a **SQL database** holding structured data.
- Uses **Fabric shortcuts** to unify everything into a **lakehouse**.
- The **bronze layer** contains **four master tables** of raw data (some from Oracle, some from SQL DB) — covering **viewership data** of programs across regions, plus general sentiment.

**Developer persona walkthrough (all via Fabric MCP server + GitHub Copilot in VS Code):**

1. **Discover access** — prompt: *list all Fabric workspaces I can access with my credentials.* Copilot identifies the Fabric MCP server, picks the relevant tool, invokes it, and returns the workspace list. Target workspace: **Zava Media**.
2. **Understand the data estate** — follow-up prompt to explain the Zava Media workspace. Copilot lists the **four lakehouse tables** and builds an **entity-relationship (ER) model** showing primary keys, foreign keys, and relationships. (Model used: **Opus model with GitHub Copilot** — "you can use a model of your choice.")
3. **Data engineer hat — bronze → gold ETL** — prompt to build a **data pipeline** using Fabric MCP server + Fabric APIs. Copilot:
   - Creates **five to-dos** automatically.
   - Step 1: understands the Fabric configuration.
   - Step 2: creates a **notebook** to move bronze → gold (demo goes straight bronze→gold; could be sequenced bronze→silver→gold).
   - Creates a **second notebook** to validate the gold data is written back to the lakehouse.
   - Final step: **deploys** the locally-authored VS Code code into Fabric **as a notebook**.
   - Writes **no code by hand** — Copilot generates the **PySpark** code.
4. **Validate in Fabric portal** — two notebooks appear (**gold viewership** + **validation**); PySpark code migrated correctly; notebooks stitched into a **Fabric data pipeline**; the pipeline **run succeeded**, with per-notebook run times shown. The lakehouse now has **five tables** (was four) — the new **gold layer** table for viewership.
5. **ML engineer hat — viewership forecast** — single prompt to build a **viewership prediction model** for Zava Media using a **Prophet model** ("profit model" in captions). Copilot accesses the gold data, builds a notebook, runs an **ML experiment**, and migrates it to the Fabric workspace via Fabric MCP server tools + **Fabric REST API**. In the portal: the **ML experiment** runs **separately by channel** (four runs), exposing ML metrics for model comparison ("Prophet seems to be good"). Results written back to the lakehouse as a new **forecast viewership delta table**.
6. **Business-user value — semantic model, dashboard & data agent:**
   - Creates a **semantic model** + a **data agent** (via Fabric MCP server tools + Fabric REST APIs) so business users can converse with the data (self-serve model).
   - Auto-generates a **Power BI dashboard** from the semantic model — created in a few minutes, fully tweakable/shareable.
   - The **data agent** connects to the two newly created forecast tables, answers business-user queries, leverages **lakehouse data**, and renders a **chart** in responses.
   - The data agent can be **published to the Microsoft store**, **converted into a Fabric MCP server** for integration with other apps, and locked down with **role-based access control (RBAC)**.

### Strategic close — the unified IQ layer
- Recap: data started entirely in the **Oracle estate**; with the **Fabric MCP server + Oracle MCP server**, all the insights, pipelines, ML, and BI were generated from prompts.
- Bigger vision: bring this into **Fabric IQ, Foundry IQ, and Work IQ** layers — a **unified IQ layer** makes Oracle **transactional data more actionable**.
- Explicitly tied to **Satya Nadella's keynote from the day before**.
- The payoff: Oracle data can drive decisions informed by your **emails, Teams chats, calendars, and business workflows** — combining transactional data with the IQ layer.
- Closing message: *"Oracle and Microsoft are powerful together"* — ongoing investment to make building **agents and agentic solutions** more seamless for developers.

## 🛠️ Products / Features / Technologies Mentioned
- **Oracle AI Database@Azure** — first-party Azure offering; portfolio: **Autonomous Database (ADB), Base DB, Exadata, Exascale**.
- **Oracle MCP server** — GA; in OCI portal + Microsoft AI catalog; installs as a VS Code extension.
- **Microsoft Fabric MCP server** — VS Code extension; tools for workspaces, data estate, pipelines, ML, semantic models, agents.
- **GitHub Copilot** — orchestration / natural-language driver; model choice (e.g., **Opus**).
- **VS Code** — IDE hosting the MCP server extensions (referred to on stage as "Visual Studio").
- **SQLcl (SQL Command Line)** — Oracle utility the MCP server runs under the hood.
- **Oracle Statistics Optimizer** — built-in Oracle DB tool for performance tuning, index/constraint checks.
- **OCI GoldenGate** — real-time Oracle→Fabric replication connector.
- **Fabric mirroring** — native near-real-time Oracle mirroring into Fabric.
- **Microsoft Fabric** — OneLake, lakehouse, shortcuts, notebooks, data pipelines, ML experiments, semantic models, **data agents**, Fabric **REST API**.
- **OneLake** — Fabric storage where exported data lands.
- **PySpark / Spark Delta tables** — notebook code + storage format (bronze/gold/forecast delta tables).
- **Prophet model** — time-series forecasting model for viewership prediction.
- **Power BI** — auto-generated dashboard from the semantic model.
- **Medallion architecture** — bronze / (silver) / gold layering.
- **Fabric IQ, Foundry IQ, Work IQ** — unified "IQ layer" vision.
- **Microsoft store** — publishing target for the data agent.
- **Azure Marketplace** & **OCI portal** — provisioning/discovery surfaces.
- **RBAC (role-based access control)** — security on the data agent.
- **Azure IAM** — governance keeping data inside Azure.

## 🚀 Announcements / What's New
- **Oracle MCP server availability** — now available via the **OCI portal** *and* the **Microsoft AI catalog**, with a **blog post published the same day** as the session. (Framed as "available for you to get started today.")
- The **Fabric MCP server** is presented as available as a **VS Code extension** for connecting to Microsoft Fabric.
- (Other items — e.g., the IQ layer vision and GoldenGate/mirroring options — are presented as available/strategic direction rather than net-new announcements at this session.)

## 💡 Demos
- **Demo 1 (Partha) — Oracle fraud-detection data:** Provision Oracle ADB via Azure Marketplace + empty Fabric workspace → connect Oracle & Fabric MCP servers → Copilot creates 2 tables × ~100 rows of synthetic data (via SQLcl) → validate rows/samples → run statistics optimizer + index/constraint checks → export Oracle data to Fabric OneLake (CSV for demo; GoldenGate for enterprise) → verify landing in OneLake → create Fabric notebook with ML/Spark Delta files. All driven by Copilot prompts; data stays in Azure.
- **Demo 2 (Raji) — Zava Media analytics, ML & BI on Fabric:** Unify Oracle (mirrored) + SQL data into a lakehouse via shortcuts (4 bronze tables) → list workspaces → build ER model of the data estate (Opus model) → data-engineer ETL bronze→gold (Copilot creates 5 to-dos, PySpark notebooks, data pipeline; deploys to Fabric; run succeeds; 5th gold table appears) → ML-engineer viewership forecast with Prophet (4 runs by channel, metrics, forecast delta table written back) → business-user semantic model + Power BI dashboard + Fabric data agent (publishable to Microsoft store, convertible to MCP server, RBAC-secured). End-to-end, "just a few prompts."

## 📊 Notable Stats / Quotes
- **~100 rows per table** in the two synthetic Oracle tables (Demo 1).
- **4 → 5 lakehouse tables** after the gold ETL; **6th**-equivalent **forecast delta table** added after the ML experiment.
- **5 to-dos** auto-created by Copilot for the ETL pipeline build.
- **4 ML experiment runs** (one per channel) for the Prophet forecast.
- **4 t-shirts** given away (two XL, two large) for audience questions. 👕
- Time compression theme: tasks that took **days/weeks** (synthetic data, ETL, ML experiments) reduced to **minutes/hours**.
- *"Oracle and Microsoft are powerful together if you're bringing the transactional data with [the] IQ layer added on top of it."* — Raji
- *"All we are getting is a head start to not create all of this from scratch... save a lot of hours as a developer."* — Raji
- *"A unified IQ layer makes your Oracle transactional data more actionable."* — Raji (tying to Satya's keynote)

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install the **Oracle MCP server** + **Fabric MCP server** VS Code extensions and reproduce the connectivity check → synthetic data → SQLcl validation flow against an Oracle ADB.
  - Stand up an **Oracle AI Database@Azure (ADB)** from the Azure Marketplace and an empty Fabric workspace; test **GoldenGate** vs **Fabric mirroring** for Oracle→Fabric.
  - Recreate the **bronze→gold** medallion ETL with Copilot-generated PySpark notebooks + a Fabric data pipeline.
  - Build a **Prophet** forecasting ML experiment in Fabric and write results back as a delta table; then auto-generate a **Power BI** dashboard + a **Fabric data agent** and publish/secure it with RBAC.
- [ ] Questions:
  - Is it really **VS Code** (extensions/Copilot Chat) rather than full Visual Studio? (Workflow strongly implies VS Code.)
  - What are the **licensing/cost** implications of GoldenGate vs Fabric mirroring for Oracle→Fabric at scale?
  - How does the **Oracle MCP server** authenticate (OCI creds, Azure identity passthrough)? How is least-privilege enforced?
  - Where exactly is the **blog post** + on-demand Build catalog session referenced for deeper detail?
  - How mature is **Work IQ / Foundry IQ / Fabric IQ** integration with Oracle transactional data today vs roadmap?
- [ ] Relevant to:
  - Customers running **Oracle workloads** who want Azure-native analytics/AI without moving off Oracle.
  - **Data/ML engineering** teams exploring MCP + Copilot to accelerate ETL and ML scaffolding in Fabric.
  - Agentic-app builders interested in **Fabric data agents** + the unified **IQ layer**.

## 🔗 Related
- [[Microsoft Build 2026]]
- [[Microsoft Fabric]]
- [[Model Context Protocol (MCP)]]
- [[GitHub Copilot]]
- [[OneLake]]
- [[Oracle AI Database@Azure]]

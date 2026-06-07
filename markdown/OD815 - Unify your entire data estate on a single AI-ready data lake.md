---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/fabric
  - topic/onelake
  - topic/data-lake
  - topic/ai
source: https://www.youtube.com/watch?v=Alb2Tnw4moo
session_code: OD815
event: Microsoft Build 2026
speakers: Deepti Borkar, Josh (OneLake team), Weishung (OneLake team), Michaela (OneLake team), Rohan (demo)
duration_min: 35
aliases:
  - Unify your entire data estate on a single, AI-ready data lake
---

# OD815 — Unify your entire data estate on a single, AI-ready data lake

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Deepti Borkar (OneLake & Fabric teams — intro/overview), Josh (OneLake — pillars: storage, open access, security), Weishung (OneLake — shortcuts & mirroring), Michaela (OneLake — AI-ready / Fabric IQ + Foundry), Rohan (live demo narration)  
> **Duration:** ~35 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=Alb2Tnw4moo)

## 🎯 TL;DR
OneLake is pitched as "the OneDrive for data" — a single logical data lake (always exactly **one per organization**) that unifies a customer's entire data estate with **zero ETL**, via two mechanisms: **shortcuts** (virtualize data in place, no movement) and **mirroring** (CDC-based replication of whole databases). Data lands in **open formats (Delta Lake + Iceberg)** and is then reachable everywhere across the Microsoft ecosystem (Fabric, Power BI, Excel, SharePoint, Foundry, Copilot) and by dozens of external engines (Databricks, Snowflake, Salesforce, DuckDB, ClickHouse, ServiceNow, etc.). The session is organized around **four pillars**: (1) a **unified data estate**, (2) **open access** ("one copy" of data consumed by many engines via the OneLake table API for Delta + Iceberg), (3) **AI-ready** data + context through **Microsoft IQ / Fabric IQ** and native **OneLake catalog ↔ Foundry** integration, and (4) **unified discovery & governance** via **OneLake security** (now GA) and the **OneLake catalog**. Headline new items include **lifecycle management with storage tiering**, **SharePoint list mirroring**, **Excel shortcuts**, **table API metadata writes**, **mirroring over workspace private link**, and **OneLake security GA** (plus Event House in preview).

## 🔑 Key Takeaways
- **OneLake = "OneDrive for data."** One unified logical lake per org that spans Fabric engines, ADLS/on-prem, SharePoint, other clouds (S3, GCP) and many data providers — all with **zero ETL**.
- **Always exactly one lake per organization** — never more, never less. This invariant is a core anti-silo design choice; all data shows up in open formats, is auto-indexable/scannable, and is always protected by OneLake security.
- **Two ways to bring data in:** (1) **connect** your existing estate in place (shortcuts/mirroring — no movement, no duplication, no migration; you keep managing your storage) or (2) **physically store** it in OneLake (Microsoft manages scale/throughput). After ingest, **all functionality is identical regardless of path**.
- **OneLake is the foundation of Microsoft Fabric** — **every Fabric customer is a OneLake customer**: 35,000+ paying customers, **80%+ of the Fortune 500**, **48 billion interactions/day**, **9.4 million active shortcuts**, growing **4× year-over-year** in storage.
- **Native storage is expanding beyond Fabric:** Snowflake can now natively store its **Iceberg** tables in OneLake; **Azure Databricks** native storage in OneLake is in **preview**. OneLake exposes the same **ADLS + Blob APIs**, so anything that talks to Azure storage can read/write it.
- **Shortcuts vs mirroring:** shortcuts connect data wherever it lives with no movement (on-prem or any cloud); mirroring brings an entire database catalog in via the source's **change data capture (CDC)** to keep an up-to-date mirrored database.
- **Lots of sources are GA** for shortcut/mirroring: SQL Server (incl. SQL Server 2025 and on-prem), Snowflake, Oracle, SAP Datasphere, plus newly **SharePoint & OneDrive**. New in **public preview**: Dremio (caption "Dream U"), Azure Monitor, and **AWS Glue coming soon**.
- **"One copy" principle:** one physical copy of data is consumed by **multiple engines** (T-SQL warehouse team and Python/notebook lakehouse team both land data in OneLake, readable by any engine) — decoupling how data is created from how it's consumed.
- **OneLake table API** now exposes the same open-source APIs for **both Delta Lake and Iceberg natively**, so any Iceberg- or Delta-compliant app can read **all** OneLake data regardless of how it was written. New: **writing metadata** (create tables/schemas, update/publish transactions) via the table API — **available today** (reading metadata was already GA).
- **AI-ready means data + context, not just data.** **Microsoft IQ / Fabric IQ** frees the knowledge/context that was trapped in silos alongside the data, encapsulates it with the data in OneLake, and distributes both to ground AI agents (semantic models + operational intelligence).
- **OneLake catalog is now natively integrated into Foundry** — discover trusted enterprise data (sensitivity labels, endorsements) and use it directly in Foundry **knowledge** for grounding agents, with **no data copy** (shortcuts virtualize structured + unstructured data including SharePoint, S3, NetApp, Azure Blob).
- **OneLake security is GA.** It pushes engine-specific controls (row-level, column-level) **down into the lake**, so you **define security once** and it's **enforced across every engine** (SQL endpoint, Spark, semantic models / Direct Lake, Power BI, Excel). **Event House** support is in **public preview**.
- **OneLake catalog** is the discovery/governance surface, **trusted by 240,000+ organizations worldwide** — described as the "final piece" of OneLake.
- **Customer proof points:** **Lumen** (ingest once, use anywhere), **London Stock Exchange Group** (Data-as-a-Service on Fabric; chose it for Snowflake/Databricks interop + openness), **AP Pension** (eliminated the E and L of ETL, kept only Transformation via mirroring).
- **Enterprise hardening shipped:** customer-managed-key encryption at rest (**GA**), immutable diagnostic logs, and stronger network security (workspace-level private links, outbound access protection, workspace firewall, **resource instance rules** for specific Azure services).

## 📚 Detailed Notes

### What OneLake is — "the OneDrive for data"
Deepti Borkar opens by framing **OneLake** as *the OneDrive for data*. Its job is to **unify an organization's entire data estate** without ETL:
- **Microsoft-managed estate:** Fabric (with all its engines) and the broader Azure/on-prem estate (ADLS and others).
- **Business productivity:** **SharePoint** (cloud or on-prem).
- **Other clouds & providers:** **S3, GCP**, and many more.

The unification happens with **zero ETL** through two mechanisms (covered in depth later): **shortcuts** and **mirroring**. Once data is in OneLake as a **single pane of glass**, it becomes reachable across the Microsoft ecosystem — **Teams, Fabric, Foundry**, and even **Excel**, where the **OneLake hub** can be opened to pull structured data straight into a spreadsheet.

Crucially, the data stays **completely open**. OneLake supports **Delta and Iceberg** open formats, which means the same data is consumable by a long tail of external products and services: **DuckDB, Databricks, Snowflake, ServiceNow, Salesforce, ClickHouse**, and many others. The stated goal: give you unification of **data — and, for the AI age, context** — and make it **accessible everywhere**.

### The OneLake ecosystem
Deepti describes a "vibrant, continuously growing" ecosystem with several integration patterns:
- **Native integration** — e.g. Databricks and Snowflake can read/write directly on top of OneLake (Josh covers native storage later).
- **Catalog federation** — integrate via catalog mechanisms (Iceberg, Presto catalogs, etc.); a broad range of services fall here.
- **Data movement tools** — Informatica, Fivetran and others integrate so you can land data natively into OneLake from many sources.

She invites builders to integrate with OneLake too.

### Scale, momentum & customer proof
OneLake is the **foundation for Microsoft Fabric**, the single product for managing, exploring, gaining insights from, and making data **AI-ready**. **Every Fabric customer is a OneLake customer.** Stats cited:
- **35,000+ paying customers** on Fabric/OneLake.
- **80%+ of the Fortune 500** use OneLake/Fabric.
- **48 billion interactions per day** on the OneLake service, with strong reliability.
- **9.4 million active shortcuts** already created across the ecosystem (sources include AWS S3, GCP, on-prem, etc.) — heavy use of **zero-copy**.
- **4× year-over-year growth** in storage.

Three highlighted customers:
- **Lumen** — OneLake let them **ingest data once and use it anywhere** (the single-pane-of-glass benefit).
- **London Stock Exchange Group (LSEG)** — their **Data-as-a-Service** offering is built on Fabric; they adopted it for **interoperability** between Snowflake, Databricks and others, plus OneLake's **openness**.
- **AP Pension** — **eliminated the E and the L** of ETL, leaving only the **Transformation**, using OneLake's **mirroring** capabilities.

### The four pillars of OneLake
Deepti sets up the structure for the rest of the talk — OneLake's core has **four aspects**:
1. **Unified data estate** — open, accessible from many platforms.
2. **Open access** — built so any engine can consume the data.
3. **AI-ready** — integrates with Foundry and other products to power AI.
4. **Unified discovery & governance** — via **OneLake security** and the **OneLake catalog**.

She then hands to **Josh** to walk through the pillars.

### Pillar 1 — Unified data estate (Josh)
Josh frames the origin story: customers were drowning in **data silos** — unable to get to or blend the data they needed. **OneLake came in "like a wrecking ball,"** busted the silos open, freed the data, and unified everything into **a single logical lake**.

Key invariant: **there is always exactly one lake per organization** — you can never have more than one or fewer than one. This is one of the primary ways silos are avoided. In OneLake, **all data shows up in open formats**, can be **automatically indexed and scanned**, and is **always protected by OneLake security**.

**Two ways to bring your data estate to OneLake:**
1. **Connect your existing estate (easiest).** Connect data **wherever it lives** with **no data movement, no duplication, no migration** — Azure, other clouds, or on-prem. You keep managing your existing storage resources but get all the OneLake benefits/features.
2. **Physically store data in OneLake.** Microsoft manages **over 3 million storage accounts** for users today (the thing that "really makes us the OneDrive for data"). OneLake auto-handles **scale and throughput** as needs change, without you managing individual storage resources.

**The payoff:** no matter how data arrives (connected vs stored), **all functionality is identical afterward**.

### Native storage improvements (Josh)
Since launch, Fabric has always stored its data inside OneLake. Newer expansions:
- **Snowflake** can now **natively store its Iceberg tables** in OneLake.
- **Azure Databricks** native storage in OneLake is in **preview**.
- This is **in addition to anything that talks to Azure storage** — OneLake exposes the **same ADLS and Blob APIs**, so any storage-speaking service can natively read/write OneLake.

**Enterprise security hardening on native storage:**
- **Data encryption with customer-managed keys (CMK) at rest** — **generally available today**.
- **Diagnostic logs with immutable storage** — see/debug everything happening across the entire data lake.
- **Stronger network security:** **workspace-level private links**, **outbound access protection**, **workspace firewall**, and newly **resource instance rules** that specify which specific Azure services may connect to your data.
- Reference: the **Fabric Security white paper**.

### Pillar 1 recap (Josh)
After the storage demo, Josh recaps what just shipped:
- **OneLake File Explorer** — **generally available**, along with the **OneLake MCP**.
- **Item size reporting** — **public preview**.
- **Lifecycle management with data tiering** — described as "probably our biggest announcement" — **now available**.

He then hands to **Weishung** for connecting existing data (shortcuts & mirroring).

### Shortcuts & mirroring (Weishung)
Two complementary ways to unify the estate:
- **Shortcuts** — "super cool": connect to data **wherever it is** with **no data movement**; works for data **on-premises or in any cloud**.
- **Mirroring** — brings your **entire data catalog** into OneLake. For sources like **Oracle / SQL Server** (on-prem or cloud), it leverages the underlying **change data capture (CDC)** to keep an **up-to-date mirrored database**.

Combined, shortcuts + mirroring let you **unify your data estate into OneLake**.

**Generally available sources** (sampling): the **SQL family** (SQL Server 2025, on-prem SQL Server, and more), **Snowflake**, **Oracle database**, **SAP Datasphere**, and more recently **SharePoint and OneDrive**. You can use these to bring data in **with or without data movement**.

**New in public preview:** **Dremio** (rendered "Dream U" in captions), **Azure Monitor**, with **AWS Glue coming soon**.

**Mirroring over workspace private link** (a top customer ask): adds private-link network security to your mirrored database and routes **all traffic through the Microsoft private network instead of the public internet** — now in **public preview**, initially supporting **Azure Cosmos DB, Azure SQL Managed Instance (SQL MI), and SQL Server 2025**, with more sources coming.

### Shortcut transformation (Weishung)
**Shortcut transformation** enriches data with **native AI capabilities in OneLake** — **generally available**. You point at **source folders in OneLake** and add **defined AI transformations**; it then **continuously auto-tracks source changes** and **syncs to the destination** while enriching with AI.

New improvements:
- **Preview and define schemas** (top customer ask).
- **Manage transformations with detailed logs** / **enhanced monitoring** to understand what's happening under the hood.

**What shortcut transformation can do (at a glance):**
- **Format conversions** — Parquet → table, Excel → table, and many more.
- **AI enrichment** — **PII detection, translation, text summarization, sentiment analysis, name recognition**, and more.

### Pillar 2 — Open access & "one copy" (Josh)
Having unified the estate, the **purpose** is to use the data in many places. **All OneLake data is available across the entire Microsoft ecosystem** — deep integrations with **Foundry, Power BI, Office, Excel, Copilot** — and **well beyond Microsoft** to dozens of services including **Databricks, Snowflake, Salesforce**.

**The "one copy" principle:** you can use **one copy of data across multiple engines**. This separates *how you create* the data/lake from *how you consume* it:
- A team that prefers **stored procedures + T-SQL** can build a **data warehouse**.
- A team that prefers **Python + notebooks** can build a **lakehouse**.
- Both end up as **data in OneLake**, consumable by **any engine** — within Fabric, Databricks, or anywhere that reads an open data format.

**OneLake table API:** OneLake now exposes the **same open-source APIs for both Delta Lake and Iceberg natively**. Any application that understands **at least one** of those formats (Snowflake, Databricks, etc.) can read **all** data in OneLake — **regardless of how/what format it was written in**.
- Already **GA:** **reading metadata** through the table APIs.
- **New (available today):** **writing metadata** — create tables, create schemas, update/publish transactions via the table API.

Beyond APIs, OneLake is **deeply integrated** with dedicated experiences in **Fabric, Excel, and SharePoint**, so data is visible and usable directly. "OneLake data literally is everywhere."

### Pillar 3 — AI-ready data + context: Microsoft IQ / Fabric IQ (Josh → Michaela)
Josh's key insight: when data was freed from silos, **it wasn't the only thing stuck — so was the knowledge/context** that lived in people's heads inside those silos. **Microsoft IQ** and **Fabric IQ** free the data *and* **encapsulate that context with the data** in OneLake. Once data + context are together, you can **distribute both** to all the data/applications (and **agents**) that need it — so you get not just data, but **the knowledge of how best to work with it**. OneLake spans **all databases, all clouds**, and brings **semantic models (analytical intelligence)** plus **operational intelligence**, making it the best source of knowledge to **ground AI applications**.

**Michaela** extends this: OneLake already brings together **unified data, business intelligence, and operational intelligence**. What's **new** is making the data usable across a **full set of AI consumers** — **Fabric, Foundry, Copilot Studio, and partner tools**. When data flows through these AI experiences it is **never copied**; it's exposed through a **common data foundation** with **shared context and intelligence** on top.

A lot of enterprise value is in **unstructured** data — **documents, PDFs, SharePoint sites, customer conversations, contracts, invoices**. With OneLake you can unify **structured and unstructured** data in one place from many sources (SharePoint, Amazon S3, etc.) **without replication**.

**OneLake catalog → Foundry (native):** the **OneLake catalog is now natively integrated into Foundry**. You can **discover all trusted enterprise data in one place** and immediately use it inside **knowledge, agents, and any AI workload**, with the catalog's full discoverability capabilities — **sensitivity labels and endorsements** — giving a consistent view across **Fabric and Foundry**.

### Pillar 4 — Discovery & governance: OneLake security + catalog (Josh)
To safely access data from anywhere (including AI), you must **secure and govern** it. **OneLake security is now generally available** and "changes the game."
- The old world: the most capable security lived **at the edges** — in presentation layers and database engines — with **different security for every single engine**.
- OneLake unified the **data** ("one copy across multiple engines"); security needed the same. **OneLake security takes engine-specific capabilities — row-level security, column-level security — and moves them down to the data lake.**
- You **define security definitions once**; they **live with the data in the lake** and are **enforced everywhere the data is used, in any engine**.

After the security demo, Josh adds:
- **OneLake security for Event House** is in **public preview**, joining the engines in Fabric that can enforce OneLake security across the board.
- This is **part of the OneLake catalog**, the **final piece** of OneLake. The **OneLake catalog** exposes data for **discovery and governance** and is **trusted by 240,000+ organizations worldwide**.
- To learn more about the catalog: see the session from **Kim Manis**. Closing: bring your data and build a single unified data lake for your whole organization.

## 🛠️ Products / Features / Technologies Mentioned
- **OneLake** — the unified, open, AI-ready logical data lake; "the OneDrive for data"; exactly one per organization; foundation of Microsoft Fabric.
- **Microsoft Fabric** — single product for managing/exploring data and making it AI-ready; built on OneLake.
- **OneLake shortcuts** — virtualize/connect data in place with **no movement** (on-prem or any cloud); 9.4M active.
- **Mirroring** — CDC-based replication that brings an entire database catalog into OneLake (keeps an up-to-date mirror).
- **SharePoint list mirroring** — mirror a SharePoint Online list into OneLake (announced in session).
- **Excel shortcuts** — shortcut to an Excel workbook; Fabric detects the file and turns **each sheet into a first-class table** (announced).
- **Shortcut transformation** — continuous, auto-tracking AI enrichment + format conversion on OneLake source folders (GA).
- **OneLake table API** — exposes Delta Lake **and** Iceberg APIs natively; read **and now write** metadata (create tables/schemas, publish transactions).
- **Delta Lake / Apache Iceberg** — the two open table formats OneLake natively supports.
- **OneLake File Explorer** — Windows File Explorer integration showing workspace items as folders/files; drag-and-drop ingest (GA).
- **OneLake MCP** — Model Context Protocol surface for OneLake (GA, mentioned alongside File Explorer).
- **OneLake storage report / item size reporting** — item-level storage visibility incl. soft-deleted + system folders (public preview).
- **Storage tiers + lifecycle management (data tiering)** — auto-move infrequently used data to cool/cold tiers; default + customizable tiering rules.
- **OneLake security** — row/column-level security defined once at the lake, enforced across all engines (GA); **Event House** support in preview.
- **OneLake catalog** — discovery + governance surface (sensitivity labels, endorsements, promotion); trusted by 240k+ orgs; now native in Foundry.
- **Microsoft AI Foundry** — AI dev platform; uses **knowledge** to index OneLake context for grounding agents; OneLake catalog natively integrated.
- **Foundry knowledge** — indexing step turning raw files into searchable/retrievable knowledge for agents.
- **Microsoft IQ / Fabric IQ** — encapsulates context/knowledge alongside data in OneLake to power agents (semantic + operational intelligence).
- **Copilot / Copilot Studio** — AI consumers of OneLake data.
- **Power BI / Direct Lake** — reporting and semantic models built over OneLake mirror tables, honoring OneLake security.
- **Semantic models** — analytical intelligence layer carried with the data.
- **ADLS + Blob APIs** — OneLake exposes the same storage APIs so any Azure-storage client can read/write it.
- **Diagnostic events / immutable logs** — capture who accesses OneLake data; can be made immutable.
- **Customer-managed keys (CMK)** — encryption at rest under your own keys (GA).
- **Network protection** — workspace-level private links, outbound access protection, workspace firewall, resource instance rules.
- **Catalog federation** — integrate external catalogs (Iceberg, Presto) into OneLake.
- **Data movement partners** — Informatica, Fivetran (and others) land data natively into OneLake.
- **External engines / consumers** — Databricks, Snowflake, Salesforce, ServiceNow, ClickHouse, DuckDB (open-format read/write/consume).
- **SQL endpoint / Spark** — query engines in the demo that honor OneLake security row/column rules.

## 🚀 Announcements / What's New
**Generally available (GA):**
- **OneLake security** — define row/column-level security once at the lake; enforced across all Fabric engines.
- **OneLake File Explorer** (Windows File Explorer integration) and the **OneLake MCP**.
- **Lifecycle management with data tiering** (cool/cold storage tiers + default & custom tiering policies) — called "probably our biggest announcement."
- **Customer-managed-key (CMK) encryption at rest** for native OneLake storage.
- **Shortcut transformation** (native AI enrichment + format conversion on OneLake folders) — plus new schema preview/define and detailed-log monitoring improvements.
- **OneLake table API — writing metadata** (create tables/schemas, update/publish transactions); reading metadata was already GA. "Available today."
- **Shortcut & mirroring sources GA:** SQL Server 2025, on-prem SQL Server (and broader SQL family), Snowflake, Oracle, SAP Datasphere, and newly **SharePoint & OneDrive**.

**Public preview:**
- **Azure Databricks native storage in OneLake** (store Databricks data directly in OneLake).
- **Item size reporting** (OneLake storage report with item-level + soft-deleted + system-folder visibility).
- **Mirroring over workspace private link** — initially Azure Cosmos DB, Azure SQL MI, SQL Server 2025 (traffic over Microsoft private network).
- **New shortcut/mirroring sources:** **Dremio** (caption "Dream U") and **Azure Monitor**.
- **OneLake security for Event House** (joins existing engines that enforce OneLake security).

**Announced in-session (mirroring/shortcut features demoed live):**
- **SharePoint list mirroring** — mirror a SharePoint Online list into OneLake (demoed; GA listed among shortcut/mirroring sources).
- **Excel shortcuts in OneLake** — "Starting today"; each sheet becomes a first-class lakehouse table.
- **OneLake catalog natively integrated into Foundry** — discover trusted enterprise data and use it in Foundry knowledge/agents.

**Coming soon / roadmap:**
- **AWS Glue** support for shortcut/mirroring.
- More mirroring sources over workspace private link.

**Already-GA capabilities reinforced (status as stated):**
- Snowflake natively storing **Iceberg** tables in OneLake.
- Snowflake/Databricks/Salesforce open-format interoperability via Delta + Iceberg table APIs.

## 💡 Demos
**Demo 1 — New OneLake storage features (narrated, post-Josh).** Opens in a "busy, real, production-looking" workspace. Shows the **OneLake File Explorer** surfacing all item types as folders/files in one consistent Windows view, with **drag-and-drop ingest** (no storage account provisioning, no infra setup). Introduces the **OneLake storage report**: item-level storage so you can spot what's driving footprint, including non-obvious things like **soft-deleted data and system folders** (logs/metadata/temp). Scenario: a lakehouse holds **4 TB of bronze data** kept for compliance but rarely touched after a few days — a common at-scale pattern. **Storage tiers + lifecycle management** then auto-move infrequently used data to **cool/cold tiers** (lower storage cost, higher transaction price only on access), with **default tiering rules** that are customizable. Reinforces enterprise management in one place: diagnostics events (who accessed data, optionally immutable), network protection rules, and CMK encryption. **Point proved:** you can see *and act on* storage cost/governance in the same place without separate tooling.

**Demo 2 — Unified estate with SharePoint list mirroring + Excel shortcuts (Rohan / "Zalva" / "Ziva").** Starts from a basic Fabric task flow (store → analyze/visualize → alert). A lakehouse is built from **shortcuts to several DB sources** — but critical data also lives in a **SharePoint list** (the ops team tracks readiness/staffing/build-out for 15 new stores across Atlanta, Chicago, Seattle, Miami). Old pain: export CSVs / Power Automate. New: **SharePoint list mirroring** — create a mirrored SharePoint Online list item (enter site URL or pick a connection, select the list, optionally auto-mirror future tables, name it, create). The mirror starts and shows **195 rows already replicated**; a **shortcut** to the mirrored list makes the data appear in the lakehouse with **no pipeline/copy job**. Then **Excel shortcuts**: the team's regional budget/forecast workbook (build-out costs, marketing spend, projected revenue) is shortcut in — Fabric detects the Excel file and turns **every sheet into a first-class table** ("two sources, one lakehouse, zero friction"). A **Power BI report** shows store readiness + staffing with **SharePoint-list data sitting next to Excel-workbook data**. Live update test: a regional manager bumps **Chicago staffing in Excel**; the store manager sets **Chicago status "ready to open" in the SharePoint list**; a report **refresh** lights up "Chicago ready to open, fully staffed, budget on track." **Point proved:** the single pane of glass — SharePoint, Excel, and databases all flow into one lakehouse and power one set of reports, using tools teams already know, with no CSVs/Power Automate/IT tickets.

**Demo 3 — Unify Fabric + Foundry for AI on unstructured data (Michaela).** Most orgs have valuable **unstructured** content in SharePoint (business docs, PDFs, Excel) that's disconnected from analytics/AI. In a Fabric **lakehouse**, unstructured SharePoint files live alongside structured data; because they're **OneLake shortcuts**, files are **virtualized in place** (no copy/movement/duplication), unified with **multi-cloud** data (S3, NetApp files behind network protection, Azure Blob holding customer-support transcripts). In **AI Foundry**, **knowledge** indexes this context (turning raw files into searchable/retrievable knowledge for grounding). The **OneLake catalog** (natively integrated) lets her search available data, see **endorsements** and **sensitivity labels** to judge trust, and confirm a **promoted** lakehouse is ready for broad use. She adds the **OneLake knowledge source** to an agent and asks a business question ("What are my best-selling products and how can I improve my sales?"). **Point proved:** connect to business data where it lives, unify structured + unstructured **without copying**, discover trusted data via the catalog, and ground a Foundry agent natively.

**Demo 4 — OneLake security end-to-end ("Zahara").** Platform admin **Zahara** consolidates sales data into OneLake via a **mirror database** (customers + sales). She creates **OneLake security roles**: a **non-PII** role (picks tables, then configures **column-level security (CLS)** to remove email and phone from the customers table; adds **Patrick**), and a **data science no-EU** role (allows PII but **restricts EU rows** for compliance; members **Diego** and **Priya**). Enforcement is then shown across engines: **Priya** (data scientist) verifies via the **SQL endpoint** (sees only allowed rows, identity honored), then **shortcuts** the data into her own lakehouse and queries with **Spark** (joining sales + customers) — **EU rows restricted seamlessly** for ML. **Diego** (sales manager) builds a **semantic model directly over the mirror tables using Direct Lake**; the **security roles are pulled into the model automatically**, and his **Power BI** report hides EU customers because he's in the no-EU role. **Patrick** (business analyst) uses the **OneLake catalog** to find Diego's report but the sales table is disabled (he's non-PII and can't see phone numbers); he then analyzes the semantic model **in Excel**, where **OneLake security automatically hides PII columns** while he still builds a pivot table. **Point proved:** "Secure your data once and have it be enforced everywhere" — across SQL endpoint, Spark, Direct Lake semantic models, Power BI, and Excel.

## 📊 Notable Stats / Quotes
- **35,000+** paying Fabric/OneLake customers.
- **80%+ of the Fortune 500** use OneLake/Fabric.
- **48 billion** OneLake service interactions **per day**.
- **9.4 million** active shortcuts across the ecosystem.
- **4× year-over-year** storage growth.
- **3+ million** storage accounts Microsoft manages for OneLake users.
- **240,000+** organizations worldwide trust the OneLake catalog.
- Demo specifics: **4 TB** bronze data kept for compliance; **195 rows** replicated via SharePoint list mirroring.
- *"OneLake... is the OneDrive for data."* — Deepti Borkar.
- *"OneLake really came in like a wrecking ball and busted open these silos, freed the data, and unified all into a single logical lake."* — Josh.
- *"There's always one lake per organization. You can never have more than one. You can never have less than one."* — Josh.
- *"Two sources, one lakehouse, zero friction."* — Rohan (demo).
- *"Secure your data once and have it be enforced everywhere."* — Josh (OneLake security).

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up a OneLake **shortcut** to an existing ADLS/S3 path and confirm **zero-copy** access in a lakehouse.
  - Test **SharePoint list mirroring** + **Excel shortcuts** to reproduce the "one report from three source types" pattern.
  - Enable **lifecycle management / data tiering** on a cold lakehouse (e.g. bronze) and measure storage-cost vs transaction-cost trade-off.
  - Define a **OneLake security** role (RLS + CLS) once and verify enforcement across SQL endpoint, Spark, Direct Lake, Power BI, and Excel.
  - Wire the **OneLake catalog → Foundry knowledge** path to ground an agent on structured + unstructured data with no copy.
- [ ] Questions:
  - Cost model details for **cool/cold tiers** (storage savings vs per-access transaction pricing) at real scale?
  - Latency/throughput of **mirroring CDC** for high-write OLTP sources (Oracle/SQL Server) — and limits on SharePoint list mirroring?
  - How do **OneLake security** definitions behave for **external engines** (Snowflake/Databricks) reading via the table API — are RLS/CLS enforced there too, or only inside Fabric engines?
  - GA timeline for **Azure Databricks native storage** and **AWS Glue** shortcut/mirroring?
- [ ] Relevant to:
  - Any data platform consolidating silos (ADLS + on-prem + SaaS) onto an open lake without ETL.
  - Teams grounding AI agents on enterprise data (Fabric + Foundry) needing trust signals (sensitivity labels, endorsements).
  - Governance/security owners needing one place to define RLS/CLS enforced across engines.

## 🔗 Related
- [[OD811 - Powering the next AI frontier with a unified data platform]] — sibling Fabric session on the unified data platform vision.
- [[OD818 - The AI-native Data Engineer]] — sibling Fabric session on the AI-native data engineering experience.
- [[OD812 - Fabric IQ Bringing enterprise intelligence into the developer workflow]] — sibling Fabric session in the same Build 2026 OneLake/Fabric track.
- [[Microsoft Fabric]] — the product OneLake is the foundation of.
- [[OneLake]] — the unified, open, AI-ready data lake covered in this session.
- [[Microsoft AI Foundry]] — AI platform that natively integrates the OneLake catalog for grounding agents.
- [[Delta Lake and Apache Iceberg]] — the open table formats OneLake exposes via the table API.
- Source list: [[2026 Build Session List]]

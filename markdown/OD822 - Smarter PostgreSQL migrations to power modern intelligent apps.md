---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/postgresql
  - topic/migration
  - topic/azure-database
  - topic/oracle-migration
  - topic/ai
source: https://www.youtube.com/watch?v=GbjjE9_3lWQ
session_code: OD822
event: Microsoft Build 2026
speakers: Guy Bowerman (with demos by Jonathan Frost)
duration_min: 28
aliases:
  - Smarter PostgreSQL migrations to power modern intelligent apps
---

# OD822 — Smarter PostgreSQL migrations to power modern, intelligent apps

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Guy Bowerman (Product Manager, Azure Database for PostgreSQL Flexible Server); demos presented by Jonathan Frost (Program Manager, Azure Postgres team)  
> **Duration:** ~28 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=GbjjE9_3lWQ)

## 🎯 TL;DR
PostgreSQL migration tooling on Azure is in a phase of rapid improvement — it's more accessible and cheaper than ever. This session makes the case for consolidating database workloads onto PostgreSQL (mature, open-source, no license fee, extensible for AI/GIS), and specifically onto **Azure Database for PostgreSQL Flexible Server** as a managed service that removes the total-cost-of-ownership burden of self-hosting. Guy Bowerman walks through recent performance/scale features (Premium SSD v2, V6 compute SKUs, cascading read replicas, elastic clusters/Citus) and Build 2026 announcements across migrate/maintain/monitor/build categories. The headline is the **AI-assisted Oracle-to-PostgreSQL migration tool** now in the VS Code Postgres extension — a multi-agent, self-correcting system that converts Oracle schema, database code, and application code at scale (validated on 2,000+ objects), demonstrated live by Jonathan Frost on schema conversion and a Java application migration.

## 🔑 Key Takeaways
- **Industry trend toward Postgres consolidation is accelerating** — driven by Postgres being a mature DB with a highly optimized query engine, an extension model suited to AI and industry-specific tech (e.g. GIS), open-source backing by an independent community, and **no license fee**.
- **Azure runs open-source Postgres "as is"** as a managed service with enterprise features — major customers like **OpenAI bet production workloads on managed Postgres on Azure**.
- **Total cost of ownership argument vs self-hosting on a VM/Kubernetes** — managed service removes overhead of HA, DR, scalability, configuration, security, compliance, maintenance, and major version upgrades. A **TechTarget study** found companies moving from self-managed to Azure Database for Postgres both saved cost AND got better application performance.
- **Microsoft contributes upstream** — has a team of independent Postgres committers; significant Postgres 18 features (query execution, async I/O, observability) were contributed by Microsoft committers, giving customers direct access to top experts.
- **VS Code Postgres extension is free and crossed 500K+ downloads** a few months ago; it's evolving from a dev environment into a full **database operations platform** (deploy, manage, monitor, troubleshoot, visualize).
- **Premium SSD v2 is now GA** — up to **80K IOPS**, **1.2 GiB/s throughput**, incremental space additions (pay only for what you need), ~4× transaction rate over SSD v1 with sub-millisecond latency.
- **Intel & AMD V6 compute SKUs now GA** — up to **3× memory** and **2× vCores** of V5, better per-core and price-performance; combined with upcoming **Ultra Disk** storage can reach **up to 400K IOPS**.
- **Cascading read replicas now GA** — a primary can replicate to read replicas that themselves replicate to another layer, up to **30 replicas** from one primary, supporting read scale-out and cross-region DR.
- **Elastic clusters (GA, uses the Citus extension)** — shard data across multiple Postgres nodes behind a single endpoint (shard by row or by schema); unique to Postgres on Azure among managed services and unlocks massive scale.
- **Postgres 18 + major version upgrade support added**, plus a **pre-upgrade validation check** to simulate upgrades and fix issues beforehand ("no surprises").
- **Maintenance control improvements** — defer a maintenance update for up to **two weeks** and apply updates **on demand** rather than waiting for a predefined window.
- **The flagship: AI-assisted Oracle-to-Postgres migration tool** in the VS Code Postgres extension — multi-agent, self-correcting schema/code/app conversion validated on **2,000+ objects**, addressing the historically complex and costly cross-database migration problem.
- **Postgres-to-Postgres migration is a one-step service** — point it at any source endpoint (VM, other services, and newly **EDB and Huawei** sources); supports online (minimal downtime) and offline (fewer limitations) migrations.
- **New monitoring/security additions** — Grafana dashboards in the Azure portal, free data mirroring to Microsoft Fabric, and Defender security assessments (public access, public schema/role access, PG audit settings).

## 📚 Detailed Notes

### Agenda & framing
Guy Bowerman (PM for Azure Database for PostgreSQL Flexible Server) structures the session around: (1) **why migrate** to Postgres, (2) **why on Azure** plus recent features and Build 2026 announcements, (3) **tooling for migrating Postgres workloads** to Azure, and (4) **migrating Oracle workloads** (schema, database code, apps) to Postgres on Azure. His thesis: migration tooling is improving rapidly, the technology is more accessible, and the cost is lower than ever.

### Why migrate to PostgreSQL
The industry trend to **consolidate database workloads onto Postgres is accelerating**, for several reasons:
- **Mature database service** with a **highly optimized query engine**.
- **Extension model** is "perfectly suited" to adapt to new technologies — whether the latest AI innovations or industry-specific tech like **GIS**.
- **Open source**, backed by an **independent community** with **no license fee** — cost is a key driver.

### Why PostgreSQL on Azure
Azure takes **open-source Postgres just as-is, with no changes**, and runs it as a **managed service** with the enterprise features needed for critical workloads. Evidence and rationale:
- Works with household-name customers; **OpenAI** is cited as willing to bet **production workloads on managed Postgres on Azure**.
- Microsoft builds the **enterprise features customers ask for** plus enterprise fundamentals (performance, security, reliability), while also investing heavily in the **developer community** — e.g. the **VS Code extension**, the **Azure AI extension**, and **Microsoft Foundry integration**.

### The self-host vs managed cost argument
Addressing "why not just self-host on a VM (or Kubernetes) in Azure?", Guy frames it around **total cost of ownership for a production workload**. Self-hosting in production carries ongoing overhead to "stay online" and meet requirements including: **high availability, disaster recovery, scalability, configuration, integration, security, compliance, maintenance updates, and major version upgrades** (and more). 

A **TechTarget study** measured before/after costs of self-managed vs Azure Database for PostgreSQL. In a managed environment where you can **scale compute and disk resources** and use features like the **built-in connection pooler**, companies were able to **not just save costs but also get better application performance** than running on-premises.

### Responsibility to the open-source community
Hosting an open-source database isn't only about cost — Azure has a responsibility to the **upstream open-source community**:
- Microsoft employs a team of **independent Postgres committers** — Microsoft doesn't tell them what to work on; they contribute to upstream open-source Postgres.
- In **Postgres 18**, significant features for **query execution, async I/O, and observability** were contributed by Microsoft committers.
- Benefit for customers: if they hit problems, Microsoft can reach out to **the top experts in the world** on these topics for help.

### Developer experience: the VS Code Postgres extension
- **Free to use** and "rapidly becoming a standard for Postgres developers" — it **passed half a million (500K+) downloads a few months ago**.
- More than a dev environment — becoming a **database operations platform**: deploy and manage Postgres, performance monitoring, troubleshooting, and visualization.
- Receives **regular updates / continuous improvement**, and is revisited later in the session in the **migration** context (it hosts the Oracle migration tooling).

### Staying current: the Postgres tech community blog
There is a tech community blog — **"Microsoft blog for Postgres"** — that **recaps the latest features every month**. It's positioned as a great resource for keeping up with the product/engineering teams, demonstrates the pace of development (a new set of features monthly), and includes guidance on where to find more information and how to use features.

### Performance & scale updates

**Premium SSD v2 (recently made Generally Available):**
- Enables **up to 80K IOPS** and **1.2 GiB/s throughput**; ideal for **I/O-intensive workloads**.
- **Incremental space additions** — if you need more space you add it and **pay only for what you need** (no need to double size and pay for all of it).
- A **PG bench test across five workload profiles (32 → 256 concurrent clients)** showed **SSD v1 maxing out at 20K IOPS** as concurrency rises, while **SSD v2 continues to scale to ~4× the transaction rate with sub-millisecond latency**.
- **Ultra Disk** (even higher-IOPS / more powerful storage) is **coming soon**.

**Intel & AMD V6 compute SKUs (now Generally Available):**
- Up to **3× the memory** and **double the vCores of V5**, with better per-core performance and better price-performance.
- Based on **5th-gen Intel Xeon** and **4th-gen AMD EPIC 9004**.
- With V6 SKUs + the upcoming **high-performance Ultra Disk** storage option, you can reach **up to 400K IOPS**.

**Scaling out — cascading read replicas (recently GA):**
- A Postgres **primary** can replicate to **read replicas**, which can in turn replicate to **another layer of read replicas**.
- Supports **up to 30 replicas from one primary** for read-heavy workloads, with flexibility to place replicas in **other regions** for **cross-region disaster recovery**.
- This is how customers like **OpenAI** achieve massive scale.

**Scaling out data — elastic clusters (GA for a while):**
- Uses the **Citus Postgres extension** — your app talks to **one Postgres endpoint** while data is **sharded across multiple Postgres nodes**.
- Overcomes the **storage and processing limits of a standalone server**; you can **shard by rows or by schema** depending on whether you want app changes and the level of parallelization desired.
- Can lead to **massive performance improvements**; this managed feature is **unique to Postgres on Azure**, is **tried and tested** (powering other Microsoft services behind the scenes), and "unlocks scale."
- Related recent additions: **Postgres 18** and **major version upgrade support**.

### Build 2026 announcements (organized: Migrate / Maintain / Monitor / Build)

**Migrate:**
- Deeper **AI-assisted migration features** (detailed later in the session).
- **Azure Migrate** added **PostgreSQL server discovery** and improvements — helps the **first phase of migration** (understanding what you have and need to migrate).

**Maintain:**
- A managed service needs maintenance (minor version updates to Postgres, security patches to the container OS). New controls give more say over timing:
  - **Defer a maintenance update for up to two weeks.**
  - **Apply an update on demand** instead of waiting for a predefined window — useful to avoid inconveniencing a production workload.
- For **major version upgrades**: extended **pre-upgrade validation check** so you can **simulate an upgrade and fix issues before applying**, targeting an upgrade "with no surprises."

**Monitor:**
- New **Grafana dashboard option** for Postgres in the **Azure portal** — easier, customizable monitoring.
- If you run analytics/reporting in **Microsoft Fabric**, you can **mirror your data from Postgres for free**; added support for more scenarios (e.g. **empty tables**, more **DDL data-definition-language operations**) for robustness.
- Added **Defender security assessments** to audit security posture — e.g. does the database have **public access**, **public schema access**, **public role access** (needing lockdown), or the **recommended PG audit settings**.

**Build:**
- Multiple improvements to the **VS Code Postgres extension**: **query plan visualization**, an **enhanced performance dashboard** (work with the **query store** to troubleshoot top queries), and more operations like **backup and restore**.
- Links provided to Build sessions showcasing these, and to the high-performance **Horizon DB** service (in **preview**).

### Postgres-to-Postgres migration tooling
For moving an existing Postgres workload (on-premises, in a VM, etc.) to Azure:
- A **migration service** moves it **in one step** — point it at the **source endpoint** and move it.
- Broad source support, including a VM and various services; **EDB and Huawei** were **recently added as sources**.
- **Online migration** (minimize downtime) or **offline migration** (fewer limitations, very easy setup).
- Supports **flexible server → flexible server** migration — not officially a supported option, but it works and can be useful for certain configuration changes that would otherwise require a point-in-time restore.

**How to reach/run it:**
- Run from the **Azure portal** or the **command line via Azure CLI**.
- Portal path: **create a new flexible server → select the migration option**, then select your source; it walks you **step by step** and lists **prerequisites**. The **list of checks is worth careful attention** and links to docs/tutorials.
- CLI has **full support built in**. If you hit limitations, you can fall back to open-source **pg_dump / restore** (a link to such scenarios is promised).

### Migrating Oracle workloads to Postgres on Azure
- **Number one driver: license cost.** Example shown is the list price of a **16-processor Oracle license** vs the **Postgres license cost of zero** — a "really compelling" reason. (Even with a discount, the contrast is stark.)
- **The historical blocker:** cross-database migration has always been **complex and therefore costly**, which stopped many from migrating.
- **Migration journey phases:** starts with **discovery and assessment**, but the most challenging/complex phases are:
  1. **Database schema** migration
  2. **Database code** migration (stored procedures, packages, triggers, etc.)
  3. **Application** migration (e.g. Spring Boot, Hibernate, .NET, Python apps)
  4. **Data** migration
- After landing in Postgres on Azure, there's substantial **performance tuning and cloud optimization** opportunity.
- Microsoft has added **its own tooling specifically for the first three complex phases** (schema, database code, application) to reduce complexity and cost.

### The AI-assisted Oracle-to-Postgres migration tool
- Available **now in the VS Code Postgres extension**.
- Handles the **Oracle schema, database code, and application code** phases of migration.

**How schema conversion works:**
1. **Extracts the Oracle schema** and **groups it into related objects**.
2. Uses an **LLM to create related chunks**.
3. Deploys a set of **schema conversion agents** that interact with the LLM to **generate the SQL code for Postgres**, **validate the code**, then make **further iterative improvements**.
4. The **final schema output** is available to review; **notes from this phase** are captured for the AI tooling to reuse in the **code conversion phases**.

**How application conversion works:**
- You create a **VS Code workspace migration project** and copy the application files locally.
- The extension leverages **GitHub Copilot agent mode** with **custom conversion blueprints and report templates** carried over from the schema conversion phase.
- Agents use **LMTs (large-language-model-based translation layers)** to convert code, queries, and application logic across technology stacks.
- It also uses an **Azure Database for PostgreSQL instance** to **validate versions and extensions** as it goes.

### Recap (speaker's closing)
The session recapped: reasons behind the industry trend to consolidate on Postgres; why Postgres on Azure; latest performance/scale features and Build 2026 announcements; Postgres-to-Postgres migration tooling; and the AI-assisted Oracle-to-Postgres tooling. Next steps/links were promised, including Build 2026 sessions (some only available at Build, others online) via the short link **aka.ms/postgres-on-azure-build-2026 (as spoken: "ak.ms postgres on azure build 2026")**, plus links to **Postgres documentation on migration and migration tools**.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Database for PostgreSQL Flexible Server** — the managed Postgres service at the center of the session.
- **VS Code PostgreSQL extension** — free; 500K+ downloads; dev + database operations platform; hosts the Oracle migration tool; query plan visualization, enhanced performance dashboard, query store, backup/restore.
- **Azure AI extension** & **Microsoft Foundry integration** — developer-experience investments for Postgres.
- **Premium SSD v2** — storage tier (80K IOPS, 1.2 GiB/s, incremental sizing). **SSD v1** (20K IOPS) referenced for comparison. **Ultra Disk** — higher-performance storage, coming soon.
- **V6 compute SKUs (Intel & AMD)** — 5th-gen Intel Xeon, 4th-gen AMD EPIC 9004; up to 3× memory / 2× vCores of **V5**.
- **Cascading read replicas** — up to 30 replicas, multi-layer, cross-region DR.
- **Elastic clusters** — built on the **Citus** Postgres extension; sharding by row or schema.
- **PostgreSQL 18** — with major-version-upgrade support; pre-upgrade validation check.
- **Azure Migrate** — PostgreSQL server discovery for the assessment phase.
- **Grafana dashboards** (in Azure portal) — monitoring.
- **Microsoft Fabric** — free data mirroring from Postgres for analytics/reporting.
- **Microsoft Defender** — security assessments (public access, public schema/role access, PG audit).
- **PostgreSQL migration service** — one-step Postgres-to-Postgres migration; online/offline; EDB & Huawei sources.
- **pg_dump / restore** — open-source fallback for migration edge cases.
- **GitHub Copilot agent mode** — drives application conversion with custom blueprints/templates.
- **LLM / LMTs (LLM-based translation layers)** — power schema/code/app conversion.
- **Azure OpenAI endpoint** — used in agent mode to scale migration to thousands of objects (per demo).
- **Java App Mod extension** — provides LMTs (build Java project, generate unit tests) leveraged during Java app conversion.
- **Horizon DB** — high-performance Postgres service, in **preview**.
- **Built-in connection pooler** — referenced in the TCO/cost study.
- **Citus**, **GIS**, **PG bench**, **Spring Boot / Hibernate / .NET / Python** — ecosystem/tech references.

## 🚀 Announcements / What's New
- **Premium SSD v2 — Generally Available** (80K IOPS, 1.2 GiB/s, incremental sizing).
- **Intel & AMD V6 compute SKUs — Generally Available** (up to 3× memory, 2× vCores of V5).
- **Cascading read replicas — Generally Available** (up to 30 replicas, multi-layer, cross-region DR capable).
- **PostgreSQL 18 support + major version upgrade support** added.
- **Pre-upgrade validation check** (extended) — simulate major version upgrades and fix issues first.
- **Maintenance controls** — defer maintenance updates up to two weeks; apply updates on demand.
- **Azure Migrate** — added PostgreSQL server discovery and improvements.
- **Grafana dashboard option** for Postgres in the Azure portal.
- **Microsoft Fabric mirroring** — free data mirroring with expanded scenario support (empty tables, more DDL operations).
- **Microsoft Defender security assessments** for Postgres.
- **VS Code Postgres extension** build improvements — query plan visualization, enhanced performance dashboard / query store troubleshooting, backup & restore operations.
- **AI-assisted Oracle-to-PostgreSQL migration tool** — available now in the VS Code Postgres extension (schema, database code, and application code conversion).
- **EDB and Huawei** added as **migration sources** for the Postgres migration service.
- **Ultra Disk** storage and **Horizon DB** service flagged as **coming soon / in preview** (forward-looking).

## 💡 Demos

### Demo 1 — Oracle → PostgreSQL schema conversion (presented by Jonathan Frost)
- **Create a migration project** in the Postgres extension and name it.
- **Connect to an Oracle server** via connection parameters — in this case **Oracle 19c**; list available schemas and select one or more to convert to Postgres.
- **Configure a scratch Postgres database** — used to **test each converted schema object and automatically fix discovered issues**. This **agentic self-correction approach against a live Postgres database significantly improves reliability**.
- **Connect to an Azure OpenAI endpoint** — used with **agent mode to scale migration to thousands of objects**, "something Copilot agent mode cannot do out of the box."
- Click **Migrate**: 
  - **Stage 1 — extract Oracle DDL** (shown via top progress bar).
  - **Stage 2 — convert each DDL chunk** via the **multi-agent orchestration workflow**; chunks are **compiled against the Postgres scratch database**. When **errors occur**, the **conversion agent takes them into account, reconverts, and recompiles** until successful, then applies the chunk.
  - **Coding notes** were captured (e.g. two notes) as **context items** that the **application conversion tooling later consumes**.
- A **comprehensive migration report** is generated showing **objects converted, object types, and Postgres extensions detected/used** for conversion context. This **test run processed 34 objects**; **customers have successfully tested at a scale of 2,000+ objects**.
- Use the extension's **visualize schema feature** to validate tables/relationships; **right-click a table (e.g. addresses) to compare the Oracle vs generated Postgres DDL side by side**.
- **Interactive mode**: after the initial conversion, for **every conversion issue that couldn't be resolved automatically**, the tool **creates a follow-up task for the developer** (shown as a table of tasks). For a **complex trigger** task, clicking **Run Task** generates a **custom prompt giving full context to agent mode**, which **recognizes the issue and provides a correction**; review the modified files, keep the changes, and **finalize the migration**.
- **Outcome:** connected to Oracle, converted its schema to Postgres format **at scale**, and **tracked/resolved complex issues in interactive mode**.

### Demo 2 — Oracle → PostgreSQL application code migration (Java app, presented by Jonathan Frost)
- Continuing from an existing **schema conversion project**, proceed to the wizard's **Application Conversion** step and click **Convert Application**.
- **Select the application codebase location** (a copy is in the root of the VS Code workspace) and a **Postgres database connection** to provide database context.
- This starts a **composite prompt** that invokes a **custom LMT** to convert the Oracle client application code to Postgres equivalents using the **target Postgres database context**. Along the way, additional **LMTs obtain the Postgres version and installed extensions**.
- **Coding notes from the recent schema migration are read in** to provide valuable context to the application conversion flow.
- The tool makes **resource and database connection changes** to the codebase, then **changes the ORM code to align with the Postgres table data types**.
- Calls the **Build Java Project LMT** (provided by the **Java App Mod extension**) — referencing this LMT in the blueprints lets the tool **leverage capabilities across related extensions**; the **build succeeds on the first try**.
- Calls the **Generate Unit Test LMT** (also from the Java App Mod extension) — **successfully generated and ran 30+ tests with a 100% passing rate**.
- A **comprehensive report** is generated and **opened automatically** when the flow completes.
- **Outcome:** converted an Oracle client application codebase to Postgres equivalents using a **combination of custom LMTs for code conversion and database context**, with the tool **detecting it was a Java app** and **leveraging the Java App Mod extension LMTs** for enhanced cross-extension capabilities.

## 📊 Notable Stats / Quotes
- **VS Code Postgres extension passed half a million (500K+) downloads** a few months ago.
- **Premium SSD v2:** up to **80K IOPS**, **1.2 GiB/s throughput**; **SSD v1 maxes at 20K IOPS**; SSD v2 reaches **~4× the transaction rate with sub-millisecond latency** (PG bench, 32–256 concurrent clients).
- **V6 compute SKUs:** up to **3× memory** and **2× vCores** of V5; with upcoming Ultra Disk, **up to 400K IOPS**.
- **Cascading read replicas:** up to **30 replicas** from one primary.
- **Oracle license example:** **16-processor license** list price vs **Postgres license cost = $0** — a "really compelling reason to look into migration."
- **Schema demo:** test run processed **34 objects**; **customers have tested at 2,000+ objects** scale.
- **App demo:** **30+ generated unit tests, 100% passing rate**, **build succeeded on the first try**.
- > "OpenAI is a good example… they're willing to bet their production workloads on managed Postgres running on Azure." — Guy Bowerman
- > "The Postgres license cost of zero — there's a really compelling reason to look into migration." — Guy Bowerman (on Oracle→Postgres license savings)
- > "The agentic self-correction approach using this live Postgres database significantly improves reliability of the migration process." — Jonathan Frost
- > "This endpoint is used in combination with agent mode to scale migration to thousands of objects, something Copilot agent mode cannot do out of the box." — Jonathan Frost

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install/update the **VS Code PostgreSQL extension** and explore the new **query plan visualization**, **performance dashboard / query store**, and **backup & restore** operations.
  - Spin up an **Oracle 19c** test instance and run the **AI-assisted Oracle→Postgres schema conversion** end-to-end (scratch DB + Azure OpenAI endpoint), then try **interactive mode** on a complex trigger.
  - Try the **Java application conversion** flow with the **Java App Mod extension** to see the build + unit-test LMTs in action.
  - Benchmark **Premium SSD v2** vs **SSD v1** with **pg_bench** on a flexible server; test **V6 SKU** price-performance.
  - Stand up **cascading read replicas** and an **elastic cluster (Citus)** to evaluate read scale-out and sharding-by-schema vs sharding-by-row.
  - Configure **Grafana dashboards**, **Fabric mirroring**, and **Defender security assessments** on a test server.
- [ ] Questions:
  - What LLM/model backs the schema conversion agents by default, and can the **Azure OpenAI endpoint** model be chosen/tuned? (App conversion is noted to use a Claude model via Copilot agent mode.)
  - What are the **cost implications** of the AI-assisted migration (Azure OpenAI token usage) at the 2,000+ object scale?
  - Where does **Ultra Disk** and **Horizon DB** sit on the roadmap (GA dates) and how do they compare to SSD v2 / standard flexible server?
  - Is **flexible-server → flexible-server** migration moving toward officially supported status?
  - Which exact source platforms are supported by the migration service beyond VM, **EDB**, and **Huawei**?
- [ ] Relevant to:
  - Any **Oracle→Postgres** modernization or license-cost-reduction initiative.
  - **Azure Database for PostgreSQL Flexible Server** planning, sizing, and performance/scale decisions.
  - Customers evaluating **managed vs self-hosted** Postgres TCO.
  - AI-assisted **database migration** demos and POCs.

## 🔗 Related
- aka.ms/postgres-on-azure-build-2026 — Build 2026 session links (some Build-only, some online)
- [[Microsoft Build 2026]]
- [[Azure Database for PostgreSQL]]
- [[PostgreSQL]]
- [[Oracle to PostgreSQL migration]]
- [[VS Code PostgreSQL extension]]
- [[Citus]]
- [[GitHub Copilot agent mode]]

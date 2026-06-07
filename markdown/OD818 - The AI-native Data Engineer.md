---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/data-engineering
  - topic/fabric
  - topic/ai
  - topic/analytics
source: https://www.youtube.com/watch?v=I-m7bUUprzY
session_code: OD818
event: Microsoft Build 2026
speakers: Pierro Morano (PM Lead, Developer Experience for Data Engineering & Data Science, Microsoft Fabric); Rocky Rockman (Principal Software Engineer, SQL Server Telemetry & Intelligence Team)
duration_min: 31
aliases:
  - The AI-native Data Engineer
---

# OD818 — The AI-native Data Engineer

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Pierro Morano — Product Management Lead for the developer experience for data engineering & data science in Microsoft Fabric; Rocky Rockman — Principal Software Engineer on the SQL Server telemetry & intelligence team (3–4 year Fabric customer)  
> **Duration:** ~31 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=I-m7bUUprzY)

## 🎯 TL;DR
This session reframes the data-engineering role for the AI era: the engineer still *owns* the architecture, quality, and outcomes, but delegates the implementation grind to AI. Pierro frames the shift from the "traditional" data engineer to the "AI-native" one and argues there is **no single best surface** — you match the AI interaction model (Fabric web portal, VS Code IDE, or CLI/terminal) to the task while keeping engineering control of the important decisions. Two product experiences anchor this: the enhanced **Copilot chat in Fabric notebooks** (web/portal) and the **Fabric Data Engineering extension for VS Code** (now MCP- and tools-enhanced so Copilot is Fabric-aware). A live demo shows a Fabric-aware notebook agent ingesting a streaming event-stream feed into a medallion (bronze→silver) architecture by reading repo "skills." Rocky then delivers the practical heart of the talk: the **"Ralph loop"** mentality — put AI in a tightly bounded box with a well-defined task and good hints, and let it work tirelessly — demonstrated on a real local dev-container setup that mounts production OneLake read-only (Blob Fuse), runs Spark locally (Livy + Fabric Spark), and uses Copilot CLI + deterministic CLI tools + AI-friendly code structure to build, test, and ship a bronze→silver pipeline that later runs at scale in Fabric Spark.

## 🔑 Key Takeaways
- The AI-native data engineer is **not a different person** — it's the same job evolved. The engineer keeps ownership of architecture, quality, and the end result; AI accelerates the *implementation*.
- **No single best surface.** Pick the tool for the task: Fabric web portal (zero setup, visual exploration, collaboration), VS Code IDE (professional dev workflow, GitHub Copilot, source control), CLI/terminal (scriptable, repeatable, automation-focused).
- **Match the AI interaction model to the task:** conversational/step-by-step for exploration, debugging, and ad-hoc analysis (stay close to the data); delegate-and-review for repeatable or operational work.
- Microsoft as a product team is investing **beyond code generation** — in the foundations that make AI useful for real engineers: APIs, tools, skills, and better context/experience.
- Two key experiences: **Copilot chat in Fabric notebooks** (portal) and the **Fabric Data Engineering VS Code extension** enhanced with **MCP and tools** to make a custom GitHub Copilot agent Fabric-aware.
- **"Skills" are repo-discoverable instruction files** (YAML front matter + markdown) that ground Copilot. In the demo, Copilot scanned a built-in folder, found two skills (E2E medallion architecture, event house authoring), and produced a solid implementation plan from them.
- Medallion ingestion best practices surfaced by Copilot: parse the raw JSON `value` string into columns, add metadata (ingestion timestamp, batch ID) for lineage, write to a Delta bronze table in **append-only** mode with a **checkpoint** (crash-safe resume, no dupes/loss), then validate row counts.
- **Stay in control with explicit constraints:** scope to specific phases (bronze + silver only), name explicit lakehouse targets, forbid edits to certain cells, and instruct Copilot to reuse existing setup — the demo did all of these.
- Rocky's core mental model: the **"Ralph loop"** (after Ralph Wiggum) — AI is a charming, simple, *tireless* worker; put it in a **context-bounded box** with a well-defined task and good hints and it will keep trying until it succeeds. Control comes from *you* providing rich, bounded context.
- **Mount production OneLake locally, read-only, via Blob Fuse** (standard Linux ADLS driver) inside a VS Code dev container, then use *local* compute (local Spark via Livy) to query real production Delta tables — "best of both worlds."
- **Parallelize AI across machines.** A single engineer can throw 10 Copilot CLIs across 10 GitHub Actions runners / dev boxes at a problem — doing the work of ~10 people — instead of serializing tasks themselves.
- **Author your code in an AI-friendly way.** A shared interface/trait (`DataTransformer`: `DataFrame → DataFrame`) lets you tell AI "control-F for this, reuse existing patterns, comply with our code" — bounding it to testable, on-pattern output, exactly like onboarding a human engineer.
- **Pair skills with deterministic CLI tools.** Skills give flexibility; deterministic tools (e.g. a TS tool that runs Spark SQL and returns markdown) give *repeatable* behavior the AI can invoke reliably.
- **Give AI the same "eyes" a human has.** Let it `DESCRIBE` tables, sample raw rows, and receive encoding hints (e.g. "the body is base64-encoded JSON") so it can do the same cognitive analysis you'd do visually — freeing you for higher-impact work (requirements, schema decisions).
- **Trust-building CI loop:** generate code + unit tests (seeded with a "North Star" gold-standard test), run Spark jobs locally, auto-fix-and-retry without a human in the loop, test on real OneLake production data via Azure DevOps/GitHub Actions *before* merging, then run the same Spark code in Fabric Spark at scale (up to ~200 nodes × 64 cores).
- The foundation persists even as models/tools churn: **ground AI in your context, structure code to be AI-extensible, and provide an excellent local dev environment.**

## 📚 Detailed Notes

### Framing: the role is evolving, not disappearing
Pierro opens by positioning AI as something that changes *how* engineers work — not merely by generating code, but by helping rethink the **full developer workflow** across Fabric, VS Code, and CLI. He contrasts two columns:
- **Traditional data engineer (left):** building pipelines, writing ETL logic, debugging issues, managing dependencies, ensuring data flows reliably. This work is *still critical*.
- **AI-native data engineer (right):** the *same* role, evolved. The engineer still owns **architecture, quality, and the end result**, but uses AI to accelerate implementation.

From a **product standpoint**, this means Microsoft invests not only in code generation but in the **foundations that make AI useful for real engineers**: APIs, tools, skills, and better context and experience. The encouragement to the audience: figure out which of these tools makes *you* more productive.

### Microsoft Fabric foundation (for newcomers)
Fabric brings the core experiences data teams need into **one unified platform**: databases, data orchestration, analytics, real-time intelligence, and Power BI. The point that matters in the AI age is that these experiences are **not isolated** — they're connected through the Fabric platform with **OneLake** as the common data foundation, plus shared governance and security.

### Choosing the right "power tool" — there is no single best surface
The key thesis: **no single surface is best for every engineer or every task.** Three surfaces, each with a sweet spot:
1. **Fabric web portal** — great for **zero setup**, visual exploration, collaboration, and quick access to data.
2. **IDE in VS Code** — where many professional developers and data engineers are most productive: **GitHub Copilot, source control**, and more.
3. **CLI / terminal** — best when the task is **scriptable, repeatable, and automation-focused**.

### Matching the AI *interaction model* to the task
Not every task needs the same AI experience:
- **Exploration, debugging, ad-hoc analysis** → want a **conversational flow**: stay close to the data and guide the AI step by step.
- **Repeatable / operational work** → **delegate more of the execution** while you review the plan and results.

The simple rule: *match the AI interaction model to the task and keep engineering control of the important decisions.*

### The two anchor experiences
1. **Enhanced Copilot chat in Fabric notebooks** — helps users work directly in the **Fabric portal**.
2. **Fabric Data Engineering extension in VS Code** — now enhanced with **MCP (Model Context Protocol) and tools** that make a **custom GitHub Copilot agent aware of Fabric context** (e.g. it can resolve lakehouses, interact with Fabric resources).

### Demo 1 — Fabric-aware notebook agent: streaming event-stream → medallion (bronze→silver)
**Scenario:** read an event stream in a **Spark notebook leveraging Kafka**, bridging Spark and **RTI (Real-Time Intelligence)** in Fabric. The stream arrives as JSON; goal is to transform it into Delta tables following **medallion architecture** and **event hub / event house** best practices. The presenter admits being *unfamiliar with streaming*, so leans on Copilot — a deliberate "learn-with-AI" framing.

**Notebook setup:**
- Done in the **new Fabric Data Engineering VS Code extension**, using the **new Fabric-aware notebook agent mode** to integrate a new *social media feed* from an event stream.
- **Cell 1** = a parameter cell. **Cell 2** = connects to the Fabric event stream as a **Kafka source**, decoding the binary key/value columns to strings.
- Running the cells, events start arriving — each record is a **JSON payload with customer-feedback details**.

**Prompt to Copilot (paraphrased from transcript):** *"Can you check this notebook that reads from event-streaming social media feeds and suggest a plan to incorporate it into our medallion architecture and event house authoring best practices in my built-in folders?"*

**How Copilot grounded itself:** it **scanned the built-in folder** and discovered **two available skills** — *E2E medallion architecture* and *event house authoring*. By reading the **medallion architecture skill**, it generated a solid implementation plan.

**Plan — Phase 1 (Bronze layer):**
1. **Parse the `value` column** (currently one big JSON string) into structured form.
2. **Add tracking / metadata columns** — break the payload into individual columns and add **ingestion timestamp** and **batch ID** so every record can be traced back to its source.
3. **Write to a Delta bronze table in append-only mode**, adding a **checkpoint** — so if the notebook crashes and restarts it picks up exactly where it left off, avoiding duplicates or data loss.
4. **Validate** — check row counts to confirm data is flowing.

**Plan — Silver layer:** read from the bronze Delta table just created, apply **quality rules** (e.g. remove duplicates), do **schema conformance**, and write **curated data to a silver table**. The plan also proposed *additional* steps — a **gold layer**, **event house optimizations**, and even a **graphical view of the proposed architecture**.

**Staying in control (the key teaching moment):** rather than letting Copilot run the whole plan, the presenter constrains it:
- Continue with **Phase 1 and Phase 2 only** (bronze + silver).
- Make **lakehouse targets explicit**: `Retail LH` for bronze, `Retail curated LH` for silver.
- **Preserve existing setup** — do **not** modify the first two cells; implement everything **starting from cell 3**, keeping all new steps in the same notebook.

Copilot identifies the two lakehouses using the **Fabric notebook MCP server**, proceeds with the plan, leaves the first two cells untouched, and adds **clear markdown cells** (handy for team collaboration). After a few iterations the final notebook has readable markdown cells, a cell to control the incoming streaming data, etc.

**Execution:** the presenter asks Copilot to **run the notebook** and to **skip one debugging cell**. Copilot understands the current cell organization, runs it, and during execution **confirms the number of incoming streaming records** being written into the bronze and silver tables. On completion, data is visibly flowing through the pipeline — transformed from the original JSON events into Delta tables in the bronze and silver lakehouses. *"This saved me a significant amount of time."* Closing best practice: **have another team member review and validate** the notebook before moving forward.

### Rocky's mental model — the "Ralph loop"
Rocky introduces AI through **Ralph Wiggum** (The Simpsons): charming, simple, *not too bright but extremely hard-working*. Give Ralph a task **plus the hints** to achieve it, and he becomes the **hardest worker in the room**. In AI terms this is the **"Ralph loop"** (a real, momentum-gaining industry term — he suggests searching for it). The essence:
- Place AI into a **context-bounded box** with a **well-defined task**.
- Like Ralph, AI will **try its hardest** to achieve what you asked — but **it's up to you to place it in the right context**.

This frame recurs throughout: control and quality come from *bounding* the AI well, not from babysitting every keystroke.

### Rocky's team architecture & workflow
**Ingestion:** like other enterprises, the team uses the **medallion architecture**. Data arrives at **very high velocity** from all sorts of sources (e.g. Kafka, as Pierro showed) and lands in **Delta Lake** as **bronze** — *no schema, no structure, no columnar compression*.

**First job of the data engineer — "schema on read":** apply a robust schema to the bronze data. The schema may be complex (XML, nested JSON, etc.). Get it into **columnar format** and store it in Delta Lake in a **well-compressed structure** so queries run fast.

**The local-compute trick (3 years of OneLake experience):** because Rocky works in **VS Code**, he wants to use the **compute power of his local machine** against **production data in OneLake**:
- Windows users know **OneLake Explorer**; here he uses a **Linux VS Code dev container** with a mount called **Blob Fuse** — a standard Linux driver (search "Blob Fuse driver for ADLS"). It mounts **OneLake as a read-only mount** into the local file system.
- On screen: `/tmp/mount/onelake` (shown as "TMP mount One Lake") — a local drive exposing OneLake Delta tables locally. In the demo, **three lakehouses** from the Fabric production workspace are mounted, with **hundreds of Delta tables** (high-partition data) visible via `tree`.

**Simulating Fabric Spark locally:** the team runs **Spark locally** to use local compute on data living in OneLake. The local stack:
- **Livy server** (REST API to Spark), **Fabric Spark**, the **Hive API**, and the **Copilot CLI**.
- Transform with regular Spark code (**PySpark or Scala**) *or* with **dbt (Data Build Tool)** — explicitly called out as **gaining a lot of traction** in the industry.
- **All of it is open source**, with **GitHub links** provided to reproduce the demo locally.

**Testing & confidence loop:** any locally written code runs **full unit tests and full integration tests** — on **production data**, on the local computer. Then:
- **Parallelize with the Ralph loop across machines** — e.g. GitHub Actions CI machines or multiple dev boxes — running the loop **across 10 different machines**, effectively doing the work of **10 users**. Where Rocky previously *serialized* tasks (and got less done than the business needed), AI lets even a **single person parallelize** and "throw AI at the data-engineering problem" — while staying **fully in control**, because the human supplies lots of input (Ralph in his box).
- **Build confidence before merge:** use **Azure DevOps or GitHub Actions** to test the generated code on **OneLake's production data** *before* merging the PR into `main`.
- **Scale up in Fabric on merge:** after merging to `main`, the **same Spark code** runs on **Fabric Spark**, scaling to **~200 nodes with 64 cores** — far beyond local capacity. Net: **best of both worlds**, with the pipeline running confidently in production.

### Demo 2 — local dev container, Copilot CLI, and a bronze→silver pipeline
**Environment orientation:** Rocky is inside **VS Code running in the dev container**, with the **Fabric Data Engineering extension** to interact with Fabric. On screen is a **Copilot skill** — authored as **YAML front matter** (so the Copilot CLI can *discover* what the skill does) plus **markdown** body.

**Starting up:** he turns on the **locally running Copilot CLI**, then shows OneLake mounted locally (`tree` of `/tmp/.../mount` → three production lakehouses; `tree -L 4` reveals the many Delta tables and high partitions). This is "production OneLake mounted locally."

**The task:** ingest a **brand-new data source** requested of him, moving it from **bronze → silver** (or gold).

**Firing the skill (bounding the box):**
- He copies the skill's path and "fires it" into the Copilot task — the **"Spark bronze to silver"** skill.
- The **most important part is the authoring of the skill**, which immediately places Copilot (here running **Claude Opus** — caption "Cloud Opus") into a **bounded box**:
  - **"You're not allowed to commit the code. You're not allowed to add the code. I'm going to review everything you produce."**
  - **Hints about the codebase structure** — it's a **Scala** codebase, **quite complex**, at least **a few hundred thousand lines of code** (serving the **SQL Server OneLake data lake**).
- Crucial efficiency lesson: **don't let Copilot rediscover the whole codebase every time** — you'll **run out of the context window**. Instead, tell it the team's pattern: **loader classes, transformer classes, driver classes**; **reuse as much code as possible**, **run unit tests**, **run the Spark jobs**, then **vacuum the table** so production tables are in good format.

**Copilot picks up context** while reading, then asks **which bronze tables to transform to silver** (full database + table name).

**The vibe-coded local UI:** Rocky shows a small **UI he "vibe coded" for his team**, using **Livy as an API** to query local Spark, and **local Spark to query OneLake**. He picks an example table (an **"Arc SQL Server extension"** block), pastes a query, clicks **Run** — Livy on the local dev container + local Spark queries OneLake (possibly on the other side of the world) and returns the data. The **bronze data has no schema**; the **body is unreadable by a human** — a **binary-encoded payload**. That's "bronze."

**Handing the bronze sample back to Copilot — and the deterministic-tools lesson:**
- He pastes the table reference back to Copilot. Key point: **skills are great, but you also want deterministic code the AI can invoke** for **repeatable behavior**.
- His team built **deterministic CLI tools** — e.g. an `index.ts` skill/tool that lets a human *or* Copilot **run regular Spark SQL statements and get results back as markdown**.
- Copilot then **`DESCRIBE`s the table** to learn the schema and **samples the raw data** to see the data's shape.

**Encoding hints — giving AI "the same eyes":** you must tell it the **encoding** — in Rocky's case the body is **base64-encoded JSON**. With these tips Copilot figures out the data's shape. The insight: the **same cognitive analysis a human does by eye** (look at the data, infer structure) can be handed to Copilot by giving it the **same eyes and tools** (describe, sample, encoding hints). Then the manual grunt work — figuring out gzip compression, decoding, etc. — gets **delegated to the machine**, freeing the engineer to gather requirements and make schema decisions (the **higher-impact** work).

**End-to-end walkthrough (kept running in the background "in the interest of time"):**
- **AI-friendly code authoring is the most important thing.** Analogy: a new human engineer can't grok an unstructured codebase; **AI has a context window** and can't read a billion lines either. So the team **interfaces all code** through an `extends DataTransformer` trait.
- The **`DataTransformer` trait** defines a single **transformation method: `DataFrame → DataFrame`**. **Every** data transformer in the (huge) codebase implements it. You can `control-F` for `extends DataTransformer` and find them all.
- Why it matters: you **don't want AI writing untestable, off-pattern code**. Bounding it to the trait keeps output **testable and on-pattern**. Rocky literally tells AI: *"search for it, control-F for it, look at my existing coding patterns, and any new code you generate has to comply with the code I have."* It's like **onboarding a human engineer** with your best practices.
- Copilot then **figures out the body format, data types, timestamps, JSON structure** — deterministically, **at machine speed**. He further instructs it to **reuse existing code** rather than creating new classes — *"put the code in the best class where you think this data belongs"* — and it reuses, e.g., the team's `T&I` (team name) **JSON transformations**.

**Design proposal + guardrails:**
- AI presents a **comprehensive design proposal**: the **schema** and the **destination table**. It then **pauses and prompts** ("pause, do not proceed") — and **~10 times out of 10 it complies** with the stop instruction.
- After validation, you tell it to **write the code**; you also pass **coding standards** — e.g. **register new tables for liquid clustering and vacuuming**.

**Unit tests via a "North Star" gold standard:**
- Finally, AI is asked to **generate unit tests**. Rocky gives it a **gold-standard reference test** — an **OpenTelemetry columnar integration test** — as a **North Star**, so AI doesn't have to invent what good tests look like; it knows the team's **robust best-practice** expectations and generates matching test code.

**Running the job + autonomous fix loop:**
- AI runs the **Spark job** (created via a **Spark job definition**) **locally** — again, you need a **CLI tool** that takes the **driver class** and runs it.
- AI **keeps running the code**; if it fails, it **makes code changes, rebuilds the JAR, reruns the tests** — doing all of this **without the human in the loop**.
- This might take **1 hour, 2 hours, or 30 minutes — it doesn't matter.** When everything is tested, **open the PR**, and the code quality is *"as good as if I sat here and wrote it myself."*

**Rocky's one-line summary of working with AI:** *"Ground it in context, put it inside a box, and let Ralph Wiggum do what he does best — keep trying until what you asked for succeeds."*

### Closing principles (durable beyond any single tool)
Rocky and Pierro converge on a foundation that survives the daily churn of new models, tools, and skill sets:
1. **Ground AI in your context** — repo structure, patterns, encoding, gold-standard examples.
2. **Write code in an AI-extensible manner** — shared interfaces/traits, consistent patterns AI can find and comply with.
3. **Have an excellent local development environment** — e.g. the **VS Code dev container**, with CI on **GitHub Actions** when PRs merge.

**The full pipeline, end to end:** dev container on VS Code locally → test via GitHub Actions on PR merge → fan out to **10 GitHub Action machines, throwing 10 Copilot CLIs at the same problem** → merge the unit tests → push to **Fabric**, where the code runs **with as much confidence as needed**. Rocky shares **two Git repos** (his GitHub handle): one **dev container** to build/reproduce locally, and one with **sample code** showing the **GitHub skills and patterns**.

Pierro wraps up: in a short demo Rocky **encapsulated many Fabric features and workloads**. For those less familiar with Fabric, links to **documentation, tutorials, and the YouTube channel** are shared (subscribe and give feedback).

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Fabric** — unified data platform spanning databases, data orchestration, analytics, real-time intelligence, and Power BI; the connective tissue for the whole session.
- **OneLake** — Fabric's common data foundation (single logical data lake) with shared governance and security; mounted locally read-only in Rocky's demo.
- **OneLake Explorer** — Windows tool for browsing OneLake locally (Rocky uses Blob Fuse on Linux instead).
- **Copilot chat in Fabric notebooks** — newly enhanced; lets users work with AI directly in the Fabric portal (the web-first surface).
- **Fabric Data Engineering extension for VS Code** — IDE extension enhanced with **MCP and tools** so a custom GitHub Copilot agent is **Fabric-aware**; includes a **Fabric-aware notebook agent mode**.
- **Fabric notebook MCP server** — MCP server used by the agent to resolve Fabric resources (e.g. identify the bronze/silver lakehouses).
- **GitHub Copilot** — AI assistant used both in VS Code (notebook agent) and as **Copilot CLI** (terminal).
- **Copilot CLI** — terminal-based Copilot used in Rocky's local dev-container demo to drive the bronze→silver pipeline.
- **Claude Opus** (caption: "Cloud Opus") — the model Rocky runs inside the Copilot CLI for his demo.
- **Spark / Apache Spark** — distributed compute engine; run **locally** in the demo and at scale in **Fabric Spark**.
- **Fabric Spark** — managed Spark in Fabric; scales to **~200 nodes × 64 cores** for production runs.
- **PySpark / Scala** — the two Spark languages referenced; Rocky's production codebase is **Scala** (hundreds of thousands of LOC).
- **dbt (Data Build Tool)** — transformation tool called out as gaining significant industry traction; usable in the local workflow.
- **Livy** — REST API server fronting Spark; used to query local Spark (and via it, OneLake) from a vibe-coded UI.
- **Hive API** — part of Rocky's local Spark stack.
- **Delta Lake / Delta tables** — open table format for the medallion layers (bronze/silver/gold).
- **Blob Fuse** — standard Linux ADLS driver used to mount OneLake as a **read-only** local file system inside the dev container.
- **ADLS (Azure Data Lake Storage)** — the storage layer Blob Fuse targets.
- **VS Code dev container** — Linux containerized dev environment hosting the whole local toolchain.
- **Kafka** — protocol/source used to read the Fabric event stream into the Spark notebook.
- **Event stream / Eventstream + RTI (Real-Time Intelligence)** — Fabric streaming ingestion bridged into Spark in Demo 1.
- **Event House** — Fabric real-time analytics store; "event house authoring" is one of the discovered skills and a best-practice target.
- **Copilot "skills"** — repo-discoverable instruction files (**YAML front matter + markdown**) that ground Copilot; examples: *E2E medallion architecture*, *event house authoring*, *Spark bronze-to-silver*.
- **Deterministic CLI tools** (e.g. an `index.ts` tool) — custom tools that run **Spark SQL** and return **markdown**, giving the AI repeatable, invokable behavior.
- **`DataTransformer` trait/interface** — Scala interface (`DataFrame → DataFrame`) every transformer implements, used to bound and constrain AI-generated code.
- **Spark job definition** — Fabric construct used to run the generated Spark driver class locally and in Fabric.
- **Liquid clustering & VACUUM / table vacuuming** — Delta optimizations the AI is instructed to register/apply for healthy production tables.
- **OpenTelemetry columnar integration test** — the "North Star" gold-standard unit/integration test Rocky feeds the AI as a quality reference.
- **GitHub Actions / Azure DevOps** — CI used to test generated code on **production OneLake data** before merge, and to parallelize Copilot CLIs across runners.
- **Power BI** — named as one of Fabric's unified experiences.
- **The "Ralph loop"** — industry term/pattern (after Ralph Wiggum) for putting AI in a context-bounded box with a well-defined task and letting it iterate to success.

## 🚀 Announcements / What's New
- **Fabric Data Engineering VS Code extension — enhanced with MCP and tools** so a custom GitHub Copilot agent becomes **Fabric-aware**, including a new **Fabric-aware notebook agent mode** (resolves lakehouses, interacts with Fabric via the Fabric notebook MCP server). Presented as newly enhanced; specific preview/GA status was not stated.
- **Enhanced Copilot chat in Fabric notebooks** — "newly enhanced" experience for working with AI directly in the Fabric portal. Preview/GA status not specified.
- No formal GA dates, pricing, or roadmap milestones were called out — the session is **capability/workflow-focused** rather than a launch announcement. Treat the above as "newly enhanced experiences shown," not dated releases.

## 💡 Demos
- **Demo 1 — Fabric-aware notebook agent: streaming → medallion (bronze→silver).** In the new Fabric Data Engineering VS Code extension, a Spark notebook reads a Fabric **event stream via Kafka** (JSON customer-feedback payloads). Copilot scans a built-in folder, discovers the **medallion** and **event house authoring** skills, and proposes a phased plan (bronze: parse value, add ingestion-timestamp/batch-ID metadata, append-only Delta write with checkpoint, validate row counts; silver: dedupe, schema conformance, curated table; plus optional gold/event-house/diagram). The presenter constrains it to **bronze+silver only**, names explicit lakehouses (**Retail LH**, **Retail curated LH**), forbids editing cells 1–2, and runs the notebook (skipping a debug cell). **Proves:** an unfamiliar engineer can ingest a streaming source into a best-practice medallion pipeline by grounding Copilot in repo skills while retaining tight control — and it visibly writes records into bronze/silver Delta tables.
- **Demo 2 — Local dev container + Copilot CLI bronze→silver on production OneLake.** Rocky shows **OneLake mounted read-only locally** (Blob Fuse; three production lakehouses, hundreds of Delta tables), **Spark running locally** queried via **Livy** from a **vibe-coded UI**, and the **Copilot CLI (Claude Opus)** firing a **"Spark bronze-to-silver" skill**. He bounds the AI (no commit/add, human review, reuse loader/transformer/driver classes, comply with the `DataTransformer` trait), feeds a **bronze sample + base64-JSON encoding hint** plus a **deterministic SQL CLI tool**, and walks the end-to-end loop: design proposal → write code → register liquid clustering/vacuum → generate unit tests against an **OpenTelemetry gold-standard test** → run the Spark job locally → **auto-fix/rebuild/retest without a human** → open PR. **Proves:** with the right context, deterministic tools, and AI-friendly code structure, AI produces production-quality, on-pattern, tested pipeline code, parallelizable across many machines.

## 📊 Notable Stats / Quotes
- **"This is not a different person. It is the evolution of the same job"** — Pierro, on the AI-native data engineer (the engineer still owns architecture, quality, and outcomes).
- **"Match the AI interaction model to the task and keep the engineering control of the important decisions."** — Pierro's core rule for choosing surfaces/interaction styles.
- **"Ground it in context, put it inside a box, and let Ralph Wiggum do what he does best — keep trying until what you asked for succeeds."** — Rocky's one-line philosophy.
- **~3–4 years** — how long Rocky's team has been a Fabric customer.
- **A few hundred thousand+ lines of Scala** — size of the production codebase serving the SQL Server OneLake data lake (why context-window discipline matters).
- **~200 nodes × 64 cores** — scale Fabric Spark can reach for production runs (vs. limited local compute).
- **10 machines / 10 Copilot CLIs** — Rocky can parallelize the Ralph loop across ~10 GitHub Action runners/dev boxes, doing the work of ~10 people as a single engineer.
- **"~10 times out of 10"** — how reliably the AI obeys an explicit "pause, do not proceed" instruction when properly bounded.
- **"1 hour, 2 hours, or 30 minutes — it doesn't matter"** — Rocky on the autonomous fix-build-test loop running unattended until the job succeeds.
- Auto-caption notes: speaker name appears as **"Pierro Morano" / "Piero"** (likely *Pierro*); model **"Cloud Opus"** is **Claude Opus**; **"vibe coded"** UI; **"Arc SQL Server extension"** table; team initials rendered **"T&I"**. Corrected sensibly; not fabricated.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Mount **OneLake read-only via Blob Fuse** in a Linux **VS Code dev container** and query production Delta tables with **local Spark + Livy**.
  - Author a **Copilot "skill"** (YAML front matter + markdown) for a real bronze→silver transform; pair it with a **deterministic SQL CLI tool** that returns markdown.
  - Adopt an **AI-friendly code interface** (a `DataTransformer`-style `DataFrame → DataFrame` trait) so AI output stays testable and on-pattern.
  - Seed AI with a **gold-standard "North Star" unit/integration test** before asking it to generate tests.
  - Try the **Fabric Data Engineering VS Code extension** notebook agent mode against a Kafka event stream for a medallion ingest.
  - Experiment with **parallel Copilot CLIs across GitHub Actions runners** (the "Ralph loop" at scale).
  - Find and clone **Rocky's two GitHub repos** (dev container + sample skills/patterns) — links shown at end of the talk.
- [ ] Questions:
  - What are the **preview/GA status and licensing** for the enhanced Copilot-in-notebooks and the MCP-enhanced VS Code extension?
  - How is **read-only Blob Fuse access to production OneLake** secured/governed (auth, RBAC, data egress) for local compute?
  - How does **context-window cost** scale on a few-hundred-thousand-LOC repo even with loader/transformer/driver hints — what's the practical token budget?
  - Where does **dbt** fit vs. native Spark in the Fabric-recommended pattern?
  - What does the **Fabric notebook MCP server** expose as tools, and can it be used outside the notebook agent?
- [ ] Relevant to:
  - Anyone building **medallion (bronze/silver/gold) pipelines** in Microsoft Fabric.
  - **Data engineers** modernizing ETL with AI while keeping architectural control.
  - Teams wanting a **local-dev + CI + Fabric-Spark-at-scale** workflow on OneLake.
  - **Platform/DevEx leads** evaluating Copilot skills, MCP, and AI-friendly code standards.

## 🔗 Related
- [[Microsoft Fabric]] / [[OneLake]] — the lakehouse + governed-storage foundation this session builds on.
- [[Fabric Data Engineering extension for VS Code]] / [[Copilot chat in Fabric notebooks]] — the two AI surfaces demoed (IDE vs portal).
- [[GitHub Copilot CLI]] / [[MCP (Model Context Protocol)]] — the terminal-agent + Fabric-aware tooling path ("Ralph loop").
- [[Medallion architecture]] (bronze → silver → gold) — the pipeline pattern both demos implement.
- [[OD812 - Fabric IQ Bringing enterprise intelligence into the developer workflow]] — sibling Fabric session (semantic/ontology layer above the data-engineering layer).
- Related Build 2026 Fabric sessions: **OD811** (unified data platform), **OD815** (AI-ready data lake), **OD819** (Real-Time Intelligence), **OD817** (agentic analytics with Power BI).
- Source list: [[2026 Build Session List]]

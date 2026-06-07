---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/azure
  - topic/databases
  - topic/ai
source: https://www.youtube.com/watch?v=E5PHOR7cz2w
session_code: BRK223
event: Microsoft Build 2026
speakers: Charles Federson
duration_min: 45
aliases:
  - From rows to reasoning
  - Designing databases for AI apps and agents
  - Horizon DB session
---

# BRK223 — From rows to reasoning: Designing databases for AI apps and agents

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Charles Federson (Lead PM, Postgres @ Microsoft, host) · James (Cosmos DB expert) · Bob (SQL expert) · Abe (Postgres / Horizon DB expert)  
> **Duration:** ~45 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=E5PHOR7cz2w)  
> **Code:** GitHub repo `aka.ms/build26/BRK223` (all demos + more)

## 🎯 TL;DR
A fast, demo-heavy tour of how Microsoft's three flagship database engines — **Cosmos DB**, **Azure SQL**, and **PostgreSQL** — are evolving to natively power AI apps and agents, so application logic (memory, embeddings, search, orchestration) can live *inside* the database rather than in external Python services. The headline announcement is **Azure Horizon DB**, a brand-new Postgres service that **separates compute from storage** (true open-source Postgres on top of a new log/page-server storage engine on Azure Storage), delivering **~3× transactional throughput** (~11.5–12K TPS vs ~4K for self-managed Postgres) and AI features baked in (AI model management, AI pipelines via the new **PG durable** extension, DiskANN vector search). Cosmos DB gains an **Agent Memory Toolkit** for agent short-/long-term memory, and Azure SQL gains a new **Azure SQL container** (private preview) for offline-first local dev that moves to Azure SQL Hyperscale unchanged. The throughline: **bring AI into the database** and keep the same code from laptop to cloud.

## 🔑 Key Takeaways
- **Three engines, one theme:** Cosmos DB (planet-scale NoSQL), Azure SQL (30+ yr relational engine), and PostgreSQL are all being re-engineered so AI workloads (memory, embeddings, vector/hybrid search, agent orchestration) run *natively in the database*.
- **Cosmos DB → Agent Memory Toolkit:** A new Python SDK + accelerator that generates, processes, stores, and retrieves agentic memories. Uses Cosmos DB **change feed** + **Azure Durable Functions** + **Microsoft Foundry** models to turn short-term memories into long-term (episodic/procedural/fact) memories automatically.
- **Azure SQL → Azure SQL container (private preview):** A *versionless* SQL Server that runs locally on your laptop but **behaves like Azure SQL**, including local AI models for embedding + inference. Build AI apps offline-first, then move to Azure SQL Database / Hyperscale with **identical T-SQL**.
- **Azure SQL → AI inside the engine:** Demonstrated regex parsing of unstructured text into JSON, **vector hybrid search** (new `vector search` T-SQL with `TOP ... APPROXIMATE`, `vector_distance`, vector index seek + JSON index seek), and an in-DB agent that mitigates incidents — all on a laptop.
- **Horizon DB is the big announcement:** A new Azure Postgres service that **separates compute and storage**. Above the line = **true open-source Postgres** (not a derivative); below = a new storage engine (log/WAL server + page servers, backed by Azure Storage, striped across availability zones).
- **Horizon DB performance:** Up to **3× faster** transactional processing and vector search. Live TPC benchmark: self-managed Postgres on VMs ≈ **4,000 TPS** vs Horizon DB ≈ **11,500–12,000 TPS**, same region/hardware/AZs.
- **Horizon DB scale & resilience:** Storage **autoscales to 128 TB**, zone-redundant ("zone-resilient") with cross-zone failover; scale out across read replicas "with a couple of clicks" — **no re-architecture, no downtime**.
- **AI Model Management (Horizon DB):** Pre-register Foundry models (e.g. embedding, chat, **Cohere rerank**) at provisioning time, then invoke them directly via **SQL AI functions** (embedding generation, re-ranking) — no separate Foundry plumbing needed.
- **AI Pipelines via PG durable:** New **open-source** extension (`Microsoft/PG durable`) that implements **durable functions natively in Postgres**. Lets you create RAG pipelines (chunk → embed → store) in **~8 lines of SQL**, running asynchronously in the background so OLTP write latency (milliseconds) is unaffected.
- **Postgres community investment is huge:** Microsoft made **~11% of all commits** to Postgres 19 (~**64,000 lines changed**, ~**8% of all changes**), including async I/O in the query engine and observability work. Postgres 19 ships ~**end of September**.
- **Zero cloud lag for major versions:** Microsoft lit up **Postgres 18** in the managed service on the **same day** as community GA (vs a 6-month wait for PG 15/16 a few years ago).
- **Deep VS Code tooling:** Object explorer, GitHub Copilot authoring SQL, redesigned **visual query plans** (tree + table view) with a **Copilot icon on every operator** for AI-assisted query debugging in agent mode, real-time live monitoring dashboards, and visual pipeline debugging. **Works against any Postgres** (local or any cloud).
- **"In the database" philosophy:** Charles repeatedly argues for putting application/AI logic *in* the database — the point is **choice**, and Horizon makes the in-DB path first-class.
- **Demo honesty:** The live Horizon DB RAG ingestion demo failed twice on stage ("praying to the demo gods"); the presenter fell back to a pre-run backup cluster — a real-world reminder that the pipeline is async and depends on correct DB/table targeting.

## 📚 Detailed Notes

### Framing & scope
- Charles Federson leads product management for **Postgres at Microsoft** and hosts the session. He's joined by three deep database experts who drive the demos: **James** (Cosmos DB), **Bob** (SQL), and **Abe** (Postgres / Horizon DB).
- Four laptops on the podium → this is a **very demo-heavy** session. Plan: **Cosmos DB → Azure SQL → Horizon DB** (the bulk of time on Horizon, the morning's big Postgres announcement).
- The three engines positioned:
  - **Cosmos DB** — Microsoft's **planet-scale NoSQL** platform; powers some of the biggest apps on the planet, **including OpenAI**.
  - **Azure SQL** — long-standing enterprise relational engine, **30+ years** of shipping, extremely performant, and on Azure with **Hyperscale** extremely scalable.
  - **PostgreSQL** — the engine **a lot of AI apps are being built on today**.
- Many announcements were made at Build beyond the keynote. There are dedicated **aka.ms blog links** per database for the full announcement detail, and **all demo code is already in a GitHub repo** (`aka.ms/build26/BRK223`).

### Cosmos DB — Agent Memory Toolkit
- **Why memory matters:** Agents need to remember past events and context to make the best future actions. The **Agent Memory Toolkit** makes this easy to do at scale on Cosmos DB.
- **What it is:** Shipped as a **Python SDK** *and* an **accelerator** for generating, processing, storing, and retrieving agentic memories in Cosmos DB.
- **How it works under the hood:**
  - Uses **Cosmos DB change feed** to automatically process memories.
  - Processing runs in an **Azure Durable Function**.
  - Enrichment/embeddings use models deployed in **Microsoft Foundry** (an LLM + an embedding model).
- **Short-term (local) memory:** While a conversational thread is open, you keep **short-term memories in client memory** for instant, low-latency reads. SDK methods: `add_local` (write) and `get_local` (read) on the memory collection.
- **Persisting to long-term memory:** Use `push_to_cosmos` to commit/persist short-term memories into Cosmos DB. Benefits:
  - **Rehydrate agentic threads** later.
  - Trigger the **change-feed processor** to transform short-term memories into long-term forms: **summarizations** of long-running threads, and **episodic / procedural / fact** memories.
- **Processing modes:** You can orchestrate memory processing **client-side** directly from the SDK (it talks to Cosmos DB to retrieve memories and to Foundry models — LLM + embedding — to process/enrich them) **or offload it to the Azure Durable Function** so it happens automatically with no orchestration after provisioning.
- **Capabilities demonstrated:**
  - Generate a **thread summary** (example: "user asked for a quick account read on Northwind Analytics…").
  - **Memory extraction** — pull out key facts and attributes for the agent to use.
  - Surface **risks + reasoning** behind why those risks matter to the customer.
- **Net:** An SDK for **CRUD + semantic search** over memories; persist short-term in Cosmos DB; auto-process into long-term via Durable Functions + Foundry; then **point reads** plus **semantic and hybrid search** to retrieve the most relevant data.

### Azure SQL — AI apps in the engine, offline-first dev
- **Scenario (Bob's demo):** Build a **live-site support system** entirely with SQL — support transactions, search incidents and **run books** (troubleshooting guides), inspect the live state of the system, and use AI, **all inside the database**. Constraint: build it on a laptop first, then move to Azure unchanged.
- **Architecture (local):**
  - A **Blazor app** (Aspire) running on the laptop.
  - A **Copilot agent** that uses an **MCP endpoint**.
  - **Data API Builder (DAB)** — zero-code exposure of the database as both a **REST endpoint** and an **MCP server**.
  - **Azure SQL container (brand new):** behaves like a SQL Server but "behaves like Azure," running entirely on the laptop. **All AI models live in the container** — **local models for both embedding and inferencing**. The *entire* stack is local.
- **Schema & tooling:** In **VS Code** with the SQL extension you can browse the schema in a **designer**, and there's a new **"chat with your schema"** feature. Tables include incidents, archives, **vector embeddings**, **JSON**, and run books.
- **Ingesting unstructured text → JSON:** Take an engineer's freeform note about a live-site problem and use **regular expressions built into T-SQL** to parse out the error message, build type, wait types, etc., storing the result as **JSON inside the incident** row. The new incident then appears in the Blazor website.
- **Vector hybrid search (T-SQL):** A stored procedure combines:
  - New **`vector search` T-SQL with `TOP ... APPROXIMATE`** over incident history.
  - **`vector_distance`** to search run books, **combined with a JSON index seek**.
  - Result: similar past incidents **plus** matching troubleshooting guides. Execution plan shows a **vector index seek** + a **JSON index seek** combined into the hybrid search.
- **In-DB agent ("mitigate incident 512"):**
  - An **agent markdown file** declares the tools (from **Data API Builder**).
  - A **skill file** defines the *protocol* for using those tools (e.g. don't build indexes when the system is busy).
  - The agent uses DAB tools to inspect the system, find incidents, read run books, and run **diagnostic procedures** (do indexes exist? is the system busy?), then calls a **stored procedure** that invokes **local AI models in the container** to generate a **mitigation plan**.
  - Output: a concrete plan (e.g. **create an index**, **lower transaction scope**) with a **confidence level** and **verification steps** to confirm the fix works — all produced on the laptop.
- **Moving to Azure (the payoff):**
  - Blazor app → **Azure Static Web App**.
  - Copilot agent → unchanged.
  - Data API Builder → runs as a **container in Azure**.
  - Database → **Azure SQL Database** (Hyperscale).
  - AI → **Azure OpenAI** (since all AI access is via **URLs**, embeddings + chat just point at Azure).
  - The **T-SQL is identical**; switching from the Azure SQL container to Azure SQL Database is "really simple."
- **Mental model:** Think of a **versionless SQL Server locally** that **behaves like Azure SQL** but with the full power of SQL Server — build powerful AI apps **offline-first**, then easily move to Azure.

### PostgreSQL at Microsoft — community + managed service
- Microsoft is **deeply invested in Postgres** across Azure *and* the community. Postgres is described as one of the most successful open-source engineering projects Charles has seen.
- **Community footprint:** hosts/runs the **largest virtual Postgres community conference in the world**, runs a **podcast** and a **blog**, and is **one of the most prolific committers** to upstream Postgres.
- **Postgres 19 (ships ~end of September):** Microsoft contributed **~11% of total commits**, **~64,000 lines changed** (~**8% of all changes** in the major version) — non-trivial work directly in the **query engine**, including major **asynchronous I/O** work and a lot of **observability** work.
- **Azure Database for PostgreSQL (Flexible Server):** managed open-source Postgres focused on enterprise requirements — **security, high availability, disaster recovery** — while staying **compatible with upstream** (reflected in the large number of supported **extensions**). Ships **almost every month** (skips one for holidays, banks one for conferences); heavy, continuous investment over 3–4 years.
- **Zero cloud lag:** A few years ago there was a **6+ month wait** to get Postgres 15/16 in the managed service. With **Postgres 18**, Microsoft lit it up in the managed service **on the same day as community GA** — aiming to repeat for the next version.

### Azure Horizon DB — architecture
- **Positioning:** Microsoft's **new Postgres service**, enterprise-ready and engineered for developers, announced in the morning keynote. Takes the managed service "up a level" by **separating compute and storage**.
- **The key architectural line:** Imagine a thick **white dotted line** across the middle of the architecture:
  - **Above the line = compute = true open-source Postgres.** Not an "almost-compatible derivative" — it **is** Postgres. **Apps that run on Postgres today just drop on top of Horizon DB and run.**
  - **Below the line = an entirely new storage engine**, comprised of a new **log server (WAL server in Postgres terms)** and **page servers**, everything **backended by Azure Storage**.
- **What the storage engine provides:**
  - A **shared storage platform striped across availability zones by default**.
  - A **highly optimized log service** that delivers the platform's transactional performance.
  - **Autoscaling storage to 128 TB**, **zone-resilient** with cross-zone failover.
- **Performance proof (live split-screen demo):** Same Postgres version, same region, same hardware, same AZs.
  - **Left:** self-managed Postgres on Azure VMs using **Patroni** (HA across zones) → **~4,000 TPS**.
  - **Right:** **Horizon DB** → **~11,500 TPS** (one row capped out ~**12,000**).
  - Both configured for **HA across zones** as any production workload should be. The gap comes from the **massively optimized storage engine**. Expectation: lift an app from Postgres-on-VMs-across-AZs onto Horizon and see these characteristics.
- **Design tenet:** highly performant for **larger, more demanding apps**, while still allowing **incredibly small form factors**.
- **Form-factor / DX features (from the product video):** powerful **AMD EPYC** processors, **zone-redundant HA**, **Entra ID authentication**, **Private Link** networking, enterprise security by default; provision from the **portal or directly from VS Code**.

### Horizon DB — AI capabilities in the database
- **Why:** Postgres became a preferred engine for new AI apps because when ChatGPT hit and everyone needed embeddings/vectors/similarity search, **`pgvector` was already there**. Microsoft has since learned that **stitching models together is tricky**, and built features to fix that.
- **AI Model Management:**
  - Enable it at **provisioning time**; Horizon **pre-registers a few models** directly out of **Microsoft Foundry**.
  - Invoke them **directly from SQL via AI functions** — e.g. **embedding generation** and **re-ranking** — without separately spinning up Foundry.
  - In Abe's demo the registry exposed **three models**: a **Cohere rerank** model, a **GPT chat** model, and an **embedding** model (`text-embedding-3-small`).
- **AI Pipelines (the feature Charles is "incredibly excited about"):**
  - Built on a **new extension: PG durable** — implements **durable functions natively in Postgres** as an **asynchronous background job** that watches for data changes.
  - **The problem it solves:** Inserting a row should take **milliseconds**. But if that row contains text you want to embed, embedding is slow — you **don't** want embedding in the **commit path** of the write.
  - **The pattern:** Set up a **watcher** on the table. The app writes/modifies rows in **milliseconds**; in an **async background task**, once **change thresholds** are hit, the durable pipeline **invokes the embedding model, chunks the data, creates embeddings, and stores them back**. The app only notices that similarity search has a **slight lag** while embeddings build.
  - **Code shape:** `AI create pipeline` (like an extension call) → handles **chunking**, specifies the **embedding model** and number of **dimensions**, and a **batch size** (e.g. `10`) so the pipeline waits for 10 table changes before invoking the batch — a performance optimization vs invoking on every transaction.
  - **PG durable is fully open source** at `Microsoft/PG durable` — you can build your own durable functions directly in Postgres.

### Horizon DB — tooling (VS Code)
- Goal: bring a **full database management experience into VS Code** for Postgres, where developers already build.
- **Pipeline visualization/debugging:** A visual UX for the AI pipelines — **debug pipelines visually**, watch numbers churn and the pipeline run in real time.
- **Query plans (a favorite):** Entirely **redesigned** query plans (design team involved) with a **tree view** and a **table view**.
  - A **Copilot icon sits next to every operator** and at the **top of the plan**.
  - Clicking an operator **auto-generates a prompt** telling Copilot what to find; it **runs in agent mode**, and you can **choose the model**. A far more efficient way to debug slow queries than hand-rolling diagnostic queries.
- **Live monitoring:** Launch a dashboard, watch **CPU charts** in real time; hit the **Copilot icon** when something goes wrong. Live-monitoring + pipeline visualization are being unified.
- **Portability:** The tooling **works with any Postgres** — local machine or any cloud — not just Horizon DB.

### Horizon DB — end-to-end RAG demo (Abe)
- **Goal:** Build a **"Zava room designer" agent** end-to-end in Postgres: **create an AI pipeline → ingest data → retrieve data → wire into an agent**, all live.
- **Data:** An **e-commerce furniture** dataset; a **product sample table (~60 rows)** for the demo.
- **AI Model Management registry:** three models available in the Horizon DB database — **Cohere rerank**, **GPT chat** (referred to as "GBT 5.4"), and an **embedding** model.
- **Pipeline (≈8 lines of SQL, no external Python orchestrator/service):**
  1. **Name** the pipeline.
  2. Set the **source** (product sample table).
  3. **Chunk** the data (so the right content is found in the right place).
  4. **Embed** the chunks.
  5. The backend **auto-creates an output table** containing chunk text + embeddings (with product IDs).
- **Async behavior highlighted:** When a new row is inserted, it lands in **milliseconds**; the embedding work runs **after the fact** in the background (job seen "kicked off 49 seconds ago"), so **OLTP throughput is sustained** and the model/API latency is hidden — all powered by **PG durable**.
- **Live demo reality:** Ingestion **failed twice** on stage; Abe fell back to a **pre-run backup cluster** that had completed successfully, attributing the failure to a **conflict / wrong DB/table targeting** while running live.
- **Retrieval on the output table:**
  - Create a **full-text search index** (`PG FTS` — Postgres full-text search).
  - Create a **DiskANN index** over the embedding column for faster vector search.
  - Use a new feature, **AI search** (**ships in June**) — here hand-rolled as a custom function — to run a **hybrid search** (vector + full text) over the chunk-text column.
  - Example query: *"I want mid-century furniture for my Brooklyn apartment with dark wood tones"* / *"comfortable chairs"* → returns relevant items (comfortable stylish chair, recliner, massage chair, etc.).
- **Query plan:** Run the AI search and inspect the redesigned **query plan** — see the **full-text search** node and the **sequential scan**, and **debug each node** of the hybrid search.
- **Agent integration (final step):** Ask the agent to **design a room**. The agent talks to **Horizon DB tools** to: run the **hybrid/AI search**, **analyze the room** with the GPT model, **curate picks** via hybrid search, have the model **re-rank** results, and return furniture matching the room's style — which the user can then buy. **Every part of the AI stack runs in Postgres**, with a final **graph to connect everything**, and all models living in **AI Model Management**.

### Wrap-up
- In ~45 minutes the session covered: **Cosmos DB + the agent memory toolkit** (easier to build that class of app), **Azure SQL**'s new **local dev container** (build locally, move to **SQL Hyperscale** in the cloud), and an **end-to-end Horizon DB** flow using AI for both **ingestion and search**.
- All code is in **GitHub** (`aka.ms/build26/BRK223`). There are **additional Build talks on Horizon DB**; it's heading into **public preview**.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Cosmos DB** — Microsoft's planet-scale NoSQL platform; powers huge apps including OpenAI. Focus of the memory demo.
- **Agent Memory Toolkit (Cosmos DB)** — new Python SDK + accelerator to generate/process/store/retrieve agentic short- and long-term memories.
- **Cosmos DB change feed** — triggers automatic processing of short-term memories into long-term memories.
- **Azure Durable Functions** — used by the memory toolkit (and conceptually mirrored by PG durable) to run background memory/pipeline processing.
- **Microsoft Foundry** — hosts the LLM + embedding (and rerank) models invoked for memory enrichment and Horizon DB AI functions.
- **Azure SQL Database / SQL Server** — 30+ yr relational engine; the in-DB AI support-system demo target.
- **Azure SQL Hyperscale** — the scalable Azure SQL tier the local container app moves to.
- **Azure SQL container (private preview)** — versionless SQL Server that runs locally and behaves like Azure SQL, with **local embedding + inference models** in the container.
- **Data API Builder (DAB)** — zero-code exposure of a database as a **REST endpoint** and an **MCP server**; provides agent tools.
- **MCP (Model Context Protocol) endpoint** — how the Copilot agent connects to the database/tools.
- **Blazor + Aspire** — front-end app framework used in the SQL demo (→ Azure Static Web App in the cloud).
- **GitHub Copilot agent / agent mode** — drives incident mitigation in SQL and query-plan debugging in Postgres tooling; authors SQL in VS Code.
- **Agent markdown file + skill file** — declare available tools and the protocol/rules for using them (e.g. don't build indexes when busy).
- **T-SQL vector search** — new `vector search ... TOP ... APPROXIMATE`, `vector_distance`, **vector index seek**, combined with **JSON index seek** for hybrid search.
- **PostgreSQL (open source)** — engine many AI apps build on; Microsoft is a top-tier upstream committer.
- **`pgvector`** — the extension that made Postgres an early home for embeddings/vectors/similarity search.
- **Azure Database for PostgreSQL – Flexible Server** — managed open-source Postgres (security/HA/DR, extension-compatible, monthly releases).
- **Azure Horizon DB** — NEW Postgres service separating compute & storage; true OSS Postgres on a new Azure-Storage-backed engine.
- **Horizon DB storage engine** — new **log/WAL server** + **page servers**, striped across AZs, autoscaling to **128 TB**, zone-resilient.
- **AI Model Management (Horizon DB)** — pre-register Foundry models at provisioning; invoke via SQL AI functions (embedding, rerank).
- **AI Pipelines (Horizon DB)** — declarative RAG (chunk → embed → store) in ~8 lines of SQL, run asynchronously.
- **PG durable** — NEW **open-source** extension (`Microsoft/PG durable`) implementing **durable functions natively in Postgres**; powers AI pipelines.
- **DiskANN vector indexing** — Microsoft's high-performance approximate vector index used for semantic search in Horizon DB (and SQL).
- **Postgres full-text search (`PG FTS`)** — full-text index used alongside vectors for hybrid search.
- **AI search (Horizon DB)** — new hybrid (vector + full-text) search capability, **ships in June**.
- **Cohere rerank model** — reranks hybrid-search results to match style/intent.
- **`text-embedding-3-small`** — embedding model surfaced via AI Model Management.
- **VS Code extension for Postgres/Horizon** — object explorer, schema chat, **redesigned visual query plans** (tree + table) with per-operator Copilot, live CPU monitoring, pipeline debugging; works with **any Postgres**.
- **Patroni** — used for the self-managed Postgres HA baseline in the benchmark comparison.
- **Entra ID auth + Private Link** — Horizon DB enterprise security defaults.
- **AMD EPYC processors** — compute powering Horizon DB.
- **Zava** — sample/fictional company/app used across the SQL and Postgres demos.

## 🚀 Announcements / What's New
- **Azure Horizon DB** — NEW Postgres service (announced in the morning keynote); separates compute/storage, ~3× transactional + vector performance, 128 TB autoscaling storage, AI built in. **Heading into public preview.**
- **Cosmos DB Agent Memory Toolkit** — NEW Python SDK + accelerator for agentic memory on Cosmos DB.
- **Azure SQL container** — NEW, in **private preview** (sign-up page shown in session); versionless local SQL Server that behaves like Azure SQL with local AI models.
- **PG durable** — NEW open-source Postgres extension for durable functions / AI pipelines (`Microsoft/PG durable`).
- **AI Model Management, AI Pipelines, and AI functions in Horizon DB** — invoke Foundry models (embedding/rerank) directly from SQL; declarative RAG pipelines.
- **AI search (Horizon DB)** — hybrid vector + full-text search, **GA/ships in June**.
- **T-SQL vector search enhancements** — `vector search ... TOP ... APPROXIMATE` + `vector_distance` enabling vector + JSON hybrid search in Azure SQL.
- **Postgres 18 same-day support** (recap) and **Postgres 19** (~end of September) with ~11% of commits from Microsoft.
- **Status note:** Horizon DB = public preview; Azure SQL container = private preview; Horizon AI search = June. Detailed per-database announcements live at the `aka.ms` blogs referenced in the deck.

## 💡 Demos
- **Cosmos DB — Agent memory (James):** Jupyter notebook. Set up async Cosmos memory client; add/get **short-term local** memories; **push to Cosmos** for long-term; **change-feed + Durable Function** processing into summaries/episodic/procedural/fact memories; **memory extraction** of facts/attributes; surfaced **risks + reasoning**; **semantic/hybrid** retrieval. *Point proven:* full memory lifecycle (CRUD + semantic search) with automatic background enrichment, minimal orchestration.
- **Azure SQL — Live-site support system (Bob), fully on a laptop:** Blazor/Aspire app + Copilot agent + Data API Builder (REST + MCP) + **Azure SQL container with local embedding/inference models**. Showed **"chat with your schema\,"** **regex-in-T-SQL** parsing unstructured notes into **JSON** incidents, **vector hybrid search** (vector index seek + JSON index seek), and an **in-DB agent** ("mitigate incident 512") that produced a mitigation plan with **confidence level + verification steps**. Then showed the **identical T-SQL** moving to Azure (Static Web App + DAB container + Azure SQL + Azure OpenAI). *Point proven:* build AI apps offline-first and move to Azure unchanged.
- **Horizon DB — Benchmark (Charles):** Split-screen live **TPC** run, same region/hardware/AZs, both HA across zones: self-managed Postgres (Patroni) **~4,000 TPS** vs Horizon DB **~11.5–12K TPS**. *Point proven:* the optimized storage engine delivers ~3× throughput for lift-and-shift Postgres apps.
- **Horizon DB — End-to-end RAG "Zava room designer" (Abe):** Create an **AI pipeline** (~8 lines SQL) to chunk + embed furniture data into an auto-created output table; **async** ingestion (insert in ms, embeddings after the fact via PG durable). **Live ingestion failed twice** → fell back to a **pre-run backup cluster**. Then **DiskANN + PG FTS** indexes, **AI search / hybrid** retrieval ("mid-century furniture… dark wood tones"), **redesigned query plans**, and an **agent** that searches, analyzes the room, reranks (Cohere), and curates furniture. *Point proven:* an entire AI-native app — ingestion, retrieval, rerank, orchestration — runs **inside Postgres**.

## 📊 Notable Stats / Quotes
- **~4,000 TPS** (self-managed Postgres on VMs, Patroni, HA across zones) vs **~11,500–12,000 TPS** (Horizon DB) — same region/hardware/AZs → **~3× transactional throughput**.
- **Up to 3×** faster transactional processing and vector search in Horizon DB (uses Microsoft's **DiskANN** vector tech).
- **128 TB** — Horizon DB autoscaling, zone-resilient storage ceiling.
- **~11%** of total commits to **Postgres 19** from Microsoft; **~64,000 lines** changed (~**8%** of all changes in the major version).
- **Postgres 18** lit up in the managed service on the **same day** as community GA (vs **6+ months** lag for PG 15/16 previously).
- **~8 lines of SQL** to build a RAG pipeline in Horizon DB (vs an external Python orchestrator/service).
- **Batch size 10** — pipeline waits for 10 table changes before invoking an embedding batch (perf optimization).
- **~60 rows** product sample table; embedding job seen **"49 seconds ago"** running async after a millisecond insert.
- Postgres 19 expected **~end of September**; Horizon **AI search ships in June**.
- *"Everything above the white dotted line is compute. It is true Postgres… not an almost-compatible derivative — it is Postgres."*
- *"I like it in the database… the point is you've got choice on how you build these applications."* — Charles, on putting AI logic in the DB.
- *"If anything goes wrong, we're praying to the demo gods here."* — Abe, before the live RAG demo (which then failed twice).

## 🧠 My Notes / Follow-ups
- [ ] Things to try: spin up **Horizon DB** (public preview) in `australiaeast` and benchmark vs Flexible Server; clone the `aka.ms/build26/BRK223` repo and run the **AI pipelines** sample.
- [ ] Questions: How does **PG durable** behave under failure/retry, and what are the cost implications of background embedding at scale? When is **Horizon DB GA** and how is it priced vs Flexible Server?
- [ ] Relevant to: customer AI-app modernization conversations (RAG-in-DB vs external orchestrators), Postgres migration pitches, and the "AI logic in vs out of the database" architecture debate.

## 🔗 Related
- [[32.02 Content]]
- 
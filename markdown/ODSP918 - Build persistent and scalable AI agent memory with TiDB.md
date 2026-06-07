---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/tidb
  - topic/agent-memory
  - topic/vector-search
  - topic/agents
  - topic/ai
  - topic/databases
source: https://www.youtube.com/watch?v=J0o-Dkt5tnI
session_code: ODSP918
event: Microsoft Build 2026
speakers: Ravish (Solutions Engineer, PingCAP / TiDB)
duration_min: 17
aliases:
  - Build persistent and scalable AI agent memory with TiDB
---

# ODSP918 — Build persistent and scalable AI agent memory with TiDB

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Ravish — Solutions Engineer at PingCAP, working on TiDB  
> **Duration:** ~17 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=J0o-Dkt5tnI)

## 🎯 TL;DR
This is a PingCAP partner session showing how to build **persistent, scalable memory for AI agents using just SQL** on **TiDB** — a distributed, MySQL-compatible SQL database with built-in vector search, full-text search, and an HTAP/AI engine. The core argument: agents stress databases differently from normal apps (bursty workloads, massive concurrency, constant context recall), and the common "memory stack" of three separate databases (relational + vector + search) glued together with ETL pipelines breaks at scale in four specific ways (stale data, read-after-write, partial writes, connection fan-out). TiDB collapses all of that into **one table in one database** — auto-generating embeddings on insert, doing vector + keyword + hybrid search in single SQL queries, and providing ACID transactions across tables. A six-step live demo walks through creating a memory table, inserting plain-English memories, and running semantic, keyword, hybrid (RRF), and multi-table ACID queries. Real production proof points (Manus, Dify, Pinterest) and a "free cluster in 30 seconds, scale to zero" pitch close it out.

## 🔑 Key Takeaways
- **Agents hit databases in three fundamentally different ways:** workloads are *bursty* (one agent flat-out for 10s, another idle for 2h), concurrency is *massive* (millions of agents, each with its own state — not thousands of users), and they need *constant context recall* (every step must remember what just happened or the agent falls apart).
- **The typical agent "memory layer" is three databases + glue:** a relational DB (source of truth for chat history/accounts), a vector DB (semantic search over embeddings), a search engine (keyword/exact matches, since vectors are bad at exact terms), and a fourth invisible piece — the **ETL/glue layer** (jobs, message buses, cron) that keeps the three in sync and that your team must build and maintain.
- **That stack is tolerable for regular apps but breaks for agents in four ways:** (1) **stale data** — the vector index lags the main DB by seconds, so the agent reads old facts; (2) **read-after-write** — an agent places an order, the user asks status 2s later, the replica hasn't caught up, agent says "no orders"; (3) **partial writes** — a multi-step refund deducts balance + logs event + triggers email, the email service dies midway, leaving a "ghost refund"; (4) **connection fan-out** — 10,000 agents × 3 systems = 30,000 connections to manage, blowing up latency on spikes.
- **These failures only surface at scale — the worst possible time** — and are real production problems, not hypotheticals.
- **TiDB is a distributed SQL database** that scales horizontally by adding nodes — **no sharding, no rewrites**, just add nodes for capacity on demand.
- **TiDB is MySQL-compatible** — existing MySQL drivers, ORMs, and tooling work unchanged.
- **TiDB has an HTAP + AI engine:** transactions, analytics, vector search, and full-text search all live in **the same database** (HTAP = Hybrid Transactional/Analytical Processing).
- **Auto-embeddings on insert via a SQL function** (`EMBED_TEXT` / "embedders text"): define the embedding as a **generated vector column**, and every insert calls the configured embedding model (e.g. Azure OpenAI) and stores the vector — **no Python, no pipeline**.
- **One table does it all:** normal SQL columns for agent state/chat history, a **vector column with an HNSW index** for semantic recall, and a **full-text index with a multilingual parser** (English, Spanish, Japanese, etc.) for keyword search.
- **Hybrid retrieval done "the right way"** = two searches (vector top-N + keyword top-N) combined with **Reciprocal Rank Fusion (RRF)** so rows ranking high in *both* lists win — all in one query, one database.
- **ACID transactions span multiple tables** — multi-step agent writes (e.g. insert memory + update per-user stats) land together or roll back together; no partial-write ghost states.
- **Agent-shaped operational features:** **scale to zero** (idle agents cost nothing; bursty traffic → bursty bill), **database branching** (isolated DB per agent spun up in milliseconds), **resource control** (cap per-workload usage so one runaway agent can't take everything down), and **fast scale-out** (compute and storage are separated, so capacity is added in seconds, not minutes).
- **Production proof, real numbers not benchmarks:** **Manus** — ~1.5M agents, a DB per agent in ms, to production in 2 weeks; **Dify** — moved ~500,000 containers onto TiDB, now one engine; **Pinterest** — replaced six database systems with one, ~**1.3M queries/sec** on TiDB.
- **Getting started:** spin up a **free TiDB Cloud "starter" cluster in 30 seconds, no credit card**; native **Azure OpenAI integration**; **Python SDK** (`pip install pytidb`) gives hybrid search + RRF in three lines; **MCP server + agent rules** for Cursor/Claude users to drop TiDB into an AI coding workflow.
- **Closing thesis:** "Stop running three databases when you only need one" — less infrastructure, more speed, engineers building product instead of patching pipelines.

## 📚 Detailed Notes

### Framing: why agents are different from the apps you've built before
Ravish opens by arguing that AI agents stress a database in ways traditional applications never did, and there are three non-negotiable characteristics:

1. **Bursty workloads.** One agent might run flat-out for 10 seconds, while another sits idle for two hours. The database must handle both extremes **without costing a lot of money** — i.e. you can't keep paying for peak capacity during long idle stretches.
2. **Massive concurrency.** This isn't an app serving a thousand users; it's **millions of agents running simultaneously, each carrying its own state.** The concurrency model is qualitatively different.
3. **Constant context recall.** Every single step an agent takes depends on remembering what just happened. Lose that recall and "the whole thing falls apart." Memory is not a nice-to-have; it's load-bearing.

These three are presented as things "you can't really skip" when designing agent infrastructure.

### The problem in concrete terms: the amnesiac agent
The motivating scenario: an agent finishes a chat with a user today. The user returns tomorrow and the agent **has no clue who they are** — it's as if the conversation never happened. Solving this persistence problem is what "agent memory" means.

### What most teams build today: three databases + a glue layer
To give the agent memory, the common pattern stitches together **three databases plus ETL pipelines**:

- **Relational database** — the **source of truth**. Stores chat history, user accounts, and similar structured data.
- **Vector database** — for **semantic search**. Stores embeddings of what the user said so the agent can retrieve by meaning.
- **Search engine** — for **keyword / exact matching**, because **vectors are bad at exact matches**. If the user literally said "Tokyo," you want a keyword index to find that exact token.
- **The glue layer (the fourth, under-discussed piece)** — the **ETL jobs, message buses, and cron jobs** that keep all three stores in sync. *Your team writes and maintains this code.*

The cost of this architecture: **three databases to run, three separate bills, three things that can break**, and **data that is never truly in sync.** Ravish concedes that for a *regular application* you can "sort of live with this" — it's annoying but survivable. For *agents*, it breaks.

### How the three-database stack breaks for agents (the four failure modes)
This is the heart of the "why TiDB" argument. Four specific, production-real failures:

1. **Stale data.** The vector index is always a few seconds behind the main database, so the agent reads **old data / old facts**. Example: the user updated their address an hour ago, but the agent still uses the old one because the embedding/index hasn't caught up.
2. **Read-after-write.** The agent just placed an order; two seconds later the user asks "what's the status of my order?" The write happened, but the **read replica hasn't caught up**, so the agent answers "I don't see any orders." The system contradicts an action it just took.
3. **Partial writes.** A multi-step operation — e.g. processing a refund — must (a) deduct the balance, (b) log the refund event, (c) trigger an email. If the **email service dies midway**, the balance shows the refund applied and the log says it happened, **but the user never got the email.** Support later looks at the logs, sees everything "looks fine," and you're left **explaining a ghost refund.** This is a transactional-integrity failure across systems.
4. **Connection fan-out.** With, say, **10,000 agents × 3 systems = 30,000 connections** to maintain and manage. Connection pools struggle to keep up; **latency rises when traffic spikes**, and you spend half your time managing connections instead of building features.

Key point hammered home: **this is not theory.** It happens in production and **you only hit it at scale — the worst possible time** to discover it.

### What TiDB is (the one-database alternative)
A quick primer on TiDB for those unfamiliar:

- **Distributed SQL database** — scales **horizontally across nodes**. **No sharding, no rewrites**; you just add nodes (and thus capacity) whenever you need it.
- **MySQL-compatible** — any MySQL drivers, ORMs, and tools work with TiDB as-is.
- **HTAP + AI engine** — **transactions, analytics, vector search, and full-text search all live in the same database.** (HTAP = Hybrid Transactional/Analytical Processing.)
- **Battle-tested in production** — used by customers including **Manus, Pinterest, Dify**, and others.

### TiDB capabilities mapped to agent needs
Ravish presents a capability table where the **first three rows fix the three data problems** above, and the **last two are quality-of-life extras** for building agents:

- **Agent state & chat history** → just **normal SQL** (the relational source-of-truth role).
- **Semantic recall** → a **vector column with an HNSW index** (replaces the standalone vector DB).
- **Keyword search** → a **full-text index with a multilingual parser** handling English, Spanish, Japanese, "whatever you throw at it" (replaces the standalone search engine).
- **Embeddings on insert** → a SQL function (`EMBED_TEXT`, spoken as "embedders text"): give it text and it **calls the embedding model and stores the vector for you** in the table — no separate embedding pipeline.
- **Hybrid retrieval** → run a **vector search and a keyword search and combine them with a ranking algorithm**, all inside the database.

Because all five capabilities live on one table in one engine, **there is nothing to keep in sync** — the stale-data, read-after-write, and partial-write problems largely dissolve because reads and writes hit a single consistent transactional store.

### TiDB's agent-shaped operational model (mapping back to "agents are different")
This slide directly answers the three opening characteristics (bursty, concurrent, recall-heavy) with operational features:

- **Scale to zero.** Idle agents **literally cost nothing** — you pay only for the requests you actually run. "When your traffic is bursty, your bill is bursty too." (Answers the bursty-workload problem.)
- **Database branching.** Spin up an **isolated database per agent in a few milliseconds**, so each agent gets its own fully-separated workspace. (Answers massive concurrency + isolation.)
- **Resource control.** **Cap how much each workload uses**, so a single runaway ("off the rails") agent can't take down everything else.
- **Fast scale-out.** **Compute and storage are separated**, so on a traffic spike the database can **add capacity in seconds instead of minutes.**

### The live demo — one free cluster, one table, six steps
Ravish runs the entire demo in the **TiDB Cloud SQL editor on a free cluster, using a single table**. (Details captured in the Demos section below.) The recurring refrain throughout each step: *"the same table, no separate engine to keep in sync."* The progression: create table → insert memories → semantic search → keyword search → hybrid search (RRF) → ACID transaction across two tables.

### Why hybrid search "the right way" matters
Ravish stresses that **real hybrid search is not a single query** — it's **two searches plus a ranking step**:
- CTE #1 runs a **vector search** for the top-10 rows **by meaning**.
- CTE #2 runs a **keyword search** for the top-10 rows **by exact word match**.
- The two result sets are fused with **Reciprocal Rank Fusion (RRF)**: the idea is simple — **rows that rank highly in *both* lists win.**

This combines semantic understanding (intent/meaning) with lexical precision (exact terms like "allergy," "peanut"), which neither approach alone handles well.

### ACID across tables — why agents need real distributed transactions
"Real agents do multi-step writes that have to land together." The demo uses two tables — the `memories` table plus a separate `user_facts` table tracking aggregate per-user stats (trips, memory count). Wrapping an `INSERT INTO memories` + `UPDATE user_facts` in a single transaction and committing means **both writes land or neither does.** This is **real distributed ACID across multiple tables** — the structural fix for the "partial write / ghost refund" failure mode.

### Production proof points
Ravish closes the technical content with three customers running TiDB in production (emphasizing these are **real numbers, not benchmarks**):

- **Manus** — an AI startup; **every agent gets its own database spun up in milliseconds**; **over ~1.5 million** such agents currently; migrated to TiDB and **reached production in two weeks.**
- **Dify** — an AI dev-platform company; backend previously ran on **~500,000 containers**, all moved onto TiDB; now **one engine does everything.**
- **Pinterest** — not an AI company, but had the same shape of problem: **six different database systems** doing different jobs, now consolidated to **one (TiDB)**, serving **~1.3 million queries per second.**

The common storyline across all three: **less stuff, more speed, engineers building product instead of patching pipelines.**

### Recap & the value proposition
With TiDB you get: **auto-embeddings on insert** (no Python pipelines), **vector + full-text search + SQL on the same table** (one source of truth), **hybrid search done right** (two searches + RRF), and an engine **built for how agents actually run** (branching, scale-to-zero, resource control). The kicker: **spin up a free cluster in 30 seconds** and it **scales to millions of agents.**

### Getting started — where to go
- **tidbcloud.com** — spin up a **free TiDB "starter" cluster, no credit card, ready in ~30 seconds.**
- **Native Azure OpenAI integration** — easily wire your Azure deployment in for the agent patterns shown.
- **Customer stories** — referenced at a PingCAP AI/agents landing page ("pingcap.com/ai...", URL caption-garbled).
- **Python SDK** — `pip install pytidb` → hybrid search + RRF in **three lines** of code.
- **MCP server + agent rules** for **Cursor and Claude** users — published on GitHub (PingCAP "agent rules" repo) — to drop TiDB directly into an AI coding workflow.

Closing line: *"Go build something cool with TiDB, and stop running three databases when you only need one."*

## 🛠️ Products / Features / Technologies Mentioned
- **TiDB** — distributed, MySQL-compatible SQL database with an HTAP + AI engine; the central product of the talk; positioned as a single store for agent memory.
- **TiDB Cloud** (`tidbcloud.com`) — managed TiDB service; offers a free "starter" cluster provisioned in ~30 seconds with no credit card.
- **PingCAP** — the company behind TiDB (the presenter's employer; caption-garbled as "Pinkap/pinkcat/pinkapp").
- **`EMBED_TEXT` SQL function** ("embedders text") — built-in function that calls the configured embedding model and stores the resulting vector; used to define a **generated vector column** so embeddings are created automatically on insert.
- **Vector column + HNSW index** — TiDB's native vector type (1536 dimensions in the demo) with an HNSW (Hierarchical Navigable Small World) approximate-nearest-neighbour index for semantic search.
- **Full-text index with multilingual parser** — TiDB's keyword/exact-match search supporting multiple languages (English, Spanish, Japanese, etc.).
- **Hybrid search + Reciprocal Rank Fusion (RRF)** — combines vector and keyword result sets via RRF ranking, all in one SQL query.
- **Distributed ACID transactions** — multi-statement transactions spanning multiple tables (commit/rollback together).
- **Scale to zero / database branching / resource control / separated compute & storage** — TiDB's agent-oriented operational features.
- **Azure OpenAI** — used as the embedding-model backend in the demo; TiDB has a native integration for it.
- **PyTiDB (Python SDK)** — `pip install pytidb`; gives hybrid search + RRF in ~3 lines.
- **TiDB MCP server + agent rules** — Model Context Protocol server and rule files (PingCAP GitHub repo) for using TiDB inside Cursor / Claude AI coding workflows.
- **MySQL** — compatibility baseline (drivers, ORMs, tooling carry over).

## 🚀 Announcements / What's New
None explicitly announced as new at Build 2026. The session is a capability/how-to walkthrough of existing TiDB features (auto-embeddings, vector + full-text + hybrid search, ACID, scale-to-zero, database branching, Azure OpenAI integration, PyTiDB SDK, MCP server). No GA/preview status changes or new releases were called out.

## 💡 Demos
A single end-to-end demo run in the **TiDB Cloud SQL editor on a free cluster**, all on **one table**, in six steps:

1. **Create the memory table.** Normal columns (`user_id`, an `id`, `content`, a `timestamp`) plus the key column: an **`embedding` vector with 1536 dimensions defined as a generated column.** On every insert, TiDB calls `EMBED_TEXT` (pointed at an **Azure OpenAI** deployment) to generate and store the embedding — **no Python, no pipeline.** The table also defines a **vector index** (semantic search) and a **full-text index** (keyword search) **on the same table.** *Proves:* one table can carry relational data, vectors, and full-text indexes with embeddings auto-generated.
2. **Insert memories & view data.** Inserts **five plain-English memory strings for `user_id` 42** (jazz/vinyl, peanut allergy, Tokyo flight, email preference, etc.). **No embedding code anywhere in the script** — TiDB calls Azure OpenAI in the background to embed each row. *Proves:* embeddings happen transparently on insert.
3. **Semantic search.** Agent asks *"what does the user like to listen to?"* — a question sharing **zero keywords** with the data (no "listen," no "like to"; the row just says jazz/Miles Davis). The **jazz row returns first** with a **distance of 0.49** (closest match by meaning). TiDB embedded the question and ranked rows by similarity **in one SQL call.** *Proves:* meaning-based retrieval works without keyword overlap.
4. **Keyword search.** Sometimes you need **exact word matching** (vectors are bad at this). A **full-text search** checks whether the user mentioned a city; the **Tokyo row** returns as the exact match with a **score of 1.34.** Crucially, this is **the same table** the vector search ran on — **no separate engine to sync.** *Proves:* exact-match search co-exists on the same table.
5. **Hybrid search (the one that "really matters").** Two CTEs — one **vector search (top 10 by meaning)**, one **keyword search (top 10 by exact word)** — combined with **Reciprocal Rank Fusion (RRF)**. Asking *"what dietary restrictions does the user have?"*: vector looks for meaning, keyword looks for words like "allergy"/"peanut," and the **peanut-allergy row comes first** because it scores well in **both**. *Proves:* one query, one database delivers proper hybrid retrieval.
6. **ACID transactions across tables.** Two tables — `memories` and a separate `user_facts` (aggregate per-user stats: trips, memory count). A transaction wraps **`INSERT INTO memories` + `UPDATE user_facts` + `COMMIT`.** Result: the new memory lands, the **trip counter goes 0 → 1**, and the **memory counter goes 0 → 1** — **both writes land together**, and if either had failed, **neither would have stuck.** *Proves:* real distributed ACID across multiple tables (fixes the partial-write problem).

## 📊 Notable Stats / Quotes
- **Embedding dimensions:** vector column = **1536 dimensions** (demo).
- **Semantic search result:** jazz row distance = **0.49** (closest by meaning).
- **Keyword search result:** Tokyo row full-text score = **1.34**.
- **Connection fan-out math:** **10,000 agents × 3 systems = 30,000 connections** to manage.
- **Manus:** **~1.5 million** agents, a database per agent in **milliseconds**, to production in **two weeks**.
- **Dify:** migrated **~500,000 containers** onto TiDB → **one engine**.
- **Pinterest:** consolidated **6 database systems → 1**, running **~1.3 million queries per second**.
- **Free cluster:** provisioned in **~30 seconds**, no credit card; **scales to millions of agents**.
- **PyTiDB:** hybrid search + RRF **in 3 lines** of code.
- **Time budget:** presenter framed the talk as "~20 minutes" with a demo halfway through (actual runtime ~17 min).
- **Tagline:** *"Stop running three databases when you only need one."*
- **On bursty billing:** *"When your traffic is bursty, your bill is bursty too."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
	- Spin up a free TiDB Cloud starter cluster (tidbcloud.com, ~30s, no credit card) and recreate the demo's single memory table.
	- Wire up the **native Azure OpenAI integration** + a **generated vector column** with `EMBED_TEXT` and confirm embeddings populate automatically on insert (no Python pipeline).
	- Build a hybrid-search query: two CTEs (vector top-10 + full-text top-10) fused with **RRF**; compare results vs vector-only and keyword-only.
	- Try `pip install pytidb` and see if hybrid search + RRF really is ~3 lines.
	- Install the **TiDB MCP server + agent rules** (PingCAP GitHub) into Cursor/Claude and test dropping TiDB into an AI coding workflow.
	- Validate the **ACID-across-tables** pattern (memories + user_facts in one transaction) for our own multi-step agent writes.
- [ ] Questions:
	- How does TiDB's **scale-to-zero** cold-start latency compare to keeping a small warm pool? What's the wake-up time on the first request after idle?
	- **Database branching per agent in milliseconds** — what are the real limits (max concurrent branches, cost model, cleanup) at the ~1.5M-agent scale Manus runs?
	- HNSW recall/latency tradeoffs at high dimensionality (1536) and large row counts — how does it compare to a dedicated vector DB (e.g. on accuracy/QPS)?
	- How fresh is vector search relative to writes inside TiDB itself — does the single-engine design fully eliminate the stale-index lag, or is the vector index still async?
	- What's the embedding cost/latency exposure when `EMBED_TEXT` calls Azure OpenAI synchronously on every insert at high write volume? Batching support?
	- How does TiDB's offering compare to Azure Cosmos DB / Azure Database for PostgreSQL (pgvector) + DiskANN for the same agent-memory use case?
- [ ] Relevant to:
	- Designing the **memory/persistence layer** for any multi-agent system — strong "one store instead of three" argument to evaluate against our current stack.
	- Anyone currently gluing relational + vector + search DBs with ETL who's hitting stale-data / read-after-write / partial-write / connection-fan-out pain.
	- AI agent platform / RAG architecture decisions where hybrid retrieval (semantic + exact) and transactional integrity both matter.

## 🔗 Related
- [[OD820 - Designing Reliable Multi-Agent Apps with Azure Cosmos DB]] — same problem space (data/memory layer for multi-agent apps) on the Azure-native side; good comparison to TiDB's single-store pitch.
- [[ODSP900 - Performance tuning on Cobalt with Arm Performix]] — sibling ODSP partner session at Build 2026; infrastructure/performance angle.
- [[BRK223 - From rows to reasoning]] — "designing databases for AI apps and agents" theme; directly complements vector + hybrid search for agents.
- Source list: [[2026 Build Session List]]
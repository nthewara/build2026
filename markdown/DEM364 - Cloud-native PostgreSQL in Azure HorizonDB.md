---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/azure
  - topic/postgresql
  - topic/database
  - topic/ai
source: https://www.youtube.com/watch?v=_9JC2s7G3l8
session_code: DEM364
event: Microsoft Build 2026
speakers: Maxim (Group Product Manager, Microsoft Postgres team)
duration_min: 26
aliases:
  - Cloud-native PostgreSQL in Azure HorizonDB
---

# DEM364 — Simplify app dev with cloud-native PostgreSQL in Azure HorizonDB

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speaker:** Maxim — Group Product Manager, Microsoft Postgres team (focused on generative-AI developer experiences)  
> **Duration:** ~26 min  
> **Format:** Recorded screen-capture demo (audio only over the screen recording)  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=_9JC2s7G3l8)

## 🎯 TL;DR
Azure HorizonDB is Microsoft's new cloud-native PostgreSQL database (public preview announced by Satya Nadella the day before this session), built by taking the open-source Postgres engine and connecting it to a cloud-optimized, scalable storage backend for higher resiliency, larger scale, and better performance. On top of that engine, Microsoft layered AI features — built-in managed models, in-database AI pipelines, and AI functions — designed for the era of AI agents. The session is a live demo that builds the AI components of a "Zava room designer" app, showing how HorizonDB collapses the normal AI-agent plumbing (model provisioning, embedding generation, vector + full-text + hybrid search, semantic re-ranking, and knowledge graphs) into a handful of SQL statements with no external services. The core thesis: HorizonDB lets you build a sophisticated retrieval/agent stack entirely inside Postgres, with very few lines of SQL.

## 🔑 Key Takeaways
- **Azure HorizonDB** = open-source PostgreSQL engine + cloud-optimized scalable storage backend → higher resiliency, larger scale, better performance.
- Claimed performance: **3× higher transactional throughput** and **3× faster vector search** vs. baseline Postgres.
- Scales to **very large databases** with **up to 15 read-only replicas**.
- Public preview was **announced by Satya Nadella the day before** (i.e., at Build 2026).
- HorizonDB ships with **built-in AI models, AI pipelines, and AI functions** — positioned for AI agents.
- **Model provisioning is bundled into database creation**: a single checkbox at provisioning time activates model management plus PG Vector and DiskANN vector-search extensions — you skip the usual model-infrastructure setup step entirely.
- **Three managed models** are auto-provisioned: a chat-completion model, a text-embedding model, and a semantic-ranker (reranker) model. **Bring-your-own-model (BYO)** is also supported for existing enterprise models.
- **AI pipelines** run inside the database: a SQL-defined source → chunk → embed → sync flow that vectorizes a product catalog and, via an attached **trigger**, incrementally keeps embeddings up to date as data changes — asynchronously, without blocking inserts.
- HorizonDB supports **vector search, full-text search, and hybrid search**; a new **`pgfts`** extension brings Lucene-style full-text search to Postgres, and **DiskANN** provides faster vector indexing than pgvector.
- **Hybrid search** combines full-text + vector results using **Reciprocal Rank Fusion (RRF)**; adding **`rerank => true`** triggers a Cohere semantic reranker to reorder candidates by semantic relevance.
- The **Postgres extension for VS Code** provides the whole experience: provisioning, model registry inspection, pipeline status UI, hybrid-search functions, **query-plan visualization**, and **graph visualization**.
- **Knowledge graphs** are stored natively in Postgres via the **Apache AGE** extension, queried with **Cypher**, to encode style relationships (e.g., "mid-century modern" connects coffee tables, chairs, bookcases) and **"similar-to" relationships between styles** (mid-century modern ↔ bohemian) to broaden furniture matches.
- End result: a sophisticated AI room-design agent built with **no external services** and **very few lines of SQL**, all inside HorizonDB.

## 📚 Detailed Notes

### What HorizonDB Is (Refresher)
HorizonDB is Microsoft's new PostgreSQL database. The construction approach: take the **open-source PostgreSQL engine** and connect it to a **cloud-optimized, scalable storage backend**. Decoupling compute from this storage layer is what delivers:
- **Higher resiliency**
- **Larger scale**
- **Better performance** for Postgres workloads

Quantified claims for HorizonDB vs. baseline:
- **3× higher throughput** on transactions
- **3× faster vector search**
- Scales to **very large databases**
- Supports **up to 15 read-only replicas**

On top of this engine, Microsoft built AI features so HorizonDB is "designed for this new era of AI agents":
- **Built-in AI models**
- **AI pipelines**
- **AI functions**

The session's goal is to test the claim that these AI functions simplify app development — by building an agent live on stage using only HorizonDB features.

### The Demo App — Zava Room Designer
The end-state app being (partially) rebuilt is a **Zava room designer**. Scenario:
- A photo of the presenter's **Brooklyn loft** already containing one piece of furniture (a couch).
- User clicks **"Design my room."**
- The app **analyzes the photo**, determines the room's **style and color palette**, **scans the product catalog**, and **picks furniture that fits** the style/palette — within a small budget.
- Result: the room is auto-furnished with coordinated pieces, removing the difficulty of manually choosing matching furniture.

The point: the app *looks* complex/sophisticated, but it is intentionally simple. The demo rebuilds its key components one by one to show how HorizonDB simplifies the development process.

### Step 1 — Connecting Models (the step you get to skip)
Normally, enabling an agent to reason requires **provisioning models, connecting them, and setting up all that infrastructure first**. With HorizonDB, this step is skipped because models are bundled into the database.

Provisioning flow (shown via the **Postgres extension for VS Code** — the product the whole demo is built on, and which Maxim recommends for all Postgres work):
1. In the "new server" screen there's a new entry: **Provision HorizonDB**.
2. Log in to the Azure portal with credentials.
3. Specify cluster details — named "my HorizonDB 2", a bit more compute cores, select user.
4. A **single checkbox activates model management** plus **PG Vector** and **DiskANN** vector-search extensions for Postgres.
5. Click provision — the database comes up with **all model connections already provisioned**.

(Live-demo aside: the provisioning click hit a hiccup, so Maxim switched to a **pre-provisioned HorizonDB** prepared for the demo.) Provisioning runs in the background; you don't wait for it.

### Step 2 — Prepare Data for AI Consumption (Embeddings via AI Pipeline)
Goal: make the product catalog usable by the model — which requires **embeddings** so the app can reason about which furniture *semantically* fits the room's style.

**Inspecting the model registry (in SQL):** Because models were pre-provisioned, you can query the model registry directly in SQL and see **three managed models** auto-provisioned with the database:
1. A **generic chat-completion model**
2. A **text-embedding model**
3. A powerful **semantic ranker (reranker) model** (used later to improve search quality)

**Bring-your-own-model** is also supported — connect existing enterprise models to the database.

**Building the AI pipeline:** A full pipeline is defined in SQL. Conceptually: "From the `product_sample` table as a source, perform these steps":
1. **Chunk** the data — split each row into smaller pieces (important for vector-search accuracy later) via a `chunk` function.
2. **Embed** — for each chunk, generate an embedding using the pre-provisioned **Microsoft Foundry** embedding model.
3. **Sync** — write results into an output table.

**Critical feature — the trigger:** The pipeline definition attaches a **trigger**, so the pipeline doesn't just process existing data — **any future changes to the product catalog automatically flow through the pipeline**, incrementally generating new embeddings. This handles incremental updates with no extra work.

**Running & monitoring:**
- Pipeline created successfully; status is queryable in SQL (`total processed items` increases over time).
- The VS Code extension also provides a **pipeline UI / visual diagram** showing the flow.
- Numbers from the diagram: source table has **60 rows** → chunking produces **116 chunks** → embedding step calls the Foundry embedding model → **116 vectors** generated.
- The output table is `embedding_pipeline_output`, containing the chunks and their embeddings. Final status: **116 rows processed** (after a brief demo delay).

Result: the product catalog is now **fully vectorized** and ready for vector search.

### Vector Search + Incremental Update Proof
- A simple **vector search** query is run against the output table to find "best chairs that is comfortable" (Postgres vector-search operator). Chairs are returned.
- **Incremental-update demo:** Insert a new row into `product_sample`. The embedding-pipeline output count goes from **116 → 117** quickly. The pipeline watched in the background and processed the new row **asynchronously without blocking the insert** (keeping the DB responsive).
- Re-running the same vector search shows the **newly added item already appears** in results — proving the trigger-driven incremental pipeline works end to end, with all the complicated cases (incremental updates, etc.) abstracted away.

### Step 3 — Retrieval: Hybrid Search (Full-Text + Vector)
Goal for retrieval over the vectorized catalog: **high accuracy** *and* **fast search**. Approach: enable two search types and combine them (**hybrid search**).

1. **Full-text search:** Enable the new **`pgfts`** extension on HorizonDB (brings **Lucene-type** functionality to Postgres) and create a **full-text search index** on the product catalog.
2. **Vector search:** Provision a **DiskANN vector index** for better/faster performance than pgvector.

**Simplified search function:** A helper function lets you run sophisticated searches with simple syntax. Parameters shown:
- **Search string** — a textual description of the room's style, *deduced from the photo in an earlier app step* (that photo-→-description step is skipped here for time; its output text is reused).
- **Source table**, **column**, and a **search type** parameter — can be `vector`, `full_text`, or **`hybrid`** (combines both for the strengths of each).
- Plus some joins for nicer output.

**Hybrid result behavior:** With hybrid search, **exact keyword matches get boosted**. The search string contained the term **"mid-century modern,"** and the top hybrid result was a **"mid-century modern"** keyword match. Hybrid is ideal when keyword matches matter — but for this room-design scenario, **semantic/style matching** is more important.

### Semantic Re-ranking
To improve semantic relevance, add a single parameter to the search function: **`rerank => true`**.
- Uses the **Cohere semantic ranker** model behind the scenes.
- Results shift: **coffee tables** now rank as more relevant — likely because the search string includes "wood tones" and "dark vibes," matching the coffee table's surface/material.
- One-parameter change meaningfully improves result accuracy from a semantic point of view.

### Looking Inside the Search — Query Plan Visualization
The simplified search function could feel like a black box, so the extension provides a **"Visualize query plan"** button to inspect any query. Walking the plan for the rerank'd hybrid query:
- A large chunk of the plan is just **output-formatting joins** — safely ignored.
- The core **search function** structure:
  1. **Full-text search** and **vector search** run **in parallel**, producing two ranked lists with different priorities.
  2. **Hybrid step** applies **Reciprocal Rank Fusion (RRF)** — a simple mathematical formula that **averages/merges the two ranked lists** into one.
  3. Because reranking was enabled, a call into the **semantic re-ranking function** takes the **30 candidates** and **reorders them by semantic relevance**.
  4. Finally, the **top 10** best matches are returned (because top-10 was requested).

This shows how Postgres tooling/query plans make the "magic" search transparent.

### Step 4 — Knowledge Graphs (the heart of the intelligence)
The agent's core intelligence is **matching styles** — looking at the photo and determining stylistic matches for furniture. To do this, the team built a **knowledge graph of styles** for the product catalog.
- The graph-building step (another AI pipeline + SQL scripts) is **skipped for time** but is in the repo.
- The knowledge graph is stored **natively in Postgres as a real graph** using the **Apache AGE** extension, which brings **graph-database capabilities on top of relational Postgres**.
- Queried with **Cypher** (graph query language) — queries have a series of `MATCH` clauses to **traverse relationships** in the graph.

**Graph visualization (in the tooling):** Running a graph query renders the graph visually. In the center sits a style node — **"mid-century modern"** — connecting:
- A **coffee table** (category)
- **Chairs** of similar style
- **Bookcases** of the same mid-century-modern style

**Style-to-style similarity (going further):** A basic style graph just links furniture to a style. But what if there isn't enough furniture of a particular style for the room? Styles are also **similar to each other**, and that knowledge is encoded as a **`SIMILAR_TO` relationship between styles** — e.g., **mid-century modern is similar to bohemian**. This lets the agent traverse from a chair → similar styles → e.g., **similar area rugs**, fulfilling the room with a **much broader variety** of furniture options.

Takeaway on knowledge graphs: they're a **powerful, broadly applicable tool** that frequently **encapsulates domain knowledge**, enhancing the intelligence and quality of agents.

### Conclusion / Recap
Back in the app, the "agent details" reflect what was built. Using only built-in HorizonDB AI features, the demo:
- **Prepared data** for AI consumption via **AI pipelines** (chunk + embed + incremental trigger).
- Performed **powerful hybrid search** with sophisticated accuracy options.
- Used **semantic re-ranking** to pick the best matches.
- Found **related products via knowledge graphs**.

All achieved with **no external services, no added complexity**, and **very few lines of SQL**. A repo with all source code and sample queries is available; the sample dataset is only **60 rows** but enough to illustrate how simple the app is behind the scenes.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure HorizonDB** — Microsoft's new cloud-native PostgreSQL database (open-source Postgres engine + cloud-optimized scalable storage backend).
- **PostgreSQL** — the underlying open-source database engine HorizonDB is built on.
- **Postgres extension for VS Code** — Microsoft's tooling powering the entire demo (provisioning, model registry, pipeline UI, search functions, query-plan & graph visualization).
- **Model management (HorizonDB)** — checkbox-activated feature that bundles managed AI models into the database at provision time.
- **Managed models (auto-provisioned ×3)** — chat-completion model, text-embedding model, semantic-ranker model.
- **Bring-your-own-model (BYO)** — connect existing enterprise models to the database.
- **Microsoft Foundry** — provides the embedding model the AI pipeline calls to generate vectors.
- **Cohere semantic ranker** — the reranker model used for semantic re-ranking.
- **AI pipelines (HorizonDB)** — in-database, SQL-defined source → chunk → embed → sync flow with trigger-based incremental updates.
- **PG Vector (pgvector)** — vector storage/search extension for Postgres.
- **DiskANN vector index** — faster vector-search indexing than pgvector.
- **`pgfts`** — new full-text search extension bringing Lucene-style functionality to Postgres.
- **Hybrid search** — combines full-text + vector results.
- **Reciprocal Rank Fusion (RRF)** — formula that merges/averages two ranked result lists for hybrid search.
- **Semantic re-ranking** — `rerank => true` parameter; reorders candidates by semantic relevance via Cohere ranker.
- **Visualize query plan** — VS Code extension feature to inspect query internals.
- **Apache AGE** — Postgres extension providing graph-database capabilities for knowledge graphs.
- **Cypher** — graph query language used to traverse the style knowledge graph.
- **Zava room designer** — the demo application (sample app + repo).

## 🚀 Announcements / What's New
- **Azure HorizonDB — Public Preview.** Announced by **Satya Nadella the day before this session** at Build 2026. HorizonDB is the new cloud-native PostgreSQL offering with the AI feature set (built-in models, AI pipelines, AI functions) demonstrated here. Status: **Public Preview.**
- **AI feature set on HorizonDB** (presented as available in the preview): bundled **model management**, **AI pipelines**, **hybrid search**, **semantic re-ranking**, plus the **`pgfts`** full-text extension and **DiskANN** vector indexing on HorizonDB.
- *(No separate GA dates or additional roadmap items were explicitly stated in this session.)*

## 💡 Demos
Single continuous live demo building the Zava room designer's AI components:
- **App end-state** — "Design my room" auto-furnishes a Brooklyn-loft photo. *Proves:* HorizonDB can power a real, sophisticated style-matching agent.
- **HorizonDB provisioning w/ bundled models** — single checkbox enables model management + pgvector + DiskANN. *Proves:* the model-infrastructure setup step is eliminated. (Live click hiccupped → fell back to a pre-provisioned instance.)
- **Model registry inspection in SQL** — shows 3 auto-provisioned managed models. *Proves:* models ship with the DB and are queryable in SQL.
- **AI pipeline build + run** — SQL-defined chunk→embed→sync over `product_sample`: 60 rows → 116 chunks → 116 vectors. *Proves:* embedding generation is fully in-database with minimal SQL.
- **Incremental-update test** — insert one row → output count 116→117 asynchronously without blocking; new item appears in vector search. *Proves:* trigger-driven incremental embedding works and stays non-blocking.
- **Vector / full-text / hybrid search** — hybrid surfaces the "mid-century modern" keyword match at the top. *Proves:* hybrid combines keyword + semantic strengths.
- **Semantic re-ranking** — `rerank => true` reorders results (coffee tables rise for "wood tones / dark vibes"). *Proves:* one parameter improves semantic accuracy.
- **Query-plan visualization** — exposes parallel full-text + vector → RRF → semantic rerank of 30 candidates → top 10. *Proves:* the "black box" search function is fully inspectable.
- **Knowledge graph (Apache AGE + Cypher)** — visual graph centered on "mid-century modern" linking coffee table, chairs, bookcases; plus style-to-style `SIMILAR_TO` (mid-century modern ↔ bohemian) extending to similar area rugs. *Proves:* domain knowledge can be modeled as a native Postgres graph to broaden/enhance matching.

## 📊 Notable Stats / Quotes
- **3× higher throughput** on transactions (HorizonDB).
- **3× faster vector search** (HorizonDB).
- **Up to 15 read-only replicas**; scales to **very large databases**.
- **3 managed models** auto-provisioned with the database.
- Pipeline numbers: **60 source rows → 116 chunks → 116 vectors**; after one insert → **117**.
- Search internals: **30 candidates** reranked → **top 10** returned.
- Sample dataset in the repo: **only 60 rows**.
- > "So no external services, no complexity, and very few lines of SQL."
- > "Horizon DB is designed for this new era of AI agents."

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Clone the Zava room-designer repo (linked from the session) and run the 60-row sample app end to end.
  - Provision a HorizonDB public-preview cluster from the VS Code Postgres extension with model management + DiskANN enabled.
  - Build an in-DB AI pipeline (chunk → embed → sync) and verify trigger-driven incremental embeddings on insert.
  - Compare `vector` vs `full_text` vs `hybrid` search, then toggle `rerank => true` and inspect the query plan visualizer.
  - Experiment with Apache AGE + Cypher to model a small domain knowledge graph (incl. a `SIMILAR_TO` edge between categories).
- [ ] Questions:
  - What are the public-preview region availability, pricing, and quotas for HorizonDB and its bundled models?
  - Exact syntax of the AI pipeline DDL, the simplified hybrid-search function, and the `chunk`/embed steps (not fully shown on screen).
  - Which specific Foundry/Cohere model versions back the embedding and reranker models, and can BYO swap them?
  - How does the 3×-throughput / 3×-vector-search claim benchmark (vs. Azure Database for PostgreSQL Flexible Server? open-source Postgres?).
  - Cost/latency implications of running semantic reranking (Cohere) inline in queries at scale.
- [ ] Relevant to:
  - Azure data platform / PostgreSQL modernization work.
  - RAG and AI-agent retrieval architectures (vector + hybrid + rerank in one engine).
  - Any "search/recommendation inside the database" use case wanting to avoid external vector DBs/services.

## 🔗 Related
- [[Build2026]]
- 

---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/cosmos-db
  - topic/nosql
  - topic/schema-design
  - topic/ai
  - topic/azure
source: https://www.youtube.com/watch?v=9D9Npc-7VoQ
session_code: DEM310
event: Microsoft Build 2026
speakers: Marco, Sergey
duration_min: 26
aliases:
  - Ship code faster with AI-powered NoSQL schema design
---

# DEM310 — Ship code faster with AI-powered NoSQL schema design

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Marco (Azure Cosmos DB) & Sergey (Azure Cosmos DB) — demo-led session  
> **Duration:** ~26 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=9D9Npc-7VoQ)

## 🎯 TL;DR
This demo session shows how to use the **Azure Cosmos DB Agent Kit** — a set of NoSQL best-practice "skills" packaged for Copilot agents — to design optimal Cosmos DB schemas with AI guidance instead of lazily lifting-and-shifting relational tables into containers. Sergey walks through an e-commerce data model and demonstrates two common NoSQL anti-patterns (one-container-per-table, and over-embedding arrays that cause write amplification), then has Copilot read documented **access patterns + volumetrics** and propose an optimized container design, partition keys, indexing, and embedding strategy. The whole loop — design → emulator deploy → seed/validate → app code → measure Request Units (RU) — runs locally on the Cosmos DB emulator and is validated by measuring real RU cost before vs after. The punchline: optimizing the schema this way projected **~$980,000/month in savings** for the production workload. Key message: use AI to apply NoSQL best practices early *and* use the database's own RU metrics as an API to validate and measure every design decision.

## 🔑 Key Takeaways
- **Don't lift-and-shift relational schemas.** Mapping each table → its own container "works but is not optimal." NoSQL rewards modeling for **access patterns**, not just entities.
- The **Azure Cosmos DB Agent Kit** is a public repo of **100+ indexed best-practice rules/skills** for Cosmos DB, installable into any Copilot/agent that supports skills (demoed in the VS Code extension).
- Install with one command: `npx skills@azure-cosmos-db/cosmos-agent-kit` (deploys agent skills + Cosmos DB best-practice rules locally).
- **Document access patterns in structured context** so the agent can reason about them — Sergey defined 4 patterns (P1–P4) plus extended post-launch patterns.
- **Document volumetrics / production targets**, not just demo seed sizes. Test with 10 customers in dev but state "10 million in production" so the agent can project whether the design scales — *"every mistake you do early actually going to penalize you later"* in a distributed NoSQL DB.
- **Anti-pattern #1:** one container per table (naive) → measurably high RU even on small datasets.
- **Anti-pattern #2:** over-embedding into ever-growing arrays (e.g. embedding all orders in a customer doc) → **write amplification**: doc grew from ~60 KB / 26 RU to 300 KB+ / 130 RU over 50 iterations because every order update rewrites the whole growing array.
- **The optimized AI-guided design** collapsed domains: customer+orders together (partition by `customerId`, type discriminator, line items embedded in order doc) and products+categories together (partition by `categoryId`, since they're always accessed by category and don't justify separation).
- The **Cosmos DB emulator runs locally** (now with a **Linux v-next version GA as of the session day**, plus existing Mac/Windows support) — fast, free iteration before touching the cloud.
- **RU (Request Units) is Cosmos DB's compute charge per request** — use it as a built-in measurement API to compare designs objectively.
- Measured optimization wins: **P1 >50% RU saved, P2 ~75%, P3 ~40%**; P4 was a "red herring" (~0.09% — just overhead noise).
- **JSON has only primitive types** — convert decimals carefully and store all dates/timestamps as **ISO 8601 strings** to enable proper range queries, sorts, and comparisons in Cosmos DB.
- **It's an iterative loop:** if you don't understand a recommendation, ask Copilot to "explain why / rationalize it"; feed new requirements back in and ask what needs to change.

## 📚 Detailed Notes

### Why NoSQL & Azure Cosmos DB for modern + AI apps (Marco)
- Developers love NoSQL like Azure Cosmos DB because the **JSON schema is easy to evolve and iterate** on.
- Cosmos DB is optimized for **low-latency, highly scalable** applications — both traditional apps and increasingly **AI / agent** workloads.
- It's positioned as a single store for **operational data, vector data, and AI-native applications**: keep everything in one place, keep **embeddings up to date** as new operational data arrives, with **no data movement**.
- Built-in intelligent features: **integrated vector search, full-text search, and hybrid search with semantic reranking.**
- Integrates with tooling like **Microsoft Foundry** (host your LLMs), AI SDKs, etc. Built for **low-latency, globally distributed AI workloads.**
- Marquee proof point: **OpenAI uses Azure Cosmos DB very heavily for ChatGPT.**

### AI-assisted development for NoSQL (Marco)
- Beyond GitHub Copilot for general coding, there are tools to build on NoSQL even faster.
- AI can **generate queries and code from natural language.**
- **MCP (Model Context Protocol)** is framed as "USB-C for apps and agents" — a standard, secure way to connect agents to databases and services.
- This sets up the session's centerpiece: the **Azure Cosmos DB Agent Kit**, handed over to Sergey for the demo.

### Demo scenario & the core problem (Sergey)
- Scenario: a **classic e-commerce data model** — customer domain, products domain, sales order domain — as a starting point.
- The common (bad) modernization pattern: take the relational schema and mechanically **convert each table → a container**. It works, but it's **not optimal**.
- Goal of the demo: optimize this classic pattern using **NoSQL design knowledge + best practices** to iterate faster and avoid costly mistakes.

### What the Azure Cosmos DB Agent Kit is
- **"Nothing less than a set of best practices packaged as Copilot skills"** that you can deploy anywhere.
- Demoed inside the **VS Code extension**, but works in **any Copilot/agent that can consume skills.**
- **Public repo** — anyone can download/install: `npx skills@azure-cosmos-db/cosmos-agent-kit`.
- Deploys **agent skills + Cosmos DB best-practice rules** locally — **over 100 rules, indexed**, so when you ask Copilot to do something with NoSQL/Cosmos DB it pulls the **relevant subset** of skills depending on the task (evaluating a model vs writing SDK code, etc.).
- The whole demo is packaged into a **take-away repo** users can clone and follow along.

### Adding the right context: access patterns
- Crucial NoSQL principle: optimize **not just for the data model, but for access patterns.**
- Sergey starts from a relational-style model (tables + relationships) but **documents access patterns in structured context** so the agent can use them.
- **Four access patterns defined:**
  - **P1** — Get a customer and their **5 most recent orders** (with relative volume).
  - **P2** — Get **one order with its line items.**
  - **P3** — **CRUD** operation: placing an order.
  - **P4** — List all products in a category, **sorted by price ascending** (products domain).
  - Plus **extended order patterns** for post-launch.

### Adding the right context: volumetrics
- Developers often don't know how much data they'll have — but you must reason about the **order-of-magnitude** difference.
- Simplification: document both the **demo seed size and the production target.**
  - Demo: only **10 customers** (you don't test with a million in dev).
  - Production target: **10 million** customers — do this for every entity.
- This gives the agent a **range to project**: "whatever works for 10 — will it work for 10 million?"
- Critical in a distributed NoSQL DB because **early mistakes penalize you later at scale.**

### Iteration A — the naive / anti-pattern baselines
**Anti-pattern #1: one container per table**
- Each table becomes a container; pick a partition key; run all the documented access patterns via a simple API and measure **RU (Request Units)** — Cosmos DB's per-request compute charge.
- Result: **some RU values are surprisingly high even for a small dataset.**

**Anti-pattern #2: over-embedding growing arrays (write amplification)**
- NoSQL's flexibility tempts people to combine everything; taken to the extreme it creates **massive write amplification.**
- Demo: pre-seed the emulator with a **customer document that embeds an `orders` array** — every order is appended to the array on the customer doc.
- Simulating order creation = repeatedly updating (patching) the array. Observed over **50 iterations**:
  - Document grew to **300 KB+**.
  - RU to process the doc rose to **~130 RU**.
  - vs the start (iteration ~10): only **~60 KB and ~26 RU**.
- Lesson: because NoSQL *lets* you keep patching arrays, people do so **without understanding the compute penalty** — an anti-pattern to avoid.

### Iteration B — optimized, agent-guided design
- Sergey moves everything into a **Copilot prompt**, feeding in the **naive-run summary + access patterns + volumetrics as context**, and asks Copilot to:
  > "Propose optimal Cosmos NoSQL container design, partition key strategy, indexing — accounting for access patterns and volumes — and write full recommendations to an MD file."
- Under the hood Copilot reads: the access patterns, the volumetrics, the **agent-kit Cosmos DB best-practice skills**, parses what the naive iteration did, and checks the initial container-per-table setup.
- **Recommended model** (collapsing domains instead of one-container-per-table):
  - **Customer + Orders combined**, **partitioned by `customerId`** → customer docs + order docs in the same partition, distinguished by a **type discriminator**; **line items embedded** in the order document.
  - **Products + Categories combined**, **partitioned by `categoryId`** — because they're always accessed by category and the access patterns don't justify separating them; products kept as product docs with category normalized.
- This is an **iterative loop**: ask Copilot to **"explain why / rationalize it"** if unsure, or feed in **additional requirements** to refine. Sergey accepts the model and moves on.

### Deploy to the local emulator
- Next prompt: **create a local emulator instance with the partition keys and index policies** defined in the recommendation MD.
- **Beauty of Cosmos DB:** although the cloud service is Azure-only, the **emulator installs and runs locally** (here in a VM) — iteration is **fast and easy.**
- Initial DB had customers/orders/product-categories/products as **separate containers**; the emulator lets you do **point look-ups** (key/value) or **queries** (`SELECT * FROM c WHERE customerId = 'C...'`).
- Copilot creates the new database + containers (**customer-orders**, etc.) and an **updated index policy** including all properties used in the access patterns.

### Seed & validate data shapes
- Next prompt: **seed and validate data shapes** — take sample CSV data for the entities and convert into the **combined document shapes**, matching data types, then validate **shapes and counts.**
- Copilot builds a **data migration/conversion tool**; it calls out a key subtlety:
  - CSVs have a **special decimal parser**; JSON only has **primitive data types**, so decimals must be converted properly.
  - **Cosmos DB has no native date type** — convert all timestamps/dates to **ISO format strings**, which enables proper **date ranges, sorts, and comparisons.**
- After running the script and sampling/validating, the combined docs are visible:
  - **Customer document:** `type: customer`, `customerId` = partition key, `id` = unique partition-key + Cosmos-generated identifier, with **embedded order summaries.**
  - **Order document:** same partition key, `type: order`, with **order line items built in.**

### Build the application code & measure
- Next prompt: **build the app code to exercise all access patterns** — a simple structure of models, repository, service, and main, in Python — explicitly instructing **"use Cosmos DB best practices."**
- Output is instructed to **summarize results for P1–P4** so they can be compared against the naive pre-run to **measure RU before vs after.**
- Copilot **re-reads the Cosmos DB best-practice skills — but a different section** this time: the **SDK best practices** (retries, **singleton client**, etc.) rather than the data-modeling ones. (A minor hiccup: it got confused by an example `.env` entry.)
- Reinforced reusable workflow: whenever you have **new requirements**, feed Copilot your **existing app structure + new requirements** and ask **what needs to change and what needs to be fed in.**

### Results — measuring the win
- Comparison table: **Iteration A (naive) vs Iteration B (optimized)** across P1–P4, showing **delta %** and **RU saved per request.**
  - **P1 (B1): >50% RU saved.**
  - **P2 (B2): ~75% RU saved** — also demonstrates **point read vs query** (single-doc retrieval via point read is cheaper than a query).
  - **P3: ~40% RU saved.**
  - **P4: ~0.09% — a "red herring,"** essentially just overhead noise.
- **Production cost projection** (applying savings to the documented volumetrics):
  - **~3,000 reads/sec saved** for P1 and P2 combined.
  - **~500 writes/sec saved** for P3.
  - Converting those savings to **Cosmos DB list price → ~$980,000 per month saved** by optimizing the schema.
- Closing message: customers **leave huge money on the table** by doing **lazy conversions**. The biggest value of NoSQL is taking **full advantage of its flexibility while using the database's own RU API to validate and measure** that your design is optimal — quickly, without building complex synthetic test harnesses.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Cosmos DB** — Microsoft's globally distributed, low-latency NoSQL database; the focus of the session.
- **Azure Cosmos DB Agent Kit** — public repo of 100+ indexed NoSQL/Cosmos DB best-practice rules packaged as **Copilot skills**, installable into any skill-aware agent.
- **Azure Cosmos DB Emulator** — local emulator for fast, free iteration; **Linux v-next version GA as of the session day**, alongside existing Mac/Windows support.
- **Request Units (RU)** — Cosmos DB's per-request compute charge; used as the measurement metric for design optimization.
- **Integrated vector search / full-text search / hybrid search with semantic reranking** — Cosmos DB's built-in intelligent query features.
- **Microsoft Foundry** — platform for hosting LLMs; integrates with Cosmos DB for AI workloads.
- **MCP (Model Context Protocol)** — "USB-C for apps and agents"; standard, secure way to connect agents to databases/services.
- **GitHub Copilot** — AI coding assistant; the demo runs the Agent Kit skills through Copilot in the VS Code extension.
- **VS Code extension** — host used to demo the Agent Kit (works in any skill-capable Copilot/agent).
- **`npx skills@azure-cosmos-db/cosmos-agent-kit`** — one-line install command for the Agent Kit.
- **Python + Cosmos DB SDK** — used to build the app code; SDK best practices include retries and a **singleton client.**
- **JSON / ISO 8601 date strings** — document format; dates stored as ISO strings since Cosmos DB has no native date type.
- **MongoDB / DynamoDB** — other NoSQL databases referenced when polling the audience.
- **OpenAI / ChatGPT** — cited as a heavy production user of Azure Cosmos DB.

## 🚀 Announcements / What's New
- **Azure Cosmos DB Emulator — Linux v-next version GA "as of today"** (session day). An existing emulator already shipped; this is the newer "v-ex"/v-next Linux build for Mac/Windows/Linux laptops. (Stated as generally available that day.)
- **Azure Cosmos DB Agent Kit** highlighted as publicly available (public repo, `npx` install) — presented as the session's key tool. (Promoted as available; exact GA/preview wording not specified beyond "public repo anybody can download and install.")

## 💡 Demos
- **End-to-end AI-guided NoSQL schema optimization** (Sergey), all on the local Cosmos DB emulator:
  1. **Naive baseline (Anti-pattern #1):** one-container-per-table, ran P1–P4, measured RU → some high even on small data. *Proves lift-and-shift is suboptimal.*
  2. **Over-embedding baseline (Anti-pattern #2):** customer doc with an embedded growing `orders` array; 50 update iterations grew the doc to **300 KB+ / ~130 RU** (from ~60 KB / ~26 RU). *Proves write amplification from unbounded array embedding.*
  3. **Optimized design via Copilot:** fed access patterns + volumetrics + agent-kit skills → Copilot wrote a recommendations MD collapsing domains (customer+orders by `customerId`; products+categories by `categoryId`; embedded line items). *Proves AI can apply NoSQL best practices to produce an optimal model.*
  4. **Emulator deploy:** Copilot created the new DB/containers + index policies from the MD.
  5. **Seed & validate:** Copilot built a CSV→JSON conversion tool, handled decimal parsing + ISO date conversion, validated shapes/counts; combined docs (customer with embedded order summaries, order with embedded line items) shown live.
  6. **App code + measurement:** Copilot generated Python (models/repository/service/main) using SDK best practices, re-ran P1–P4.
  7. **Results table:** A vs B comparison → **P1 >50%, P2 ~75%, P3 ~40% RU saved**, P4 negligible. *Proves measurable optimization → projected **~$980k/month** production savings.*
- (Minor live hiccups: a momentary lost-connection on the shared screen, and Copilot briefly confused by an example `.env` entry — both recovered.)

## 📊 Notable Stats / Quotes
- **~$980,000 per month** projected savings from schema optimization at production scale.
- **~3,000 reads/sec** saved (P1 + P2) and **~500 writes/sec** saved (P3) at production volume.
- Over-embedding anti-pattern: doc grew to **300 KB+** and **~130 RU** after 50 iterations, up from **~60 KB / ~26 RU**.
- RU savings: **P1 >50%, P2 ~75%, P3 ~40%, P4 ~0.09%** (red herring).
- Demo vs production volumetrics: **10 customers** (dev) → **10 million** (production target).
- **100+ indexed rules** in the Azure Cosmos DB Agent Kit.
- **OpenAI uses Azure Cosmos DB very heavily for ChatGPT.**
- *"Every mistake you do early actually going to penalize you later"* — on the cost of bad early NoSQL modeling at scale.
- *"USB-C for apps and agents"* — on MCP.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install the Azure Cosmos DB Agent Kit (`npx skills@azure-cosmos-db/cosmos-agent-kit`) into VS Code Copilot and try it against a sample relational schema.
  - Spin up the new **Linux Cosmos DB emulator** locally and run the naive-vs-optimized RU comparison loop.
  - Practice documenting **access patterns (P1…Pn) + volumetrics (dev seed vs prod target)** as structured context for the agent.
- [ ] Questions:
  - What's the exact public repo URL / org for the Agent Kit, and how often are the 100+ rules updated?
  - How does the RU projection map demo numbers to the ~$980k figure (which list price / region assumptions)?
  - Does the Agent Kit support APIs beyond Cosmos DB NoSQL (e.g. MongoDB API), and other languages beyond Python?
- [ ] Relevant to:
  - Any Cosmos DB / NoSQL data-modeling or modernization work.
  - AI-app backends needing operational + vector data co-located.

## 🔗 Related
- [[Azure Cosmos DB]] — the NoSQL database whose data-modeling best practices this session packages into an AI agent kit.
- [[OD820 - Designing Reliable Multi-Agent Apps with Azure Cosmos DB]] — sibling Cosmos DB session; agentic apps + memory on the same platform.
- [[OD821 - Building Azure DocumentDB on Open-Source Foundations]] — the open-source document-database engine underpinning Cosmos DB for NoSQL.
- [[Model Context Protocol (MCP)]] — the protocol that surfaces the Cosmos DB Agent Kit's rules as Copilot-callable skills.
- [[Request Units (RU) and Cosmos DB cost optimization]] — the RU/write-amplification economics the demo optimizes against.
- [[NoSQL data modeling — embedding vs referencing]] — the core schema-design tradeoff (over-embedding growing arrays) the AI guidance corrects.
- Source list: [[2026 Build Session List]]

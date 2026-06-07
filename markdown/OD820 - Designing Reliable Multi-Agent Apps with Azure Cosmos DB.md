---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/cosmos-db
  - topic/multi-agent
  - topic/ai
  - topic/reliability
  - topic/azure
source: https://www.youtube.com/watch?v=2mZNsC58S64
session_code: OD820
event: Microsoft Build 2026
speakers: Justine Kouchi (PM, Azure Cosmos DB), Ayush Kataria (Software Engineer, Azure Cosmos DB)
duration_min: 46
aliases:
  - Designing Reliable Multi-Agent Apps with Azure Cosmos DB
---

# OD820 — Designing Reliable Multi-Agent Apps with Azure Cosmos DB

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Justine Kouchi (Program Manager, Azure Cosmos DB) · Ayush Kataria (Software Engineer, Azure Cosmos DB)  
> **Duration:** ~46 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=2mZNsC58S64)

## 🎯 TL;DR
This session walks through building a **production-grade multi-agent AI application** — a personalized travel assistant — on top of **Azure Cosmos DB**, using it as the durable backbone for agent state, memory, and search. The first half is about **agentic memory**: why it beats RAG, the three memory layers (state, short-term, long-term), and the four long-term memory types (facts, procedural, episodic, user summary) managed automatically by the new **Cosmos DB Agent Memory Toolkit** (public preview). The second half is about **reliability and scale**: the new **Cosmos DB Agent Kit** that bakes best-practice instincts into your coding agent (GA), plus platform features that remove brittle app-side error handling — **per-partition automatic failover** (GA), **cross-container distributed transactions** (preview), **integrated embeddings** via Microsoft Foundry, and **global secondary indexes** (GA). The thesis: let the Cosmos DB platform do the heavy lifting so your agents stay simple and your app stays reliable.

## 🔑 Key Takeaways
- **Multi-agent beats single-agent** for non-trivial domains: smaller focused contexts per agent reason better, agents can be developed/updated independently, and the system is composable — vs one monolithic system prompt that confuses the model and hits context-window limits.
- An **orchestrator agent is the "front door"** — its only job is to read intent and route to the right specialist (hotel, dining, activity). Specialists each own a single domain with their own prompt and tools.
- **Agents never touch the database directly** — they go through an **MCP server** (tools like recall memories, discover places, transfer between agents). MCP decouples tools from agent code so tools can be reused and updated independently.
- **Agentic memory > RAG** for agent apps: RAG is static, shared, similarity-only, and stateless; agentic memory is **dynamic, user-specific, salience-scored (importance + confidence + recency), learns from every interaction, and is time-aware with TTL**.
- Three precise memory concepts: **State** (full app snapshot to restore an exact point), **short-term memory** (within-session conversation history), and **long-term memory** (cross-session, enables personalization and "building a relationship").
- **Four long-term memory types**, each with a different lifetime: **Facts/semantic** (durable, never expire), **Procedural** (inferred behavioral patterns, never expire by default), **Episodic** (time/place-bound, expire after ~90 days default), and **User Summary** (rolling synthesis regenerated every few turns, fed into the orchestrator's system prompt).
- The **Agent Memory Toolkit** runs as a **background runtime** hanging off the same Cosmos DB account, with its own `memories` container; the agent never calls it directly. It automates extraction, conflict resolution, summarization, and recall on the right cadence.
- **Memory extraction is threshold-driven & asynchronous**: a background pipeline runs every Nth turn, asks the LLM "anything new worth remembering?", classifies it (fact/procedural/episodic), and writes it back to Cosmos DB without blocking the agent loop. Greetings (hi/hello) are deliberately *not* extracted.
- **Conflict resolution preserves an audit trail**: when facts contradict (e.g. "I'm vegan" → later "I love steak"), the toolkit doesn't delete the old fact — it marks it **`superseded by`** the winner, so you can debug *why* the system changed its mind months later.
- **Memory-conditioned search is the payoff**: before any specialist searches, it recalls relevant memories and encodes them as **explicit filters** — so "show me hotels in Tokyo" silently becomes "show me *luxury* hotels in Tokyo." Personalization is baked into the query, not bolted on.
- The **Cosmos DB Agent Kit** is a *repo of skills* (not a service) that any skills-compatible coding agent (GitHub Copilot, Claude Code, Gemini CLI) can pull in — giving it years of Cosmos DB instincts on partitioning, indexing, and RU economics. Drop it into CI/PR reviews for a free expert opinion on every change.
- For **five-nines availability**, use the **active-active** pattern: either **multi-writer** (leaderless, all regions accept reads+writes, RTO ≈ 0 / RPO ≈ 0) or **single-writer + per-partition automatic failover** (fail over individual partitions, not whole regions — "brownout vs blackout").
- **Per-partition automatic failover (GA)** gives zero downtime, zero data loss, zero touch — the SDK does the heavy lifting; no app-side coordination or expensive whole-region failover decisions.
- **Cross-container distributed transactions (preview)** give atomic execution across partitions/containers (e.g. book-trip = update status + store memory + emit event, all succeed-or-fail together), removing brittle multi-write error handling from app code.
- **Integrated embeddings** let you write the raw message to Cosmos DB and have embeddings generated **asynchronously via Microsoft Foundry** at write time — eliminating the synchronous external OpenAI call that caused rate-limiting (Ayush saw 30–40s waits while testing).
- **Global secondary indexes (GA)** create an auto-synced copy container partitioned for a *different* access pattern, turning heavy cross-partition dashboard queries into single-partition lookups — demoed at **~90% RU savings** (30 RU → 3 RU).

## 📚 Detailed Notes

### The scenario: a multi-agent travel assistant
The running example throughout the talk is a **travel assistant** — a multi-agent AI application that helps users plan personalized trips. Its core surface is a **chat feature**: a user types something like *"plan a trip to Paris,"* and that single message kicks off a rich back-end flow.

A single conversational **turn** looks like this:
1. The message lands in the **orchestrator agent**.
2. The orchestrator routes it to specialist agents (e.g. the **hotel agent**).
3. The system **looks up existing memories** about the user in Azure Cosmos DB.
4. The initial query is **embedded with Azure OpenAI** into a vector, so it can be searched against existing metadata (places, restaurants, hotels in Paris).
5. The response is sent back with the data found, helping the user plan.
6. Eventually, when the trip is created, the system **extracts memories** so it remembers the interaction next time the user logs in.

### Designing around the user journey: where latency vs reliability matters
A key framing: **different parts of the user flow have different priorities.**

- **Front half (early in the conversation):** **latency and personalization** matter most. Agents must remember key things about users and respond fast — otherwise the user gets frustrated and defects to a competitor travel site.
- **Back half (creating/booking the trip):** **consistency and reliability** matter most. You must not double-book a trip or forget something already discussed.

Keeping the user's perspective in mind across the flow is what ultimately drives the architecture decisions in the rest of the talk.

### Why multi-agent? The single-agent failure modes
Ayush frames multi-agent by first showing **what goes wrong with a single agent**:
- One agent handling **every domain in a single system prompt** → the model gets **confused**; it doesn't know which capability to invoke or when.
- **No separation of concerns** → every change risks breaking something else; you can't improve one area of expertise without touching everything.
- As conversations grow, you **hit context-window limits** → the model forgets earlier parts of the conversation, producing inconsistent behavior.

**The multi-agent solution** replaces the monolith with **specialized agents**, each with a focused prompt and a specific tool set, with an **orchestrator on top** routing by intent. The big wins:
1. **Smaller, more focused context per agent → better reasoning.**
2. **Independent development/updates** — adding a new specialist doesn't require touching existing ones.
3. **Composability** — plug in new capabilities without rewriting the whole system.

### Agentic memory vs RAG (the most important idea in the talk)
Ayush calls this the most interesting part. Most people know **RAG** (retrieval-augmented generation): a fixed knowledge base, embedded documents, retrieve relevant chunks on a question and feed them to the model. It works for what it does, but has fundamental limits for **agent-based** apps. The comparison:

| Dimension | Traditional RAG | Agentic Memory |
|---|---|---|
| Freshness | **Static** — fixed until you explicitly update it | **Dynamic** — grows automatically with every interaction |
| Scope | Same results for everyone (shared corpus) | **User-specific** — stores individual preferences/history; two users get completely different experiences |
| Retrieval | By **similarity alone** (nearest in embedding space) | **Salience scoring** — factors in **importance, confidence, and recency** |
| Learning | Doesn't learn — pure lookup | **Actively learns and adapts** — every conversation extracts new knowledge |
| Time | No concept of time | **Cross-session persistence with TTL policies** |

This distinction motivates the whole memory architecture: agents need memory that is personal, evolving, and time-aware — not just a static retrieval index.

### Full system architecture
Zooming out, the end-to-end architecture of the travel app:

- **Orchestrator agent** — the **front door**. Every conversation comes through it first; its only job is to understand intent and decide which specialist handles it.
- **Specialized agents** — **hotel, dining, activity**. Each owns a single domain, has its own system prompt, and pulls from a focused set of tools.
- **MCP server** — *none of the agents talk to the database directly.* They go through the **Model Context Protocol (MCP) server**, which exposes tools like **recall memories, discover places, transfer between agents**, and more. The point of MCP is **decoupling**: you can update or add tools without touching agent code, and one tool can be reused across every agent.
- **Azure Cosmos DB** — sits under the MCP layer and stores everything the app needs: **sessions, messages, places, trips, API events**, and more. Places are searched using **hybrid search**. **Every container uses a hierarchical partition key**, so the system is **multi-tenant from day one**.
- **Agent Memory Toolkit** — a **new Cosmos DB offering** that hosts the memory layer. It's a **separate background runtime** that hangs off the *same* Cosmos DB account, owning its own container called **`memories`** where conversation turns, extracted facts, user summaries, and thread summaries are all stored. **The agent never calls it directly.**
- **Azure OpenAI** — provides the **LLM reasoning and embedding** capabilities; a shared utility feeding both the agent runtime and the toolkit pipeline.

### Memory vocabulary: state vs short-term vs long-term
Before going deeper, the speakers insist on precise terms, because "memory" is used loosely. Three distinct concepts:

- **State** — a **snapshot of the entire application** at a given moment. Contains everything needed to restore the app to that exact point: what the user said, what the agent decided, what tools were called.
- **Short-term memory** — what happens **within a single session**: the conversation history, messages going back and forth. This is what lets an agent refer back to something said three messages ago and stay coherent.
- **Long-term memory** — **persists across sessions**. When a user returns days or weeks later, the agent recalls what it learned previously (preferences, past decisions, feedback). This is what enables personalization and learning over time — *the difference between an agent that starts fresh every conversation and one that builds a relationship with the user.*

**How they're implemented in the travel app:** all three are used. **State** via **LangGraph's Cosmos DB checkpointer** integration; **short-term and long-term memory** via the dedicated **Agent Memory Toolkit** backed by Cosmos DB.

### The four long-term memory types
Not all long-term memories are the same — the toolkit models **four types**, each with a different lifetime, creation method, and usage:

1. **Facts (semantic memory)** — simple, durable statements about the user: *"user is vegetarian," "travels with a wheelchair," "lives in Seattle."* Objectively true, change rarely, and **should never expire**.
2. **Procedural memory** — **behavioral patterns / preferences inferred from how the user actually behaves** over multiple conversations: *"tends to book boutique hotels over chains," "prefers late dinners."* Softer than facts — the user may never say them out loud; they **emerge from repetition** and **never expire by default** (behavioral patterns are usually stable).
3. **Episodic memory** — tied to a **specific time and place**: *"visited New York City last spring," "loved seafood on my Barcelona trip."* Lets the system reference a past trip when planning a new one. **These expire — default 90 days** — because episodic memory gets noisy fast (a recommender doesn't need to remember a coffee shop you visited 4 years ago).
4. **User summary** — different from the other three. **Not extracted from a single message**; it's a **rolling synthesis of who the user is**, regenerated automatically every few turns: *"frequent solo traveler, vegetarian, prefers cultural over outdoor, mid-range budget hotels."* The **orchestrator pulls this into its system prompt at the start of every conversation**, so even on day one of a brand-new session the agent already "knows" the user.

### Making memory intelligent: the four toolkit APIs
Storing memories is only half the challenge — the real value is the system **actively managing its own knowledge**. The toolkit class exposes public-facing APIs: **extract memories, generate thread summary, generate user summary, and reconcile memories** (conflict resolution). Four mechanisms:

**1. Threshold-driven extraction (`extract memories`)** — the user never has to say "remember this." As the conversation unfolds, a **background pipeline runs every Nth turn** and asks the LLM *"is there anything new about this user worth remembering?"* If yes, it pulls out the fact, **classifies it** as fact / procedural / episodic, and writes it back to Cosmos DB. **The agent loop doesn't wait** — it's fully asynchronous. (Greetings like "hi / good morning" are deliberately excluded by prompt rules.)

**2. Conflict resolution (`reconcile memories`)** — real conversations contradict themselves ("I'm vegan" on Monday → three weeks later raves about a steakhouse). On a **separate cadence**, the toolkit sweeps the user's facts and asks the LLM to classify pairs of related memories as **duplicates or updates**. When it finds one, it **doesn't delete** the old memory — it marks it **`superseded by`** the winner, **preserving an audit trail**. The user never sees a contradiction, but a developer debugging six months later can see exactly when and why the system changed its mind.

**3. Rolling summaries** — conversations get long and token budgets are finite, so the toolkit generates **two kinds of summaries on a cadence**: a **thread summary** (the current conversation/session) and a **user summary** (who the user is across all conversations). For the demo, both regenerate **every 5 turns**; in production the cadence is a **tunable default**. The orchestrator pulls these into context at the start of every turn, so **even after 100 messages the agent doesn't lose the plot**.

**4. Memory-conditioned search (the payoff)** — everything else is "plumbing"; this is where memory shapes what the user actually sees. **Before any specialist searches** for a hotel or restaurant, it **recalls memories first** — asking the toolkit what's known about this user relevant to the query. The recall returns relevant facts/preferences, and the agent **encodes them as explicit filters** on the search call. That's how *"show me hotels in Tokyo"* silently becomes *"show me **luxury** hotels in Tokyo."* Personalization is **baked into the query itself**, not bolted on at the end.

Crucially, the toolkit runs **all of these automatically in the background on the right cadence**, with no coordination required from application code — so the agent stays simple.

### Prompts are code
The LLM prompts driving extraction/classification are **scripts checked into the codebase** (e.g. an `extract memories` prompt file). They give the LLM detailed instructions on the four memory types — the required structure, plus **rules and examples** defining what counts as a fact vs procedural vs episodic — and rules on which turns to extract (e.g. greeting-only turns are skipped). Treating prompts as versioned code is part of what makes the behavior reliable and tunable.

### Reliability & availability: SLO, RPO, RTO
The second half pivots from "it works in a demo" to "it runs at scale without setting money on fire." Justine grounds reliability in **three user-facing metrics**:

- **SLO (Service Level Objective)** — the **target level of service availability**. For a global app serving users worldwide at any hour, the goal is essentially **no downtime**.
- **RPO (Recovery Point Objective)** — *how much data could you lose* in the window before a disaster strikes. For distributed cloud apps, disaster is "**not if, but when**."
- **RTO (Recovery Time Objective)** — *how long is it acceptable to be down* after a disaster.

The target for this app: **five nines (99.999%) of availability**, always-up, globally available.

### The active-active pattern (two flavors)
To hit five nines, Cosmos DB offers the **active-active** pattern, achievable two ways:

- **Multi-writer** — **multiple Cosmos DB regions all simultaneously accepting reads *and* writes**. It's **leaderless**: writes can land in any region and are **conflict-resolved across all regions**. **RTO ≈ 0** (all regions already online) and **RPO ≈ 0** (just conflict-resolution + cross-region replication time).
- **Single-writer + per-partition automatic failover** — a **new feature** that fails over at the **individual partition level** instead of waiting for an entire region to go unavailable. This is the **"brownout vs blackout"** insight: it's far more common for an individual partition to fail than for a whole region to go down. Healthy regions/partitions keep reading and writing from the primary write region; any partition with issues **fails over seamlessly**. The application handles none of it — **no app-side failure coordination and no expensive whole-region-failover decision**. Result: the active-active pattern with five-nines availability **without** running multiple writers.

**Per-partition automatic failover** delivers **zero downtime, zero data loss, and zero touch** — the SDK does the heavy lifting.

### Consistency across containers: distributed transactions
Availability guarantees writes *can* land, but you still need **consistency**. Example: when a user clicks **"book it,"** three independent writes happen — (1) update the trip's status to **booked** in the trips container, (2) **store a memory** so the agent remembers the booking, and (3) **emit a booking event** in the events container for downstream/logging systems. If one fails, it's a terrible experience (the agent "forgets" the booking).

**Cross-container distributed transactions (public preview)** give **atomic execution of multiple requests**. Previously a transaction was limited to a single partition key; now you get **atomic transactions across partitions or even across containers**. All three operations **succeed or fail together** — consistency at the container level, with the platform doing the heavy lifting so you delete a pile of brittle app-side error handling.

### Integrated embeddings (let the platform embed)
Another chance to offload coordination. **Today's flow:** user prompt → app must **call Azure OpenAI to generate embeddings** *before* it can do anything with Cosmos DB. That synchronous external call is a **rate-limiting / error-handling risk** — you can see write-loss or availability problems even when Cosmos DB itself is fine, purely from the developer's coordination/error handling. (Ayush notes he was **rate-limited repeatedly while testing**, sometimes waiting **30–40 seconds** for an LLM response.)

**With integrated embeddings**, you **write the raw message straight to Cosmos DB**, and embeddings are **generated asynchronously**, **automatically integrated with Microsoft Foundry**. You define the **Foundry integration** plus the **source and target properties** to embed on, getting full control without an external pipeline. The app focuses on business logic instead of plumbing external embedding calls.

### Global secondary indexes (scaling new query patterns)
As the app grows, new **cross-tenant dashboard** needs appear: *"how many trips next month?", "what's the top destination?"* The trips container uses a **hierarchical partition key (tenant → user → trip ID)**, which makes **per-user** queries fast — but a broad "how many trips to Paris across all tenants?" query is a **cross-partition query**, routed to **every physical partition** to count and aggregate. That's expensive.

**Global secondary indexes (GSIs, now GA)** solve this by creating a **copy of the data partitioned on a different key** (e.g. **destination**). Finding all Paris trips then hits **one partition instead of all of them**. GSIs **automatically sync** from the source container into a copy container better suited to the new query pattern, **increase query efficiency**, transform heavy cross-partition queries into single-partition lookups, and **isolate heavy workloads** into the secondary container so they don't impact the primary.

You can also **project only the properties you need** into the GSI — in the demo, the heavy `days` array (per-day activity details) is filtered out, so the secondary schema matches how it's queried. GSIs can be added **later in the app's lifecycle** as requirements evolve — you don't need to predict the dashboard on day one.

### Closing: bringing it together
Justine's wrap-up takeaways: (1) give agentic apps **durable memory that's scalable by design**, and remember the **different memory types**; (2) **ship faster with an AI-native dev experience** (the Cosmos DB Agent Kit) to enforce best practices; (3) think about **reliability and availability** and **use platform features to avoid brittle error handling in app code**; (4) aim for **mission-critical, ready-to-ship AI applications**. Resources include the **Cosmos DB travel multi-agent** demo code (with a **workshop** to build it yourself) plus links for the day's announcements.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Cosmos DB** — the distributed database serving as the durable backbone for all agent state, memory, and search in the app.
- **Agent Memory Toolkit for Azure Cosmos DB** — new offering; a background runtime hosting the memory layer with its own `memories` container; automates extraction, conflict resolution, summarization, and recall. *(Public preview.)*
- **Cosmos DB Agent Kit** — a repo of best-practice *skills* (one-line install) that a coding agent pulls in to get Cosmos DB instincts (partitioning, indexing, RU economics, modeling). *(GA.)*
- **LangChain × Azure Cosmos DB integration** — integration package with all Cosmos DB integrations for LangChain/LangGraph used to build the app; includes a vector store integration. *(GA.)*
- **LangGraph Cosmos DB checkpointer / checkpoint store** — used for **state** management (state checkpointing) in the multi-agent app.
- **Azure OpenAI** — provides LLM reasoning + embedding generation; shared by the agent runtime and the toolkit pipeline.
- **Microsoft Foundry** — the integration target for **integrated embeddings** (async embedding generation at write time).
- **Model Context Protocol (MCP) server** — decoupling layer between agents and the database; exposes reusable tools (recall memories, discover places, transfer between agents).
- **Hierarchical partition keys** — used on every container (e.g. tenant → user → trip ID) for multi-tenancy from day one.
- **Hybrid search** — used for searching "places" in Cosmos DB.
- **Per-partition automatic failover** — fails over at partition granularity for active-active single-writer setups. *(GA.)*
- **Cross-container distributed transactions** — atomic execution across partitions/containers. *(Public preview.)*
- **Integrated embeddings** — write raw text to Cosmos DB; embeddings generated asynchronously via Foundry; define source/target properties. 
- **Global secondary indexes (GSIs)** — auto-synced copy container partitioned on a different key, with property projection, for new query patterns. *(GA.)*
- **Salience scoring** — memory-retrieval ranking factoring importance, confidence, and recency (vs RAG similarity-only).
- **TTL (time-to-live) policies** — enable time-aware, expiring memories (e.g. episodic default 90 days).
- **Coding agents named as Agent Kit consumers:** GitHub Copilot, Claude Code, Gemini CLI ("and others").

## 🚀 Announcements / What's New
- **Agent Memory Toolkit for Azure Cosmos DB — Public Preview.** Provides fact extraction, auto-summarization, and packaged instructions/prompts for conflict resolution, extracting the different memory types, and user/thread summarization.
- **Cosmos DB Agent Kit — Generally Available.** One-line install; a repo of skills any skills-compatible coding agent can use; works in CI/PR reviews to give every change a "Cosmos DB expert opinion" at no extra cost.
- **LangChain × Azure Cosmos DB integration — Generally Available.** Full Cosmos DB integration package for LangChain/LangGraph, including vector store and LangGraph checkpoint store.
- **Per-partition automatic failover — Generally Available.** Zero downtime, zero data loss, zero touch; enables active-active with five-nines availability without multiple writers.
- **Cross-container distributed transactions — Public Preview.** Atomic transactions across partitions and containers (previously limited to a single partition key).
- **Global secondary indexes — Generally Available.** Auto-synced, differently-partitioned copy containers with property projection to optimize new/evolving query patterns.
- **Integrated embeddings (with Microsoft Foundry)** — presented as a current capability to generate embeddings asynchronously at write time (preview/GA status not explicitly stated in the talk).

## 💡 Demos
- **Demo 1 — Existing user "Tony" (preloaded preferences).** Signs in as Tony and chats *"Hi, I am planning a trip to Tokyo."* The API server logs show the request hitting the **orchestrator**, which infers intent and picks tools. Asking *"what are my hotel preferences"* returns personalized answers (prioritizes reliable Wi-Fi over price for business trips; enjoys rooftop bars and quiet evenings on work travel). In the Azure portal `memories` container, a query shows the stored **facts**: "Tony prefers luxury five-star hotels," "loves art museums and contemporary galleries." **Proves:** the toolkit extracts memories, stores preferences in Cosmos DB, and the agent leverages them back into the conversation.
- **Demo 2 — New user "Peter" (no memories) + conflict resolution.** Confirms in the portal that Peter has nothing stored. Starts a session, *"I'm planning a trip to Paris"* → stored as a **turn**. Says *"I am vegan"* → portal shows it extracted as a **fact**. Then deliberately contradicts: *"I have started eating meat."* Filtering for **facts** shows a **new fact** ("started eating meat, changing from vegan") and the **old "vegan" fact marked `superseded by` the new fact's ID** — the audit trail in action. **Proves:** asynchronous extraction + conflict resolution with audit preservation.
- **Demo 3 — Memory-conditioned recommendations.** Asks Peter's assistant to **recommend restaurants**; the orchestrator routes to the **dining agent**, and the results say *"based on your updated dietary preference"* — automatically picking up the **resolved** current fact (omnivore, not vegan). **Proves:** recall + filter injection respects conflict-resolved state.
- **Demo 4 — Auto-summarization at 5 turns.** After enough turns (demo cadence = 5), asks *"create an itinerary for Paris for 3 days."* The portal shows a **user summary** was extracted ("planning a trip to Paris; changed dietary preference from vegan to omnivore") alongside a **thread summary**, and the **itinerary agent** generates the full itinerary. **Proves:** rolling summaries + multi-agent itinerary generation.
- **Demo 5 — Cosmos DB Agent Kit.** One-line install adds best-practice skills. Prompts *"can you provide recommendations on best practices for my data model?"* and gets a **report ranked by impact (highest ROI first)** with critical and high-importance recommendations; the developer can **push back interactively** and ask why a recommendation was made. **Proves:** AI-native, interactive best-practice review usable in CI/PR.
- **Demo 6 — Global secondary index in the portal.** Pulls up the **trips** container (id, user ID, trip; heavy `days` array). Defines a GSI **"trips by destination,"** **projecting out** the `days` array. Runs *"all trips to Paris, France"* on the **primary** container: 500 results, **~30 RUs**. Runs the **same query against the GSI**: same answer, **~3 RUs** — **~90% savings**. **Proves:** GSIs turn cross-partition scans into cheap single-partition lookups.

## 📊 Notable Stats / Quotes
- **Five nines (99.999%) availability** — the app's reliability target.
- **~90% RU savings** on the dashboard query via GSI: **~30 RUs → ~3 RUs** (savings vary by query and physical partition layout).
- **Episodic memory default TTL: 90 days.** Summaries regenerate **every 5 turns** in the demo (tunable in production). Extraction runs **every Nth turn** asynchronously.
- **"Even after 100 messages, the agent doesn't lose the actual plot."** — on rolling summaries.
- **"There's a gap between *it runs* and *it runs at scale without setting money on fire*."** — Ayush, on the Agent Kit's reason for existing.
- **"In Cosmos DB, that gap is paved with decisions that you make on day one and pay for on day 90."** — Ayush, on partition keys/indexing/document shape.
- **"Brownout vs blackout"** — the framing for per-partition vs whole-region failover.
- **"Show me hotels in Tokyo silently becomes show me luxury hotels in Tokyo"** — memory-conditioned search.
- Ayush was **rate-limited repeatedly while testing, sometimes waiting 30–40 seconds** for an LLM response — motivating integrated embeddings.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Clone the **Cosmos DB travel multi-agent** demo + workshop and build the app end-to-end; install the **Cosmos DB Agent Kit** in a repo and run it against an existing Cosmos service in CI/PR; spin up the **Agent Memory Toolkit (preview)** and watch facts/conflict-resolution/summaries in the `memories` container; test **GSIs** for a real cross-partition dashboard query and measure RU savings; try **integrated embeddings** with Microsoft Foundry to remove a synchronous OpenAI call.
- [ ] Questions: What are the production **default cadences** for extraction/summarization (vs the demo's every-5-turns)? How are **multi-writer conflicts** resolved by default (LWW vs custom) and how does that interact with the memory `superseded by` model? What's the **pricing/RU overhead** of the Agent Memory Toolkit background runtime and GSI sync? Is **integrated embeddings** GA or preview, and which Foundry embedding models are supported? How does **per-partition automatic failover** interact with **distributed transactions** mid-flight?
- [ ] Relevant to: Any multi-agent app needing durable, personalized memory; Azure reliability/DR design (RPO/RTO, five-nines); cost optimization on Cosmos DB (RU economics, GSIs); replacing hand-rolled RAG with agentic memory; lab work in [[labs.db]] / Azure deployments.

## 🔗 Related
- [[Azure Cosmos DB]]
- [[Multi-agent AI applications]]
- [[Agentic memory vs RAG]]
- [[MCP (Model Context Protocol)]]
- [[LangChain & LangGraph]]
- [[Azure reliability & availability (RPO RTO SLO)]]
- [[Microsoft Foundry]]
- [[Microsoft Build 2026]]
- Source list: [[2026 Build Session List]]

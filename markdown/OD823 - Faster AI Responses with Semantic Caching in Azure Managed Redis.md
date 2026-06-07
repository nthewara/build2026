---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/redis
  - topic/semantic-cache
  - topic/ai
  - topic/azure
  - topic/agent-memory
  - topic/vector-search
source: https://www.youtube.com/watch?v=QQXnwN302n8
session_code: OD823
event: Microsoft Build 2026
speakers: Shruti (PM, Azure Managed Redis); Philip Blasimann (Senior Solutions Architect, Redis); Roy (Solution Architect, Redis — EMEA)
duration_min: 31
aliases:
  - Faster AI Responses with Semantic Caching in Azure Managed Redis
---

# OD823 — Faster AI Responses with Semantic Caching in Azure Managed Redis

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Shruti (Product Manager, Azure Managed Redis) · Philip Blasimann (Senior Solutions Architect, Redis — Azure Managed Redis specialist) · Roy (Solution Architect, Redis — covering EMEA, based in the Netherlands)  
> **Duration:** ~31 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=QQXnwN302n8)

## 🎯 TL;DR
Azure Managed Redis (AMR) is positioned as the "new age" first-party Redis on Azure — fully managed, built on Redis Enterprise, up to **15× more performant** than Azure Cache for Redis with a more cost-effective TCO, zone-redundant and 4-nines by default (5-nines with geo-replication). Beyond classic caching/session/leaderboard workloads, AMR's "secret sauce" is the **Redis Search module** (free to enable), which adds vector similarity search over embeddings and unlocks two flagship AI use cases. The first is **semantic caching**: instead of exact key-value matching, prompts are embedded and compared by cosine similarity against a tunable threshold, so semantically-equivalent questions hit the cache — saving tokens, slashing latency to near-zero, and adding response consistency. The second is **agent memory**: AMR stores both short-term (conversation/state) and long-term (durable facts, preferences, interests) memory as vector hashes, retrievable via semantic search and natively integrated with the Microsoft Agent Framework. Demos showed live cache-hit behavior, threshold tuning, per-user vs. global caches for data-leakage control, a cost calculator (≈$200K+/yr saved at 70% hit rate), and an AI that learns and recalls facts about a user.

## 🔑 Key Takeaways
- **Azure Managed Redis (AMR)** is a fully managed, first-party in-memory data store on Azure built on **Redis Enterprise** software — distinct from (and successor to) the older Azure Cache for Redis.
- AMR is claimed **up to 15× more performant** than Azure Cache for Redis (the speaker corrected herself from "15%" to "15 times") with a more cost-effective TCO.
- **Reliability defaults:** zone-redundant by default, **four-nines (99.99%) SLA** by default; **five-nines** achievable with a geo-replicated (active-active) setup.
- The **Redis Search module** is AMR's "secret sauce" — configurable at **no extra cost** — and provides **vector similarity search** over embeddings stored in Redis. This single capability powers both cost-savings (semantic caching) and memory/context scenarios.
- **Exact key-value caching is a poor fit for LLMs:** two prompts can be worded differently but share the same intent/meaning. Semantic caching solves this by comparing meaning via embeddings, not literal string match.
- **Semantic cache flow:** prompt arrives → (optional exact/hash lookup) → generate embedding → vector similarity search → if cosine similarity ≥ your threshold, it's a cache hit and the stored response is returned with **zero new tokens generated**; otherwise call the LLM and store the new result.
- **Three benefits of semantic caching:** (1) **token savings** (no LLM call on a hit), (2) **response time** (in-memory Redis returns hits in ~milliseconds vs seconds/minutes for long-running agents), (3) **consistency/determinism** (same intent reliably returns the same vetted answer).
- **The similarity threshold is a tuning knob** you set in your app/client: lower (e.g. 50%) = more hits but looser matches; higher (75%, 90%) = stricter, fewer hits. A 100% "prompt-hash hit" is the exact key-value match that always fires.
- **Data-leakage control via key design:** use **per-user key naming conventions** so a user only gets cache hits on their own data; use a **global cache** for shared content like an FAQ bot where every user benefits from the same answers.
- **Cost impact is dramatic and scalable:** the demo's break-even is a **~1.2% cache-hit rate** — only ~1 in 100 queries needs to be a hit to start saving money net of embedding + Redis costs. At 200K daily queries / 70% hit rate / GPT-5 pricing, savings were **~$200K+ per year**.
- **Agent memory has two tiers:** **short-term** (conversation history, state) and **long-term** (durable facts, preferences, behavior, interests for personalization) — both stored in AMR as vector hashes and retrieved by semantic search.
- **Memory is curated, not dumped:** the agent is given decision criteria/instructions to judge each message — permanent fact vs temporary, about the user vs about the world, "would this help personalize future conversations?" — and only durable facts are saved (e.g. "I'm a software engineer" is saved; "I'm feeling tired today" is skipped).
- **TTLs govern retention:** in the demo, short-term memory kept ~30 days, long-term memory kept **over a year** so a returning user (away for months) is still recognized.
- **Native integration:** AMR's agent-memory capability is **natively embedded/supported by the Microsoft Agent Framework**; embeddings in the memory demo used Azure OpenAI's **text-embedding-3-small** model.

## 📚 Detailed Notes

### Framing: Redis has outgrown its classic use cases
Shruti (PM for Azure Managed Redis) opens by noting most people already know Redis from traditional roles — session store, leaderboards, reducing database cost, making databases more performant. But as "internet scale" has grown, Redis use cases have expanded well beyond the basics to include **time series, vector search, JSON data, and semantic caching**. The talk's thesis: Redis — specifically **Azure Managed Redis** — is the "new age" Redis for building AI apps at internet scale.

### What Azure Managed Redis (AMR) is
- A **fully managed in-memory data store on Azure**, a **first-party offering**.
- Built on **Redis Enterprise** software, giving a **more cost-effective TCO** than Azure Cache for Redis and significantly better performance.
- **Performance:** up to **15× more performant** than Azure Cache for Redis (explicitly corrected live from "15%" to "15 times").
- **Availability:** **zone-redundant by default**, **four-nines (99.99%)** by default; configure **geo-replication** to reach **five-nines** availability SLA.
- **Workloads:** all the classic acceleration scenarios — distributed cache, session management, leaderboards, pub/sub, etc. — **plus** powering **RAG scenarios** and acting as a **lightweight vector data store**.

### The state of AI agents today (the problem space)
Shruti gives a simple agent anatomy: an **input/trigger/event** kicks off the agent; internally an agent is **instructions + a model + many tool calls** that enrich what it can do; it then produces a useful **output**. To be effective, the tool calls need three things:
1. **Domain-specific knowledge** (specific to your business),
2. **Actions** it can execute to be impactful,
3. **Memory.**

**Market context:** Gartner is cited predicting **40% of enterprise applications will have task-specific AI agents by 2026** (up sharply from 2025), and growing further.

**Production challenges that emerge:**
- **Keeping pace with AI innovation** — the rate of change (especially in vector search) is hard to track and adopt for production.
- **Unpredictable cost** — tokens are new territory; the token-to-dollar relationship surprises people at month-end billing. Model calls are **expensive and slow**.
- **Agents need context and memory** to be impactful.

Solving these unlocks **enterprise-ready, internet-scale AI agents**. The session focuses on **two** of them: **cost management** and **context/memory**.

### The "secret sauce": Redis Search module + vector similarity search
The enabler for both AI use cases is the **Redis Search module**, configurable on AMR **at no extra cost**. Once enabled, AMR can perform **vector similarity search on embeddings stored inside Redis**. This single capability powers both the cost-savings story (semantic caching) and the memory/context story (agent memory). Shruti then hands off — Phil covers semantic caching, Roy covers agent memory.

### Semantic caching — from exact-match to meaning-match (Phil)
Phil Blasimann (Senior Solutions Architect at Redis, AMR specialist) frames caching as Redis's founding, "bread and butter" use case of the last ~10 years. **Classic cache pattern:** sit Redis in front of the database to offload repetitive cost and pressure and improve performance — check the cache for an existing key; if present, serve it; if not, call the database and load the result back into Redis. It's a best-practice first optimization for databases.

**Why LLMs break exact-match caching:** with generative AI (especially the last 2–3 years), **exact key-value match caching is not ideal for LLMs**. Two users can ask the *same underlying intent* with *slightly different wording*. Under exact-match, the second query misses and you pay to generate a **full set of (expensive) tokens** again even though you could have reused the prior answer.

**Semantic caching pattern:** the shape stays the same — check Redis for a hit — but:
- Instead of calling a *database* on a miss, you call an **LLM**.
- You **store vector embeddings** in the Redis instance.
- As prompts come in, you embed them and run **vector similarity search**, comparing similarity against a **threshold you set**; clearing the threshold = a cache hit.

**Three reasons semantic caching matters:**
1. **Token savings** — a hit returns the stored answer with **no token generation**; token cost is "exploding" in the news daily.
2. **Response time** — agents run longer/smarter, leading to seconds or even minutes of wait; an in-memory Redis hit returns near-instantly.
3. **Consistency** — sometimes you *don't* want LLM non-determinism; for the same intent you want confidence you're serving the same intended answer.

### Demo 1 — Semantic caching, live (Phil)
**Setup/orientation:** A split UI. **Left = a plain LLM** (think Copilot/ChatGPT/Claude). **Right = the same idea but with semantic caching under the hood, powered by a live Azure Managed Redis instance.** Metrics (tokens, timing) are captured for every prompt.

- **Prompt 1** (Contoso e-commerce persona): *"How do I improve product search relevance using vector embeddings?"* Both sides behave as normal LLMs and return **similar-but-different** answers (illustrating non-determinism): **left 118 tokens, right 131 tokens**, both ~**1–2 seconds**.
- **Prompt 2 (rephrased, same intent):** *"How can vector embeddings make product search more relevant?"* On the **right**, this triggers a **semantic cache hit**: it returns **extremely fast** and is the **exact same response** as before, with **zero tokens generated** (reusing the prior answer). On the **left** (plain LLM), it just makes a new call and generates **~126 tokens**.
- **Under-the-hood steps** (shown by clicking a query — all happening in ~a millisecond): (1) **check the cache** — first attempt an **exact/hash cache lookup** (serve like a normal data cache if a key-value pair exists); (2) since none existed, **generate embeddings**; (3) get embeddings back and run **vector similarity search**; (4) **cosine similarity** cleared the threshold → **cache hit** → fast result, no tokens.
- **Performance reassurance:** because Redis is **in-memory** it's "lightning fast" — even though all this runs on **every** request, users aren't left waiting; firing more queries shows no perceptible overhead.

### Demo 1b — Tuning the similarity threshold (Phil)
Using a base prompt — *"What's the most cost-effective caching strategy for serving personalized product recommendations to 10 million daily active users?"* — plus several variations (some very similar, some unrelated), Phil runs a **cosine vector similarity** test and sweeps the **similarity threshold** (the value you'd set in your app/client):
- **50% threshold:** the **top four** prompts qualify as semantic cache hits.
- **75% threshold:** "variation four" drops out — no longer similar enough.
- **90% threshold:** **every** variation misses (super strict).
- **Prompt-hash hit:** the exact key-value pair **matches 100% of the time** regardless of threshold (it's an exact match, not a semantic one).

Takeaway: the threshold gives you **per-scenario flexibility** over how strict matching should be.

### Demo 1c — Data-leakage control: per-user vs global caches (Phil)
Concern: if two users ask similar questions but one has **user-specific data**, how do you avoid leaking it via a shared cache hit?
- **Per-user cache:** Two personas — **Merchandiser Mia** (left) and **Platform Priya** (right). Asking *"What's my job?"* yields a semantic cache hit **strictly on the keys saved for that user**. This is achieved by the **key naming convention in Redis** — structure keys per user/domain so the search engine queries only that user's scope. Result: **no chance of leakage** between users.
- **Global cache:** Some cases *want* a shared cache — e.g. an **FAQ bot** where the user's identity doesn't matter and everyone asks similar things. Demo: a Contoso public FAQ bot for unauthenticated users; *"What are your hours?"* gets a cache hit because it's similar enough to a prior question. A later visitor (e.g. 5 minutes on) "wouldn't know any different," and in such public instances **almost every response can be a semantic cache hit** with **no tokens spent** — using real company data.

Takeaway: AMR supports **either global or per-user** caching depending on the use case.

### Demo 1d — Cost at scale (Phil)
A calculator for an enterprise scenario:
- Inputs: **200,000 daily queries**, **70% semantic cache-hit rate**, a deliberately **low token budget**, **GPT-5 pricing**.
- Baseline annual token spend: **~$300,000/year**.
- **Savings rule of thumb:** your **net savings ≈ your cache-hit rate**. At 70% hit rate → **~70% savings**, i.e. annual spend drops to **~$90K (just under $100K)**.
- This **factors in both** the **embedding costs** per query and the **Redis instance** needed to power the load — and still **saves over $200,000/year**.
- **Break-even rate:** at a **~1.2% cache-hit rate**, you only need **~1 in 100 queries** to be a semantic cache hit for the setup to net-save money after that first query. Conclusion: highly **scalable**, "set it and leave it," strong performance + token-spend wins.

### Agent memory with AMR (Roy)
Roy (Solution Architect for AMR covering EMEA, based in the Netherlands) shifts to **agent memory** — using AMR so agents in an **agentic workflow** (multiple agents collaborating on high-fulfilling tasks) can leverage memory and act even better.

**Two memory tiers:**
- **Short-term memory:** the interaction/conversation, certain **state**, etc.
- **Long-term memory:** **personalization** — durable facts, preferences, behavior, and a user's interests, so the system "knows" the user.

**Why AMR shines here:** agents get **rapidly fast access** to this data and fold it into their tool use / LLM reasoning. Critically, when **agents collaborate**, one agent can pass context to another simply because it's **stored in AMR** — "Hey, have a look at this" — and the next agent grabs that information instantly, improving the overall workflow and user experience.

### Demo 2 — Personalization memory, live (Roy)
Same Contoso context as Phil's demo, split UI: **left = without memory**, **right = with memory**. The right side stores conversations and durable facts (work, preferences, interests).
- Roy teaches the AI: *"I'm a software engineer working on machine learning projects and I love hiking, photography on the weekends."*
  - **Left:** responds politely ("nice to meet you") but **saves nothing** — neither conversation nor long-term memory.
  - **Right:** **analyzes the message**, responds, and **remembers durable facts** (user is a software engineer; loves hiking; loves photography). The **agent activity log** shows the steps: analyze → reason about the message → save the chosen facts to long-term memory.
- Because facts are stored in a **vector database as a hash vector**, Roy uses **semantic search** to query them: *"What do you know about my work?"* → it recalls the ML/work facts and stack; *"What activities do I enjoy?"* → it recalls hiking/photography. The **left side has no clue**; the **right side knows him**.

**TTLs in this demo:**
- **Short-term memory:** kept **30 days** — every conversation saved for 30 days.
- **Long-term memory:** kept **over a year** — so a user who goes away for ~2 months is still recognized on return.

### Demo 2 — How it works under the hood (Roy)
Pipeline for a message like *"What are my hobbies?"*:
1. **Generate a query embedding** using Azure OpenAI's **text-embedding-3-small** model.
2. **Vector search** around that embedding.
3. **Build context** from retrieved memory.
4. **Use AI to generate a response.**
5. **Persist:** any new facts saved as **vectors (factor/vector hashes)**; **conversation history updated**. Everything works together as a distinct flow.

**Curating long-term memory (the key design idea):** you **don't save everything**. The AI/agents are given a **set of instructions / decision criteria** and analyze every message:
- Is this a **permanent** fact or **temporary**? (e.g. *"I'm feeling tired today"* → temporary → **not saved**; could feel fine tomorrow.)
- Would it **help personalize future conversations**?
- Is the fact **about the user** (not about the world)?
- A **special tag** marks facts to save; the decision criteria then **save or skip** accordingly.

Example: *"I'm a software developer at Microsoft and I love playing tennis on the weekends"* → the system **identifies multiple facts** and **stores each** in the vector database, creating embeddings (via the embeddings model) and storing them as **vector/"factor" hashes** per fact type.

### Demo 2 — Storage view & multi-agent sharing (Roy)
From an **AMR storage perspective**:
- **Short-term memory:** entries for different users (e.g. "Phil," "me and Thomas" talking to the AI), each with a visible **TTL**; opening one reveals the **full conversation**.
- **Fact store:** all stored facts visible — tagged **interest / personal / work**.

This lets **multiple agents** access durable or short-term information **rapidly and in common** — so a whole agentic workflow shares the same knowledge, boosting performance and the customer experience. **Illustrative use case — a travel companion app:** it already knows "I like Airbnbs and early flights," so the user never re-specifies preferences each session; booking is faster and feels personalized.

### Integration & wrap-up
- AMR's **agent-memory capability fully integrates with the Microsoft Agent Framework** — natively embedded and supported.
- Closing recap (Roy): the session covered **semantic caching, semantic search, agent memory, and Azure Managed Redis as the foundation** for all of them. Thanks to Phil and Shruti.
- **Resources:** the team points to useful resources and **sample demos on GitHub**, and invites questions/feedback by email.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Managed Redis (AMR)** — fully managed, first-party in-memory data store on Azure, built on Redis Enterprise; the foundation for every scenario in the talk.
- **Redis Enterprise** — the software AMR is based on; source of its performance and TCO advantages.
- **Azure Cache for Redis** — the prior/legacy Azure Redis offering; AMR is positioned as up to 15× more performant with better TCO.
- **Redis Search module** — the "secret sauce"; enables **vector similarity search** over embeddings stored in Redis, configurable at no extra cost. Powers both semantic caching and agent memory.
- **Vector similarity search / cosine similarity** — the matching mechanism behind semantic cache hits and memory retrieval; compared against a tunable threshold.
- **Semantic caching** — embedding-based caching that returns stored answers for semantically-equivalent prompts, saving tokens and latency.
- **Agent memory (short-term & long-term)** — conversation/state vs durable facts/preferences/interests, stored in AMR as vector hashes.
- **Azure OpenAI — text-embedding-3-small** — embedding model used in the memory demo to vectorize messages/facts.
- **GPT-5** — the chat model whose pricing was used in the cost calculator.
- **Microsoft Agent Framework** — natively integrates/supports AMR's agent-memory capability.
- **RAG (Retrieval-Augmented Generation)** — AMR can power RAG scenarios and act as a lightweight vector store.
- **TTL (time-to-live)** — used to expire short-term (~30 days) and long-term (>1 year) memory.
- **Redis classic use cases** — distributed cache, session management, leaderboards, pub/sub, time series, JSON data.
- **GitHub** — hosts the sample demos referenced at the end.
- **Contoso** — fictional e-commerce company used across the demos (personas: Merchandiser Mia, Platform Priya; an FAQ bot).

## 🚀 Announcements / What's New
None explicitly announced. The session is an overview + demo of existing Azure Managed Redis capabilities (semantic caching, vector similarity search via the Redis Search module, and agent memory with Microsoft Agent Framework integration) rather than a launch/preview/GA reveal. No preview or GA dates were stated.

## 💡 Demos
- **Demo 1 — Semantic caching (live, Phil):** Split UI (plain LLM on left vs LLM + semantic cache on right, backed by a live AMR instance). Showed a rephrased-but-same-intent prompt triggering a **semantic cache hit** on the right — identical response, returned near-instantly, **0 tokens** — while the left LLM made a fresh ~126-token call. **Proved:** semantic equivalence (not exact string match) can be reused, saving tokens and time.
- **Demo 1a — Under-the-hood trace (Phil):** Clicked into a query to reveal the pipeline (exact/hash lookup → generate embeddings → vector similarity search → cosine similarity clears threshold → cache hit), all in ~a millisecond. **Proved:** the matching logic and why hits are effectively free and instant.
- **Demo 1b — Threshold tuning (Phil):** Swept the cosine similarity threshold (50% → top-4 prompts hit; 75% → one variation drops out; 90% → all miss; the exact prompt-hash always matches 100%). **Proved:** you control match strictness per scenario via a single threshold value.
- **Demo 1c — Per-user vs global cache (Phil):** Personas Merchandiser Mia & Platform Priya each got cache hits only on their own keys (per-user naming convention → no data leakage); a Contoso FAQ bot showed a global cache where unauthenticated users share hits. **Proved:** AMR supports both isolation and sharing depending on use case.
- **Demo 1d — Cost calculator (Phil):** 200K daily queries, 70% hit rate, GPT-5 pricing → ~$300K/yr baseline cut to ~$90K (incl. embedding + Redis costs), saving **$200K+/yr**; break-even at ~1.2% hit rate. **Proved:** the economics are compelling even at very low hit rates.
- **Demo 2 — Personalization memory (live, Roy):** Split UI (without vs with memory). Taught the AI facts about himself; only the right side analyzed, saved durable facts, and later recalled his work and hobbies via semantic search. Showed the agent activity log, TTLs (short-term 30 days, long-term >1 year), the embedding pipeline (text-embedding-3-small), and the curation logic (permanent vs temporary, about-user vs about-world). **Proved:** AMR delivers selective, durable, retrievable agent memory for real personalization.
- **Demo 2a — AMR storage view (Roy):** Inspected stored short-term conversations (per user, with TTLs) and tagged facts (interest/personal/work), illustrating how multiple collaborating agents share the same memory rapidly. **Proved:** the storage model and multi-agent context-sharing benefit.

## 📊 Notable Stats / Quotes
- **Up to 15× more performant** than Azure Cache for Redis (corrected live from "15%" → "15 times").
- **Four-nines (99.99%)** availability by default; **five-nines** with geo-replication; **zone-redundant by default**.
- **Gartner: 40% of enterprise applications will have task-specific AI agents by 2026** (up from 2025).
- **Redis Search module: configurable at no extra cost.**
- Demo 1 token/timing: prompt 1 = **118 tokens (left) / 131 tokens (right)**, both **~1–2 seconds**; rephrased prompt = **~126 tokens** on the plain LLM vs **0 tokens** on the semantic-cache hit.
- Threshold sweep: **50% → top 4 hits**, **75% → variation 4 drops**, **90% → all miss**; exact prompt-hash = **100% match**.
- Cost calculator: **200,000 daily queries**, **70% hit rate**, **GPT-5 pricing** → **~$300K/yr** baseline → **~$90K/yr** after caching → **>$200K/yr saved**; **break-even ≈ 1.2% hit rate** (~1 in 100 queries).
- Memory TTLs: **short-term ~30 days**, **long-term >1 year**.
- Embedding model in memory demo: **Azure OpenAI text-embedding-3-small**.
- *"Whatever your cache hit rate percentage is, that is your net savings."* — Phil, on the savings rule of thumb.
- *"If you think about a travel companion type of application... it already knows this and it gives me a way better experience."* — Roy, on personalization via long-term memory.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Spin up an **Azure Managed Redis** instance and enable the **Redis Search module**; build a minimal semantic-cache wrapper (embed prompt → vector similarity search → threshold gate → store/serve).
  - Experiment with the **similarity threshold** on real prompts to find the sweet spot between hit rate and false positives for a given app.
  - Implement **per-user key naming** to validate the no-leakage pattern, and a separate **global FAQ cache** to compare hit rates.
  - Build an **agent-memory** prototype with short-term (conversation) + long-term (curated facts) tiers, TTLs, and `text-embedding-3-small`, then wire it into the **Microsoft Agent Framework**.
  - Find and clone the team's **GitHub demo samples** referenced at the end of the talk.
- [ ] Questions:
  - What exact pricing/SKU sizing makes the cost-calculator numbers hold (which AMR tier powers 200K daily queries)? 
  - How is the **break-even 1.2%** derived — what embedding + Redis cost assumptions underlie it?
  - What's the recommended **eviction/consistency** strategy when cached answers go stale (e.g. FAQ data changes)?
  - How does AMR's agent-memory module compare to other memory stores integrated with Microsoft Agent Framework?
  - Is there guidance on **embedding-model choice** (dimensions/cost) vs cache-hit quality?
- [ ] Relevant to:
  - Any LLM/RAG app where **token cost or latency** is a concern — semantic caching is a quick win.
  - **Agentic systems** needing shared, durable, personalized memory across collaborating agents.
  - Azure architecture decisions weighing **AMR vs Azure Cache for Redis** for AI workloads.
  - Cost-optimization reviews for production GenAI workloads.

## 🔗 Related
- [[Azure Managed Redis]]
- [[Semantic Caching]]
- [[Vector Similarity Search]]
- [[Agent Memory]]
- [[Microsoft Agent Framework]]
- [[Azure OpenAI Embeddings]]
- [[RAG - Retrieval Augmented Generation]]
- Source list: [[2026 Build Session List]]

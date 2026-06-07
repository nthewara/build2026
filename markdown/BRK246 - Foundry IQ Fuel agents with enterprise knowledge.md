---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/foundry
  - topic/rag
  - topic/agentic-retrieval
  - topic/azure-ai-search
  - topic/ai
source: https://www.youtube.com/watch?v=FRptM_WiBRg
session_code: BRK246
event: Microsoft Build 2026
speakers: Pablo Castro (Microsoft — leads the AI Knowledge team, CoreAI division)
duration_min: 45
aliases:
  - Foundry IQ Fuel agents with enterprise knowledge
---

# BRK246 — Foundry IQ: Fuel agents with enterprise knowledge and agentic retrieval

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Pablo Castro — leads the AI Knowledge team in the CoreAI division at Microsoft (Foundry IQ, Azure AI Search, Azure Content Understanding)  
> **Duration:** ~45 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=FRptM_WiBRg)

## 🎯 TL;DR
Foundry IQ is Microsoft's managed knowledge layer for connecting agents and AI models to the data they need to do real work — your application data, your Microsoft 365 content, your analytics, and the live web. The session walks the full lifecycle (provision → create a knowledge base → add knowledge sources → retrieve) and shows how the system is intentionally **layered** so you can start with a drag-and-drop "chat with my files" experience and grow into a sophisticated, multi-source, security-aware agentic retrieval pipeline without re-platforming. The headline announcement is the **public preview of serverless Foundry IQ** (scales to zero, ~10–20s to create, pay only for storage when idle), alongside a **second-generation agentic retrieval engine** that delivers better answers with fewer tokens. Every knowledge base is automatically an **MCP server**, and the whole stack enforces document-level security (Entra ACLs + Microsoft Purview sensitivity labels) at the bottom of the stack so you never have to bolt on your own.

## 🔑 Key Takeaways
- **Foundry IQ = the thing you use to connect agents to knowledge.** It's the grounding/retrieval layer between your agents/models and your enterprise data.
- Three design goals drive everything: (1) **easy to get started**, (2) **versatility** as needs grow, (3) **top quality** across every AI-powered component (ranking, relevance, content understanding).
- The system is a **clean, non-hiding stack of three layers**: Foundry integration layer → knowledge-retrieval (agentic) layer → core retrieval engine (Azure AI Search). You pick the layer you need and can move **up and down** the stack freely — you're never locked in.
- **Every knowledge base is automatically an MCP server** — append `/mcp` to the knowledge-base API endpoint and you have an MCP server with no extra setup. It's also callable as a plain REST API.
- **NEW: Serverless Foundry IQ (public preview)** — no friction to start, ~10–20s to create, **scales to zero**, costs nothing until used, you only pay for index storage when idle. Production-ready, same state-of-the-art stack as dedicated.
- **Serverless vs dedicated is now a real choice:** serverless for usage-based/dynamic/dev/unit-test/agent-created workloads and many small-to-medium indexes; **dedicated** for steady, highly predictable, isolated workloads (and optional **confidential computing** top to bottom).
- A **knowledge base** is the *scope/domain of knowledge + the policy for using it* (retrieval effort, steering instructions, answer synthesis on/off) — deliberately hidden from the agent to separate concerns. Underneath it sit one or more **knowledge sources**.
- Knowledge sources span a **spectrum**: loose files → file knowledge source (indexed) → object stores (Blob, OneLake, databases) → **Microsoft IQ surfaces (Work IQ / Fabric IQ / Web IQ)** → any app via **MCP**. You don't rebuild the plumbing for each.
- For indexed sources Foundry IQ runs a **full ingestion pipeline by default** (content extraction, chunking, vectorization, image handling) — assembled automatically, but **every step is customizable** with your own injected steps.
- **Azure Content Understanding is integrated** for high-end extraction: OCR, document layout, correct reading order, hard tables (spanning pages, sparse, handwritten), checkbox extraction, and **schema-driven** structured extraction.
- **Ingestion is continuous, not one-shot:** connectors track source changes and **incrementally** feed updates into the index, so your grounding index is always fresh.
- **Second-generation agentic retrieval:** query planning → source selection → query decomposition → parallel search → reflect/iterate (per configured retrieval effort) → final result. Revamped to exploit newer models' improved tool-calling loops.
- **Quality + efficiency wins:** material improvements across recall, answer correctness, completeness, and "knows when it doesn't know" vs BM25, hybrid, and minimal mode — and a **better Pareto frontier (better answers with fewer tokens)** via batched queries, a new semantic ranker, improved answer synthesis, model-specific MCP-parameter-binding prompts, and prefix/token-cache-aware prompt construction.
- **Security is enforced at the bottom of the stack:** Entra-integrated ACL propagation (SharePoint, Blob w/ hierarchical namespaces) and **Microsoft Purview** sensitivity-label support (decode → index → re-secure → propagate labels to your UI). Pass the user's delegated token at query time; results look like only what that user can see.
- **Speed changes how you think about retrieval:** raw search indexes are effectively instantaneous (a 22M-chunk full-English-Wikipedia index searches faster than you can type), so an agent can fire 10–20+ parallel searches per round; agentic retrieval trades a few seconds (up to ~10s on hard, multi-iteration queries) of latency for much higher answer quality.
- **Everything shown is available today** — via Foundry, the Azure portal, or the SDKs.

## 📚 Detailed Notes

### What Foundry IQ is and why it exists
Agents and AI models are only as useful as the knowledge they can reach. The Foundry model powering an agent has a knowledge cutoff and no access to your proprietary data on its own. **Foundry IQ is the component you use to connect agents to the knowledge that ties them to your applications, your company, and the data they need to get their job done.** Pablo frames the whole talk around three goals the team optimizes for:
1. **Easy to get started** — getting a working knowledge base should be a "piece of cake."
2. **Versatility** — as your application gets sophisticated, your needs grow, or the problem gets hard, you should find what you need **in the same platform** without switching tools.
3. **Top quality** — like any AI-based system, quality must hold across every AI-powered component. For retrieval specifically that means **great ranking, great relevance, great content understanding**.

### The "easy to get started" path (drag-and-drop files → working agent)
The opening demo proves goal #1. In Foundry: go to **Build → a Foundry project → Knowledge**, which is where you manage all your knowledge bases. Create a new knowledge base, choose the easy case ("my data is just in files"), **drag and drop** a handful of files (Pablo used Wikipedia movie articles → named it *movies wiki*), give it a **name and a description so agents know what it's for** ("full articles about movies"), and **Save**. The knowledge base lives inside a Foundry IQ instance he'd already created (named `demo3`).

Crucially, **out of the box every knowledge base is an MCP server** — you don't stand anything up or run anything. To consume it he used **GitHub Copilot as the agent** (rather than write a new one): add a new MCP server in Copilot, point it at the knowledge base endpoint. The endpoint shape is:
`https://<service>.search.windows.net/knowledgeBases/<knowledge-base-name>` (backed by **Azure AI Search**), and **appending `/mcp`** to that turns the same API entry point into an MCP server. APIs are versioned (he used the brand-new API version shipped that day). Once connected, asking *"which pill did Neo take?"* causes Copilot to ground on the MCP knowledge base, send a few sub-queries, retrieve grounding, and answer **"Neo took the red pill"** (from *The Matrix*). The point: **zero to a working, agent-consumable knowledge base in about a minute**, via MCP or API.

### The layered architecture (the core mental model)
Foundry IQ is built as a **comprehensive, layered system that does not hide options** — you choose which layer to use:
- **Top — Foundry integration layer.** The fast, productive surface you just saw for building new agents.
- **Middle — complete knowledge-retrieval system.** Uses **agentic retrieval when needed**: iterative query planning, handling multiple sources, choosing **when to query what**, connecting to the entire Microsoft IQ surface, with **APIs you can call directly**.
- **Foundation — core retrieval engine.** State-of-the-art Azure AI Search: **vector retrieval, lexical search, hybrid (the two combined), state-of-the-art ranking models** — everything for best-quality ranking without rebuilding from scratch, under enterprise-grade security, quality, and scale.

A non-trivial design achievement: even after you pick a layer, **you're not stuck in it** — you can go up and down the stack as needs change, or change your mind after building.

### The four-stage lifecycle
Using Foundry IQ in detail follows four stages, each of which the session improves:
1. **Provision** a Foundry IQ instance.
2. **Create a knowledge base.**
3. **Add knowledge sources.**
4. **Retrieve.**

### Stage 1 — Provisioning: dedicated vs the NEW serverless
Historically Foundry IQ / Azure AI Search required **dedicated capacity** — great for **steady workloads**: predictable, isolated to your environment, full control over competing workloads — but you must **know your capacity up front**.

**Announcement — public preview of serverless Foundry IQ.** With serverless: **no friction to start, ~10–20s to create a service, costs nothing until you actually use it, scales to zero when idle, and you only pay for the storage your indexes use.** It's **production-ready** (dev workloads *and* very dynamic workloads — e.g., agents creating services, or apps creating/deleting services on the fly). Same state-of-the-art tech as the existing stack: **state-of-the-art ranking, an instant RAG stack, a rock-solid foundation — plus serverless dynamics.**

**Choosing between them:**
- **Serverless** → usage-based plan; lots of medium/small indexes; the developer workflow; unit tests that create/delete on the spot; **agents that create their own services/indexes** autonomously.
- **Dedicated** → highly predictable plan; **isolated capacity**; option to run on **confidential computing** stacks top to bottom.

Provisioning serverless was shown two ways: **(a)** by telling a Copilot agent to "create a new Foundry IQ service, create an index, and load the first ~100 rows from this IMDb file" (it picked a name, created a *serverless* service + an index, and loaded 100 documents on its own); and **(b)** in Foundry UI: create new resource → name + resource group → pick a **serverless-supporting region** (e.g., West Central US) → choose **serverless** as the SKU → Create (10–20s). The same option appears in the **Azure portal**.

### Stage 2 — Knowledge bases (scope + policy, not access)
Think of a **knowledge base** as the **scope of knowledge and the policy for using it** — *not* how it's accessed — and it's **hidden from the agent** to separate concerns. It defines the **domain of knowledge** and the **usage policy**, e.g.:
- **Retrieval effort** — quick single pass vs iterative retrieval.
- **Steering instructions** — influence how the model behaves.
- **Answer synthesis** — whether Foundry IQ composes a natural-language answer (with citations) or returns raw passages.
- The **orchestration model** — when a knowledge base has multiple/online sources you must specify the model used for orchestration (he used **GPT-4.x mini**, with a default reasoning effort you can override, optional answer synthesis, and optional steering instructions for each).

Underneath the agentic retrieval stack sit the **knowledge sources**. For most, you point Foundry IQ at where the knowledge lives and it **builds vector + lexical indexes**; some sources are **federated** (accessed online at runtime). Regardless of representation, **at runtime the system chooses which sources to use** for a given scenario and queries them.

### Stage 3 — Knowledge sources (the data spectrum)
Real-world data is everywhere, so Foundry IQ offers a spectrum so you never reinvent the plumbing:

**Loose files vs the file knowledge source.** Local file access (what coding agents do well) is great for ~50–100 files / a few MB. But developers routinely have "a million PDFs in a blob account" — you can't grep your way through that if you want to fire 10–20 queries a second. The **file knowledge source** lets you upload content but puts the **full retrieval engine behind it**: pushed files run through **full content processing** (extraction, image handling, vectorization) and build indexes for fast retrieval.

**Object stores (Blob / database / OneLake-on-Fabric).** When an app manages content internally it usually lands in Blob, a database, or OneLake. Point Foundry IQ at it and it **assembles a full ingestion pipeline by default** — chunking, vectorization, etc. — for very high-quality results, while letting you **customize every step or inject custom steps** for exact control. It handles **text-heavy and multimedia** content.

**Azure Content Understanding (integrated).** First step is understanding what's actually inside files (PDFs especially) before presenting to agents. Content Understanding provides high-end **OCR, document layout, correct reading-order preservation,** and robust **table handling** (tables spanning pages, sparse tables, handwritten/partially-handwritten tables, **checkbox extraction**). It can also do **schema-driven extraction** — give it a schema of the elements you want and it isolates/extracts them to feed the agent or use as **filters**. With an embedding model it vectorizes; add a **chat-completion model** and it does **image verbalization** for media.

**Continuous, incremental ingestion.** Connecting a source (demo: a Blob container of movie annotations, using **system identity**, **standard** = full Content Understanding, an embedding model, optional chat model for image verbalization) **imports everything now and then keeps running**, tracking source changes and **incrementally** feeding them into the index — so the grounding index is **always fresh**.

### Stage 3 (cont.) — Microsoft IQ surfaces: Work IQ, Fabric IQ, Web IQ
Your data rarely lives in isolation. The **Microsoft IQ** family lets agents reach organizational knowledge, and Foundry IQ **integrates with the entire spectrum out of the box**:
- **Work IQ** — direct access to your **Microsoft 365 tenant** (Word docs, calendar, email, etc.). Integration is trivial: **point at your tenant — nothing to configure** — but the **tenant admin must consent** (it's your Office data). Once consented, it just works.
- **Fabric IQ** — your analytics estate in **Microsoft Fabric** (OneLake → structured files like Parquet + unstructured content → semantic models → Power BI reports → **data agents** and **ontologies**). Foundry IQ integrates with the **entire OneLake catalog**, so you can browse lakehouses, data agents, ontologies, etc. Fabric IQ handles **natural-language-to-SQL** and navigating multiple data sources. Demo: a simple **data agent** over Parquet movie-stats files (ratings, etc.) answered NL questions (Fabric turns them into SQL). Added as a knowledge source, it's queried **agent-to-agent** at retrieval time (a lakehouse would get indexing options; the data agent needs no indexing — questions are integrated at retrieval time).
- **Web IQ** — **announced the day before** this session — access to the live web. Added here as an **MCP knowledge source** (endpoint from the Web IQ preview + auth, choosing the **web search** tool).

Guidance: each IQ component **works fine in isolation** — if your data lives in just one place, use only that one and don't over-complicate. But it's common to mix your own app data with M365 content and analytics, and Foundry IQ makes connecting all those dots easy. In the demo a **single knowledge base** ended up combining Wikipedia articles (indexed), the **web** (via Web IQ MCP), and **Fabric data agents** — and the consuming agent doesn't need to know any of those moving parts exist; the **agentic orchestration chooses what to use when**.

### Stage 3 (cont.) — Extensibility via MCP (any app as a data source)
When the built-in options don't fit, MCP is the escape hatch. There's no "ODBC for agents," but **MCP is universal and everywhere**, and if you don't have an MCP server it's easy to make one — so it became a great integration point. Foundry IQ turns MCP output (via heuristics) into an **item-oriented list** where possible and **runs its own ranking on top to improve relevance even for MCP** results. This means **any data source** — your own app, or e.g. the **GitHub MCP server turning issues into a table** you feed the system — "just works."

### Stage 4 — Retrieval (where the value is delivered)
Retrieval is the moment all the prior work pays off: a search engine is useful the instant your **top three or four results** are what the agent needed to ground its answer. Foundry IQ includes an **agentic retrieval pipeline** you can opt into (or skip in favor of raw indexes):
1. **Query planning** — given the calling agent's question/data requirement, decide **which data sources** to consult and **how to decompose** the query.
2. **Search** — run several searches.
3. **Reflect** — examine results and decide whether it got what it hoped for.
4. **Iterate** — if not (and depending on configured **retrieval effort**), search again on the new information.
5. **Final result** — produce the result for the agent.

This is now the **second generation** of agentic retrieval. A key driver: models changed a lot from ~October last year to now (notably **tool-calling loops**), so the team **significantly revamped** the retrieval workflow to fit how today's models perform best.

### Where the quality and efficiency gains come from
Charts compare the new system against **BM25 (lexical only)**, **hybrid (vector + lexical)**, and a knowledge base with agentic retrieval off (**"minimal mode"**), across: **recall, answer correctness, answer completeness,** and **how often the model says "I don't know" even though the answer was present**. Result: **material improvements across the entire metric set.** The trade-off is **latency** — raw indexes are instantaneous (ignore them in your latency budget), whereas agentic retrieval can take **a few seconds, sometimes ~10s** if it must iterate.

Improvement sources are a mix:
- **Better language models** → the retrieval workflow was updated to fit their style (big difference).
- **A newly trained semantic ranker** (the team keeps pushing reranker quality).
- **Improved answer synthesis.**
- **Model-specific prompts for tasks like MCP parameter binding** — tuned per model because variability between models is significant.

**Token efficiency** is now first-class. Anyone can *do a search* with few tokens — the real question is *did you get it right?* A Pareto-style chart (full agentic retrieval vs hybrid + an outer orchestrating agent) shows **fewer tokens needed to produce better answers**. Prompts are also constructed to be **token-cache-aware**: managing their own context so calls **hit the prefix cache** on the target model — making it both **faster** (cache hits) and **cheaper** (cached tokens cost less than full tokens). The science team publishes detailed write-ups (a URL on screen) for those in information retrieval who want the full evaluation methodology and data.

### Putting it together — a single multi-source retrieve call
Pablo "vibe-crafted" a small client that calls the **retrieve API** against the combined knowledge base, run at **medium** effort. For a question spanning *ratings* and *box office*, the activity trace showed: the **planner** ran → went to the **Fabric data agent** (ratings live in Parquet, queried via SQL) to find top sci-fi movies → hit the **web MCP server** for box-office figures not in any dataset (discarding some content) → a **synthesis step** built the answer → the reasoning finished. The response came with **full references** per result: which **knowledge source** it came from and, where available, **links to underlying files**. You normally wouldn't show this in the UX, but it's great to **feed to an agent** to understand the interaction or for **debugging**. The punchline: **all the ranking/relevance/agentic-retrieval science sits behind one MCP-server call or one retrieve call** — everything else happens under the covers.

### Document-level security (enforced at the bottom of the stack)
Early RAG made "chat with your documents" feel novel — dump everything into an index, put a chat UI on top. But in real companies **not everyone can see every document**, and **document-level security isn't something to improvise** while building the rest. The **retrieval system must support the same security model as the underlying data.** Foundry IQ:
- **Propagates access-control info** from sources that support it (e.g., **SharePoint**, **Blob with hierarchical namespaces / ACLs**) into the indexes it builds under the covers, **integrated with Entra** (so **group membership** and the expected behaviors work).
- At **query time** you present the **user's credentials (delegated token)**; the searchable surface then **looks like it only contains the subset that user can see**. You don't layer your own security on top.
- Supports **Microsoft Purview**: documents with **sensitivity labels** are encrypted and can't be indexed by a random tool, but Foundry IQ **decodes, indexes, then re-secures** them with the original ACLs — so you control **who can see them** *and* can **propagate the sensitivity labels to your UI**, making your app "look like Office" for labeling. A **complete example** (URL on screen) shows how to assemble all these moving parts.

### Versatility — going up and down the stack
Because the stack is cleanly layered, you can start at **Foundry integration**, drop to **knowledge bases**, or go **straight to the core retrieval engine** (Azure AI Search) — and move between layers as you need, or **change your mind** after building one. Pablo demonstrated peeking under the covers of the combined knowledge base in the **Azure portal**: in the `demo3` service's **Azure AI Search blade** you can see the **knowledge base**, all its **knowledge sources**, and for the two indexed sources the actual **indexer** (the data pipeline that pulls/transforms data into the index — inspect runs, configure internals) and the **index** itself. From the index you can view the **schema** and tune low-level details, e.g. **vector-search compression** (default **8-bit quantization**, but you can choose a different quantization or reranking policy), and inspect the **actual chunked content snippets** and even the raw **vectors** used for vector-distance comparisons. This control also enables explicit **latency trade-offs**: choose **full agentic retrieval** (a few seconds, great results) or a **files-style burst of fast searches** you iterate on quickly.

### Scale and speed (why it changes your retrieval design)
To show raw speed, Pablo built a service over **all of English Wikipedia**, chunked into **~22 million chunks** — a sizable index. Searching it on **every keystroke**, he literally **could not type fast enough to out-run the search** ("I can't force the lag"). The implication: an agent can issue **10 searches, or multiple rounds of 10–20 searches each**, and they all finish **well within a second in parallel** — even at **tens or hundreds of millions of documents**. This **completely changes how you think about retrieval**: let Foundry IQ run the agentic loop for you, **or** hand the agent direct entry points and let it hit the search index **as hard as you want**.

### Wrap-up
Everything demonstrated is usable **today** — via **Foundry**, the **Azure portal**, or the **SDKs** — and the session pointed to related Build sessions on the same theme.

## 🛠️ Products / Features / Technologies Mentioned
- **Foundry IQ** — Microsoft's managed knowledge/retrieval layer that connects agents and AI models to enterprise (and web) knowledge; the central subject of the talk.
- **Serverless Foundry IQ** *(public preview, announced)* — scale-to-zero, usage-based deployment option (~10–20s to create, pay only for index storage when idle).
- **Dedicated capacity** — predictable, isolated Foundry IQ/Azure AI Search capacity; supports **confidential computing** top to bottom.
- **Azure AI Search** — the core retrieval engine under Foundry IQ (vector, lexical, hybrid search; state-of-the-art ranking; indexers; index schema control). Knowledge-base endpoints live at `*.search.windows.net`.
- **Knowledge base** — top-level resource defining the **scope of knowledge + usage policy** (retrieval effort, steering instructions, answer synthesis, orchestration model); hidden from the agent.
- **Knowledge sources** — connections under a knowledge base (files, object stores, IQ surfaces, MCP); indexed or federated.
- **File knowledge source** — upload files but with the full retrieval engine behind them (extraction, vectorization, indexing).
- **Foundry IQ MCP server** — every knowledge base is automatically an MCP server (append `/mcp` to the API endpoint); consumable by any MCP-compatible host.
- **Agentic retrieval pipeline (2nd generation)** — query planning → source selection → query decomposition → parallel search → reflect/iterate → result; configurable **retrieval effort**.
- **Minimal mode** — agentic retrieval turned off (used as a baseline in benchmarks).
- **Semantic ranker** — newly trained reranker improving relevance.
- **Answer synthesis** — optional composition of a natural-language answer with citations.
- **Azure Content Understanding** — integrated extraction: OCR, document layout, reading-order preservation, complex/handwritten/sparse tables, checkbox extraction, **schema-driven** structured extraction.
- **Image verbalization** — handling media by adding a chat-completion model to describe images for indexing.
- **Microsoft IQ** — umbrella for the enterprise-intelligence surfaces below.
- **Work IQ** — direct access to Microsoft 365 tenant content (docs, calendar, email); tenant-admin consent required.
- **Fabric IQ** — access to the Microsoft Fabric analytics estate (OneLake, semantic models, Power BI, **data agents**, ontologies) with natural-language-to-SQL.
- **Web IQ** *(announced the day before)* — live-web access; added as an MCP knowledge source (web search tool).
- **Microsoft Fabric / OneLake / data agents / Parquet** — structured analytics data and agents Foundry IQ queries agent-to-agent at retrieval time.
- **Azure Blob Storage (incl. hierarchical namespaces/ACLs)** — supported object-store knowledge source with continuous, incremental ingestion and ACL propagation.
- **Microsoft Entra** — identity backbone for ACL propagation and group-membership-aware, query-time security.
- **Microsoft Purview** — sensitivity-label support (decode → index → re-secure → propagate labels to your UI).
- **Model Context Protocol (MCP)** — universal integration point; both how knowledge bases are exposed and how arbitrary apps (e.g., the **GitHub MCP server**) become data sources.
- **GitHub Copilot** — used as the agent that consumed the knowledge-base MCP server and provisioned a serverless service from a one-line prompt.
- **MCP `mcp-o-proxy` ("odd proxy")** — proxy used to connect GitHub Copilot's MCP config to the Foundry IQ knowledge-base endpoint in the demo.
- **GPT-4.x mini** — the orchestration model chosen for the multi-source knowledge base (with selectable default reasoning effort).
- **Embedding model (e.g., text-embedding family)** — used for vectorization of source content.
- **Token / prefix caching** — prompts constructed to hit the model's prefix cache for faster, cheaper retrieval.

## 🚀 Announcements / What's New
- **Serverless Foundry IQ — public preview.** No-friction, scale-to-zero deployment: ~10–20s to create, costs nothing until used, pay only for index storage when idle. Production-ready; built on the same state-of-the-art stack as dedicated; ideal for dev/unit-test/dynamic workloads and **agents that create/delete services and indexes on the fly**. Available in serverless-supporting regions (e.g., West Central US shown).
- **Second-generation agentic retrieval engine.** Revamped to exploit newer models' tool-calling loops; delivers **material gains in recall, answer correctness, completeness, and "knows when it doesn't know,"** while using **fewer tokens** (better Pareto frontier) via batched queries, a **newly trained semantic ranker**, improved answer synthesis, model-specific MCP-parameter-binding prompts, and token/prefix-cache-aware prompting. Detailed science write-ups published (URL on screen).
- **Web IQ** — referenced as **announced the day before** this session; integrated here as an MCP knowledge source for live-web grounding.
- **General availability emphasis:** Pablo stressed *"everything I showed you today you can use today"* via Foundry, the Azure portal, or the SDKs (including the new API version used for knowledge-base/MCP endpoints).

## 💡 Demos
- **Zero-to-working knowledge base in ~1 minute.** Drag-and-drop Wikipedia *movies* articles into a new knowledge base, then consume it from **GitHub Copilot** by adding the auto-generated **MCP server** (`<service>.search.windows.net/knowledgeBases/<name>` + `/mcp`). Asking *"which pill did Neo take?"* returned **"the red pill"** grounded from *The Matrix* — proving the "easy to get started" goal and that **every KB is an MCP server with no setup**.
- **Agent self-provisioning a serverless service.** A one-line prompt to a Copilot agent ("look at this IMDb file, create a new Foundry IQ service + index, load ~100 rows") resulted in the agent **creating a serverless service, an index, and loading 100 documents** autonomously — verified in the Azure portal (serverless service `Fiq-IMDb…`, index with 100 docs). Demonstrates serverless for agent-driven workloads.
- **Serverless creation in the Foundry UI.** Create new resource → name/RG → serverless-supporting region (West Central US) → choose **serverless** SKU → Create (~10–20s) → ready for knowledge bases. Same option exists in the Azure portal.
- **Connecting a Blob knowledge source with Content Understanding.** Added a Blob container of movie annotations using **system identity** + **standard** extraction (full Content Understanding) + embedding model; ingestion runs in the **background and continuously/incrementally** tracks changes to keep the index fresh.
- **Azure Content Understanding extraction quality.** Showed a scanned PDF with a **partially handwritten table** extracted to markdown **including checkboxes**, correct **two-column layout/reading order**, extracted pictures; plus **schema-driven** extraction of specific document elements for filters/agent input.
- **Fabric data agent as a knowledge source.** A simple Fabric **data agent** over Parquet movie-stats files answered NL questions (Fabric → SQL); added to the knowledge base it's queried **agent-to-agent** at retrieval time (no indexing needed).
- **Single multi-source knowledge base.** Combined Wikipedia articles (indexed) + **Web IQ** (MCP) + **Fabric** data agent — the consuming agent is unaware of the parts; orchestration chooses sources per question.
- **Multi-source retrieve call (medium effort).** For a ratings + box-office question, the activity trace showed planner → **Fabric data agent** (ratings via SQL on Parquet) → **web MCP** (box office, some content discarded) → **synthesis** → done, returning **full references** (knowledge source + links) useful for agents/debugging.
- **Under-the-covers inspection (Azure portal).** Viewed the knowledge base, its sources, the **indexer** (data pipeline + runs), and the **index schema** — tuning **vector compression** (default **8-bit quantization**), inspecting chunked snippets and raw vectors.
- **22M-chunk Wikipedia speed test.** Searching all of English Wikipedia (~**22 million chunks**) **on every keystroke** — search kept up faster than Pablo could type, illustrating that agents can fire **many parallel searches per round** sub-second, even at hundreds of millions of documents.

## 📊 Notable Stats / Quotes
- **~10–20 seconds** to create a serverless Foundry IQ service; **scales to zero** and **costs nothing until used** (pay only for index storage when idle).
- **~22 million chunks** — all of English Wikipedia chunked into one index; searchable **faster than you can type**, on every keystroke.
- **100 documents / first ~100 rows** loaded by the self-provisioning agent demo from an IMDb file.
- **Default 8-bit quantization** for vector-search compression (customizable).
- **A few seconds, sometimes ~10s** — agentic-retrieval latency when iterating, vs **instantaneous** raw index search.
- Benchmark axes: **recall, answer correctness, answer completeness, and rate of "says it doesn't know" when the answer was present** — improved across the board vs **BM25 / hybrid / minimal mode**, while spending **fewer tokens**.
- *"Foundry IQ is the thing you use to connect agents to knowledge."*
- *"For easy scenarios we should do easy things"* — but in practice data is everywhere ("I have a million PDFs in this blob storage account — what do I do?").
- *"Life is too short to … handle things like tables that span pages, sparse tables"* — the case for Content Understanding.
- *"Security is enforced at the bottom of the stack. You don't have to layer your own on top."*
- *"Everything I showed you today you can use today."*
- *"I used to say I wrote [the code] as in I wrote the code … I don't know what to say these days"* — on vibe-coding the retrieve-API demo client.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Spin up a **serverless Foundry IQ** instance (West Central US or another supported region), drag in a few files, and consume it from an MCP host via the `/mcp` endpoint.
  - Reproduce **agent self-provisioning**: a one-line prompt that creates a serverless service + index and loads rows from a CSV/Parquet.
  - Build a **multi-source knowledge base** mixing an indexed Blob source + a **Fabric data agent** + **Web IQ**, then inspect the **retrieve activity trace + references**.
  - Test **Content Understanding** on a messy PDF (handwritten/sparse tables, multi-column) and try **schema-driven extraction** for filters.
  - Validate **document-level security** end-to-end: ACL propagation from SharePoint/Blob + Purview sensitivity-label round-trip, passing a user delegated token at query time.
  - Compare **minimal vs low vs medium** retrieval effort on a multi-hop question; measure latency vs answer quality and token spend.
- [ ] Questions:
  - Exact **GA vs preview matrix** by Search REST API version (KBs GA per blog; serverless + MCP-as-source in preview) — which features are blocked on which API version?
  - Which **regions** support serverless at launch, and the pricing detail for idle storage vs active usage?
  - How does **agent-to-agent** querying of Fabric data agents handle auth, latency, and cost at scale?
  - How configurable is the **MCP-result ranking/heuristic item extraction** for arbitrary MCP servers?
  - For confidential computing (dedicated), what's covered "top to bottom" and any quality/latency trade-offs?
- [ ] Relevant to:
  - Any enterprise RAG / agent-grounding project on Azure (replace bespoke per-project pipelines with a reusable KB).
  - Azure lab work and demos needing fast, multi-source, security-aware retrieval.
  - Related Build 2026 sessions: **BRK240** (Microsoft IQ / context-aware agents), **LAB532** (agent-ready knowledge with Foundry IQ), **DEM331** (APIs/tools/data → agent velocity).

## 🔗 Related
- [Foundry IQ blog — Build smarter agents faster with unified knowledge and serverless retrieval](https://devblogs.microsoft.com/foundry/build-smarter-agents-faster-with-foundry-iq/)
- [What is Foundry IQ? — Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq)
- Build 2026 sessions: **BRK240** (Build context-aware agents with Microsoft IQ), **LAB532** (From data to context: agent-ready knowledge with Foundry IQ), **DEM331** (Turn APIs, tools, and data into real agent velocity)
- Topics: [[Azure AI Search]] · [[RAG]] · [[Agentic retrieval]] · [[Model Context Protocol (MCP)]] · [[Microsoft Fabric]] · [[Microsoft Purview]]
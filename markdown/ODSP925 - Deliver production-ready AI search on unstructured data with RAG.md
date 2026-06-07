---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/rag
  - topic/unstructured-data
  - topic/vector-search
  - topic/ai
  - topic/dotnet
source: https://www.youtube.com/watch?v=4qjrKSe3QF8
session_code: ODSP925
event: Microsoft Build 2026
speakers: Ed Charbonneau (Progress Software)
duration_min: 14
aliases:
  - Deliver production-ready AI search on unstructured data with RAG
---

# ODSP925 — Deliver production-ready AI search on unstructured data with RAG

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Ed Charbonneau — Principal Developer Advocate, Progress Software; 10-time Microsoft MVP  
> **Duration:** ~14 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=4qjrKSe3QF8)

## 🎯 TL;DR
A vendor-led introduction to Retrieval Augmented Generation (RAG) and why it's the answer to making sense of the ~400 million TB of data the world generates *every day*. Ed Charbonneau frames RAG within the broader family of "context augmented generation" — distinguishing plain context-stuffing and cache-augmented generation from true RAG, which uses a **vector database + semantic (vector) search** to retrieve grounded, citable information into an LLM's context window. He argues that hand-built, in-house RAG stacks are complex, hard to scale, and hard to cost-predict because they glue together many vendors' pieces (UI, embedding/chat models, document parsers, evaluation) and demand software-engineering + data-science + AI expertise simultaneously. The pitch: **Progress Agentic RAG**, a RAG-as-a-Service platform that handles ingestion of structured/unstructured documents, agent-driven extraction + embedding, hybrid (keyword + semantic + graph) search reranked by an agent, and built-in quality evaluation (the "Remy" agent) — consumable via a no-code UI/widget builder or via .NET, TypeScript/JavaScript, and Python SDKs and REST APIs. A .NET + Blazor demo shows a financial dashboard ingesting SEC-filing PDFs and returning *structured* chart data through the C# SDK's `AskAsync` method.

## 🔑 Key Takeaways
- **The data problem is the whole motivation for RAG.** The world now generates/collects ~400 million TB (≈0.4 zettabytes) per day, ≈147 zettabytes/year — far beyond what humans can process unaided, so AI (LLMs) is mandatory for sense-making.
- **"Context augmented generation" is the umbrella concept.** It simply means adding data to an LLM's context window so it can answer questions about that data. Understand this first; RAG is a specialized member of this family.
- **Three flavours sit on a scale:** (1) plain **context augmentation** (drop a file/transcript into the context window — e.g. the Gemini "summarize" button on YouTube), (2) **cache augmented generation** (store more data as vectors in memory and pull pertinent pieces in — e.g. GitHub Copilot in VS Code indexing your project files), and (3) **RAG** (a dedicated vector *database* for large-volume storage + semantic retrieval).
- **Retrieval ≠ keyword search.** RAG's "retrieval" uses **vector search** for *semantic similarity* (meaning) rather than exact-keyword matching — you find content that *means* the same thing, not just content containing the same words.
- **The RAG loop:** ingest → embed → store in vector DB → vector-search on a query → retrieve relevant chunks → inject into LLM context → generate a new, grounded response → optionally emit **citations**.
- **Citations are a first-class feature, not a nicety.** They trace answers back to their source and *prove the answer is grounded in real knowledge* — "showing receipts" that the answer wasn't hallucinated.
- **Embedding models extract meaning from text** so semantic search is possible; **chunking** breaks large documents into smaller bite-size pieces that are easier to ingest, embed, and store.
- **RAG enables "generative AI search"** — letting users query huge datasets in natural language without learning query syntax, and treating unstructured sources (websites, PDFs, images, video) *as if* they were a relational database.
- **End-to-end RAG is genuinely hard to build in-house.** You need a UI, embedding + chat models, a data strategy, document providers/parsers (PDF, Office, video, images → text), and quality evaluation — typically from multiple vendors, requiring software-engineering + data-science + AI expertise. It's hard to scale and hard to predict cost.
- **The market is moving to *agentic* RAG.** A cited VentureBeat article notes enterprises transitioning *away* from in-house RAG stacks that lacked agentic retrieval — i.e. agents that **rerank** search results and **evaluate** system metrics during ingestion/retrieval.
- **Progress Agentic RAG = RAG-as-a-Service.** Pre-built document providers ingest video/audio/chat logs/docs; in-system agents extract key text, tags, entities and generate embeddings via LLMs.
- **Hybrid search + agent reranking is the core retrieval strategy:** keyword + semantic + **graph** search, all reranked by an agent — broader than vector-only RAG.
- **"Remy" is an embedded evaluation/quality agent** that continuously assesses system stability as data is ingested and retrieved (the agentic-evaluation piece in-house stacks were missing).
- **Two consumption paths:** no-code (UI dashboard + HTML **widget builder** for quick search experiences with citations) and code-first (**SDKs for .NET, TypeScript/JavaScript, Python + REST APIs**) for custom agents, UIs, and full app architectures.
- **Structured output from unstructured data is the standout SDK trick:** the C# SDK `AskAsync` method accepts a plain class type (e.g. `ChartAugmentedAnswer`); it's turned into a JSON schema the retrieval agent fills from search results, then deserialized back into your object — so you get chart-ready *structured* data out of PDFs.

## 📚 Detailed Notes

### Why RAG matters — the data deluge
Ed opens by grounding RAG in a data-scale argument he's been making since an **M3 conference talk in 2016** on the future of data storage and its relationship to machine learning. Back then the estimate was **44 zettabytes** collected by 2020. By **2026**, the world generates/collects roughly **400 million terabytes per day** worldwide — about **0.4 zettabytes/day**, or **~147 zettabytes/year**. The point: humans cannot make use of data at that scale without AI. His 2016 prescription was machine learning; today ML is "a commodity in the form of large language models," and the job of sifting data for answers is done by **human operators assisted by agentic systems**. RAG is how you connect those LLMs to *your* data.

### Context augmented generation — the parent concept
Before defining RAG, Ed insists on defining **context augmented generation**, because it sets the scale of the architectures involved. Definition: **adding data to the context window of an LLM** so you can ask questions about that data.
- **Simplest form — direct context loading:** upload a file into the context window and query it. Real-world example: the **Gemini button on some YouTube videos** — click it and the video's *transcript* is loaded into the LLM's context window, letting you query the video conversationally.

### Cache augmented generation — the middle tier
A richer form: take *more* data and store it in **vector memory**, then search that memory structure, pull out pertinent pieces, and insert those into the LLM's context.
- Real-world example: **GitHub Copilot inside VS Code.** The agent keeps memory of the conversation; your **project files are loaded into memory as vector data** for fast semantic searching; the LLM has all of this in its context. When you ask it to write code, it reaches into its cache, retrieves pertinent data, and uses it to generate code, answer questions, create summaries, etc.
- Mental model: cache-augmented generation = vector memory used as a fast, in-context cache, as opposed to a dedicated, large-scale vector *database*.

### Retrieval Augmented Generation — the definition
RAG is "another form of context augmented generation," but this time it uses a **vector database** to **store and retrieve information from large volumes using semantic similarity**. Two halves:
- **Retrieval** = finding useful information through **vector search**. Crucially *different from traditional keyword search*: instead of matching exact keywords, you use AI to find content with **semantically similar meaning**.
- **Augmented generation** = once relevant info is found, **retrieve it from the vector DB** and **place it into the LLM's context window**, then ask the LLM to **generate a new response** using that information.
- **Citations** can be requested so users trace where information originated. Ed stresses citations prove the answer is **grounded in real knowledge** — the system can "show receipts that prove the answer was not hallucinated."

### How data gets into a vector database — embedding & chunking
The ingestion mechanics:
1. **Ingest resources** (documents, etc.).
2. **Pass them through a vector embedding model.** The embedding model **extracts the meaning from the text** so searches can be done by semantic similarity (it turns text into vectors that encode meaning).
3. **Chunk large documents.** If a document is big enough, split it into **smaller bite-size pieces** — this makes it easier to ingest and store in the vector DB (and keeps each stored unit semantically coherent and retrievable).

### Generative AI search — what RAG unlocks
Because RAG can store large volumes, it's "perfect for generative AI search." **Generative AI search** empowers users to:
- Query large datasets in **natural language**, without memorizing specific query syntax.
- Make sense of large volumes of **business data stored in unstructured formats** — websites, PDFs, images, videos, and more.
- Do all of this *as if* the data were coming from a **relational database**, thanks to AI. This "structured query feel over unstructured sources" is the experience RAG is selling.

### Why end-to-end RAG is hard (the build-vs-buy argument)
Ed is candid that a real end-to-end RAG architecture is **complex** and usually multi-vendor. To ship one yourself you need:
- A **user interface**.
- **Embedding models** and **chat models**.
- A **data strategy**.
- **Document providers** that translate every document type (PDF, Office files, video, images, etc.) **into text** so it can be embedded into the vector DB.
- **Evaluation** of the quality of data flowing in and out of the RAG system.

Gluing these together demands **software engineering + data science + AI expertise** simultaneously. The result is **difficult to scale** and **difficult to predict cost**. He cites a recent **VentureBeat article** reporting enterprises **transitioning away from their in-house RAG stacks** — stacks that lacked the fundamentals of **agentic RAG**, where **agents help rerank search results and evaluate system metrics** as data is ingested and retrieved. (This is the gap the product pitch fills.)

### Progress Agentic RAG — the platform
> ⚠️ Caption note: the auto-captions garble the product name throughout (rendered variously as "Progress GenAI RAG", "Progress Corticon", "Progress OpenEdge RAG"). Corticon and OpenEdge are *other* Progress products; in context the speaker is consistently describing one offering — **Progress Agentic RAG**, the RAG-as-a-Service platform he names at the start. Treated as one product below.

Progress Agentic RAG is positioned as a **complete, end-to-end RAG-as-a-Service** that solves the above problems for you:
- **Ingests all sorts of documents** — video, audio, chat logs, and other info. **Document providers are already in place** to ingest data, so you don't build parsers.
- **Handles both structured and unstructured data.**
- **In-system agents** extract **key text, tags, entities**, and **generate embeddings**, all using large language models.
- **Hybrid search** = **keyword search + semantic search + graph search**, with results **reranked by an agent** (this is the "agentic" differentiator).
- **Remy** — an embedded **quality & evaluation metric/agent**: an AI agent that **evaluates system stability as data is ingested and retrieved**.
- **Management UI** — a system administrator logs in to ingest/manage data, **orchestrate AI agents**, and check evaluation metrics. Dashboard surfaces metrics on **quality, storage, and recently-ingested resources**.
- **Two build paths:**
  - **Fast / no-code:** an **HTML widget builder** to create robust search experiences (including citation + retrieval) deployable via HTML snippets — good for quick turnarounds.
  - **Custom / code-first:** **SDKs for .NET, TypeScript/JavaScript, and Python**, plus **REST APIs**, for custom agents, custom UIs, and complete application architectures.

### Ingestion & extraction in the UI (demo walkthrough — part 1)
From the **Upload** tab you can ingest **files, folders, links, text resources, entire site maps, and Q&A resources**. File resources can be any Office type, plus **videos, images, and audio (e.g. MP3)**. Ed has pre-ingested **SEC filings / financial reports** from major companies (Amazon, Apple, etc.). Opening **Apple's SEC filing** shows:
- The original **PDF** stored in a *file field* (the whole filing, ingested into the system).
- **Generated fields** — data **extracted from the PDF by background AI agents**.
- Those extraction **agents are configured on an Agent screen**, where you can **test and evaluate** them in the UI. The highlighted agent is configured to **extract chart-friendly data** from the unstructured files — a step that helps the **retrieval agent** find the right data when you later query the system with *structured* data types.
- A **simple search window** lets you sanity-check ingested data: asking *"What was Apple's revenue?"* returns *"Apple's total net sales from 2024 were $391 million"*. (Spoken figure; note Apple's FY2024 net sales were ~$391 **billion** — the captions/wording compress "billion," but the demo's point is the grounded retrieval, not the exact magnitude.) That simple search can be turned into a **widget** via *Create widget* and deployed to a webpage with HTML snippets.

### Going custom with the C# SDK + Blazor (demo walkthrough — part 2)
For something more advanced, Ed switches to **Visual Studio** and a **Blazor Server** app using the **C# SDK** to build a fully custom UI over Progress Agentic RAG.
- The SDK exposes a **search interface** with an **`AskAsync`** method.
- **Structured-output pattern (the key idea):** `AskAsync` optionally takes a **structure you want the system to fulfill** — *just a plain class object*. Here it's a class called **`ChartAugmentedAnswer`**, passed along with the user's request.
- When that type is passed in, it's **turned into a JSON structure/schema**. The **retrieval agent** sees that JSON, **maps values from the search results into it**, and **fulfills all the requested properties**.
- The filled JSON is **serialized back into the `ChartAugmentedAnswer` object** inside the app, which can then be displayed as **text *and* charts**.
- The running browser app is a fully customized UI built with the **Telerik UI for Blazor** component library, backed by the Progress Agentic RAG **C# SDK**.

### Custom UI in action (demo walkthrough — part 3)
In the chat interface, preset suggestions let you e.g. **compare Nvidia and Google's revenue** with one click, or type a natural-language query. Comparing **Nvidia vs Google** returns a **detailed textual comparison** *and* an openable **chart** — the **structured data** requested from Progress Agentic RAG is relayed back to the Blazor app and handed off to **UI components for chart rendering**. The takeaway Ed draws: this shows the **depth of customization** possible — any front-end tech you like, backed by the platform + SDKs.

### Where to learn more
Visit **progress.com**; a **QR code on screen** gathers all presentation resources, **including the financial-services application** that uses the **C# SDK + Blazor**.

## 🛠️ Products / Features / Technologies Mentioned
- **Progress Agentic RAG** — the session's headline product; a RAG-as-a-Service platform for ingesting, embedding, searching, and evaluating structured/unstructured data end-to-end. *(Product name garbled in captions as "GenAI RAG / Corticon / OpenEdge RAG"; resolved here.)*
- **Hybrid search (keyword + semantic + graph), agent-reranked** — Progress Agentic RAG's core retrieval engine.
- **"Remy" evaluation agent** — embedded AI agent that evaluates system stability/quality during ingestion and retrieval.
- **Document providers** — pre-built parsers that translate PDFs, Office files, video, images, and audio (MP3) into text for embedding.
- **Widget builder (HTML)** — no-code way to publish a search experience (with citations + retrieval) via HTML snippets.
- **Progress Agentic RAG SDKs** — .NET (**C#**), TypeScript/JavaScript, and Python, plus **REST APIs**, for custom agents/UIs/architectures.
- **`AskAsync` method** — C# SDK call that accepts a target class (e.g. `ChartAugmentedAnswer`) and returns structured, schema-filled results.
- **Telerik UI for Blazor** — Progress's component library used to build the custom demo dashboard UI.
- **Blazor Server** (spoken "Blazer") — .NET web UI framework hosting the custom demo app.
- **Large language models (LLMs)** — the chat/generation and extraction/embedding engines underpinning RAG.
- **Vector embedding model** — extracts meaning from text into vectors enabling semantic similarity search.
- **Vector database** — stores large volumes of embedded data for semantic retrieval (the heart of RAG).
- **Vector search / semantic similarity** — meaning-based retrieval, contrasted with keyword search.
- **Chunking** — splitting large documents into smaller pieces for ingestion/embedding/storage.
- **Citations / grounding** — traceability feature proving answers come from real source data, not hallucination.
- **Context augmented generation** — umbrella concept: adding data to an LLM's context window.
- **Cache augmented generation** — storing more data as vectors in memory and pulling pertinent pieces into context.
- **GitHub Copilot in VS Code** — cited as a real-world example of cache-augmented generation (project files as vector memory).
- **Gemini "summarize" button on YouTube** — cited example of plain context augmentation (transcript loaded into context).
- **SEC filings (Amazon, Apple, Nvidia, Google)** — sample financial PDFs ingested in the demo.

## 🚀 Announcements / What's New
None explicitly announced. This is an introductory/educational session plus a product overview of an existing **Progress Agentic RAG** platform; no previews, GA dates, or roadmap items were stated. (The clearest "new to you" item is simply the platform itself and its agentic hybrid-search + "Remy" evaluation capabilities, presented as available today.)

## 💡 Demos
- **Ingestion + AI extraction in the Progress Agentic RAG UI:** Uploaded SEC-filing PDFs (Apple/Amazon, etc.); showed the original PDF stored alongside **generated fields** extracted by background AI agents; demonstrated the **Agent screen** where an extraction agent is configured to pull **chart-friendly data** from unstructured files. *Point proved:* unstructured PDFs become queryable, partially-structured data automatically, priming the retrieval agent for structured queries.
- **Simple search → widget:** Asked *"What was Apple's revenue?"* and got a grounded answer (*"total net sales from 2024 were $391M"* as spoken), then converted that search into a deployable **HTML widget**. *Point proved:* zero-code path from ingested data to an embeddable search experience with citations.
- **C# SDK + Blazor structured retrieval:** In Visual Studio, used `AskAsync` with a `ChartAugmentedAnswer` class → platform serializes it to JSON, the retrieval agent fills it from search results, and it deserializes back into the app object. *Point proved:* you can get **structured, chart-ready data** out of unstructured PDFs via a plain C# class.
- **Custom Blazor dashboard in the browser:** A Telerik-UI-for-Blazor financial dashboard; clicked **"compare Nvidia and Google revenue"** (and free-text queries) to get a **text comparison + an openable chart** rendered from the returned structured data. *Point proved:* full UI customization and rich visualizations over any front-end, backed by the SDK.

## 📊 Notable Stats / Quotes
- **~400 million TB / day** generated worldwide in 2026 — *"about 0.4 zettabytes a day, or 147 zettabytes per year."*
- **44 zettabytes** — the 2016-era estimate (from his M3 2016 talk) for data collected **by 2020**.
- **"It's not humanly possible to make use of all that data we collect without using some sort of AI."**
- **"Instead of searching for exact keywords, we use AI to search for content with semantic similar meaning."**
- On citations: **"The system can show receipts that prove the answer was not hallucinated."**
- Demo answer: **"Apple's total net sales from 2024 were $391 million"** *(as spoken; Apple's FY2024 net sales were ~$391 **billion** — caption/phrasing compresses the magnitude).*
- Speaker credentials: **Principal Developer Advocate at Progress Software, 10-time Microsoft MVP.**

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Reproduce the **`AskAsync` + plain-class structured-output** pattern conceptually with Azure OpenAI structured outputs / JSON schema to compare DX vs the Progress SDK.
  - Spin up a tiny RAG loop (embed → vector DB → semantic search → grounded answer + citation) over a few PDFs to internalize chunking + citation grounding hands-on.
  - Evaluate **hybrid search (keyword + semantic + graph) with agentic reranking** in an Azure-native stack (Azure AI Search supports hybrid + semantic ranking) to see how close you can get without a managed RAGaaS.
  - Try the demo's **SEC-filing → chart** scenario with **Azure AI Search + a chart-friendly extraction prompt** to map the idea onto Microsoft-first tooling.
- [ ] Questions:
  - What exactly is "**graph search**" in their hybrid mix — knowledge-graph traversal over extracted entities, or graph-of-chunks? How is the graph built during ingestion?
  - How does **"Remy"** quantify "system stability" during ingestion/retrieval — what metrics does it surface, and can it gate bad ingestions?
  - What's the real cost/scaling model of a managed RAGaaS like this vs. the in-house-stack costs Ed says are "difficult to predict"?
  - Where's the boundary between "cache augmented generation" and "RAG" in practice — at what data volume do you graduate from vector *memory* to a vector *database*?
- [ ] Relevant to:
  - Anyone designing **production RAG over unstructured enterprise docs** (PDFs, Office, video/audio) who's weighing build-vs-buy.
  - **.NET / Blazor** teams wanting LLM-backed search with **structured (chart-ready) outputs** via an SDK.
  - Architects evaluating **agentic retrieval** (rerankers + evaluation agents) vs. classic vector-only RAG.
  - Our own Azure AI Search RAG work — useful conceptual contrast (hybrid search, citations/grounding, chunking, evaluation) even though the product is a third-party (Progress) platform, not Azure.

## 🔗 Related
- [[RAG (Retrieval Augmented Generation)]]
- [[Vector search & embeddings]]
- [[Azure AI Search]]
- [[Chunking strategies for RAG]]
- [[Grounding & citations in LLM apps]]
- [[Blazor]]
- [[Microsoft Build 2026]]
- Source list: [[2026 Build Session List]]
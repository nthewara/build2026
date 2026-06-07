---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/agents
  - topic/tools
  - topic/mcp
  - topic/ai
  - topic/foundry
source: https://www.youtube.com/watch?v=nZM5PkjzSKo
session_code: BRK242
event: Microsoft Build 2026
speakers: Maria Nagaga, Joe Blick
duration_min: 43
aliases:
  - Turn your agents into action Connect tools APIs documents
---

# BRK242 — Turn your agents into action: Connect tools, APIs, and documents

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Maria Nagaga (Program/Product Manager, Microsoft Foundry tools) · Joe Blick (Content Understanding)  
> **Duration:** ~43 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=nZM5PkjzSKo)

## 🎯 TL;DR
Agents create business value through **tool calling** — but as the tool ecosystem explodes (MCP, OpenAPI, A2A, connectors, skills, CLIs, plugins…), wiring tools into agents has become the real bottleneck: every integration has its own identity, protocol, and credential model, so "six integrations" silently balloons into hundreds. Microsoft Foundry's answer is **Toolbox** — a reusable, managed bundle that exposes *any* tool type through a single MCP-compatible endpoint with one auth, plus **Tool Search** so the agent loads only the one tool it needs (saving context/tokens) instead of every tool. The second half covers **Content Understanding**, a GA pipeline (parse → classify → extract) that turns messy multimodal files (PDFs, docx, images, video, charts) into clean, grounded, structured JSON/markdown so agents stop choking on documents — with **agentic extraction**, section-level splitting, knowledge-source training, and GPT-5-family engines arriving in July. The throughline: the same "Fibby" fiber-optic field-ops agent demonstrates toolbox + content understanding working together end to end.

## 🔑 Key Takeaways
- **Tool calling is the single most important agent capability** — LLMs provide reasoning, but tool calling is what lets an agent *take action* and deliver real business value.
- The tool ecosystem is exploding beyond MCP: **OpenAPI, MCP, A2A, Logic App connectors, skills, CLIs, plugins** and more — and the hard part is no longer the *number* of tools but the *types*.
- Three unsolved agentic problems sit on top of a catalog: **tool creation** (curate a set per task), **tool discovery** (pick the best tool within a *token budget*), and **tool governance** (control who/what gets which tools).
- **Tool discovery ≠ searching a registry** — it's choosing the best tool to complete a task *while minimising tokens / context-window bloat*.
- **Integration, not discovery, is the real pain**: each tool has its own identity, team-of-origin, protocol, and credential management; one field-ops agent's "6 integrations" multiplied across many agents becomes *hundreds* of integrations. Devs spend more time integrating than building agents.
- **Toolbox** = a reusable bundle of tools, **managed in Foundry**, consumed through one **consistent interface regardless of tool type** — four pillars: **Build, Discovery, Consuming, Governed**.
- Toolbox gives **one unified MCP-compatible endpoint, one auth, one experience** — the agent doesn't care whether the underlying tool is MCP, an OpenAPI spec, a skill, or a connector.
- **Tool Search** is a tool *inside* the toolbox: it reads tool metadata and loads only the required tool into the context window (e.g. "I need GitHub" → only the GitHub tool loads, not all 10).
- Toolbox is portable across runtimes: **GitHub Copilot / CLI, GitHub Copilot SDK**, targeting **Claude Code**, and **soon Microsoft Copilot Studio**.
- The **tools catalog shipped in 2025**; for a private registry you can pair it with **Azure API Center + Azure API Management** for extra governance.
- **Content Understanding** turns messy, multimodal content into **clean, structured, agent-ready output** (structured JSON + key-value pairs + markdown) so agents stop writing brittle custom code to crack files.
- Content Understanding is a **single pipeline: parse → classify → extract**, works across **any modality** (PDF, docx, image, video, even zip/email files), and is **already GA (~6 months) and in production ~1.5 years**.
- Extracted fields are **grounded to bounding boxes/words in the source** and carry **confidence scores**, enabling **auto-approve when confident / route to human review when not** — the basis for real automation.
- A low-quality default parser silently produces **ungrounded, wrong answers** (e.g. missing measurements, "scheduled" vs "completed"); turning on Content Understanding yields correct, grounded answers and even **JSON for charts/figures**.
- Coming **July**: **agentic extraction** (build an answer by reasoning across files, not just find it), **section-boundary splitting**, **knowledge-source training** on your own document types, and **cheaper pre-built analyzers** plus **GPT-5-family engines**.
- Content Understanding plugs into agents three ways: **Foundry IQ ingestion**, **context provider** (incl. a **LangChain** primitive) to pre-process incoming files, and **encoding business rules** via custom classify/extract analyzers.

## 📚 Detailed Notes

### Framing: what it means to build an agent platform at Microsoft
The session opens with Microsoft's agent-platform story: **build on GitHub**, use **Microsoft Foundry** as the platform (agent runtime, agent optimisation, and the tools you need), and **distribute through M365**. Foundry itself provides **agent services, models, IQ tools, and a control plane**, and lets you **govern the lifecycle from cloud to edge**. Within Foundry, **Foundry Tools** (Maria's area, with colleague Linda) is the hub for **pre-built tools and third-party tools** with enterprise-grade scalability — the goal is **one place for all your tools, regardless of tool type**.

### Why tool calling matters (and why it's hard)
- **LLMs supply reasoning; tool calling supplies *action*.** Tool calling is how agents deliver real business value.
- This is also where the danger lives: **tools reach into production code, databases, and APIs and generate real results.** Security has to cover both the *agent's* access to the right tools *and* the access of the *individual humans* using those agents.
- Customer pain points (thousands of papers written on this) cluster into recurring themes:
  - **Steering** — finding the right tool for the job in a rapidly growing ecosystem.
  - **Sprawl** — managing tools, keeping them secure, making them easy to publish.
  - **Security / control** — controlling which tools are exposed and to whom.

### The three missing capabilities (on top of a catalog)
Even once you can *find* tools, three problems remain in the agentic ecosystem:
1. **Tool creation** — curate the set of tools a given agent needs for a specific task, then **share that curated list across every agent** you control.
2. **Tool discovery** — *not* "search a registry." It's **choosing the best tool to complete the task while spending the fewest tokens** (avoiding context-window bloat). Maria stresses token efficiency repeatedly.
3. **Tool governance** — fine-grained control so different people/agents get different tool access ("I don't want Maria to have the same tool access as Linda").

### The tool catalog (shipped 2025) — and its limits
- The **tools catalog** (built last year, **shipped in 2025**) solves the "all tools in one place" problem. Foundry ships a catalog of community/ecosystem tools custom-built for it.
- For a **private registry**, you can layer on **Azure API Center** and **Azure API Management** for additional governance.
- **The tool landscape is about *types*, not just counts:** OpenAPI, MCP, A2A, Logic App connectors, skills, CLIs, plugins, "books," and more — "there's going to be foo bar, x bar, it's going to continuously grow."

### The real bottleneck: integration, not discovery
- Catalog solves *finding*; it does **not** solve *integrating*. These are two different problems.
- Worked example: a **field-ops agent** with six integrations — **Entra, SharePoint, ticketing, a custom MCP/API, Teams access, blob storage, Azure Search**. It *sounds* simple, but each tool has:
  - its **own identity**,
  - is built by a **different team**,
  - uses a **different protocol**,
  - and has **different credential management**.
- Now multiply by every integration that agent needs, **and** by every *other* agent (customer support, billing, networks, inventory…). "Six integrations" becomes **hundreds** — before you even count permissions, failure handling, and debugging. Net effect: **developers spend more time integrating tools than building agents** (the thing that actually makes money).

### Toolbox — the proposed solution
A **Toolbox** is *"a reusable bundle of tools managed in Foundry that agents can consume through a single consistent interface regardless of tool type."* (Featured in Satya's keynote earlier in the event.) The three words that matter:
- **Reusable** — build a toolbox once, use it across any agent.
- **Managed** — Foundry handles the lifecycle so you don't have to.
- **Consistent interface** — the agent doesn't care whether the underlying tool is MCP, an OpenAPI spec, a skill, or a connector. You get **one unified endpoint, one auth, one experience**.

#### The four pillars of Toolbox
1. **Build** — create tools in a **named, reusable bundle**, configure and publish them. (E.g. a single *Field Ops* toolbox holding the Entra/SharePoint/etc. config instead of scattering it.)
2. **Discovery** — when the agent prompts the toolbox, it **retrieves only the tool required** to complete the task.
3. **Consuming** — a **single MCP-compatible endpoint** exposes every tool to any agent runtime; carry that one endpoint across every agent.
4. **Governed** — **centralised authentication and observability** to monitor all tool calls.

#### Features that implement the pillars
- **Toolbox** — how you build the bundles.
- **Tool Search** — a tool that lets you **search and discover tools at runtime** (see below).
- **Unified endpoint** — the **MCP-compatible** consumption surface.
- **Control & visibility** — add your **own policies and guardrails**; a **governance dashboard** is coming for more detail.

#### Portability (where you can consume a toolbox)
The toolbox endpoint is meant to travel: **GitHub Copilot / CLI, GitHub Copilot SDK**, with **Claude Code** support being worked on, and **soon Microsoft Copilot Studio**. The lifecycle promise: *build a toolbox → consume a unified endpoint → know it's governed.*

### Tool Search — how token savings actually happen
**Tool Search** is a tool *within* the toolbox. Instead of loading every tool definition into the context window, it **pulls the metadata of all tools in the toolbox, finds the right one, and loads only that tool**. In the closing demo the agent "found 10 tools but only selected one." This is the concrete mechanism behind the repeated "use fewer tokens" message — the diagram Maria shows goes from **manually wiring every tool to an agent** → **attach a toolbox, expose one unified endpoint, let Tool Search decide and load just the needed tool**.

### Skills, the catalog, and a new browser-automation tool (Foundry portal tour)
In the Foundry portal under **Build → Tools** you now see three things: **Toolbox, Tools, and Skills.**
- **Skills** can be uploaded and shared: Maria uploads an "art skill" (one that helps make better architectural diagrams) from her desktop so **any agent in that project** can use it; she also publishes it to the repo.
- **Browser automation is a new tool available *today*** — **built on Playwright**, it can **scrape information and fill in forms** (demoed by auto-filling a Microsoft form).
- Building a toolbox in the portal: **Toolbox → Create → name it → Add tools** (shows every catalog tool) **→ Add skills** (e.g. the skill just uploaded). A toolbox can be **set as default**, which **points the hosted agent's endpoint at that specific toolbox version**. There's a per-toolbox **"turn Tool Search on/off"** toggle.

### Part 2 — Agents in the real world need documents, not just APIs (Joe Blick)
Toolbox solves agents-accessing-tools and saves tokens, but **a lot of the content an agent needs lives in documents, videos, and PowerPoint decks**, not APIs. When agents try to crack that content themselves they **break, scramble, and burn tokens** — writing custom code to parse a PowerPoint, missing content, finding a table but failing to read its cells. **Content Understanding** exists to fix this.

### What Content Understanding is
It **takes messy, multimodal content and turns it into clean, structured, agent-ready output.** Any file type flows in, gets **parsed, classified, extracted**, and comes out as **structured JSON with key-value pairs plus markdown** that represents the file's details with **high fidelity**.
- Not new/experimental: **GA'd ~6 months ago, in production ~1.5 years.**
- **Foundry IQ** uses it as its **content-extraction layer** to get the highest-fidelity input for grounding agents.
- **Microsoft 365 Copilot** uses it when you ask a question about a document or PDF.

### How customers use it (proof points)
- **Wolters Kluwer** — trusted professional tools for **tax automation, legal, and healthcare**. Their **CCH Access Tax** product uses Content Understanding to ingest **tax forms, supporting tax documents, and other financial documents** in structured format to **automate tax-prep processing end to end**.
- **DataSnipper** — an **agentic platform for audit and finance**. Their AI extraction capability is **powered by Content Understanding**, taking any document **directly into Excel** (where finance pros want to work) in structured format. They cite **faster reviews, more reliable evidence, and trustworthy AI**.

### The pipeline: parse → classify → extract
A **single pipeline**, available for **any modality** (video, image, document, PDF, even old formats like zip/email files), with a **custom-tailored solution per file type**:
- **Parse** — turn any input document into **markdown**. Built on **Microsoft's OCR + layout technology refined over 20 years**, still state-of-the-art. Handles **tables, multilingual documents, even a crumpled page**. It's the **foundation of search ingestion for Foundry IQ**. Key advancement seen in the demo: **extract tables well into structured markdown** to ground agents, and **detailed representations of figures (charts/diagrams)** so that content isn't lost on ingestion.
- **Classify** — decide **what kind of document** something is, or **break a long document into logical parts**. Enterprise files are often **packages** (a case file, an application bundle, a tax submission) of many documents combined. Classification lets you **identify the classes you care about, throw away irrelevant parts, and extract from the right pieces**. *Coming July:* split documents on **section boundaries**, not just page boundaries (a top customer ask, since real boundaries rarely fall neatly on pages).
- **Extract** — parse content into **structured fields / structured output**: **key-value pairs, confidence scores, grounded results.** Each field is **grounded back to a bounding box / word / sentence** in the source (not just an LLM completion), so you can jump back into the file to see where it came from. **Confidence scores** drive **auto-approve when high / human review when low** — the basis for real automation workloads.

### Quality + integration improvements
- **Broad coverage:** more new file types supported.
- **Better quality:** the **GPT-5 family of models** added as an engine for running **extraction and classification**.
- **Easier integration:** support for **Logic Apps, Agent Framework, LangChain, markdown**, and a set of **open-source tools** so extraction can run as part of your agent runtime.

### What's coming in July (extract roadmap)
- **Knowledge-source training:** provide a few examples of a document type that matters to you (a specific tax form, an industry financial doc); **Content Understanding trains on it and improves results.**
- **New pre-built analyzers** with **significant cost/token reductions** — much more efficient.
- **Agentic extraction** (detailed below).

### Agentic extraction — "build the answer, don't just find it"
Standard extraction is good at **finding answers and summarising data** in a document. But a **broader class of problems** needs an answer that must be **built step-by-step by reasoning across content**, e.g.:
- *"For this contract and this set of amendments, which clause applies across the entire chain of changes?"*
- *"How do I root-cause this issue?"*

For these, just finding a single value isn't enough — you must **reason across the files**. **Agentic mode** (coming **July**) turns this on for the hardest problems where standard extraction fails.

**Recorded demo (agentic extraction):** uses the same grounding documents as morning **demo session 331** (repo available via QR code). Scenario: a **complicated fiber-optic cable failure** described across a document/history. You set **questions in the schema** — *"What's the root cause? How much will it cost to fix? Is it on budget?"* — and Content Understanding's agentic mode **uses a set of tools to reason across the corpus of evidence and loop over it**. In the trace it **finds specific evidence in the documents, asks follow-up questions about images, runs calculations and code**, and **captures a set of evidence to support a final, well-grounded answer**. Output: a **root cause + cost analysis**, correctly answered — work that would otherwise require a lot of custom coding.

### The three ways to use Content Understanding with agents (Fibby demo)
Joe returns to the **"Fibby" fiber-optic field-ops agent** (the same agent Maria demoed) to show three high-value patterns. The agent UI exposes which **Foundry IQ knowledge source** and which **context provider** it's using.

1. **Foundry IQ ingestion / knowledge source.**
   - With a **minimal knowledge source that does NOT use Content Understanding**, asking about an **F3 fiber** measurement (a "1310" value that has *no recorded evidence* in the doc) makes the agent **hallucinate "46" — an ungrounded answer.**
   - Turning on **Content Understanding (standard mode)** generates a **structured markdown representation of the maintenance log** that surfaces the **missing value** explicitly — so the agent now correctly says **there's no recorded separate value**, instead of a simple PDF parser lumping it into a long list and inventing a number. During **indexing**, Content Understanding pulls **figure descriptions, tables, and structure with minimal loss** into the index for correct answers.

2. **Context provider (real-time file upload).**
   - Agent harnesses typically have **very limited file support** — e.g. **`.docx` files aren't supported** by default. Enabling **Content Understanding as a context provider** (a primitive in **Agent Framework**, with a **LangChain** equivalent) **pre-processes files and generates a text version** to hand the agent, so it can process **any file type, not just PDFs**.
   - Even with PDFs, the **default low-quality parser gives wrong answers**: asked about **work order 89**, the agent says **"scheduled,"** but the order is actually **"completed."** Turning on Content Understanding produces a **nice structured table** (and a **JSON representation of chart data** so chart context isn't lost), and the agent then correctly reports **work order 89 is complete** — matching the PDF.

3. **Encoding business rules via custom analyzers.**
   - Some files are inherently hard to interpret. Example: a work order where **J. Martinez** is the **field technician**, but **John Smith** is listed as the **site contact**. With **no guidance**, the agent wrongly answers **"John Smith."**
   - Fix: build a **classify + extract analyzer** in **Content Understanding Studio** (where you can visualise/edit analyzers). The analyzer **classifies the whole file** ("is this a work order or not?" — with a description; you could list hundreds of classes, or classify page-by-page / section-by-section), and on a work order **extracts the technician** using **guidance** ("this *route* field tells you who the technician is"). With those **business rules encoded**, the agent correctly answers **Jay Martinez** — even for a genuinely hard question.

**Summary of the three scenarios:** (1) Foundry IQ indexing with structure/figures/tables preserved, (2) context provider to process any incoming file type accurately, (3) custom analyzers to encode your own business rules — *"a work order, a tax file, or whatever the type of documents I care about."*

### Closing demo and resources (Maria)
A final demo shows an agent using the **unified endpoint inside an Agent Framework / LangGraph application** (similar to Fibby). Watching the **activity line**: it goes into the toolbox, **loads a skill, finds 10 tools but selects only one**, pulls that tool, checks the order, and returns results — proving Tool Search loads one tool instead of all of them, and that it's real and usable today.

**Where to go:**
- **`ai.azure.com`** → Foundry (try toolbox/tools/skills).
- **`aka.ms/<build session number>`** — demo content for this session.
- **`aka.ms/phoebe`** — the **live Fibby demo** you can open on phone/computer; **up for the rest of the week**, with **demo code** included.
- Join the **Foundry Discord** and the documentation.

> Honesty note from the room: several live demos struggled ("the demo gods weren't with me today"); Maria attributed failures to site load and joked about "demo ghosts." The recorded/GIF fallbacks and the hosted `aka.ms/phoebe` agent were provided as proof the features work.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — the agent platform: agent services, models, IQ tools, a control plane; governs lifecycle cloud-to-edge.
- **Foundry Tools** — hub of pre-built + third-party tools with enterprise-grade scalability.
- **Tools Catalog** — Foundry's catalog of ecosystem tools; **shipped 2025**; "all tools in one place."
- **Toolbox** — reusable, Foundry-managed bundle of mixed-type tools behind one MCP-compatible endpoint + one auth (keynote feature).
- **Tool Search** — tool inside a toolbox that loads only the required tool at runtime via metadata (token saver).
- **Unified endpoint** — single **MCP-compatible** consumption surface for any agent runtime.
- **Skills** — uploadable/shareable capability units (e.g. an architectural-diagram "art skill"); addable to toolboxes; visible under Foundry → Build → Tools.
- **Browser automation tool** — *new, available today*; **built on Playwright**; scrapes info and fills forms.
- **MCP (Model Context Protocol)** — the baseline protocol; toolbox's endpoint is MCP-compatible. Referenced as "the time when all we had was MCP."
- **Tool types named** — **OpenAPI, MCP, A2A (Agent-to-Agent), Logic App connectors, skills, CLIs, plugins, "books"** and more.
- **Azure API Center** — pair with the catalog to host your **own private tool registry** with extra governance.
- **Azure API Management (APIM)** — additional governance layer for a private registry.
- **GitHub** — where you build; toolbox consumable via **GitHub Copilot / CLI** and the **GitHub Copilot SDK**.
- **Claude Code** — target runtime for toolbox support (in progress).
- **Microsoft Copilot Studio** — toolbox consumption coming soon.
- **Microsoft 365 (M365)** — distribution channel for tools/agents.
- **Entra, SharePoint, Microsoft Teams, Azure Blob Storage, Azure AI Search** — example enterprise integrations for a field-ops agent (each with its own identity/protocol/credentials).
- **Azure Container Apps** — where the hosted Fibby agent runs.
- **Governance dashboard** — coming, for detailed control/visibility over tool calls.
- **Content Understanding** — GA pipeline (parse → classify → extract) turning multimodal files into clean, grounded structured JSON + markdown.
- **Content Understanding Studio** — UI to visualise and edit classify/extract analyzers.
- **Foundry IQ** — uses Content Understanding as its content-extraction/grounding layer; knowledge-source + indexing.
- **Microsoft 365 Copilot** — uses Content Understanding to answer questions about documents/PDFs.
- **GPT-5 family of models** — added as an engine for Content Understanding extraction + classification.
- **Microsoft OCR + layout technology** — 20-year-refined engine underpinning Parse (tables, multilingual, degraded pages).
- **Agent Framework** — supports Content Understanding as a **context provider** primitive.
- **LangChain / LangGraph** — supported: a LangChain context-provider primitive; closing demo runs in a LangGraph app.
- **Logic Apps** — integration target for Content Understanding.
- **Pre-built analyzers** — coming July with significant token/cost reductions.
- **Wolters Kluwer — CCH Access Tax** — customer using Content Understanding for tax/financial document ingestion.
- **DataSnipper** — audit/finance agentic platform whose AI extraction is powered by Content Understanding (docs → Excel).

## 🚀 Announcements / What's New
- **Toolbox** — reusable, Foundry-managed bundles of mixed-type tools behind a single MCP-compatible endpoint with one auth + Tool Search; **featured in Satya's Build keynote**. Presented as available to build/try in Foundry now (portal + code); broader runtime support (Claude Code, Copilot Studio) in progress.
- **Tool Search** — runtime tool-selection capability inside toolbox that loads only the needed tool (token savings), demoed live ("found 10 tools, selected one").
- **Browser automation tool** — **available today**, built on Playwright; scrapes data and fills forms. Called out as a brand-new tool.
- **Tools catalog** — (recap) shipped in 2025; foundation this builds on.
- **Content Understanding GPT-5-family engines** — GPT-5 family added for extraction/classification (quality improvement).
- **Broader file-type coverage + open-source integrations** — Logic Apps, Agent Framework, LangChain, markdown tooling for Content Understanding.
- **Coming July (Content Understanding):**
  - **Section-boundary document splitting** (not just page boundaries).
  - **Knowledge-source training** — train analyzers on your own document types from a few examples.
  - **New pre-built analyzers** with significant cost/token reductions.
  - **Agentic extraction** — reason across files to *build* answers for the hardest extraction problems.
- **Governance dashboard for toolbox** — roadmap item (no date given).
- **Live demo agent** at **aka.ms/phoebe** available for the rest of Build week, with demo code.
- Q&A close: asked for a rough timeline on an unspecified item, the speaker estimated **"two to three months"** (explicitly "don't hold me to it").

## 💡 Demos
- **"No-toolbox" config (anti-pattern):** showed raw app config wiring **3 MCP servers** by hand — auth sprawled from **line 33 to line 104**, and that's only three servers. Point: manual multi-protocol wiring balloons fast and wastes dev time. (Code was AI-generated and non-runnable, shown only to illustrate the pain.)
- **Toolbox config:** the equivalent collapses to a tiny config — auth configured once, all servers in one toolbox, which **generates a URL** to drop into any app. Point: toolbox replaces the sprawl with one endpoint.
- **Tool Search:** showed that asking for GitHub loads **only** the GitHub tool into the context window, not every tool. Point: token/context savings.
- **Foundry portal tour:** Build → Tools shows **Toolbox / Tools / Skills**; uploaded an **"art skill"** (architectural-diagram helper) from desktop so any agent in the project can use it.
- **Browser automation:** auto-filled a **Microsoft form** from a pasted request (with a GIF fallback prepared). Point: new Playwright-based tool works end to end.
- **Build a toolbox in-portal:** Toolbox → Create → name → Add tools (from catalog) + Add skills; set a toolbox as **default** to point the hosted agent's endpoint at that version; per-toolbox **Tool Search on/off** toggle.
- **Hosted agent work order (live):** asked the agent to find a work order and check completeness/parts availability — succeeded live after a load-related stumble. Point: the unified endpoint drives a real agent.
- **Fibby agent on the same MCP endpoint:** hosted in **Azure Container Apps**; the **activity view** shows which tools were called, how Tool Search picked them, and how they loaded.
- **Content Understanding — Foundry IQ grounding:** minimal source hallucinated an **F3 fiber / 1310** measurement ("46") that has no evidence; enabling Content Understanding produced structured markdown exposing the **missing value** → correct "no recorded value" answer.
- **Content Understanding — context provider:** default harness can't take **.docx**; enabling Content Understanding as a context provider pre-processes any file to text. With PDFs, the default parser said **work order 89 = "scheduled"** (wrong); Content Understanding produced a structured table + **chart JSON** → correct **"completed."**
- **Content Understanding — business-rule analyzer:** a work order had technician **J. Martinez** but contact **John Smith**; unguided agent answered "John Smith"; a custom classify+extract analyzer (built in Content Understanding Studio, using the *route* field as guidance) returned the correct **Jay Martinez**.
- **Agentic extraction (recorded):** fiber-optic cable failure scenario (shared with demo 331); schema questions (root cause / cost / on-budget?) drove reasoning across evidence — searching docs, asking about images, running calculations/code — to produce a grounded **root cause + cost analysis**.
- **Closing LangGraph agent (live):** activity line showed it **load a skill, find 10 tools, select 1**, check the order, and return results. Point: Tool Search is real and usable today.

## 📊 Notable Stats / Quotes
- **"6 integrations → hundreds of integrations"** — the core scaling problem once you multiply tools across many agents.
- **Config sprawl: lines 33–104** of auth config for just **3 MCP servers** without a toolbox.
- **Tool Search: "found 10 tools, but only selected one"** loaded into the context window (twice demonstrated).
- **Content Understanding: GA'd ~6 months ago; in production ~1.5 years.**
- **20 years** of refinement on Microsoft's OCR + layout technology behind Parse.
- **GPT-5 family** added as the extraction/classification engine.
- Roadmap cadence: **"coming in July"** (section splitting, knowledge-source training, cheaper analyzers, agentic extraction); a Q&A estimate of **"two to three months"** for an unspecified item.
- **"LLMs provide the reasoning… tool calling is what enables your agent to perform an action… this is how your agents provide real business value."**
- **"Tool discovery is choosing the best tool to complete the task while using the limited amount of tokens."**
- **"Your agent shouldn't have to care what the underlying tool type is."** — one endpoint, one auth, one experience.
- **"An answer needs to be built, not found"** — the rationale for agentic extraction.
- **"The demo gods weren't with me today."** — on the live-demo struggles (most still succeeded or had fallbacks).

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Build a **Toolbox** in Foundry (`ai.azure.com`) bundling a couple of MCP servers + a skill, set it default, and point a hosted agent at the unified endpoint.
  - Toggle **Tool Search** on a toolbox and watch the activity view confirm only the needed tool loads (measure token impact).
  - Try the **browser automation** (Playwright) tool to fill a form / scrape a page.
  - Open the live **aka.ms/phoebe** Fibby agent + pull the demo code from `aka.ms/<this session's build number>`.
  - Turn on **Content Understanding** as a Foundry IQ knowledge source and as an **Agent Framework / LangChain context provider**; feed it a `.docx` and a chart-heavy PDF and compare answers vs the default parser.
  - Build a classify+extract **analyzer** in Content Understanding Studio to encode a business rule (e.g. pick the right field from a work order/tax form).
- [ ] Questions:
  - Exact **pricing/token model** for Toolbox + Tool Search, and for Content Understanding standard vs agentic mode.
  - What's the **GA vs preview** status of Toolbox itself (keynote feature — preview tier? regions?) and the **July** items.
  - How does toolbox **governance** map to **Entra**/RBAC for per-user (not just per-agent) tool access?
  - Does the **MCP-compatible** endpoint interop with non-Microsoft MCP clients cleanly today?
  - Which **file types** are newly supported in Content Understanding, and analyzer **training data** requirements/limits?
- [ ] Relevant to:
  - Any agent project facing **tool/integration sprawl** across multiple agents (field ops, support, billing, inventory).
  - **Document-heavy** agent scenarios (finance/audit/tax/legal) needing grounded, structured extraction.
  - Foundry IQ / RAG pipelines wanting **table + figure fidelity** at ingestion.

## 🔗 Related
- [[Microsoft Foundry]]
- [[Foundry IQ]]
- [[Model Context Protocol (MCP)]]
- [[Content Understanding]]
- [[Agent Framework]]
- Build 2026 demo session **331** (shared agentic-extraction grounding docs)
- `aka.ms/phoebe` — live Fibby fiber-optic field-ops agent + demo code

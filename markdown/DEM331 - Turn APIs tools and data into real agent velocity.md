---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/azure-ai-foundry
  - topic/content-understanding
  - topic/agents
  - topic/multimodal
source: https://www.youtube.com/watch?v=b23ZV37_9Hw
session_code: DEM331
event: Microsoft Build 2026
speakers: Azure AI Foundry Content Understanding team (presenter, name not stated in transcript)
duration_min: 22
aliases:
  - Turn APIs tools and data into real agent velocity
---

# DEM331 — Turn APIs, tools, and data into real agent velocity

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Azure AI Foundry — Content Understanding team (live-demo presenter; specific name not stated in the captions)  
> **Duration:** ~22 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=b23ZV37_9Hw)

## 🎯 TL;DR
Agents break when they hit real-world content — scanned PDFs, long emails, complex tables, images, audio, and video — because they can reason but can't reliably *read*. Azure AI **Content Understanding** solves this by turning messy multimodal content into clean, structured, agent-ready Markdown + JSON through a single **parse → classify → extract** pipeline with built-in grounding, confidence scores, and governance. The session is a live demo of a telecom incident-response scenario (a 6:47 a.m. fiber-cut alert) where documents, audio, and video are converted into structured evidence, fed to an LLM to diagnose root cause, plan materials within budget, and dispatch a repair crew. It shows four integration "acts" — from manual SDK pipeline calls, the Foundry/CU Studio no-code playground, custom analyzers + classification/routing, all the way to seamless orchestration via the **Content Understanding context provider in Microsoft Agent Framework**, which adds auto-analysis of attachments and multi-turn caching. A standout claim: the SDK's `to_llm_input` formatter helper produced an **85% token reduction** in their scenario.

## 🔑 Key Takeaways
- **Agents can reason but can't read.** Throwing raw, messy content directly at LLMs causes custom-code sprawl, misread tables, skipped figures, lower reliability, and higher token bills.
- **Content Understanding = one pipeline** that *parses, classifies, and extracts* multimodal content into clean structured output (well-formatted **Markdown** + **JSON** key-value pairs) that is "agent ready-to-act."
- **Built-in grounding, confidence scores, and governance** come with the output — not bolted on afterward.
- **Pre-built analyzers** cover common needs out of the box: `document search`, `invoice`, `audio`, `video`, plus a long catalog spanning tax, legal, identity, payment, mortgage, etc.
- **`document search`** extracts layout + embedded elements: tables (with row/column structure preserved), figures, selection marks (checkboxes), barcodes/QR codes, and signatures — ideal for feeding RAG / AI Search.
- **A local PDF parser loses structure** (table layout, QR codes, selection marks) even on clean typed PDFs, forcing the agent to guess — Content Understanding preserves it as LLM-readable evidence.
- **Custom analyzers** go beyond extraction: they can **reason, infer, and generate** new fields by calculating/reasoning (e.g., dispatch urgency, budget verdict) that aren't literally present in the document.
- **Classifier + routing**: a *single call* classifies an unknown document, routes it to the right analyzer (pre-built or custom), and extracts — minimizing branching logic in app code. Recommended for production.
- **`to_llm_input` SDK helper** formats output as Markdown with YAML front matter, can send full doc *or* fields-only, and drove an **85% token reduction** in the demo scenario.
- **Microsoft Agent Framework integration** via a **context provider** primitive that hooks the agent run loop: it sees/detects messages (e.g., attachments) *before they reach the LLM*, processes them, and returns structured output into the conversation loop.
- **Multi-turn caching**: a follow-up question reused the context provider's cached Content Understanding results — no repeat analysis calls.
- **Same underlying service, different integration shapes**: manual SDK pipeline vs. Agent Framework context provider (auto-analysis, auto-formatting, caching, one provider for any agent).
- **Initialization is simple**: reuse your **Azure AI Foundry resource endpoint** + credentials with the SDK (Python shown).
- **No-code path** exists in the **Foundry portal → Content Understanding playground** and **CU Studio** (Discover tab) for trying analyzers without writing code.
- **Direct integrations** also provided for frameworks like **LangChain** (and raw Markdown), not only Agent Framework.

## 📚 Detailed Notes

### The Problem: agents meet real-world content
Tools and agents inevitably run into content that *doesn't* come from clean APIs and structured data: poor-quality scanned PDFs, long emails, office documents with complex tables, images, audio, and video files. This is where agents often break — **they can reason, but they cannot really read.** When raw content is thrown at the LLM, the agent scrambles: for every incoming file it writes custom code, uploads images to models, misreads tables, skips figures. The downstream result is dropping quality and reliability *and* a rising LLM bill.

### The Solution: Content Understanding
Content Understanding takes messy multimodal content and turns it into **clean, structured, agent-ready output through a single pipeline**: **parse, classify, and extract**, with built-in **grounding, confidence scores, and governance**. The output is **well-formatted Markdown and JSON files with key-value pairs** that give agents ready-to-act inputs.

### The Demo Scenario: a 6:47 a.m. fiber incident
The narrative scenario: at **6:47 a.m.** an alert fires — **signal degradation on the "Tower Ridge Corridor," 42 customers at risk.** Today, an on-call engineer would have to search **nine documents, media files, and attachments**, then manually investigate and correlate everything. This is the exact workflow the demo automates.

The plan for the demo:
1. Use Content Understanding to turn each document pulled by the alert/incident into **structured data** — layout, tables, figures, barcodes, custom fields you define, plus classification and routing.
2. Send that information to an agent — first via a **direct call to GPT-4.1** (auto-caption likely "GPT-4 1") — to **diagnose, identify, and dispatch a plan.**
3. In the final act, show the whole thing integrated seamlessly with **Microsoft Agent Framework.**

### Act 1 — Initialize the client + `document search` (SDK)
- **Initialization is intentionally simple**: you use the **same endpoint as your Azure AI Foundry resource**, initiate with endpoint + credentials, then use the SDK (Python).
- Make a simple **pre-built analyzer call with `document search`** — one of many pre-built analyzers.
- *(Live hiccup: a presenter extension didn't load — "I think the extension did not work, but we'll do this together" — handled gracefully; they walked the flow and client-init code manually.)*
- **`document search` is optimized for extracting document layout and embedded elements**: tables, figures, selection marks, barcodes, signatures, etc. It generates rich information you can send to downstream apps like **RAG or AI Search.**

**Running it on a site maintenance log:**
- The log has **two embedded tables**, lots of information formatted in a way that's *not* intuitive for an LLM agent to extract directly, plus selection marks and QR codes.
- Within a few seconds, Content Understanding returns:
  - **Two tables** with **row and column structure preserved**.
  - **One barcode / QR code decoded.**
  - **Two checked and one unchecked selection marks.**
- That structured information is then sent to the LLM to reason and is tracked as a **piece of evidence.**

**Comparison vs. a local PDF parser:**
- The document is a *typed* PDF, so OCR isn't a big challenge — yet the **local parser completely loses table structure** (returns raw bytes) and **misses the QR code and selection-mark information entirely.**
- Net effect: with a local parser the agent has **incomplete information** and must guess at element structure/meaning. Content Understanding instead produces an **LLM-readable state**, then sends it to the agent via a **`to_llm_input` formatting helper** (detailed later).

### Act 2 — Multimodal pre-built analyzers + the no-code experience
Before diving back into code, the presenter shows the **no-code interface**:
- **Foundry portal → Deployments and AI services → Content Understanding playgrounds** (at the bottom).
- A set of pre-built analyzers is available. Example: the **`invoice`** analyzer extracts critical fields/values; the JSON output includes, for every text piece and value, the **offset and length** plus **bounding boxes** of where it sits in the document, so you can **trace back to a citation.**

**Audio pre-built analyzer:**
- They feed an **audio file** (crew members inspecting fiber cuts in situ). The analyzer pulls out **timestamps** and transcribed speech to send to the LLM/agent.
- *(Caption note: some sample audio snippets bleeding in — e.g., a banking "$1,000 certificate of deposit" line and "Approaching vault TV3… visuals on the conduit entry… the protective sleeve is completely off" — appear to be demo/sample clips. The relevant content: two crew members exchanging info about approaching **vault TV3**, the conduit entry, and a situation with a **crack and bent fiber**.)*

**CU Studio:**
- Reached via a button to **CU Studio**; the **Discover tab** lists pre-built models across **tax, legal, identity, payment, mortgage, etc.**

**Video search analyzer:**
- They analyze a **short inspection video clip** before sending it to the document analyzers.
- *(Caption note: a neural TTS / Cognitive Services voice promo plays as a sample — "higher fidelity… sounded a lot more like an actual human voice.")*
- The relevant clip: *"We've got a fiber strike in this excavation, but before the repair crew can work, we need to address the condition around the line first."* → the analyzer produces a **summary that can be sent to the LLM for follow-up analysis.**

**Bringing modalities together (document with embedded images):**
- They take transcripts from **audio and video** plus a **document file containing six embedded images**, and run it through the **`document search`** analyzer.
- Result: it **OCRs all detailed text**, **preserves location**, captures **text within images**, and — importantly — **generates a description of each image across all six photos**, which is sent to the agent to reason over.
- The LLM was then able to **identify a "3 cm displacement"** and, by correlating audio + document evidence, conclude the **root cause is around "TV vault 3" (vault TV3).**

### Act 3 (setup) — Custom analyzers + classifier/routing
Beyond pre-built analyzers, agents often benefit from **decision-ready fields**, and you may want to customize a field to extract insight specific to your business.
- **Custom analyzers don't only extract** — they also **reason, infer, and generate fields by calculating and reasoning.**
- Scenario: **six different document input types**; build an analyzer for each to extract only the fields of interest.
- **How to define a custom analyzer:** identify your **schema**, and for each field provide a **name** and a **definition** including **type, method, and a natural-language description.** Deploy all custom analyzers via the **SDK.**

**Classifier (called out as very useful):**
- Similarly, you **identify categories** and what they're for, to handle any unknown document that arrives.
- It can **automatically route** any unknown incoming document to an analyzer (pre-built or custom) to perform the purpose-designed extraction.
- Demo: deploy **six custom analyzers** for the six document types, create a **classifier for six categories**, and send documents one at a time through the pipeline (takes ~a minute to process).

**Pre-processed results shown:**
- For each document type, the **custom analyzer returns the custom-defined fields** — and some fields **aren't literally found in the document**; they require **reasoning and collaboration** for the LLM to generate.
- The agent can additionally **collect evidence and reason** about the next action.
- **Classification:** all **six files correctly identified** and routed to their respective analyzers.

**Midpoint recap:** Content Understanding takes multimodal content → text representations → classification/routing → pre-built or custom analyzers → extract fields *and* infer fields/insights unique to the scenario. The next two acts show how an **agent leverages all that** to diagnose root cause, identify a material plan within budget, and dispatch the next action.

### Act 3 — Four-step agent thinking (direct SDK → LLM)
A **four-step agent reasoning** flow:
1. **Assemble** all Content Understanding output gathered so far.
2. Use the **`to_llm_input`** formatter (from the SDK) to package it for the LLM.
3. Send requests to: **diagnose root cause → identify material & build plan → dispatch an action** to the repair crew.

**Expected results:**
- **Root cause analysis:** identified **mechanical failure of the shared underground conduit at vault TV3**, caused by a **micro-bend**, with full details. An **evidence chain** is attached (based on all document evidence collected along the way) plus a **final verdict.**
- **Material plan:** includes the **budget cap** (approved by named personnel) and a **materials table** to move forward with.
- **Dispatch email:** identifies **key personnel** from the raw data-collection process and sends **only the necessary information** for them to act on next.

### Act 4 — Integration with Microsoft Agent Framework
The entire process can be **orchestrated using the Content Understanding context provider within Microsoft Agent Framework.**
- A **context provider** is a **primitive in Agent Framework that hooks into the agent run loop.** It can **see/detect messages before they reach the LLM** and act on them — e.g., detect attachments, process them, and send the structured output back into the conversation loop.

**Setup:**
- Define the **context provider** with the **content endpoint + credential**, specifying the **analyzer ID.**
- Use **Agent Framework's Foundry chat client** for this scenario.
- For the agent run, construct the agent by providing **instructions** plus the **context provider = Content Understanding.**
- Build a message using a **simple prompt** + **attachments from PDFs.**

**Follow-up / caching:**
- After the first diagnosis round, they ask a **follow-up question** and show that Agent Framework can **reuse cached results** from the Content Understanding context provider — **without repeating** the analysis.

**Final output & comparison:**
- The Agent Framework path yields **very similar results to the manual SDK pipeline**, but in essentially **one step**, and the follow-up answer used the **same session + context provider with no new Content Understanding calls.**
- **SDK pipeline (Acts 1–3) vs. Agent Framework (Act 4):** *same underlying Content Understanding service, different integration shape.* Agent Framework adds:
  - **Auto-analysis on attachments**
  - **Automated/included formatting code**
  - **Multi-turn caching**
  - **One provider for any type of agent**

### Closing guidance (live-demo takeaways)
- **Start with pre-built `document search`** (or other pre-builds) when you **don't know the document type**, or when you need to send **enriched information** to your agent to reason through — e.g., **RAG and AI Search** scenarios.
- **Use custom analyzers** to pull out **specific fields** that are better *reasoned through* (e.g., **dispatch urgency, budget verdict**).
- **In production**, you'll often get payloads/documents of **unknown type** — use **classification + routing**: a **single call** classifies, routes, and extracts, minimizing branching logic in app code.
- **`to_llm_input` helper** formats output as **Markdown with YAML front matter**, supports **full document or fields-only**, and gave an **~85% token reduction** in their scenario.
- **Multiple ways to feed agents:** Agent Framework simplifies it, and **direct integrations with LangChain and Markdown** are also provided.

### Resources & next steps mentioned
- **All code** — the **demo app** and a **detailed tutorial notebook** — is available on **GitHub** for this demo session (a **QR code** was shown).
- **Attend breakout session 242** at **4:00 p.m.** the same afternoon to learn what's coming in Content Understanding, including an **"agentic mode"** for **even more complex document scenarios** and how it works with **toolboxes in Foundry.**

## 🛠️ Products / Features / Technologies Mentioned
- **Azure AI Content Understanding** — single pipeline (parse, classify, extract) turning messy multimodal content into structured Markdown + JSON with grounding, confidence scores, and governance.
- **`document search` (pre-built analyzer)** — extracts document layout + embedded elements (tables, figures, selection marks, barcodes/QR codes, signatures); great for RAG / AI Search.
- **`invoice` (pre-built analyzer)** — extracts critical fields/values with offsets, lengths, and bounding boxes for citation traceability.
- **Audio (pre-built analyzer)** — transcribes speech with timestamps for LLM/agent consumption.
- **Video / video search (pre-built analyzer)** — analyzes video clips and produces summaries for downstream LLM analysis.
- **Custom analyzers** — user-defined schema/fields; can extract *and* reason/infer/generate fields (e.g., dispatch urgency, budget verdict) via SDK deployment.
- **Classifier + routing** — categorizes unknown documents and auto-routes to the right analyzer; single call classifies + routes + extracts.
- **`to_llm_input` SDK helper** — formats Content Understanding output as Markdown + YAML front matter; full-doc or fields-only; ~85% token reduction.
- **Azure AI Foundry portal** — Deployments & AI services; hosts the Content Understanding playground.
- **Content Understanding playground** — no-code interface to try pre-built analyzers.
- **CU Studio** — Discover tab listing pre-built models (tax, legal, identity, payment, mortgage, etc.).
- **Microsoft Agent Framework** — agent orchestration; hosts the **context provider** primitive.
- **Content Understanding context provider** — Agent Framework primitive that hooks the run loop, detects/processes attachments before the LLM, and returns structured output to the conversation; supports multi-turn caching.
- **Foundry chat client** — Agent Framework chat client used in the demo.
- **GPT-4.1** — LLM used for direct-call diagnosis/reasoning in the demo.
- **LangChain** — direct integration target for Content Understanding output (alongside raw Markdown).
- **Local PDF parser** — used as a baseline comparison (lost structure, QR codes, selection marks).
- **GitHub repo (demo)** — demo app + tutorial notebook for the session (QR code shared).

## 🚀 Announcements / What's New
- **No hard GA/preview status was explicitly stated** in the transcript for Content Understanding features. Treat the following as *showcased capabilities / roadmap pointers* rather than confirmed release milestones:
  - **Content Understanding context provider for Microsoft Agent Framework** — demonstrated as a way to orchestrate the full pipeline with auto-analysis, auto-formatting, and multi-turn caching.
  - **Custom analyzers that reason/infer/generate fields** (not just extract) — demonstrated.
  - **Classification + routing in a single call** — positioned for production workloads.
  - **Direct integrations** with **LangChain** and **Markdown** — mentioned as available.
  - **Roadmap teaser:** an upcoming **"agentic mode"** for more complex document scenarios and **integration with toolboxes in Foundry** — to be covered in **breakout session 242** (4:00 p.m. same day).

## 💡 Demos
> Single continuous live demo built around the **6:47 a.m. fiber-cut incident** ("Tower Ridge Corridor," 42 customers at risk), structured as four "acts." One presenter extension failed to load mid-demo and was handled gracefully by walking the flow manually.

- **Act 1 — `document search` on a site maintenance log:** Proved Content Understanding preserves **two tables (row/column structure)**, decodes a **QR code**, and reads **selection marks (2 checked, 1 unchecked)** — whereas a **local PDF parser lost the tables, QR code, and selection marks** entirely, forcing the agent to guess.
- **Act 2 — No-code playground + multimodal analyzers:** Showed the **Foundry Content Understanding playground / CU Studio**, the **`invoice`** analyzer (fields + bounding boxes/citations), an **audio** analyzer (crew fiber-inspection clip), and a **video** analyzer (fiber-strike excavation clip). Proved breadth across modalities and the **no-code on-ramp**, plus that a **document with six embedded images** can be OCR'd, located, and **image-described per photo** — enabling the LLM to identify a **3 cm displacement** and correlate to **vault TV3**.
- **Act 3 — Custom analyzers + classifier/routing:** Deployed **six custom analyzers** + a **six-category classifier**; proved custom analyzers return **defined fields (including reasoned/inferred ones not literally in the document)** and that the classifier **correctly identified and routed all six files.**
- **Act 3 (reasoning) — Four-step agent via direct SDK → GPT-4.1:** Produced a **root-cause analysis** (mechanical failure of shared underground conduit at vault TV3, micro-bend) with an **evidence chain + verdict**, a **material plan within an approved budget cap** (materials table), and a **dispatch email** to the right personnel with only necessary info. Proved end-to-end agent decision-making from structured evidence.
- **Act 4 — Microsoft Agent Framework context provider:** Reproduced the same diagnosis/material/dispatch results in essentially **one step**, then answered a **follow-up question using cached context** with **no new Content Understanding calls.** Proved the simplified integration shape (auto-analysis, auto-formatting, multi-turn caching).

## 📊 Notable Stats / Quotes
- **~85% token reduction** in the demo scenario from using the `to_llm_input` helper (full-doc vs. fields-only formatting).
- **6:47 a.m.** alert; **signal degradation on "Tower Ridge Corridor"**; **42 customers at risk.**
- Manual baseline today: an on-call engineer must search **nine documents, media files, and attachments** and correlate everything by hand.
- **Six** document types / **six** custom analyzers / **six** classifier categories — all correctly classified and routed.
- Site maintenance log results: **2 tables, 1 QR/barcode decoded, 2 checked + 1 unchecked selection marks.**
- Document with **six embedded images** OCR'd + individually image-described; LLM identified a **3 cm displacement** and correlated root cause to **vault TV3.**
- Diagnosed root cause: **mechanical failure of the shared underground conduit at vault TV3, caused by a micro-bend.**
- Key paraphrased insight: *"They can reason, but they cannot really read"* — the core framing for why Content Understanding exists.
- Field-extraction caveat: some custom fields **aren't found in the document** and require the LLM to **reason and collaborate** to generate them.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - [ ] Clone the **session GitHub repo** (demo app + tutorial notebook) and run the four-act pipeline end to end.
  - [ ] Spin up the **Content Understanding playground / CU Studio** in the Foundry portal and run the `invoice`, audio, and video pre-built analyzers.
  - [ ] Prototype a **custom analyzer** (schema: name + type/method/natural-language description) for a real document type and test the **reason/infer/generate** field capability.
  - [ ] Build a **classifier + routing** flow for mixed/unknown document payloads and measure the reduction in branching logic.
  - [ ] Wire the **Content Understanding context provider into Microsoft Agent Framework** (Foundry chat client) and verify **multi-turn caching** on a follow-up question.
  - [ ] Benchmark the **`to_llm_input`** helper (full-doc vs. fields-only) and confirm the token-reduction claim on our own data.
  - [ ] Compare Content Understanding output vs. our current **local PDF parser** on docs with tables, QR codes, and checkboxes.
- [ ] Questions:
  - [ ] What are the **pricing / token-cost** implications of Content Understanding calls vs. the LLM savings from the 85% token reduction?
  - [ ] What are the **confidence-score thresholds** and how should agents act on low-confidence extractions?
  - [ ] How does the **context provider caching** scope/expire across sessions, and is it per-conversation or shared?
  - [ ] What's included in the upcoming **"agentic mode"** (breakout 242) and how does it differ from custom analyzers?
  - [ ] Which **modalities/file types** are GA vs. preview, and what are the size/page limits?
  - [ ] How does **governance/grounding** surface in the output (citations, bounding boxes) for compliance/audit use cases?
- [ ] Relevant to:
  - [ ] Any RAG / AI Search ingestion pipeline handling messy enterprise documents.
  - [ ] Agent projects on **Microsoft Agent Framework** that must process attachments.
  - [ ] Incident-response / operations automation involving mixed media evidence.
  - [ ] Document-heavy verticals: tax, legal, identity, payment, mortgage, insurance.

## 🔗 Related
- [Microsoft Build 2026 session 242 — Content Understanding breakout (agentic mode + Foundry toolboxes)] — *follow-up session referenced; link TBD*
- [[Azure AI Foundry]]
- [[Microsoft Agent Framework]]
- [[Azure AI Content Understanding]]
- [[RAG]] / [[Azure AI Search]]
- [YouTube — DEM331 recording](https://www.youtube.com/watch?v=b23ZV37_9Hw)
---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/fabric
  - topic/data
  - topic/governance
source: https://www.youtube.com/watch?v=px76jA-Vdmw
session_code: DEM362
event: Microsoft Build 2026
speakers: Alex (Foundry / agents & orchestration), Hannah (Microsoft Fabric / data), Raphael (Copilot & Agent 365 / governance & compliance)
duration_min: 28
aliases:
  - Building a Multi-Agent Workflow in Microsoft Fabric
---

# DEM362 — Building a Multi-Agent Workflow in Microsoft Fabric

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Alex (Azure AI Foundry — agents & orchestration), Hannah (Microsoft Fabric — data engineering & notebooks), Raphael (Microsoft 365 Copilot & Agent 365 — governance, compliance & data privacy, based in Germany)  
> **Duration:** ~28 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=px76jA-Vdmw)

## 🎯 TL;DR
This demo-heavy session shows how to stand up a **multi-agent, data-grounded workflow inside Microsoft Fabric** using the **three Microsoft "IQs"** — **Work IQ** (your daily M365 business data: mail, Teams, calendar, files), **Fabric IQ** (your enterprise/business data modelled as ontologies on top of a lakehouse), and **Foundry IQ** (a unified knowledge base spanning multiple sources). The narrative is framed around three personas — Alex (builds agents on Foundry), Hannah (engineers the Fabric data), and Raphael (owns governance/compliance) — to make the point that a production-ready AI solution needs all three: **intelligence, data, AND trust**. The core technical message is that **ontologies (graphs) in Fabric IQ** are the fastest, most accurate way to ground a **Fabric data agent**, that those agents can be consumed both *inside* Fabric (internal connection) and *outside* (published to M365 Copilot, Foundry, or Copilot Studio via MCP), and that **Agent 365 + Microsoft Purview** finally close the trust gap by giving full observability over every agent interaction. The earlier "black box" agents (Azure OpenAI Studio era, 3–4 years ago) failed to reach production because customers couldn't see or control them; the new stack fixes that.

## 🔑 Key Takeaways
- **Three IQs = three context layers.** Work IQ (M365 daily/business data), Fabric IQ (modelled business data via ontologies), Foundry IQ (a single knowledge base over many sources). They give agents *grounded* context instead of relying on the LLM's stale training data.
- **The "broken chatbot" problem is the motivation.** A bespoke knowledge base (the speaker's PhD chatbot 10 years ago) works great for in-scope questions but fails instantly the moment a question falls outside it — grounding across real enterprise sources is the fix.
- **Trust was the production blocker, not intelligence.** Agents built ~3–4 years ago on Azure OpenAI Studio (rigged to SharePoint Online + Blob Storage) demoed well but stayed in POC because they were black boxes — customers wouldn't put critical company data into something they couldn't see or control.
- **Work IQ is exposed as MCP servers.** Inside M365 Copilot it's used implicitly; from *outside* (Foundry, Copilot Studio, other resources) you connect to Work IQ MCP servers — Copilot, Teams, Calendar, **Email/Mail**, Word, Dataverse, etc.
- **Human-in-the-loop differs by surface.** From Foundry you must **explicitly approve** an agent connecting to your Work IQ Mail (it's outside M365); inside M365 Copilot the same access is pre-authorised and answers come back directly.
- **Ontologies (graphs) beat SQL for grounding.** A Fabric IQ ontology (nodes + relationships) lets the agent reason about how entities relate, retrieves more grounded context, and is faster than the older path of translating the query to SQL against the lakehouse.
- **Fabric data agents work two ways.** *Internal* — the data agent is part of Fabric, so querying from within Fabric is a direct internal connection. *External* — publish the agent (e.g. to **M365 Copilot**) and consume it elsewhere using its **workspace ID + artifact/data-agent ID**.
- **"Chat with your data" + auto-visualisation.** Once published, non-Fabric users can ask natural-language questions, convert time-zones, compute revenue, and even ask for a plot — Copilot generated **Python (matplotlib)** code and rendered the chart inline in M365 Copilot.
- **Fabric IQ data agents need SDK-based config, testing & evaluation.** You can't fully configure/test/evaluate a Fabric data agent in the portal — use the **Fabric data agent SDK** (set workspace ID, Azure OpenAI URL, temporary test token) to query, then run **agent evaluation** on critical prompts before production.
- **Fabric has no native agent orchestration — so use Microsoft Agent Framework or pipelines.** Orchestration can be done via **Copilot Studio** or **Microsoft Agent Framework** (code agent → agent calls), but to stay *natively on Fabric* the speaker orchestrates a **multi-agent workflow via Fabric pipelines + notebooks** (prep data → query data agent → enrich from Foundry IQ → send email via Foundry agent + Work IQ Mail MCP).
- **Agent 365 + Purview = the trust/observability layer.** Agents created on Foundry, Copilot Studio, Fabric, or Copilot all surface in **Agent 365**; agent activity flows into **Microsoft Purview**, where you see every interaction, **sensitive info types**, and alarms (e.g. someone querying invoice data they're not allowed to) and can hunt the user.
- **Everything ships as reusable templates.** All the demo code (data-agent notebooks, evaluation notebooks, orchestration) will be published to a **repo after Build**, anonymised, so attendees can run it on their own data.
- **Medallion architecture still underpins it.** Spark/Spark Express ingestion → **bronze/silver/gold lakehouse** → semantic model → **generate ontology** → feed the data agent.

## 📚 Detailed Notes

### Framing: agents, Fabric, and the three IQs
The session is explicitly about **agents + Fabric + the three IQs**. The speaker stresses these are three distinct context systems and uses a **three-person team metaphor** to map them:
- **Alex (the speaker on Foundry):** builds the agent, handles orchestration, coding.
- **Hannah (the middle / Fabric):** provides the data, runs the notebooks, prepares data for different use cases.
- **Raphael (Germany / governance):** owns **Copilot + Agent 365**, data privacy and compliance. The blunt point: *"You can create your data, but if the compliance guy is not on your side, you're done."* In Germany especially, data-privacy concerns can kill the whole project — so governance is a first-class pillar, not an afterthought.

The deeper message tying it together is Satya's framing of **intelligence + trust**: the intelligence has been available for years, but **trust** was missing, which is why earlier agents never went to production.

### The "broken chatbot" problem (why grounding matters)
Drawing on his **PhD ~10 years ago**, the speaker built a custom database/knowledge base for a chatbot. Users were initially happy — but the moment they asked something *outside* the knowledge base, it **failed instantly**. This is the classic "broken chatbot": great inside its scope, useless outside it. The whole modern stack exists to ground agents across **real, live enterprise data** so they don't fall off a cliff at the edge of a static KB.

### Work IQ — your daily/business M365 data, as context (and as MCP)
**Work IQ** surfaces the **daily business data in your tenant**: emails, meetings, files, chats — whatever lives in M365. Two consumption modes:
- **Inside M365 Copilot:** Work IQ is used implicitly/underneath; access to your data is already authorised, so answers come back directly.
- **Outside (Foundry, Copilot Studio, other resources):** Work IQ is exposed as **MCP servers** that can be requested from elsewhere. There are several (Work IQ **Copilot, Teams, Calendar, Email/Mail, Word, Dataverse**, …).

**Demo — Foundry IQ agent + Work IQ Mail (MCP):**
- The speaker created an **"IQ agent"** on Foundry running **GPT-5** (referred to as "GPT-5 for" in the captions — the chat model grounding the agent). Without a tool, it can only answer from the model's training knowledge; enabling **web search** adds current web data beyond the LLM's training cutoff.
- He connects **Work IQ Mail as an MCP** tool. Now the agent can query his mailbox from *Foundry* (which is **outside M365**).
- Asking it to summarise mail triggers a **human-in-the-loop approval** — because this is Foundry, not M365, you must explicitly approve the agent connecting to your work mail. (On the corporate/M365 side the same request just answers, because Copilot is pre-authorised to use your data, with Work IQ underneath.) He approves, and email summaries come back. He notes he can filter to e.g. *security emails only*.

### Copilot Studio for visibility into the agent's steps
The speaker switches to **Copilot Studio** (another place, like Foundry, where you author agents) because it gives **more insight into what's happening behind the scenes**. He can connect the same tools — **Work IQ Mail**, **Foundry agents**, **Fabric data agents** — and watch the orchestration trace:
- **Sequence observed:** Work IQ Mail initialised → **data agent** initialised → agent decides which to call.
- For *"show me, for each store, any freezer operated… and create a draft mail"*, the **freezer data lives in Fabric**. Copilot Studio shows: it searches email (Work IQ Mail MCP) → passes the data question to the **Fabric data agent (MCP)** → the data agent returns rows (raw output shows **Paris** and **Berlin**) → it then calls MCP to **create a draft email** ("Dear team, please…").
- **Point proven:** a single agent in Copilot Studio **combines data from multiple sources** — Work IQ Mail MCP + Fabric data agent MCP — and returns a synthesised result (here, a drafted email grounded in store/freezer data).

### Foundry IQ — one knowledge base over many sources
**Foundry IQ** is a **knowledge base** you build over multiple connection types: **Azure AI Search, web, SharePoint, Fabric IQ, Azure Blob Storage**. You then query the knowledge base ("I don't know where this data lives — please find it") and the agent goes and retrieves it. So far this is all achievable in a **single agent** (Work IQ + Fabric data agent + knowledge base all via MCP) — the multi-agent orchestration comes later.

### Fabric IQ and ontologies — the heart of the talk
The "new thing" the speaker is most excited about is **Fabric IQ** and its support for **ontologies**. Echoing his PhD work, he argues an **ontology (a graph of nodes + relationships)** is **the quickest, most accurate way to provide knowledge to an agent**:
- A graph lets the agent figure out that, e.g., a **sales** node relates to other nodes, so when you ask a question it can traverse those relationships instead of guessing table joins.
- **Pipeline / medallion flow:** ingest data via pipelines (**Spark / "Spark Express"**) → store on **lakehouse** → **silver** (enrich + clean) → **gold** → expose as **semantic model** or **ontology** to the data agents.
- **Real-world example — Swiss Airlines:** moved from on-prem to Fabric using **source-domain-aligned data products** on bronze/silver, **shortcut** them, built **customer-aligned data products**, then a **semantic model**, ready to feed data agents.

**Demo — Fabric data agent over an ontology (internal):**
- The ontology contains **freezers, products, sales** data. Asking *"which store is lower than 46%"* returns **Berlin and Paris** — the same answer seen earlier from Foundry, but here it's **easier/faster because the data agent is part of Fabric (internal connection)**.
- Looking at the completion trace: the query was **grounded** — it expanded into a richer, more contextual question (listing each store's freezers and recorded values) before running, giving the agent better information.
- **Ontology vs SQL:** previously (going straight to the lakehouse) the agent **translated to SQL**, which works but **takes more time**. The speaker's long-held view (from the 10-year-old chatbots that never used SQL) is that a **graph/ontology underneath** is the better path. ("HANA"/"Hana" in the captions is a caption garble — read it as the data-agent answer/engine, not SAP HANA.)

### Publishing a Fabric data agent for external use
To use the data agent **outside** Fabric you must **publish** it:
- Publish target includes **Microsoft 365 Copilot** (must be explicitly selected — it isn't auto-selected). Click next, and the data agent shows up in M365 Copilot.
- **"Chat with your data" in M365 Copilot:** someone *not* familiar with Fabric (Raphael, or Alex from Foundry) can now query it naturally — "give me the second [value] per store" (Paris, Berlin), **convert timestamps to my time zone**, **revenue per store**, *"tell me about the data stored"* (it surfaces telemetry data, storing data, etc.).
- **Inline visualisation:** ask it to **define a window and plot** the data — Copilot **wrote Python (matplotlib) code** and rendered the chart **directly inside M365 Copilot**, turning bare numbers into a picture on demand.
- **Publishing to Foundry:** alternatively publish to get the **workspace ID + data agent (artifact) ID**, then in Foundry add it as a **data agent** using a new or existing connection + workspace ID + artifact ID — then you can query the data agent's data from Foundry.

### Enabling and building ontologies
- **Admin prerequisite:** in the **admin portal** you must enable two items — the **ontology items** and the **graph preview** — before you can create ontologies.
- **Build path:** from the **lakehouse → create the semantic model → confirm it → "generate ontology"**. After a few minutes the ontology exists.
- In the ontology view, for e.g. **products** you see **properties** and **connections/relationships**. Unlike raw SQL (where you might see a 1-to-many FK but not know what it *means*), you can **specify the semantic relationship** — his memorable example: *"Alex is speaking right now at the conference; there are many speakers but only one conference,"* i.e. you can name the relation explicitly so agents reason correctly. You can also add new entities and even attach **another model to predict from stocks**.

### Fabric IQ data agents: SDK config, testing & evaluation
A key limitation: a **data agent in the cells/portal** can be created but **not fully configured, tested, or evaluated in the portal**. To close that gap, use the **Fabric data agent SDK**:
- Configure: **workspace ID**, **Azure OpenAI URL**, **temporary test token**; set up Azure OpenAI; then **query the data agent from notebooks** in code.
- After SDK setup, **connect and run evaluation** — *the data agent should be evaluated by you, not by end users in production*. Create an evaluation **run on evaluation data**, define **critical prompts**, run **agent evaluation**, retrieve the summary, store, and **visualise** results.
- Rationale: in production you **must know what your data agent is doing** — you can't just deploy and wait for end users to report "it doesn't work."
- **All this code (data-agent notebooks + evaluation notebooks) ships to a public repo after Build**, anonymised, runnable on your own data.

### Multi-agent orchestration on Fabric (the title payoff)
Crucial caveat: **Fabric has no native agent orchestration**. Your options:
- **Copilot Studio** — create the orchestration there, or
- **Microsoft Agent Framework** — code the agents and orchestrate (agent A finishes → calls agent B → workflow), but that's *off* Fabric.
- **To stay natively on Fabric**, the speaker orchestrates via **Fabric pipelines + a chain of notebooks** (all to be in the repo). The notebooks: **prepare the data → produce a summary → ask the data agents for information → call Foundry IQ to enrich the data** (you can call out to whatever you need). This mirrors Microsoft Agent Framework's pattern (one agent triggers the next) but **keeps the whole workflow inside Fabric**.
- **Closing the loop / output:** at the end it can pull from **Blob Storage** (or another source), then **connect to Foundry agents** and use the **Work IQ Mail MCP** to **send the result as an email**. So the multi-agent workflow combines and enriches data across sources and finishes with an action (email).
- The notebooks are delivered **as templates** — e.g. for calling **Azure data agents** you set the **payload**, handle the **run authorization**, then call the data agent from a notebook in code, and feed results into **evaluation/running on Foundry**.

### Agent 365 + Purview — the trust & observability finale
The last pillar — and the answer to the old "black box" failure — is **Agent 365**:
- Agents authored on **Foundry, Copilot Studio, Fabric, and Microsoft Copilot** all become **visible in Agent 365**, including **data agents**. You can see what information each agent produces and which user triggered it.
- **Agent activity flows into Microsoft Purview.** From an agent's activity you drill into Purview and see **all interactions** across **different apps** (data agent, M365 Copilot, M365 app, …).
- Critically, Purview surfaces **sensitive info types** and **alarms**: if something goes wrong — e.g. someone asks a data agent about an **invoice they're not allowed to see** — it shows up as an **alarm**, and you can **hunt that user** and investigate.
- This is the trust layer that makes the difference between a slick POC and a **production** deployment: full insight into "what is happening on your side."

### Throughline
The recurring theme: agents have been intelligent for years, but **production requires trust = visibility + control + governance + evaluation**. The 2026 stack (three IQs for grounding, ontologies for accurate/fast knowledge, SDK-based evaluation, pipeline/Agent-Framework orchestration, and Agent 365/Purview for observability) is the speaker's argument that the "puzzle is now complete."

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Fabric** — the unified data platform that is the home base for the whole workflow; data agents run as part of Fabric (internal connections).
- **Fabric IQ** — Fabric's intelligence/knowledge layer; introduces **ontologies (graphs)** over business data to ground agents.
- **Ontology / graph (in Fabric IQ)** — nodes + named relationships modelling business data; fastest/most accurate grounding for agents vs SQL.
- **Fabric data agent** — agent that answers questions over Fabric data (ontology or lakehouse); usable internally or published externally.
- **Fabric data agent SDK** — programmatic config/query/test of data agents from notebooks (workspace ID, Azure OpenAI URL, test token); enables agent evaluation.
- **Lakehouse / medallion (bronze → silver → gold)** — storage + refinement layers feeding semantic models/ontologies.
- **Spark / "Spark Express"** — ingestion/compute for pipelines in Fabric (caption term — read as Fabric Spark).
- **Semantic model** — built from the lakehouse; the basis from which an ontology is "generated."
- **Fabric pipelines + notebooks** — used to orchestrate the multi-agent workflow natively on Fabric.
- **Work IQ** — context layer over M365 daily/business data (mail, meetings, files, chats); exposed as MCP servers externally.
- **Work IQ MCP servers** — Copilot, Teams, Calendar, **Email/Mail**, Word, Dataverse, etc. — connect to your M365 data from outside M365.
- **Foundry IQ** — a single knowledge base over many sources (Azure AI Search, web, SharePoint, Fabric IQ, Azure Blob Storage).
- **Azure AI Foundry ("Foundry")** — where Alex builds/orchestrates agents; can consume Work IQ Mail (MCP) and Fabric data agents.
- **Microsoft Copilot Studio** — alternative agent-authoring + **orchestration** surface; gives step-by-step visibility into tool calls.
- **Microsoft 365 Copilot** — consumes published Fabric data agents; "chat with your data," timezone conversion, revenue queries, inline plotting.
- **GPT-5** — the chat model grounding the demo Foundry agent ("GPT-5 for" in captions).
- **Web search (agent tool)** — adds current web data beyond the LLM's training cutoff.
- **Microsoft Agent Framework** — code-first multi-agent orchestration (agent → agent calls); alternative to Fabric pipelines/Copilot Studio.
- **Microsoft Agent Framework agent evaluation** — running critical prompts against the agent to validate before production.
- **Agent 365** — single pane showing all agents (Foundry/Copilot Studio/Fabric/Copilot) and their activity; the production governance gateway.
- **Microsoft Purview** — receives agent activity; shows interactions, **sensitive info types**, alarms, and user hunting.
- **Azure OpenAI** — used in SDK config (Azure OpenAI URL + token) to power data-agent queries.
- **Azure Blob Storage** — a data source (and example output source) in the workflow.
- **Azure AI Search** — a Foundry IQ knowledge-base connection type.
- **SharePoint Online** — a knowledge/data source (also used in the older Azure OpenAI Studio agents).
- **Dataverse / Teams / Calendar / Word** — additional Work IQ MCP-connectable data surfaces.
- **matplotlib (Python)** — the library Copilot auto-generated code with to plot data inline in M365 Copilot.
- **Azure OpenAI Studio (formerly Azure AI / "Azure Open AI Studio")** — the ~3–4-years-ago tooling where the speaker built the earlier "black box" agents (historical contrast).

## 🚀 Announcements / What's New
- **Work IQ surfaced as MCP and live in the demo tenant** — the speaker repeatedly notes the green "new" Work IQ status he'd "never seen until today," up and running. Presented as new/emerging functionality (preview-stage feel; **explicit GA/preview status not st
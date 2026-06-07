---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/search
  - topic/conversational-ai
  - topic/rag
  - topic/agents
  - topic/elastic
  - topic/azure
source: https://www.youtube.com/watch?v=avlMmJZUPuU
session_code: ODSP922
event: Microsoft Build 2026
speakers: Greg Khrist (Cloud Ecosystem Architect, Elastic), Jonathan Simon (Senior Product Marketing Engineer, Elastic)
duration_min: 25
aliases:
  - Develop a conversational search experience without rebuilding your app
---

# ODSP922 — Develop a conversational search experience without rebuilding your app

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Greg Khrist (Cloud Ecosystem Architect, Elastic) · Jonathan Simon (Senior Product Marketing Engineer, Elastic)  
> **Duration:** ~25 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=avlMmJZUPuU)

## 🎯 TL;DR
This Elastic-partner session shows how to upgrade an existing app from traditional search to a conversational, agentic AI search experience **without re-architecting the application**. Using **Elastic Agent Builder** (now generally available) plus a model deployed in **Microsoft Foundry**, Jonathan Simon takes a fictitious camping-gear e-commerce site ("Wayfinder Supply Company") that already has lexical/hybrid search and adds an AI-powered "trip planner" concierge agent. The walkthrough demonstrates wiring in a third-party LLM via an Azure connector, building a workflow → MCP tool → agent chain, grounding answers in your own product catalog and CRM data, and dropping the resulting agent back into the React/FastAPI app with only an API call. The core message: every tool and agent you build in Agent Builder is exposed as an MCP tool / REST API, so adding conversational search to an existing app is an integration job, not a rebuild. Elastic is available on the Azure Marketplace (deployed, managed, billed through Microsoft) for a frictionless zero-to-production path.

## 🔑 Key Takeaways
- **You don't rebuild the app** — the existing Wayfinder site keeps its React front end and Python/FastAPI back end; the conversational agent is added by calling a new API endpoint, not by re-architecting.
- **Elastic Agent Builder is now Generally Available** (it was in technical preview previously) and is therefore supported for production workloads.
- **Models are the engine, your data is the fuel** — Greg's framing: "a model without the right context, without the right data, is just a very expensive auto complete." Elastic supplies the grounding/context-engineering layer; Microsoft Foundry supplies the models.
- **Elastic ships three solutions on one platform**: Search, Observability, and Security — all fed by bringing your own data into Elastic.
- **Elastic Search now spans three retrieval modes**: lexical (exact-match), semantic (vector-based), and **agentic** (AI agents built with Agent Builder).
- **Procurement is frictionless** — Elastic is natively on the Azure Marketplace ("Elastic serverless"), deployed/managed/billed through Microsoft, so no separate vendor relationship or procurement motion.
- **Everything you build in Agent Builder is an MCP tool** — with an API key, any external app can call your workflows, tools, and agents; agent operations are also accessible via REST API.
- **Workflows are the building block**: versioned, typed-input, multi-step units that can call external MCP servers via HTTP POST, with per-step on-failure handlers (retries + delays) and console logging.
- **The tool chain is layered**: Workflow → Tool (workflow/ESQL/index-search/MCP types) → Agent (instructions + assigned tools) → integrated back into your app.
- **Hybrid search solves vocabulary mismatch** — a lexical search for "coats" returns nothing (no product uses that word), but hybrid (vector) search correctly returns jackets because the catalog text was run through Elastic's inference service into a vector database.
- **Agent reasoning is transparent** — both Agent Builder's UI and the integrated web app surface a live "thinking/reasoning" trace showing each tool call (weather, clickstream, product searches) as the agent works.
- **LLM choice is flexible and pre-wired** — Agent Builder ships pre-configured connectors (Anthropic by default, plus many others); you can add any model via a "create connector" flow (e.g. an Azure/Foundry-deployed Mistral Large 3).
- **Bring-your-own-model via Foundry is fast** — deploying Mistral Large from the Foundry catalog and wiring its target URI + API key into an Elastic connector took only a couple of minutes on stage.
- **The agent can write your integration code** — you can ask the agent in-chat to "generate an example Python API call" to itself, producing starter code (requests import, URL, API key, prompt, query, print response).
- **Grounded answers blend multiple data sources** — the trip-planner agent fuses product catalog (semantic search), user clickstream/affinity (ESQL), live weather/road safety (MCP workflow), and CRM customer profile (MCP workflow) into one recommendation.
- **Free on-ramps exist** — Agent Builder docs, a public GitHub repo for the Wayfinder app (with README), a free no-install workshop, and a QR code for a 7-day free Elastic-on-Azure trial.

## 📚 Detailed Notes

### The setup: two fast-moving ecosystems meeting
Greg Khrist (Cloud Ecosystem Architect, Elastic) opens by framing the demo as sitting at the intersection of two things moving fast: the **Microsoft AI ecosystem** (Azure OpenAI and **Foundry IQ**, giving developers a powerful environment to discover, evaluate, and deploy LLMs) and **Elastic's ability to bring your own data into the AI conversation**. His central thesis: a powerful model is necessary but not sufficient — *"a model without the right context, without the right data, is just a very expensive auto complete."* The value Elastic adds is grounding answers in *your* data so the model produces "grounded, relevant, trustworthy AI answers… powered by your data and not just the model's training data."

### Why Azure Marketplace matters (the procurement story)
Greg stresses the commercial/operational friction Elastic removes. Elastic is **natively available on the Azure Marketplace** — deployed, managed, and **billed through your Microsoft Marketplace**. The benefits he calls out:
- Go from **zero to production-grade AI search** without leaving the Azure ecosystem.
- **No separate procurement motion.**
- **No additional vendor relationships to manage.**
- "Elastic on Azure the way Azure customers expect things to work."

When you pair Elastic with the models you're already exploring in the **Microsoft Foundry model catalog** (Azure OpenAI or others), you get grounded, trustworthy answers. This is the "best of Microsoft's AI platform + Elastic's context engineering and search retrieval" pitch.

### What the demo will cover (Jonathan's agenda)
Jonathan Simon (Senior Product Marketing Engineer, Elastic) lays out the path:
1. Quick overview of Elastic's solutions.
2. Introduce Agent Builder.
3. Demo a fictitious e-commerce site — **Wayfinder Supply Company** (camping gear).
4. Tour Elastic Agent Builder.
5. Build a **workflow**.
6. Build an **MCP tool** from that workflow.
7. Build an **agent** that uses the tool.
8. Integrate the agent back into the Wayfinder web app.
9. Walk through the Wayfinder architecture.

### Elastic's three solutions (one platform)
Elastic offers **Search, Observability, and Security**, all powered by bringing your data into the platform:
- **Search** — bring any data into Elastic for "blazing fast" **lexical exact-match** search, **semantic** (vector-based) search, and now **agentic** search powered by AI agents built with Agent Builder.
- **Observability** — bring your logs in; Elastic uses AI to **parse and partition logs into a structured format**, enabling application performance monitoring (APM), metrics, and instant visibility into running apps.
- **Security** — for protecting systems, monitoring endpoints, or running a SOC; features include **attack discovery** and **automatic remediation via workflows** to stay ahead of modern threats.

**Getting started on Azure:** log in to Azure → Microsoft Marketplace → search **"Elastic serverless"** → the three solutions appear → click **Get it now** → a full-featured Elastic project is created.

### The GA announcement: Elastic Agent Builder
Jonathan announces that **Elastic Agent Builder**, after being in **technical preview** "for a while," is now **officially Generally Available** — meaning it's ready for **production workloads**. He says the best way to explain it is to show it, and moves into the demo.

### Demo part 1 — The starting point: a normal e-commerce site
The Wayfinder site sells camping gear. All products, descriptions, and titles were **generated with generative AI**, and search is powered by Elastic. Standard e-commerce behaviour works: browse gear, click an item to see images/details/title, add to cart. The search box offers three modes already present: **chat-based search, hybrid search, and lexical search**.

**Vocabulary-mismatch demonstration (the key "why hybrid" moment):**
- Typing **"jackets"** → a clean list of jackets (lexical match works).
- Typing **"coats"** → **no results**, because **no product contains the word "coat"/"coats"** in its title or description.
- Switching to **hybrid search** for "coats" → jackets are returned. Why? The titles and descriptions were run through the **Elastic inference service** to create vectors stored in a **vector database**; hybrid search therefore knows "coats" are semantically similar to "jackets" and returns the right results.

### Demo part 2 — The gap: an agent that doesn't exist yet
Jonathan raises the bar: what if users could ask a sophisticated, natural-language question to an **AI-powered trip planner**, e.g. *"Plan a 3-day backpacking trip to Yosemite next weekend"*? Running it returns an error — **"trip planner agent is not built yet."** That's the hook: the rest of the session builds that agent in Elastic Agent Builder.

### Demo part 3 — Agent Builder out of the box
The Agent Builder interface already has, with **zero configuration on install**:
- An **enabled agent**.
- A pre-configured **LLM** the agent can use (currently **Anthropic**), with a dropdown of many other **pre-configured LLMs** available by default.

**Adding a model that isn't in the list:**
- Click **Manage** → see all pre-configured LLMs → **Create connector** → search **"Azure"** → select Azure.
- You now need somewhere to find/deploy/run the model — **Microsoft Foundry running in Azure**.

### Demo part 4 — Deploying a model in Microsoft Foundry and wiring it in
In Microsoft Foundry, no models are deployed initially. Steps shown:
1. **Deploy base model** → large catalog of models appears.
2. Select **Mistral Large** (specifically deploys "Mistral large"), use **default settings**, deploy — *"that was pretty fast."*
3. Go to the deployment's **Details** → copy the **target URI**.
4. Back in the Elastic connector settings → paste the URI.
5. Return to Foundry → grab the **API key** → enter it for authentication.
6. Name the connector **"Mistral Large 3"** → **Save and test**.
7. Settings save; a test interface runs a **"hello world" prompt** → **test successful**.
8. Back in Agent Builder's LLM selector → **Mistral Large 3** now appears as a selectable model.

Takeaway he states: *"right out of the box, Agent Builder is a great place for you to try out agents with LLMs and your own data."*

### Demo part 5 — Building the workflow (get customer profile)
The first building block for the trip planner is a **workflow**. Jonathan opens Workflows (a few already exist), creates a new one, and pastes a pre-saved definition from **Visual Studio Code**. Walking through the workflow elements:
- **version** — workflows are versioned.
- **name** — `get customer profile`.
- **input** — takes a `userId` input of type **string**.
- **trigger** — this one is **triggered manually** (other trigger types exist).
- **steps** — one or more; this has a single step, **`call CRM MCP`**, which does an **HTTP POST to an external MCP server** to fetch the customer profile.
- **on-failure handler** — each step can define failure handling; here it **retries twice** with a **1-second delay** between attempts.
- **logging** — workflows can **log their output**; this logs the profile to the console (`log profile to the console`).

**Running it:** save → run → prompted for the `userId` value → enters `user member` (caption-garbled; the input is the user identifier) → run → **successful**. The response shows the **log profile output** in a readable format: customer **Alex Heiker** (caption renders it both "Heiker"/"Hiker"), his **loyalty tier**, **lifetime purchases**, **lifetime value**, and **purchase history**. The workflow works.

### Demo part 6 — Turning the workflow into a tool
Next, create a **tool** that uses the workflow. Path: Agent Builder → **More** menu → **View all tools** → **New tool**. Tool types available:
- **ESQL tool** — uses **Elastic Search Query Language** (similar to SQL but "even more powerful").
- **Index Search tool** — straight search against an Elastic index.
- **Workflow tool** — wraps a workflow (the type used here).
- **MCP tool** — **currently in tech preview**; lets you **chain tools together** to create a complex workflow.

Steps: select **Workflow** type → pick the **Get Customer Profile** workflow → give a **tool ID** (copied from VS Code: `tool workflow get customer profile`) → paste the **description** → **Save and test**. Because the underlying workflow needs a `userId`, the tool's test flyout asks for the same input; entering the user identifier and submitting returns the same **Alex Heiker** profile (loyalty tier, lifetime value, purchase history). 

**Critical reusability point:** *"any tool that you create in Agent Builder, it's officially an MCP tool. So with an API key, you can access that tool from any other application that you're building."*

### Demo part 7 — Building the agent
Create an agent: Agents → **More** → **View all agents** → **New agent**. Values are copied from VS Code:
- **agent ID** → named the **trip planner agent**.
- **customer/custom instructions** — a **markdown** block specifying exactly how the agent should behave: search the product catalog, generate a trip plan, which areas to search for trip plans, and additional details.
- **display name** and **description**.

**Assigning tools:** open the **Tools** tab → sort by ID → enable the newly created **`tool workflow get customer profile`** tool plus **three other tools** (total of four). Then **Save and chat**, which drops you into Agent Builder with the trip planner agent selected for quick testing (you can switch agents via a dropdown).

### Demo part 8 — Running the agent and the reasoning trace
Test prompt: *"Plan a 3-day backpacking trip to Yosemite this weekend."* Run it. A standout feature: Agent Builder shows a **summary of what it's thinking/reasoning**, expandable to see exact steps. The observed reasoning chain:
- Knows "this weekend" is **March 13th–15th**.
- Gets **weather conditions** for those dates and **road alerts**.
- Runs an **ESQL query** for the user's **past clickstream**.
- Searches for **waterproof tents**, then **rain jackets**, then gets **more tent details**.
- Searches **sleeping bags suitable for the expected temperatures**, gets **more sleeping-bag details**.

Result ("Voilà"): a **backpacking trip itinerary to Yosemite** with a **trip overview**, **weather conditions**, **product recommendations** matched to the trip's conditions/timing, and a **suggested 3-day itinerary**.

### Demo part 9 — Agent operations via API + self-generated code
Beyond the chat UI, **all agent functions are accessible via API**, making integration into existing apps easy. Jonathan demonstrates a clever trick: instead of (or in addition to) reading the agent API docs, you can **ask the agent to write the integration code**: *"Hey, generate an example Python API call to the trip planner agent with the prompt that we ran before."* It returns **simple Python**: imports the `requests` library, sets the **URL** to reach the agent, notes you'll need an **API key**, includes the **prompt**, performs the **query**, and **prints the response**. The point: you can collaborate with the agent to generate starter code for integrating it into your apps.

### Demo part 10 — Integrating back into the Wayfinder web app
With the agent built, integrate it back into Wayfinder. The app is written so that **if the trip planner agent is available, it works; if not, it shows the "not yet implemented" error** from earlier. After refreshing: click **Trip planner** → choose a suggested prompt → "this weekend" → run. It works. Like the Agent Builder UI, the web app also **surfaces the reasoning** (expandable): planning the Yosemite trip, **getting the customer profile**, searching for **waterproof rain gear** by temperature, **sleeping bags** for expected temps, **backpacks**, and **tents**. 

The integrated result shows: a **3-day Yosemite backpacking trip plan**, **weather conditions**, **recommended gear**, and — in a side pane — **all recommended gear with one-click "add to cart" buttons**, plus a way to **view/print the itinerary** to bring on the trip. Summary of the journey: *"We went from an e-commerce site that had chat, hybrid, and lexical search to using Agent Builder to build an agent that powered a concierge-type trip planner with product recommendations… tied to an LLM that's running on Microsoft Foundry."*

### The architecture (Wayfinder web app tour)
Top-to-bottom data flow:
1. **Front end** — written in **React**. User submits a query (e.g. "plan my trip to Yosemite").
2. That sends an **HTTP request** to the **back end** — **Python running a FastAPI server**.
3. The Python back end makes an **API query to the Elastic stack** running the **trip planner agent**.
4. The Agent Builder agent has access to **four tools**:
   - **product search** — **semantic search** against the product catalog.
   - **get user affinity** — an **ESQL query** against the user's data (clickstream/affinity).
   - **check trip safety** — runs a **workflow** that does an **HTTP POST to an MCP server** for **weather information**.
   - **get customer profile** (the one built live) — runs the **get customer profile** workflow → **HTTP POST to an external MCP server** that **queries a CRM service**.

All four tools together produce the trip planner experience. The architecture cleanly illustrates the layered pattern: front end → API → Elastic agent → (semantic search tools + ESQL tools + workflow-backed MCP tools → external services).

### Resources & on-ramps
Jonathan closes with starter resources:
- **Agent Builder documentation.**
- **GitHub repo** for the **Wayfinder Supply web app** — all the code to run it on your own machine, with a detailed **README** explaining how everything works.
- A **free, no-install workshop** to try it yourself.
- A **QR code** to get **Elastic running on Azure free for 7 days**.

Greg wraps up, inviting attendees to visit Elastic at **Microsoft Build Conference 2026** and scan a QR code to learn more.

## 🛠️ Products / Features / Technologies Mentioned
- **Elastic Agent Builder** — the headline tool; build workflows, tools, and agents to add agentic AI search to apps. **Now GA.**
- **Elastic Search** — search solution with lexical (exact-match), semantic (vector), and agentic retrieval.
- **Elastic Observability** — APM, metrics, and AI-driven log parsing/partitioning into structured format.
- **Elastic Security** — endpoint/SOC protection with attack discovery and automatic remediation via workflows.
- **Elastic inference service** — generates vectors from text (titles/descriptions) for semantic/hybrid search.
- **Elastic vector database** — stores the embeddings that power hybrid/semantic search.
- **ESQL (Elastic Search Query Language)** — SQL-like but more powerful query language; one of the tool types and used for user-affinity/clickstream queries.
- **Elastic Workflows** — versioned, typed-input, multi-step units with on-failure handlers (retries/delays) and logging; can call external MCP servers via HTTP POST.
- **Elastic serverless (Azure Marketplace listing)** — search term in Microsoft Marketplace that surfaces the three solutions; one-click "Get it now" provisions a full Elastic project.
- **MCP (Model Context Protocol) tools/servers** — every Agent Builder tool is exposed as an MCP tool; workflows POST to external MCP servers (CRM, weather); an MCP tool type (tech preview) chains tools.
- **Microsoft Foundry** — Azure environment to discover/deploy/run models from a large catalog; used to deploy the LLM.
- **Foundry IQ** — referenced as part of Microsoft's LLM discovery/evaluation/deployment environment.
- **Microsoft Foundry model catalog** — the catalog of deployable models (Azure OpenAI and others).
- **Azure OpenAI** — example model source within Foundry.
- **Mistral Large (deployed as "Mistral Large 3" connector)** — the specific model deployed in Foundry and wired into Elastic via an Azure connector.
- **Anthropic** — the default pre-configured LLM in Agent Builder.
- **Azure Marketplace / Microsoft Marketplace** — deployment, management, and billing channel for Elastic.
- **React** — Wayfinder web app front end.
- **Python + FastAPI** — Wayfinder web app back end.
- **Visual Studio Code** — used to store/copy workflow, tool, and agent definitions during the demo.
- **Wayfinder Supply Company app** — fictitious camping-gear e-commerce demo app (open-sourced on GitHub).
- **Tool types in Agent Builder** — ESQL tool, Index Search tool, Workflow tool, MCP tool (tech preview).
- **Agent tools used by the trip planner** — product search, get user affinity, check trip safety, get customer profile.

## 🚀 Announcements / What's New
- **Elastic Agent Builder is now Generally Available (GA).** Previously in **technical preview** "for a while"; Jonathan explicitly announces it is now officially GA and ready for **production workloads**. This is the session's primary announcement.
- **MCP tool type is in technical preview** — the Agent Builder tool type that lets you **chain tools together** into complex workflows is called out as currently tech preview (the Workflow/ESQL/Index Search tool types are not flagged as preview).
- **Elastic is natively available on the Azure Marketplace** ("Elastic serverless"), deployed, managed, and billed through Microsoft Marketplace — positioned as a current capability rather than a brand-new announcement.
- No other GA/preview status changes were stated. Foundry, Foundry IQ, Azure OpenAI, and the specific models (e.g. Mistral Large) are referenced as existing Microsoft platform capabilities, not new releases announced here.

## 💡 Demos
The session is essentially one continuous end-to-end live demo, broken into stages:
- **Wayfinder e-commerce baseline** — browsing camping gear, viewing product details, add-to-cart; three existing search modes (chat, hybrid, lexical). *Proves:* the app already works with conventional Elastic search before any AI agent is added.
- **Lexical vs hybrid search ("coats" vs "jackets")** — lexical "coats" returns nothing; hybrid "coats" returns jackets via vectors from the Elastic inference service. *Proves:* semantic/vector search overcomes vocabulary mismatch that exact-match search cannot.
- **The missing trip-planner agent** — natural-language trip request errors with "agent not built yet." *Proves:* the gap the rest of the demo fills; sets up the "add it without rebuilding" narrative.
- **Adding a model via Foundry** — deploy Mistral Large in Microsoft Foundry, copy target URI + API key into an Elastic Azure connector, hello-world test passes, model appears in Agent Builder. *Proves:* bring-your-own-model integration is fast (a couple of minutes) and any catalog model can power the agent.
- **Building a workflow (get customer profile)** — paste workflow YAML/definition, run with a user ID, get back Alex Heiker's CRM profile (loyalty tier, lifetime value, purchase history) via HTTP POST to an MCP server. *Proves:* workflows can call external systems with retries/logging and are the reusable unit of work.
- **Workflow → tool → agent chain** — wrap the workflow as an MCP tool, then create the trip planner agent with markdown instructions and four assigned tools. *Proves:* the layered composition model and that every tool is reusable/MCP-exposed.
- **Running the agent with a visible reasoning trace** — "Plan a 3-day backpacking trip to Yosemite this weekend" produces a multi-step reasoning chain (weather, road alerts, clickstream ESQL, tents, rain jackets, sleeping bags) and a full itinerary with weather + product recommendations. *Proves:* the agent orchestrates multiple tools/data sources transparently.
- **Self-generated integration code** — asking the agent to write an example Python API call to itself produces working starter code. *Proves:* integration friction is low; the agent helps you wire it in.
- **Integrated Wayfinder trip planner** — the same experience now works inside the React/FastAPI app, with reasoning trace, recommended-gear pane with add-to-cart buttons, and a printable itinerary. *Proves:* the agent slots into the existing app via an API call — no rebuild.
- **Architecture walkthrough** — React front end → FastAPI back end → Elastic agent with four tools (product search/semantic, get user affinity/ESQL, check trip safety/weather MCP workflow, get customer profile/CRM MCP workflow). *Proves:* the clean separation enabling "no rebuild" integration.

## 📊 Notable Stats / Quotes
- **"A model without the right context, without the right data, is just a very expensive auto complete."** — Greg Khrist, framing why grounding/your-data matters (the session's signature line).
- **Three Elastic solutions:** Search, Observability, Security — on one platform fed by your data.
- **Three search modes** in Elastic Search: lexical (exact-match), semantic (vector), agentic (Agent Builder agents).
- **Four tools** power the trip-planner agent: product search, get user affinity, check trip safety, get customer profile.
- **Retry policy demoed:** on-failure handler retries **twice** with a **1-second delay** between attempts.
- **"This weekend" resolved to March 13th–15th** by the agent for the Yosemite itinerary.
- **7-day free trial** of Elastic on Azure (via QR code).
- **"Zero to production-grade AI search deployment without leaving the Azure ecosystem"** — Greg, on the Azure Marketplace path.
- Customer profile returned in demo: **Alex Heiker** — with loyalty tier, lifetime purchases, lifetime value, and purchase history.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Clone the **Wayfinder Supply** GitHub repo and run it locally (React front end + Python/FastAPI back end) to study the agent integration pattern end-to-end.
  - Run the **free no-install workshop** to build a workflow → MCP tool → agent without provisioning anything.
  - Spin up **Elastic on Azure** via the Marketplace ("Elastic serverless") using the **7-day free trial**; confirm the one-click "Get it now" provisioning.
  - Deploy a model in **Microsoft Foundry** (e.g. Mistral Large or an Azure OpenAI model) and wire it into Agent Builder via the **Azure connector** (target URI + API key).
  - Build a **Workflow tool** and a couple of **ESQL tools**, then compose an agent; test the live **reasoning trace**.
  - Exercise an agent purely via its **REST/MCP API** with an API key — replicate the self-generated Python `requests` snippet against my own agent.
- [ ] Questions:
  - Where exactly does **hybrid search** combine lexical + vector scores (RRF? linear)? The talk shows the behaviour but not the ranking algorithm.
  - What are the **pricing/billing** mechanics when Elastic is billed through Azure Marketplace vs. inference costs for the embeddings + LLM calls?
  - For the **MCP tool type (tech preview)** — what's the GA timeline, and how does tool-chaining differ from a multi-step workflow?
  - How are **secrets/API keys** for external MCP servers (CRM, weather) and the Foundry connector stored/rotated in Elastic?
  - What are the **latency and cost** characteristics of an agentic query (multiple tool calls + LLM reasoning) vs. plain hybrid search at e-commerce scale?
  - Does the agent's **reasoning trace** surface to end users by default, and is it safe/desirable to expose in production?
- [ ] Relevant to:
  - Any team with an **existing search-backed app** wanting to add natural-language/conversational search without re-architecting.
  - E-commerce / catalog search, support/knowledge search, and internal enterprise search use cases needing **RAG-style grounding** on proprietary data.
  - Azure-centric orgs wanting **frictionless procurement** (Marketplace billing) and **Foundry-hosted models** paired with a retrieval/context layer.
  - Architects evaluating **MCP-based tool composition** and agent-as-API integration patterns.

## 🔗 Related
- [[Elastic Agent Builder]]
- [[Microsoft Foundry]]
- [[Model Context Protocol (MCP)]]
- [[Hybrid Search & Vector Embeddings]]
- [[RAG - Retrieval Augmented Generation]]
- [[Azure Marketplace - SaaS procurement]]
- [[Conversational & Agentic Search]]
- Source list: [[2026 Build Session List]]

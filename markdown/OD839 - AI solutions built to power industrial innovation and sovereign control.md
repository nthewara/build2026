---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/sovereign-ai
  - topic/industrial
  - topic/edge
  - topic/ai
source: https://www.youtube.com/watch?v=8Y7IIw6jlSM
session_code: OD839
event: Microsoft Build 2026
speakers: Inbal Segev (Principal Product Manager, Microsoft)
duration_min: 27
aliases:
  - AI solutions built to power industrial innovation and sovereign control
---

# OD839 — AI solutions built to power industrial innovation and sovereign control

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Inbal Segev — Principal Product Manager, Microsoft (focused on AI that runs locally)  
> **Duration:** ~27 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=8Y7IIw6jlSM)

## 🎯 TL;DR
This session introduces **Foundry Local running on Azure Local** — Microsoft's stack for bringing the full Foundry agentic AI capability (models, inferencing, RAG, tools, agents) into customer-owned, on-premises, and **fully disconnected / air-gapped** environments. The driver is *sovereign AI* — control over data, models, and operations, not merely data location — for customers facing geopolitical, regulatory, and resilience constraints (public safety command centres, energy/utilities, critical infrastructure) where AI must keep running even when the network goes down. The headline is a **public preview** spanning three pillars: (1) **models** — Foundry Local model catalog + inferencing now scaling from single-node to **multi-node** with two consumption modes (model-as-a-platform vs Microsoft-managed model-as-a-service for frontier/partner models); (2) **knowledge** — a refreshed **local agentic RAG** offering that can now take action; and (3) **tools/agents** — custom and out-of-the-box MCPs, solution templates for a local chat UI and a **video agent**, all running on Arc-enabled Kubernetes across Azure Local form factors. Everything runs locally with no cloud calls, secured with the same Entra ID / TLS governance customers already use.

## 🔑 Key Takeaways
- We are in a **once-in-a-generation platform shift from applications to agentic AI as the operating layer**; cited analyst data: **1.3 billion AI agents by 2028** and **82% of organizations adopting agents within three years**, moving from pilots to core workforce.
- Customer requirements here are **hard constraints, not design preferences**: geopolitical risk, regulatory control, operating through outages, and adopting AI *without giving up sovereignty*. "AI strategy has to work when things break" — not just on a healthy cloud.
- **Sovereign AI = control, not just location.** A *sovereign private cloud* keeps data, models, and operations within a defined regulatory/geographic boundary under full customer or national control, combining cloud capabilities with isolated, compliant infrastructure (Azure Local).
- **Azure Local is the foundation** — an AI-optimized, purpose-built infrastructure platform (not just a server) that runs the full Foundry Local stack. It is **GA** for both connected and fully-disconnected sovereign use cases.
- Azure Local ships **pre-validated, certified hardware spanning CPU, NPU, and GPU** — from single-node inferencing/lightweight models to multi-node GPU clusters for high-performance generative AI — removing lengthy qualification cycles.
- Operations are **Kubernetes-native via Arc-enabled Kubernetes**; Foundry Local installs as an **Arc extension**. "If your team knows Kubernetes, they already know how to operate this" — no proprietary orchestration.
- **Connectivity spectrum is first-class:** connected mode syncs model catalog + management policies from cloud via Azure Arc; **air-gapped mode caches models locally and runs inference with zero cloud dependency.**
- Security/governance is the **same layer extended to on-prem**: identity via **Microsoft Entra ID with JWT validation**, inference endpoints secured with **TLS + API key / token-based auth**.
- **Today's preview announcement has three pillars** — Models (single → multi-node catalog + inferencing), Knowledge (local agentic RAG that can now take action), and Tools (custom MCPs + out-of-the-box MCPs + agents/chat).
- **Two model consumption modes:** *model-as-a-platform* (customer fully manages the stack, open-source/community models) and *model-as-a-service* (Microsoft-managed access to **frontier/partner proprietary models** like Mistral and OpenAI, gated by eligibility criteria for the most sensitive disconnected workloads).
- **Inference layer:** ONNX Runtime for single-node (generative *and* predictive AI) + **vLLM for multi-node high-performance serving**, all exposed through one consistent **OpenAI-compatible REST endpoint**.
- Catalog breadth matters: **71 models** in the catalog spanning proprietary, open-weight, and specialized/domain-tuned — customers are **not locked into a single model strategy** and pick the right model for the use case, performance need, and regulatory constraint.
- **Agentic RAG runs fully locally** with an iterative plan→search→merge loop that rewrites queries and re-retrieves until it hits high-confidence evidence or a configured effort limit; **every response is traceable to the source document**, no cloud calls.
- **Local data connectors:** RAG can ground on **SharePoint and Exchange Server via Microsoft 365 Local** running on Azure Local (currently POC — register to try).
- A **video agent** solution template (using **Video Indexer on Azure Local**) enables live video analysis, e.g. analyzing CCTV camera content fully on-prem.

## 📚 Detailed Notes

### Context — the agentic platform shift and why it forces a sovereign/edge story
The talk frames a **once-in-a-generation shift from applications to agentic AI as the operating layer** — agents become the way the next decade of software is built and run. Supporting analyst data on the slide: **1.3 billion AI agents by 2028** automating end-to-end ("A to N") business processes, and **82% of organizations adopting agents within the next three years**, moving from pilots to *core workforce*. The takeaway: organizations already operating with some AI agents now need to define how software runs going forward — "everything is about agents and agentic capabilities."

Microsoft grounds the product in **real customer scenarios that impose hard constraints**, explicitly *not* optional design choices:
- **Geopolitical risk**
- **Regulatory control**
- **The need to operate through outages**
- **Pressure to adopt AI without giving up sovereignty**

The defining principle: a customer's **AI strategy has to keep working when things break** — not only when everything runs smoothly on cloud.

Two anchor scenarios are called out:
- **Public safety** — running a command center or responding to a crisis allows **no tolerance for latency, dependency, or outages**. AI must operate **fully disconnected** while still delivering real-time situational awareness and decision support. No external calls, no data sent to the cloud: *if the network goes down, the system cannot go down.*
- **Critical infrastructure (energy & utilities)** — distributed, often remote environments where **connectivity is not guaranteed**, yet they depend on AI for real-time monitoring, diagnostics, and incident response. If a substation or rail system loses connectivity, operations must not — the AI must keep running locally, safely, and in compliance.

The reframing: **AI is no longer just about performance or scale — it's about resilience, control, and the ability to operate under constraint.** The organizations solving for this now will be the ones able to deploy AI *everywhere it matters*.

### Sovereign AI portfolio — control, not just location
Microsoft's sovereign cloud portfolio gives customers freedom to choose the right balance of **control, capability, and autonomy**. The key conceptual point repeated throughout: **sovereign AI is about control, not location itself.**

In the middle of the portfolio sits the **sovereign private cloud** — a cloud environment operated under **full customer or national control**, where **data, models, and operations remain within a defined regulatory or geographic boundary**. It combines cloud capabilities with isolated, compliant infrastructure (Azure Local) that can operate independently, ensuring **continuity, control, and resilience even without external cloud connectivity.**

### What is Azure Local, and why Foundry runs on it
Before diving into the AI offering, the speaker establishes the foundation. **Azure Local is not new** and is **GA on both connected and fully-disconnected sovereign use cases.** It is the foundation that makes sovereign and enterprise AI possible on-premises.

Crucially, **it's not just a server** — it's a **purpose-built, AI-optimized infrastructure platform designed to run the full Foundry Local stack.** "Foundry Local" here means everything *from models to inferencing to agentic workflows*, entirely within the customer-owned environment.

**Hardware layer:**
- Delivers **AI-optimized hardware configurations spanning CPU, NPU, and GPU.**
- **Validated and certified** to run a set of Foundry workloads **out of the box.**
- Covers the range from **single-node inferencing / lightweight models** to **multi-node GPU clusters** for high-performance generative AI.
- Hardware is **pre-validated**, so customers deploy with confidence and **without lengthy qualification cycles.**

**Operations layer — Kubernetes-native:**
- Everything runs on **Arc-enabled Kubernetes**, meaning AI workloads are deployed, scaled, and managed with the **same declarative, operator-based approach** IT teams already use for containerized apps.
- **Foundry Local is installed as an Arc extension** — no custom orchestration or proprietary tooling.
- Stated plainly: *"If your team knows Kubernetes, they already know how to operate this."*

**Connectivity spectrum (a core differentiator):**
- **Connected mode:** syncs the **model catalog and management policies** from the cloud through **Azure Arc.**
- **Fully disconnected / air-gapped mode:** the **same infrastructure continues to operate autonomously** — **models are cached locally** and **inference runs without any cloud dependency.** Operations teams **retain full control.**

**Security & governance (the same layer, extended on-prem):**
- Identity handled through **Microsoft Entra ID with JWT validation.**
- Inference endpoints secured with **TLS and API key / token-based authentication.**
- This is the **same identity and governance layer customers use across their cloud estate**, simply extended to on-premises AI **without compromises.**

Summary: Azure Local is the **AI-ready platform** that brings Foundry capabilities from cloud to the **enterprise edge** — pre-validated hardware + Kubernetes-native ops + the same security model.

### The Foundry family — situating today's announcement
Microsoft positions three points on the Foundry spectrum:
1. **Microsoft Foundry** — the out-of-the-box offering to **build agents on the public cloud** (already known/available).
2. **On-device inferencing SDK** — an SDK **optimized for Windows, macOS, and Android** for on-device inference.
3. **(NEW — public preview) Foundry Local on Azure Local** — Foundry Local running on the on-prem infrastructure above, for **both connected and disconnected** scenarios, **single-node and multi-node**, across the different **form factors of Azure Local.** This is what the session announces.

### The three pillars of the Foundry Local announcement
When Microsoft says "Foundry Local," today's preview delivers **three capabilities**:

1. **Models** — In **February this year**, Microsoft already announced the Foundry Local **model catalog on single-node deployment** (good for customers whose needs are met by **ONNX inferencing** on a single node). Now, customers who need to **scale across multi-node** can use the Foundry Local **model catalog *and* inferencing** at multi-node scale.
2. **Knowledge** — A **refreshed local RAG offering** that helps you manage organizational knowledge locally (demoed later).
3. **Tools** — Connect a **custom MCP** to your local sources, mixing the **right model + RAG + custom MCPs + other local tools.** The combination runs on an **Arc-enabled Kubernetes** environment across Azure Local form factors, **single-node to multi-node.**

### Models in depth — discover, deploy, and bring-your-own
The model experience (left → right) covers:
- **Discover & deploy** from a **curated catalog** of models tuned for these scenarios.
- **Bring your own model (BYOM):** if you have a container with models chosen from **Hugging Face** (the example given is a predictive/generative model — caption rendered "Yellow 10," likely a **YOLO**-style vision model), you can **package it and merge it with your own OCI registry.**
- **Serving options:** Microsoft provides serving via either **vLLM** or **ONNX Runtime.**

On the **agent/tool side**, you can connect to local data via the MCPs mentioned, get a **reference application** to build a local chat experience, and **build agents that run locally** and connect with the entire platform offering.

### Two model consumption modes — model-as-a-platform vs model-as-a-service
The model offering ships in **two distinct modes**:

**1. Model-as-a-platform (customer-managed):**
- The **entire stack is managed by the customer.**
- Brings the **complete Foundry Local community / open-source models**, runnable across Azure Local form factors from **single-node to multi-node.**
- **Pre-built inferencing:** **ONNX Runtime for single-node**, **vLLM for multi-node.**
- Works for **both connected and fully disconnected** scenarios.

**2. Model-as-a-service (Microsoft-managed):**
- The approach for customers to **access frontier models.**
- Microsoft is **working with partners** to bring their **proprietary IP models** — e.g. **Mistral, OpenAI, and others** — to customers with the **most sensitive workloads** who **cannot access the cloud.**
- **Gated:** there are **specific eligibility criteria**; *not available to everyone.* Microsoft is still partnering with some of these vendors.
- Targeted at customers with **geopolitical / sovereign-driven model restrictions** — e.g. requirements for **EU-only LLMs**, geopolitical tension, regulatory pressure, concerns about **foreign jurisdiction / external access**, and a preference for **long-term strategic autonomy, fully disconnected.**

Both modes are **valid**; there's a **link/form** to request access and support from the product groups for either model-as-a-platform or model-as-a-service.

### How the stack layers together (models)
From bottom to top:
- **Infra:** Azure Local
- **Orchestration:** Kubernetes clusters
- **Inference model:** **ONNX** (single-node) or **vLLM** (multi-node — announced today)
- **Models:** community models on top — a **partial list of 71 models** is shown in the catalog

The customer chooses whether to manage models **through the platform itself** or via **model-as-a-service** (which also unlocks the **frontier models** meeting eligibility criteria). From the Azure Local UI, **IT can choose to deploy Foundry Local** and make it available to developers.

### Inference layer — one consistent runtime, OpenAI-compatible
The preview's inference support is explicitly:
- **Generative AI via ONNX Runtime** for single-node deployment, **plus**
- **vLLM** for multi-node high-performance serving, **plus**
- **Predictive AI workloads via ONNX Runtime.**

The unifying value: **all models — Foundry catalog, partner-provided, or customer BYOM — run through one consistent runtime exposing OpenAI-compatible REST endpoints.**

### Model breadth = flexibility without compromise
A key enabling point: customers are **not locked into a single model strategy.** They can choose across **proprietary, open-weight, and specialized models** depending on use case, performance need, and regulatory constraint. That means **frontier models for reasoning** *or* **smaller efficient models for edge/disconnected** environments, plus **domain-tuned models for specific workloads** — **all within the same platform.** Result: *the right model in the right place under full customer control, without compromise.*

### Agents & tools with Foundry Local — building the application
The second part enables developers to **build their own AI application** on the deployed models, via **solution templates** (code samples) available in **Microsoft Foundry solution templates.** Two offerings:
- **Chat UI** — a standard end-to-end chat experience, connectable to an **agent** the developer creates; that agent uses the **deployed model on the cluster.**
- **Video agent** — another use case where, e.g., **CCTV camera content can be analyzed** through **Video Indexer running on Azure Local.**

On the **knowledge side**, the extension enables **agentic RAG** — manage local knowledge with a **local chat UI** wired to **local RAG logic** that, **for the first time, can take action** (called out as one of today's preview announcements). For tools, you can **build your own custom MCP** or use an **out-of-the-box MCP from the catalog.** Microsoft will **expand the MCP catalog based on customer requests** for the local sources they need to connect.

### Agentic RAG — how the local knowledge pipeline works
The knowledge pipeline operates as follows:
1. A user asks a question.
2. The agent **plans the query** — decides what to search for.
3. It **selects which knowledge sources** to hit.
4. It **merges results into a grounded answer.**

The **key property is that it's iterative:** if the agent inspects the results and decides it doesn't have enough, it **loops back — rewrites the queries, expands the scope, and retrieves again.** That iterative loop is what makes it **agentic RAG.** It keeps going **until it has high-confidence evidence or hits the configured effort limit.**

Critical guarantees:
- **All of this runs locally — no cloud calls.**
- **Every response is traceable back to the source document.**

**Source types (two):** **indexed** or **remote.** An explicit call-out is made for **SharePoint and Exchange Server**, both part of **Microsoft 365 Local** that runs on Azure Local. Microsoft is **partnering and testing a POC** specifically for reading this local data — interested customers are invited to **register and try the POC.**

### Putting it together — the local chat + agent demo flow
In the middle sits the **local chat experience.** The developer **builds a local agent** that works with the **deployed model**, the **Azure RAG (agentic RAG)**, and the **tools.** In the example, the agent runs on **Mistral**; a question is asked and the agent (connected to that implementation) returns an answer **with its sources shown.** **SharePoint and Exchange are toggled on** because the template ships with **pre-configured connectivity to local data.** Every response **shows where the information was fetched from.** The model is selectable via a **drop-down menu** (as in other local chat experiences) — and the speaker notes you **don't necessarily need a strong model** for that particular scenario.

### Video analysis — the video agent template
The final offering is **video analysis.** From the **Foundry solution templates**, customers can — **for the first time** — download the **code sample for video analysis** and try it themselves, analogous to the local chat experience. The **video agent** serves multiple scenarios, **mainly live video analysis.**

### Getting started
- There's a **registration link** to join the **preview** covering everything shown; customers can choose to try **only the model offering**, or **expand to RAG + local chat experience.** Available for customers running **Kubernetes on Azure Local.**
- A **blog post** explains both the technicalities and code samples.
- **Documentation** is available covering the different models offered and which scenarios to use each in.
- Microsoft is **actively seeking customer/developer feedback** on the newly announced preview.

## 🛠️ Products / Features / Technologies Mentioned
- **Foundry Local (on Azure Local)** — the full Foundry stack (models, inferencing, agentic workflows) running on-prem in customer-owned, connected or disconnected environments. *Announced in public preview.*
- **Azure Local** — purpose-built, AI-optimized on-prem infrastructure platform (CPU/NPU/GPU); foundation for sovereign/enterprise AI. **GA** for connected and disconnected use cases.
- **Microsoft Foundry** — the public-cloud offering for building agents (the cloud counterpart).
- **Foundry on-device inferencing SDK** — SDK optimized for **Windows, macOS, and Android** for on-device inference.
- **Azure Arc / Arc-enabled Kubernetes** — declarative, operator-based ops layer; Foundry Local installs as an **Arc extension**; syncs catalog/policies in connected mode.
- **ONNX Runtime** — inference runtime for single-node deployments; supports generative *and* predictive AI.
- **vLLM** — high-performance inference engine for multi-node serving (announced for multi-node today).
- **Microsoft Entra ID** — identity with **JWT validation** securing the platform.
- **Model-as-a-platform** — customer-managed mode with community/open-source models.
- **Model-as-a-service** — Microsoft-managed mode for frontier/partner proprietary models (eligibility-gated).
- **Hugging Face** — source for bring-your-own models packaged into the customer's OCI registry.
- **OCI registry** — where customers store/merge their own packaged model containers.
- **MCP (Model Context Protocol) — custom + out-of-the-box** — connects agents/RAG to local tools and data sources; catalog to expand by customer demand.
- **Agentic RAG (local)** — iterative plan→retrieve→merge knowledge pipeline that runs locally, cites sources, and can now take action.
- **Microsoft Foundry solution templates** — code samples for a **chat UI** and a **video agent**.
- **Video Indexer (on Azure Local)** — powers the video agent for live/CCTV video analysis on-prem.
- **Microsoft 365 Local** — brings **SharePoint** and **Exchange Server** on-prem as local RAG data sources (POC).
- **OpenAI-compatible REST endpoints** — the consistent API surface for all served models.
- **Partner/frontier models** — **Mistral**, **OpenAI**, and others offered via model-as-a-service (e.g. GPT-OSS-20B and Mistral 3B used in demo).

## 🚀 Announcements / What's New
- **Foundry Local on Azure Local — public preview**, supporting **both connected and fully-disconnected** scenarios and **single-node + multi-node** across Azure Local form factors.
- **Models pillar:** Foundry Local **model catalog + inferencing now scale to multi-node** (building on the **single-node catalog announced February this year**). Catalog **expanded** to include more community and proprietary models, validated to run on Azure Local connected/disconnected.
- **Two model consumption modes:** **model-as-a-platform** (customer-managed, open-source/community) and **model-as-a-service** (Microsoft-managed access to frontier/partner models — eligibility-gated, for the most sensitive disconnected workloads).
- **Knowledge pillar:** refreshed **local agentic RAG** offering — and **for the first time, local RAG can take action** (explicitly called out as a preview announcement today).
- **Tools/agents pillar:** support for **custom MCPs** and **out-of-the-box MCPs** from a catalog; **solution templates** for a **local chat UI** and a **video agent**, all running on Arc-enabled Kubernetes.
- **Video analysis code sample** available **for the first time** in Foundry solution templates (video agent built on **Video Indexer on Azure Local**).
- **Microsoft 365 Local (SharePoint + Exchange Server) RAG connectors** — currently a **POC** open for registration.
- **Inference support stated for preview:** generative AI via ONNX Runtime (single-node) + vLLM (multi-node) + predictive AI via ONNX Runtime, all behind OpenAI-compatible REST endpoints.
- *Status note:* **Azure Local itself is GA** (connected + disconnected); the **Foundry Local model/RAG/tools offering on top is in public preview**, with model-as-a-service partner availability still being finalized and eligibility-restricted.

## 💡 Demos
- **IT deployment of the Foundry Local extension (Azure portal):** From **Settings → Extensions**, click **+**, choose the new **"Foundry Local on Azure Local"** option, fill in configuration parameters, then **review & create**. Point proven: standing up Foundry Local on Azure Local is a simple, IT-driven extension install — no bespoke setup.
- **Model deployment via PowerShell / CLI:** Showed that everything is available via **SDK, CLI, or API** (not just UI). Steps: **fetch an access token**, run a command that **lists all available models**, then **deploy a selected model** with a `POST` request — naming it (e.g. **"GPT-OSS-VLLM"**), specifying the model in the body (**GPT open-source 20B**), and choosing the inferencing engine. Response confirmed **"being deployed."** Repeated for a second model by switching the body to **Mistral 3B**, deploying both selected models via command line. Point proven: developers can script real multi-model deployments to the cluster.
- **Local chat + agentic RAG (Mistral):** A local agent wired to the deployed **Mistral** model, **Azure agentic RAG**, and tools. A question is asked; the agent returns an answer with **SharePoint and Exchange toggled on** (pre-configured local-data connectivity) and **shows the source** of each response. Model is switchable via a **drop-down**. Point proven: grounded, source-cited local chat over on-prem M365 data with no cloud calls.
- **Video agent template:** Downloadable code sample for **live video analysis** (e.g. CCTV) via **Video Indexer on Azure Local** — demonstrated as a second solution-template use case alongside chat.

## 📊 Notable Stats / Quotes
- **1.3 billion AI agents by 2028** automating end-to-end business processes (analyst data on slide).
- **82% of organizations** adopting agents within the next **three years**, moving from pilots to core workforce.
- **71 models** shown in the Foundry Local catalog (a partial list).
- Demo models: **GPT open-source 20B (GPT-OSS-20B)** and **Mistral 3B**.
- Single-node Foundry Local catalog originally announced **February this year**.
- *"Sovereign AI is about control, not just about the location itself."*
- *"AI strategy has to work when actually things break"* — not just when everything runs smoothly on cloud.
- *"If the network goes down, the system cannot go down."* (public-safety command center framing)
- *"If your team knows Kubernetes, they already know how to operate this one."*
- *"Every response is traceable back to the source document. All of these run locally. No cloud calls."* (on agentic RAG)
- Platform-shift framing: *"once in a generation platform shift from applications to agentic AI as the operating layer."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Register for the **Foundry Local on Azure Local preview** (model offering first, then expand to RAG + local chat).
  - Stand up an **Arc-enabled Kubernetes** Azure Local node and install **Foundry Local as an Arc extension**; deploy a model via the **PowerShell/CLI** flow (token → list → `POST` deploy) using **GPT-OSS-20B** and **Mistral 3B**.
  - Test the **agentic RAG** loop against local docs and verify **source traceability** + the **configured effort limit** behaviour.
  - Try the **SharePoint + Exchange (Microsoft 365 Local)** RAG POC — register for it.
  - Pull the **video agent** solution-template code sample and run **live video analysis** via **Video Indexer on Azure Local**.
  - Experiment with **BYOM**: package a Hugging Face model into an **OCI registry** and serve via **vLLM** / **ONNX Runtime**.
- [ ] Questions:
  - What are the exact **eligibility criteria** for **model-as-a-service** frontier/partner models (Mistral, OpenAI)?
  - Which **MCPs** ship **out-of-the-box** in the catalog today, and how is the catalog roadmap prioritized?
  - What are the **hardware SKUs / minimums** (CPU/NPU/GPU) for single-node vs multi-node Foundry workloads on Azure Local?
  - For **air-gapped** updates, how are model catalog + security patches delivered without cloud sync?
  - What's the **GA timeline** for the Foundry Local model/RAG/tools preview, and for the M365 Local RAG POC?
  - What "can now take action" means concretely for **agentic RAG** — which action/tool types are supported?
- [ ] Relevant to:
  - Sovereign / regulated workloads (gov, defense, public safety, EU-data-residency).
  - Edge & **disconnected/air-gapped** industrial scenarios (energy, utilities, rail, substations).
  - Teams standardizing on **Azure Arc + Kubernetes** wanting on-prem agentic AI without proprietary tooling.
  - Anyone evaluating **on-prem RAG over SharePoint/Exchange** with full data sovereignty.

## 🔗 Related
- 
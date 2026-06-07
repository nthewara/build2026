---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/logic-apps
  - topic/automation
  - topic/agents
  - topic/azure-integration
source: https://www.youtube.com/watch?v=MglAzcQEkUg
session_code: OD832
event: Microsoft Build 2026
speakers: Divya Swarnkar
duration_min: 23
aliases:
  - From workflows to agentic automation with Azure Logic Apps
---

# OD832 — From workflows to agentic automation with Azure Logic Apps

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Divya Swarnkar (Product Manager, Azure Logic Apps)  
> **Duration:** ~23 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=MglAzcQEkUg)

## 🎯 TL;DR
Azure Logic Apps is evolving from a decade-proven enterprise integration platform into a full **AI automation platform**, and this session anchors that shift around three big moves. First, the headline announcement: **Azure Logic Apps Automation**, a new enterprise-ready platform (public preview at `auto.azure.com`) that strips out infrastructure overhead and the Azure portal dependency — you sign in with just a Microsoft Entra ID, no Azure expertise required, yet everything you build still runs on Azure with full enterprise rigor. Second, **Knowledge as a Service**: managed RAG built directly into workflows so you upload files and Logic Apps auto-ingests, chunks, vectorizes, and retrieves with zero pipeline code (built on Cosmos DB + Azure OpenAI). Third, **deep Azure AI Foundry + Logic Apps integration**: build/host agents in Foundry, then trigger, orchestrate, and operationalize them from Logic Apps with 1,400+ connectors, human-in-the-loop, and full run-history traceability. The unifying goal across all three: make AI automation **easier to build and easier to trust in production**.

## 🔑 Key Takeaways
- Logic Apps is being repositioned from an "enterprise integration platform" to an **"AI automation platform"** — the same trusted foundation now extends natively to agents.
- The platform's scale story: **100,000+ customers**, **millions of workflow executions** and **trillions of connector operations per month**, across **1,400+ connectors** (SaaS, databases, AI services, on-prem) — including most of the Fortune 500.
- Core thesis: most companies have built an AI agent **demo**, but very few run one in **production** — because the gap is retries, error handling, logs, networking, identity, security, and governance, all of which Logic Apps provides from day zero.
- The same enterprise control that makes Logic Apps powerful also made it **heavy to start** — procurement approvals for multiple Azure services/models, provisioning overhead, and self-wiring separate services were the real friction.
- **Azure Logic Apps Automation** (announced, public preview at `auto.azure.com`) solves this by removing **infrastructure management** and the **Azure portal dependency** while keeping Azure-grade reliability and scale.
- Two deliberate changes + one deliberate non-change: (1) took out infra management but **kept Azure**; (2) took out the Azure portal so you sign in with **Entra ID only**; and they did **not** change the enterprise rigor.
- AI lowers the barrier so **operations leads, analysts, AI builders, and knowledge workers** can describe a workflow in natural language and participate in building it — breaking the central-integration-team / IT bottleneck.
- Real-world solutions combine **deterministic steps + AI reasoning** in one workflow (e.g. ServiceNow/Salesforce deterministic actions around an AI invoice-validation agent).
- Agents in the new platform are built on the **GitHub Copilot SDK** and run on a **sandbox** — isolated compute per workflow, with native file, shell, and web operations, plus support for **skills and MCPs**.
- **Knowledge as a Service** collapses a complex RAG pipeline into a few steps: upload files → automatic ingest, chunk, vectorize; retrieval is a native workflow step. Built on **Cosmos DB** (vector store) + **Azure OpenAI** (embeddings + chat). Now in public preview.
- The governance model has **two layers / two roles**: **Project** (an Azure ARM/RBAC resource the admin owns — members, permissions, policies, quotas, knowledge, sandboxes, models) and **App** (where developers build workflows with no Azure access required). One team governs, another builds — same secure boundary.
- **Azure AI Foundry + Logic Apps** together: Foundry is where agents **live** (models, tools, instructions, grounding, evaluation, versioning, observability); Logic Apps is where agents are **invoked and orchestrated** (triggered by any event/schedule, using native connectors).
- You can **create and edit Foundry agents from inside Logic Apps** (it calls Foundry APIs to provision), and Foundry agents can use **native Logic Apps connectors/APIs/workflows as their tools** — the key "unlock."
- **Human-in-the-loop** is first class: long-running workflows can pause an agent for Teams-based approval and resume on response. Execution is correlated across both portals by **run ID** — operational view in Logic Apps, agent reasoning/traces in Foundry.

## 📚 Detailed Notes

### Framing: from integration platform to AI automation platform
Divya Swarnkar (PM, Azure Logic Apps) opens by framing the entire narrative: Logic Apps is moving from an **enterprise-proven integration platform** to an **AI automation platform**. The session is structured in three parts, each with a demo:
1. **Logic Apps Automation** — a brand-new platform announced at Build.
2. **Knowledge as a Service** — managed RAG ("managed drag") built directly inside workflows.
3. **Azure AI Foundry + Logic Apps** — coming together to build and orchestrate real-world AI agents.

### What Logic Apps already is (the grounding)
Before the new announcements, she grounds the audience in the existing platform's maturity:
- **Proven across a decade** of enterprise use, operating at **planetary scale**.
- **100,000+ customers**, running **millions of workflow executions** and **trillions of connector operations every month**.
- **1,400+ connectors** spanning SaaS applications, databases, AI services, and on-prem applications.
- Rapid token-usage growth is coming from **agentic workflows running in production at scale**.
- The audience signal: a large share of customers — **most of the Fortune 500** — are already running enterprise workloads on Logic Apps in production.

Crucially, it's "not just scale." The platform ships with everything needed for production-grade apps: **dedicated compute, VNet support, security, identity, networking, compliance**. These are **not add-ons** — they are **built in from day zero**. And every one of these enterprise foundations now **extends to AI**: on the same foundation, Logic Apps offers workflows plus AI capabilities including **agents, tools, and human-in-the-loop controls**.

### The "demo to production" gap (the central argument)
The recurring theme: when customers ask "What's our path from AI demo to production?", the answer is increasingly "**you already have the platform you can trust**." The reasoning:
- Most companies have built an **AI agent demo**, but **very few have one in production**.
- For a **demo**, the happy path is enough — no retries, no error handling, no logs.
- For **production**, you need **consistent outcomes** and a platform where networking, identity, security, and governance are **on from day one**.
- That difference — happy-path prototype vs. business-critical, governed workflow — is the real "distance," and Logic Apps is purpose-built for the production ("right column") side.

### The catch: power created friction
Honest acknowledgment: the very things that make Logic Apps powerful and give customers control **also made it heavy to start**. Friction points:
- **Procurement / approvals** for multiple Azure services and AI models.
- **Provisioning and management overhead** of services and infrastructure.
- Because capabilities ship as **separate Azure services**, developers **wire them together themselves** — the real hidden cost.

The consequence: developers either **burn weeks** getting to "Hello World"/a basic prototype, or they **pick a lighter-weight tool that doesn't actually fit** just because it's faster to start. Either way, the powerful platform **isn't reaching the people who need it most**.

### Why now: AI changes who can automate
Historically, automation was limited to **people who could write code**, so those closest to the business problems often couldn't build solutions — creating the classic **IT bottleneck**. AI changes the dynamic: an **operations lead, analyst, AI builder, or knowledge worker** can now describe a workflow in **natural language** and participate in building it. Automation is no longer confined to **central integration teams**. This creates the clear need: a platform with **power and reliability for production workloads** that **doesn't require you to be an Azure expert**.

### The solution shape: two changes, one deliberate non-change
The design move that defines Logic Apps Automation:
- **Problem 1 — infrastructure overhead:** they **took out infrastructure management** but **kept the Azure**, so you still get full **Azure-grade reliability and scale**.
- **Problem 2 — barrier to entry:** they **removed the Azure portal dependency** — sign in with your **Entra ID** and start building. **No Azure access or expertise required**, yet whatever you build is still **built on Azure**.
- **Deliberate non-change:** the **enterprise rigor** stays. "Remove the friction, but not the rigor."

These two things "almost never come together" — and now they do.

### Announcement: Azure Logic Apps Automation
**Azure Logic Apps Automation** — an enterprise-ready automation platform built for **developers of every kind**, offering a **low barrier to entry with the same enterprise rigor**. **Available in public preview today at `auto.azure.com`.** Four defining attributes:
1. **Same enterprise-ready platform** that runs trillions of action executions per month → **production-ready from day one**.
2. **Day-zero friction gone** — all compute, infrastructure, and service provisioning is **hosted on your behalf**; you sign in and you're ready to build.
3. **No Azure portal needed** — it's **hosted outside Azure**; all you need is **Microsoft Entra ID** to log in.
4. **Still built for enterprises** — isolated compute, **RBAC**, auditability, **VNet support**, and everything Logic Apps offers as an enterprise platform today.

### Under the hood: the resource/organization model
After the first demo, Divya explains the underlying constructs:
- **Project (topmost construct):** where an **admin** operates. Think of projects as **environments** — scoped by development environments or by **business domains** (your choice). Projects are how the **platform/infrastructure team controls access, networking policies, and shared resources**.
- **Applications (inside a project):** developers create one or many. This is where **builders work day-to-day**; **no Azure access** is needed.
- **Shared resources (project level, platform-team managed, app-consumable):** **knowledge** (for grounding), **sandboxes** (isolated agent compute), **policies** (governance/guardrails), and the **ability to include/exclude connectors**.
- **Per-app resources:** each app has its own **workflows, connections, files, and skills**, plus an **analytics dashboard** and its own permission model (**reader or contributor**) so teams collaborate without exposing the rest of the project.

This yields a **clean separation**: **admins govern the platform, developers build on top.**

### Two-layer governance model
- **Layer 1 — Project:** an **Azure resource** governed by **ARM RBAC**. The **project admin** owns it and manages members, permissions, policies, quotas, knowledge, sandboxes, and models scoped at the project level.
- **Layer 2 — App (developer/builder):** developers build apps (workflows, connections, files, skills). **No Azure access or permissions required.** They consume **project-scoped resources within the policies the admin set**.
- Net: **one team governs while another builds, both inside the same secure boundary.**

### Sandbox & agent execution model
The **sandbox** is an **isolated environment** to run **GitHub Copilot agents** with **native file, shell, and web operations** and isolated execution. These agents can **write code dynamically** and support **skills and MCPs** for reasoning and actions. The sandbox is **configured at the project** with repositories, skills, and other context. In the invoice example, the **invoice agent is built on the GitHub Copilot SDK** and runs on a **sandbox** (isolated compute **per workflow**, configured at the project). You can provide it **business context** (e.g. the invoice), **skills** (validation, notification), and even **GitHub or Azure DevOps repositories**.

### Knowledge as a Service (managed RAG)
Building a RAG pipeline today is **complex**: prepare the vector store and data, then build a pipeline to **parse, chunk, and tokenize** documents. Logic Apps **collapses this into a few simple steps**:
- You **upload files**; Logic Apps **automatically ingests, chunks, and vectorizes** the content.
- **No pipeline to configure, no infrastructure to maintain.**
- **Retrieval is a native workflow step.**
- This **dramatically lowers the barrier** for anyone building **grounded, personalized agents**.

Implementation details from the demo:
- The **knowledge base is scoped at the app level**, so it's shared across workflows in the same app.
- **One-time setup:** built on **Cosmos DB** as the vector store and **Azure OpenAI** for models — you connect the knowledge base to a **Cosmos DB instance**, then provide a model for **embedding generation** and another for **chat completions**.
- Files are organized into **groups**, which are the **unit of reference from an agent** — group logically by scenario/outcome. On upload you choose the group and add **metadata (name, description)**. Each file goes through **tokenization, chunking, and embedding**, with a **status** shown so you know when it's ready.
- In the agent, a **knowledge section** lets you select the specific **knowledge group** to expose (and add files directly). Behind the scenes the agent performs **semantic search and retrieval** against the group based on the query. **References to knowledge are surfaced** in both the agent chat and the run history, and the agent node shows the **knowledge group used + token utilization**.

### Azure AI Foundry + Logic Apps: two services, one cohesive experience
The third pillar brings two Azure services together:
- **Azure AI Foundry (left):** Microsoft's AI platform where **agents are built and hosted**. You **define agents** with models, tools, instructions; **ground** responses in knowledge and enterprise data; and **evaluate, version, and observe** agent behavior. **"Foundry is where your agent lives."**
- **Azure Logic Apps (right):** your **automation and orchestration platform**, where agents are **invoked and orchestrated**. You **trigger agents from any event or schedule** using the **hundreds of connectors** Logic Apps offers natively.

The integration provides an improved experience to use the services together to **automate and operationalize AI agents and run them in production at scale**.

Key mechanics from the auto-loan demo:
- In Logic Apps you create a workflow and add an **agent node** that **connects to a Foundry project**; you can **pick any model or existing agent** in that project (every Foundry agent "shows up ready to invoke").
- If the agent you need doesn't exist, you can **create it without leaving Logic Apps** — behind the scenes Logic Apps **calls the Foundry APIs to provision it**, and it appears in your Foundry project. A **deep link** lets you jump between portals.
- **Two-way sync:** updating instructions in Logic Apps **flows straight back to Foundry**; the agent **stays in sync**.
- The **unlock:** the loan agent's **tools are native Logic Apps connectors, APIs, and workflows** — i.e. **Foundry as the AI platform + the full Logic Apps ecosystem (1,400+ connectors, your APIs, your custom code) as the agents' tools**, on a proven enterprise platform.

### Human-in-the-loop and dual-lens observability
The auto-loan workflow handles incoming loan requests **autonomously**, combining **deterministic business steps with AI reasoning** — using a **triage agent** in Foundry for **duplicate checks**, then an **auto-loan agent** for the **approval decision**. Flow:
- A submitted loan request that **needs human approval** pauses the agent; the **approval request lands in Teams**.
- With Logic Apps workflows you can build **long-running human-in-the-loop processes** with Foundry agents.
- Once the approver responds, the **workflow resumes**, the loan agent **finalizes the decision**, and the customer gets an **approval notification** — "autonomous with a human in the loop exactly where it matters."
- **Two correlated lenses, one execution:**
  - **Logic Apps run history** — every step end to end: **inputs, outputs, token usage** — the **operational/governance view** for platform and automation teams.
  - **Foundry** — the agent's **own traces and logs**: reasoning, tool calls, thread history — the **developer view** to tune prompts, debug behavior, and track quality.
  - The two are **correlated by run ID across both portals**, so you get the right view in the right place "without losing the thread between them."

### Session recap (Divya's own wrap)
Three key capabilities, one common goal:
1. **Logic Apps Automation** — a new platform for building automations on the **same enterprise-grade platform at scale**, but with **low barrier to entry**.
2. **Knowledge as a Service** — managed RAG directly inside workflows.
3. **Deep Foundry ↔ Logic Apps integration** — for agent orchestration.

The unifying goal: **make AI automation easier to build and easier to trust in production.** Learn more via the docs, blogs, and demos referenced in the session.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Logic Apps** — the decade-proven enterprise integration platform being extended into an AI automation platform.
- **Azure Logic Apps Automation** *(new)* — enterprise-ready automation platform with no infra management and no Azure portal dependency; public preview at `auto.azure.com`.
- **Knowledge as a Service / Knowledge in Logic Apps** *(new, public preview)* — managed RAG (ingest, chunk, vectorize, retrieve) as native workflow steps.
- **Azure AI Foundry** — Microsoft's AI platform where agents are built, hosted, grounded, evaluated, versioned, and observed.
- **Microsoft Entra ID** — the only credential needed to sign in to Logic Apps Automation (replaces Azure portal access).
- **GitHub Copilot SDK** — the framework the automation-platform agents are built on.
- **GitHub Copilot agents** — agents run in the sandbox with native file/shell/web operations.
- **Sandbox** — isolated compute environment (per workflow, configured at project) for running agents, supporting skills and MCPs.
- **MCP (Model Context Protocol)** — supported by sandbox agents for reasoning and actions.
- **Skills** — reusable capabilities (e.g. validation, notification) provided to agents.
- **Azure Cosmos DB** — vector store backing the Knowledge as a Service capability.
- **Azure OpenAI** — provides embedding-generation and chat-completion models for the knowledge base.
- **ARM RBAC (Azure Resource Manager role-based access control)** — governs the Project layer.
- **VNet support** — built-in networking isolation for enterprise workloads.
- **Connectors (1,400+)** — native Logic Apps connectors to SaaS, databases, AI services, on-prem; usable as Foundry agent tools.
- **ServiceNow** — deterministic step (ticket creation) in the invoice-processing workflow.
- **Salesforce** — deterministic step (record update) in the invoice-processing workflow.
- **Microsoft Teams** — destination for human-in-the-loop approval requests.
- **GitHub / Azure DevOps repositories** — can be provided as context/source to agents.
- **JavaScript (in-workflow code)** — Copilot writes JavaScript expressions/code in action scope with exception handling.
- **Default hosted LLM** — provided out of the box; you can bring additional first-party and third-party models via your GitHub account.

## 🚀 Announcements / What's New
- **Azure Logic Apps Automation — public preview** (announced at Build). Available today at **`auto.azure.com`**. New enterprise-ready automation platform: no infrastructure management, no Azure portal dependency (Entra ID sign-in only), with isolated compute, RBAC, auditability, and VNet support retained.
- **Knowledge as a Service (Knowledge in Logic Apps) — public preview.** Managed RAG built into workflows — upload files and get automatic ingest/chunk/vectorize plus native retrieval; built on Cosmos DB (vector store) + Azure OpenAI (embeddings + chat). "Bring your organization's documents into your agents without writing a single line of pipeline code."
- **Azure AI Foundry ↔ Logic Apps deep integration.** Improved experience to build/host agents in Foundry and invoke/orchestrate them from Logic Apps — including creating/editing Foundry agents from within Logic Apps (via Foundry APIs), two-way instruction sync, native Logic Apps connectors as agent tools, human-in-the-loop, and run-ID-correlated observability across both portals. (Presented as a new/improved integrated experience; specific GA/preview status not explicitly stated.)

## 💡 Demos

### Demo 1 — Logic Apps Automation (zero-setup onboarding + invoice processing)
- Open a browser → `auto.azure.com` (hosted **outside** Azure); landing page previews capabilities; **sign in with Entra ID only**.
- Land on a **projects** page; inside a project are **apps** and **shared resources** (sandbox, models, network policies); **project admins add developers and assign role-based permissions**.
- **Sandbox** highlighted as isolated environment for GitHub Copilot agents (native file/shell/web, skills, MCPs), configured at project with repos/skills/context.
- Create a workflow by **describing it in natural language**; the agent **scaffolds the workflow**, with Copilot picking connectors and configuring many parameters (connections still need updating). Iteratively build/test with Copilot; when asked to write code, Copilot adds the action and writes **JavaScript with exception handling**. Updates can be **workflow-scoped or action-scoped**.
- A pre-built **invoice-processing workflow** shows the **deterministic + AI** pattern: **ServiceNow ticket creation** and **Salesforce update** are deterministic; the **invoice agent** (GitHub Copilot SDK, on a sandbox) validates against business context/skills; after validation, deterministic steps update Salesforce and close the ticket if approved.
- **Code view** is an editable, real-time-synced view of the same workflow; Copilot can be scoped to a **specific action** for targeted JavaScript expressions/code, with **multi-turn conversations** to iterate.
- On trigger (invoice received), the **run history shows full traceability and auditability** of every step, with **real-time streaming** into each step as it happens. For an **agent node**, you can **visually see in real time the tools it's using**. Every step is logged with **inputs, outputs, execution time, status**, and **agent outcomes include token utilization at each step**.
- **Point proved:** the heavy prerequisites are gone — sign in and build — while keeping full enterprise traceability and the deterministic-plus-AI workflow model.

### Demo 2 — Knowledge as a Service (managed RAG inside a workflow)
- Set up a **knowledge base** scoped at the **app level** (shared across workflows in the app).
- **One-time setup:** connect to a **Cosmos DB** instance (vector store) and provide an **Azure OpenAI** model for **embeddings** and another for **chat completions**.
- Add files to the knowledge base and organize into **groups** (the unit of reference from an agent); on upload choose the group and add **metadata (name, description)**. Each file goes through **tokenization, chunking, embedding**, with **status** shown until ready.
- A workflow with an **agent that classifies incoming documents** — and if it's a **contract**, validates against the org's approval rules/policies — is grounded via the agent's **knowledge section**: select the **knowledge group** (connection pre-set), add files directly, and provide instructions. Behind the scenes the agent runs **semantic search and retrieval**.
- Run with a **sample contract**: run history shows the agent **classified the document as a contract**, then ran the **contract validation steps**, all **grounded** in the uploaded classification + contract-processing guides, with **knowledge references surfaced in both agent chat and run history**, plus the **knowledge group used and token utilization**.
- **Point proved:** what normally takes significant effort as a custom ingestion + retrieval pipeline is **fully handled for you** — grounded agents with no pipeline code.

### Demo 3 — Foundry agents orchestrated from Logic Apps (auto-loan approval)
- In Logic Apps, create a workflow and add an **agent node** connected to a **Foundry project**; **pick any model or existing agent** (every Foundry agent shows up ready to invoke).
- **Create a new Foundry agent in-place** with just a name + model — Logic Apps calls the **Foundry APIs** to provision it, and it appears in the Foundry project; a **deep link** lets you jump between portals. **Updating instructions in Logic Apps flows back to Foundry** (agents stay in sync).
- **Auto-loan approval workflow** handles incoming loan requests **autonomously in real time** using a **triage agent** (duplicate checks) and an **auto-loan agent** (approval decision) — both living in **Foundry**, but using **native Logic Apps connectors, APIs, and workflows as their tools**.
- Submit a loan request that **requires human approval**: run history shows the agent **paused waiting on human approval**; the **approval request lands in Teams**; once the approver responds the **workflow resumes**, the loan agent **finalizes the decision**, and the customer gets an **approval notification**.
- **Dual-lens observability:** Logic Apps run history captures every step end to end (**inputs, outputs, token usage**) for the platform/automation/governance view; **Foundry** shows the agent's **traces, logs, reasoning, tool calls, thread history** for developers — the **same execution correlated by run ID** across both portals.
- **Point proved:** Foundry as the AI platform + the full Logic Apps ecosystem as the agents' tools enables **long-running, human-in-the-loop, autonomous workflows** that are fully observable on a proven enterprise platform.

## 📊 Notable Stats / Quotes
- **100,000+ customers** running on the Logic Apps platform.
- **Millions of workflow executions** and **trillions of connector operations every month.**
- **1,400+ connectors** to SaaS apps, databases, AI services, and on-prem applications.
- The platform runs **trillions of action executions per month** (cited as why Logic Apps Automation is production-ready from day one).
- **Most of the Fortune 500** already run enterprise workloads on Logic Apps in production.
- *"We wanted to remove the friction, but not the rigor."*
- *"Most companies at this point have built an AI agent demo, but very few have one running in production."*
- *"Foundry is where your agent lives."* / Logic Apps is *"where agents are invoked and orchestrated."*
- *"Same execution, two lenses correlated by run ID across both portals."*
- *"Low barrier to entry with same enterprise rigor."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
    - Sign in to **`auto.azure.com`** with an Entra ID and scaffold a workflow from a natural-language prompt to gauge how much Copilot configures vs. what needs manual wiring.
    - Stand up the **Knowledge as a Service** one-time setup (Cosmos DB vector store + Azure OpenAI embedding/chat models) and test grounding an agent against a small document group.
    - Build a minimal **Foundry agent + Logic Apps** orchestration with a **Teams human-in-the-loop** approval step and inspect the run-ID correlation across both portals.
    - Compare a **deterministic + AI** invoice/contract workflow here vs. an equivalent hand-built pipeline to quantify the time-to-Hello-World savings.
- [ ] Questions:
    - What are the **pricing / quota / token-billing** mechanics for the hosted compute, default LLM, and sandbox in Logic Apps Automation?
    - Since the platform is **hosted outside Azure** (Entra ID only), how does **data residency, VNet, and compliance** map back to a customer's Azure tenant in practice?
    - Is the **Cosmos DB + Azure OpenAI** dependency for Knowledge configurable (other vector stores / models), or fixed?
    - What's the **GA timeline** for Logic Apps Automation, Knowledge, and the Foundry integration?
    - How do **MCPs and skills** in the sandbox interoperate with the standard 1,400+ connectors — overlap or complementary?
- [ ] Relevant to:
    - Azure integration / iPaaS modernization and any "AI demo → production" governance conversations.
    - Customers wanting **citizen-developer / low-barrier** automation without surrendering enterprise controls.
    - Agent orchestration architectures pairing **Azure AI Foundry** with **human-in-the-loop** business processes.

## 🔗 Related
- [[Azure Logic Apps]]
- [[Azure AI Foundry]]
- [[Agentic automation]]
- [[Retrieval-Augmented Generation (RAG)]]
- [[GitHub Copilot SDK]]
- [[Human-in-the-loop]]
- [[Model Context Protocol (MCP)]]
- [[Microsoft Build 2026]]
- Source list: [[2026 Build Session List]]

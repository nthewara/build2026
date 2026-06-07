---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/agents
  - topic/multi-agent
  - topic/support
  - topic/ai
  - topic/mcp
  - topic/redhat
source: https://www.youtube.com/watch?v=ofGlquMeYKw
session_code: ODSP915
event: Microsoft Build 2026
speakers: Carlos (Red Hat), Sharon (Red Hat)
duration_min: 6
aliases:
  - Resolve support cases with multi-agent workflows
  - ODSP915
---

# ODSP915 — Resolve support cases with multi-agent workflows

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Carlos & Sharon (both Red Hat)  
> **Duration:** ~6 min (a ~5-minute all-live lightning demo)  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=ofGlquMeYKw)

> [!note] Caption note
> This is a short, fast, all-live partner demo and the auto-captions garble a couple of product names. Best-effort corrections used below: the communication/agent-to-agent layer captioned **"8way"** is read as **A2A (Agent2Agent)**, and **"ADK"** is the **Agent Development Kit** used to build the agents. The catalog is referred to both as the **Red Hat AI "secure MCP catalog"** and the **OpenShift AI MCP catalog** — treated here as the same Red Hat catalog. Where a term is genuinely uncertain it is flagged as *caption-uncertain* rather than invented.

## 🎯 TL;DR
Carlos and Sharon from **Red Hat** give a fast, fully-live (~5 min) demo of an **open-source multi-agent support-resolution system** that diagnoses and resolves customer support cases **across different partner ecosystems**. The headline technical move: they deploy an **Azure MCP server** straight from the **Red Hat OpenShift AI MCP catalog** onto a **Red Hat OpenShift** cluster — **no glue code, no custom integration** — and then consume it as a regular workload inside a multi-agent app. The app is layered: a chat **web front-end** (their "quick start"), an **orchestration & security layer** (authentication, authorization, audit), a **routing agent** that detects user intent and delegates to the right specialist, and specialist agents like an **auto support agent** that wraps the Azure MCP server. **Identity-based access control** governs which agents a user can reach, and **OpenTelemetry** captures a full **audit trail** of every request (accepted or denied). The demo proves the routing + MCP-tool execution end-to-end, then shows a user with *no* agent access being correctly denied — with both the success and denial visible in the audit log.

## 🔑 Key Takeaways
- **Goal:** facilitate **support-case resolution across different partners within the same ecosystem** using a multi-agent AI workflow.
- The system is a **simple-yet-powerful open-source multi-identity system** purpose-built so **identity-aware workflows** can diagnose and resolve problems.
- Two key building blocks are leveraged: the **Azure MCP server** and the **Red Hat AI secure MCP catalog** (OpenShift AI MCP catalog).
- **MCP catalog = browse → pick → deploy.** The OpenShift AI MCP catalog offers **pre-built MCP servers** you can deploy to your cluster; here the **Azure MCP server** is deployed onto a **Red Hat OpenShift** cluster.
- **No glue code, no custom integration** — you only set the deployment name, project, and connection config; the catalog handles the **container image, configuration, and authentication via managed identity**, and you consume the MCP server as a normal workload.
- **Layered architecture:** (1) user access layer (chat web app), (2) orchestration & security layer (authn/authz/audit), (3) a **routing agent**, and (4) **specialist support agents**.
- **Routing agent** detects the **intent** of each request and **delegates** execution to the right specialist agent (e.g. the **auto support agent**).
- The **auto support agent wraps the Azure MCP server**; tool calls are visible in the output — typically one MCP tool resolves the **intent** and a second performs the **actual execution** that returns the answer.
- **Identity-based access control:** each user can reach only the agents their identity/department permits (demo user has **3 of 4** agents); a user with **no department** (Josh) is **denied** by the routing agent.
- **Full auditability via OpenTelemetry:** every security event is stored, giving an **audit trail / audit log** showing user-to-group access and whether each request was **accepted or denied**.
- Agents were built with **A2A** (Agent2Agent, captioned "8way") as the communication layer and the **ADK (Agent Development Kit)** as the development framework.
- **Everything was live** — the team explicitly framed the ~5-minute session as all real, no slideware.

## 📚 Detailed Notes

### Who & what this is
**Carlos and Sharon, both from Red Hat**, present a lightning demo (ODSP = on-demand / partner-style short session). Their stated objective: show how to **deploy an MCP server from the MCP catalog** and then **use it in a multi-agent application** that **diagnoses and resolves support cases across different partner ecosystems** — "only 5 minutes, all live." The business problem they target is **support resolution across different partners within the same ecosystem**: when an issue spans multiple vendors/partners, you want agents that can route to the right expertise and act on it.

### The core idea: an open-source multi-identity multi-agent system
They built a **simple yet powerful open-source multi-identity system** designed so that **identity workflows can diagnose and resolve problems**. "Multi-identity" is the key framing — access and behaviour are driven by **who the requesting user is** (their identity and group/department membership), not just by what they ask. The two technologies they explicitly lean on:
- **Azure MCP server** — the tool/capability surface the agents call into.
- **Red Hat AI secure MCP catalog** (a.k.a. the **OpenShift AI MCP catalog**) — the catalog from which that MCP server is deployed.

### The layered architecture
The solution is organised into distinct layers:

1. **User access layer** — a **web application** ("a butterfly web application" in the captions; *caption-uncertain* descriptor) that gives users a **chat interface** to interact with routing and support agents.
2. **Orchestration & security layer** — handles all **authentication, authorization, and audit**. This is the control plane that decides who is allowed to do what and records it.
3. **Routing agent** — responsible for **routing requests from users to the specific agent** that can help with their issue. It inspects the request, **detects intent**, and **delegates** accordingly.
4. **Specialist support agents** — the agents that actually troubleshoot, e.g. the **auto support agent**, which **wraps the Azure MCP server** and executes MCP tools to answer.

For the plumbing between agents, they used **A2A** (Agent2Agent protocol — captioned "8way") as the **communication layer**, and built **all the agents in the demo with the ADK (Agent Development Kit)**.

### Step 1 — Deploy the Azure MCP server from the MCP catalog
The **OpenShift AI MCP catalog** gives you **pre-built MCP servers** that you can **browse, pick, and deploy** to your cluster. In this demo they deploy the **Azure MCP server** to their **Red Hat OpenShift** cluster. The deployment UX is deliberately minimal:
- Choose the **deployment name** and the **project**.
- Set up the **configuration details** needed to **connect to your Azure tenant**.
- The catalog then **handles the container image, the configuration, and all authentication through managed identity**.

The repeated emphasis: **"we will not be writing any glue code… we won't be building any custom integration."** You simply **deploy from the catalog** and then **consume the MCP server as a regular workload**. After filling in the details you click **Deploy the Azure MCP server**, wait for the **operator** to run the deployment, and it comes up **ready to use**. (This operator-driven, catalog-based deploy is the heart of the "no integration code" value proposition.)

### Step 2 — Use it: routing agent → auto support agent → MCP tools
With the MCP server live, they log into the **quick start** as a user who has access to the **auto support agent**. Observations:
- This user can see **three out of four agents**, including the **auto support agent**, and can **ask questions out of the box**.
- **Example query 1:** *"the well-architected framework for Azure."* The **routing agent detects the intent** of the request and **delegates execution to the auto support agent**, which **wraps the Azure MCP server**. The output shows the answer **plus all the MCP tools that were executed** — typically the **first tool resolves the intent** of the request and the **second tool performs the actual execution** that returns the correct answer.
- **Example query 2:** *"best practices for developing Azure web applications."* Same flow — the routing agent detects intent, routes the request, and the **specific MCP tools are executed**. Here the **output is a Markdown file** containing the requested best practices. Again you can see the routing agent **delegated to the auto support agent**, the **output**, and then the **MCP tools that were called** (first = intent, second = actual output shown in chat).

This makes the **observability of tool calls** explicit to the user: you don't just get an answer, you see **which MCP tools ran and in what order**.

### Step 3 — Audit trail via OpenTelemetry
Because the app **stores all events using OpenTelemetry**, there's a full **audit log / audit trail** of the application's **security events**. From it you can see, for example, **which users have access to which specific groups**, and **whether each request was accepted or denied**. This ties the multi-agent behaviour back to the **orchestration & security layer** — every action is attributable and reviewable.

### Step 4 — Access control demonstrated (the denial case)
To prove the identity model works, they **re-run the quick start as a different user, "Josh," who has no access to any of the agents**:
- Josh **doesn't belong to any department**, so **none of the agents are able to answer his requests**.
- When Josh asks a question, the **routing agent denies the request**.
- That **denial event is also visible in the audit log / audit trail**, just like the successful requests.

The point: access is **identity- and department-driven**, the **routing agent enforces it**, and **both grants and denials are auditable**. They close with "and this is all — thank you."

### Why this matters
The demo packs three reusable ideas into ~5 minutes: (1) **MCP servers as catalog-deployed workloads** — turning an integration project into a pick-and-deploy operation with managed-identity auth and zero glue code; (2) **multi-agent routing** — a router that classifies intent and delegates to specialist agents that wrap MCP tools; and (3) **identity-governed, fully-audited agent access** — a multi-identity model where what an agent will do for you depends on who you are, with OpenTelemetry capturing every accepted/denied event. Together they sketch a pattern for **cross-partner support resolution** that is both **secure** and **operationally simple** on Red Hat OpenShift.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure MCP server** — Microsoft's MCP server exposing Azure capabilities as MCP tools; deployed from the catalog and wrapped by the auto support agent.
- **Red Hat AI secure MCP catalog / OpenShift AI MCP catalog** — Red Hat's catalog of **pre-built MCP servers** you can browse, pick, and deploy to an OpenShift cluster (handles image, config, and managed-identity auth).
- **Red Hat OpenShift** — the Kubernetes platform/cluster the Azure MCP server is deployed onto; an **operator** runs the deployment.
- **Managed identity** — used by the catalog deployment to authenticate the MCP server to the Azure tenant (no manual credential glue).
- **Multi-agent application (the "quick start")** — the web app demoed; chat front-end over routing + specialist agents.
- **Routing agent** — detects request intent and routes/delegates to the correct specialist agent.
- **Auto support agent** — specialist agent that wraps the Azure MCP server and executes MCP tools to answer support questions.
- **Orchestration & security layer** — handles authentication, authorization, and audit for the whole system.
- **A2A (Agent2Agent)** — the **communication layer** between agents (captioned "8way"; *best-effort correction*).
- **ADK (Agent Development Kit)** — the framework used to **build all the agents** in the demo.
- **OpenTelemetry** — used to store all events and produce the **audit log / audit trail** of security events.
- **Azure Well-Architected Framework** — referenced as a sample query answered via the Azure MCP server.

## 🚀 Announcements / What's New
None explicitly announced. This was a live demo/showcase of an existing open-source multi-agent pattern built on the Azure MCP server and the Red Hat OpenShift AI MCP catalog, not a product launch. (No previews, GA dates, or roadmap items were stated.)

## 💡 Demos
**Single end-to-end live demo (~5 min, "all live"):**
1. **Catalog deploy** — from the **OpenShift AI MCP catalog**, pick the **Azure MCP server**, set deployment name + project + Azure-tenant connection config, click **Deploy**, wait for the **operator**; comes up ready — **no glue code / no custom integration**.
2. **Authorized user flow** — log into the **quick start** as a user with access to the **auto support agent** (sees **3 of 4 agents**). Ask *"well-architected framework for Azure"* → **routing agent detects intent → delegates to auto support agent (wraps Azure MCP server)** → output plus the **MCP tools executed** (1st = intent, 2nd = execution). Ask *"best practices for developing Azure web applications"* → same routing flow → output is a **Markdown file** of best practices.
3. **Audit trail** — open the **OpenTelemetry-backed audit log**: see **user→group access** and **accepted/denied** requests.
4. **Denied user flow** — log in as **"Josh"** (no department, no agent access) → ask a question → **routing agent denies** the request → denial also appears in the **audit log / audit trail**. *Proves the identity-based access control end-to-end.*

## 📊 Notable Stats / Quotes
- **"Only 5 minutes, all live. Let's go."** — the demo's framing; everything shown was real, not slideware (Build catalog lists ~6 min).
- **"We will not be writing any glue code… we won't be building any custom integration."** — the core value proposition of catalog-based MCP deployment.
- **3 of 4 agents** — number of agents the authorized demo user could access (vs **0** for Josh, who belongs to no department).
- **Two MCP tool calls per request** — pattern observed: the **first** resolves the request's **intent**, the **second** performs the **actual execution** returning the answer.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Browse the **OpenShift AI MCP catalog** and deploy the **Azure MCP server** to a test OpenShift cluster end-to-end — confirm the **no-glue-code / managed-identity** claim and time how long the operator deploy takes.
- [ ] Things to try: Build a minimal **routing-agent → specialist-agent** pattern with **ADK + A2A** where the specialist wraps an MCP server, and wire **OpenTelemetry** to capture accepted/denied events.
- [ ] Questions: What exactly is the **"multi-identity"** model backing the routing agent's allow/deny — is it Entra ID groups, OpenShift RBAC, the app's own department mapping, or a combination? How are agent permissions mapped to user departments?
- [ ] Questions: Is the **"butterfly" web app** and this whole demo published as an open-source repo/quick start? (They called it "open source" and a "quick start" — find the link.)
- [ ] Questions: Confirm the captioned **"8way"** is indeed **A2A**, and whether **ADK** here is Google's Agent Development Kit or a Red Hat/MS variant.
- [ ] Relevant to: Designing **secure, auditable multi-agent support systems** across partner ecosystems; MCP-server deployment strategy on OpenShift; identity-governed agent access patterns.

## 🔗 Related
- [[BRKSP94 - Orchestrate specialist agents with NVIDIA Nemotron on Foundry]] — another partner multi-agent talk: orchestrating specialist agents + governing them via identity, with a Foundry managed toolbox of MCP tools.
- [[BRK242 - Turn your agents into action Connect tools APIs documents]] — connecting agents to tools/APIs/MCP, the same "agent wraps tools" pattern shown here.
- [[BRK246 - Foundry IQ Fuel agents with enterprise knowledge]] — grounding/feeding agents, complementary to routing + specialist support agents.
- [[BRK240 - Build context-aware agents]] — building agents that route on intent and act, the architecture this demo embodies.
- [[BRK251 - Build secure and enterprise-ready agents with Agent 365]] — the security/identity/audit angle (authn/authz/audit) that this demo's orchestration layer implements.
- [[BRK252 - From observability to ROI for AI agents on any framework]] — observability/audit-trail theme (here via OpenTelemetry) for agent workflows.
- Source list: [[2026 Build Session List]]

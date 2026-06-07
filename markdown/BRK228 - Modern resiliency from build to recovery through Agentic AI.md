---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/resiliency
  - topic/azure
  - topic/devops
source: https://www.youtube.com/watch?v=nzDPYlNXRf0
session_code: BRK228
event: Microsoft Build 2026
speakers: Abi Manu, Aditi, Shobit
duration_min: 45
aliases:
  - Modern resiliency from build to recovery through Agentic AI
---

# BRK228 — Modern resiliency from build to recovery through Agentic AI

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Abi Manu, Aditi & Shobit (Azure resiliency / reliability product team)  
> **Duration:** ~45 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=nzDPYlNXRf0)

## 🎯 TL;DR
This session walks through Microsoft's reimagined **Azure resiliency** story, centred on a three-phase journey — **Start resilient → Get resilient → Stay resilient** — and the new **agentic AI** capabilities that help users discover and close resiliency gaps. The headline launch is the **public preview of Azure Infrastructure Resiliency Manager**, unifying infrastructure, data, and cyber resiliency in one place with **goals**, advisor-powered **recommendations**, **resiliency drills** (Chaos Studio), and **recovery plans**. Live demos show the **Resiliency Agent in Azure Copilot** generating zonally resilient Bicep from natural language, the **Azure MCP server + Azure Advisor tools** scanning and auto-fixing IaC drift in VS Code/GitHub Copilot, **service groups** making brownfield apps zonally resilient, vaulted backups for ransomware protection, and the new **Azure Advisor AI-powered prioritization** that collapses hundreds of recommendations into a ranked top-5 action plan. It closes by announcing **Azure Chaos Studio workspaces** in public preview (June 11).

## 🔑 Key Takeaways
- Resiliency = designing systems that keep operating when things go wrong; in the real world **failures are expected, not exceptions** (zone outages, regional outages, data loss).
- Azure resiliency rests on **three pillars**: **Infrastructure** (hardware/datacentre failures + planned retirements), **Data** (integrity, availability, recoverability — RPO/RTO via Azure Backup), and **Cyber** (immutable backups + isolated recovery environments to survive ransomware).
- The resiliency **lifecycle** has three phases: **Start resilient** (day-zero), **Get resilient** (close gaps in existing/brownfield apps), and **Stay resilient** (ongoing drills, recovery plans, monitoring) — resiliency is continuous, not a one-time setup.
- **Public preview launch: Azure Infrastructure Resiliency Manager** — manage zonal resiliency via **goals**, **recommendations** (Advisor), **resiliency drills** (Chaos Studio), and **recovery plans** (ordered recovery workflows respecting interdependencies).
- Planning is **shifting from resource-level to application-level** using **service groups** — the whole application must be resilient, not just individual resources. (Foundation laid at Ignite, expanding Azure Business Continuity Center into unified "Azure resiliency".)
- **Resiliency Agent in Azure Copilot** turns natural-language architecture intent into **zonally resilient, modular Bicep templates** — no need to be a resiliency expert or leave the Azure portal.
- The agent surfaces **per-resource zonal-resiliency guidance** (e.g. VMSS needs instances + disks spread across zones; PostgreSQL flexible server needs General/Memory-Optimized tier; Key Vault needs an AZ-supported region) plus a detailed report with top + alternate recommendations.
- End-to-end developer flow stays in-tool: generate Bicep → download to VS Code Web → **create a GitHub pull request** directly from the Resiliency Agent in Azure Copilot.
- **Azure MCP server + Azure Advisor tools** let any AI coding agent (GitHub Copilot, Cursor, Claude, etc.) **scan Terraform/ARM IaC against the Advisor recommendation catalog in one pass** — catching zonal gaps, **retiring SKUs**, and monitoring gaps — then **auto-fix inline** for review/accept so "nothing broken ever ships."
- **Service groups** let you make **brownfield apps zonally resilient**: discover resources (by tag/RG/subscription/resource IDs via ARG), assign a **zonal resiliency goal**, check **posture**, run a **prerequisite check**, then have the agent **enable HA** (demo: HA on a PostgreSQL flexible server, done in minutes).
- Data + cyber resiliency via **Azure MCP server in VS Code**: find unprotected PostgreSQL flexible servers and **configure vaulted backups** (existing vault + policy) for **ransomware protection** and **long-term retention up to 10 years**.
- **Azure Advisor AI-powered experience** intelligently ranks recommendations using real signals — **blast radius, criticality, upcoming deadlines, cost** — to produce a **personalized top-5 action plan** with completion-progress tracking and short/mid/long-term breakdown (next 30 days vs 3 months vs later).
- Export the prioritized plan as **Word or PDF**; **coming soon**: generate work items directly in **Jira / ServiceNow** and assign to teammates.
- **Landing soon: AI-powered resource-level prioritization** — ranks *which specific resources* to fix first within a recommendation, using live signals (HA goals, active service health events, prod vs non-prod).
- **Announced: Azure Chaos Studio workspaces** — public preview **June 11**, a complete reimagining with **application-centric workspaces, new scenarios, and a new agentic service** to rehearse the outages you actually fear.
- The **Azure Advisor AI-powered prioritization experience** is in **limited preview starting today** (sign up by meeting the team after the session — limited spots).

## 📚 Detailed Notes

### What resiliency means & why it matters
Resiliency is about **designing systems that continue to operate even when things go wrong**. In the real world, failures are **expected, not an exception**, and they occur at multiple levels: an **availability zone** can go down, a **regional outage** can occur, or there can be **data loss**. Azure provides primitives to handle these — **availability zones, region repair, region pairing, geo-replication, and backup**. Combining capabilities across zones, region pairs, disaster recovery, and strong backup delivers true **end-to-end resiliency**. The simple goal: **minimize downtime, prevent data loss, and recover quickly** when failures happen.

### The three pillars of resiliency
1. **Infrastructure resiliency** — withstanding **hardware failures, issues, or datacentre outages**, and accounting for **planned retirements** (e.g. a SKU being retired in a month). It's about designing systems to handle these failures.
2. **Data resiliency** — maintaining **data integrity, availability, and recoverability** at all times; ensuring critical data has a defined **RPO and RTO** so you can recover from failures. **Azure Backup** is the example primitive.
3. **Cyber resiliency** — even with the best IT defenses, **ransomware and cyber attacks happen**. The goal is **immutable backups, isolated recovery environments**, and the ability to recover when attackers strike your data systems and environments.

### The resiliency lifecycle (Start → Get → Stay)
- **Start resilient** — build resiliency **from day one/day zero**. Azure offers availability zones, region pairs, architecture best practices, and tooling like the **Resiliency Agent in Azure Copilot** and **Advisor tools via Azure MCP** to build resilient apps from the start.
- **Get resilient** — workloads evolve; **brownfield apps** accumulate new services, databases, and systems. The aim is to **know the gaps** and close them. **Resiliency Agent + backup tools via Azure MCP** let you proactively **assign resiliency goals, find gaps, and mitigate**. With real apps producing tons of recommendations, **Azure Advisor AI-powered experiences** help **prioritize** what matters.
- **Stay resilient** — resiliency is an **ongoing exercise**, not a one-time setup. Capabilities like **resiliency drills, recovery plans, service health, and Azure Advisor** help **detect, monitor, and stay resilient**.

Overall framing: resiliency isn't just **surviving failures** — it's building systems that **continuously adapt, learn, and improve over time**.

### Context from Ignite → unified "Azure resiliency"
At **Ignite last year**, Microsoft significantly **expanded the scope of the Azure Business Continuity Center**, introducing **"resiliency in Azure"** — a **unified solution** bringing infra/data/cyber capabilities into a **single place** that surfaces **high-impact risks**, simplifies **remediation**, and enables **proactive planning**. A key concept introduced then: stop looking at **individual resources alone** and instead evaluate the **sum** — i.e. **the whole application** (e.g. an "Ask HR" app) is either resilient or not. This is the shift from **resource-level to application-level** business-continuity planning, implemented via **service groups**. These resiliency experiences can be managed via **Azure portal, PowerShell, CLI, and Azure Copilot** — with intelligent guidance/remediation pushed into developer workflows including **GitHub Copilot**.

### Launch: Azure Infrastructure Resiliency Manager (public preview)
The first concrete step bringing this vision together. It lets customers manage **zonal resiliency** through several capabilities:
- **Goals** — declare an intent (e.g. "my entire application must be zonally resilient") and drive toward it.
- **Recommendations** — powered by **Advisor**, to help you get resilient.
- **Resiliency drills** — **simulate failures** (e.g. a zone going down), powered by **Chaos Studio**, to test your app's resiliency posture in a controlled way rather than discovering gaps during a real outage.
- **Recovery plans** — for real outages where many resources must be recovered in order (fail over a DB, fail over a VM, etc.) with interdependencies. Recovery plans let you create a **workflow defining the order** in which resources are recovered.

> The presenters repeatedly encourage trying the **public preview** experience.

### Phase 1 — Start resilient (Resiliency Agent in Azure Copilot)
Traditionally, building resilient apps required **deep expertise** — knowing which properties/resources to enable and what they do, and resiliency often became an **afterthought** (build first, then realize you need to be resilient). The Resiliency Agent changes this by bringing **intelligence and a guided, natural-language experience**: whether an app is a web app, VM, or PostgreSQL database, you **express your architecture intent** and the agent converts it into **zonally resilient templates**.

**Demo 1 — "Start green" with new IaC (Zava Payroll):** Persona = cloud DevOps engineer tasked with creating a new "Zava Payroll" app (compute via VMSS + a PostgreSQL database) and making it zonally resilient.
- In **Azure portal → Resiliency → Copilot**, the chat opens on the right and is expanded to full screen.
- Prompt: *create zonally resilient templates with the app in **East US** in resource group **Zava apps**, a **VMSS with 5 instances**, a **PostgreSQL flexible server**, all **connection strings/passwords sourced from a Key Vault**, and a **modular structure of Bicep templates**.*
- The agent maps the intent to Azure services and explains what makes each **zonally resilient** via a **zonal resiliency support column**:
  - **VMSS** — guidance on how to make it zonally resilient.
  - **PostgreSQL flexible server** — tier must be **General Purpose or Memory Optimized**.
  - **Key Vault** — must be in an **availability-zone-supported region**.
  - Confirms **East US supports zone redundancy / availability zones** (matching the stated region requirement).
- The agent generates a **detailed report**: an overview of *why* zonal resiliency matters and its impact, plus **per-resource-type recommendations**. For **VMSS**: spread instances across AZs **and** make disks zonally resilient; also **alternate recommendations via ASR**. Similar recommendation sets for **PostgreSQL** and **Key Vault**, plus **cross-cutting considerations** and a **summary checklist** at the bottom.
- A suggested prompt **generates the Bicep templates**: a **`main.bicep`** entry point plus **modular Bicep files per resource type** (identity, network, key vault, etc.), a **`parameters.json`**, and **deployment instructions**.
- Outputs are attachable/expandable in the chat (tabs per Bicep file). You can **download into VS Code Web** and interact directly.
- The demo finishes by **creating a GitHub pull request** straight from the Resiliency Agent in Azure Copilot: log into GitHub, choose the repo and branch, **update pull request**, then **review pull request** in GitHub. Whole flow: **intent → resilient IaC → PR**, never leaving Azure Copilot.

**Demo 2 — "Start green" with existing IaC drift (Zava Commerce, Azure MCP + Advisor in VS Code):** Many developers live in code editors and aren't starting from scratch — existing IaC accumulates **drift** over time. The **Azure Advisor tool in Azure MCP** addresses this. Configure **Azure MCP** in your AI coding agent of choice; then with a **single prompt** you can scan your **entire IaC (Terraform or ARM)** against the **Advisor recommendation catalog** in **one pass** — surfacing not just zonal-resiliency risks but also **retiring SKUs, monitoring gaps**, and other reliability risks. It **auto-fixes** issues with changes presented **inline** for review/accept, so **nothing broken ever ships** and your infra is resilient **before it touches Azure** ("start green, don't fix it later").
- Persona = developer on the **Zava Commerce** app (VMs + container registries) with pre-authored **ARM templates** that have gone stale (drift, behind-on SKUs, hard-to-catch gaps).
- In **VS Code** with **Azure MCP server** configured, open the ARM templates (one VM, one container registry), open **GitHub Copilot**, and ask it to **check for reliability issues and fix them**.
- Behind the scenes it calls **Azure Advisor tools**, scans the files, and finds **two issues**:
  1. **Container registry on Basic SKU** → recommends upgrading to **Premium** to unlock **geo-replication, availability zones, and private endpoints**.
  2. **VM using an F-series SKU that is retiring soon** → flagged as costly/hard to fix later if shipped as-is.
- The flow **auto-fixes both** in a **single pass** (upgrades registry Basic→Premium; recommends a replacement VM SKU). All changes are reviewable **inline** so you keep only what makes sense. Result: scan + fix all issues without leaving the editor, in minutes.

### Phase 2 — Get resilient (brownfield apps via service groups)
Goal: make **already-deployed (brownfield) apps zonally resilient**. Doing this manually is **complex and time-consuming**. Approach: put an application's resources into a **service group**, analyze the **posture**, then use the **Resiliency Agent** to make it zonally resilient.

**Demo 3 — Zava Ask HR (VM + PostgreSQL flexible server):**
- In **Azure portal → Resiliency blade**, the starting point is **creating a service group** via **Azure Copilot**.
- To populate it you can supply **resource IDs** or use **criteria** (resource group, subscription, or **tag**). Demo uses the **tag** `Zava ask HR` and names the service group **Zava ask HR**.
- Copilot runs an **ARG query**, **discovers two resources** (a **VM** and a **PostgreSQL flexible server**), and creates the service group. (Note: equally works for other stacks, e.g. an **AKS cluster + Cosmos DB**.)
- Verify membership via **Service group blade → Members** (confirms 1 VM + 1 PostgreSQL).
- Back in chat, **assign a zonal resiliency goal** to the service group (request submitted; takes a few minutes). After confirming the goal is assigned, **check posture** — both resources are reported **not zonally resilient** (a **posture report** can be downloaded as **PDF**).
- Run a **prerequisite check** to see whether resources can be made zonally resilient and surface blockers — it reports it **can enable HA** for both the VM and the PostgreSQL flexible server.
- Demo enables HA on the **PostgreSQL flexible server**: the **agent configures HA**, and it becomes **zonally resilient** — brownfield app made resilient in **minutes with a few clicks**.

**Demo 4 — Data + cyber pillars (vaulted backups via Azure MCP in VS Code):** Once zonally resilient, is the app also **data- and cyber-resilient**? Use the **Azure MCP server in VS Code** to configure **vaulted backups** and protection for the PostgreSQL flexible server — guarding against **ransomware** and meeting compliance via **long-term retention up to 10 years**.
- Verify the **Azure MCP server extension** is installed and `mcp.json` is configured correctly; **start the Azure MCP server**; initiate chat.
- Prompt: check whether the **Zava Ask HR** app has an **unprotected PostgreSQL flexible server** (not protected by Azure Backup). An **ARG query** returns **`Zava ask HRDB`** as unprotected, with its **resource group and location**.
- Prompt to **configure protection** for `Zava ask HRDB`. Backups need a **backup vault + backup policy in the same region**; it finds an existing **Zava vault** and a **"PostgreSQL daily" backup policy** in-region and creates a **protected item** (named on screen).
- Verify via another **ARG query** — confirms the **protected item was created** and the PostgreSQL flexible server is now **protected**.

### Azure Advisor AI-powered prioritization
Real apps can have **hundreds of reliability gaps** (zonal gaps, **retiring SKUs**, monitoring gaps). The hard part isn't only knowing something must change — it's knowing **what to prioritize first** to reduce risk. **Azure Advisor's AI-powered experience** builds a **personalized, prioritized action plan** you can run with immediately, **ranking recommendations using real signals**: **blast radius, criticality, upcoming deadlines, and cost implications**. For each action item you get **completion-progress tracking** (what's done vs still exposed) and a downloadable **custom action plan** broken into **next-30-days vs later**.

**Landing soon — AI-powered resource-level prioritization:** for each recommendation, Advisor will rank **which specific resources** to fix first (since apps have hundreds of resources), using **live signals**: whether an **HA goal** is set, whether a resource is hit by an **active service health event**, and **prod vs non-prod** distinctions. So you'll know not only **which issue types** to prioritize but also **which resources** within them to start with.

**Demo 5 — Zava Ask HR grown into an internal HR chatbot:** The app has grown from VM+PostgreSQL into an **internal HR chatbot** on **App Services** with **Storage accounts, Cosmos DB, Redis cache**, plus a dependency on another app, **Zava People** (people/org data). Opening **Advisor** floods the developer with **hundreds of recommendations across two subscriptions**.
- A new **Azure Advisor AI-powered widget** lights up in the **Overview** blade. Click it → **select a subscription** (Zava Ask HR app) → **continue**.
- Provide intent via prompt: **"improve the reliability."** Optionally add **additional subscriptions/resource groups** — here, the dependent **People app** is selected — then ask it to **fetch all reliability recommendations**.
- Advisor scans both subscriptions and returns **just five recommendations** to start with. For each it shows the **active resources to address, completion-progress rate, potential benefits**, and crucially the **"why"** behind its ranking:
  - **#1 — Service retirement** for a **Storage account**, losing support in the **next 30 days** → biggest gap; the **hard deadline** puts it at the top.
  - **#2 & #3 — Zonal resiliency** recommendations. **Cosmos DB has no zone redundancy**, ranked above another zonal recommendation because a Cosmos DB failure takes out the **entire primary data tier** (**wider blast radius** than losing a **cache layer**). This shows ranking is **environment-specific**, based on the user's own data/context.
- Clicking a recommendation opens a **details page**: what it's about, when support ends, **remediation steps**, and exactly **which resources are impacted** — everything needed to act in one place.
- An **action plan** at the bottom is split into **short / mid / long term** (next 30 days, next 3 months, later). The list can be **exported as Word or PDF** to coordinate remediation offline.
- **Coming soon:** generate these action items as **work items in Jira or ServiceNow** and assign them to teammates.
- Drilling into the **Cosmos DB** recommendation shows the **specific affected resources**; **landing soon** this list will be **individually ranked by priority** using live environment signals.
- Wrap-up: in under two minutes, **hundreds of recommendations → top 5 + environment-specific action plan**. Microsoft will keep refining and will bring **resiliency flows and Advisor flows closer together** for one seamless end-to-end resiliency experience. This experience is in **limited preview starting today** (limited spots; sign up after the session).

### Phase 3 — Stay resilient (Azure Chaos Studio workspaces)
A critical part of staying resilient is **validating** that your resilience is what you *think* it is. Every Azure customer **believes they're resilient until** an AZ goes down, **AI workloads silently degrade**, or **throttling cascades** to take out **checkout during Black Friday**. This is where **Azure Chaos Studio workspaces** come in.

**Announcement:** launch of **Chaos Studio workspaces in public preview on June 11** — a **complete reimagining** with **application-centric workspaces, new scenarios, and a new agentic service**, letting you **rehearse the outages you actually fear**. The session closes and opens to **Q&A**.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Infrastructure Resiliency Manager** — newly launched (public preview) solution to manage zonal resiliency via goals, recommendations, drills, and recovery plans.
- **Azure resiliency (unified)** — single place bringing infra/data/cyber resiliency together; evolution of the Azure Business Continuity Center (expanded at Ignite).
- **Azure Business Continuity Center** — prior home for backup/DR; scope expanded into unified Azure resiliency.
- **Resiliency Agent (in Azure Copilot)** — agentic, natural-language experience that turns architecture intent into zonally resilient templates and remediates gaps.
- **Azure Copilot** — AI assistant in the Azure portal hosting the Resiliency Agent / resiliency chat.
- **Service groups** — group an application's resources so resiliency is assessed/managed at the application level (assign goals, check posture).
- **Resiliency goals** — declarative intent (e.g. zonal resiliency / HA) applied to a service group.
- **Posture (report)** — assessment of whether resources meet the assigned resiliency goal; downloadable as PDF.
- **Prerequisite check** — checks whether resources can be made zonally resilient and surfaces blockers before remediation.
- **Resiliency drills** — simulate failures (e.g. a zone going down) to test resiliency posture; powered by Chaos Studio.
- **Recovery plans** — ordered recovery workflows that respect resource interdependencies during a real outage.
- **Azure Advisor** — recommendation engine for reliability (and other categories); source catalog for IaC scans.
- **Azure Advisor AI-powered experience / widget** — AI prioritization that ranks recommendations into a personalized top action plan.
- **Azure Advisor tool (in Azure MCP)** — scans IaC against the Advisor catalog and auto-fixes issues from the coding agent.
- **Azure MCP server** — Model Context Protocol server exposing Azure tools (Advisor, backup, ARG, etc.) to AI coding agents.
- **GitHub Copilot** — AI coding agent used in VS Code to invoke Azure MCP/Advisor tools and apply inline fixes.
- **VS Code / VS Code Web** — code editors used for IaC editing, MCP integration, and downloading generated Bicep.
- **Bicep** — IaC language; agent generates modular Bicep (`main.bicep` + per-resource modules + `parameters.json`).
- **ARM templates** — existing IaC scanned for drift/SKU/reliability issues.
- **Terraform** — supported IaC format for Advisor-via-MCP scanning.
- **Azure Resource Graph (ARG)** — queried to discover resources, build service groups, and verify protection state.
- **Availability zones / zone redundancy** — core zonal-resiliency primitive (e.g. East US AZ support).
- **Region pairs / region repair / region pairing** — regional resiliency primitives.
- **Geo-replication** — data redundancy primitive (e.g. unlocked by ACR Premium).
- **Azure Backup** — managed backup for RPO/RTO and data resiliency.
- **Vaulted backups** — isolated, immutable-style backups for ransomware protection and long-term retention (up to 10 years).
- **Backup vault & backup policy** — required (same-region) constructs to protect a resource (e.g. "PostgreSQL daily" policy).
- **Azure Site Recovery (ASR)** — alternate path for making resources (e.g. VMSS) zonally resilient.
- **Azure Chaos Studio / Chaos Studio workspaces** — fault-injection/chaos engineering; powers drills; workspaces launching in public preview.
- **Virtual Machine Scale Sets (VMSS)** — compute resource; resilient by spreading instances + disks across zones.
- **Azure PostgreSQL flexible server** — database; zonally resilient via HA + General/Memory-Optimized tier.
- **Azure Key Vault** — secrets store for connection strings/passwords; needs AZ-supported region.
- **Azure Container Registry (ACR)** — registry; Premium SKU unlocks geo-replication, AZs, private endpoints.
- **Azure Cosmos DB** — database; flagged for missing zone redundancy (primary data-tier blast radius).
- **Azure Redis cache** — cache layer (lower blast radius than the primary data tier).
- **Azure App Service** — hosting for the evolved HR chatbot app.
- **Azure Storage account** — flagged for an impending service-retirement (support ending in 30 days).
- **Azure Kubernetes Service (AKS)** — cited as an alternative service-group stack (with Cosmos DB).
- **Azure Service Health** — active service-health events used as a live prioritization signal.
- **Jira / ServiceNow** — external work-item systems; future target for generating/assigning remediation work items.
- **Zava (Payroll / Commerce / Ask HR / People)** — fictional demo applications used throughout.

## 🚀 Announcements / What's New
- **Azure Infrastructure Resiliency Manager — public preview** (available now): manage zonal resiliency via goals, Advisor-powered recommendations, resiliency drills (Chaos Studio), and recovery plans. Presenters invite trial.
- **Resiliency Agent in Azure Copilot** — generate zonally resilient Bicep from natural-language intent and remediate brownfield gaps (shown live; part of the resiliency preview experience).
- **Azure Advisor tool in Azure MCP server** — single-prompt IaC scanning (Terraform/ARM) against the Advisor catalog with inline auto-fix across reliability categories (zonal, retiring SKUs, monitoring).
- **Azure MCP server backup tooling** — configure vaulted backups / ransomware protection for PostgreSQL flexible server from VS Code.
- **Azure Advisor AI-powered prioritization** — **limited preview starting today** (limited spots; sign up by meeting the team after the session). Ranks recommendations into a personalized top-5 action plan with short/mid/long-term breakdown and Word/PDF export.
- **AI-powered resource-level prioritization (Advisor)** — **landing soon**: ranks which specific resources to fix first using live signals (HA goals, active service health events, prod/non-prod).
- **Jira / ServiceNow work-item generation (Advisor)** — **coming soon**: create and assign remediation work items directly in external systems.
- **Azure Chaos Studio workspaces — public preview on June 11**: complete reimagining with application-centric workspaces, new scenarios, and a new agentic service.
- **Roadmap intent:** bring the resiliency flows and Advisor flows closer together for a single, seamless end-to-end resiliency experience.

## 💡 Demos
1. **Start green — new IaC (Zava Payroll):** In Azure portal → Resiliency → Copilot, a natural-language prompt produced per-resource zonal-resiliency guidance (VMSS, PostgreSQL, Key Vault) + a detailed report, then generated modular Bicep (`main.bicep` + modules + `parameters.json`) and created a **GitHub PR** directly from the Resiliency Agent. *Proves:* you can go from intent → resilient IaC → PR without leaving Azure Copilot or being a resiliency expert.
2. **Start green — existing IaC drift (Zava Commerce):** In VS Code with Azure MCP configured, GitHub Copilot called Azure Advisor tools to scan ARM templates, found a **Basic-SKU ACR** (recommend Premium for geo-replication/AZs/private endpoints) and a **retiring F-series VM**, then **auto-fixed both in one pass** with inline review. *Proves:* a single prompt catches and fixes multiple reliability risk types pre-deployment, so nothing broken ships.
3. **Get resilient — brownfield service group (Zava Ask HR):** Created a service group by tag via Azure Copilot (ARG discovered VM + PostgreSQL), assigned a zonal goal, checked posture (both not resilient), ran a prerequisite check, and the agent **enabled HA on the PostgreSQL flexible server** to make it zonally resilient. *Proves:* brownfield apps can be made zonally resilient at the application level in minutes.
4. **Data/cyber — vaulted backups (Zava Ask HR DB):** In VS Code via Azure MCP, found an **unprotected PostgreSQL flexible server** (ARG), then configured a **protected item** using an existing in-region vault + "PostgreSQL daily" policy and verified success. *Proves:* ransomware protection / long-term retention can be configured agentically from the editor.
5. **Advisor AI prioritization (Zava Ask HR chatbot + Zava People):** The Advisor AI widget scanned **two subscriptions** and collapsed **hundreds of recommendations into a top 5**, each with the "why" (e.g. **storage-account service retirement in 30 days** #1; **Cosmos DB no zone redundancy** ranked above a cache-layer gap due to **blast radius**), plus a short/mid/long-term action plan exportable to Word/PDF. *Proves:* environment-aware ranking turns recommendation overload into an actionable plan.

## 📊 Notable Stats / Quotes
- **3 pillars** of resiliency: infrastructure, data, cyber.
- **3 lifecycle phases:** start resilient, get resilient, stay resilient.
- **VMSS demo:** **5 instances** requested.
- **Vaulted backup retention:** **up to 10 years** for compliance/long-term retention.
- **Advisor prioritization:** **hundreds of recommendations → top 5** to start with; action plan split into **next 30 days / 3 months / later**.
- **#1 prioritized risk in demo:** storage-account **service retirement with support ending in 30 days**.
- **Chaos Studio workspaces public preview:** **June 11**.
- *"In the real world failures are not an exception. They are expected."*
- *"Resiliency is not a one-time setup. It's an ongoing exercise."* — systems should *"continuously adapt, learn, and improve over time."*
- *"Nothing broken ever ships"* — IaC made *"resilient even before it touches Azure"* ("start green").
- *"Every Azure customer believes that they are resilient until... an availability zone goes down, your AI workloads silently degrade, or a throttling cascades down to take out checkout during Black Friday."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Spin up the **Azure Infrastructure Resiliency Manager** public preview and create a **service group** for a real app; assign a **zonal goal** and check posture.
- [ ] Things to try: Configure **Azure MCP server** in VS Code + GitHub Copilot and run a single-prompt **Advisor scan** over existing ARM/Terraform IaC; review inline fixes.
- [ ] Things to try: Use the **Resiliency Agent in Azure Copilot** to generate **zonally resilient Bicep** for a sample stack (VMSS + PostgreSQL flexible server + Key Vault) and open a PR.
- [ ] Things to try: Configure **vaulted backups** for a PostgreSQL flexible server (ransomware protection / long-term retention) via Azure MCP.
- [ ] Things to try: Sign up for the **Azure Advisor AI-powered prioritization** limited preview; mark **June 11** to check out **Chaos Studio workspaces** public preview.
- [ ] Questions: Which Azure resource types are covered by service-group **zonal goals / auto-HA** today vs roadmap (AKS, Cosmos DB, App Service)?
- [ ] Questions: How does Advisor's **blast-radius / criticality** ranking weight signals, and can the prioritization logic be tuned per org?
- [ ] Questions: What are the exact prerequisites/limits for **Azure MCP server** backup operations and Advisor IaC auto-fix (auth, scopes, supported file types)?
- [ ] Questions: For **recovery plans**, how are interdependency ordering and failover steps defined/tested?
- [ ] Relevant to: Azure landing-zone / WAF Reliability pillar guidance; DR runbooks; resiliency drills program; IaC CI gates ("start green"); ransomware/backup compliance posture.

## 🔗 Related
- [[2026 Build Session List]]
- Microsoft Build 2026 — Azure resiliency / reliability sessions
- Azure Well-Architected Framework — Reliability pillar
- Azure Chaos Studio / chaos engineering notes
- Azure Backup & vaulted backups / ransomware protection
- Azure MCP server & GitHub Copilot agentic IaC workflows

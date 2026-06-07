---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/dotnet
  - topic/modernization
  - topic/agents
  - topic/azure
  - topic/app-service
  - topic/mcp
source: https://www.youtube.com/watch?v=wtUD8IV7rdA
session_code: OD801
event: Microsoft Build 2026
speakers: Andrew Westgarth, Grace Sef, Gaurav (Azure App Service PMs)
duration_min: 49
aliases:
  - Modernize intelligent apps and agents with NET that scale as you grow
---

# OD801 — Modernize intelligent apps and agents with .NET that scale as you grow

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Andrew Westgarth (Product Manager, Azure App Service), Grace Sef (Product Manager, Azure App Service), Gaurav (Product Manager, Azure App Service — demo)  
> **Duration:** ~49 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=wtUD8IV7rdA)

> [!note] Caption-uncertain names
> Speaker names are auto-caption-derived. "Andrew Westgarth" (rendered "Weskarth") is the well-known Azure App Service PM. "Grace Sef" and the demo presenter "Gaurav" (rendered variously "Gorov / Garav / Gav") are best-effort corrections and may be spelled differently.

## 🎯 TL;DR
This Azure App Service session shows how to **move existing .NET (especially .NET Framework / Windows) applications to PaaS and then make them intelligent** — without a costly rewrite. The centrepiece is **Managed Instance on Azure App Service** (public preview, launched at Ignite Nov 2025), which lets you bring Windows/third-party dependencies, registry access, drive-letter storage mounts, custom install scripts, and even **Bastion-secured RDP** into a fully managed PaaS that scales 1→N instances at a click. The headline Build 2026 announcement is **built-in MCP for App Service**: surface an existing REST API and App Service auto-generates an **MCP server** (one tool per API method), secured by managed identity / OAuth / RBAC, so legacy APIs become AI-consumable tools for agents and coding assistants. The session also covers **agentic application patterns** (orchestrator + specialised domain agents), the **GitHub Copilot app modernization tooling** in Visual Studio (AI-assisted assessment + refactoring for .NET and Java), and new **agent observability** (App Insights-backed agent metrics in the portal). A long live demo stitches all of it together: assess → migrate → configure → expose as MCP → observe.

## 🔑 Key Takeaways
- **Managed Instance on App Service = lift-and-modernize PaaS for Windows/.NET Framework apps** — bring Windows dependencies along instead of rewriting (public preview today; launched at Ignite Nov 2025).
- Five recurring modernization blockers are called out: **legacy system dependencies, stateful design, scattered config/secret management, and long migration timelines** — Managed Instance is positioned to dissolve the first set.
- **Zero-to-minimal code changes is the stated design goal** — preserve registry access, drive-letter mounts, third-party MSIs, and OS roles via a **custom install script (`install.ps1`)**, ideal when you don't own the source or can't touch a critical third-party app.
- **Custom dependencies install via an `install.ps1` packaged in a zip** (with any MSIs/fonts/components) uploaded to a storage account; App Service downloads, unzips, and runs it on each instance — re-applied automatically on maintenance/scale so customizations persist.
- **Registry read/write is supported**, with the actual registry values stored as **Key Vault secrets** — full secure secret chain end-to-end.
- **Storage mounts with drive letters** (e.g. `J:`) map to **Azure Files, a VNET UNC share, or local temp storage**; connection strings are held as Key Vault secrets. ⚠️ Local mounts are **ephemeral** (lost on restart).
- **First-ever Bastion-secured RDP into App Service instances** for troubleshooting with familiar tools (Event Viewer, regedit, MMC, IIS) — but **RDP changes are non-persistent**; bake everything into the install script.
- **Built-in MCP (NEW at Build 2026, preview):** App Service detects your API and **auto-exposes it as an MCP server** — one **tool call per REST method** — making legacy/.NET Framework APIs usable by agents and coding assistants.
- Built-in MCP is **language-agnostic** (.NET, Java, Node.js, Python) and **secured via managed identity, OAuth, and RBAC** with auditable interactions.
- **You feed an OpenAPI-compliant JSON spec** and configure auth; App Service generates the MCP server at a chosen endpoint path — consumers reference it in `mcp.json` and immediately call the tools.
- **Agentic pattern = orchestrator + specialised domain agents** (e.g. sales, product, shipping); the orchestrator picks the most efficient execution sequence, and per-agent modularity enables **granular, independent scaling**.
- **Agentic design works with both greenfield and existing/legacy systems** — you don't need a brand-new language or rewrite to participate in agent workflows.
- **GitHub Copilot app modernization tooling (in Visual Studio)** runs an **AI assessment** that reports mandatory vs. potential issues per Azure target, generates refactored code, and accelerates greenfield scaffolding — supports **.NET and Java**.
- **Target choice matters in the assessment:** the same .NET Framework app shows **0 mandatory / 4 potential** issues for App Service Managed Instance vs **2 mandatory** for App Service (Windows), because the classic Windows sandbox blocks registry writes and MSI installers — Managed Instance auto-resolves those blockers.
- **Premium v4 (Pv4) only:** Managed Instance currently runs on **Pv4 SKUs** (e.g. P1 V4), described as the most performant SKU in the fleet with attractive Windows pricing.
- **New agent observability:** with App Insights configured, the portal shows **agent count, call volume, token usage, and error rate** (demo: 5 agents, 52 calls, last 30 days) with drill-through to App Insights logs.

## 📚 Detailed Notes

### Session framing & agenda
Andrew Westgarth and Grace Sef (Azure App Service PMs) open by previewing new App Service capabilities aimed at accelerating cloud migration **and** AI adoption. The agenda:
1. Understand the common **modernization challenges** organizations hit.
2. Review **Managed Instance on Azure App Service** (launched at Ignite, Nov 2025).
3. Introduce the Build 2026 launch: **built-in MCP** — expose APIs as AI-consumable tools.
4. Show how **GitHub Copilot app modernization tooling** assesses apps and makes code changes across languages.
5. A full **live demo** by their colleague Gaurav.
6. Wrap-up with summary + key resources.

### Understanding modernization challenges
From years of customer research, the team groups blockers into a few categories:

- **Legacy system dependencies.** Heavy reliance on specific OS features — e.g. **MSMQ client, SMTP**, Windows APIs like **GDI drawing libraries** — plus third-party reporting libraries, control sets, or in-house components. Traditional PaaS (incl. classic App Service) **doesn't let you install third-party/self-built components via MSIs/EXEs**, which blocks migration. (This session directly addresses that.)
- **Stateful vs. stateless design.** Apps that lean on in-memory **session management** can't scale massively; stateless architectures (externalizing state to a database, table storage, or a Redis cache — caption said "radius") give scalability and flexibility out of the box. Some customers solved this on-prem; others surface it during cloud adoption.
- **Configuration & secret management.** Enterprises accumulate **scattered, non-centralized** config services and shared secrets unique to each flow. The challenge is **centralized governance and secure management** — where Azure (Key Vault + managed identity) helps.
- **Migration timelines.** After an assessment, teams face many tasks; even "simple" modernization can take **multiple months**. The goal is to **shorten that and raise ROI**.

### Managed Instance on Azure App Service — overview
Introduced at **Ignite (November 2025)**, **public preview today**. Goal: **accelerate the move to PaaS** with extreme flexibility but high scale.

- **Preserve Windows dependencies** — bring third-party and Windows Server OS dependencies along.
- **Unlock scale** — go from **1 instance to ~30** quickly via a few clicks, a template deployment, or a CLI command, instead of racking servers / building VMs / physical tin.
- **Security by design** — uses **managed identity** to talk to SQL (database backends), Key Vault (secrets + certificate management), etc.
- **Add Azure AI value immediately** — layer **agents and MCP** onto legacy apps.
- **Premium v4 SKU** — deploys on **Pv4**, the most performant SKU in the fleet, with attractive pricing specifically for Windows customers.

### Managed Instance — foundation for cloud adoption (zero/minimal code changes)
The explicit design goal is **minimal — ideally zero — code changes**:

- Use a **configuration/install script** to bring dependencies, install **server roles/features**, or make needed changes.
- **Read/write the registry**, storing those key values in **Key Vault** → secure secret chain end-to-end.
- **Mount storage volumes with drive letters** (common on-prem pattern) rather than only UNC paths.
- This preserves existing dependencies/config **without any code change**, which is critical when you **don't have the source code** or it's a **third-party app you can't modify** but is business-critical (e.g. during a data-center shutdown / forced migration).

### Managed Instance — cloud-native benefits out of the box
- **Scalability:** horizontal (1→N instances immediately) **and** vertical — start small (single core, low RAM) up to **32 cores / 256 GB RAM**, at the click of a button vs. long procurement.
- **High security:** managed identities required throughout, used to connect to other Azure services to improve posture from day one.
- **High availability:** multiple instances plus **availability zones** for resiliency.
- **Operational offloading:** as PaaS, Microsoft handles **infrastructure maintenance, patching, scaling** — freeing dev teams to focus on value and eliminating ops cost of patching instances.
- **Incremental modernization pathway:** Managed Instance can be a **final destination** (just get to the cloud) **or** a launchpad — once you're "in the App Service stable," you can later rewrite **core components** in a newer language (e.g. .NET Core) **piecemeal**, reducing risk and time-to-value instead of rewriting everything before moving.

### Managed Instance — capability details
- **Data management backed by Key Vault** — secrets, credentials, config settings all in Key Vault, integrated with managed identity.
- **Storage compatibility** — drive-letter mapping onto **Azure Files, local temporary storage, or a UNC file share inside your VNET**, maintaining app compatibility.
- **Custom dependency installations** — an **install script** includes custom dependencies for legacy components (third-party, or OS components not installed by default).
- **Bastion-secured RDP (first time ever in App Service)** — remote desktop directly to instances over **Azure Bastion** with a secure protocol, giving **full access** to use familiar tools (Event Viewer, registry viewer, server manager) for troubleshooting/investigation.
  - ⚠️ **RDP-session changes are temporary** — they must be backed by the **install script** to persist, because when Microsoft does maintenance or **replaces instances**, customizations are re-applied from the script.
- **Dynamic scaling and maintenance** — configure auto-scale by application need, or scale manually / on a schedule; OS updates and maintenance are handled by the platform team.

### Built-in MCP (the Build 2026 launch)
A **new App Service feature announced at Build 2026** that **adds AI value to apps immediately** by turning **APIs into AI tools**:

- You **surface an API**; App Service **detects and discovers** it inside your app and **exposes MCP tooling** you can incorporate elsewhere.
- **Secured via managed identity, OAuth, and RBAC**, keeping **auditable API interactions**.
- **Language-agnostic** — supports **.NET, Java, Node.js, and Python**.
- **Architecture shown in the demo:** a **.NET Framework inventory web API** running on Managed Instance is already exposed as an API; built-in MCP exposes it so its capabilities (built years ago) can be consumed by **modern development frameworks** and agents.

### Agentic application patterns
App Service can host **agent-based modular designs**:

- **Specialised agents per domain** — e.g. a **sales** agent, **product** agent, **shipping** agent — each exposing distinct, task-focused functionality (more modular than a monolith).
- **Orchestrator coordination** — an orchestrator receives requests and determines the **most efficient execution sequence** and which agents to involve.
- **Granular scalability** — because agents are split by task, scaling can flex independently as user demand evolves.
- **Works with legacy + greenfield** — agentic design **does not require** brand-new greenfield projects in the latest languages; you can integrate **existing legacy systems** alongside new ones.

### GitHub Copilot app modernization tooling
The bridge between "old app" and "cloud-ready app":

- **AI-assisted code modernization** — Copilot analyzes **legacy and modern** codebases and **generates refactored code** aligned with modern architecture practices, identifying improvements that reduce cloud-migration problems and align with newer paradigms.
- **Fast greenfield development** — with the right prompts/scaffolding, generate **new APIs, tests, deployment scripts**, and prototypes quickly.
- **Multi-language** — covers **.NET and Java**, versatile across enterprise project types.
- **Built into Visual Studio** and **integrates directly with platforms like Azure App Service**, enabling **modernization assessments** to find problems/improvements **before** moving to App Service → faster cycles, better collaboration, no piecemeal migrations.
- Also handles **other app types** — e.g. moving a **.NET or Node.js app to App Service Linux** uses the same tooling.

### Demo walkthrough (Gaurav) — Part 1: GitHub Copilot app modernization assessment
- Starts with a **classic ASP.NET / .NET Framework web app** containing web forms + an **API controller**.
- Dependencies shown: **log4net** writing logs to **local disk**, a **local SMTP server** writing mail to local disc, and a **database connection string stored in a registry key**.
- To assess: **right-click solution → Modernize → "Migrate to Azure"**, wait for the assessment.
- The **assessment report** proposes Azure targets. For .NET Framework web apps the **default target is Azure App Service Managed Instance**.
  - Example guidance: for **logging**, if targeting Managed Instance, **prefer App Insights or App Service logging**; if file-system logs are required, **write to a mounted Azure file share**.
  - Report also covers **file-system management** and **static content** handling.
- **Target comparison (key point):**
  - **App Service Managed Instance:** **0 mandatory**, **4 potential** issues.
  - **App Service (Windows):** **2 mandatory** issues — because classic App Service (Windows) runs in a **sandbox** with a security lockdown that **blocks registry read/write and MSI installers**.
  - Switching back to Managed Instance **auto-resolves** those blockers — the rationale for launching Managed Instance at Ignite.
- **Migration options:** right-click project → **Publish to App Service Managed Instance**, **or** use an **agentic migration flow** via an existing PowerShell script (Gaurav published a **blog with pilot source code on GitHub** — agents you can download and modify).

### Demo — Part 2: Creating a Managed Instance App Service plan
Via **Create resource → Marketplace → type "managed instance" → "Web app for managed instance" → Create**:

- Provide **subscription, resource group** (existing or new), **name**, and **runtime**.
  - The runtime list is **shorter** because behind the scenes Managed Instance runs a **child Hyper-V VM** with default runtimes pre-installed — but you **can install other runtimes/versions** (.NET Framework, Node, Java major/minor) via the install script. Demo selects **4.8**.
  - Regions are **continuously rolling out**; demo uses **West Central US**.
- **SKU:** Managed Instance is **only on Pv4** → demo picks **P1 V4**. **Zone redundancy** is a toggle.
- **New step — install package:** the plan asks for a **storage account, container, and zip file**:
  - Create an **`install.ps1`**, zip it **together with all installers/MSIs/components**, upload to a storage account.
  - Select the **storage account + container + zip file name** (only constraint: the script must be named **`install.ps1`**; zip name is free).
  - A **managed identity** secures app↔storage communication; App Service downloads the zip, unzips, and **runs the install script steps** on the instance.
  - **Example install script contents:** installing **custom fonts**, **enabling the SMTP server role**; you can also enable other **Windows features**, install **Windows services**, or an **MSMQ client**.
  - ⚠️ The install package is **optional** — if your app has no extra dependencies, **skip it** ("optional yet super powerful").
- **Deployment tab:** standard experience — point at **GitHub source** and App Service pulls and deploys the code on creation.
- **Networking tab:** enable **public access** as needed. **Major difference:** instead of configuring a VNET per app, the **entire plan is joined to a virtual network**, so **all web apps in the plan are in the VNET**. Select a **VNET**, enable **VNET integration**, choose a **subnet**.
- **Review + Create:** App Service provisions the chosen instance size, creates the plan, downloads the zip, runs the install script, and (if given) pulls + deploys the source.

### Demo — Part 3: Plan configuration (storage mounts, registry, Bastion)
On an already-created Managed Instance plan (looks/behaves like a standard App Service plan), the new **Configuration** option exposes:

- **Install package config** — the storage account, script container, and zip name.
- **Storage mounts** — demo app has three mounts (e.g. **K:**, **L:**, **H:**). To add one (e.g. **storage4** → **J:**):
  - Map to an **Azure file share** (select storage account → file share); connectivity secured by a **secret = connection string stored as a Key Vault secret** (provide the **Key Vault** + **mapped secret**), then assign the **drive letter**.
  - Can also be a **UNC path** (a file server on Azure or in your own data center, reachable from the VNET) **or a local file share**.
  - ⚠️ **Local mounts are ephemeral** — content is lost if the instance restarts.
- **Registry entries** — e.g. the app reads its DB connection string from the registry. To add one: provide a **registry path** (e.g. `HKEY_LOCAL_MACHINE\SOFTWARE\...`), the **Key Vault** holding the actual value as a secret, and the **type** (**string** or **DWORD**). Use case beyond demo: a component that writes a **license file to the local registry**.
- **Bastion / RDP** — a **checkbox enables/disables remote desktop** for the plan. Under **Instances**, select an instance → **Connect** for **secure RDP** (or **Restart** an instance). In the RDP session Gaurav verifies the **created registry (regedit)**, the **event log**, the **MMC snap-in showing the SMTP role configured**, and access to the underlying **IIS server**. Install logs live under an **`install scripts`** folder (a log folder named after your script), and an overall **`adapter.log`** sits on **C:**.
  - ⚠️ Repeated warning: **RDP changes are not permanent** — put all installers/config in the **install.ps1 + zip** so they persist across **scale-out, scale-up, and restarts**.
- The migrated app is **indistinguishable from a standard Windows App Service app** — so you get **deployment slots, deployment center, quick env-var changes, authentication/identity, backups/resiliency, custom domain certificates**, and **scale up / scale out (rule-based or manual)**.

### Demo — Part 4: Built-in MCP (turning a REST API into an MCP server)
- The web app includes an **inventory REST API** with methods like *all inventory*, *inventory by ID*, and *inventory by category*.
- The second half of "move and improve" is making the app **intelligent / agent-ready** — reuse a powerful existing solution (e.g. inventory management / supply chain) in agentic flows **without writing new functions**.
- Steps:
  1. Generate an **OpenAPI-compliant JSON** spec for the REST API.
  2. In the portal, go to the **AI blade → MCP servers** (preview; the **Build 2026** "in-built API MCP" feature). Give it a **name** and an **endpoint path** for the MCP server (demo: "mobile 2026"), optionally a location for the `spec.json`, then **provide the OpenAPI spec** (browse to the file) and optionally **configure authentication**.
  3. App Service **creates a tool call per REST method** on the MCP server.
- **Using it:** in Visual Studio, add the MCP server to **`mcp.json`** (the only change), then ask **GitHub Copilot** (built into Visual Studio) a simple question like "get me the inventory" — Copilot **talks to the MCP server** and pulls inventory via the available tools. Consumers could equally be **your agents** or **any coding assistant/tool**.

### Demo — Part 5: Agent observability
- With **agents running on the app** and **App Insights configured**, the portal surfaces agent intelligence: in the demo, **5 agents total**, **52 calls in the last 30 days**, plus **token usage** and **error rate** over 30 days.
- **Drill-down:** click **logs** on an individual agent → routes to **App Insights**.
- **Where to find it:** same place as the MCP server experience — **AI blade → MCP servers**, with an adjacent **Agents** tab.

### Wrap-up & next steps (Andrew)
Andrew closes by framing the three pillars working together — **Managed Instance**, **built-in MCP**, and **GitHub Copilot app modernization tooling** — and points to resources (see Announcements/Related): the **App Service at Build 2026 blog**, a **3-article series on agentic app development with .NET** (build + publish on App Service), **built-in MCP** docs, **agent observability**, **Managed Instance** docs/overviews, the **GitHub Copilot app modernization tooling**, and **Gaurav's article on an agentic migration pathway to Managed Instance**. Theme: **embrace AI gradually** — take an existing app, get it to PaaS, then expose MCP tools and observe agents, expanding as feedback comes in.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure App Service** — the PaaS host for web apps/APIs that the whole session builds on.
- **Managed Instance on Azure App Service** — flexible PaaS tier (Pv4) that preserves Windows/third-party dependencies, registry, drive-letter mounts, install scripts, and Bastion RDP; public preview (launched Ignite Nov 2025).
- **Built-in MCP for App Service** — NEW (Build 2026, preview): auto-generates an **MCP server** from an app's API (one tool per method); secured by managed identity/OAuth/RBAC; supports .NET, Java, Node.js, Python.
- **Agent observability in App Service** — NEW: App Insights-backed portal view of agent count, calls, token usage, error rate, with log drill-through.
- **GitHub Copilot app modernization tooling** — Visual Studio tooling for AI assessment + refactoring; supports .NET and Java; integrates with App Service targets.
- **Visual Studio** — IDE hosting the modernization tooling and GitHub Copilot used to call the MCP server.
- **GitHub Copilot** — AI assistant used both for code modernization and (in-IDE) to invoke MCP tools.
- **Azure Bastion** — secure connectivity providing first-ever RDP into App Service instances.
- **Azure Key Vault** — stores secrets, credentials, registry values, and storage connection strings.
- **Managed identity** — required throughout for secure service-to-service auth (SQL, Key Vault, storage, MCP).
- **Azure Files / UNC share / local temp storage** — backing options for drive-letter storage mounts.
- **Azure SQL** — example database backend reached via managed identity.
- **Application Insights (App Insights)** — telemetry backend for app logging and agent observability.
- **Availability zones** — used for HA/resiliency across multiple instances.
- **OpenAPI specification (spec.json)** — the API contract fed to built-in MCP to generate tools.
- **`mcp.json`** — client config file where consumers register the generated MCP server.
- **`install.ps1` (+ zip package)** — PowerShell install script (zipped with MSIs/components) that provisions custom dependencies, OS roles/features, fonts, and services on instances.
- **.NET Framework / ASP.NET / .NET Core** — application runtimes; demo app is .NET Framework 4.8, with .NET Core cited for incremental rewrites.
- **log4net** — logging library in the demo app (writing to local disk).
- **SMTP server role / MSMQ client / GDI libraries** — examples of Windows/legacy dependencies Managed Instance can carry.
- **Hyper-V child VM** — the per-instance compute model behind Managed Instance (enables installing extra runtimes).
- **Deployment slots / Deployment Center** — standard App Service capabilities available post-migration.
- **Java / Node.js / Python** — additional languages supported by built-in MCP and the modernization/Linux scenarios.

## 🚀 Announcements / What's New
- **Built-in MCP for Azure App Service — NEW at Build 2026 (preview).** Auto-exposes an app's REST API as an MCP server (one tool per method), language-agnostic (.NET/Java/Node.js/Python), secured via managed identity, OAuth, and RBAC.
- **Agent observability in Azure App Service — NEW (announced at Build).** App Insights-backed portal metrics for agents running on the app (count, calls, token usage, error rate) with drill-through to logs.
- **Managed Instance on Azure App Service — public preview** (originally launched at **Ignite, November 2025**; reaffirmed here), continuing **regional rollout**; currently **Pv4 SKUs only**.
- **App Service at Build 2026 blog** — collects all of the above App Service announcements/capabilities for follow-up.
- **Gaurav's blog + GitHub pilot source code** for an **agentic migration flow to Managed Instance** (PowerShell-script-driven agents you can download/modify).
- **3-article series on agentic app development with .NET** on App Service (build + publish guidance).

## 💡 Demos
A single end-to-end demo (presenter: Gaurav) stitching the concepts together:
- **App modernization assessment (Visual Studio + GitHub Copilot):** assessed a classic .NET Framework web app (log4net, local SMTP, registry-stored DB connection string). Showed the report recommending **App Service Managed Instance** as default target, with logging/file-system guidance. **Proved the core value:** Managed Instance = **0 mandatory / 4 potential** issues vs **App Service (Windows) = 2 mandatory** (registry + MSI blockers in the sandbox), which Managed Instance auto-resolves.
- **Creating a Managed Instance plan (Azure Portal):** walked the marketplace flow — runtime (4.8), **P1 V4 SKU**, **install-zip (`install.ps1` + MSIs/fonts/SMTP role)** on a storage account secured by managed identity, GitHub source deployment, and **plan-level VNET integration**. **Proved** dependency-preserving, low-code migration to PaaS.
- **Plan configuration:** added **storage mounts** (drive letters → Azure Files/UNC/local, secrets in Key Vault), **registry entries** (path + Key Vault secret + string/DWORD), and **Bastion RDP** into an instance — verifying the **registry, event log, SMTP role (MMC), IIS**, and install logs (`install scripts` folder, `adapter.log`). **Proved** full Windows-style control + persistence model (RDP changes non-permanent → use the script).
- **Built-in MCP:** generated an **OpenAPI JSON** for an inventory REST API, used the portal **AI → MCP servers** blade to create an MCP server (endpoint path "mobile 2026"), yielding **one tool per API method**; added it to **`mcp.json`** and had **GitHub Copilot** answer "get me the inventory" by calling the MCP tools. **Proved** a legacy REST API becoming an agent/assistant-consumable tool with essentially one config change.
- **Agent observability:** showed the portal agent dashboard — **5 agents, 52 calls (last 30 days)**, token usage, error rate, with **App Insights** log drill-through. **Proved** built-in operational visibility for agentic apps.

## 📊 Notable Stats / Quotes
- **1 → ~30 instances** at a click / template / CLI — the scale-out promise vs. racking servers.
- **Vertical scale up to 32 cores / 256 GB RAM**, from a single-core/low-RAM starting point.
- Assessment counts: **Managed Instance = 0 mandatory + 4 potential** issues; **App Service (Windows) = 2 mandatory** issues for the same app.
- **Pv4 only** (e.g. **P1 V4**) — "our most performant SKU in our fleet," with attractive Windows pricing.
- Agent observability snapshot: **5 agents, 52 calls, last 30 days** (+ token usage, error rate).
- **Managed Instance launched at Ignite, November 2025**; built-in MCP + agent observability launched at **Build 2026**.
- Design ethos quotes: *"we're aiming for zero code changes"*; *"move and improve"*; *"optional yet super powerful"* (the install package); *"embrace AI gradually."*
- **First time ever** in Azure App Service: **RDP (via Bastion) directly into instances**.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Run **GitHub Copilot app modernization assessment** on a .NET Framework app in Visual Studio and compare **Managed Instance vs App Service (Windows)** issue counts.
  - Stand up a **Managed Instance plan (P1 V4)** in a test sub and exercise an **`install.ps1` + zip** (e.g. enable SMTP role / install a font) → verify via **Bastion RDP**.
  - Generate an **OpenAPI spec** for an existing REST API and use **built-in MCP** to expose it, then call it from **GitHub Copilot** via `mcp.json`.
  - Wire **App Insights** to an agent app and confirm the **agent observability** dashboard populates.
  - Read **Gaurav's agentic-migration blog** and try the **PowerShell-script agents** from GitHub.
- [ ] Questions:
  - What are the **GA timelines** for Managed Instance, built-in MCP, and agent observability? (All preview here.)
  - Which **regions** currently support Managed Instance, and what's the rollout cadence?
  - Cost: how does **Pv4 Managed Instance** (incl. the child Hyper-V VM model) price vs. standard App Service Premium and vs. VMs/AKS?
  - For built-in MCP, what **auth options/limits** apply, and how is **tool schema** derived/customized from OpenAPI?
  - Any **per-plan instance ceiling** (the talk cited "~30") and limits on **VNET-joined plans**?
- [ ] Relevant to:
  - **Azure migration / app-modernization labs** (lift-and-modernize of Windows/.NET Framework workloads).
  - **Agent/MCP architecture** work — exposing existing enterprise APIs as agent tools.
  - Customers blocked by **registry/MSI/third-party dependencies** on classic App Service.

## 🔗 Related
- App Service at Build 2026 blog (announcements hub)
- Managed Instance on Azure App Service — docs/overview
- Built-in MCP for Azure App Service (preview)
- Agent observability in Azure App Service (preview)
- GitHub Copilot app modernization tooling (Visual Studio)
- Agentic app development with .NET on App Service — 3-article series
- Gaurav's blog: agentic migration pathway to Managed Instance (+ GitHub pilot source)
- [[Microsoft Build 2026]]
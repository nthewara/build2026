---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/agent-365
  - topic/security
  - topic/governance
  - topic/agents
  - topic/identity
source: https://www.youtube.com/watch?v=qaOIwXD9HJ4
session_code: BRK251
event: Microsoft Build 2026
speakers: Netta, Kendra, Aarti, Ray (GenSpark)
duration_min: 47
aliases:
  - Build secure and enterprise-ready agents with Agent 365
---

# BRK251 — Build secure and enterprise-ready agents with Agent 365

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Netta (host/MC), Kendra (Agent 365 PM — value, concepts & admin experience), Aarti (developer demo — onboarding a LangChain agent), Ray (co-founder, GenSpark — partner integration)  
> **Duration:** ~47 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=qaOIwXD9HJ4)

## 🎯 TL;DR
Agent 365 is positioned as the **control plane for every agent in an organization** — not just Microsoft-built agents, but third-party, custom (e.g. LangChain on AWS/GCP), and pre-built SaaS agents. It organizes its value around three jobs-to-be-done: **Observe** (you can't govern what you can't see), **Govern** (guardrails that *speed up* adoption rather than block it), and **Secure** (treat agents like employees, protected by Entra, Defender, Purview, and Intune). The session walks through the **Agent 365 SDK** (which *wraps* an existing agent to make it discoverable — it does **not** build or host the agent), introduces foundational concepts (**agent blueprint**, **agent identity**, two authentication models), and demos end-to-end onboarding of a LangChain travel agent using shippable **Agent 365 skills** invoked from a coding agent. The admin experience inside the M365 admin center is shown in depth — registry, risk drill-downs into Purview/Entra, **templates** (the "hero feature" that bundles policies), **rules** for lifecycle automation, and **registry sync** for visibility-only ingestion of agents from Amazon Bedrock and Google Vertex AI. Partner **GenSpark** closes by explaining how they built on Agent 365's identity, MCP/tools, and observability primitives instead of building their own auth, storage, and audit layers.

## 🔑 Key Takeaways
- **Agent 365 is a control plane, not an agent-building platform.** It governs and secures any agent regardless of who built it or where it's hosted (Azure, AWS, GCP, on-prem).
- **IDC prediction framing:** by **2028 there will be ~1.5 billion agents** in organizations — more than the population of most countries — making discovery, governance, and security non-negotiable.
- **Three pillars structure everything: Observe → Govern → Secure.** "You cannot govern what you cannot see" is the recurring thesis.
- **Governance is reframed as an accelerant, not a brake** — guardrails sized to each agent's risk factor let orgs adopt agents faster and more confidently.
- **The Agent 365 SDK *wraps* your agent** to make it discoverable; it doesn't host or build it. It grants an agent ID, observability, tools/messaging, threat protection, governance, and data security — and you can adopt only the pieces you want.
- **Four onboarding tiers:** (1) native experience for Microsoft-built agents, (2) partner agents via an extended SDK ecosystem, (3) custom agents you onboard yourself with the SDK, (4) connected platforms via **registry sync** (visibility-only).
- **Two new foundational concepts:** an **agent blueprint** (a reusable "recipe" defining tools, data, rules, and guardrails) and an **agent identity** (a service-principal identity *up-leveled* toward a user-level identity, because agents are "built like apps but function like users").
- **Two agent authentication models:** *on-behalf-of-user* (agent assumes the invoking user's credentials/permissions) and *agent user identity* (agent has its own identity and permissions and acts independently).
- **Shippable Agent 365 skills** (~6 and growing) let a coding agent (GitHub Copilot, Claude Code, etc.) auto-onboard an agent in ~10 minutes — detecting stack, installing packages, wiring identity, observability, Work IQ/MCP servers, then register/publish/deploy.
- **Agents become first-class collaborators**: once configured with an endpoint, an agent can be **@mentioned in Word comments and emailed**, not just used in Teams — interacting like a hired employee.
- **The four "legs of the stool":** Microsoft **Entra** (identity), **Defender** (risk assessment + real-time threat detection/blocking), **Purview** (data governance/audit logs), and **Intune** (shadow-AI detection) hold Agent 365 up.
- **Templates are the hero feature** — they aggregate custom policies across Entra, Defender, Purview, and SharePoint into one reusable bundle applied consistently at agent publish/approval time.
- **Rules automate lifecycle management** — e.g. bulk-reassign agents to a leaver's manager, or auto-block an agent when risk is detected — reducing manual admin toil.
- **Registry sync** ingests agents from third-party platforms (Amazon Bedrock, Google Vertex AI) for visibility, and mirrors whatever permissions you hold there (e.g. delete) — though without the full SDK-level observability.
- **Shadow-agent management is expanding** beyond OpenClaw to leverage Defender across **~22+ additional local platforms** to discover, block, or bring agents under management.
- **Security inheritance is the partner win:** because agents get a unified identity, existing Purview policies (e.g. sensitivity labels, DLP) and audit logging apply automatically — partners like GenSpark don't build their own auth/storage/security layers.

## 📚 Detailed Notes

### The problem: an agent explosion that's hard to see, trust, and govern
The session opens (Netta) with an audience check: nearly everyone is building or using agents, but almost no one believes their agents are **enterprise-ready, observed, secure, and governed**. That gap is the whole point of the talk. **IDC predicts ~1.5 billion agents in organizations by 2028** — a number larger than the population of most countries.

Agents arrive in three broad shapes:
- **SaaS agents** — pre-built, shipped inside applications or on the web, that orgs simply start using.
- **Endpoint agents** — ones you build yourself, including open-core agents and agents built with CLIs and other tooling.
- **Cloud agents** — built across different clouds, platforms, and frameworks.

This sprawl raises the core questions every organization faces: Can we **discover** all these agents? **Manage** them? Are they **behaving** according to intent — or breaking from it, **misusing tools**, **oversharing/leaking data**? And can they ultimately be **governed and audited**? Historically teams stitch together many disparate frameworks and products to answer these. The desired properties for any agent are: **observability** (registered in an inventory/registry), **identity** (attribute an action to a specific agent), **threat protection** (against new generative-AI risks like prompt injection, intent breaking, tool misuse), **data security** (no over-sharing/leaking), and **governance & compliance**. Agent 365 is presented as the single **control plane** that delivers all of this for any agent in the organization.

### Why Agent 365 — the three pillars (Observe, Govern, Secure)
Kendra frames the value around three pillars aligned to the core jobs-to-be-done for managing agents at scale. The headline rule, repeated throughout: **Agent 365 covers Microsoft agents *and* third-party, custom, and external agents.**

- **Observe** — "You cannot govern what you cannot see," and you cannot trust you're protected if you don't know what agents exist. Observability surfaces every agent across every platform, plus adoption and usage trends (which platforms agents are built on, etc.), *and* the actions needed to mitigate issues and keep the ecosystem safe.
- **Govern** — explicitly reframed: governance is **not about putting brakes on innovation or adoption**. It's about **guardrails sized to each agent's risk factor**, so the right protections are in place every time regardless of who built the agent or how. The intent is to *speed up* the pace of adoption and innovation.
- **Secure** — secure agents like you'd secure any employee, data asset, or app across the tenant. With **Defender, Purview, and Entra** you block threats in real time *and* go further: **deep hunting and investigation** to understand root cause, **full Purview logs** capturing every step an agent took when an incident occurred, and the ability to **identify other agents with similar vulnerabilities** so you can mitigate them *before* incidents happen.

### How it covers everything: the Agent 365 SDK
The audience quiz ("Does Agent 365 support *all* agents?" — answer: yes) sets up the key enabler. The **Agent 365 SDK is explicitly NOT an agent-building SDK and will not host your agent.** Its sole purpose is to **wrap an existing agent and make it discoverable within Agent 365**. Through the SDK you can:
- Assign an **agent ID** to the agent.
- Enable **full observability**.
- Apply **full security policies**.
- Access **productivity capabilities via the tools gateway**.

The SDK delivers (and you can opt into only what you need): **identity, observability, tools, messaging, threat protection, governance, and data security**.

### The "stool" architecture and the four onboarding tiers
Foundationally, Agent 365 is an **end-to-end governance platform** to scale and operationalize agent governance/management. Picture it as a **stool**, with four enterprise security solutions as its legs:
- **Microsoft Entra** — identity management.
- **Microsoft Defender** — risk assessment and real-time threat detection/blocking.
- **Microsoft Purview** — data governance.
- **Microsoft Intune** — shadow-AI detection.

On top sit a wide range of agent solutions: Microsoft's own agent-building platforms and pre-built agents (e.g. **Co-work**, **Researcher**), valuable third-party agents customers already use (acknowledging a "heterogeneous mix"), custom agents built on platforms of choice (LangChain agents, AWS, Gemini, etc.), and common platforms worth automating/ingesting.

Coverage breaks into **four tiers**:
1. **Microsoft-built agents — native experience.** Out of the box you see every agent (draft or in production, including real-time changes), with full observability data, policy templates, security guardrails, and the ability to take action — **no additional effort**.
2. **Third-party partner agents.** Microsoft is building a **partner agent ecosystem** that proactively extends the SDK into partner agents to enable an agent ID, observability, and more. (One such partner — GenSpark — presents at the end.)
3. **Custom agents (you onboard).** Agents you build on LangChain, another SDK, or an AWS cloud solution can be onboarded with the Agent 365 SDK, gaining identity, observability, tools, messaging, threat protection, governance, and data security — with the flexibility to onboard only what you want.
4. **Connected agent platforms — registry sync.** Using your existing permissions/credentials on platforms like **Amazon Bedrock** and **Google Vertex AI**, registry sync **ingests those agents into the registry for visibility only**. Any governance capabilities/permissions you already hold on those platforms (e.g. delete) are also exposed inside Agent 365.

### Foundational concepts: agent blueprint & agent identity
Two new-but-fundamental terms are introduced before the demo:

- **Agent blueprint** — a **reusable instruction set / "recipe"** for an agent defining what **tools** and **data** it can leverage, plus the **rules and guardrails** in place. Other agents and **agent identities** are created *from* a blueprint. (In the demo, the developer's onboarding produces a blueprint; multiple *instances* can be created from it.)
- **Agent identity** — takes a service-principal identity and **up-levels it toward a user-level identity**. Rationale: agents are unique — **they're built like apps but function like users**, so they need an identity appropriate to that function. Agent identities are purpose-built to support agents.

**Two authentication models** for agent identities:
- **On-behalf-of-user** — when a user invokes the agent, the agent **assumes that user's credentials**, passes the credential as the auth token, and operates with **that user's permissions** for information retrieval / task completion.
- **Agent user identity** — the agent **maintains its own identity and permissions**, passes its own identity for authentication, and **functions independently** without acting on behalf of a user.

### Developer demo: onboarding a LangChain travel agent (Aarti)
Aarti "wears several hats," starting as an **agent developer in VS Code**. The subject is a **travel agent built on LangChain using Node.js (TypeScript)** — deliberately chosen as a non-Microsoft example to prove the breadth claim. Given a source, destination, and dates, it returns three hotel options, three flight options, and some restaurants (demoed: three airlines Seattle→San Francisco plus hotels).

**The task:** make this agent "ready for Agent 365." While you *could* stitch the concepts together manually using the available Learn docs and samples, Microsoft **ships specific Agent 365 skills** for coding agents to do the work. Key points:
- Skills are invoked from the coding agent (shown via `/skills` → `Agent 365` in VS Code). Aarti switches to **GitHub Copilot** to run them, noting **any coding agent works** (Claude Code, your choice — "does not matter").
- There are **~6 skills and growing.** Two "main" skills are the interesting ones; others are **piecemeal** building blocks — e.g. just get an **identity**, just instrument **observability** (telemetry), or optionally add **Work IQ servers** so the agent can interact with productivity surfaces (create documents, access its own calendar, etc.).
- The full run takes **~10 minutes** (skipped live for time).

**What the skill does, end to end:**
1. **Detects the agent's stack** with minimal input (just point it at the agent folder and say "make this agent ready for Agent 365") — correctly identifies Node.js + LangChain + TypeScript, and (being a coding agent with code access) understands what the agent *does*.
2. **Checks prerequisites** — downloads required packages/dependencies, ensures the machine is set up; picks the **latest Agent 365 CLI** version. Uses the already-authenticated **Azure CLI** login and targets the chosen **tenant**.
3. **Produces a detailed plan** and executes it: install required agent packages → validate → build → add **observability**, **Work IQ**, then **register, publish, and deploy**.
4. **Result:** a fully extended Agent 365 agent. It **created a blueprint**; the **actual agent identity is created later when an admin activates the agent in the Microsoft admin center**. It configured observability and Work IQ, and — per Aarti's choice — wired up **Word and OneDrive MCP servers**, producing a manifest.

The developer then **hands off to the admin**: the admin decides whether the agent is shared with a **subset of users or all users**, then assigns it — at which point the agent is live in the tenant.

### Agent-as-employee: using and collaborating with the agent
Aarti switches to an **agent-user** persona. From **Teams**, she opens the app list and **creates an instance** — her own version of the agent that "reports up to her." She prompts it (plan a trip to Austin after Build) and deliberately asks it to **both reply and create a Word document**, to demonstrate cross-surface interaction. The agent returns near-identical suggestions (she likes Southwest + Marriott) plus an **editable Word document**.

The standout moment: in the Word doc she **@mentions the agent in a comment** ("can I get some coffee places as well, please") exactly as she would a human colleague — arguing it's more natural/contextual than switching to Teams. This works because onboarding **created an endpoint** for the agent, so it can **respond to notifications over Teams, @mentions in Word comments, and emails**. The agent replies in-comment (e.g. recommending an Italian place, "Loro," "popular with excellent food and a nice atmosphere"). Crucially, the agent **can be hosted anywhere** — demoed in Azure, but it could run in GCP, AWS, or any cloud; "it does not matter."

**Observability has three audiences:**
- **Developers** — what their agents are doing and who uses them.
- **End users** — since "this is my employee," users can see their own chats (today's tests, recent chats on refresh, including a couple of **failures** where the agent didn't complete the task), the prompts given, and whether tasks were carried out.
- **IT admins** — see activity across **all instances of a blueprint** (e.g. colleagues Pooja and Alister each have instances; Aarti's is heavily used), including an **activity view** and the **exact users** of the agent.

**Demo recap:** start with a basic Node.js LangChain agent (hosted anywhere) → use **skills** to make it Agent 365-ready (Entra config + blueprint, observability via **OpenTelemetry**, optional Word/OneDrive MCP servers, notification endpoint for Teams + @mentions) → it's configured and ready in the tenant to unlock all Agent 365 features.

### Admin experience: the Microsoft 365 admin center
Kendra returns to the **admin experience inside the Microsoft 365 admin center** — the place for full observability across the tenant. (Noted as a work-in-progress: **multi-tenant capabilities** are coming; today it's single-tenant.)

**Overview / landing page:**
- **High-level analytics**: total agents, total **users** (clarified as *human* employee users, **not** agentic users), and **total runtime hours**.
- **Registry sync** entry point (revisited later).
- **Calls to action** — where to lean in: **pending requests** (agent approvals, like Aarti's instance), **agent risks** seen, **agents without owners** (a "big one" for keeping **agent sprawl** under control and maintaining good hygiene), and **agents with exceptions** (any **error in agent runtime** surfaces as an exception).
- **Granular analytics**: agents built by your org vs. third-party providers vs. across Microsoft; **top platforms** agents are built on; **agent adoption over time** (useful for adoption campaigns or launching high-profile agents like IT-support or benefits agents); and **trending agents** used heavily across the org.

**Agent registry:** lists **all agents across all platforms** — explicitly *not* just Microsoft (examples shown include **Workday** and partner agent **GenSpark**). The list can be sliced/diced/customized to manage large numbers.

**Inside an agent (example: a "Zava procurement agent"):**
- **Metadata**: what the agent does, publish date, last-updated date, **publisher**, **owner**, and **agent ID**.
- **Agent instructions** — exactly what the agent is doing / its purpose.
- **Full identity history** — **bot ID**, **blueprint ID**, and **Entra agent ID**. For a **Copilot Studio** agent you'd see environment details; for a **Foundry** agent you see platform details with a link out to the agent itself.
- **Users the agent is shared with**, **applied policies** (from onboarding/approval — drill into **Purview** or **Entra** to investigate), and **permissions** the agent holds.
- **Unified activity view across all agent types** (called out as a favorite): total users, total sessions, exceptions, runtime hours, **successful sessions**, and the ability to watch for **spikes in exceptions** and lean in. Below that, the **users driving traffic** with total sessions and last-activity dates.

**Visual / graph view:** beyond the list, a visual representation shows **agents working with other agents**, aggregated by the platforms they're built on. Hovering over multi-agent solutions reveals which agents they leverage — **even across different platforms**. A **list view of connected platforms** shows, e.g., all agents a "researcher agent" uses and whether each is **available or blocked**. The stated value: understand **dependencies** and, before blocking an agent, know the **blast radius** — "if I block this agent, what else does it break?"

### Risk, ownership, and lifecycle automation (rules)
- **Drilling into risks:** clicking a risk jumps to the agent and shows the **source** of the risk. From there you can drill into **Entra** or **Purview** to see incidents granularly — Purview gives **full log access down to the document/data-source layer** that triggered the (blocked) risk. The admin can **block the agent** and hand off to the **SecOps team** for further investigation/mitigation.
- **Agents without owners:** owners can be reassigned (e.g. "make Aarti the owner"), but doing it manually is tedious at scale.
- **Rules** solve this: a simple way to **automate lifecycle-management actions**. Examples: **bulk reassignment** when someone leaves the org (for agents built in **Agent Builder**, auto-reassign to their **manager**); **auto-block** an agent when risk is identified (no manual blocking required). Microsoft is **investing heavily in risk** with more functionality over the coming quarters.

### Templates — the "hero feature"
**Templates** aggregate custom policies from across **Entra, Defender, Purview, and even SharePoint** into **one reusable template** applied to agents consistently and comprehensively. There are **default templates** and you can create custom ones. A custom template shown includes **access packages** (multiple selectable), **conditional access**, and a range of default policies such as **DLP protection** and **lifecycle-management protections**.

Templates plug into the **agent approval flow**: when a maker wants to **publish an agent** org-wide (demoed with a "staffing agent"), the **IT admin must approve it and apply the appropriate template**. This is where **data and tools** matter most — to make an informed decision the admin needs to know **what the agent is made of**: what **data** and **tools** it can access, which defines its **risk level**. The publish flow lets the admin select users (pre-install for all, or just make it discoverable in the store), then a **default template is applied as a baseline** ("all agents should have some level of protection"), optionally swapped for a **custom template** (e.g. a "DevOps template"). Policies and appropriate **permissions** are applied, reviewed, approved — and the agent becomes available org-wide.

### Registry sync & shadow-agent management (revisited)
**Registry sync** ingests agents from common third-party platforms (**Amazon Bedrock**, **Google Vertex AI**). After configuring access, clicking into **Google** shows the deployed agents (one in the demo). You **don't get the full SDK-level observability**, but you gain **awareness of every agent deployed** on that platform. Permissions mirror what you hold there — because the admin already has **delete** permission in Google, the same **delete** action is available inside Agent 365.

Beyond synced platforms, Agent 365 helps **identify and bring shadow agents under management**. This is **expanding beyond OpenClaw** to **leverage Defender** and discover **~22+ (give or take) additional local platforms**, so admins can **block** those agents or **bring them under management**. The platform also lets you **govern and manage all of your tools** centrally (shown briefly before the time signal).

### Customer momentum & early adopters
Kendra closes the Microsoft portion with customer proof points:
- **EY** — for **mission-critical agents**, Agent 365 is key: it gives them the **trust** to unlock these agents and feel confident leveraging them across the organization.
- **GenSpark** — an early-adopter partner who presents directly (next section).

### Partner deep-dive: GenSpark on building atop Agent 365 (Ray)
Ray, **co-founder of GenSpark**, explains how GenSpark integrates with Agent 365. **GenSpark is a unified AI workspace for knowledge workers**, with **2,000+ organizations** already registered as a daily work tool.

**The motivating insight — different jobs need different AI back-ends:**
- *"Sarah"* in finance needs to prep a **board deck by Friday** — summarize content and make slides; she needs **lightweight, chat-based AI tools**.
- *"Tom"* has a **200+ MB CSV** needing heavy compute for calculations/summarization; he needs a **dedicated virtual machine**.

Agent 365 gives developers like GenSpark the **flexibility to combine different AI back-end infrastructures** behind a single governed surface.

**Three primitives GenSpark builds on (Ray's framing of Agent 365):**
1. **Identity** — with **federated identity credentials**.
2. **Unified UI/UX interface** — the M365 software suite (Teams, Outlook, Word, etc.).
3. **Observability, Purview, audit + full lifecycle management.**

**GenSpark's architecture (three layers):**
- **Top layer** — Microsoft software suite (Teams, Outlook, Word, etc.).
- **Middle layer** — a *very thin* integration layer using the **Agent 365 Python SDK**, providing **identity, streaming, and MCP** access over Microsoft software, plus **observability, Purview, and lifecycle management**.
- **Bottom layer** — GenSpark's **flexible back-ends**: lightweight chat-based AI tools, and heavyweight compute like **GenSpark Cloud** and **dedicated VMs**.

**How GenSpark uses each primitive:**
- **Identity** — they **authenticate *every* request/message** from Teams through their back-end, **not just once at session start**. Example: if someone in a Teams group chat @mentions the agent asking for private info, the agent can detect the requester is **not in the org's AAD** and **refuse the request**. With Agent 365 they **don't build a separate auth layer** — they use Microsoft's.
- **MCP / tools** — Agent 365 already provides **powerful MCPs** (PowerPoint, Outlook, Word, etc.). For each request, GenSpark can **generate a PowerPoint or Word document on the fly** and **write it back to the user's or agent's OneDrive via MCP** — so they **don't build their own storage layer**.
- **Observability, security & governance** ("the most amazing part") — every agent **invocation, inference, and activity is logged into Purview**, giving tenant admins a **single, unified dashboard** to monitor all agent activity. Because each agent has its **own unified identity**, **existing enterprise Purview policies automatically apply** — e.g. a **sensitivity label** on a Word document also applies to the agent, and DLP/Purview policy can **automatically block** the agent if it tries to leak sensitive info. All agent logs are **unified via the same Microsoft APIs**, so IT can use the **same SQL queries** to analyze agent activity.

**The partnership payoff:** GenSpark gives users flexibility to choose different agent back-ends (chat-based or dedicated VMs), while the enterprise **retains full control** — all activity/logs sit on top of Microsoft APIs, so IT managers use **existing tools** to monitor, observe, and audit. Ray reports enterprise customers "love this feature a lot."

### Wrap-up
Netta closes: attendees saw how to **build enterprise-ready agents with Agent 365** — integrate the **SDK**, then **observe, secure, and govern** the agent. Resources were shared on screen: **how to get started**, **how to get started with the SDK**, and a **recently released blog**.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Agent 365** — the control plane / end-to-end governance platform for *every* agent (Microsoft, third-party, custom, external) across the organization.
- **Agent 365 SDK** — *wraps* an existing agent to make it discoverable; grants agent ID, observability, tools, messaging, threat protection, governance, data security (not an agent-building or hosting SDK). Available in **Python** (used by GenSpark) and used in the **Node.js/TypeScript** demo.
- **Agent 365 skills** — ~6+ shippable skills for coding agents to auto-onboard an agent (setup/identity, observability instrumentation, optional Work IQ servers, plus two main end-to-end skills).
- **Agent 365 CLI** — command-line tooling the skills invoke; auto-updated to latest during onboarding.
- **Microsoft Entra** — identity management; source of the **Entra agent ID**; "leg of the stool."
- **Microsoft Defender** — risk assessment, real-time threat detection/blocking; powers expanded **shadow-agent** discovery across ~22+ local platforms.
- **Microsoft Purview** — data governance, full audit logs down to the document/data-source layer; applies sensitivity labels/DLP to agents.
- **Microsoft Intune** — shadow-AI detection; "leg of the stool."
- **Microsoft 365 admin center** — the admin surface for Agent 365 (registry, analytics, approvals, risk, templates, rules, registry sync).
- **Agent blueprint** — reusable "recipe" defining an agent's tools, data, rules, guardrails; agent identities/instances are created from it.
- **Agent identity** — service-principal identity up-leveled toward user-level; supports on-behalf-of-user and agent-user-identity auth models.
- **Registry sync** — visibility-only ingestion of agents from connected third-party platforms; mirrors held permissions.
- **Templates** — reusable bundles aggregating policies across Entra, Defender, Purview, SharePoint (access packages, conditional access, DLP, lifecycle protections); applied at approval/publish.
- **Rules** — automation for lifecycle actions (bulk reassignment to managers, auto-block on risk).
- **Work IQ servers / MCP servers** — let agents interact with productivity surfaces (create documents, access calendars); demo used **Word** and **OneDrive** MCP servers.
- **Tools gateway** — productivity capability access exposed through the SDK; centralized tool governance/management in the admin center.
- **OpenTelemetry** — the observability standard wired up for the agent during onboarding.
- **Microsoft Copilot Studio** — agent-building platform (admin center shows environment details for Copilot Studio agents).
- **Microsoft Foundry** — agent-building platform (admin center shows platform details + link-out for Foundry agents).
- **Agent Builder** — platform referenced in rules (e.g. auto-reassign Agent Builder agents to a leaver's manager).
- **Co-work / Researcher** — examples of Microsoft pre-built agents.
- **GitHub Copilot** — coding agent used to run the Agent 365 skills in the demo (Claude Code and others also supported).
- **VS Code** — the developer's editor in the demo.
- **LangChain** — framework the demo travel agent is built on (Node.js/TypeScript).
- **Amazon Bedrock** — third-party platform supported by registry sync.
- **Google Vertex AI** — third-party platform supported by registry sync (demoed, with delete permission mirrored).
- **AWS / GCP / Azure** — possible hosting clouds for an onboarded agent ("host anywhere"); demo hosted in Azure.
- **Azure CLI** — used for the authenticated login/tenant targeting during onboarding.
- **Microsoft Teams / Outlook / Word / OneDrive** — productivity surfaces agents plug into (use, @mention, email, document creation/storage).
- **SharePoint** — one of the policy sources aggregated into templates.
- **Workday, GenSpark** — example third-party/partner agents visible in the registry.
- **GenSpark** (partner) — unified AI workspace; **GenSpark Cloud** and **dedicated VMs** as heavyweight back-ends; integrates via the Agent 365 Python SDK.

## 🚀 Announcements / What's New
No formal GA/preview dates were stated, but the session positions the following as new or actively rolling out:
- **Microsoft Agent 365** as the cross-platform agent control plane (Microsoft + third-party + custom + external).
- **Agent 365 SDK** (Python + Node.js/TypeScript) for wrapping/onboarding non-native agents.
- **Agent 365 skills** for coding agents (~6 and "constantly adding") to automate onboarding end-to-end.
- **Agent blueprint** and **agent identity** as foundational constructs (with two auth models).
- **Templates** (policy aggregation across Entra/Defender/Purview/SharePoint) — called a "hero feature."
- **Rules** for lifecycle automation (bulk reassignment, auto-block on risk) — "investing heavily... over the next couple quarters."
- **Registry sync** for Amazon Bedrock and Google Vertex AI (visibility-only ingestion).
- **Expanded shadow-agent management** beyond OpenClaw via Defender across **~22+ additional local platforms** (described as in progress).
- **Multi-tenant capabilities** — explicitly called out as **coming / being worked on** (today is single-tenant).
- **Partner agent ecosystem** — Microsoft proactively extending the SDK into partner agents (GenSpark a launch example).

*(Status note: several items are framed as current/early or roadmap; exact preview vs. GA labels were not given in the transcript.)*

## 💡 Demos
- **Developer onboarding demo (Aarti):** A **LangChain Node.js/TypeScript travel agent** is made "Agent 365-ready" by invoking **Agent 365 skills** from **GitHub Copilot** in VS Code. The skill detects the stack, checks prerequisites, installs packages, uses Azure CLI login/tenant, plans, then **builds → adds observability (OpenTelemetry) → Work IQ → register → publish → deploy** in ~10 min — producing a **blueprint**, configured **Word + OneDrive MCP servers**, and a manifest. *Proves:* non-Microsoft agents can be fully onboarded with minimal manual effort, hosted on any cloud.
- **Agent-as-employee demo (Aarti):** From **Teams**, she creates her own **agent instance**, asks it to plan an Austin trip *and* generate a **Word document**, then **@mentions the agent in a Word comment** to request coffee places — the agent replies in-comment. *Proves:* the onboarding-created **endpoint** lets the agent respond across Teams, Word @mentions, and email — collaborating like a hired colleague.
- **Observability views (Aarti):** Shows developer/end-user/admin observability — recent chats, **failed runs**, prompts, and **per-blueprint instance activity** (colleagues Pooja/Alister have their own instances). *Proves:* every step is observable for all three audiences.
- **Admin center walkthrough (Kendra):** Overview analytics (total agents/users/runtime hours), calls to action (pending requests, risks, **agents without owners**, exceptions), built-by-org vs. third-party vs. Microsoft breakdowns, top platforms, adoption-over-time, trending agents; the **registry** (showing Workday, GenSpark, etc.); a **Zava procurement agent** detail (metadata, instructions, **identity history** with bot/blueprint/Entra IDs, shared users, policies, permissions, unified activity); and a **graph view** of agent-to-agent dependencies with **blast-radius** insight. *Proves:* unified cross-platform visibility and actionability.
- **Risk + ownership + rules (Kendra):** Drill from a risk into Entra/Purview down to the **document layer**, **block** the agent, hand to SecOps; **reassign owners**; and set **rules** to auto-reassign/auto-block. *Proves:* governance scales from manual to automated.
- **Templates + approval flow (Kendra):** Build a custom template (access packages, conditional access, DLP, lifecycle protections), then publish a **staffing agent** through the **admin approval flow** — select users, apply a baseline default template or a custom **DevOps template**, review/approve permissions. *Proves:* consistent, risk-appropriate guardrails at publish time.
- **Registry sync (Kendra):** Configure access to **Google Vertex AI**, view the ingested agent, and (because the admin holds the permission) **delete** it from within Agent 365. *Proves:* visibility-only ingestion that respects existing platform permissions.
- **GenSpark integration architecture (Ray):** Walks the three-layer architecture and live framing of how identity (per-message auth, refusing out-of-AAD requests), MCP (on-the-fly Word/PowerPoint to OneDrive), and Purview observability/policy inheritance work. *Proves:* a partner can build on Agent 365 primitives instead of rebuilding auth, storage, and audit.

## 📊 Notable Stats / Quotes
- **"By 2028, there will be 1.5 billion agents in organization"** — IDC prediction ("more than most of countries in the world").
- **GenSpark: 2,000+ organizations** already registered it as a daily work tool.
- **Shadow-agent expansion to ~22+ additional local platforms** via Defender ("give or take").
- **~6 Agent 365 skills** shipping and "constantly adding to this."
- **~10 minutes** for the skill-driven onboarding run to complete.
- **GenSpark example workloads:** a **200+ MB CSV** needing dedicated-VM compute vs. a chat-based slide-deck task.
- **"You cannot govern what you cannot see."** — the recurring thesis for the Observe pillar.
- **"Governance is all about implementing guardrails... not intended to put the brakes on innovation"** — reframing governance as an accelerant.
- **Agents are "built like apps but function like users"** — the rationale for agent identities.
- Audience reality check: nearly everyone is building/using agents, but only **one person** felt their agents were enterprise-ready, observed, secure, and governed.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Run the **Agent 365 skills** from GitHub Copilot against a sample LangChain/Node agent to see the full register→publish→deploy flow end to end.
  - Stand up a **template** combining Entra access packages + Purview DLP + conditional access, and apply it via the agent approval flow.
  - Test **registry sync** against a Google Vertex AI / Amazon Bedrock agent to evaluate visibility-only ingestion vs. full SDK onboarding.
  - Try the **@mention-in-Word** agent collaboration flow to feel the "agent-as-employee" UX.
- [ ] Questions:
  - What are the exact **preview vs. GA** statuses and licensing/pricing for Agent 365 and the SDK?
  - When do **multi-tenant** admin capabilities ship?
  - Which specific **~22+ local platforms** does the Defender-based shadow-agent discovery cover?
  - For **registry sync**, what governance actions beyond delete propagate, and what observability is genuinely missing vs. SDK onboarding?
  - How do **agent identities** consume licenses / count against directory objects at the 1.5B-agent scale?
- [ ] Relevant to:
  - Anyone planning **enterprise agent governance** across mixed clouds (Azure + AWS + GCP).
  - **Security/IT admin** teams owning agent sprawl, risk, and audit (Defender/Purview/Entra/Intune).
  - **Developers** shipping custom agents (LangChain, etc.) who need them discoverable and governed.
  - **ISVs/partners** wanting to integrate with the M365 productivity surface without rebuilding auth/storage/audit.

## 🔗 Related
- 
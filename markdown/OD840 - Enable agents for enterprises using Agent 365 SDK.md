---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/agent-365
  - topic/enterprise
  - topic/agents
  - topic/m365
  - topic/security
  - topic/entra
  - topic/purview
  - topic/defender
source: https://www.youtube.com/watch?v=_OtDAmR3vIk
session_code: OD840
event: Microsoft Build 2026
speakers: Jeremiah Fallis (PMM, Microsoft Security for AI), Sunil Garg (PM, Agent 365 SDK & CLI)
duration_min: 24
aliases:
  - Enable agents for enterprises using Agent 365 SDK
---

# OD840 — Enable agents for enterprises using Agent 365 SDK

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Jeremiah Fallis (Product Marketing Manager, Microsoft Security for AI team) · Sunil Garg (Product Manager, Agent 365 team — runs the Agent 365 SDK & CLI, deployed PM driving ecosystem/partner adoption)  
> **Duration:** ~24 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=_OtDAmR3vIk)

## 🎯 TL;DR
This session makes the case that an enterprise-ready agent is not a feature inside an app — it's an **actor with its own identity** that must be discoverable, scoped to least privilege, observable, governed, and auditable from day one. Sunil Garg lays out the four things keeping CISOs/CIOs up at night (agent sprawl, data oversharing, indirect prompt injection, regulatory uncertainty) and frames the bar for a production agent as "could it pass a Fortune 500 onboarding review?" The answer Microsoft offers is **Agent 365** — the control plane for agents (GA on May 1st) — and its **SDK**, which lets developers layer **observability, governance, and security** onto *any* framework (OpenAI SDK, LangChain, Claude, LlamaIndex, Microsoft Agent Framework, or custom code) incrementally, not as a rewrite. Once integrated, the agent automatically lights up across **Entra** (agent ID, conditional access, lifecycle/access governance), **Purview** (sensitivity labels, DLP, insider risk, compliance), and **Defender** (threat hunting, anomaly detection, block/respond), so security teams manage agents with the exact tools they already use for humans. A live GenSpark demo shows the agent inventoried in the M365 admin center, a Purview sensitivity label and DLP rule blocking the agent, and a Defender high-severity alert firing on a prompt-injection attack.

## 🔑 Key Takeaways
- **"An agent is not an app — it's an actor with its own brain."** The biggest mindset shift: give every agent a scoped identity, least-privilege access, and an audit trail *from day one*. Bolt governance on later and you've already lost it.
- **Four enterprise fears, by the numbers:** agent sprawl & resource access; data oversharing (**80%** say data leaking through AI is their top concern); the new threat surface (**88%** worry about indirect prompt injection); and regulatory uncertainty (**>half** of leaders admit they don't fully understand how AI will be regulated). The real risk is the **compounding** of all four.
- **Adoption momentum is real:** **82%** of leaders plan to deploy agents in the next 12–18 months — that same momentum is exactly what's creating the security anxiety on the other side of the table.
- **Treat agents like new hires.** When an employee joins, IT provisions a managed identity, scopes access to role, a manager sets expectations, and everything is auditable. Agents need the identical machinery — and enterprise buying questions map almost 1:1 to onboarding-a-new-hire questions.
- **Think in data *flows*, not individual permissions.** Two perfectly reasonable permissions (read a CRM + send an email) can combine into an **exfiltration path**. Design with the full flow in mind.
- **Assume your agent will be manipulated.** The moment it reads an email, parses a document, or browses a page, untrusted content enters its reasoning loop — build hooks/guardrails for detection and **design for graceful failure**.
- **The bar isn't "does it work" — it's "could it pass a Fortune 500 onboarding review?"** Identity, behavior, data handling, auditability. Build to that bar and you're building agents enterprises will *trust* — and trust is what takes a demo to production.
- **Agent 365 is the control plane for agents** (observe, govern, secure every agent in the environment). It went **GA on May 1st**, along with the SDK.
- **Microsoft AI platforms are wired in out of the box.** Build in Agent Builder, Copilot Studio, or Foundry — no-code/low-code/pro-code — and the agent shows up in Agent 365 automatically with identity, observability, governance, and security.
- **The SDK is "not all or nothing."** Bring OpenAI SDK, LangChain, Claude, LlamaIndex, Microsoft Agent Framework, or fully custom code and **layer on capabilities incrementally** — you pick where to start (observability → governance → security) and how far to go. It's a layer, not a rewrite.
- **Observability = full OpenTelemetry tracing** (every input, output, tool call, model invocation). Two paths: the recommended **Microsoft OpenTelemetry distro** (auto-instrumentation for OpenAI, LangChain, Agent Framework + hooks for everything else) or **direct ingestion to an OTel endpoint** (reuse an existing pipeline / unsupported stacks like Java). **AI-guided setup** wires registration + telemetry for coding agents so you reach your first trace without reading docs.
- **Governance routes M365 data through governed MCPs.** Mail, Calendar, OneDrive, SharePoint, Teams become reachable via admin-controlled, auditable, revocable permissions — no bespoke connectors or consent flows to build. You can also **bring your own MCPs** and register them for the same controlled access.
- **Security = Entra Agent ID via the SDK.** Enable it and identity protection, conditional access, and ID governance light up for admins — your agent gets a **real, verifiable, first-class identity** managed with the same Entra controls used for users.
- **Three pillars, no new tools to learn:** **Entra** (identity, lifecycle, conditional access, access governance), **Purview** (sensitivity labels, DLP, insider risk, compliance), **Defender** (advanced hunting, misconfig/vuln investigation, detect/block/respond to tool misuse). Security teams work where they already work.

## 📚 Detailed Notes

### Framing: why security stalls agent adoption
Jeremiah opens by naming the tension: developers everywhere are building agents to drive real business and technology transformation, but **security and risk concerns can stall adoption fast**. The session's purpose is to help developers (and security leaders) understand why **observability, governance, and security** matter for agents, what the Agent 365 SDK does, and what you get from integrating with it. Sunil notes this is the question he gets more than any other right now — and that the excitement around agents is *completely justified* (82% of leaders plan to deploy in 12–18 months to keep up with workforce demand). The catch: that same momentum is what's generating anxiety on the enterprise side.

### The four things keeping enterprises up at night
When Sunil talks to CISOs and CIOs, four concerns consistently surface:

1. **Agent sprawl & resource access.** Every team is spinning up agents, and each one needs identity, permissions, and access to data and tools. The pivotal mental-model shift for a developer: *an agent is not an app, it's an actor with its own brain.* Give it a **scoped identity, least-privilege access, and an audit trail from day one** — because if you bolt on governance later, you've already lost it.
2. **Data oversharing.** **80%** of leaders say their top concern is sensitive data leaking through AI. Crucially, this usually **isn't a model problem — it's a grounding problem.** The agent has access to a SharePoint site, a CRM, or an email thread the user technically *can* reach but probably shouldn't be surfacing in this context. Developers must design with **data boundaries**: respect sensitivity labels, honor the permissions of the invoking user, and never let the agent become a shortcut around controls that already exist in the enterprise.
3. **The new threat surface.** **88%** of organizations worry about **indirect prompt injection** — and they should. The moment an agent reads an email, parses a document, or browses a web page, **untrusted content enters its reasoning loop**. The developer's job is to build the right hooks and guardrails so enterprise security teams can detect and respond — *that's where tools like Defender plug in.* **Assume your agent will be manipulated and design for graceful failure when it is.**
4. **Regulatory uncertainty.** More than half of leaders admit they don't fully understand how AI will be regulated — EU sector-specific rules in finance and healthcare, evolving guidance in the US. Sunil's advice: **don't wait for the rules to settle. Build observability and traceability now.** If you can answer *"what did this agent do, on whose behalf, with what data, and why?"* you're ready for whatever framework lands.

**The real risk is the compounding effect**, not any single item: an agent with too much access, reasoning over untrusted data, making decisions no one can audit, in a regulatory environment that's still being written. The good news — every one of these problems has an answer, and **most of those answers are things developers control.** As Jeremiah summarizes Sunil's point: the developers who win aren't shipping the flashiest agents; they're building agents **CISOs will actually approve.**

### The core frame: "agent as an actor" → treat agents like new employees
This is the frame shift Sunil says "unlocks everything else." Stop thinking of agents as *features inside an application* and start thinking of them as **members of the workforce.** When a new employee joins, an entire machinery kicks in: IT provisions a managed identity, access is scoped to role, the manager sets expectations, and everything they do is auditable. Nobody calls that bureaucratic overhead — *that's just how organizations operate at scale.* Agents need the same treatment.

The questions enterprise customers ask map almost **one-to-one** to the questions they'd ask about any new hire:
- **Can IT discover and manage them?** Today, mostly *no*. **Register your agents with an identity from day one** — because if IT can't see it, IT can't protect it.
- **Who are they sharing sensitive information with?** Think in **flows of data, not just permissions on individual actions.** An agent can have two perfectly reasonable permissions on their own — *read from a CRM* and *send an email* — and the combination still creates an **exfiltration path**. Design with the full flow in mind.
- **Are they behaving properly?** Build in the **telemetry, behavioral signals, and hooks** that let security teams monitor and course-correct. *You can't fix what you can't see.*
- **Are they well governed and audited?** Every action must be **attributable**: which agent, on whose behalf, with what data, to what outcome.

Sunil's bar for an enterprise-ready agent: *not whether it works — whether it could pass an **onboarding review at a Fortune 500.*** Identity, behavior, data handling, auditability. Build to that bar and you're not just building agents people will *use*, you're building agents enterprises will **trust** — and **trust is what takes a demo to production.**

### The developer pain point Microsoft is solving
Jeremiah pushes back: passing a Fortune 500 onboarding review is a *high* bar, and for a developer just trying to ship, all of this can feel overwhelming. Sunil agrees it's been a big pain point — developers may need a variety of open-source and developing tools, sometimes having to justify, identify, and pass these controls themselves, and figure out how customers will eventually use and benefit from those bespoke implementations. The bottom line: **it's hard to maintain various controls from different vendors and make them all enterprise-proof.** Microsoft's intent is to solve this *for* developers — enable security and governance controls easily in the agents they build, **no matter where they build it, how they build it, and where they run it.**

### Agent 365 — the control plane for agents
**Agent 365 is the control plane for agents**, built so enterprise customers can **observe, govern, and secure every agent** in their environment. It became **generally available on May 1st**, along with the **SDK**. The SDK is "what makes everything real for developers" — and the rest of the session focuses on exactly that: **how a developer uses the SDK to make their agent fully observable, manageable, and governable by Agent 365.**

There are effectively **three on-ramps** into Agent 365, by build surface:

#### 1) Built on Microsoft AI platforms → zero extra work
For makers/developers working in **Agent Builder, Copilot Studio, or Foundry**, getting Agent 365 controls requires **"nothing extra."** Agent 365 is **natively integrated out of the box** with these platforms. No-code, low-code, or pro-code — when you build on Microsoft AI platforms, the agent **shows up in Agent 365 automatically**, with **identity, observability, governance, and security all wired in.**

#### 2) Built on leading third-party platforms → register via connected-platform integration
For agents built on a *different* platform entirely, Agent 365 **already connects directly to leading third-party platforms** like **Vertex AI** and **AWS Bedrock** (with more on the way). Those agents can be **registered in the Agent 365 registry through connected platform integration.** Registration is the **first step to solving agent sprawl** — once your agent is in the registry, **customer admins can discover it.**

#### 3) Built with your own SDK / framework / custom code → the Agent 365 SDK
This is the largest group — developers using **OpenAI's SDK, LangChain, Claude, LlamaIndex, the Microsoft Agent Framework, or fully custom code** — and they need the same things (observability, governance, security), not *just* registration. That's exactly where the **Agent 365 SDK** comes in.

### How the Agent 365 SDK works — incremental, "not all or nothing"
The first principle: the SDK is **not all-or-nothing.** Whatever you're building with, you can **layer Agent 365 capabilities onto what you're already running, incrementally.** You pick **where to start and how far to go** across the three capability tiers — **observability, governance, security.** It's a layer, not a rewrite.

#### Observability
The SDK adds **full OpenTelemetry-based tracing** — capturing **every input, every output, every tool call, every model invocation.** Two paths:
- **Microsoft OpenTelemetry distro (recommended).** Ships with **auto-instrumentation for OpenAI, LangChain, and the Agent Framework**, plus **hooks for everything else.**
- **Direct ingestion to an OTel endpoint.** If you already run an OpenTelemetry pipeline, or you're on a stack the SDK doesn't support yet (**Java** was the example), you can **plug straight in and reuse what you've built.**

A convenience layer: **AI-guided setup for coding agents** that **wires up registration and telemetry for you**, so developers aren't reading docs to get to their first trace.

The security payoff: with observability enabled, **enterprise security teams can use it for threat hunting in the Microsoft Defender portal.** The unified observability the SDK provides enables **both IT and security teams to secure and govern agents with complete visibility.**

#### Governance
The SDK lets a customer's **IT and security teams govern tool access**, including access to **Microsoft 365 data through MCPs.** So **mail, calendar, OneDrive, SharePoint, and Teams** are all reachable through **governed, admin-controlled, auditable, revocable permissions.** Developers **don't have to build bespoke connectors or handle consent flows** — the SDK provides the **tool surface**, and **admins decide what the agent is allowed to touch.** Developers can also **bring their own MCPs and register them with Agent 365** to get the same controlled access across all their MCPs.

#### Security
This is where **Entra Agent ID** comes in (the transcript's "intra-agent ID" — i.e. **Microsoft Entra Agent ID**). Developers **enable Entra Agent ID through the SDK**, and once enabled, a whole set of capabilities **light up for the customer's admins**: **identity protection, conditional access, and ID governance.** The agent gets a **real, verifiable identity**, and admins manage it with the **same Entra controls they already use for users.**

The shortest summary Sunil gives: **bring whatever framework or model you want — the Agent 365 SDK gives you observability, governance, and security as incremental capabilities, not a rewrite.**

### Where Entra and Purview fit after SDK integration
Jeremiah asks how Entra and Purview slot in once the SDK is integrated. Sunil reframes:
- **Entra:** *nothing extra to wire up.* Entra Agent ID is **part of the SDK**, so once integrated, **identity & access management, governance, and threat hunting in Defender all just light up** for the customer — **no additional plumbing.**
- **Purview (data security & compliance):** controls like **sensitivity labels, DLP, and data lifecycle policies** work across the **M365 surface area** (e.g. **Teams**) wherever the agent interacts with users. For *other* scenarios, **Microsoft provides Purview APIs** that developers can use to **wire data controls into the agents they build.** Either way, **enterprise customers configure and enforce their own Purview policies at runtime.** Microsoft is "looking into making this even easier" from a developer perspective.

So it's the **same agent, two extension paths: one built-in (Entra) and one with a runtime hook (Purview).**

### What customers actually get — the three pillars
Once an agent is integrated, here's what security teams get, all built on the **security tool set enterprise customers already use every day**:

1. **Microsoft Entra** — the agent gets assigned an **agent ID**, and from there the agent identity can be **secured and governed like any other identity in the org**: **lifecycle management, conditional access, access governance** — all the controls Entra admins already run.
2. **Microsoft Purview** — **data security and compliance.** Customers manage the **agent's data security posture**, configure **information protection and DLP**, layer in **insider risk management**, and build **compliance controls** so the agent meets the regulatory requirements they're held to.
3. **Microsoft Defender** — security teams **investigate misconfigurations or vulnerabilities** in agents and do **advanced hunting right in the Defender portal**. If the agents integrate with tools like **Microsoft 365 apps**, Defender can also **detect, block, and respond to threats** such as **tool misuse**.

The unifying pattern across all three: **security teams don't have to learn new tools — they work where they already work.**

### The wrap
Jeremiah's closing picture: enterprise customers need controls to **manage agent sprawl, prevent data leakage, protect agents against threats, and meet compliance requirements** — that's the bar customers hold developers to. **Agent 365 is what makes agents meet that bar**, whether you build on Microsoft AI platforms or integrate an agent built anywhere else via the Agent 365 SDK. Sunil's final point for developers: **you don't have to choose between shipping fast and being enterprise-ready.** Build on the framework you already use, and **the moment you integrate, your agents inherit the identity, governance, and security capabilities enterprise customers expect** — *and that's what unlocks adoption.* The session ends pointing viewers to **three resources** to start building with the Agent 365 SDK (save the links).

## 🛠️ Products / Features / Technologies Mentioned
- **Agent 365** — Microsoft's **control plane for agents**; lets enterprises observe, govern, and secure every agent in their environment. **GA May 1st.**
- **Agent 365 SDK** — lets developers layer **observability, governance, and security** onto any agent framework incrementally; the focus of the session. Also a **CLI** exists (Sunil runs both).
- **Agent 365 registry** — where agents (including third-party-platform agents) are **registered** so admins can discover them; **registration is the first step against agent sprawl.**
- **Connected platform integration** — mechanism by which third-party-platform agents get registered into Agent 365.
- **Microsoft Entra / Entra Agent ID** ("intra-agent ID" in captions) — gives the agent a **real, first-class verifiable identity**; enables **identity protection, conditional access, ID/access governance, lifecycle management** with the same controls used for human users. Built into the SDK.
- **Microsoft Purview** — **data security & compliance**: **sensitivity labels, DLP, data lifecycle policies, insider risk management, information protection, compliance controls.** Also exposes **Purview APIs** for wiring data controls into custom agents.
- **Microsoft Defender** — **threat hunting / advanced hunting** in the **Defender portal**; investigate misconfigs/vulnerabilities; **detect, block, and respond** to threats like **tool misuse** and **prompt injection.**
- **Microsoft 365 admin center** — where a registered agent appears as **inventoried, visible, manageable** enterprise asset (shown in demo).
- **OpenTelemetry (OTel)** — the tracing standard the SDK builds on (every input/output/tool call/model invocation).
- **Microsoft OpenTelemetry distro** — recommended observability path; **auto-instrumentation** for OpenAI, LangChain, Agent Framework + hooks for everything else.
- **OTel endpoint (direct ingestion)** — alternative observability path to reuse an existing pipeline or support unsupported stacks (e.g. **Java**).
- **MCP (Model Context Protocol) servers** — the governed tool surface for **mail, calendar, OneDrive, SharePoint, Teams**; developers can also **bring & register their own MCPs** for the same governed, auditable, revocable access.
- **Microsoft 365 data sources via MCP** — Mail, Calendar, OneDrive, SharePoint, Teams.
- **AI-guided setup** — wires up **registration + telemetry** for coding agents automatically.
- **Blueprint** — the registration construct that, combined with Entra Agent ID, makes a GenSpark agent show up and become manageable in the M365 admin center (from demo).
- **Microsoft AI platforms (native integration):** **Agent Builder, Copilot Studio, Foundry** — Agent 365 is wired in out of the box (no-code/low-code/pro-code).
- **Third-party platforms (connected):** **Google Vertex AI**, **AWS Bedrock** (more on the way).
- **Agent frameworks / SDKs supported via Agent 365 SDK:** **OpenAI SDK, LangChain, Claude, LlamaIndex, Microsoft Agent Framework**, and **fully custom code.**
- **GenSpark agent** — the third-party agent used in the live demo, already integrated with the Agent 365 SDK.

## 🚀 Announcements / What's New
- **Agent 365 + Agent 365 SDK general availability — May 1st.** Sunil states Agent 365 was made **generally available on May 1st, along with the SDK.** This is the headline GA called out in the session.
- **Connected-platform integration for Vertex AI & AWS Bedrock — available, more on the way.** Agent 365 *already* connects directly to these leading third-party platforms, with additional platforms described as coming.
- **AI-guided setup for coding agents** — auto-wires registration + telemetry so developers reach their first trace without reading docs. Presented as a current SDK capability.
- **Roadmap / "coming" notes (not dated):** more third-party platform connectors on the way; broader OTel stack support (e.g. **Java** noted as not yet supported by the SDK distro — direct OTel ingestion is the workaround today); and Microsoft is **"looking into"** making Purview data-control wiring **easier from a developer perspective.**
- No private/public-preview SKUs were explicitly named beyond the May 1st GA of Agent 365 and the SDK.

## 💡 Demos
**Live demo — GenSpark agent already integrated with Agent 365 SDK** (presented by Sunil). The demo walks the three pillars end-to-end on a real third-party agent:

- **Identity / discoverability (Entra + blueprint):** Because GenSpark integrates with the SDK, the agent has an **Entra Agent ID and a blueprint**, so it **shows up in the Microsoft 365 admin center** — *visible, inventoried, and manageable like any other enterprise asset.* The instant the agent is **registered through a blueprint**, it gets a **first-class Entra Agent ID in the tenant**, automatically subject to the **same governance the org runs for human users.** Sunil shows the **audit logs** of what the agent has done and the **sign-in logs** to each endpoint the agent made or attempted — *"just like how we audit human users, now we can audit agents."*  
  **Point proved:** an agent built on a non-Microsoft platform becomes a governed, audited tenant identity with zero bespoke identity work.
- **Data governance (Purview):** Every interaction — every message read, every file pulled from SharePoint, every email drafted — **automatically flows through the tenant's Purview policies.** Two controls are demonstrated:
  - A **sensitivity label** configured so **"highly confidential"–labeled documents can only be shared with human users** — this **prevented the agent from reading the document even though the document was created by that agent.**
  - A **DLP rule** to prevent users from **sharing sensitive data with AI agents** — **Purview blocked the message**, enforcing it **at the platform layer.**  
  **Point proved:** the same controls protecting humans now protect (and constrain) the agent, automatically.
- **Threat protection (Defender):** Defender **continuously monitors the agent's behavior** the same way it monitors any tenant user — watching for **anomalous tool calls, unusual data-access patterns, and signs of compromise.** A **high-severity alert** is raised when **the user attempts a prompt-injection attack**; the rule kicks in and **the tool is blocked.** This works for **all tools/MCPs available on Agent 365 *and* your own registered MCPs.**  
  **Point proved:** when something goes wrong, the security team **doesn't need a custom playbook for AI agents — they use the one they already have.**

## 📊 Notable Stats / Quotes
- **82%** of leaders plan to deploy agents in the next **12–18 months** to keep up with workforce demand.
- **80%** of leaders say their **top concern is sensitive data leaking through AI.**
- **88%** of organizations are worried about **indirect prompt injection.**
- **More than half** of leaders admit they **don't fully understand how AI will be regulated.**
- 🗣️ *"An agent is not an app. It's an actor with its own brain. Give it a scoped identity, least-privilege access, and an audit trail from day one. If you bolt on governance later, you have already lost it."* — Sunil Garg
- 🗣️ *"The bar for an enterprise-ready agent isn't whether it works. It's whether it could pass an onboarding review at a Fortune 500."* — Sunil Garg
- 🗣️ *"You can't fix what you can't see."* — Sunil Garg (on telemetry/behavioral signals)
- 🗣️ *"Trust is what takes a demo to production."* — Sunil Garg
- 🗣️ *"The developers who win here aren't the ones shipping the flashiest agents. They are the ones building agents that CISOs will actually approve."* — Sunil Garg
- 🗣️ *"Assume your agent will be manipulated and design for graceful failure when it is."* — Sunil Garg (on prompt injection)
- 🗣️ *"Same agent, two extension paths: one built-in [Entra] and one with a runtime hook [Purview]."* — Sunil Garg
- 🗣️ Key data-flow insight: two reasonable permissions — *read from a CRM* + *send an email* — *"still creates an exfiltration path. Design with the full flow in mind, not just the individual action."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up a minimal custom/LangChain agent and integrate the **Agent 365 SDK** incrementally — start with **observability only** (Microsoft OTel distro), confirm traces, then layer governance, then Entra Agent ID.
  - Reproduce the demo's three guardrails in a test tenant: a **sensitivity label** that excludes agents, a **DLP rule** blocking sensitive data to AI agents, and verify a **Defender** alert fires on a prompt-injection attempt.
  - Try **registering a custom MCP** with Agent 365 and confirm admin-controlled, revocable access to M365 data (mail/SharePoint).
  - Test the **direct OTel ingestion** path for an unsupported stack (e.g. a Java service) vs. the Microsoft distro auto-instrumentation.
  - Explore the **AI-guided setup for coding agents** to see how far it auto-wires registration + telemetry.
- [ ] Questions:
  - What exactly is a **"blueprint"** in Agent 365 vs. plain registration, and how does it relate to Entra Agent ID provisioning?
  - Which agent frameworks does the **Microsoft OTel distro auto-instrument today** beyond OpenAI/LangChain/Agent Framework, and what's the roadmap for LlamaIndex/Claude?
  - What's the **licensing/SKU** model for Agent 365 + the SDK now that it's GA (per-agent? per-tenant? bundled with M365 E5 / Entra Suite / Purview)?
  - How are **Purview APIs** structured for non-M365 ("other scenario") agents, and what's the effort to wire them vs. the built-in Teams surface?
  - For **third-party-platform agents** (Vertex/Bedrock) registered via connected integration — do they get full Entra Agent ID + Purview/Defender, or only registry/discovery until the SDK is also integrated?
- [ ] Relevant to:
  - Any team shipping production agents into a regulated enterprise (finance/health) that must pass a security/onboarding review.
  - Platform/security teams standardizing **agent identity, governance, and threat hunting** on existing Entra/Purview/Defender investments.
  - Developers on **non-Microsoft stacks** (OpenAI SDK, LangChain, Claude, LlamaIndex, custom) who need enterprise-readiness without rebuilding a security stack.

## 🔗 Related
- [[Microsoft Build 2026]]
- Topics: [[Agent 365]] · [[Microsoft Entra Agent ID]] · [[Microsoft Purview]] · [[Microsoft Defender]] · [[Model Context Protocol (MCP)]] · [[OpenTelemetry]] · [[Indirect Prompt Injection]]
- 
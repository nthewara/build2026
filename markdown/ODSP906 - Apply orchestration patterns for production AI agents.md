---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/agents
  - topic/orchestration
  - topic/agent-framework
  - topic/automation
  - topic/uipath
  - topic/production
source: https://www.youtube.com/watch?v=kUDXvURx-yk
session_code: ODSP906
event: Microsoft Build 2026
speakers: Cliff Simpkins (UiPath) + UiPath product team
duration_min: 20
aliases:
  - Apply orchestration patterns for production AI agents
---

# ODSP906 — Apply orchestration patterns for production AI agents

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Cliff Simpkins (Lead, Developer Relations — UiPath) + UiPath product team (keynote highlight reel from UiPath's Bengaluru developer conference)  
> **Duration:** ~20 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=kUDXvURx-yk)

## 🎯 TL;DR
This is a UiPath partner session positioning **UiPath as Microsoft's preferred enterprise agentic automation platform**, built on Azure. The thesis: prototypes and Copilot are great for open-ended work in Microsoft 365, but **complex, long-running, exception-driven enterprise processes** (claims, loans, approvals) need a dedicated **orchestration layer** with governance, durable state, human approvals, and observability out of the box. UiPath's answer is **Maestro**, an orchestration engine offering three canvases — **BPMN** (business processes), the new **Flow** (developer canvas, file-based and coding-agent-native), and **Case** (dynamic, exception-driven work). The second half is a ~15-min cut of UiPath's developer keynote demoing coding agents (Claude Code, Gemini CLI, Codex) building/debugging/deploying on UiPath, plus new **agentic testing** (Autopilot, Delegate) in Test Cloud. Everything shown is available now or in early access; Flow is in early access.

## 🔑 Key Takeaways
- **UiPath = the production "execution layer" for agents**, not the place you prototype them. It supplies governance, observability, human approvals, and durable state out of the box so agents become enterprise-ready.
- **Orchestration ≠ automation.** Automation is "one bot doing one thing at one time." Orchestration is modeling a whole **process** — a journey spanning many heterogeneous tasks (agents that reason, RPA bots, human reviews, ERP/system integrations, exceptions).
- **Maestro is the orchestration engine** at the core of UiPath. It handles control flow for AI agents + human approval steps + system integrations, manages state across long-running processes, and handles retries, timeouts, and partial failures. Every process is observable and automatable out of the box.
- **Three Maestro canvases map to three operating models:** **BPMN** (time-tested BPMN 2.0 standard for business-process owners), **Flow** (developer canvas), and **Case** (complex, dynamic, exception-driven processes).
- **Flow is the new developer-friendly canvas** running on the Maestro runtime. Its key differentiator: a **schema natively supported by coding agents**, so a coding agent can author the entire flow file and drive everything that happens in it.
- **Flow is file-based and local.** Flow files live on your machine in VS Code, so you get **Git / version control** for reviewing changes you and teammates make — proper developer workflow, not a locked web designer.
- **Agents are configured inline in Flow** — tools, context, prompts, output schema, advanced error handling, and **platform-level guardrails** (PII detection, harmful-content detection, user-prompt-attack defense) — no separate project required.
- **Case is for dynamic, exception-driven work** (e.g. loan origination). It is **not** straight-line BPMN: stages have **no arrows**; the **case manager** activates each stage via rules or **agent reasoning**, enabling parallel work, re-entering stages, escalations, and ad-hoc stages without losing continuity.
- **Coding-agent support is platform-agnostic.** Demos used Claude Code, Gemini CLI, and Codex interchangeably; UiPath provides CLIs/tools giving agents full, governed control of the platform.
- **GitHub Copilot integration:** install **UiPath skills + CLI via npm** and Copilot gets full context on UiPath APIs, CLI commands, and deployment patterns — build/deploy/manage agentic automations without leaving VS Code.
- **UiPath conversational agents now run in Microsoft Teams** — packaged via standard Teams packaging; employees use them in 1:1 chats or channel workflows to submit info, check status, and get updates.
- **Evaluations are coming to end-to-end processes in Flow** — think "test cases for your process orchestrations," extending agent evals to whole orchestrations.
- **Agentic testing in Test Cloud** targets the testing bottleneck created by AI-accelerated code: **Autopilot** runs/explores tests autonomously (Playwright on web, Appium on mobile, plus SAP/Epic/Citrix), and **Delegate** eliminates QA busy-work (running tests, filing Jira issues, reporting).
- **Because UiPath runs on Azure, you inherit existing security, identity, and compliance** — "nothing new for you to approve."
- **Headline industry stats cited:** 40%+ of code is now AI-generated; 85% of developers use coding agents.
- **Adoption is low-friction:** install the CLI, add UiPath skills to GitHub Copilot, start building in VS Code — entry point at **uipath.com/developers**.

## 📚 Detailed Notes

### Framing: why a dedicated orchestration layer (and what UiPath is)
Cliff Simpkins (Dev Relations lead at UiPath) opens by positioning UiPath as **Microsoft's preferred enterprise agentic automation platform** — built on Azure and deployed into some of the most governed enterprise environments. For developers, three things matter:
1. **UiPath Orchestrator is the execution layer that makes an agent production-ready** — governance, observability, human approvals, and durable state all out of the box. It's the enterprise runtime your agents deploy directly into.
2. **GitHub Copilot users can build on UiPath out of the box** — install UiPath skills + CLI via npm and Copilot gets full context on the platform's APIs, CLI commands, and battle-tested deployment patterns; you can ship without leaving VS Code.
3. **Running on Azure means inherited security, identity, and compliance** — the controls the enterprise already trusts, "nothing new to approve."

UiPath is known for its **RPA roots**, but the pitch is that the platform is now a **runtime for orchestrating complex, agentic processes** — one of the only platforms that can manage agents, robots, human-review steps, system integrations, and exceptions together in a governed, auditable execution environment. Developers keep flexibility: low-code tools, pre-built agents, **or custom agents using the frameworks/models/tools they already trust**, with secure access to data **without moving or duplicating it** (built-in data governance for stringent compliance).

### Maestro — the orchestration engine and its responsibilities
At the core of the platform is **Maestro**, the UiPath orchestration engine. Its job is to handle **control flow** across a process that mixes AI agents, human approval steps, and system integrations. Concretely Maestro:
- **Manages state across long-running processes** (durable orchestration that survives over time).
- **Handles retries, timeouts, and partial failures** — the reliability primitives production processes need.
- Makes **every process observable and automatable out of the box**.

The mental model the team stresses: **automation is one bot doing one thing at one time, but a *process* is a journey that spans many tasks.** Some tasks are automations (RPA), but others are **agents that reason** (e.g. an investigation/triage agent), **humans** doing reviews/approvals, or **integrations into ERP systems**. Maestro is what stitches these heterogeneous task types into one governed flow — this is the "orchestration pattern" the session title refers to, applied at enterprise scale rather than as in-code agent primitives.

### The three Maestro canvases (the orchestration "patterns")
Maestro supports **three canvases** to model how an organization operates — the session essentially frames these as three orchestration styles:

- **Maestro BPMN** — the **business process canvas**, built on the **BPMN 2.0 standard**. Time-tested and still the industry standard for process owners. Best for well-defined, linear-ish business processes.
- **Maestro Flow** — the **developer canvas** (new). Same Maestro runtime underneath (enterprise governance, auditability, durability) but a developer-friendly, **file-based** experience whose schema is **natively understood by coding agents**.
- **Maestro Case** — for **more complex and dynamic business processes**; purpose-built for **exception-driven** work that doesn't fit a linear flow.

### Pattern 1 — Maestro BPMN (linear, standards-based business orchestration)
BPMN is positioned as the foundation: it uses the **BPMN 2.0 standard**, which process owners already know and trust. It's the right tool when the process is well-understood and largely sequential. Importantly, capabilities shown in Flow (extraction nodes, script routing, data-fabric lookups, agents) are noted as **also supported in Maestro BPMN** — Flow is a different authoring surface, not a different capability set.

### Pattern 2 — Maestro Flow (developer canvas, coding-agent-native)
Flow is the headline developer story. Key points from the demo (a **billing-dispute process**):
- **The canvas is new; the runtime is Maestro** — so you keep enterprise-grade governance, auditability, and durability.
- **Coding-agent-native schema:** unlike other visual workflow tools, Flow's schema is designed so **a coding agent can write the entire flow file** and affect everything in the flow. You build alongside Claude Code (sidebar), Codex (terminal), etc.
- **Local files + version control:** Flow files live on your **personal machine in VS Code**, so you (and teammates) review changes via **Git or any VCS** — real developer workflow.
- **Multiple triggers of different types:** the demo starts from a manual/webhook trigger, then adds an **Outlook "email received" trigger** — Flow supports several trigger types on one flow.
- **Inline agent configuration (no separate project):** add an agent node and configure its **tools, context, escalations, prompts, output schema, and advanced error handling** inline. You can also **wire outputs from previous nodes** and preview the output schema.
- **Platform-level guardrails on agents:** **PII detection, harmful-content detection, and user-prompt-attack** protection — described as critical so you can trust an agent that runs on inbound email.
- **Rich node types in the flow:** an **invoice extraction node referencing an IXP project** (so you don't call a separate process to do IXP extraction from Maestro), **script nodes** for routing, **native data-fabric lookups**, **discrepancy detection** on a constructed payload, then a second agent for **dispute analysis** with an **inline context-grounding index** (the agent consults its standard operating procedure).
- **Full observability / trace view:** the **trace view** shows **every call an agent makes** plus the inner workings of all platform components the flow references.
- **Human approval inline:** the dispute agent routes to an **approval task** that **shows up right in your screen** — no trip to Action Center or another platform; approve and keep debugging.
- **End-to-end finish:** call an **API function for a financial adjustment in the ERP**, hand to a **final agent** that drafts the customer email, send it, and fire a **Slack** notification internally.
- **Evaluations for whole processes:** UiPath announced **bringing evaluations to end-to-end processes in Flow** — "test cases for your process orchestrations," extending the agent-eval concept to entire orchestrations.

The recurring message: *"You don't have to choose between a developer experience you actually enjoy and the power of an enterprise platform — with Flow you get both."*

### Pattern 3 — Maestro Case (dynamic, exception-driven orchestration)
Case targets the messiest reality. The motivating example is a **loan process**: many departments, missing documents that get kicked back and resubmitted, partial reprocessing of only the newly submitted docs, and mid-process life events (e.g. changing jobs) that alter how the loan is processed — i.e. lots of **exceptions, ad-hoc steps, and deviations** the process must handle natively. Maestro lets you **visualize and harness this complexity** instead of forcing it into a linear flow where you'd have to define every path.

Demo: **loan origination implemented in Maestro Case** (a "case plan"):
- A new canvas **purpose-built for dynamic, exception-driven work** — "not just straight-line BPMN."
- Structure: a **case manager** on top; the case is organized into **stages**, with **tasks** under each. Tasks can be **agents, API workflows, RPA, BPM, or external agents** — anything you could do in Maestro BPMN.
- **Crucially, after the intake stage there are NO arrows in the diagram.** Each stage is **activated based on what the case manager decides — via rules or agent reasoning** — rather than fixed sequential edges. This is the core difference from BPMN.
- **Rework illustrated:** sanction screening ran **twice**; the **execution trail** is opened to see why. The **case agent always gives its rationale** for each decision it made.
- **Parallelism + escalation:** **underwriting and escalation run in parallel**. The trace shows the agent **reasoned a medium-risk loan should go to a manager for approval (escalation) but should also proceed to underwriting** because it isn't high-risk — i.e. a task can **cross boundaries and activate multiple stages at once.**
- The summary of the dynamism: **parallel work, re-entering stages, escalations, and ad-hoc stages — all without losing continuity.**

### Coding agents across the lifecycle (build → debug → deploy)
A central theme: developers are now the most leveraged people in their company, and coding agents compress the lifecycle. The "same five stages, dramatically different timelines" — planning/building drop from months to hours/days; debugging/deploying/testing to hours; an incident can be remediated in **minutes** (a coding agent can even start before you get the incident).

Demos:
- **Failing onboarding queue (Claude Code):** an onboarding automation in an online portal fails on a Friday. Claude Code investigates like a human but faster — goes to **Orchestrator**, reads logs, investigates target systems, forms and tests hypotheses, and finds the root cause (**target system blocked the APIs**). It produces a clear timeline (what/why/when) and a suggested fix. Told to fix it, it walks the existing code + recommendations, **switches the automation from API to UI** when needed, identifies the required UI element, and (fast-forwarded ~30 min) has built an **object repository, UI files, and the needed actions** (filling the form, typing inputs), then **builds the package and pushes it to Orchestrator** — all in the same trusted, governed environment.
- **Platform-agnostic agents (Gemini CLI):** to prove the coding-agent support is **agnostic**, the same kind of work is done with **Gemini CLI** — it reads the **PDD**, understands the requirement, and recommends structuring the code as a **producer/consumer with a queue.**

The takeaway line: *"You get coding agents to help you from build to troubleshoot to production and back."* UiPath provides the **tools and CLIs** that give agents full, governed control of the platform.

### Agentic testing — keeping QA up with AI-speed code (Test Cloud)
Because code ships faster, **testing risk rises too**. UiPath's **Agent Testing solution in Test Cloud** moves from manual testing to **AI-augmented / autonomous software testing**, with three capabilities under one mission (autonomous software testing):
- **Autonomous test-case execution with Autopilot:** manual tests that **run themselves with no pre-built automations** — point Autopilot at the tests, give it a mission, and it executes across the **web (Playwright)**, **mobile (Appium)**, or any UI including **SAP, Epic, Citrix**.
- **Autonomous test *exploration*:** hand Autopilot a goal and it returns **full coverage with edge cases you didn't think of**, plus planning/mapping of application testing.
- **UiPath Delegate** — your "sidekick" that **eliminates QA/testing busy-work** (the administrative overhead).

Demo (**Delegate**, tester at a bank): asked to run all assigned tests, email the test manager, and file any issues. Delegate pulls **"skills"** to talk to UiPath products (it reads info from **Test Manager** in context), and — beyond planning — it **interacts with desktop/web/any applications** under test. It identifies the problem, collates info, **files the issues (a Jira link is shown with full context + results)**, creates reports, and **publishes results back to Test Manager** — the skills keep it on track. The framing: *"not the future of testing — this is happening right now."*

### Microsoft-focused integrations (the joint architecture)
The recommended architecture for a **Microsoft-first environment**: most enterprise work starts in **Microsoft 365**, but complex processes (claims, loans, approvals) need a dedicated orchestration layer **Copilot wasn't designed to be out of the box.** So:
- Employees **collaborate in Teams, Outlook, SharePoint, and Copilot** to orchestrate open-ended/complex tasks.
- Those complex tasks **run in UiPath's orchestration layer** — problem-solving, dynamic decisions, and long-running execution across documents, desktops, legacy apps, and enterprise systems.
- **If a human is needed, the process surfaces it back to a human via Teams.**
- Net: users, teams, and data stay where they are, with an orchestration engine bringing them together.

Two **new Microsoft integrations** called out:
1. **UiPath conversational agents in Microsoft Teams** — agents are built/deployed in UiPath (using the extensive **integration service connectors**) then deployed via **standard Teams packaging**; employees use them in **1:1 chats or channel-based workflows** to submit info, check process status, and receive updates without leaving Teams.
2. **Copilot unlocks the UiPath platform** — install **UiPath skills + CLI via npm**, and Copilot gets full context on the platform's **APIs, CLI commands, and deployment patterns**; from there you build, deploy, and manage agentic automations on UiPath using your preferred coding agent.

### Reliability, observability & governance for orchestrated agents (the production story)
Pulling the production threads together, the orchestration patterns are made "production-grade" by capabilities baked into Maestro/Orchestrator rather than bolted on:
- **Durable state + retries/timeouts/partial-failure handling** for long-running, multi-step processes (Maestro).
- **Observability everywhere** — every process is observable out of the box; the **trace/execution view** exposes every agent call and every platform-component interaction, and the **case agent records its rationale** for each decision (auditable reasoning).
- **Human-in-the-loop** as a first-class task type (approval tasks inline in Flow; surface-to-Teams in the joint architecture).
- **Guardrails** at the platform level (PII, harmful content, prompt-injection/user-prompt-attack defense) applied to agents.
- **Governed, auditable execution environment** spanning agents, robots, human steps, and system integrations — with **Azure-inherited** security/identity/compliance.

### Wrap-up & availability
Closing message: if you're building AI agents that must run in an enterprise environment where you need **audit trails, processes that cross multiple systems/teams, and humans in the loop**, UiPath is worth evaluating, and the **entry point is low friction**. Install the CLI, add the UiPath skills to GitHub Copilot, and start building on the platform **without leaving VS Code**. Everything to get started (SDKs, docs, CLI, GitHub Copilot skills, community resources) is at **uipath.com/developers**.

## 🛠️ Products / Features / Technologies Mentioned
- **UiPath** — Microsoft's preferred enterprise agentic automation platform; built on Azure, deployed into highly governed environments.
- **UiPath Orchestrator** — the execution/runtime layer that makes agents production-ready (governance, observability, human approvals, durable state); coding agents read its logs and push packages to it.
- **Maestro** — UiPath's orchestration engine; control flow + durable state + retries/timeouts/partial-failure handling; observable and automatable out of the box.
- **Maestro BPMN** — business-process canvas built on the **BPMN 2.0** standard (for process owners).
- **Maestro Flow** — new developer canvas on the Maestro runtime; file-based, local, coding-agent-native schema, inline agent config, multi-trigger.
- **Maestro Case** — new canvas for dynamic, exception-driven processes; stage/task model driven by a **case manager** via rules or agent reasoning (no fixed arrows).
- **IXP (Intelligent Xtraction / document extraction)** — referenced via an **invoice extraction node** in Flow so extraction runs without a separate process.
- **Data Fabric** — native data lookups inside a flow.
- **Context grounding index** — inline grounding for agents to consult standard operating procedures.
- **Integration Service connectors** — used to build/deploy UiPath conversational agents.
- **UiPath CLI + UiPath skills (npm)** — give coding agents (and GitHub Copilot) full, governed context/control of the platform.
- **GitHub Copilot** — gains full UiPath context via the skills/CLI; build/deploy/manage in VS Code.
- **Claude Code** — coding agent used to investigate/fix the failing onboarding queue (sidebar in Flow).
- **Gemini CLI** — coding agent used to prove platform-agnostic support (producer/consumer + queue).
- **Codex** — coding agent (terminal) cited as usable in Flow alongside Claude Code.
- **UiPath Test Cloud** — home of the agentic/autonomous testing solution.
- **UiPath Autopilot (testing)** — autonomous test execution + exploration; Playwright (web), Appium (mobile), plus SAP/Epic/Citrix UIs.
- **UiPath Delegate** — autonomous QA "sidekick" that runs tests, interacts with apps, files issues, and reports; uses "skills" to talk to UiPath products.
- **UiPath Test Manager** — test management product Delegate reads from and publishes results to.
- **Microsoft 365 / Teams / Outlook / SharePoint / Copilot** — collaboration surfaces in the joint architecture; Teams hosts conversational agents and human escalations; Outlook provides the email-received trigger.
- **Azure** — UiPath runs on Azure, so customers inherit existing security, identity, and compliance controls.
- **Slack** — used for an internal notification at the end of the Flow billing-dispute process.
- **Jira** — Delegate files bug issues into Jira with full context + results.
- **Playwright / Appium** — web and mobile automation engines Autopilot uses to execute tests.
- **BPMN 2.0** — the time-tested process-modeling standard underpinning Maestro BPMN.
- **Object Repository / UI files** — UiPath UI-automation artifacts the coding agent generated for the onboarding fix.
- **PDD (Process Definition Document)** — read by Gemini CLI to understand and structure the automation.

## 🚀 Announcements / What's New
- **Maestro Flow (developer canvas)** — new visual canvas on the Maestro runtime with full VS Code + coding-agent support; schema is natively authorable by coding agents. **Status: early access**, with public availability "in the coming weeks."
- **Maestro Case** — new canvas purpose-built for complex, dynamic, exception-driven processes (stage/task model driven by a case manager via rules or agent reasoning). Shown as a major evolution of Maestro/business orchestration.
- **Evaluations for end-to-end processes in Flow** — announced; "test cases for your process orchestrations," extending agent evals to whole orchestrations.
- **UiPath conversational agents in Microsoft Teams** — new integration; deploy UiPath agents into Teams (1:1 and channel workflows) via standard Teams packaging.
- **GitHub Copilot ↔ UiPath integration (skills + CLI via npm)** — gives Copilot full UiPath platform context for build/deploy/manage in VS Code. **Status: live now**, with full GitHub Copilot support.
- **UiPath CLI + UiPath skills** — **live now**.
- **Agentic testing in Test Cloud — Autopilot (autonomous test execution + exploration) and Delegate (QA busy-work elimination)** — framed as "what we're delivering next"; the Delegate capability was demoed as already working ("happening right now"). Overall, everything shown is **"available now or in early access."**
- ⚠️ This is a UiPath (partner) session, so these are **UiPath product announcements** surfaced at Microsoft Build, not Microsoft product GAs. Exact GA dates beyond "now" / "early access" / "coming weeks" were not given.

## 💡 Demos
- **Failing onboarding queue, fixed by Claude Code (Orchestrator):** Claude Code reads Orchestrator logs, investigates target systems, forms/tests hypotheses, finds root cause (target system blocked APIs), produces a timeline + suggested fix, then implements it — switching the automation from API to UI, generating an object repository/UI files/actions, building the package, and pushing to Orchestrator. **Proves:** coding agents can do end-to-end investigate→fix→deploy in a governed environment, compressing incident remediation to minutes.
- **Gemini CLI building a producer/consumer automation:** reads the PDD, understands the requirement, recommends a producer/consumer + queue structure. **Proves:** UiPath's coding-agent support is platform-agnostic (not tied to one vendor's agent).
- **Flow billing-dispute process (live run):** Outlook email trigger → classification agent (with guardrails) → IXP invoice extraction node → script-node routing → native data-fabric lookups → discrepancy detection → dispute-analysis agent with inline context-grounding index → inline approval task (approved on-screen) → ERP financial-adjustment API → final agent drafts customer email → send email + internal Slack notification; trace view shows every agent call and platform-component interaction. **Proves:** a complete, observable, human-in-the-loop enterprise process built/run in a developer-friendly, version-controlled canvas.
- **Maestro Case loan origination:** case plan with a case manager + stages/tasks and **no arrows after intake**; shows **rework** (sanction screening ran twice, with agent rationale in the execution trail) and **parallel underwriting + escalation** (agent reasoned a medium-risk loan needs manager approval *and* should proceed to underwriting). **Proves:** dynamic, exception-driven orchestration — parallel work, re-entering stages, escalations, ad-hoc stages — without losing continuity.
- **Delegate autonomous testing (bank tester):** asked to run all assigned tests, email the test manager, and file issues. Delegate pulls "skills" to read Test Manager, interacts with desktop/web apps under test, identifies the problem, files Jira issues (link shown with full context + results), creates reports, and publishes results back to Test Manager. **Proves:** autonomous QA that handles the full pre/post-test busy-work, not just planning.

## 📊 Notable Stats / Quotes
- **"40% or more of code is now generated by AI."**
- **"85% of developers use coding agents to do their work now."**
- On the lifecycle shift: *"The world of development… has dramatically changed in the last 12 months — more so than it changed in the last two decades"*; building/planning compress *"from months to hours and days,"* and an incident can be remediated *"in minutes"* (a coding agent can start *"even before you get an incident"*).
- *"Automation is one bot doing one thing at one time. However, process is a journey that spans many tasks."*
- *"The canvas is new, the runtime is Maestro."* (Flow)
- *"You don't have to choose between a developer experience you actually enjoy and the power of an enterprise platform. With Flow, you get both."*
- *"What you're seeing is not the future of testing. This is what is happening right now."* (Delegate)
- ~**15-minute** keynote cut; UiPath's developer conference ran ~**3 weeks** before Build in **Bengaluru**.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install the **UiPath CLI + skills via npm** and add them to **GitHub Copilot**; build a trivial automation end-to-end in VS Code without leaving the editor.
  - Stand up a **Maestro Flow** billing-dispute–style process and drive it with **Claude Code / Codex**; commit the flow file to Git and review the diff to feel the "flow-as-code" workflow.
  - Prototype a **Maestro Case** plan for an exception-heavy process (e.g. loan/claim) to see case-manager rules vs. agent-reasoning stage activation, parallel stages, and rework.
  - Wire a **UiPath conversational agent into Teams** and test 1:1 + channel workflows with human escalation back to Teams.
  - Trial **Autopilot/Delegate** in Test Cloud on a web app (Playwright) to gauge autonomous coverage + Jira filing.
- [ ] Questions:
  - How does Maestro's **durable state + retry/timeout** model compare to Durable Task / Temporal-style orchestration, and is there an OpenTelemetry export for the trace view?
  - For **Case**, how is the case manager's decision policy authored/governed (rules DSL vs. an LLM agent) and how is non-determinism audited/replayed?
  - Where does the **agent reasoning** in Flow/Case run (which models, hosted where) and how do the platform guardrails (PII/prompt-injection) integrate with Azure AI Content Safety?
  - What exactly do the **"skills"** Delegate/Copilot consume look like (schema/format), and can custom skills be authored?
  - Pricing/licensing model for Maestro Flow/Case + Test Cloud at enterprise scale?
- [ ] Relevant to:
  - Anyone taking agents **from prototype to production** who needs governance, durable state, human-in-the-loop, and audit trails on top of (or alongside) Microsoft 365 / Copilot.
  - Enterprise architects designing **multi-agent, multi-system, exception-driven** processes (claims/loans/approvals) in a Microsoft-first environment.
  - Teams adopting **coding agents** (Claude Code/Gemini/Codex) for build→debug→deploy and wanting platform-agnostic agent support + agentic testing.

## 🔗 Related
- [[OD820 - Designing Reliable Multi-Agent Apps with Azure Cosmos DB]]
- [[BRK241 - From prototype to production build and run agents at scale]]
- [[ODSP909 - Take AI agents from prototype to production with OpenTelemetry]]
- [[Microsoft Agent Framework]]
- [[Multi-agent orchestration patterns]]
- [[Human-in-the-loop agent design]]
- Source list: [[2026 Build Session List]]

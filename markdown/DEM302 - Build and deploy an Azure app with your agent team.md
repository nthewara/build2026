---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/agents
  - topic/azure
  - topic/github-copilot
  - topic/foundry
  - topic/devops
source: https://www.youtube.com/watch?v=c4xpRbUytLw
session_code: DEM302
event: Microsoft Build 2026
speakers: Brady Gaster (GitHub), Ron (PM, Microsoft)
duration_min: 26
aliases:
  - Build and deploy an Azure app with your agent team
---

# DEM302 — Build and deploy an Azure app with your agent team

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Brady Gaster (GitHub — joined "a couple weeks ago", creator of *Squad*) & Ron (PM at Microsoft, Foundry)  
> **Duration:** ~26 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=c4xpRbUytLw)

## 🎯 TL;DR
A fully live, two-person demo (no slides until the final CTA) that builds and deploys a complete **multi-agent customer-insights system** for a fictional retailer "Zava" — entirely through prompting. **Ron drives everything inside VS Code** using GitHub Copilot + the **Foundry Toolkit VS Code extension** to scaffold a 4-agent workflow with the **Microsoft Agent Framework**, wire it to enterprise data via a **Foundry Tools Toolbox**, debug it with the **Agent Inspector**, add **evaluations** at scale, and **deploy it as a hosted agent** in Microsoft Foundry. **Brady then forks her repo and works entirely inside Copilot CLI**, unleashing **Squad** (his open-source multi-agent framework for Copilot) plus **Azure MCP tools + Azure skills** to provision the Foundry instance, build a React front end, and deploy both front end and back end to **Azure Container Apps** — with the front end and agent reusing the same Foundry model across two compute hosts, secured via **Managed Identity**. The throughline: humans write almost zero code; agents (and teams of agents) do the building, the infra, the fixing, and even document their own work.

## 🔑 Key Takeaways
- **You can go from prompt → production multi-agent app → live deployment without writing code by hand.** Both presenters repeatedly stress "I did not write a single line of code."
- **The Microsoft Agent Framework** is the open-source orchestration layer for multi-agent systems; an entire 4-agent workflow (with conditions and branching) is composed in essentially **one `workflow` function / four lines of code**.
- **Copilot learns new/unfamiliar services via skills.** Because Agent Framework and Foundry are brand-new, Copilot pulled the **Foundry skill** shipped with the Foundry Toolkit VS Code extension to get current knowledge before scaffolding.
- **Plan mode first, then implement** — Ron switches Copilot to plan mode to discuss and lay out the architecture before generating code; it's cheaper and produces a better plan.
- **The 4 agents:** (1) **Classifier** (sentiment: positive/negative), (2) **Enrichment** (looks up customer + order data, VIP status), (3) **Triage** (decides whether to draft a customer email), (4) **Aggregate** (assembles the final result).
- **Foundry Tools Toolbox** packages many tools behind **one unified endpoint + one auth** — here bundling **Azure AI Search** (product catalog index) and a **Fabric IQ connector** (customer/orders data). Only the enrichment agent is granted the toolbox.
- **Microsoft Fabric** is positioned as the single data platform where all your data lives; agents in Foundry connect back to it through the toolbox.
- **Agent Inspector** (Foundry Toolkit extension) is a visualizer + playground + debugger: live workflow diagram built from **runtime object models**, hover-to-inspect variables, and **per-node capture of every runtime event** (inputs/outputs).
- **Evaluations are added by prompting** ("add evaluations to my agent") — Copilot reads the source, generates a **10-row test dataset**, selects + implements **evaluators**, and submits the eval run via the **Foundry MCP server**, with results viewable inside VS Code.
- **Deploy a hosted agent with one command** ("deploy hosted agent") via a short wizard → fully managed + observable, with a live playground talking to the real service.
- **Live log streaming + one-click Copilot fix:** the hosted-agent playground streams server-side call stacks; clicking sends the messages to Copilot, which can fix errors/exceptions in place.
- **Squad** = Brady's open-source **multi-agent framework for GitHub Copilot** (built with his friend Tamir). Token-hungry (many agents talk simultaneously) but reaches the goal faster than single-threaded chat.
- **Give agents distinct roles, not identical instructions** — otherwise they "fight over work like hungry hungry hippos." Each Squad agent knows only its job and collaborates with others.
- **Azure MCP server + Azure skills** power Squad: MCP tools (incl. all Foundry tools) provide the *capabilities*; **Azure skills** (markdown files on disk) tell Copilot *how to use those tools the right way* to complete tasks.
- **Agents adapt to mistakes autonomously:** Squad re-targeted the deployment from the wrong compute host (Container Apps) to the correct Foundry endpoint and rewrote everything in ~1 hour using its skills + tools.
- **One Foundry model, reused across two compute layers/hosts**, with the React front end and the agent back end authenticating to each other via **Managed Identity (MI)** — secure cross-app communication.
- **Squad self-documents:** at the end it produces a **report** of everything it wrote, deployed, the tools used, and the skills consulted.

## 📚 Detailed Notes

### Setup, speakers & framing
This was billed as the **last demo in the theater for the evening** (the Chainsmokers were performing after). Brady Gaster opens — he joined **GitHub a couple of weeks ago** — and hands to **Ron**, a **PM at Microsoft**. Their explicit goal: **be in a live demo within the first minute**, and use the ~25 minutes to **build a "Zava customer insights agent system" together**. Zava is framed as an online retailer that "really cares about customers" and wants to understand and act on customer feedback. A running gag/constraint: **Ron does literally everything inside VS Code** ("you can tell me if I ever step out of VS Code"), while **Brady does everything inside Copilot** (CLI + a customized "for Build in San Francisco" Copilot app).

### The end product (what they're building toward)
Before touching code, Ron shows the finished app: a **front-end website** connected to a back-end **agent team running in Microsoft Foundry**. It ingests customer feedback, analyzes sentiment, and **takes actions**. Example feedback items shown:
- *"Price reasonable but delivery was slow"* → **mixed** sentiment (positive + negative).
- *"App crashed"* → clearly **negative**.
- *"My item arrived damaged very bad"* → **negative**.

For the damaged-item case, the system didn't just classify sentiment — it **connected the feedback to a specific customer**, looked up their orders in **Microsoft Fabric**, and **determined a free replacement was warranted**, triggering downstream actions. All of this happens agent-side via **multiple agents working together**.

### Kicking off in VS Code: prompt + plan mode
Ron's very first action was opening VS Code + Copilot and sending essentially this prompt:
> *"I want to build a production-ready Foundry hosted agent using the Microsoft Agent Framework."*

Workflow habits demonstrated:
- **Switch to plan mode** so Copilot **discusses and lays out a plan before implementing** — cheaper and better-architected.
- Because the demo is time-boxed, she replays the **actual history from ~a week earlier** (same prompt) rather than waiting live.

**Why Copilot needs help:** both the **Microsoft Agent Framework** (a "really wonderful" open-source multi-agent orchestration framework) and **Microsoft Foundry** are **very new** and **actively being built**. So when asked to use them, Copilot **pulled up the Foundry skill** shipped with the **Foundry Toolkit VS Code extension** to learn the latest about the service and framework before it could plan the build.

### Evolving from one agent to a team of four
The initial idea was trivial: a single **sentiment analysis** agent that takes feedback and returns a positive/negative score. Iterating with Copilot in plan mode, Ron expanded it into a **multi-agent system of four agents**:
1. **Classifier agent** — determines negative vs. positive feedback.
2. **Enrichment agent** — looks up back-end data: *which customer is this? Is this a VIP? What's their order status?*
3. **Triage agent** — decides *do I need to draft an email to the customer?*
4. **Aggregate agent** — **puts everything together** into the final result.

Copilot then **scaffolded the entire project** — Ron reiterates she **did not write a single line of code**.

### The code: orchestration in ~4 lines
Copilot generated code using the **Microsoft Agent Framework** (shown via its import statement). The key reveal: the **four agents are composed with roughly four lines of code**, and a **single `workflow` line** ties everything together — including **conditions and branching flows between agents**, all defined in **one function**. (Hard to read intent from raw code alone — hence the Agent Inspector visualizer later.)

### Connecting to enterprise data: Fabric + the Toolbox
The enrichment agent needs **customer + order data living in Microsoft Fabric**. Fabric is pitched as the **one platform where all your data lives**. The challenge: *if my agent runs in Microsoft Foundry, how do I connect back to Fabric data?* → **Foundry Tools + Toolbox.**

A **toolbox** is "a way to package various tools into a single entity" your program interacts with. Ron's toolbox bundles:
- **Azure AI Search** — indexing a **product catalog**.
- A **Fabric IQ connector** — linking to **customer and orders data**.

Benefits: **one unified endpoint + one unified authentication** — *connect once, reach everything in the toolbox*. A single line of code **attaches the toolbox to the enrichment agent only**; all other agents lack that capability (least-privilege by design).

### Running the agent locally
Everything runs **locally**: code on local disk, but **connecting to a Foundry model in the cloud** and to the **toolbox** (part of the Foundry service). She prepares **test data in raw JSON** (the format Brady's front end will later replace) and runs it.

### Agent Inspector (Foundry Toolkit VS Code extension)
A possibly-new UI that serves **multiple purposes**:
- **Visualizer** — left-hand diagram showing how multiple agents flow together (clarifies what's hard to see in code).
- **Playground** — send a payload and watch it execute.
- **Debugger** — standard VS Code debugging: **hover to inspect variables** (she sees 3 payload items; first two classified negative, last positive), step/continue through the workflow.
- **Live diagram updates** — built from **runtime object models**, so you can follow execution in real time.
- **Per-node runtime event capture** — *every event in and out of every agent* is captured; selecting a node shows its specific **input and output** (e.g., what the enrichment agent takes in vs. emits).

A nice ops tell from Ron: *"I know things are working when it's taking a long time — because it didn't fail right away"* (the enrichment agent's Fabric/AI Search calls take a moment). Results show **overall sentiment**, **per-item product identification**, and a **draft email** produced by one of the agents.

### Adding evaluations at scale (by prompting)
A 3-item payload is fine as a **PoC/prototype**, but production needs **scale testing + formal evaluations**. Being "lazy," Ron just told Copilot:
> *"Add evaluations to my agent."*

Because Copilot **has access to the source code**, it understands the agent's inputs/outputs and **figured everything out**, generating:
- A **test dataset of 10 rows** (simulated customer-feedback scenarios).
- A set of **evaluators** — suggested *and* implemented automatically.

She replies *"all looks good, just run it,"* and Copilot uses the **Foundry MCP server** behind the scenes to **submit the evaluation directly to the Foundry service**. Results are then **viewable directly inside VS Code**.

### Deploying as a hosted agent
Everything so far ran locally. To get a **fully managed + observable hosted agent**, Ron runs:
> *"deploy hosted agent"*

A short **wizard** ("a couple steps") completes the deploy. The hosted agent gets a **playground** like the local one — but this one **talks to the live service**.

### Ron's favorite feature: live log streaming + one-click Copilot fix
The hosted-agent playground provides **log streaming** as the agent runs, including **all server-side call stacks**. The "magic": **review logs directly in VS Code** — clicking **extracts the messages from the service and sends them to Copilot**, and if there are **errors/exceptions/issues, Copilot can fix them right there**. This closes the loop: deploy → observe → diagnose → fix, all without leaving the editor. Ron then hands off to Brady for the front end.

### Handoff to Brady: fork, clone, and "throw a squad at it"
Contrast in styles: Ron did everything in **VS Code**; Brady does everything in a **customized Copilot ("for Build in San Francisco")**, rarely inside VS Code. He **forked Ron's repo first** (*"otherwise it'd be rude"*) then **cloned it** locally — now he has her code and wants to **"throw a squad at it."**

**What is Squad?** A **multi-agent framework for GitHub Copilot** that Brady built with his friend **Tamir**. It runs **multiple agents talking at the same time** — uses **a lot of tokens**, but **reaches the endpoint quicker** than a single-threaded conversation with Copilot. Works in **brownfield or greenfield**, brand-new or existing repos.

### Bootstrapping Squad
Inside the repo he types **`squad init`** (using the **"no workflows" version** — *"if you know, you know"*), which lays down **a bunch of files on disk**. Then in Copilot he goes to **autopilot mode**, selects the **`squad` GitHub Copilot agent** (*"yes, I trust you, Brady and Squad"*), and fires a prompt from his **cheat sheet**. Copilot reads the code + prompt and **builds a team of agents** for him.

He deliberately gave the agents **"cool names" instead of descriptive ones**. Crucial design principle:
> If you send all agents the **same instructions**, *"they'll fight over work like hungry hungry hippos."* Instead, **each agent knows only its job** and **collaborates** with the others.

### The back end: Azure MCP tools + Azure skills
Two `MCP`/`skills` introspection commands reveal Brady's toolbox:
- **MCP servers/tools** — including all the **Azure MCP tools** from the **Azure MCP server**, dialed into his CLI **by default** (plus **all the Foundry tools**). These are the **capabilities** for "all the different Azure things and Foundry things."
- **Azure skills** — *"a series of markdown files on disk that tell Copilot how to use all those MCP tools together the right way to get tasks done."*

So his Squad — and anything on his Copilot instance — has access to **all those tools + all those skills**, letting him **"talk to my squad in [my] favorite language"** and get going.

### Provisioning Foundry — and recovering from a wrong compute host
Brady's first prompt: take Ron's code and **provision a new instance in Azure Foundry — and only that** (the infra was "already written"… by **Squad, in the hotel room last night**, because he's "too lazy to do it myself").

The honest war story: he'd originally been **deploying the agent to the wrong compute host (Azure Container Apps)**. Ron proofread it the night before and flagged *"that's the wrong endpoint."* He told Squad, and **Squad changed everything in ~1 hour** — *using all those skills and tools, working together to figure out how to rewire it.* He'd **never used the service** and feared he'd never get it working, but was **done in ~45 minutes**, crediting the skills + tools.

### The front end: React on Azure Container Apps via `azd`
Second prompt: **"the backend is live"** and the **React front-end code is already written by Squad** (Brady is a **.NET person**, so he has a **React agent on the team**). Now deploy it as a **second container app**.

Brady works **almost entirely in the CLI** via **`azd` (Azure Developer CLI)**. He asked Squad to deploy **both front end and back end 100% with `azd`**. Squad honestly determined it **couldn't be done with `azd` alone** — there were **additional steps required with the Foundry SDK/CLI**. Not only did Squad **figure that out**, it realized it could perform them as a **post-deployment hook** using the existing infra — **and just did it**.

Running that second command deploys the front-end stack: an **Azure Container App**, a **Container Apps environment**, a **Container Registry** (newly needed), and a **Log Analytics workspace** — all standard **dependencies of an ACA environment** required by the **React front end**, *not* by Ron's agent code.

### The surprise: one Foundry model across two compute hosts
Clicking into the deployed front end → **"send feedback."** The reveal (a surprise even to Ron): the **front end calls her Foundry model to generate fake feedback**. So the **same Foundry model instance is reused across two different compute layers / two different compute hosts**, with the two apps **authenticated to one another using Managed Identity (MI)** → *"completely secure with those apps talking to each other."* Entirely built with **prompts + Squad + the existing tools** installed in **both** his CLI and her VS Code (*"the same tools, CLI and everything else"*).

### Squad self-documentation report
At the very end, Squad produces a **report** showing **everything the squad agents did**: everything they **wrote**, everything they **deployed** (incl. **Python**), all the **tools used**, and all the **skills consulted** (Brady notes they consulted even more during development *"because I don't know how to use half this stuff"* — the skills laid down all the IaC). Takeaway: you can have the squad **do the work *and* document it on the fly**.

### Call to action (the single slide)
Both presenters are visibly proud of finishing on time. The CTA:
- **Foundry Toolkit for VS Code** — install it.
- **Azure skills + Azure MCP tools** for your **Copilot CLI** — *"install all of it. You need it all."*
- **GitHub Copilot** (the app) — get it.
- **Try Squad** — like it, hate it, leave comments/issues/PRs. It will **always stay an open-source project**, though it may **move out of "some guy's organization"** to somewhere more efficient (**no ETA**).

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — service hosting the agents/model; supports **hosted agents** (managed + observable); brand-new and actively evolving.
- **Microsoft Agent Framework** — open-source multi-agent orchestration framework; composes the 4-agent workflow with conditions/branching in ~4 lines + one `workflow` function.
- **Foundry Toolkit (VS Code extension)** — ships the **Foundry skill**, the **Agent Inspector**, deploy commands, and eval result viewing.
- **Foundry skill** — current knowledge about Foundry/Agent Framework that Copilot pulls to scaffold correctly.
- **Foundry Tools / Toolbox** — packages multiple tools behind one unified endpoint + auth.
- **Azure AI Search** — product-catalog index inside the toolbox.
- **Microsoft Fabric** + **Fabric IQ connector** — single data platform for customer/orders data; connector links it into the toolbox.
- **Agent Inspector** — visualizer + playground + debugger; live runtime diagram + per-node event capture.
- **Foundry MCP server** — submits evaluation runs to the Foundry service.
- **GitHub Copilot** — app + **Copilot CLI**; plan mode, autopilot mode, custom agents.
- **Squad** — open-source multi-agent framework for GitHub Copilot (by Brady Gaster & Tamir); `squad init`, "no workflows" mode.
- **Azure MCP server / Azure MCP tools** — Azure + Foundry capabilities dialed into the Copilot CLI by default.
- **Azure skills** — markdown files telling Copilot how to use MCP tools correctly.
- **Azure Container Apps** + **Container Apps environment**, **Azure Container Registry**, **Log Analytics workspace** — front-end (React) compute + dependencies.
- **Azure Developer CLI (`azd`)** — primary deployment tool; extended via Foundry SDK/CLI **post-deployment hook**.
- **Managed Identity (MI)** — secure auth between front-end and back-end apps.
- **React** — front-end framework (built by a dedicated Squad "React agent").
- **Python** — back-end language scaffolded/deployed by the agents.
- **VS Code** — Ron's entire workflow surface.

## 🚀 Announcements / What's New
None explicitly announced as new releases — this was a **live demo session**, not a launch keynote. That said, the session **surfaces and showcases very new / actively-evolving capabilities**:
- **Microsoft Foundry hosted agents** + **one-command deploy** ("deploy hosted agent") with managed/observable runtime, live playground, and **log streaming with one-click Copilot fix**.
- **Microsoft Agent Framework** for multi-agent orchestration (explicitly called "very new").
- **Foundry Toolkit VS Code extension** features: **Foundry skill**, **Agent Inspector** (live runtime visualizer + event capture), and **MCP-driven evaluations**.
- **Foundry Tools / Toolbox** unifying Azure AI Search + Fabric IQ behind one endpoint/auth.
- **Squad** — Brady's open-source multi-agent framework for GitHub Copilot (still in "some guy's org," may relocate; no ETA).

## 💡 Demos
- **End-product walkthrough** — Zava feedback site classifying mixed/negative feedback and auto-deciding a free replacement (Fabric order lookup → action).
- **Prompt → plan → scaffold** — single prompt in Copilot plan mode produces the 4-agent architecture; Copilot pulls the Foundry skill to learn the framework.
- **Orchestration code reveal** — 4 agents in ~4 lines + a single `workflow` function with conditions/branching.
- **Toolbox wiring** — one line attaches the Azure AI Search + Fabric IQ toolbox to *only* the enrichment agent.
- **Local run + Agent Inspector** — live workflow diagram from runtime object models, hover-to-inspect variables (3 items; 2 negative, 1 positive), per-node input/output event capture, draft-email output.
- **Eval-by-prompt** — "add evaluations to my agent" → 10-row dataset + evaluators auto-generated, submitted via Foundry MCP server, results in VS Code.
- **One-command hosted deploy** — "deploy hosted agent" wizard → live playground + **log streaming** with **one-click Copilot fix** of server-side errors.
- **Fork → Squad init** — Brady forks/clones Ron's repo, runs `squad init` (no-workflows), autopilot mode builds a named team of collaborating agents.
- **CLI tooling tour** — Azure MCP tools (incl. Foundry) + Azure skills (markdown how-to files) listed from the CLI.
- **Provision Foundry + recover** — Squad re-targets from wrong host (Container Apps) to correct Foundry endpoint in ~1 hour; Brady productive in ~45 min on a service he'd never used.
- **`azd` front-end deploy** — React app → second Container App; Squad self-discovers it needs a **Foundry SDK/CLI post-deployment hook** and adds it; stack includes ACA env, Container Registry, Log Analytics.
- **Cross-host model reuse** — front end calls Ron's Foundry model to generate fake feedback; same model across two compute hosts, secured with **Managed Identity**.
- **Squad self-documentation report** — lists everything written, deployed (incl. Python), tools used, and skills consulted.

## 📊 Notable Stats / Quotes
- **4 agents, ~4 lines of code** — the entire multi-agent workflow composed via one `workflow` function.
- **10-row** auto-generated evaluation dataset.
- **~1 hour** for Squad to re-platform from the wrong compute host (Container Apps) to the correct Foundry endpoint.
- **~45 minutes** for Brady to get a never-before-used service working, thanks to skills + tools.
- **~25 minutes** total demo budget; goal to be **"in a live demo in the first minute."**
- **1 Foundry model reused across 2 compute layers / 2 compute hosts.**
> *"I did not write a single line of code here."* — Ron (a recurring refrain from both presenters).
> *"If you just send all the agents the same instructions, they're going to fight over work like hungry hungry hippos."* — Brady, on why each agent needs a distinct role.
> *"I know things are working when it's taking a long time — because it didn't fail right away."* — Ron, on the enrichment agent's Fabric calls.
> *"Squad wrote that infra in the hotel room last night because I'm too lazy to do it myself."* — Brady.
> *"A toolbox is really just a way to package various tools into a single entity that you can interact with from your program."* — Ron.
> *"Those are a series of markdown files on disk that tell Copilot how to use all those MCP tools together the right way."* — Brady, on Azure skills.
> *"Install all of it. You need it all."* — Brady's CTA.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install the **Foundry Toolkit VS Code extension** and explore the **Agent Inspector** (runtime visualizer + per-node event capture) on a toy multi-agent workflow.
  - Build a minimal **Microsoft Agent Framework** workflow (classifier → enrichment → triage → aggregate) and confirm the "~4 lines" orchestration claim.
  - Stand up a **Foundry Tools Toolbox** combining **Azure AI Search** + a **Fabric IQ connector**; test the single-endpoint/single-auth claim and least-privilege (attach to one agent only).
  - Try the **"add evaluations to my agent"** prompt flow → confirm Copilot auto-generates dataset + evaluators and submits via the **Foundry MCP server**.
  - Try **one-command hosted deploy** + **log streaming → one-click Copilot fix** loop.
  - Install **Squad** (`squad init`, no-workflows mode) on a brownfield repo; test the "distinct roles vs. hungry hippos" effect.
  - Wire **Azure MCP server + Azure skills** into **Copilot CLI**; deploy a React front + Python back to **Azure Container Apps** with `azd` and confirm the **Foundry SDK/CLI post-deployment hook** pattern.
  - Reproduce **cross-host Foundry model reuse** secured with **Managed Identity** between front end and back end.
- [ ] Questions:
  - Where does **Squad** end up living (it may move out of "some guy's organization")? What's the repo + license? (No ETA given.)
  - How does the **Foundry MCP server** authenticate eval submissions, and what evaluators are available out of the box?
  - What exactly is the **"no workflows" version** of Squad vs. the workflows version?
  - How does the **Foundry hosted agent** pricing/quotas compare to running locally?
  - What are the precise **Foundry SDK/CLI steps** that `azd` alone can't cover (the post-deployment hook)?
  - Is the **Foundry skill** auto-pulled, or must Copilot be told to use the Foundry Toolkit?
- [ ] Relevant to:
  - Anyone building **multi-agent systems on Microsoft Foundry** with the **Agent Framework**.
  - Teams connecting agents to **enterprise data in Fabric** via toolboxes.
  - **Agentic dev workflows** (Copilot + Squad) for greenfield/brownfield app delivery.
  - **Azure deployment** patterns: ACA + `azd` + Foundry hosted agents + MI.

## 🔗 Related
- [[DEM303 - Late to agentic coding Dont panic build]] — sibling DEM demo on getting started with agentic coding.
- [[DEM312 - Multi-agents in action 3 agents 3 frameworks]] — sibling multi-agent demo (compare orchestration approaches).
- [[DEM301 - Rethinking CI Actions AI Agents End of Commit-Fail-Commit]] — sibling agentic-dev/CI demo.
- [[ODSP923 - Create enterprise apps with AI and MCP]] — enterprise apps with AI + MCP tooling.
- [[BRK243 - Claw and agent harness in Microsoft Foundry]] — agent harness on Foundry (deeper dive).
- [[BRK241 - From prototype to production build and run agents at scale]] — prototype → production agents (mirrors the eval/deploy arc here).
- [[DEM340 - Build work-ready agents with Foundry and Work IQ]] — Foundry agents + IQ data connectors.
- Source list: [[2026 Build Session List]]

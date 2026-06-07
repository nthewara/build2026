---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/foundry
  - topic/agent-harness
source: https://www.youtube.com/watch?v=e_ZJy3RsNkg
session_code: BRK243
event: Microsoft Build 2026
speakers: Sean Henry, Glenn, Amanda
duration_min: 46
aliases:
  - Claw and agent harness in Microsoft Foundry
---

# BRK243 — Claw and agent harness in Microsoft Foundry

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Sean Henry (Microsoft Foundry), Glenn (Hermes deployment demo), Amanda (Teams / M365 Copilot publishing demo) — all on the Microsoft Foundry team  
> **Duration:** ~46 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=e_ZJy3RsNkg)

> [!note] On the title "Claw"
> "Claw" in the title is **not** a separate Microsoft product. The session repeatedly uses **"claw" / "claw-style" / "claw-like"** to describe the class of autonomous agent harnesses popularised by **OpenClaw** — local, always-running agents that own a sandbox/VM, carry their own memory and skills, self-improve, and talk to you over a messaging channel. **Hermes** is presented as a "second-generation" claw-like agent (similar ingredients, not a literal OpenClaw fork). The talk's real subject is **agent harnesses** and how to deploy these claw-style patterns into Microsoft Foundry.

## 🎯 TL;DR
This session unpacks what an **agent harness** is — the "car" you build around the LLM "engine" so it can run long, complex tasks — and shows three concrete ways to get advanced, "claw-style" agents running in **Microsoft Foundry**. Sean Henry defines the harness's core components (agent loop, context management, skills/tools, sub-agent orchestration, memory/session persistence, lifecycle hooks, human-in-the-loop). Glenn demos deploying **Hermes** (an off-the-shelf claw-like agent) onto **Foundry Hosted Agents**, using a new **Routines** feature (preview) for nightly self-maintenance and a shut-down-when-idle design to avoid paying for an always-on sandbox. Sean then shows building a **custom** harness with **Microsoft Agent Framework** (now v1.0) — agent loop + workflows + harness — and deploying it to Foundry, a console TUI, or an AG-UI web front end. Finally Amanda demos **one-click publish to Teams / M365 Copilot** and introduces a third agent identity type, **Autopilot agents**, which act on their own behalf with a real user account (email, Teams, documents), exemplified by a group-chat **workstream manager** sample.

## 🔑 Key Takeaways
- An **agent harness** = the shell of tools/scaffolding around an agent that lets it perform longer, more complicated tasks. Analogy: the model is the **motor/engine**; the harness is the **whole car** (wheels, steering, seats) that makes the motor useful.
- The harness's **core nugget is the agent loop**: give the LLM context + available tools → it requests tool calls → execute tools → feed results back → loop until the goal is reached.
- Other harness components: **context management** (incl. context compaction), **skills + tools** (skills = text-based capabilities; tools over MCP/OpenAPI/code), **giving the agent a computer** (file system + code/program execution = human-like capability), **sub-agent orchestration**, **memory & session persistence** (which lets the runtime be **stateless**), **lifecycle hooks** (before/after agent, LLM, tool calls — where you inject policy), and **human-in-the-loop** for higher-risk actions.
- **"Claw-style" agents** (OpenClaw-popularised pattern): own their sandbox/VM, have memory + skills + autonomy, run for long periods, talk to you via Telegram/Slack/etc., and **self-improve** with use. They are extremely **"pet-like"** (you literally name them).
- **Hermes** is a claw-like agent with those ingredients but is **not an OpenClaw fork**; Glenn deployed it onto **Foundry Hosted Agents** (which provide a **built-in sandbox**).
- **Routines** (new, **in preview**) let agents react to external/scheduled stimuli — e.g. Hermes auto-creates a **nightly maintenance routine** that prunes stale skills and backs the agent up to blob storage; routines can **spin a shut-down sandbox back up** to do maintenance, then let it idle off again.
- **Agent state makes each instance unique by design** (own skills/content/learning) — but that uniqueness causes **pain when recovering/resuming from errors**, so you must deliberately decide how to handle/back up state.
- Foundry Hosted Agents keep the **sandbox file system for ~30 days of inactivity**; the **Foundry session ID controls which file system / VM** the agent gets — changing it spins up a brand-new agent from the deployed snapshot.
- **Microsoft Agent Framework** (Python + .NET, full feature parity) reached **v1.0** (released to preview Oct last year). Three parts: **agent loop**, **workflows**, **harnesses**.
- You can now **`.AsAgentHarness()`** on top of any chat client/agent to get file-system/code/shell tools + context compaction **for free**, then customise by swapping "Lego bricks" rather than assembling from scratch.
- Agent Framework connects to many model providers (OpenAI, Anthropic, Gemini, Bedrock, local via Ollama) and agent types (Foundry prompt agents, Copilot Studio, Claude Code, GitHub Copilot CLI, A2A), and deploys to Foundry Hosted Agents, Azure Functions, Azure Container Apps, even AWS.
- **Workflows** support multi-agent patterns: sequential/hand-off (context moves too), author-critic, and **Magentic** (a planner/supervisor pattern built with Microsoft Research); plus custom directed workflows mixing agents with plain code, authored in code or **YAML**.
- **AG-UI** (open standard for UI ↔ agent) + **CopilotKit** let you put a real web UI on a harness agent with a couple of lines (enable AG-UI endpoint), including **auto-generated charts/controls for free**.
- Foundry offers **one-click publish to Teams + M365 Copilot** — fill a short form, choose self-only or submit to the **Microsoft admin center** for org-wide approval; you get **both Teams and Copilot UIs out of the box**.
- New **Autopilot agents**: the third agent identity type (after **assistive** and **autonomous**). Unlike autonomous agents, an autopilot agent has a **real user account** (email alias, can send Teams messages, create Word docs on its own behalf) — removing the limitation that work-IQ-style actions previously needed a human's identity. **Scout** is cited as a ready-made example of an autopilot agent.

## 📚 Detailed Notes

### Framing: Foundry's three layers for agents
Sean Henry opens (day two of Build) introducing himself and colleagues **Glenn** and **Amanda**, all on **Microsoft Foundry** — Microsoft's AI platform for using models and building AI apps and agents. The session is a deep-dive follow-on to Tina and Jeff's Foundry overview from the prior day.

Foundry's mental model is a stack of layers:
1. **Intelligence (bottom):** the **models** — Foundry exposes "thousands… hundreds of models" usable with agents.
2. **Runtime (middle):** how agents are **hosted, deployed, and managed** in Foundry.
3. **Human + agent collaboration (top):** where agents **meet you where you work** — Teams, M365 Copilot — to help you every day.

All wrapped in a cross-cutting layer of **trust, security, manageability, observability, and evaluations** needed to run agents in production. A core Foundry value is **choosing your level of simplicity vs. control**: start with simple prompt agents built in the portal, or move to **advanced agents written in code**, bringing your own libraries and connecting to other systems. This talk focuses on the **agent runtime** and the **collaboration** layer for those advanced agents.

### What's changed in the last six months
Referencing a similar talk he gave at **Ignite six months ago**, Sean notes how much has shifted:
- **Frontier models got very good at coding**, changing the role of software development — coding agents now do most of the actual coding while humans **supervise** and ensure the right thing gets built. Tools cited: **GitHub Copilot, Claude Code, Cursor**.
- **OpenClaw** emerged: an agent that **runs locally with your credentials**, that you **interact with over messaging**, **constantly running**, waiting for you.
- A **second generation** of these "claw-style" apps appeared (**Hermes**, covered later).
- The new frontier: taking the **agent-harness techniques** learned from coding agents and claws and **applying them to scaled enterprise applications** — the whole point of the session.

### Defining the agent harness
Sean acknowledges there are "dozens of definitions" and offers Foundry's: an agent harness is **the shell — the set of tools you put around your agent so it can perform longer, more complicated tasks.** The **engine/car** analogy: a motor alone is useless; you need wheels, steering, seats — but you still need the core motor.

**Components of an agent harness:**

- **The agent loop (the core "nugget"/motor):** give the agent context + available tools, call the LLM for a response; it typically asks you to execute tools; you run them and return results; loop continues until the goal is reached. This is the traditional-agent concept at the heart of the harness.
- **Context management:** as you add prompts, messages, tools, skills, the context grows. The harness proactively **keeps context contained**, including **context compaction** — looking at everything in the context window and compacting it to something more manageable.
- **Skills and tools:** tools have always existed; **skills** (text-based capabilities you add to the agent) are now much more common. Tools come over **MCP, OpenAPI**, or code. A key insight: **tools that give the agent a computer are very powerful** — file-system read/write, the ability to **write and execute code**, or **run programs** — enabling more **human-like tasks**.
- **Agent orchestration:** the harness **manages/orchestrates specialised agents** (e.g. web browsing, code execution, document synthesis).
- **Memory & session persistence:** so the agent **remembers things about you and what it learned** to improve over time. Critically, this lets the **runtime be stateless**, so it can be hosted across different environments/deployments — important when agents run for long periods.
- **Lifecycle hooks:** connect the agent to your existing apps at every cycle — before/after the agent runs, before/after the LLM call, before/after tool calls — **the place to apply your app-specific policy and logic**.
- **Human-in-the-loop:** as agents do more powerful/advanced things, the harness provides **channels for direct human communication**, so the agent can **ask a human before a higher-risk tool call/execution** (e.g. writing files or executing code).

These are framed as the **core capabilities common across all agent harnesses** (there are others). The rest of the session shows three ways to get harnesses into Foundry.

### Demo 1 — Deploying Hermes (an off-the-shelf claw-like agent) into Foundry (Glenn)

**Clarifying "claw-like":** Glenn adds colour on the **claw pattern**: take a harness that has **memory**, **owns its environment** (sandbox or VM), has **tools** and **autonomy**, can **execute for long periods deciding its own actions**, and typically has a **communication platform** (Telegram, Slack, etc.). **OpenClaw popularised** this architecture. Many things are "literally claws" or a flavour of claw (he mentions **nano-claw** and "various things… that have claw in their name"). **Hermes** has the same claw qualities/ingredients but is **not literally an OpenClaw clone or fork** — its makers do many of their own things. Hermes focuses heavily on a **"collective wisdom" / constant self-improvement** layer: the more you do a task with Hermes, the **better it gets** at it.

**The deployment goal / design constraint:** Most claw-like architectures today are optimised to run on a machine/VM the agent **owns** — making them the **most "pet-like" thing invented since the start of cloud computing** (recalling the early-cloud **"pets vs. cattle"** analogy; you literally name them). Glenn wanted a setup where the **back end runs on Foundry** but the agent is **always available to talk to**, yet **shuts down when idle** so he isn't **paying for it all the time** — "I always had this Hermes there… but I wasn't paying for it all the time."

**The setup shown:**
- Back end on **Foundry**; Glenn "lives in the terminal," so the interface is a **Hermes TUI** running on his machine.
- He's **not using OpenShell** today (left in the script as something you might want depending on deployment) because **Foundry Hosted Agents has a sandbox built in**, which he relies on.
- On start-up the TUI **connects to a Hermes agent running on Foundry Hosted Agents**, using his **local Azure Default Credential** to reach the endpoint, then the **same Entra credentials to pull a model from Foundry** (a Foundry model).
- He tries to have Hermes read a SharePoint file (`build demos.docx` — the demo script for Tina & Jeff's session) via a **Work IQ SharePoint MCP** (shown as "MCP … Work IQ SharePoint"). **Conference networking failed**, so the MCP download didn't work — but the architectural point stands: **Hermes is deployed to the cloud, has a toolbox connection, and uses its identity + yours to reach the Work IQ MCP / SharePoint.**

**The state / maintenance problem and Routines (new, preview):**
- As you work, **Hermes generates files, skills, and context on disk** — which can start to **cause problems** (bloat/staleness).
- In the **Foundry portal**, the deployed agent has a **Foundry agent endpoint** the TUI connects to, plus a new section called **Routines** (**"this is new… in preview"**).
- Hermes ships **maintenance routines** that **curate skills** — delete stale/old skills, etc. Because Glenn **doesn't want the sandbox running forever**, the agent **shuts down after ~15 minutes of idle time**, and the **routines spin it back up when it's time to do maintenance**, then let it idle off again.
- The portal showed a **maintenance routine that had already run** (its output appeared at the top of the TUI on launch).
- A **shell script** sets environment variables and runs the TUI, pointing it at the back end. It contains a **session ID** string (e.g. *"George the Build Hermes"*). **Every Foundry session ID controls the file system the agent gets.** Changing it (e.g. to *"Jeff the Build Hermes"*) yields a **brand-new Hermes** — new file system, new VM — **recreated from the snapshot** deployed when the Hermes agent was created. On first launch the new agent **automatically creates a new nightly maintenance routine**.
- That **nightly maintenance routine**: deletes old scheduled skills, curates files, and **importantly backs Hermes up** — creating an **independent backup** (onto **blob storage**) so the files are always safely on disk.
- **Routines** generally let an agent **react to external stimuli** and **prompt an agent to do something**. You create one by selecting an **agent + session + prompt + recurrence** — but, crucially, **agents can create routines themselves to re-enter the same session**. That's why the listed routines have "weird names": **each was created by the agent itself** to maintain itself because it knew it needed to.

**The overall topology Glenn built:**
- Hermes runs **in the cloud**; a **TUI** is on his local machine; a **proxy** carries the (agent-to-engine) **protocol over the network** to the cloud Hermes agent; a **routine** manages and looks after the agent's context.
- After a fresh respawn (because the internet was bad), it worked: **isolated in a sandbox**, with Work IQ access, correctly identifying the demo document as **authored by Jeff Holland**, and the new instance had **auto-created its own routine** he could run **test runs** against.

**Glenn's key point — state:** the **agent state creates unique environments**; every Hermes instance/file system/agent in a claw-like pattern is **unique by design** (you *want* uniqueness so it keeps its own skills/content and keeps learning/evolving). But (as learned **painfully** building cloud apps) **uniqueness causes pain when recovering/resuming from errors**, so **you must decide how to handle that state**. His chosen constraint: **nightly backup to blob storage** + reliance on Foundry Hosted Agents **keeping the sandbox file system for ~30 days of inactivity** (deleted only after 30 days idle; otherwise kept indefinitely while in use).

**Wrap / call to action:** Glenn has **all the code available** (a **proof of concept** he keeps evolving), invites people to find him to use Hermes/routines, and notes he's making **PRs directly into the Hermes repo** to improve its Foundry integration.

### Demo 2 — Building a custom harness with Microsoft Agent Framework (Sean)

Sean pivots from off-the-shelf to **building your own custom harness** with **Microsoft Agent Framework** — Microsoft's **library/SDK for building AI applications and agents** in **Python and C#**, **released to preview last October**, recently reaching **version 1.0** "a couple months ago."

**Three parts of Agent Framework:**

1. **Agent loop** — the core **AI agent construct**. Builds loops that talk to **Foundry models, Foundry tools, and host directly in Foundry**, but also connects elsewhere in the AI ecosystem: **OpenAI directly, Anthropic directly, Gemini, Bedrock, local models via Ollama**, and **any tool over OpenAPI / MCP / code**. **Deploy anywhere:** Foundry Hosted Agents, **Azure Functions, Azure Container Apps**, or even **AWS** ("I don't know why you'd want to do that"). It also provides **connectors that abstract other agent providers** — connect to **Foundry prompt agents** (declarative agents built in Foundry), **Copilot Studio agents**, **Claude Code agents**, **GitHub Copilot CLI agents** (many people bridge their agent systems into GitHub Copilot), or the broader ecosystem via the **A2A (agent-to-agent) protocol**.

2. **Workflows** — built-in constructs for **multi-agent systems**:
   - **Sequential / hand-off** — one agent talks to another, **moving the context** along.
   - **Author–critic** — agents continually **refine output**.
   - **Magentic** — a **planning** pattern built with **Microsoft Research**: a **supervisor agent generates a plan** and **sub-agents work through it**.
   - **Custom directed workflows** — a full directed-workflow capability; you can **mix agents with regular code** ("not everything needs to be an agent"), authored in **code or declaratively in YAML**.

3. **Agent harnesses** (the latest addition) — the **shell on top of the agent**: common **tools** (file-system access, code execution, shell execution), **built-in context** (chaining prompts + skills + agent memory smartly before handing to the LLM), **planning capabilities** (these systems often — not always — work much better with a planning phase plus specialised sub-agents), and **extensive middleware** (context compaction, **tool selection** algorithms, **permissions/capabilities** definitions for what the agent and its tools can do). Enables **deep-research agents, coding agents (à la GitHub Copilot / Claude Code), content-generation agents** — **goal-driven agents** you give an abstract goal and let them plan their own path to success. Being a framework, you can **build your own custom harness and mix-and-match** harnesses with workflows.

**Coding demo (shown in C#; full parity in Python):**
- Familiar first lines set up a **chat client** = the **core agent loop**.
- New capability: **slap an agent harness on top of any agent** via **`.AsAgentHarness()`**. A **minimal** harness is two lines (lines ~79–80 in his sample), and those two lines will become **optional after preview**.
- Adding the harness gives **all those tools, plus compaction, for free**. Contrast: old Agent Framework was "a bunch of **Lego bricks** you attached together"; the harness approach gives you the **thing already built**, and you **take bricks away or swap pieces** to customise.
- **Customising — a research agent example:** configured with a **name + description + metadata**; a **tool that converts a web page into a markdown file**; **model-level settings like reasoning effort**; **where to store files / memory / which files to grant access to** (a **file access store**); **where telemetry goes** — it **emits the full complement of OpenTelemetry from the GenAI spec**, sendable up to Foundry or anywhere; and **preconfigured background agents** (e.g. one doing **web search in the background**).
- **Harness Console (a TUI)** — built to make harness agents **easy to run, demo, and prototype**, similar to Hermes' TUI. He runs the research agent through it with **configuration, listeners, observers, and event handlers** for events coming off the agent.
- **Live run:** prompts *"write a blog about Microsoft Agent Framework announcements at Build 2026."* The agent enters **plan mode** (modes include **plan** and **plan-and-execute**; can show its **to-do list** and **export the session**). It calls many tools, loads skills (he'd prebuilt a **blog-outlining skill**), reads files, builds a **to-do list**, and downloads info to build an outline. It then hits a **human-in-the-loop** moment, **asking what type of blog/content** (a harness event the console listens for); they pick **"developers building AI agents."** It continues building/iterating the plan; when finished it **shows the plan and asks for approval to execute**. They **approve and execute** and it **writes the blog post**, running in the background over a long period.
- **AG-UI + CopilotKit (web UI):** because customers usually **don't want a TUI**, Foundry worked with the **AG-UI** and **CopilotKit** folks. **AG-UI** = an **open standard for UI that talks to agents**. With a couple of lines (similar to **ASP.NET** usage) you **enable AG-UI on top of your agent** via an app, giving it an **AG-UI endpoint**; **CopilotKit** provides a library that talks directly to it. Demoed a **different agent given a sales CSV**, showing the **same harness behaviours** (tool calls appearing/completing) in a **nice web UI** (you can hide tool calls in production). With **CopilotKit's built-in controls**, the agent can **generate charts** — **no extra code**, just telling the agent it can produce these controls/charts — "for free."
- **Deploy to Foundry:** because it's just an agent, use the **agent host builder** to create a **responses endpoint** and interact with it (with tools). Shout-out to the **Foundry Toolkit Agent Inspector** for building/debugging agents — connect to your agent, view **previous responses and events**, and **debug** through it. Hitting **deploy** takes a few minutes; Sean had deployed one earlier so showed his agent **up and running in Foundry**, now behaving like **any other agent** — interact with it, see **traces**, and use all of Foundry's tools to **manage, monitor, and evaluate** it.

Summary of Demo 2's three ways to run/consume the same harness agent: **(1)** in a **workflow with no UI at all**, **(2)** in a **console/TUI** application, or **(3)** in a **web UI** via AG-UI — and then **deploy directly into Foundry**.

### Demo 3 — Getting agents where people work: Teams & M365 Copilot publishing + Autopilot agents (Amanda)

Amanda covers **"what comes next"** once an agent is built: you usually **don't want a standalone UI** — you want the agent in the **surfaces you use every day**. Foundry provides **one-click publish to Teams and M365 Copilot**: once an agent is deployed, a **drop-down** lets you fill in a few details and the agent is **instantly available** (scoped to yourself), with an option to **share with your whole organisation**.

**Publishing experience (demoed with a simple prompt agent):**
- Once you have a **tested version** you're happy with, click the **Publish** drop-down → **"Publish to Teams and M365 Copilot."**
- A dialog lets you **name the agent** and provide **key details** — importantly these are **what end users see** when interacting (focused on **actions it can perform**, not internal implementation details).
- Next page offers two options: **make it available just to yourself** (shows up immediately, usable right away) or **submit to the Microsoft admin center for approval** → once approved, **available to everyone in your org**. There's also an option to **download and customise**.
- She'd pre-published a **Zava** *customer & product support agent* and showed it in **M365 Copilot** answering *"what products do we sell."* Key benefit: **one publish gives you BOTH the Teams and Copilot UIs out of the box** — nothing else to build.

**Three agent identity types in Foundry:** Amanda situates a new type against the two existing ones. **All** agent types have a unique **Entra agent identity**, but they differ in **whose behalf they act on**:
1. **Assistive agents** — typically a **personal productivity** agent given a **Work IQ** tool; can **send emails / draft Teams messages on your behalf**; most functions are an **extension of you**.
2. **Autonomous agents** — usually **run in the background**; you can **assign the agent's identity permissions** (e.g. on an **Azure resource group** or **storage account**), trigger it from a **non-human, chat-based trigger**, and it **performs actions on its own behalf**. **Limitation:** the Work-IQ-style actions available to assistive agents **can't be done** here — because those need a user account.
3. **Autopilot agents (NEW)** — also always act on **their own behalf**, but the difference is they have a **real user account**, giving the agent its **own email address/alias**, the ability to **send Teams messages on its own behalf**, and **create Word documents on its own behalf** — essentially **any action, even those that normally require a user account**. (Amanda demoed a snippet of these in **yesterday's keynote**.) **Scout** in Foundry is positioned as **one out-of-the-box example** of an autopilot agent; Foundry gives you the **platform to build any type of autopilot agent** yourself.

**Workstream Manager hero sample (group-chat autopilot agent):** Foundry focused on a hero scenario called the **workstream manager agent**, built around **group-chat behaviours** as the key unlock:
- **Automatically tracks open items**; can **answer questions about everything in your team's chat**; includes an **onboarding flow**.
- After deploying the sample, you go to the **Microsoft admin center → Requests tab**, **approve** the agent, then go to **Teams and "hire" it**.
- Because she **created the instance**, she gets an **onboarding message** asking **who it should be able to talk to** (by **default only the creator** can). She grants access to teammates (**Seth, Elijah**, others); the agent will then **respond to them one-on-one and in group chats**.
- **Access control demo:** she throws **Burke** (no access) plus the workstream manager into a chat and says hi — the point being you have **complete control over who can talk to it**.
- **Out-of-the-box group-chat behaviours:** for every message it will respond to, it **signals it's working on a response**; if you **@-mention** the agent it **@-mentions you back**; and **critically it does NOT respond to every message** — when she asks **other chat members** to do things, the agent **stays silent**, which is **essential behaviour for agents in group chats**.
- Call to action: **start building with the code sample** — a set of examples **meant to be tailored** to your team's needs and behaviour preferences.

### Wrap-up (Sean)
The session showed **three things** under the banner of **agent harnesses**: (1) taking an **off-the-shelf harness — Hermes — and deploying it into Foundry**; (2) **building custom harnesses with Microsoft Agent Framework** and running them in Foundry; and (3) **getting agents where customers are** — in **M365 Copilot and Teams** — via the publishing experience and the new agent identity types. **All code is on GitHub** (linked in the deck and the breakout-session repo). They plug the **Agent League hackathon** (running **until the 14th**, with prizes; join via a QR code), point to **other Foundry/agent sessions**, and invite attendees to the **Foundry agents booth** (Sean has **stickers**).

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — Microsoft's AI platform for using models and building AI apps, agents; the host/runtime/management plane throughout the talk.
- **Foundry Hosted Agents** — Foundry's agent hosting with a **built-in sandbox**; keeps the sandbox file system ~30 days after inactivity; Foundry **session ID** controls the agent's file system/VM.
- **Foundry models** — the thousands/hundreds of models usable with agents (intelligence layer).
- **Foundry prompt agents** — simple, **declaratively built** agents created in the Foundry portal.
- **Routines (preview)** — schedule/stimulus-driven triggers that prompt an agent into a session; can spin an idle sandbox back up; **agents can create their own routines** (e.g. nightly self-maintenance/backup).
- **Hermes** — a **claw-like** autonomous agent harness (memory, sandbox/VM ownership, tools, autonomy, self-improvement); **not** an OpenClaw fork; deployed here onto Foundry Hosted Agents.
- **OpenClaw** — the agent that popularised the local, credential-using, messaging-driven, always-running **"claw" architecture**.
- **nano-claw** — mentioned as one of the many "literal claw" flavours.
- **OpenShell** — referenced (not used in the demo) as an optional component depending on your deployment.
- **Work IQ** — Microsoft tool/MCP surface giving agents access to **SharePoint / org data** (used for the SharePoint document retrieval).
- **Microsoft Agent Framework** — Python + .NET SDK for AI apps/agents; **v1.0**; three parts: agent loop, workflows, harnesses; `.AsAgentHarness()` to add a harness to any agent.
- **Harness Console** — a TUI from Agent Framework to run/prototype/iterate on harness agents with event listeners.
- **AG-UI** — open standard for UI that talks to agents; exposes an AG-UI endpoint on your agent.
- **CopilotKit** — UI library that talks to AG-UI; provides built-in controls incl. **auto-generated charts** with no extra code.
- **Magentic** — multi-agent **planning/supervisor** workflow pattern built with **Microsoft Research**.
- **A2A (agent-to-agent) protocol** — open protocol to connect agents across the ecosystem.
- **MCP (Model Context Protocol)** — tool/connector protocol (used for Work IQ SharePoint, general tools).
- **OpenAPI** — alternative way to expose tools to agents.
- **OpenTelemetry / GenAI semantic spec** — full telemetry emitted by harness agents, sendable to Foundry or anywhere.
- **Foundry Toolkit Agent Inspector** — tool to connect to, view responses/events for, and **debug** agents.
- **Agent host builder / responses endpoint** — Agent Framework mechanism to expose/deploy an agent (e.g. a responses-style endpoint) and into Foundry.
- **Teams & M365 Copilot** — collaboration surfaces; Foundry **one-click publish** delivers both UIs out of the box.
- **Microsoft admin center** — where org-wide agent publishing is **approved** (Requests tab to approve/"hire" the agent).
- **Entra (agent identity / Default Credential)** — every agent has an Entra agent identity; demo authenticated via **Azure Default Credential / Entra credentials**.
- **Blob storage** — target for Hermes' nightly independent backups.
- **Azure Functions / Azure Container Apps** — additional deploy targets for Agent Framework agents.
- **Scout** — an out-of-the-box example of an **autopilot agent** in Foundry.
- **Assistive / Autonomous / Autopilot agents** — Foundry's three agent identity types (see Detailed Notes).
- **Ecosystem connectors named:** GitHub Copilot, Claude Code, Cursor, Copilot Studio, GitHub Copilot CLI, OpenAI, Anthropic, Gemini, Amazon Bedrock, Ollama (local models), AWS (as a deploy target).

## 🚀 Announcements / What's New
- **Routines in Foundry — in preview.** Stimulus/schedule-driven triggers for agents; agents can create their own; used for self-maintenance, skill curation, and backups. *(Explicitly called "new… in preview.")*
- **Autopilot agents — new third agent identity type** that acts on its own behalf **with a real user account** (own email alias, can send Teams messages and create Word documents on its own behalf). Demoed in snippet form in the **Build 2026 keynote** the day before. *(New; preview status not explicitly stated.)*
- **Workstream Manager sample** — a hero, group-chat autopilot-agent code sample (auto-tracks open items, answers team-chat questions, onboarding + access control, selective group-chat replies). Available in the breakout-session repo.
- **Microsoft Agent Framework v1.0** — Agent Framework (released to **preview last October**) reached **version 1.0** "a couple months ago," now including the **agent harness** capability (`.AsAgentHarness()`, built-in tools + compaction, planning, middleware). The two minimal-harness setup lines will become **optional after preview**.
- **One-click publish to Teams + M365 Copilot** from Foundry (both UIs out of the box, self-scope or org-wide via admin center). *(Presented as available/current capability.)*
- **Hermes on Foundry Hosted Agents** — Glenn's working **proof-of-concept** integration (with code available; he's submitting **PRs into the Hermes repo** to improve Foundry support). *(POC, not GA.)*
- **Agent League hackathon** — running **until the 14th**, with prizes; join via QR code. *(Event, not a product.)*

## 💡 Demos
- **Hermes on Foundry (Glenn):** A local **Hermes TUI** connecting over a network **proxy** to a **Hermes agent on Foundry Hosted Agents**, authenticating via Azure Default Credential/Entra and pulling a **Foundry model**. Showed the agent attempting **SharePoint retrieval via a Work IQ MCP** (failed on conference Wi-Fi, recovered after respawning a fresh instance, then correctly identified the doc's author as **Jeff Holland**). Showed **Routines** in the portal: an **auto-created nightly maintenance routine** (prunes stale skills, backs up to blob storage) and how the **session ID** swaps the entire file system/VM from a snapshot. **Point proved:** you can run a pet-like, self-improving claw-style agent on Foundry **without paying for an always-on sandbox**, *if* you deliberately externalise/back up its unique state.
- **Custom harness with Agent Framework (Sean):** In **C#**, added a harness to a chat client with **`.AsAgentHarness()`** (file/code/shell tools + compaction for free), then a **customised research agent** (web→markdown tool, reasoning effort, file/memory stores, full OTel telemetry, background web-search agent). Ran it in the **Harness Console**, prompting *"write a blog about Microsoft Agent Framework announcements at Build 2026"*; it entered **plan mode**, loaded a prebuilt **blog-outlining skill**, built a **to-do list**, hit a **human-in-the-loop** question (audience chose "developers building AI agents"), produced a plan, and on **approve/execute** wrote the blog. **Point proved:** harness behaviours (planning, skills, tools, human-in-the-loop, long-running background work) are available out of the box and easy to customise.
- **AG-UI + CopilotKit web UI (Sean):** Enabled an **AG-UI endpoint** on an agent in a couple of lines; ran a **sales-CSV agent** in a CopilotKit web UI showing live tool calls and **auto-generated charts with no extra code**. **Point proved:** the same harness agent can ship a polished customer-facing web UI trivially. Then **deployed the agent into Foundry** (responses endpoint, traces, Agent Inspector). **Point proved:** one agent → workflow / console / web UI / Foundry deployment.
- **Teams & M365 Copilot publishing (Amanda):** **One-click publish** of a **Zava** support prompt agent to Teams + Copilot (self-scope vs. admin-center org approval), then used it in **M365 Copilot**. **Point proved:** both UIs out of the box, no extra build.
- **Workstream Manager group-chat autopilot agent (Amanda):** Onboarding message granting chat access to named teammates; demonstrated **access control** (Burke denied), the **"working on a response" signal**, **@-mention reciprocity**, and **selective (not every-message) responses** in group chats. **Point proved:** autopilot agents can behave like a well-mannered group-chat participant with creator-controlled access.

## 📊 Notable Stats / Quotes
- *"If you think of your agent as the motor, as the engine… then the harness is the car… a motor by itself is not very useful."* — Sean's defining analogy for an agent harness.
- Claws are *"the most pet-like thing we perhaps have invented since the beginning of cloud computing"* — Glenn, on pets-vs-cattle.
- *"I always had this Hermes there doing whatever I wanted, but I wasn't paying for it all the time."* — Glenn's design goal (shut-down-when-idle).
- Hermes idles down after **~15 minutes** of inactivity; **Routines** spin it back up for maintenance.
- Foundry Hosted Agents retain the sandbox file system for **~30 days** of inactivity (then deleted; otherwise kept indefinitely while in use).
- **Microsoft Agent Framework:** preview **last October** → **v1.0** ~a couple months ago; **full feature parity between .NET and Python**.
- Foundry offers **thousands… hundreds of models** for agents.
- **Three** ways to consume a harness agent (workflow / console / web UI) and **three** agent identity types (assistive / autonomous / autopilot).
- **Agent League hackathon** runs **until the 14th** with prizes.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Stand up **Microsoft Agent Framework v1.0** (C# or Python), add a harness with `.AsAgentHarness()`, and run the **Harness Console** locally; then expose it via **AG-UI + CopilotKit** and deploy to **Foundry**.
- [ ] Things to try: Deploy a **claw-style agent (Hermes)** onto **Foundry Hosted Agents** and replicate Glenn's **idle-shutdown + Routines self-maintenance/backup** pattern; grab his POC code at the booth/repo.
- [ ] Things to try: Build an **Autopilot agent** from the **Workstream Manager** sample and test the **group-chat access control + selective-reply** behaviours; compare against **Scout**.
- [ ] Things to try: Use the **Foundry Toolkit Agent Inspector** to debug responses/traces on a deployed agent.
- [ ] Questions: What is the **GA / pricing** model for **Foundry Routines** and **Autopilot agents** (esp. the per-autopilot **user account** cost/licensing)? Are autopilot user accounts standard Entra/M365 licences?
- [ ] Questions: How does **session-ID-controlled file system isolation** interact with multi-user/team agents — collisions, sharing, RBAC on the sandbox FS?
- [ ] Questions: For idle-shutdown agents, what's the **cold-start latency** when a Routine (or a user message) wakes the sandbox?
- [ ] Questions: Find the **GitHub repo** link from the deck / breakout-session resources for all three demos' code.
- [ ] Relevant to: Anyone building **enterprise agent harnesses** on Azure/Foundry; teams evaluating **OpenClaw-style** patterns for production; **agentic ops/automation** projects; my own OpenClaw setup (Routines ≈ cron/heartbeat self-maintenance parallels).

## 🔗 Related
- Build 2026 Foundry overview (Tina & Jeff's prior-day session — referenced repeatedly)
- [[Build2026]] session notes index
- Microsoft Agent Framework docs / GitHub (workflows, Magentic, harnesses)
- OpenClaw / Hermes agent-harness patterns
- AG-UI + CopilotKit (agent web UI standard)
- Foundry: Routines, Autopilot agents, Scout, Work IQ

---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/teams
  - topic/agents
  - topic/m365
  - topic/copilot
source: https://www.youtube.com/watch?v=vaerCmx8754
session_code: DEM332
event: Microsoft Build 2026
speakers: Umang (Senior PM, Teams Platform); Amir (Senior Software Engineer, Teams SDK)
duration_min: 20
aliases:
  - 'From zero to teammate in 25 minutes: Build a Teams agent live'
---

# DEM332 — From zero to teammate in 25 minutes: Build a Teams agent live

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Umang — Senior Product Manager, Teams Platform; Amir — Senior Software Engineer, Teams SDK  
> **Duration:** ~20 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=vaerCmx8754)

## 🎯 TL;DR
A fast, demo-driven walkthrough of how Microsoft has collapsed the painful multi-step journey of getting an AI agent into Microsoft Teams down to minutes. The team introduces the new **Teams SDK** (a consolidation of last year's Teams AI Library plus tooling), a brand-new **Teams CLI** built "agent-first" for both humans and coding agents, and a **Teams dev agent skill** that lets Copilot scaffold and integrate an agent end-to-end. They take an existing standalone web app ("project management helper") and, live on stage with Copilot in YOLO mode, register it, integrate the Teams packages, and install it into Teams (1:1 and group chat) — then show how **Agent 365 (A365)** turns that agent into a true *teammate* with its own identity, email, and presence across the M365 ecosystem (Teams, Outlook, Word, Excel, PowerPoint).

## 🔑 Key Takeaways
- The headline promise: go **from zero to a working Teams "teammate" in under 25 minutes**, live and from scratch.
- **Teams SDK** is this year's evolution — a *consolidation* of all the libraries and tools developers were juggling into one streamlined developer experience (last year shipped the Teams AI Library in TypeScript and C#).
- The traditional path to a Teams agent is long and high-friction: register app → get credentials → set an endpoint → upload a manifest → configure environment → start the bot — spanning multiple concepts and surfaces. The whole session is about killing that friction.
- Three guiding pillars: **(1) any agent, any stack** onto Teams (Foundry, Vercel, CrewAI, Replit — they're unopinionated about where your agent lives); **(2) frictionless scaffolding** to cut developer cognitive overhead; **(3) make the agent a true teammate** with its own identity, closing the agentic loop.
- The new **Teams CLI** is designed for *both humans and agents* — interactive arrow-key menus for humans, and machine-friendly behaviour for coding agents.
- A single command — **`teams app create`** — provisions an **Entra application**, a **bot**, **secrets**, glues them together, and returns an **installation link** at the end.
- For agents, the CLI uses **progressive disclosure**: subcommands are revealed step-by-step (`teams -h` → `teams app -h` → `teams app update`) so the agent only loads the context it needs for its current goal, not every subcommand at once.
- The CLI has a **`--json` mode**: same data as the pretty human output but as structured JSON, so agents can pipe it into more complex scripts without parsing prose.
- A **Teams dev agent skill** equips Copilot with two abilities: it can **drive the Teams CLI** and it can **read the Teams docs** — so a one-line prompt ("Integrate this application into Microsoft Teams… give me the installation link") does the whole integration.
- Once installed, the **exact same feature set from the web app works inside Teams** — 1:1 chat and group chat — with no rewrite.
- New **group UX capabilities** for agents are coming: **emoji reactions**, **targeted/private messages & slash commands**, **quoted replies**, **suggested actions**, **markdown support**, and **source citations** (deep-dive in a dedicated group-chat session the next day).
- **Agent 365 (A365)** is "M365 for agents" — it gives an agent an **agentic identity** so it can live across Teams, Outlook, Word, PowerPoint, Excel, etc., carrying project context everywhere.
- A single built agent becomes a **blueprint**: you can spin up many scoped personas (e.g. a PM for the "mobile redesign" project vs. the "back-end architecture" project), each with its **own alias and email**, each knowing only its own project's context.
- A teammate agent can **send email from its own address**, be **@mentioned in group chats and meetings**, and be referenced in **Word comments** — and its contact card identifies it as an **AI agent**.
- IT benefits too: A365 gives **visibility, observability, permissions, and control** over what each agent is doing and the impact it has.
- Teams reach is the draw for partners: **320 million daily active users**; named partners building on the Teams SDK include **Cursor, Linear, Perplexity, Datadog, and Atlassian**.
- Try it: **aka.ms/teams-sdk** (SDK + new CLI + skills).

## 📚 Detailed Notes

### Framing: the agenda and the "25 minutes" challenge
Umang (Senior PM on the Teams platform) opens by asking how many in the room have built an agent on Teams. The framing is that anyone who *has* knows how many steps and concepts it takes; anyone who *hasn't* is "in for a feast." The stated goal: build an agent **from zero to teammate in under 25 minutes**, live. Amir (Senior Software Engineer on the Teams SDK) is the live-demo driver. The agenda:
1. Recap of the Teams SDK (where they left things at last year's Build).
2. Introduce a **brand-new CLI** and a set of **skills** with a working agent.
3. Build that agent using the skills + CLI together.
4. Take the agent into a **group chat**.
5. Transform the agent into a **teammate** with its own identity.

### Recap — from Teams AI Library to the Teams SDK
Last year at Build they shipped the **Teams AI Library** in **TypeScript and C#**. This year they're shipping the **Teams SDK** — explicitly described as a **consolidation of all the libraries and tools** developers were using into **one streamlined developer experience**.

Last year also delivered **one-on-one agentic features**: streaming in a chat, feedback loop, follow-up, citations, and starter prompts. This year the focus expands to **group UX features** to make an agent "shine within a group" (with a dedicated follow-up session the next day).

They're also **integrating with other SDKs across the Microsoft ecosystem**. Over the past year they partnered with **Cursor, Linear, Perplexity, Datadog, and Atlassian**, all building on the Teams SDK to tap the **320 million daily active users** on Teams.

### The friction problem
Working with those partners revealed that the path to a *successful* agent on Teams is long. The traditional sequence:
- Register your app
- Get it credentials
- Set an endpoint
- Upload a manifest
- Configure the environment
- Start the bot

That journey spans multiple scenarios, multiple concepts, and multiple surfaces. The team's goal: **get your agent into Teams as quickly as possible.**

### The three pillars
1. **Any agent, any stack onto Teams.** Whether the agent lives in **Foundry, Vercel, CrewAI, or Replit**, Microsoft is "unopinionated" about where the agent runs — they just want to make bringing it to Teams easy.
2. **Frictionless scaffolding.** Developers burn a lot of cognitive overhead getting an agent onto Teams; the SDK/CLI/skill combo is meant to minimise that and make success seamless.
3. **Make the agent a true teammate** — with its own identity — which "closes the agentic loop."

### The starting point — a standalone web app
Amir takes over and shares his screen. He has an agent he's been building "on the side": a **project management helper**, a plain **web application**. The left pane lists his projects; the main view runs the agent and answers questions like:
- "Summarize the status of all my projects" → returns statuses for all projects.
- "How is the conference demo project going?" → returns the status of one specific project.

This works, but only as a web app — the goal is to bring it into Teams.

### Step 1 — Register the agent with `teams app create`
Amir switches to the terminal and uses the **Teams CLI**:
- Command: **`teams app create`**
- Prompts encountered: a **name** (he enters "project management agent"), a **messaging endpoint URL** (skipped for now), **where to store credentials** (he chooses the **`.env` file**), and **optional customizations** (skipped). Then **create**.
- What the command does under the hood (as Umang previewed): creates an **Entra application**, creates a **bot**, creates **secrets**, and **glues all those pieces together**.
- Output at the end: an **installation link** (usable to install the app into Teams), plus the created app, the **bot ID**, etc.

That's the first half of the journey (provisioning). The second half is the **actual integration** into the existing app.

### Step 2 — Integrate via Copilot + the Teams dev agent skill
Traditionally, integration means: download the Teams SDK packages, read the docs, understand how the packages work, then wire them into your existing app. Instead, Amir uses **Copilot in YOLO mode** ("Hopefully demo gods agree with me"). This Copilot session has been **scaffolded with the Teams dev agent skill**.

His prompt is deliberately simple: **"Integrate this application into Microsoft Teams. Once you're done, give me the installation link."**

Copilot immediately picks up the **Teams dev agent skill**. The skill can do **two things**:
1. **Talk to the Teams CLI.**
2. **Read the Teams docs.**

While Copilot works in the background, Amir gives a tour of the CLI.

### The Teams CLI — built ground-up for humans *and* agents
**For humans — interactivity.** Traditional CLIs force you to construct long commands, supply arguments, and sometimes call other commands just to fetch IDs/arguments. The new CLI is **interactable**: type `teams app`, then use **arrow keys** to select. Demo flow:
- `teams app` → choose **create app** / select the existing **Project Management Helper** app.
- Available actions surfaced: **get app details, update app, download the package** (to share with colleagues), **manage secrets, manage permissions** — "most of the things you'd need to manage your app."
- He picks **update app → update basic information → change the description** to "Use this to manage your projects" (jokes about a typo) — modifying the app interactively with no long command string.

**For agents — progressive disclosure.** When designing for agents they used **progressive disclosure**:
- `teams -h` (help) shows only the **top-level commands**: e.g. **`teams app`** (manage your application), **`teams project`** (create/configure new projects).
- Instead of dumping *all* subcommands at once, the CLI reveals commands **progressively based on the agent's goal**. Example: to update a field, the agent reasons "this is part of managing," runs **`teams app -h`**, sees it needs update, runs **`teams app update`**, and only *then* is given the **full list of flags** for that command.
- **Why it matters:** the agent only fills its context with what it actually needs for the current goal — not "useless things it might not end up using." This keeps the agent's context window lean.

**JSON mode.** The other agent-friendly feature:
- `teams app list` → get the ID of the app just created.
- `teams app get <id>` → a **nice-looking, grokkable, legible** human output (details + installation link).
- Add **`--json`** → the **same output as structured JSON**.
- **Why it's powerful:** agents don't need pretty output; JSON lets them use these commands inside **more complex scripts** and pull values out **without parsing prose**.

Amir notes there's much more to the CLI and encourages trying it.

### Step 3 — Back to the running agent: installed in Teams
Returning to the Copilot session: it "did a lot of stuff," has an **endpoint running**, **edited the app**, and finally produced an **installation link**. Amir:
- Copies the installation link.
- Opens **Teams on the web** → is presented with a clean **installation modal** → clicks **Add**.
- Runs the same query as the web app: **"Summarize the status of all my projects."** The agent responds — **the exact same feature from the web application is now live in Teams.**

### Step 4 — Same agent in a group chat
Using the same installation link again, Amir introduces the agent into a **group chat** ("project discussions" group chat). He messages the agent: **"What's the status of my conference demo project?"** — and the agent responds, now available in the group. He hands back to Umang.

### Sneak peek — new group-chat capabilities for agents
Umang stresses the significance of a CLI that is **agent-first** in a world of coding agents. He previews the group-chat features (full deep-dive in tomorrow's session):
- **Emoji reactions** — the agent can respond with emojis.
- **Targeted messages & slash commands** — the agent can **privately message you** in a group chat, and you can **privately message the agent** (e.g. to "ask all the embarrassing questions").
- **Quoted replies** — the agent can **quote a past message**; important for **long-running tasks** in group chats that have a "fire hose" of messages.
- Plus **suggested actions, markdown support, source citations**, and other capabilities carried over/extended from last year's Build.

### From agent to teammate — Agent 365 (A365)
Umang reframes "teammate": his project management agent becomes a teammate when it can be, say, the **project manager for a mobile redesign project** that **lives across his M365 ecosystem**. Concretely, a true teammate means you can:
- **Send an email** to that project manager.
- **@mention / tag** it in a group chat.
- Add a **Word comment** and **@mention** it there.

So it's embodied **everywhere you work — in Teams and beyond.**

The enabling layer: just as there's **M365 for humans**, there's **A365 / Agent 365 for agents**. A365 lets you take your agent and:
- Make it a **teammate** with an **agentic identity**.
- Have it **live across the tools and apps** where you work.

In return, **IT gets more visibility, observability, permissions, and control** to understand the agent's impact.

### Blueprints — one agent, many scoped personas
The agent you build becomes a **blueprint** to spin up many project managers / personas, each **specific to one project** (e.g. mobile redesign vs. back-end architecture). Each persona **carries context** across **Word, Outlook, PowerPoint, Excel, and Teams**.

### Teammate demo (pre-recorded video, for time)
Amir notes this segment is a **video** (in the interest of time). It uses the *same* project management agent built earlier with Copilot:
- In Teams, the agent is used as a **blueprint to create more project managers** — here, a PM for the **mobile redesign** project.
- The new PM gets its **own identity**: its **own alias** and **own email**.
- Because it has an identity, you can **message it directly (1:1)**. Amir asks **"What's the current status of the project?"** *without specifying which project* — and because this PM is responsible for exactly one project, it knows that's the only thing in its context and responds with the **mobile redesign** status.
- The agent can be **included in relevant contexts** — **meetings** discussing the project, and **group chats**. Just like adding a user, you add the agent to a group chat; messaged there, it knows it's ready to help with the mobile redesign project.
- Because these agents have access to the **wide range of M365 tools** *and* their own identity, they can **send emails from their own accounts**. Amir asks it to send an email summary of the project; in **Outlook**, the email **arrives from the mobile redesign project manager**. Hovering the agent's **contact card** shows it's identified as an **AI agent** — powered by the **same Copilot/agent built moments earlier**.

### Closing
Umang reiterates the punchline: **from within Teams, you asked an agentic teammate to send an email from its own address to you — without ever leaving Teams.** "Your work starts to really get done in Teams." Reminders: a **dedicated group-chat session tomorrow**, and a call to **try the SDK and new CLI** at **aka.ms/teams-sdk**.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Teams SDK** — this year's consolidation of the Teams libraries/tools into one streamlined developer experience; the foundation for building Teams agents.
- **Teams AI Library** — last year's release (TypeScript and C#) that the Teams SDK now consolidates/supersedes.
- **Teams CLI** — the new command-line tool built ground-up for both humans (interactive arrow-key menus) and agents (progressive disclosure + JSON mode). Key commands: `teams app create`, `teams app list`, `teams app get <id>`, `teams app update`, `teams project`, `teams -h`.
- **`--json` mode** — CLI flag returning structured JSON instead of human-formatted output, for scripting/agent consumption.
- **Progressive disclosure (CLI design)** — reveals subcommands step-by-step so agents only load context relevant to the current goal.
- **Teams dev agent skill** — a skill that scaffolds Copilot to (1) drive the Teams CLI and (2) read the Teams docs, enabling one-prompt integration.
- **GitHub Copilot (YOLO mode)** — used live to integrate the web app into Teams from a single natural-language prompt.
- **Microsoft Entra** — identity platform; `teams app create` provisions an **Entra application** for the agent.
- **Bot (Teams)** — the messaging endpoint/bot resource created and wired up by the CLI.
- **`.env` file / secrets** — where the CLI stores the agent's credentials/secrets.
- **Agent 365 (A365)** — "M365 for agents"; provides agentic identity and presence across the M365 ecosystem, plus IT visibility/observability/permissions/control.
- **Microsoft 365 (M365) apps** — Outlook, Word, PowerPoint, Excel, Teams — the surfaces a teammate agent lives across.
- **Group chat agent capabilities** — emoji reactions, targeted/private messages, slash commands, quoted replies, suggested actions, markdown support, source citations.
- **One-on-one agentic features (recap)** — streaming in chat, feedback loop, follow-up, citations, starter prompts.
- **Partner/host platforms (agent stacks)** — Foundry, Vercel, CrewAI, Replit (named as valid places an agent can live before being brought to Teams).
- **Ecosystem partners on Teams SDK** — Cursor, Linear, Perplexity, Datadog, Atlassian.
- **aka.ms/teams-sdk** — landing page for the SDK, new CLI, and skills.

## 🚀 Announcements / What's New
- **Teams SDK** — new this year; consolidates the prior Teams AI Library and assorted tools into a single streamlined developer experience. (Status not explicitly stated as GA vs preview in the talk; presented as available to try via aka.ms/teams-sdk.)
- **New Teams CLI** — brand-new, agent-first command-line tool with interactive mode, progressive disclosure, and `--json` mode. Presented as available to try (status GA/preview not explicitly stated).
- **Teams dev agent skill** — new skill enabling Copilot to drive the Teams CLI and read Teams docs for one-prompt integration. (Status not explicitly stated.)
- **New group-chat agent capabilities (coming)** — emoji reactions, targeted/private messages & slash commands, quoted replies, suggested actions, markdown support, source citations. Explicitly previewed as upcoming, with a dedicated deep-dive session the following day; treat as **announced/forthcoming** rather than confirmed-GA.
- **Agent 365 (A365)** — positioned as the mechanism to give agents an agentic identity and turn them into teammates across M365, with IT controls. (Referenced as the enabling product; specific availability status not detailed in this session.)
- *Note:* The session did not give explicit GA dates or preview tiers for these items; statuses above reflect exactly what was (and wasn't) stated.

## 💡 Demos
- **Live: `teams app create`** — registered the agent, provisioning an Entra app, a bot, and secrets, and returning an installation link + bot ID. Proved one command replaces the multi-step register→credentials→endpoint→manifest dance.
- **Live: Copilot (YOLO) + Teams dev agent skill integration** — a single prompt ("Integrate this application into Microsoft Teams… give me the installation link") drove Copilot to use the skill, run the CLI, stand up an endpoint, edit the app, and return an install link. Proved the "frictionless scaffolding" pillar — no manual package wiring.
- **Live: CLI tour** — interactive arrow-key navigation (`teams app` → update description), progressive disclosure (`teams -h` → `teams app -h` → `teams app update`), and `teams app get <id> --json`. Proved the CLI is genuinely dual-purpose for humans and agents.
- **Live: agent running in Teams (1:1)** — installed via the generated link, then "Summarize the status of all my projects" returned the same result as the original web app. Proved feature parity with zero rewrite.
- **Live: agent in a group chat** — same install link added the agent to a "project discussions" group chat; it answered "What's the status of my conference demo project?". Proved group availability.
- **Video (for time): agent → teammate via A365** — used the built agent as a **blueprint** to create a mobile-redesign PM with its own alias/email; answered an ambiguous "what's the current status of the project?" correctly from its scoped context; was added to a group chat/meeting; and **sent an email from its own address** that arrived in Outlook with an **AI-agent contact card**. Proved the full teammate experience and that the email-sending teammate is powered by the same Copilot-built agent.

## 📊 Notable Stats / Quotes
- **320 million daily active users** on Teams — the reach partners build for.
- **"From zero to a teammate in under 25 minutes"** — the session's framing challenge ("you can start your timers").
- **Named partners on the Teams SDK:** Cursor, Linear, Perplexity, Datadog, Atlassian.
- **Two things the Teams dev agent skill can do:** talk to the Teams CLI, and read the Teams docs.
- **"A CLI that is built for coding agents is what we're bringing to you."** — Umang, on the agent-first design.
- **"What you just saw is within Teams, you were able to ask an agentic teammate to send an email using its own email address to you… without you having to leave Teams."** — Umang, the closing punchline.
- Traditional Teams-agent journey enumerated as **6 steps**: register app → credentials → endpoint → manifest → configure environment → start bot.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install the new Teams CLI and run `teams app create` end-to-end on a throwaway app; inspect what gets provisioned in **Entra** + the **bot** + `.env` secrets.
  - Wire up the **Teams dev agent skill** in Copilot and reproduce the one-prompt "Integrate this application into Microsoft Teams" flow on an existing web app.
  - Compare `teams app get <id>` human output vs `--json` and script something that pulls the installation link/bot ID out of JSON.
  - Explore **progressive disclosure** (`teams -h` → `teams app -h` → `teams app update`) and note how it keeps an agent's context lean.
  - Bring an agent hosted elsewhere (Foundry / Vercel / CrewAI / Replit) into Teams to test the "any stack" pillar.
  - Try the group-chat features once available: emoji reactions, slash commands, private/targeted messages, quoted replies.
- [ ] Questions:
  - What's the **GA vs preview** status (and licensing) of the Teams SDK, the new CLI, the dev agent skill, and **Agent 365**? Not stated in-session.
  - How does **A365 agent identity** map to Entra — is each teammate a distinct service/agent identity, and how are its email + permissions governed by IT?
  - What are the cost implications of spinning up many scoped "blueprint" personas (one per project)?
  - How is per-agent **observability/permissions/control** surfaced to IT admins?
  - Does the integration require a specific app framework, or is it truly stack-agnostic at the code level?
- [ ] Relevant to:
  - Building internal Microsoft Teams agents/bots and migrating existing web-app assistants into Teams.
  - Agent identity / governance discussions (Agent 365, Entra agent identities).
  - Designing **agent-first CLIs** (progressive disclosure + JSON mode) for our own tooling.
  - Copilot-driven scaffolding / "skills" patterns for developer workflows.

## 🔗 Related
- [[Microsoft Teams SDK]]
- [[Teams AI Library]]
- [[Agent 365]]
- [[Microsoft Entra]]
- [[GitHub Copilot]]
- [[Microsoft 365 Agents SDK]]
- Source list: [[2026 Build Session List]]
---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/github
  - topic/fabric
source: https://www.youtube.com/watch?v=gJX6MOyef8Q
session_code: SEG04
event: Microsoft Build 2026
speakers: Microsoft (product segment — GitHub Copilot keynote demo)
duration_min: 6
aliases:
  - GitHub App + Rayfin
---

# SEG04 — GitHub App + Rayfin

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Microsoft product segment (GitHub Copilot keynote demo; presenter name not stated in transcript — follows Satya Nadella, hands back to Satya)  
> **Duration:** ~6 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=gJX6MOyef8Q)

## 🎯 TL;DR
This keynote segment introduces the **new GitHub Copilot desktop app** — a "home base for development and operations" that runs multiple agentic coding sessions in parallel using **Git worktrees** for isolation, plus **agent merge** to babysit PRs through CI, review, and conflicts. It showcases multi-model access via one Copilot subscription (OpenAI, Anthropic, Google) and a "rubber duck review" where one model cross-checks another's work. Two new interaction concepts are demoed: **Canvas** (an agent builds a custom UI on the fly — including a camera/computer-vision PR-approval widget) and **pick and polish** (point at any UI element and tell the agent to change it). The grand finale: an agent-built, containerized app gets deployed to enterprise-grade **Microsoft Fabric** infrastructure with a single `rayfin up` command via **Rayfin**.

## 🔑 Key Takeaways
- The **GitHub Copilot app** is positioned as your **home base** for both development *and* operations on your own machine.
- **Parallel agentic sessions**: kick off one session *per issue* with no stashing/conflict worries — handled by **Git worktrees** (isolated environments per session).
- **Agent merge** continuously shepherds a PR through **CI checks, code review, and merge conflicts** — agents don't just write code, they finish it.
- **Single Copilot subscription = all top models** (OpenAI, Anthropic, Google) in one **model picker**; pick the right model per task.
- **Rubber duck review**: for bigger features, one model (e.g. GPT‑5.5) can request a review from another (e.g. **Claude Opus 4.8**) — multi-model catches blind spots earlier.
- **Canvas**: agents can build a **custom UI** to communicate with you — going beyond chat (incl. live camera / computer-vision approval).
- **Pick and polish**: select any element in the app, add it to chat, and ask the agent to modify it ("add reordering to this list") — and it just works.
- **Add a session from any repo** (local *or* GitHub) with **no clone, no pull** — "it just works."
- **Rayfin** = deploy your agent-built, containerized apps to **enterprise back ends on Microsoft Fabric** with `rayfin up`, "deploy with confidence."
- Core thesis: this is **not just a session manager** — session managers make it easy to *create* work; **GitHub Copilot helps you finish it**.

## 📚 Detailed Notes

### Framing — "What can I try on my laptop today?"
The presenter opens to a developer audience late in a busy keynote day ("drinking from the fire hose"), urging everyone to watch with the mindset of *what can I try out on my laptop later today?* Satya had teased **Rayfin** (rendered "Raven" in auto-captions); the presenter pivots to start with the **new GitHub Copilot app** first.

### The GitHub Copilot app — home base
- The app is your **home base for development and operations** on your computer.
- **Home screen**: kick off a new **agentic coding session** from the start.
- Playful touch: you can drag **Mona** (the GitHub mascot/octocat) around the home screen — there's a little **game** built in.

### Parallel sessions via Git worktrees
- A session started earlier produced a **review of release blockers**; the presenter picks the **critical ones (H3)** then decides to **do all of them**.
- The app **spins up a separate session for every single issue** — no stashing, no coding conflicts.
- This is powered by **Git worktrees**: *isolated environments for each session*, so agents work **in parallel without stepping on each other**.

### Agent merge
- Parallel work still has to be **merged**. On a chosen issue, the presenter runs **`agent merge`**.
- Once enabled, **Copilot continuously "babysits" the PR** through **CI checks, code review, and merge conflicts** — automating the path to merge.

### Work, Automations, and Sessions views
- **Work** view: a focused view of all activity + loaded projects — **issues and PRs**, everything in one place.
- **Automations**: a set of **reusable sessions and workflows** that can run **locally or in the cloud** (jokingly references "issue poetry" that is "real and load-bearing").
- **Sessions**: add a new repository via a button — pull from a **local repo or a GitHub repository**. Demo adds a session in an open-source repo ("Pocket Cow"): **start a session anywhere, it just loads** — *no clone, no pull*.

### Inside a session — integrated workspace
- Opening a session gives an **integrated browser**, a **terminal**, and the **chat**, all loading together.
- Can **toggle light/dark mode** within the session.
- **Pick and polish** button: click it, then **pick any element** in the app — it's added to chat. Ask e.g. *"add reordering to this list"* and the change *just works*, all living inside the session.

### Multi-model + Rubber duck review
- **All the most popular models** are available via a **single GitHub Copilot subscription**, including **OpenAI, Anthropic, and Google** — visible in the **model picker**.
- Beyond picking the right model per task, for **bigger features Copilot can request a "rubber duck review."**
- Example: a session running on **GPT‑5.5** automatically requested a review from **Claude Opus 4.8**. Rationale: *all models have blind spots*; the **multi-model approach catches them earlier**.

### Beyond chat — the Canvas concept
- "Working with AI in 2026 should be **more than just chat**." Enter the **Canvas**: *how an agent can build a custom UI to communicate with you.*
- Demo ("What if your AI could **see**?"): with the camera on, the agent renders a canvas showing your **PRs**, which you **approve/reject with a thumbs up / thumbs down** gesture (computer vision). The presenter approves a PR live.
- Framed as *just the beginning* of what custom agent-built UIs can do.

### The finale — deploy to enterprise with Rayfin
- The presenter returns to the parallel sessions kicked off earlier, highlighting a **"signal box" app** that is **100% agent-built**, **containerized with a database back end**.
- Rhetorical question: *would you deploy this to your enterprise with no questions asked?* Audience: **No.** Answer: not on your own — **but you can with Rayfin.**
- In a new terminal, the presenter types **`rayfin up`** and the app **deploys**, **hosted on Microsoft Fabric**.
- With **Rayfin**, *your agents get an enterprise back end*, so you can **deploy with confidence** in the way that's best for you.

### Closing thesis
- The key message: this app is **not just another session manager**. It *does* manage many sessions, but **session managers just make it easy to create work** — whereas **GitHub Copilot helps you to finish it.** Sign-off: "Happy Pride. Back to you, Satya."

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot app** — new desktop "home base" app for development + operations; runs agentic coding sessions locally.
- **Agentic coding sessions** — agent-driven work sessions you launch from the app (one per issue if desired).
- **Git worktrees** — isolated per-session environments enabling parallel agents without conflicts.
- **Agent merge** — Copilot continuously manages a PR through CI checks, code review, and merge conflicts.
- **Work / Automations / Sessions views** — focused activity view; reusable local/cloud workflows; repo session management.
- **Pick and polish** — select any UI element, add it to chat, and have the agent modify it.
- **Model picker / multi-model access** — all popular models (OpenAI, Anthropic, Google) via one Copilot subscription.
- **Rubber duck review** — one model requests a review from another model to catch blind spots (e.g. GPT‑5.5 → Claude Opus 4.8).
- **Canvas** — agent-built custom UI for richer-than-chat interaction (incl. live camera / computer-vision PR approval).
- **Rayfin** — framework/CLI (`rayfin up`) to deploy agent-built, containerized apps onto enterprise back ends. *(Microsoft Fabric data-apps framework/SDK; auto-captions garble it as "Raven"/"Rayfen".)*
- **Microsoft Fabric** — the enterprise hosting platform Rayfin deploys onto.
- **Mona (octocat mascot)** — draggable on the home screen with a built-in mini-game.

## 🚀 Announcements / What's New
- **New GitHub Copilot desktop app** — introduced as the developer "home base" (development + operations). *Status: shown in keynote demo; GA/preview status not explicitly stated in transcript.*
- **Agent merge** — continuous, automated PR shepherding (CI, review, conflicts). *Status: demoed.*
- **Canvas** — agent-built custom UIs beyond chat, incl. camera/computer-vision interaction. *Status: demoed as "just the beginning."*
- **Pick and polish** — direct-manipulation UI editing via the agent. *Status: demoed.*
- **Rubber duck review** — cross-model review (GPT‑5.5 ↔ Claude Opus 4.8). *Status: demoed.*
- **Rayfin** — one-command (`rayfin up`) enterprise deployment of agent-built apps to Microsoft Fabric. *Status: demoed live ("Blammo!"). Specific GA/preview timing not stated in transcript.*

## 💡 Demos
- **Release-blocker triage → parallel sessions** — kicking off a session per issue (worktrees) → proves agents can run in parallel with no conflicts.
- **Agent merge on a PR** — proves Copilot can drive a PR to merge through CI/review/conflicts unattended.
- **Add a session from an open-source repo ("Pocket Cow")** — proves zero clone/pull friction.
- **Pick and polish ("add reordering to this list")** — proves direct, in-app, agent-driven UI edits.
- **Rubber duck review (GPT‑5.5 requesting Claude Opus 4.8)** — proves multi-model blind-spot catching.
- **Canvas + camera PR approval** — proves agents can build custom UIs and use computer vision (thumbs up/down to approve a PR).
- **`rayfin up` deploy of an agent-built signal-box app to Fabric** — proves enterprise-ready deployment of agent-built containerized apps.

## 📊 Notable Stats / Quotes
- *"Git worktrees are isolated environments for each session that you run, so your agents can work in parallel without stepping on each other."*
- *"All models have blind spots and the power of the Copilot multi-model approach means that I can catch them earlier."*
- *"The canvas is how an agent can build a custom UI to communicate with you."*
- *"Would you be able to deploy this to your enterprise with no questions asked? … No, but you can with Rayfin."*
- *"With Rayfin, your agents get an enterprise back end. So you can deploy with confidence in the way that's best for you."*
- *"Session managers just make it easy to create work. But GitHub Copilot helps you to finish it."*
- "**100% agent built**" — the signal-box demo app (containerized, with a database back end).

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Install the new **GitHub Copilot app**; kick off **multiple sessions across issues** and confirm **worktree** isolation; enable **agent merge** on a low-risk PR; experiment with **pick and polish** and **Canvas**.
- [ ] Things to try: Stand up a small containerized app and run **`rayfin up`** to test Microsoft Fabric deployment end-to-end.
- [ ] Questions: Is the GitHub Copilot app **GA or preview**, and which OSes? Does **agent merge** require specific branch-protection/CI configs? What are **Rayfin**'s prerequisites (Fabric capacity, networking, cost model, supported runtimes)?
- [ ] Questions: How does **rubber duck review** pick the reviewing model, and is the model list configurable/governable for enterprise?
- [ ] Relevant to: Platform/DevEx teams evaluating agentic dev workflows; data-app teams adopting **Rayfin + Fabric**; anyone running parallel Copilot agents at scale.

## 🔗 Related
- [[BRK225 - Data apps and agents the future of app dev with Rayfin]]
- [[2026 Build Session List]]

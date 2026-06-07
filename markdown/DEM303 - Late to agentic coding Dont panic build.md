---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/agentic-coding
  - topic/copilot
  - topic/ai
  - topic/productivity
source: https://www.youtube.com/watch?v=6F7HgRhWL9E
session_code: DEM303
event: Microsoft Build 2026
speakers: Martin Woodward, Cassidy Williams (GitHub)
duration_min: 26
aliases:
  - Late to agentic coding Dont panic build
---

# DEM303 — Late to agentic coding? Don't panic, build.

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Martin Woodward (GitHub) & Cassidy Williams (GitHub)  
> **Duration:** ~26 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=6F7HgRhWL9E)

## 🎯 TL;DR
A fast-paced, highly interactive live-build session where Martin Woodward and Cassidy Williams from GitHub reassure the audience that, despite the "everyone's already doing it" hype on social media, **they are actually early adopters of agentic coding** — and have a real opportunity to shape how these tools and practices evolve. The pair demonstrate the new **GitHub Copilot app** (built on top of the Copilot CLI/SDK), running multiple agentic coding sessions in parallel from crowd-sourced GitHub issues. Core themes: **choice matters** (models, interface, editor, workflow), **don't blindly YOLO in the enterprise** (use plan mode and Copilot instructions to enforce quality), **let Copilot check its own work with a different model** ("rubber duck") for statistically significant improvements, and **auto mode** for cost-aware model routing. The session closes with practical CLI commands (`remote`, `chronicle`, cost tips) and the message: you're not late — just give it a go.

## 🔑 Key Takeaways
- **You are NOT late to agentic coding.** On the Moore's innovation-adoption curve, Build attendees sit in the **early adopters / early majority** band. The loud "you're behind" voices on Twitter are a tiny innovator fringe, not the norm — most colleagues back at the office haven't started yet.
- **The data backs "early":** A recent Microsoft study found **~84% of developers** use AI nearly daily, yet **~84% of people outside the tech industry have *never* touched it.** The world has yet to catch up, so practitioners now can genuinely *shape* practices and tooling.
- **Copilot is GitHub's own #1, #2, and #3 contributor** to the GitHub codebase. A provocative question to the audience: if Copilot *isn't* your top contributor at work, why not? It can work 24/7 — what's blocking broader team adoption?
- **Choice is foundational** — not just model choice, but choice of *interface* (CLI, web, IDE, app), *editor*, and *workflow*. Different people on the adoption curve have very different needs; enterprises must offer choice or adoption stalls.
- **Don't run YOLO/Autopilot mode in the enterprise.** Live "just say go" demos are fun, but in real organizations you should use **plan mode** and guardrails so quality stays high across *all* developers, not just the experienced ones.
- **Copilot instructions are how you constrain and steer Copilot.** Check them into the repo to encode coding standards, layout, and build expectations — this is how less-experienced teammates produce decent-quality code. Copilot can auto-generate these from an existing project.
- **The "rubber duck" pattern works:** having Copilot vet its own plan/work with a *different model family* (e.g. GPT checked by Claude/Gemini) yields a **statistically significant improvement every single time.**
- **Auto mode does cost-aware model routing.** It intelligently picks the right model for the context, preventing the classic mistake of burning expensive premium-request budget (e.g. Opus 4.8) on a trivially simple question.
- **The new GitHub Copilot app** is built directly on the **Copilot CLI/SDK** — the *same engine* on your machine — and is **deeply integrated with GitHub** (it auto-detected an issue template and applied it; it live-pulls new issues without refreshing).
- **Work happens in isolated git work trees**, so multiple parallel agent sessions don't step on each other.
- **AI removes the "learn from failure" loop.** Teams must consciously create ways to keep learning from each other and bring up less-experienced people who don't yet know how to "hold it correctly."
- **Writing code has never been faster, but emitting code isn't the goal.** Huge volumes get generated and dumped in open-source repos but never merged/committed. The challenge: build code that *lasts* and avoid becoming "slop factories."
- **Experienced devs get the most leverage** — "Copilot is rocket fuel to experienced devs" — because they know which frameworks to pick and can give the agent constraints. Devs still must steer, set constraints, and own architecture.
- **Practical homework: check out Spec Kit** — agent-native documentation via markdown files/instructions that tell agents how to work with your repos.

## 📚 Detailed Notes

### Format & Setup: A Live, Interactive Build
The session is deliberately interactive. The speakers — fresh off working on the keynote all day — wanted to actually *build live* rather than just present. They ask the audience to scan a QR code (or visit `gh.io/dem303/idea`) and **log in with GitHub on their phones** to submit build ideas. Martin jokes the login requirement is itself "the first test of the day" and conveniently boosts his sign-in numbers. The plan: collect ideas → kick off builds → talk → build more → talk.

### Audience Show-of-Hands (Adoption Snapshot)
The room is polled on how they use Copilot:
- **Currently using GitHub Copilot:** nearly everyone (relief/laughter).
- **Agent mode in VS Code:** the majority.
- **Visual Studio:** some.
- **Command line (CLI):** some.
- **The new GitHub app** (announced that day, "very new"): just **one person**.
- **Web / coding agent** (`github.com/copilot`): a couple.
- **Built-in code review on github.com:** a handful.

This snapshot frames the whole talk: even this advanced audience has barely touched the newest surfaces — reinforcing the "you're early" thesis.

### The GitHub Copilot App — What It Is
Martin demos the **GitHub Copilot app** (switching to light mode for visibility). Cassidy explains the architecture: **the app is built on top of the GitHub Copilot CLI**, using all the same SDKs — so it's the *exact same engine* running on your machine that powers every session. You kick off a "session" to do agentic work.

Key capabilities surfaced during the demo:
- **Voice-to-text input** via **Cmd+H (macOS) / Win+H (Windows)** — the speakers repeatedly (and comically) forget to use it.
- **Typo tolerance** — "It understands your typos."
- **Deep GitHub integration:** when asked to "create some issues for ideas on what to build," the app **auto-detected a checked-in issue template / coding standards** and prefixed each new issue with `idea:` per the repo's idea form. Martin notes he didn't know it would do that — a genuine "pretty awesome" moment.
- **Live data:** new issues submitted by the audience appear in the app **without any refresh.**

### Crowd-Sourced Build Ideas
The audience (and the agent) generate issues. Shouted-out / submitted ideas include:
- Whiskey / IPA **review app** (it's 5pm, end of day).
- **Face-controlled Breakout** game.
- **Gesture-controlled ping pong.**
- **Gesture rock-paper-scissors.**
- **Side-scrolling platformer game.**
- "Build a better MS Build app."

These become the live-build fodder for the rest of the session, run in parallel.

### The Core Argument: You're Early, Not Late
Martin and Cassidy deliver the session's thesis between builds:

**The hype is misleading.** Agentic coding growth is massive — pull requests from agents are "going through the roof." Martin, who lived through dot-com, says the last time he saw anything approaching this pace was the dot-com boom — but *that* played out over a year or two, whereas this feels like it happened **within the last 6 months.** It's "a brand new epoch" in how software is built.

**Where you actually sit on the curve.** Using the classic **Moore's innovation-adoption curve**, the "blah blah blah" people on Twitter making you feel behind are the tiny **innovator** fringe. Build attendees are squarely in **early adopters**, crossing into **early majority**. The colleagues back at the office are way over on the other side — they haven't started.

**Different cohorts have different needs.** Innovators/early adopters will *completely change how they work* to suit a new tool — they want the latest and coolest. That will **not** happen in the broader organization. If someone there can only work in, say, "a random version of Eclipse," and it can't talk to Copilot, they'll never adopt Copilot. People are attached to their existing tools — which is exactly **why choice across the company is so important.**

**The 84%/84% study.** Cassidy cites a recent Microsoft study: **~84% of developers** use AI nearly daily — *wild* — but the same study, viewed across the *whole world outside tech*, shows **~84% of people have never touched it.** So even casual dabblers at Build are not just early — they're positioned to **"be the change you want to see"** and shape practices, because so much of the world has yet to catch up.

### Quality, Craft & Learning in the Agentic Era
Several connected cautions:
- **Speed ≠ value.** Writing/emitting code has never been faster, but mass volumes pour into open-source repos and **often never get merged or committed.** The real question: *how do we build code that's going to last* and avoid becoming **"slop factories"**?
- **Guardrails for everyone.** Copilot is "rocket fuel to experienced devs," but organizations must build the **safeguards, skills, and instructions** so that *everybody* — not just senior devs — produces decent-quality code.
- **The lost failure-learning loop.** Cassidy's standout point: a disadvantage of AI is **you don't get to learn from failure the way you once did.** Teams must deliberately create ways to keep communicating and learning from each other — learning the tools the *right* way — and **bring up less-experienced people** who don't yet know "how to hold it correctly."
- **Humans still steer.** Martin's self-deprecating framing: Cassidy is "an actually good developer" who knows which frameworks to pick, so she can give the agent constraints and get what she wants. Someone who "just plays a developer on TV" can make bad architecture choices. **Developers still have to be in control, steer, set constraints, and point it the right way.**

### Demo: "Plan Mode" vs "Autopilot/YOLO"
Cassidy walks through the **reasoning/mode controls** in the app:
- **Reasoning level** is adjustable (low → high). Lower reasoning is cheaper/faster for simpler tasks.
- **Model selection:** all major model providers are available; you can **bring your own key** or **bring in local models** (e.g. hosted on **Foundry**).
- **Interactive mode** = step-by-step collaboration.
- **Plan mode** = produce a plan first (it nearly renders a Mermaid-style diagram).
- **Autopilot** = "just go do it." The CLI slash command is **`/yolo`** (or `allow all`) — it runs to a finished product so you can come back later.

For the **gesture rock-paper-scissors** issue (issue #19), they "come up with a plan," see the proposed **tech stack (MediaPipe Hands for gesture recognition)**, then drop it into **autopilot ("just say go")** as a *demo*. **Crucial caveat:** in the enterprise, "we very, very rarely stick it in YOLO mode… we do not say go typically at work." Plan mode + guardrails are the responsible default.

### Deep Dive: How to Use Plan Mode Well
Cassidy's personal workflow when starting a project or feature:
- Use **plan mode** in an existing repo, **or** start in a **"quick chat"** — a session *not attached to a repo* where you can ask any side question (even "what's the weather in Chicago," depending on which MCP servers you've pulled in), add MCP servers/skills, and go.
- For a second parallel build (**side-scrolling platformer, issue #17**), she asks for a step-by-step plan, picks **GPT-5.5**, starts with **low reasoning**, and notes you can also use **auto mode**.
- **Keep prompting / interrogating the plan.** Some models rush to "here's your plan, done." Cassidy deliberately goes **back and forth to find holes.** She steers the stack ("Don't worry about the stack," then later "I want to do this with **Phaser**").
- **Interrupt freely** — it's a collaboration tool; you don't have to wait for it to finish a thought. You can edit the plan inline in chat or **open it in a side markdown editor.**

### Deep Dive: The "Rubber Duck" Pattern
A highlighted technique: **rubber duck** vets the plan using a **different model family** than the one you're working in. While using GPT-5.5, the rubber duck might run **Claude (e.g. Opus 4.8) or Gemini** to **find holes in the plan**, refine it, and potentially ask you more questions. You can run it automatically on different runs or manually ("just start the rubber duck"). The payoff per the speakers: **having Copilot check its own work with a different model gives a better result *every single time* — a statistically significant improvement.**

### Deep Dive: Auto Mode & Cost/Token Management
Martin raises the universal pain: asking a "really dumb question" while accidentally in **Opus 4.6 / 4.8**, burning ~**54 or 100 premium requests** (the day's quota number) on something trivial — when a cheaper/faster model would've cost "0.1." **Auto mode handles your model routing automatically**, picking the right model for the right use case. As models proliferate with different costs, **auto mode becomes increasingly important.**

### Parallel Execution & Work Trees
Multiple agent sessions run **side by side** because **everything happens in git work trees** — so concurrent tasks **won't step on each other.** You can ask the agent to do anything (open a browser, spin up a web server) or do it yourself in a terminal.

### Tip: Playwright MCP for Visual Vetting
Cassidy shares a colleague's favorite workflow: use the **Playwright MCP server** (kept always-on at the *user level*) to **screenshot websites and vet designs visually.** Examples: feed in a URL and ask "How would you describe this design?", or "take the styles from the Microsoft Build website and apply it to my project." It opens the browser, takes the screenshot, and does everything the MCP server can — **just from a command.**

### The Rock-Paper-Scissors Payoff
The gesture RPS app actually builds and runs. There's a humorous live moment where it "froze your face," the game seems to win every time ("It's too good… I feel like that's cheating"), and then finally works correctly. It demonstrates the end-to-end loop: issue → plan → build → run → review, all from the app.

### Web Delegation: @Copilot and Assign-to-Copilot
For "build a better MS Build app," Martin shows **using Copilot through the web**: you can **`@Copilot`** in a conversation or **assign an issue to Copilot** (you don't even need a prompt — "just hit assign") and it joins the conversation to do the work. This is how you **delegate activity** to the coding agent on the web.

### Closing CLI Tips & Commands
Before wrap-up, several practical pointers:
- **Copilot instructions are critical.** When you start the CLI and it can't find Copilot instructions, it "tells you off" — that's how important they are. They tell Copilot about your project: coding standards, how to build, how things are laid out. Copilot is **amazing at analyzing an existing project and generating a Copilot-instructions file** for you. **Create them and check them in** to constrain code and onboard less-experienced teammates.
- **Spec Kit (homework):** an agent-native way to add markdown files / instructions telling agents how to work with your repos — "documentation that's agent native… a really great way of working."
- **`/remote` (remote on):** creates a **pipe back into your agent**, so you can kick off a long-running task on your local machine, **point your phone at it, walk away, and control it remotely** from your phone.
- **`/chronicle`:** a newly landed command with options like **stand-up** ("what did I do yesterday?") and **cost tips.** Cassidy loves **cost tips** — it analyzes your usage and advises which model to use more, when to switch modes, and **how to reduce context windows / be more efficient with tokens.**
- You can also just **click "Implement"** on a plan instead of typing a command.

### Closing Message
The speakers run out of time but stress they could "play with this all day." They invite the audience to the **Ask the Experts** area and the **Ship & Tell booth** ("we're here all week"). The core call to action: **just give it a go — try these tools, learn them, play with them, and use your time at Build to do it so you can ship it at home.** Cassidy closes warmly: they genuinely love teaching this, attendees are "at the forefront of so many new changes," and the team wants feedback to make the tools better.

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot** — core agentic coding assistant; GitHub's #1–3 codebase contributor.
- **GitHub Copilot app** — new desktop app built on the Copilot CLI/SDK; deeply GitHub-integrated; light/dark mode; live issue sync.
- **GitHub Copilot CLI** — command-line agent; the engine underneath the app.
- **GitHub Copilot coding agent (web)** — `github.com/copilot`; `@Copilot` mentions and assign-to-Copilot delegation.
- **GitHub.com built-in code review.**
- **VS Code** & **Visual Studio** — Copilot agent mode surfaces.
- **Agent mode / Plan mode / Interactive mode / Autopilot (YOLO)** — execution modes.
- **Auto mode** — automatic cost-aware model routing.
- **Rubber duck** — cross-model self-review feature.
- **Quick chat** — repo-less session for side questions.
- **MCP servers** — incl. **Playwright MCP** for screenshots/visual design vetting.
- **Skills** — pluggable into sessions.
- **Models referenced:** GPT-5.5, Claude / Opus 4.6 & 4.8, Gemini; "high Q"; bring-your-own-key; local models.
- **Microsoft Foundry** — host for local/self-hosted models.
- **MediaPipe Hands** — gesture-recognition library used in the RPS build.
- **Phaser** — JS game framework chosen for the platformer.
- **Git work trees** — isolation for parallel agent sessions.
- **Spec Kit** — agent-native markdown documentation/instructions for repos.
- **Copilot instructions** — checked-in file to constrain/steer Copilot.
- **Voice-to-text** — Cmd+H / Win+H.
- **CLI commands:** `/yolo`, `allow all`, `/remote` (remote on), `/chronicle` (stand-up, cost tips).

## 🚀 Announcements / What's New
- **GitHub Copilot app** — described as "very new" / talked about that day at Build; only one audience member had used it. Built on the Copilot CLI/SDK with live GitHub integration.
- **`/chronicle` CLI command** — "a new command that just landed," offering stand-up summaries and **cost tips** (usage-based model/efficiency advice).
- **`/remote`** — pipe back into your agent to run long tasks locally and control them from your phone.
- *(Context: the broader keynote earlier that day covered agentic coding growth and agent-generated PR volume, referenced but not detailed here.)*

## 💡 Demos
1. **Auto-generating GitHub issues from voice/text** — the Copilot app created idea issues and auto-applied the repo's `idea:` issue template / coding standards.
2. **Gesture Rock-Paper-Scissors (issue #19)** — planned (tech stack: MediaPipe Hands), dropped into autopilot, built, run live; comedic "it wins every time / froze your face" moments before working correctly.
3. **Side-scrolling platformer (issue #17)** — built in **plan mode** with GPT-5.5 + low reasoning; stack steered toward **Phaser**; **rubber duck** invoked to vet the plan with a different model family; live back-and-forth refinement.
4. **"Build a better MS Build app"** — delegated via web by **assigning the issue to Copilot** (no prompt needed) to research the current app and propose iOS/Android improvements.
5. **Parallel sessions in work trees** — multiple builds running side by side without collision; agent asked to open a browser / start a web server.
6. **`/remote`** — demonstrated piping the agent back to a phone for remote control.
7. **`/chronicle` → cost tips** — usage-based efficiency/model recommendations.

## 📊 Notable Stats / Quotes
- **"Copilot is the number one, two, and three contributor to the GitHub codebase right now."** — Martin Woodward.
- **~84% of developers** use AI (nearly daily), yet **~84% of people outside tech have never touched it** (recent Microsoft study, via Cassidy).
- **"The last time I saw anything approaching this was during dot com… and this feels like it's happening within the last 6 months."** — Martin, on the pace of change.
- **"Copilot's rocket fuel to experienced devs."** — Martin.
- **"The disadvantage of AI is you don't get to learn from failure like you once did in the past."** — Cassidy.
- **"How do we make sure we don't become like slop factories?"** — Martin.
- **"Having Copilot check its own work with a different model… gives you a better result every single time"** — a **statistically significant improvement.**
- On wasted spend: asking a "really dumb question" in **Opus 4.6/4.8** can burn **~54–100 premium requests** when a cheaper model would cost **~0.1**.
- **"You're at Build for crying out loud — you are in the early adopters."** — Martin (paraphrased thesis).
- **"You can be the change you want to see in the world and shape the way these tools are going."** — Cassidy.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Try the **GitHub Copilot app** (CLI/SDK-based) and connect it to a real repo with a checked-in **issue template** to see auto-detection in action.
  - Author and commit a **Copilot instructions** file (let Copilot generate a draft from an existing project), then verify it constrains output for the team.
  - Experiment with the **rubber duck** cross-model review (e.g. GPT-5.5 vetted by Claude/Gemini) and measure quality delta on a real plan.
  - Switch to **auto mode** and watch model routing / token spend; run **`/chronicle` cost tips** to get efficiency advice.
  - Wire up **Playwright MCP** at the user level for screenshot-based design vetting ("describe this design" / "apply these styles").
  - Test **`/remote`** to drive a long-running local agent task from my phone.
  - Read up on **Spec Kit** and try agent-native markdown instructions on one of my repos.
  - Run a build entirely in **plan mode**, interrogating the plan for holes before letting it implement.
- [ ] Questions:
  - What's the exact source/date of the "84% of developers / 84% of non-tech" Microsoft study, and how is "using AI nearly daily" defined?
  - How does **auto mode** decide routing under the hood, and how aggressively does it down-route to save premium requests?
  - What's the current premium-request quota referenced ("54 or 100… today") and how does it map to my plan?
  - Which model families can the **rubber duck** use, and can I pin a specific reviewer model?
  - Is the **GitHub Copilot app** generally available, and on which platforms (macOS/Windows/Linux)?
  - How do **work trees** surface in the app UI for managing many parallel sessions?
- [ ] Relevant to:
  - Driving broader **team adoption** of Copilot (the "why isn't Copilot your #1 contributor?" challenge).
  - Establishing **enterprise guardrails**: checked-in Copilot instructions + plan mode over YOLO.
  - **Cost/token governance** as model choice proliferates (auto mode, `/chronicle` cost tips).
  - Onboarding **less-experienced developers** without losing the failure-learning loop.
  - Standardizing **agent-native docs** (Spec Kit) across our repositories.

## 🔗 Related
- [[Microsoft Build 2026]]
- [[GitHub Copilot]]
- [[Agentic Coding]]
- [[GitHub Copilot CLI]]
- [[Spec Kit]]
- [[Model Context Protocol (MCP)]]
- [[Copilot instructions]]

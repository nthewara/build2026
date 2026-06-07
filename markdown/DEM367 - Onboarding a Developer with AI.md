---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/developer-productivity
  - topic/github-copilot
  - topic/onboarding
source: https://www.youtube.com/watch?v=kppO36BR6pg
session_code: DEM367
event: Microsoft Build 2026
speakers: Michel Hubert (Avanade, Microsoft MVP)
duration_min: 24
aliases:
  - Onboarding a Developer with AI
---

# DEM367 — Onboarding a Developer with AI: A Better First-Day Experience

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speaker:** Michel Hubert — Avanade (France), Microsoft MVP (17 years)  
> **Duration:** ~24 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=kppO36BR6pg)

## 🎯 TL;DR
A demo-driven talk reframing developer onboarding as a **developer-experience problem** that AI agents (GitHub Copilot with `@workspace` context) can dramatically compress. Through a fictional new hire "Sarah" on her first day in an unfamiliar 2,000+ file, multi-language codebase, Michel walks four "acts": (1) **understand the codebase** — get a mental map in minutes, (2) **surface hidden context** — the *why* behind decisions that never made it into the docs, (3) **identify what & who matters** — critical files and the right people to ask, and (4) **ship the first PR** — a real contribution that follows team conventions on day one. The central thesis: **use AI as a context engine, not a code generator** — in onboarding, the value is understanding what already exists. The codebase itself becomes the living documentation, and the agent reads what is *actually* there (commits, PRs, issues) rather than stale docs.

## 🔑 Key Takeaways
- Onboarding to a new codebase typically takes **3–9 months** to reach full productivity (autonomy, not just first commit) — this is a developer-experience problem, not an HR one.
- An AI agent can replace what would normally be a **2-hour whiteboard session with a tech lead**, delivering an architectural tour, entry points, and data flow in ~2–3 minutes.
- **`@workspace` gives Copilot the actual code in context** — it reads imports, recent commits, and infers module boundaries from how code actually connects, rather than just listing folders.
- The agent can **generate architecture/class diagrams directly from the code** even when none exist in the documentation, by analyzing relationships and dependencies.
- Agents distinguish **active code vs. legacy/dead code** by analyzing recent commit activity per folder — invaluable for knowing where to focus.
- Pulling **PR descriptions, commit messages, and issue threads** lets the agent reconstruct the *full history and motivation* of a module — including major refactors and migration milestones — not just the latest version.
- The agent surfaces **unwritten conventions** (logging, error handling, naming) from the real active code (e.g. "use `structlog`, not the stdlib `logging`") rather than from docs.
- It can identify **the five most important files to read first** and the **top contributors/owners** of a module (from PR/commit history) so a newcomer knows who to ask.
- For the first PR: the agent reads a real issue, proposes a **plan first** (without writing code), then on approval **implements the fix, runs tests, debugs, and drafts a convention-matching PR description**.
- **Traceability matters:** record which model/agent made a change (e.g. "Copilot + Claude Sonnet 4.6") in the PR so production issues can be traced back.
- **Three principles:** AI is a context engine not a code generator; the codebase *is* the documentation (invest in readable code + good comments, maintain fewer pages); senior time is the scarcest resource — every question AI answers keeps the team focused.
- **Actionable metric:** measure **time-to-first-PR** before vs. after AI. If you can't improve it, the problem is likely in your codebase's readability.

## 📚 Detailed Notes

### Framing: the moment a developer joins a team
The talk is *not* about HR onboarding or badge pickup. It's about the moment a developer opens a **repo they've never seen** and wonders where to start. Michel's question: how does that moment change when an **AI agent sits next to you**?

He introduces himself as Michel Hubert, working for **Avanade in France**, a **Microsoft MVP for 17 years**.

### Three numbers that set the scene
1. **3–9 months** — the average time for a developer to become *fully productive* (autonomous) in a new codebase. This is not "time to first commit," but time to genuinely operate independently.
2. **40%** — how much of **week one** is spent **reading** code, not writing it. This is normal and expected. The problem is that reading time is usually **solitary** and dependent on documentation quality — and documentation is generally **obsolete / not up to date**. That's the reality.
3. **One in three questions** — Michel's favorite. When you start on a new project, **one in three questions never gets asked out loud**: the new developer is afraid of looking dumb, the tech lead is in a meeting, or the question feels too basic.

His conclusion: these three numbers describe **developer experience**, not an HR problem — and that's what the session attacks.

### The four "acts" (the structure of the talk)
- **Act 1 — Understand the codebase:** get from zero to a mental map in minutes.
- **Act 2 — Surface the hidden context:** the decisions that shaped the code and never made it into the docs.
- **Act 3 — Identify what and who really matters:** critical components and the right people to talk to.
- **Act 4 — Ship the first contribution:** a real PR that follows the team's conventions on day one.

Note on format: Michel originally wanted all demos fully live, but **AI agents sometimes take minutes rather than seconds**, so he ran a **pseudo-live demo** (pre-captured) instead.

### Meet "Sarah" — the scenario
Sarah is a **fictional** new developer in a situation everyone has seen. Day one, new team, a repo she's never opened. The reality she faces:
- **Documentation last updated 14 months ago** — not up to date.
- **Tech lead is in meetings until 5:00 PM** — hard to get an architecture conversation.
- **2,000+ files** in the codebase — a real, substantial codebase.
- **5+ different languages:** Python, React, .NET, SQL, and more.
- A mix of **legacy and recent/active code**.
- An **implicit deadline:** first PR by end of week. Nobody states it, but everyone expects it.

**The actual codebase used:** the open-source **PostHog** project, chosen specifically because it has a **long history**. Michel stresses: *the more history a codebase has, the better the agent performs* (more commits/PRs/issues to learn from). He has no affiliation with PostHog — it was just a convenient real-world repo with depth.

### Act 1 — Understand the codebase (zero to mental map)
Sarah opens her agent and asks the most natural question: *"I just joined the team. Give me a tour. Give me the entry points. Explain the codebase — not just the technical part, but the functional part too."*

Key point: the agent **does not just list folders**. With **`@workspace`**, Copilot gets the actual code in context — **reading imports, recent commits, and inferring boundaries from how the code actually connects**.

What the agent returned (in ~2–3 minutes, replacing a 2-hour whiteboard session):
- Description of the **front end (React)** and its different **entry points**.
- Explanation of the **Node.js server** — its methods, modules, classes, and the files where each class lives.
- The **architecture and data flow** from front end to back end, with methods and classes.
- The **query path** back-to-front and the relevant **Kafka topics**.
- An analysis of **active code vs. older/legacy code** — which folders have been active in recent months vs. where the legacy code lives (code that may never be used but won't change for months).
- A **class diagram of the whole project** — *not in the documentation*, generated purely by analyzing the codebase, the classes, their relationships and dependencies. Zooming in showed a full diagram built from code alone. Michel calls this "very impressive."

### Act 2 — Surface the hidden context (the "why")
"Sarah has the map now, but a map doesn't tell you *why* the roads go that way." She needs context the documentation doesn't contain.

**Prompt 1 — Why does this file exist?** She asks the agent (with `@github`) to look at a specific file (`final.py` as spoken) and explain *why it exists* and *what problem it was built to solve*. The agent doesn't just read the code — it **pulls PR descriptions, commit messages, and issue threads** to understand the module's whole history, not just the last version. It returned:
- The **origin, motivation, and major refactors** of the module.
- The **core algorithm** for the module.
- The **full history from PRs and commits** — e.g. the project started in **2021**; initially used **ClickHouse Enterprise Edition**; phase two replaced it with the **open-source ClickHouse version**; a later step replaced **Postgres with ClickHouse** — each with the relevant PRs and a **timeline of milestones**.

**Prompt 2 — The Postgres → ClickHouse decision.** She asks the agent to find the **original decision** behind PostHog using **ClickHouse for analytics queries instead of Postgres**. The agent analyzed all ClickHouse-related decisions in the repo/PRs and laid out the phases:
- A **pre-existing POC** before 2020.
- **Phase 2:** a **pain point with Postgres** (performance issues on specific queries) drove the analysis of Postgres vs. ClickHouse.
- **Phase 3:** comparison of different candidate solutions to replace Postgres.
- **Phase 4:** the **migration** itself — moving from Postgres to ClickHouse — with the relevant issues/PRs.
- A **timeline**: POC → why ClickHouse was chosen → databases evaluated → the migration epic → the first implementation PR → when ClickHouse went to production. All reconstructed purely from the GitHub repository.

**Prompt 3 — Unwritten conventions.** She asks the agent to explain the codebase's conventions for **error handling, logging, and naming** — based on the **real active code, not the docs**. The agent returned which patterns to use, e.g.:
- For logging: **`import structlog`** instead of the stdlib `logging` — the convention actually implemented in the project.
- The team's **error-handling** convention, plus *how to implement logging* in her own code to match.

### Act 3 — Identify what & who really matters (prioritize)
Now Sarah understands the code and the context; she needs to prioritize.

**Prompt 1 — What to read first.** She asks: *"What are the five files I absolutely need to read first? What are the main parts of the code?"* The agent returned the **five important files** plus a **mental model** built from analyzing them.

**Prompt 2 — Who to ask.** She asks **who the main contributors are for the core module**, so she knows who to contact for a deeper discussion. Using **PR and commit history**, the agent can retrieve the **owner(s)** of a module so she knows who to ask.
- **Observed quirk:** sometimes the agent, instead of returning names directly, returned the **commands to execute** to find the top contributors. Michel notes this isn't a hallucination — just a "strange behavior." Sarah can run those commands herself if she wants the contributor list.

### Act 4 — Ship the first PR (the real contribution)
The end-to-end first-contribution flow: read an issue → plan the approach → implement following conventions → run tests → debug → draft the PR description. Michel used a **real PostHog issue (#58757)**.

Steps demonstrated:
1. **Explain the issue.** Give the agent the issue and ask what it is, what technical changes it implies, and which files to update. The agent read the issue and explained the problem and the files to modify, including what updates are needed to succeed.
2. **Plan first, don't code yet.** Before writing anything, ask the agent for an **approach / strategy / workflow** and to find the relevant files — *but explicitly not to update the code yet*. The agent analyzed the **root cause** and advised changing the **back end and database (adding a new column)**, provided the **serializer**, and laid out all the code to implement. This produces a reviewable plan.
3. **Implement the fix.** Once the plan looks right, ask the agent to **implement** it. The agent applied the updates (shown as the changed/added lines on the right of the editor).
4. **Run tests & self-debug.** Ask the agent to **run the tests to verify no regression**, and *if tests fail, debug and fix them*.
5. **Draft the PR description.** Ask the agent for the **team's PR convention/structure**. It analyzed the **most recent PRs** to learn the structure, then auto-generated the description — **title, problem statement, and the changes** made to fix the issue (back end and front end).
6. **Traceability.** The PR also records that it was **authored with an agent** — specifically **Copilot + Claude Sonnet 4.6**. Michel stresses this is *very important*: if a problem appears in production, you can trace which model/agent made the change.

### Three principles to take home
1. **AI as a context engine, not a code generator.** In onboarding, the value is *not* in writing code — it's in **understanding what already exists**. Don't judge an agent by how well it *writes*; judge it by **how well it explains**.
2. **The codebase is the documentation.** An agent reads **what is actually there**, not what we wish was there. This changes your relationship with documentation: **fewer pages to maintain, more investment in the codebase**. Make the code **readable** and add **good comments** so the agent can analyze context globally.
3. **Senior time is the scarcest resource.** Every question asked and answered by AI keeps the team focused. AI is **not a replacement for humans** — it's an **assistant / pair programmer** that helps you understand and resolve issues.

### Call to action & conclusion
- **"Try it on Monday."** Give your next hire an AI agent and **measure time-to-first-PR** — a very important metric. If you *can't* improve it, you likely have a **problem in your codebase**. Compare day-one-to-first-PR **before vs. after AI**.
- Closing maxim: *"Onboarding used to be a test of patience; with AI it can become a test of curiosity."*
- The whole onboarding reduces to **"one prompt, one plan, one PR — day one."** In reality not literally one day, but **a few days rather than a few months**, with a more productive new developer.
- Contact Michel via **LinkedIn**; no live Q&A in-session but he's available to meet during Build.

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot** — the AI coding agent used throughout as the "agent sitting next to you" for onboarding tasks.
- **`@workspace` (Copilot context)** — feeds Copilot the actual repo code, imports, and recent commits so it infers real module boundaries instead of just listing folders.
- **`@github` (Copilot context)** — pulls PR descriptions, commit messages, and issue threads to reconstruct module history and decisions.
- **Claude Sonnet 4.6** — the underlying model used (with Copilot) to author the demo PR; called out for traceability.
- **PostHog** — open-source product analytics project used as the demo codebase (chosen for its long, rich history). 2,000+ files, 5+ languages.
- **ClickHouse** — column-oriented analytics database PostHog migrated to (from Enterprise Edition → open source) for analytics queries.
- **PostgreSQL (Postgres)** — the original database PostHog used before migrating analytics to ClickHouse due to performance pain points.
- **Apache Kafka** — message/streaming layer; the agent surfaced the relevant Kafka topics in the data-flow analysis.
- **React** — front-end framework of the demo codebase.
- **Node.js** — back-end server in the demo codebase (methods/modules/classes mapped by the agent).
- **.NET** — one of the languages present in the multi-language codebase.
- **SQL** — used in the codebase (database layer).
- **Python** — primary language of much of the codebase (e.g. `structlog`/`logging` convention example, `final.py`).
- **structlog** — the structured-logging library that is the project's *actual* logging convention (vs. stdlib `logging`).

## 🚀 Announcements / What's New
None explicitly announced. This is a practitioner/demo session showcasing existing GitHub Copilot capabilities (`@workspace`, `@github`) applied to developer onboarding — no new product releases, previews, or GA announcements.

## 💡 Demos
A single continuous **pseudo-live (pre-captured) demo** of the four acts, all run against the open-source **PostHog** repo:
- **Act 1 — Codebase tour:** Proved an agent with `@workspace` can produce a full architectural map (entry points, front-end/back-end, data flow, Kafka topics, active-vs-legacy code, **and an auto-generated class diagram**) in ~2–3 minutes — replacing a 2-hour tech-lead whiteboard session.
- **Act 2 — Hidden context:** Proved the agent can reconstruct a module's *why* and full history (origin, motivation, refactors, the 2021→ ClickHouse migration timeline, the Postgres→ClickHouse decision rationale) and surface **unwritten conventions** (e.g. `structlog`) from PRs/commits/active code — none of it in the docs.
- **Act 3 — Prioritize:** Proved the agent can name the **top-5 files to read first** and identify **module owners/contributors** from PR/commit history (sometimes returning the *commands* to find them).
- **Act 4 — First PR:** Proved an end-to-end first contribution on a **real issue (#58757)** — explain issue → plan-only → implement fix → run/debug tests → draft a convention-matching PR description, with the agent/model (Copilot + Claude Sonnet 4.6) recorded for traceability.

## 📊 Notable Stats / Quotes
- **3–9 months** to become fully productive (autonomous) in a new codebase.
- **40%** of week one is spent reading code, not writing it.
- **1 in 3** questions a new developer has never gets asked out loud.
- Codebase scale: **2,000+ files**, **5+ languages**, docs **14 months stale**, tech lead unavailable until **5 PM**.
- Demo repo history starts in **2021**; real issue used: **#58757**; model: **Claude Sonnet 4.6** + Copilot.
- > "Don't judge an agent by how well it writes. Judge it by how well it explains."
- > "The codebase is the documentation. An agent reads what's actually there, not what we wish was there."
- > "Senior time is the scarcest resource."
- > "Onboarding used to be a test of patience; with AI it can become a test of curiosity."
- > "One prompt, one plan, one PR — day one."

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Point GitHub Copilot `@workspace` + `@github` at one of our larger legacy repos and run the four acts — especially the **auto-generated class diagram** and the **"why does this file exist?"** history reconstruction.
- [ ] Things to try: Establish a **time-to-first-PR** baseline for new hires, then re-measure after giving them an AI-agent onboarding flow.
- [ ] Things to try: Ask the agent to extract our **unwritten conventions** (logging/error handling/naming) from active code and compare against our written contributing guide.
- [ ] Questions: Does `@workspace` context scale cleanly to 2,000+ file / multi-language repos in practice, or does it need scoping? How fresh does the PR/commit index need to be?
- [ ] Questions: For the "plan first, then implement" flow — how reliably does the agent respect "don't change code yet," and how good is its self-debugging on failing tests?
- [ ] Relevant to: Avanade/internal developer onboarding, DevEx initiatives, reducing reliance on stale docs, codebase-readability standards (comments as agent context).

## 🔗 Related
- 

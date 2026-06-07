---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/testing
  - topic/agents
  - topic/code-validation
  - topic/ai
source: https://www.youtube.com/watch?v=NXodiipqNco
session_code: ODSP912
event: Microsoft Build 2026
speakers: Suresh Kesri (Developer Relations Manager, Testim AI)
duration_min: 13
aliases:
  - Build agentic testing systems to validate AI generated code
---

# ODSP912 — Build agentic testing systems to validate AI generated code

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Suresh Kesri — Developer Relations Manager, Testim AI  
> **Duration:** ~13 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=NXodiipqNco)

## 🎯 TL;DR
Agents can now write, run, break, and patch code — but they still can't *test* it in a way you'd trust before shipping to production. The hard part of the agentic era isn't build speed, it's **trust**: did the agent test the right thing, and can you believe it when it says "everything passed"? Testim AI's answer is **Keen CLI** (the "K and CLI" the captions garble), a new command-line **deterministic validation layer** that sits between development and shipping. You describe an end-to-end objective in plain natural language; Keen CLI opens a local (or cloud cross-browser) browser, completes the workflow with vision-based waiting, auto-discovers bugs, and emits trustworthy, shareable evidence (video, traces, agent-native ND-JSON) plus generated Playwright code. It works for humans at the CLI, as an importable SDK in CI/CD, and natively *inside* coding agents (Claude, Codex, Copilot, Gemini) via an `agent.md` file — giving those agents the "hands and eyes" to validate their own generated code.

## 🔑 Key Takeaways
- **The blind spot is validation, not generation.** "Everyone is focused on how fast we are building, but very few are asking the real question: how fast are we *validating*?" An agent can produce hundreds of lines of code in seconds — speed isn't the bottleneck, **trust** is.
- **The fix is a deterministic validation layer**, not just "more/smarter agents." You insert a reliable checking step between autonomous development and deployment so you can trust features built by one set of agents and deployed by another — without human intervention.
- **Keen CLI is intent-based.** You give a natural-language objective; there are **no brittle test scripts, locators, selectors, or XPaths**.
- **Vision-based waiting** replaces arbitrary `sleep`/time waits — it waits for the page/feature to actually render before acting, making runs resilient on complex, multi-step journeys.
- **Playwright code falls out for free.** Every natural-language run generates a Playwright test case you can keep, replay, and wire into CI/CD.
- **Auto-healing tests.** When the UI changes, Keen CLI automatically heals the affected test cases and returns updated test code.
- **Trustworthy, shareable evidence by default:** video logs, trace runs, and a shareable proof link per run — "shareable proof" you can review *before* merging a feature.
- **Bugs are surfaced automatically** during execution: if it hits a failure or finds a bug, it flags it to the user.
- **Three ways to consume it:** (1) the **CLI** directly, (2) an importable **SDK** (`import Keen`) for CI pipelines / custom agents / existing test suites, and (3) **agent-native** integration by pointing your coding agent at an `agent.md` file.
- **Agent-native output format:** results come back as structured **ND-JSON** that any agent can parse, plus an "agent rating" of the run.
- **Cross-browser / cross-device / cross-environment cloud validation** is an option on top of local-browser testing, so you can release with confidence beyond your own machine.
- **A Testim-style markdown test framework** stores written test cases as markdown that can be auto-played anytime or triggered from a CI/CD pipeline.

## 📚 Detailed Notes

### The problem: agents can build, but can't be trusted to test
The session opens by framing the current state of AI coding agents: they can **write code, run it, break it, and patch it**. The one thing they *haven't* genuinely been able to do is **test** it — at least not in the trustworthy way a careful engineer would before shipping to production. This is "the gap."

The core argument: an agent can generate hundreds of lines of code in seconds, **but the speed isn't the hard part — the trust is.** Two trust questions matter:
1. Did the agent test the *right* thing?
2. Can you actually rely on it when it reports that everything passed?

Suresh reframes the industry's obsession ("how fast are we building?") into the real, under-asked question: **"How fast are we validating?"** In a world where one set of autonomous agents develops a feature/page and *another* set deploys it, how do you trust — without human intervention — that the feature does what it's supposed to do? That is the exact blind spot the talk targets.

### The thesis: add a deterministic validation layer
The proposed fix is explicitly **not** "just add more intelligent / smarter systems." Instead, it's to insert a **deterministic validation layer between development and shipping.** Determinism is the point: the value of the layer is that its verdicts are reliable and repeatable, so a "passed" result actually means something. This is the conceptual heart of "agentic testing."

### Introducing Keen CLI
> Caption note: the transcript repeatedly renders this as "K and CLI" / "Keen CLI" / "key in CLI" / "KCLI." These are the same product — **Keen CLI** — Testim AI's newest product, launched (per the talk) to help ship end-to-end products in the agentic era.

Keen CLI is a **command-line validation layer** that lets you test any feature or application on a **local browser**. Key design properties:
- Usable **by humans** and **directly by agents**.
- **Natively integrates with all your agents** — examples given: Claude/Cloud, Codex, Gemini, Copilot.
- You **describe what you want in natural-language prompts**; Keen CLI opens a local browser and tests the feature.
- Optional **cloud validation** across **different browsers, devices, and environments** (cross-browser / cross-device / cross-environment).
- Goal: **release features and products with confidence.**

### What you get "out of the box"
The talk enumerates Keen CLI's built-in capabilities:

- **Intent-based control** — describe the objective in natural language. **No brittle test scripts, no locators, no selectors, no XPaths.**
- **Resilient runs** — stays on task even through complex, multi-step user journeys; **automatically discovers bugs** while executing and on failures.
- **Vision-based waiting** — waits on the *actually rendered* page/feature instead of inserting arbitrary time waits.
- **Playwright code generation (default)** — natural-language prompt in → Playwright test case out.
- **Testim-style (markdown) framework** — all written test cases are stored as markdown; you can **auto-play** them anytime and **trigger them from your CI/CD pipeline.**
- **Auto-heal** — on any UI change, Keen CLI heals the test cases and returns the new test code.
- **Shareable evidence** — **video logs** plus **trace runs** for each run.
- **Agent-native ND-JSON output** — structured output understandable by all agents.

### Three ways to use Keen CLI
1. **CLI directly** — run the provided command in your terminal, add a natural-language prompt, and Keen CLI starts automating it.
2. **SDK** — `import Keen` from the SDK; usable inside a **CI pipeline**, a **custom agent**, or an existing **test suite**.
3. **Agent-native** — point your coding agent at the Keen CLI **`agent.md`** file; the agent then "understands how to use Keen CLI effectively" while building applications. The mental model: the coding agent decides *what* end-to-end tests are needed for the feature it's building, and **Keen CLI gives it "hands and eyes"** to actually perform those end-to-end workflows.

### Getting started (install)
- **Download the NPM module** — copy the provided command, paste it into the terminal, let Keen CLI download.
- Once installed, open any terminal and **call Keen CLI** to start running test cases.
- It can be launched in an **interactive mode**, where the session initializes and prompts you to **paste your objective**; whatever objective you write, Keen CLI begins completing that workflow.

### How the agent-native flow works (conceptual)
While you build with **any** AI agent (Claude, Codex, Copilot, …), the agent defines the end-to-end test cases appropriate to the feature/product being developed, and Keen CLI executes them — acting as the agent's hands and eyes. **By default the agent-driven run executes in headless mode**, with results surfaced once the step completes. The run returns rich stats (pass/fail, objective completion) plus an **agent rating** and a **shareable proof** link.

## 🛠️ Products / Features / Technologies Mentioned
- **Keen CLI** — Testim AI's new command-line, deterministic end-to-end **validation layer** for the agentic era (the talk's central product; captions garble it as "K and CLI" / "KCLI" / "key in CLI").
- **Testim AI** — the company / partner presenting (ODSP = open-source/partner theater session at Build).
- **Keen SDK** — importable SDK (`import Keen`) for CI pipelines, custom agents, and test suites.
- **`agent.md` file** — the integration manifest you point a coding agent at so it learns to drive Keen CLI.
- **Playwright** — auto-generated test code output format.
- **ND-JSON** — agent-native structured output format for run results.
- **NPM** — distribution channel (install via the NPM module).
- **Coding agents referenced for integration:** Claude, OpenAI Codex, GitHub Copilot, Google Gemini.
- **Testim-style markdown test framework** — stores test cases as markdown; auto-playable and CI/CD-triggerable.
- **Cloud cross-browser / cross-device / cross-environment grid** — optional cloud validation tier.
- **Auto-heal engine** — repairs tests after UI changes.
- **Vision-based waiting** — render-aware waiting mechanism.

## 🚀 Announcements / What's New
- **Keen CLI is positioned as "the newest product launched by Testim AI."** The session functions as a launch/introduction of Keen CLI to help "ship end-to-end products in an agentic era." Treat this as the headline news of the talk: a brand-new, agent-native, deterministic end-to-end testing CLI from Testim AI, distributed via NPM and integrating with mainstream coding agents.

## 💡 Demos
The talk runs **two parallel demos** to contrast human-driven (GUI) and agent-driven (headless) usage:

**Demo A — Interactive CLI / GUI mode (multi-session checkout + clipboard-style hand-off):**
- Objective pasted in natural language: **complete a checkout flow** on a sample website, then **copy the resulting order ID** and **paste it into Google in a second session.**
- Keen CLI **bifurcates the objective into two workflows**: (1) complete checkout, (2) copy the order ID and paste it elsewhere.
- It **opens a local browser**, navigates the sample site, and reasons step-by-step; **every identified step is visible in the terminal.**
- It **auto-generates sample/test card data** to complete the card checkout, **places the order**, then **extracts and saves the order ID** from the confirmation (end of flow 1).
- Flow 2: it **opens google.com** and **pastes the saved order ID**, then **passes the test case** (workflow completed successfully).
- On **exit**, it **saves the session** to the chosen folder, **generates a Playwright script** of the completed test, and **produces a shareable link**. Opening that link shows **all step logs**, an **auto-play** replay (you can watch the cursor and the decisions it made), and it serves as **shareable proof** to validate before merging. Any bugs found are **automatically marked to the user.**

**Demo B — Agent-native mode (inside Claude, headless):**
- Paste the **`agent.md`** file to the agent so it understands how to use Keen CLI while building a feature.
- Invoke Keen CLI inside the agent by typing **`/`** then **"keen CLI"**; the session initializes within the agent environment, **identifies the user ID**, and is ready.
- The agent surfaces the **action types** Keen CLI can perform: **actions, assertions, extracting/top results, and running an existing test suite** in the project.
- Simple example objective: **"Go to testmu.ai and validate if the page opens."** (Caption renders it "testmu.ai.com"/"testmu.ai.com".) Keen CLI interacts directly with the AI agent, reasons about next steps, and — running in **headless mode by default** — returns stats: **test case passed, objective completed,** plus an **agent rating** and a **shareable proof** link to view in the browser.

## 📊 Notable Stats / Quotes
- *"Agents can write code now. They can also run it, break it and patch it. What they haven't really been able to do is test it — not in the way that you would trust before shipping an application to production. And that's the gap."*
- *"An agent can generate hundreds of [lines of] code in seconds, but the speed isn't the hard part. The hard part is trust."*
- *"Everyone is focused on how fast we are building, but very few are asking the real question: how fast are we validating?"*
- *"The fix is … to add a deterministic validation layer between shipping and development."*
- *"No brittle test scripts, no locators, no selectors, no XPaths."*
- *"Your agent can directly define what kind of end-to-end test cases it wants to write … and Keen CLI will provide them hands and eyes to perform those end-to-end workflows."*
- *Note:* No quantitative benchmarks (latency, accuracy %, coverage numbers) were given — the "stats" referenced in the demo are the per-run pass/fail status, objective-completion status, and an **agent rating**.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install Keen CLI from NPM and run it in interactive mode against a throwaway sample app (e.g. a checkout flow) to see the natural-language → Playwright output.
  - Wire the generated Playwright tests into a CI/CD pipeline and test the **auto-heal** behaviour by deliberately changing a UI element.
  - Drop the `agent.md` into a Claude/Copilot/Codex project and try the `/keen` (slash) invocation to validate an agent-built feature headlessly.
  - Inspect the **ND-JSON** output and the **shareable proof** link to evaluate how usable the "evidence" really is for PR review gates.
- [ ] Questions:
  - How "deterministic" is it really, given it's vision/LLM-driven under the hood? What makes a pass repeatable run-to-run?
  - Pricing/licensing, and what's local-free vs. cloud (cross-browser grid) paid?
  - How does it relate to legacy **Testim** (the established Tricentis-owned codeless testing product) — same lineage/branding?
  - Security model: it drives a real browser with credentials/test data — how is auth handled and isolated?
  - What's the exact product name spelling (Keen CLI vs. Kane CLI) and the real domain (`testmu.ai` vs `testim.ai`)? Verify before citing externally.
- [ ] Relevant to:
  - Anyone building **autonomous coding-agent pipelines** who needs a trustworthy validation gate before merge/deploy.
  - QA / SDET teams evaluating **AI-native, locator-free E2E testing** to replace brittle Selenium/Playwright selector suites.
  - Platform/DevEx teams designing **agent ↔ tool** integrations (`agent.md` pattern, ND-JSON, slash-command invocation).

## 🔗 Related
- [[Build2026]]
- [[Microsoft Build 2026]]
- Topics: [[Agentic Testing]] · [[AI Code Validation]] · [[Playwright]] · [[CI-CD]]

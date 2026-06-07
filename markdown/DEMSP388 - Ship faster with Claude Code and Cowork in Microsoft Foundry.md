---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/claude
  - topic/foundry
  - topic/coding-agents
source: https://www.youtube.com/watch?v=1NBzjJom-mI
session_code: DEMSP388
event: Microsoft Build 2026
speakers: Carolyn Matthews (Applied AI Architect, Anthropic)
duration_min: 21
aliases:
  - Ship faster with Claude Code and Cowork in Microsoft Foundry
---

# DEMSP388 — Ship faster with Claude Code and Cowork in Microsoft Foundry

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Carolyn Matthews — Applied AI Architect, Anthropic  
> **Duration:** ~21 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=1NBzjJom-mI)

## 🎯 TL;DR
Anthropic's Carolyn Matthews walks through how agentic coding has matured — from autocomplete to agents that write entire codebases — and why running Claude models on **Microsoft Foundry** gives you frontier intelligence plus enterprise governance, privacy, and compliance. She frames the talk around **four frontiers** of agentic coding (what agents can touch, how they know they're right, what they can perceive, and when/where they run) and demos each live. Key reveals include **Opus 4.8** (released the prior week, the most capable frontier model), **auto mode** (a safety classifier that replaces "dangerously skip permissions"), the **Oracle/evaluator** pattern for self-reviewing code, high-resolution image perception, and **dynamic workflows** for orchestrating sub-agents. The recurring theme: keep humans in the loop only for the high-value, high-risk decisions while agents safely run on their own for hours.

## 🔑 Key Takeaways
- Software development is shifting from writing/autocompleting code to **agents writing all the code for you** — and the pace is rapid (6 frontier model generations in 18 months).
- On the **SWE-bench Verified** coding benchmark, Anthropic models jumped from **49 → 87.6**, effectively saturating/"solving" coding by that metric.
- Agents can now run **autonomously for hours** — a cited benchmark hit **14.5 hours** of sustained accuracy, pointing toward hours-to-days of unattended agentic work.
- **Opus 4.8** (released ~1 week prior) is the new frontier model for hard, accuracy-critical, long-horizon problems; **Sonnet 4.6** is the recommended cost-effective starting point (great at coding); **Haiku** is the fast, low-latency model for summarization/classification at high volume.
- All three models share the **same prompting strategy, safety, and Constitutional AI guardrails** — you can freely redirect between them to manage cost.
- Running Claude on **Microsoft Foundry** combines frontier intelligence with built-in safety/governance, enterprise back-end privacy/compliance, and native Microsoft-stack integration — accelerating pilot-to-production.
- **Auto mode** (research preview) puts a **classifier between your request and the model**: it auto-approves low-risk actions (reading files, running tests) and only interrupts for risky/destructive ones — reported **0.4% false positive rate**. It replaces the unsafe "dangerously skip permissions" approach.
- The **Oracle / evaluator pattern** is central: use a *separate* judge agent (not the one that wrote the code) to adversarially review output. Architecture = **planner (decomposes) → generator (writes) → evaluator (judges)**.
- **Build the evaluator/tests FIRST** — investing time, effort, and research into a strong judge is the top priority before generating code, because it's what safely unlocks generating more code.
- Agents can now **perceive visually**: Claude in Chrome (real browser, not headless), computer use (drive the machine/iOS simulators), and **high-resolution image** support in Opus 4.8.
- High-res visual acuity is a big deal: a pen-testing example (Expo/"Expo") improved from **~58% (Opus 4.6) to ~98% (Opus 4.8)** success on agentic penetration testing.
- **Dynamic workflows** (new with Opus 4.8) provide a clean way to orchestrate sub-agents — demoed by spinning up multiple design agents + a "picker" judge + test agents to build an arcade game hands-off.
- Multi-surface, always-on operation: kick off on terminal, approve prompts on your phone, use **scheduled tasks/loops**, run agents in **parallel**, deep "Ultra Plan" planning, and even **voice** interaction.
- Guiding principle: **don't remove humans entirely** — keep them on the risky, high-value reviews while agents handle the rest safely.

## 📚 Detailed Notes

### How we got here — the trajectory of agentic coding
Carolyn opens by framing the industry shift: software development has moved from manually writing code (or relying on autocomplete) to **agents that write all of your code**. She presents it as "a history lesson" because things are moving so fast. Over the **last 18 months**, Anthropic has shipped **six generations** of frontier models. Measured on **SWE-bench Verified** — a coding benchmark built from ~500 real GitHub issues/requests, where the model must produce production-ready fixes — scores climbed from **49 to 87.6**. By this metric, coding is essentially "solved"/saturated.

Two other dimensions matter beyond raw accuracy:
- **Long-running autonomy:** one of the longest recorded sessions sustained good accuracy for **14.5 hours**. The point isn't the benchmark itself — it's that agents can run for **hours or even days**, not just the 5–30 minute sessions everyone is used to.
- **Tool use:** models are getting "very clever" about *which* tools to use and *how* to use them (largely model-driven, not hand-engineered).

### Why Foundry
All of this is available on **Microsoft Foundry**. The value proposition:
- **Frontier intelligence** from Anthropic models.
- **Built-in safety and governance** that ships with the models.
- **Enterprise back-end privacy and compliance.**
- **Native integration with the Microsoft stack.**
- Net effect: **get from pilot to production faster.**

### The model catalog (pick the right tool)
- **Opus 4.8** — released ~a week before the talk. The **most capable / frontier** model. Use for **truly challenging problems**, where **accuracy is critical**, and **long-horizon / long-running** tasks.
- **Sonnet 4.6** — very capable and the **better cost alternative**, especially strong at **coding tasks**. Recommendation: **start with Sonnet**, then move up to Opus only if needed — a great cost-management strategy.
- **Haiku** — the **fast** model. Excellent for **summarization and classification** and any **high-volume, low-latency** workload. "Don't count it out."
- Consistency across all three: **same prompting strategy, same safety, same Constitutional AI** baked in — so you can **redirect freely between models** without re-engineering.

### The four frontiers of agentic coding
Carolyn structures the rest of the talk around four "edges" that currently hold agentic coding back. Pushing each edge outward unlocks more value. Each has a live demo.

1. **What agents are allowed to touch** — how often must a human be present directing it?
2. **How will the agent know when it's right?** — we can't review every line/PR ourselves; agents must check themselves.
3. **What agents can perceive** — text/diffs are great, but agents need richer perception (vision) to work the way humans do.
4. **When and where agents run** — can it keep running and continue on its own?

She kicks off the **fourth frontier's demo first** (a long-running task) so it can execute in the background while she talks: using **Corgi Code** (auto-caption garble; this is Claude Code / Cowork-style coding agent tooling), she tells an agent to **build an arcade game** using **dynamic workflows** (new with Opus 4.8, for working with sub-agents), then leaves it running.

### Frontier 1 — What agents can touch (Auto mode)
The problem: you kick off a task, go get coffee, and come back to find the agent **asked permission repeatedly** while you were away (edit this file? update the README? run this test?). The old workaround was **"dangerously skip permissions"** — which is "about as comfortable as that sounds. It's very creepy." Everyone advises against it.

The new answer is **auto mode**:
- A **classifier sits between your requests and the model**.
- It lets the agent run but is **smart about what it allows**: low-risk actions (reading a file, running a test case) proceed automatically; **risky/destructive** actions (e.g. running a random bash command) still prompt you.
- Reported **0.4% false positive rate** — much less annoying than before.
- "Overeager actions" = cases where it allowed something you'd have preferred it ask about — still being tuned.
- Status: **research preview**, but a huge step up.

**Demo (before/after):** In regular Claude Code (no special config), she asks it to **add an endpoint to a FastAPI app**. As predicted, it interrupts to ask permission to edit the file (even though the prompt told it to), then to update the README, then to run a test — making the **human the bottleneck** on trivial tasks. She then uses **rewind** (a Claude Code feature) to reset files back to the original prompt, switches on **auto mode** (yellow indicator), and re-runs. Same result — but this time **zero interaction needed**; she walks away. The payoff: leave your desk, go to a meeting, come back to **completed work**, within safe bounds.

### Frontier 2 — How the agent knows it's right (the Oracle / evaluator)
Quality control is critical: to scale, we want **AI agents reviewing AI-generated code**, but safely and trustworthily.

**Case study:** **16 parallel agents** across **100,000 lines of code** building a **C compiler**. It cost a lot, took a ton of sessions, and was "a bit of a failure." The lesson: you need a **separate agent to judge** — *not* the agent that wrote the code.

**The recommended architecture:**
- **Planner** — decomposes the task.
- **Generator** — writes all the code.
- **Evaluator** — reviews what was generated and checks whether it truly fits the need.

In the compiler case, **GCC** provided a clean oracle (compiled code either matches or it doesn't). Not every use case has such a clean signal, but the strong recommendation is to **invest heavily in building the evaluator** — that's where time/effort/research should go, because it's what unlocks generating more and more code. **Build the tests / evaluation harness first**, before you start coding.

**Demo (the Oracle):** Using a split terminal — left = generator, right = reviewer/evaluator ("the Oracle"). She asks for a simple **bill-split function** ("friends went to dinner, split the bill"). In auto mode it builds an initial version that knowingly **drops the cents** (not ideal). The **separate reviewer agent** is told to be **adversarial / as tough as possible**, looks at the generated code, **writes its own test case**, and the test **fails** — surfacing that the basic approach works but could be handled better. The advice flows back to the writer agent, which **updates its code**. Takeaway reinforced: build the judge first; it's your "safety blanket" that code is already ready to be tested.

### Frontier 3 — What agents can perceive (vision)
Reading a diff/code is powerful, but **seeing what you see** is critical. Recent Claude capabilities:
- **Claude in Chrome** — works in a **real Chrome browser** (not a headless scrape), so it can walk through and *see* the rendered UI while working with code.
- **Computer use** — go out into the machine itself; e.g. spin up an **iOS simulator**, run the app, see what's happening, and make adjustments.
- **High-resolution images** — a very recent **Opus 4.8** capability: it can handle **much larger image resolutions** than before.

**Why it matters (stat):** **Expo** (penetration-testing example) went from **~58% success (Opus 4.6)** to **~98% (Opus 4.8)** on agentic pen testing, driven by the **visual acuity** from high-res image support.

**Demo (pen test in Foundry):** She runs **Claude Opus 4.8 in Azure Foundry** (same model, hosted in Foundry) with a **security-engineer** system prompt, asking it to evaluate a **suspicious-looking screen**. She shows the audience the screenshot for **~5 seconds** and asks who can spot risks — only **one person** could. She then feeds the same screenshot to the Claude model in Foundry; in **~3.4 seconds** it reasons over the image and identifies **multiple security risks** that were **not obvious** (no "password here" or "secrets" labels). The point: visual perception + reasoning lets the model ingest an image, understand it, and apply security knowledge to find non-obvious issues — a key lever for pushing agentic frameworks.

### Frontier 4 — When and where agents run (multi-surface, always-on)
Agents are expanding from minutes to **long-running** operation, and can run on **whatever surface you want**:
- Kick off on the **terminal**, go to a meeting, **approve a prompt on your phone** (some prompts still need human approval), then return to your desktop with work complete.
- **Loops** and **scheduled tasks** — hands-off; agents pick up tasks and run as needed.
- **Parallel** execution.
- **Ultra Plan** — go deep and produce a significant plan.
- **Voice** — speak to it; makes interaction faster.

**Payoff demo (the arcade game finishes):** Returning to the task kicked off at the start, it's **done**. The highlight is **dynamic workflows** — a clever way to manage sub-agents, surfaced via a new **`/workflows`** command. What happened automatically:
- **Three design agents** each proposed an arcade game: **"Neon Drift"**, **"Pulse Runner"** (which one agent found already existed), and **"Neon Ascent."**
- A **"picker" judge agent** chose **Neon Ascent** to move forward with, then built it.
- **Four test agents** were spun up to test it — including **opening it in a real browser** and checking **visual polish** (she had told it the game would be shown on a **projector**, so it accounted for that).
- It **found a couple of issues and fixed them** — all in **~15 minutes** with **almost no interaction** ("build an arcade game and don't talk to me about it very much, I'm busy").

She then shows the finished, playable game (with visuals and some sound), built from just a couple of lines of instruction via dynamic workflows.

### Wrap-up
The goal is **not to remove humans entirely** — it's to keep humans focused on the **most important, risky, high-value** decisions while agentic coding handles the rest in safe bounds. The four frontiers — touch, correctness, perception, and runtime — are all being pushed to make agentic coding more capable and "a little bit more human."

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry / Azure Foundry** — Microsoft's platform for hosting Anthropic/Claude models with enterprise safety, governance, privacy, compliance, and Microsoft-stack integration.
- **Claude Opus 4.8** — Anthropic's most capable frontier model (released ~1 week prior); accuracy-critical, long-horizon work; adds high-res image perception and dynamic workflows.
- **Claude Sonnet 4.6** — capable, cost-effective model; strong at coding; recommended starting point.
- **Claude Haiku** — fast, low-latency model for summarization, classification, high-volume tasks.
- **Claude Code** — Anthropic's agentic coding tool (referred to in captions as "Corgi Code"/"Cloud Code"/"Claude code"); used for the live demos.
- **Cowork** — Microsoft Foundry agentic coding experience (per session title).
- **SWE-bench Verified** — coding benchmark (~500 GitHub issues) used to measure production-ready code generation.
- **Auto mode** — research-preview classifier between request and model that auto-approves low-risk actions and prompts only for risky ones (replaces "dangerously skip permissions").
- **Rewind** — Claude Code feature to reset/return to an earlier state (files reset to a prior prompt).
- **Dynamic workflows** (`/workflows`) — new orchestration mechanism (with Opus 4.8) for managing sub-agents (planner/generator/picker/test agents).
- **The Oracle (evaluator/judge agent)** — a separate adversarial reviewer agent that writes its own tests and critiques generated code.
- **Claude in Chrome** — runs in a real Chrome browser (not headless) so the agent can see rendered UI.
- **Computer use** — lets the agent operate the machine (e.g. iOS simulators) and see results.
- **Ultra Plan** — deep planning mode for significant plans.
- **Voice** — speak-to-agent interaction for faster input.
- **Loops / scheduled tasks / parallel agents** — mechanisms for hands-off, always-on, concurrent agent operation.
- **Constitutional AI** — Anthropic's safety approach baked into all models.
- **FastAPI** — Python web framework used in the auto-mode endpoint demo.
- **GCC** — used as the "oracle" ground truth in the C-compiler case study.

## 🚀 Announcements / What's New
- **Claude Opus 4.8 — released ~1 week before the session** as Anthropic's most capable frontier model (accuracy-critical, long-horizon, long-running tasks). *(Available on Foundry.)*
- **High-resolution image support in Opus 4.8** — handles much larger image resolutions than prior models; cited as driving the pen-testing jump from ~58% (Opus 4.6) to ~98%.
- **Dynamic workflows** — new with Opus 4.8; a way to orchestrate/manage sub-agents (surfaced via `/workflows`). Described as not yet fully in the presentation but called out as new.
- **Auto mode** — **research preview**; classifier-gated permissioning replacing "dangerously skip permissions" (reported 0.4% false positive rate).
- **Claude models on Microsoft/Azure Foundry** — frontier Claude (incl. Opus 4.8) available in Foundry with enterprise governance/privacy/compliance and Microsoft-stack integration.
- *(Status note: auto mode is explicitly research preview; Opus 4.8 is GA/available; dynamic workflows tied to the Opus 4.8 release.)*

## 💡 Demos
- **Long-running arcade game (dynamic workflows)** — Kicked off at the start ("build an arcade game, don't talk to me much"), ran ~15 min in the background. Showed sub-agent orchestration: 3 design agents (Neon Drift, Pulse Runner, Neon Ascent), a "picker" judge selecting Neon Ascent, and 4 test agents (including real-browser testing + visual-polish checks for a projector). It found and fixed issues, then produced a playable game with visuals/sound. **Proves:** agents can run autonomously, orchestrate sub-agents, self-test visually, and ship a working artifact with minimal human input.
- **Auto mode (FastAPI endpoint, before/after)** — Regular Claude Code repeatedly asks permission (edit file, update README, run test), making the human a bottleneck. After **rewind** + enabling **auto mode**, the same task completes with zero interruptions. **Proves:** classifier-gated permissions let agents safely run unattended on low-risk work.
- **The Oracle (bill-split function)** — Generator writes a bill-split function that drops cents; a separate adversarial reviewer agent writes its own test, it fails, advice flows back, generator updates the code. **Proves:** a separate evaluator/judge (build it first) scales safe AI-on-AI code review.
- **Pen-test image reasoning (Foundry, Opus 4.8)** — Audience sees a suspicious screenshot for ~5s (only 1 person spots a risk); Claude Opus 4.8 in Foundry analyzes the same image in ~3.4s and surfaces multiple non-obvious security risks. **Proves:** high-res visual perception + reasoning finds issues humans miss with no explicit labels.

## 📊 Notable Stats / Quotes
- **49 → 87.6** on SWE-bench Verified across 6 model generations in 18 months — "We've pretty well solved coding when you look at it from this metric's perspective."
- **14.5 hours** — one of the longest recorded agentic sessions sustaining good accuracy ("think about that… letting it run for hours or even days").
- **0.4% false positive rate** for auto mode's permission classifier ("so we're less annoying").
- C-compiler case study: **16 parallel agents** across **100,000 lines of code** — "a bit of a failure," which motivated the planner → generator → evaluator pattern.
- Pen testing (Expo): **~58% (Opus 4.6) → ~98% (Opus 4.8)** success, attributed to high-resolution visual acuity.
- **~3.4 seconds** for Opus 4.8 in Foundry to analyze the screenshot and find security risks; only **1 audience member** spotted any risk by eye.
- On "dangerously skip permissions": *"It's about as comfortable as that sounds. It's very creepy. You don't want to do that."*
- *"That evaluator, the judge, that's very important. Do that first, and then you can do whatever you want with your code."*
- *"We don't want to remove humans entirely… the goal is to have humans evaluating and looking at the things that are most important."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Stand up **Claude Opus 4.8 / Sonnet 4.6 in Azure Foundry** and benchmark a real coding task (start Sonnet, escalate to Opus only if needed).
  - Pilot **auto mode** on a low-risk repo to evaluate the false-positive/overeager behavior in practice.
  - Build a **planner → generator → evaluator (Oracle)** loop with an adversarial reviewer + auto-generated tests *before* generating production code.
  - Experiment with **dynamic workflows / `/workflows`** + sub-agents (designer → picker → tester pattern) on a self-contained task.
  - Test **high-res image perception** for a visual QA or security-review use case (screenshot → risk analysis).
- [ ] Questions:
  - What are the exact Foundry SKUs, region availability, and pricing for Opus 4.8 vs Sonnet 4.6 vs Haiku?
  - Is **auto mode** available through Foundry-hosted Claude or only Claude Code? How configurable is the risk classifier?
  - How do **dynamic workflows** map to existing sub-agent / orchestration features — any API surface vs CLI-only (`/workflows`)?
  - How does the **Cowork** experience differ from raw Claude Code on Foundry (per the session title)?
- [ ] Relevant to:
  - Internal coding-agent / dev-productivity initiatives on Azure.
  - Security/pen-testing automation
---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/observability
  - topic/evals
source: https://www.youtube.com/watch?v=wFB7wmWvL6U
session_code: DEM361
event: Microsoft Build 2026
speakers: Jim Bennett (Microsoft MVP, Foundry & Dev Tools)
duration_min: 18
aliases:
  - Understand and fix Agent Framework apps with observability and evals
---

# DEM361 — Understand and fix Agent Framework apps with observability and evals

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speaker:** Jim Bennett — Microsoft MVP for Foundry and Dev Tools  
> **Duration:** ~18 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=wFB7wmWvL6U)

## 🎯 TL;DR
AI agents are black boxes — you build them with an LLM, instructions, and tools, then "hope it works" without seeing what happens under the hood. This demo-heavy session shows how to crack open that black box using **observability** (OpenTelemetry + **OpenInference**, visualised in the open-source **Phoenix** backend) and then verify correctness using **evals** (LLM-as-a-judge testing). Jim Bennett builds a procurement-approval agent in ~11 lines of Microsoft Agent Framework code, traces every LLM call and tool invocation, then writes an eval prompt that scores whether each decision is *grounded in the tool evidence* — exposing that the agent only worked ~50% of the time. By feeding the inputs + evals into a continuous testing loop (and even handing it all to a coding agent like GitHub Copilot CLI), he iterates toward ~90% effectiveness, demonstrating the foundations of a "self-improving software" loop.

## 🔑 Key Takeaways
- An agent = **LLM + instructions + tools**. With Microsoft Agent Framework, you interact via essentially one line (`agent.run(inputs)`) — but that convenience hides all the decision-making (which tools to call, in what order, looping back to the LLM) inside a black box.
- **OpenTelemetry** is the open standard for app observability (request timings, 200s/400s/500s). The same principle can be applied to AI apps.
- **OpenInference** (by Arize) is an open-standard *extension* to OpenTelemetry implementing the semantic conventions for AI/GenAI. It's been around a few years and works *today*, unlike the still-in-committee OTel GenAI standard.
- OpenInference is the standard underpinning Microsoft's new **assert framework / Agent Control specification** (referenced from Sarah Bird's session the prior day).
- Adding tracing is low-effort: a couple of lines to start a trace, send it to OpenInference, then export to a backend.
- **Phoenix** (free, open-source, by Arize) renders OpenInference data as a span tree: the agent run → LLM calls (system prompt, user prompt, requests, tool calls, token counts in/out) → individual tool executions and their responses — granular visibility across the whole flow.
- Because it's standard OpenTelemetry, you get standard tricks: e.g. drop in a **span processor to strip PII / customer data** on the way out. Works in dev (1–2 rows) and in production (millions of rows).
- LLM output is **non-deterministic**, so classic "given input X, expect output Y" unit testing doesn't apply. Enter **evals** = "testing for AI."
- **AI-as-judge beats humans for evaluation at scale** — not because AI is smarter, but because humans get bored, biased, and make mistakes (the parole-before-lunch bias). AI is "just as good as a human but doesn't get bored."
- A classic failure: a tool returns blank (e.g. no policy), and a "helpful" agent approves everything anyway. Evals catch this by checking whether the recommendation is **supported by the tool evidence alone**.
- An eval turns non-deterministic agent output into a **deterministic score** (supported/unsupported, 0/1) by feeding the request + tool evidence + agent decision + reasoning into a judge prompt with a scoring rubric.
- Once you have **inputs + evals**, you can build automated, TDD-style testing: collect inputs into a dataset, run them through the agent, score with the evaluator, then tweak until the numbers go green.
- **Model selection is the killer use case**: same agent, no code changes, just swapping the model (GPT-4.1 → "GPT-5.4"/GPT-5-class) jumped effectiveness from ~50% to ~90%.
- **Coding agents close the loop**: GitHub Copilot CLI (or Claude) with skills can access this data, spin the app up in a sandbox, run inputs + evals, then iterate on prompts, model choice, and tool descriptions — converging on ~90% over ~4–6 cycles. This is the foundation of **self-improving software**.
- Reality check: **agents will never be 100%** (neither are humans) — aim for ~90%.

## 📚 Detailed Notes

### Framing: Do you actually know what your agent is doing?
Jim opens by polling the room: who's heard of AI (everyone), who's *building* agents (a few), who knows what their agent is doing under the hood (few), and who knows if their agent is actually *working* (few). The whole session targets these last two questions. The thesis: **you probably don't know what your agent is doing under the hood, and you don't know if it's working.** Rather than slides, the talk is almost entirely live tooling.

### The agent itself (≈11 lines of code)
"All the cool kids tell me agents are lit" — and an agent is literally just **LLMs + instructions + tools**. Jim's demo agent is ~11 lines:
- **Model**: an OpenAI model running on **Microsoft Foundry** (Foundry = a place to run your models and do related work).
- **Instructions**: he's built a **procurement system evaluator** — a deliberately "boring line-of-business" app. Instead of humans approving/denying purchase requests, the agent runs the approve/deny cycle: read the purchase request, gather relevant policy / vendor / budget info, then decide.
- **Tools**: a series of tools — e.g. a **check-policy** tool, a **vendor lookup** tool, a **budget** lookup, etc.

This is just scaffolding. **Microsoft Agent Framework does the rest.** The entire interaction is one line: *"Agent, run. Here are the inputs. Go do your thing,"* and an output comes back. Fingers crossed it works.

### Why it's a black box
With that one-line interface, all the real decisions happen unseen:
- The **LLM decides** whether to call a tool, *which* tools to call, and in *what order*.
- The **Agent Framework** takes the tool results, calls the LLM again, does more steps, loops.
- All you ever see is the **final output**. No visibility into the intermediate steps.

**Demo (black box):** A purchase request for **$3,200** for the **engineering team** to buy an updated **IDE**. The agent returns "approved" with a reason. It *could* be right or wrong — you simply don't know. "Complete black box."

### Observability: OpenTelemetry → OpenInference
- **OpenTelemetry**: the standard way to see what applications are doing — bolt it onto a web app, see request durations, 500s/400s/200s. Wouldn't it be nice to apply that same open-standard principle to AI apps?
- **OpenInference**: an open-standard *extension* for OpenTelemetry that works with the **semantic conventions for AI** — basically making AI work with OpenTelemetry.
- The OpenTelemetry project is working on its own **GenAI standard**, but it's "in a committee and we all know what committees are like." Until that lands, **OpenInference has existed for a few years** and is usable now.
- Notable tie-in: OpenInference is the standard being used for Microsoft's **assert framework and Agent Control specification** (referenced from **Sarah Bird's** session the day before).

**Instrumenting is simple:** because OpenTelemetry is a standard, you just drop in a couple of lines to say "I want to trace this," send it to OpenInference, and export to a backend that exposes the visibility.

### Phoenix: visualising the traces
The backend shown is **Phoenix** — a free, open-source telemetry backend made by **Arize** (the folks who invented OpenInference). It's the default out-of-the-box way to render OpenInference data.

What Phoenix shows for the agent run:
- **Top-level span**: the process run — the $3,200 / IDE-upgrade request and the response ("Yes, it's compliant").
- **Tree diagram** of everything the agent did:
  - Microsoft Agent Framework **kicks off the agent**.
  - It **calls an LLM** — you can see the **system prompt**, **user prompt**, the requests, and the **tool calls** that come back.
  - Drill into **attributes**: **token counts in and out**, the model (OpenAI), framework (Microsoft Agent Framework).
  - You can see exactly **what goes into the LLM and what comes back**, and the LLM's decision to call a tool.
  - The **check-policy tool** is called (3,200 / "TechFlow") and you can see the **response it returns**, and so on down the tree.

This gives **granular, end-to-end visibility** over everything the app does — usable in **dev** (1–2 runs while experimenting) and in **production** (thousands / millions of rows).

**Standard-OTel bonus:** because it's plain OpenTelemetry, you can use standard tricks — e.g. drop in a **span processor to strip out PII / customer data** or otherwise manipulate the data on the way out.

➡️ This answers the first question: **you can now see inside the black box.** Next question: **is it working?**

### Evals: testing non-deterministic AI
Jim pivots to correctness, gently ribbing the room about not writing unit tests ("I'm not mad, I'm just disappointed").

- **Deterministic code**: given inputs → expect a specific output. Easy to unit test.
- **LLMs**: given inputs → **non-deterministic** output. The classic test pattern breaks.

So how do you know an LLM is working?
- **Easiest: ask a human to look.** But humans aren't great evaluators — they get **bored**, have **biases**, and **make mistakes**. Example: parole reviews scheduled **just before lunch** go badly; **after lunch** you're fine — bias driven by boredom/fatigue.
- **AI as evaluator** is "just as good as a human, still makes mistakes, but **doesn't get bored**" — and crucially it **runs at scale**.

**The failure mode to catch:** what if a tool fails — e.g. the **policy tool returns blank**? A "helpful" agent reasons "there's no policy, so it must be fine — approved," and now anyone can buy a million dollars of software because there was no policy. How do you detect this? Because you now have full visibility, you can take that trace data and **throw it at an AI judge**: "Is this good? Does it actually do what it's supposed to?"

This is what **evals** are — "the fancy AI word for testing." (Jim's aside: "We should have called it testing because people know what testing is, but we have to call it evals because we're cool and different.")

### Writing the eval prompt (LLM-as-a-judge)
Jim shows an eval prompt roughly structured as:
- **Role**: *"You are auditing an automated procurement evaluator."*
- **Task**: decide whether the **recommendation is supported by the tool evidence alone** (i.e. is the decision *grounded* in the data the tools returned?).
- **Rubric** for scoring: approve / reject / blank-for-review.
- **Fill-in slots**: the original **purchase request**, the **evidence** (data returned by the tools), what the **agent said**, **why** the agent said it.
- **Output**: "is the recommendation supported by tools — supported / unsupported — return one word."

The key idea: layering this eval on top of the agent **converts the non-deterministic agent output into a deterministic output** (supported / unsupported → 1 / 0).

**Running it:** go to Phoenix, **download the telemetry data**, pull out the tool outputs, drop them into the eval prompt, send to an AI, and get a score (**0 = doesn't work, 1 = works**).

### Eval results — the agent only works ~50% of the time
Switching to a different Phoenix project to see scored results:
- **First trace example**: **supported** — "the evidence shows sufficient budget, the vendor's preferred, the purchase amount is under the auto-approval threshold." The tool data agrees with the decision. 
- **But across all rows**: pass, pass, **fail, fail, fail, fail, fail** — it only works about **half the time**. Half the time the agent's decision is **not grounded** in the tool data.
- **Concrete bad row**: marked **unsupported**. There's sufficient budget, but **the policy requires BP (business-partner) approval** for this level. The agent **rejected** it — but it should have **flagged it for BP review**, not rejected it. The judge surfaces exactly what went wrong and why.

With LLM-as-a-judge, you can see precisely what's happening and what mistakes are being made.

### Closing the loop: datasets + continuous testing (TDD for agents)
Now there are **inputs + tests + results** — enough to build automated testing:
- Extract all the input data into a **dataset**.
- **Run inputs through the agent → score with the evaluator → read the score.**
- Make fixes, run again — just like **test-driven development**: write tests up front, keep running until everything goes green. Keep tweaking the agent until the numbers come out good.

### Model selection — the headline result (50% → 90%)
The classic application of this loop is **model selection** — your app is bad and you want a better model, or it's good and you want a **cheaper** model, or a provider just shipped a new model and you need to confirm your app still works.

**Demo:** the **exact same application/agent, nothing changed except the model** — running against **"GPT-5.4" instead of 4.1** (i.e. a GPT-5-class model in place of GPT-4.1). Result: now **~90% effective**, up from ~50%, with **zero code changes** — purely a model swap, validated by the dataset + eval loop.

### Coding agents → self-improving software
Take it further with **coding agents** (GitHub Copilot CLI, or Claude — Jim jokes "any Claude people in the room? It's okay, Microsoft won't shoot you"). Coding agents can have **skills**, and skills can access this eval/telemetry data. So you can hand a coding agent:
- your **code / GitHub repo**,
- the **inputs** you run through the agent,
- the **evals** you run,

and say **"fix my application."** The coding agent then:
1. Spins the app up in a **sandbox** environment.
2. Pumps in the inputs and **runs the evals**.
3. Looks at the results.
4. **Tweaks prompts, changes the model, adjusts tool descriptions**, etc.
5. Runs it again… and again, **converging on a better solution** over ~**4–6 cycles** toward the **~90%** mark.

> **Top tip:** agents will never be 100% — humans aren't either — so target ~90%.

This is the foundation of a **self-improving software loop**: monitor apps, see what's going wrong, ask coding agents to fix it. Jim frames this as "the future of the software we're building."

### Recap
- An agent is a **black box** — you don't know what it's doing.
- Add **observability** so you can see inside it. **OpenInference** is the industry standard for AI observability; it gives you the view.
- Build **evals** — use **LLM-as-a-judge** to test agent runs.
- Use that data to drive **self-improvement**: deploy models to **Foundry**, build with **Microsoft Agent Framework**, then point **GitHub Copilot CLI** at it and say "fix it."

### Logistics (closing)
- Jim shares a QR code linking to his LinkedIn for follow-up questions.
- **Phoenix** is free and open-source — scan the QR to grab it; you can run it **completely locally**.
- He *would* have shown deploying Phoenix to **Azure Container Apps**, but his **Microsoft MVP Azure credit ran out three hours earlier** — so no Azure demo.
- A **GitHub repo** with all the code is provided so attendees can reproduce the whole demo.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Agent Framework** — framework for building agents; reduces the agent to ~11 lines + a single `run` call, orchestrating LLM↔tool loops.
- **Microsoft Foundry** — platform/place to run your models (and related capabilities); deployment target for the models used here.
- **OpenAI model (GPT-4.1)** — the model originally powering the agent (~50% effective in the eval).
- **GPT-5.4 / GPT-5-class model** — the upgraded model that lifted effectiveness to ~90% with no code changes (name per auto-captions).
- **OpenTelemetry (OTel)** — open standard for application observability (timings, status codes); foundation that AI observability extends.
- **OpenInference** — open-standard extension to OpenTelemetry implementing AI/GenAI semantic conventions; usable today; created by Arize.
- **OpenTelemetry GenAI standard** — official GenAI conventions still in committee (not yet ready).
- **Phoenix** — free, open-source telemetry backend by Arize that renders OpenInference data as a span tree; runnable locally; deployable to Azure Container Apps.
- **Arize** — company that created OpenInference and Phoenix.
- **assert framework / Agent Control specification** — Microsoft work built on OpenInference (referenced from Sarah Bird's session).
- **Span processor** — OpenTelemetry mechanism used here to strip PII / customer data on export.
- **LLM-as-a-judge / evals** — pattern of using an AI to score agent outputs against a rubric, producing deterministic pass/fail.
- **GitHub Copilot CLI** — coding agent that, via skills, can access eval data and iteratively fix the application in a sandbox.
- **Claude** — alternative coding agent mentioned alongside Copilot CLI.
- **Azure Container Apps** — intended (but unshown) deployment target for Phoenix.
- **GitHub repo** — companion repo containing all demo code for reproduction.

## 🚀 Announcements / What's New
None explicitly announced as a new product release in this session. The talk is educational/demo-focused. Notable contextual items:
- **OpenInference is the standard powering Microsoft's new assert framework / Agent Control specification** (referenced from Sarah Bird's prior-day session) — a forward-looking pointer rather than a launch here.
- The **OpenTelemetry GenAI standard** is noted as still in committee (not yet available) — roadmap context.

## 💡 Demos
1. **Black-box agent run** — The ~11-line procurement-evaluator agent approves a **$3,200 IDE purchase** for engineering. *Proves:* an agent is trivial to build and call, but you only see the final answer — no insight into the tool calls/decisions behind it.
2. **Phoenix trace view** — The same run rendered as a span tree (agent → LLM call with system/user prompts, token counts → check-policy tool call + response). *Proves:* OpenInference + Phoenix give granular, end-to-end visibility inside the black box at dev and production scale.
3. **Eval scoring (LLM-as-a-judge)** — A judge prompt scores whether each decision is "supported by tool evidence alone," yielding 1/0 across rows. Result: ~**50%** pass; a flagged row shows a request that was **rejected** when it should have been **flagged for BP review**. *Proves:* evals turn non-deterministic output into deterministic, debuggable pass/fail and expose real grounding failures.
4. **Model swap (4.1 → GPT-5.x)** — Identical agent, only the model changed, re-run through the dataset + evals. Result jumps to ~**90%**. *Proves:* the eval loop lets you safely evaluate model changes/upgrades and quantify the impact with zero code changes.
5. **Coding-agent self-improvement** — Hand the repo + inputs + evals to GitHub Copilot CLI / Claude; it sandboxes the app, runs evals, and iterates on prompts/model/tool descriptions over ~4–6 cycles toward ~90%. *Proves:* the foundations of a self-improving software loop are achievable today.

## 📊 Notable Stats / Quotes
- **~11 lines of code** define the entire agent.
- **One line of code** (`agent.run(...)`) is the whole interaction surface.
- **$3,200** sample purchase request (engineering team, IDE upgrade).
- **~50% → ~90%** effectiveness improvement *from a model swap alone* (GPT-4.1 → GPT-5-class), no code changes.
- **~4–6 cycles** for a coding agent to converge toward ~90%.
- "**Agents will never be 100%. Humans are never 100%.** But you want to work towards 90%."
- "We should have called it **testing** because people know what testing is. But we have to call it **evals** because we're cool and different."
- On AI vs human evaluators: "**AI is just as good as a human. Still makes mistakes, but doesn't get bored.**"
- The **parole-before-lunch bias** anecdote — humans get fatigued/biased; AI doesn't get bored and runs at scale.
- "My **Microsoft MVP Azure credit ran out three hours ago**" — why the Azure Container Apps deploy wasn't shown.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Clone the session's **GitHub repo** and reproduce the procurement-evaluator agent end-to-end.
  - Run **Phoenix locally** and wire up **OpenInference** instrumentation on an existing **Microsoft Agent Framework** app.
  - Write an **LLM-as-a-judge eval** ("supported by tool evidence alone" + rubric) and build a small **dataset** for a TDD-style regression loop.
  - Reproduce the **model-swap experiment** (e.g. 4.1 → a GPT-5-class model) and measure effectiveness deltas via evals.
  - Try a **span processor** to strip PII before export.
  - Point **GitHub Copilot CLI** (with skills) at repo + inputs + evals and let it iterate toward ~90%.
- [ ] Questions:
  - Exact model name behind "GPT-5.4" (auto-caption) — confirm the real GPT-5-class model used.
  - What exactly is Microsoft's **assert framework / Agent Control specification** (from Sarah Bird's session), and how does it consume OpenInference?
  - OpenInference vs the in-committee **OTel GenAI** conventions — migration/compatibility path when the official standard ships?
  - Recommended way to deploy Phoenix to **Azure Container Apps** for team/production use.
- [ ] Relevant to:
  - Building/operating production agents on **Microsoft Foundry + Agent Framework**.
  - AI observability, evals, and CI-style regression testing for any agentic / LLM app.
  - Line-of-business approval/automation workflows where decisions must be grounded in tool data.
  - Self-improving software / autonomous-fix pipelines using coding agents.

## 🔗 Related
- [[Microsoft Build 2026]]
- Sarah Bird session (Build 2026) — assert framework / Agent Control specification (built on OpenInference)
- [OpenInference](https://github.com/Arize-ai/openinference) — open standard for AI observability
- [Phoenix by Arize](https://github.com/Arize-ai/phoenix) — open-source telemetry backend
- [OpenTelemetry](https://opentelemetry.io/) — base observability standard
- Microsoft Agent Framework · Microsoft Foundry · GitHub Copilot CLI
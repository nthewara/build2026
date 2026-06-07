---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/observability
  - topic/agents
  - topic/azure-monitor
  - topic/opentelemetry
  - topic/ai
source: https://www.youtube.com/watch?v=a7FELS8hQAE
session_code: BRK252
event: Microsoft Build 2026
speakers: Abishek (PM, Microsoft Foundry Observability), Sebastian (PM, Microsoft Foundry Observability), Felicia (PM, Microsoft Foundry), Vivek (PM, Microsoft Foundry)
duration_min: 35
aliases:
  - From observability to ROI for AI agents on any framework
---

# BRK252 — From observability to ROI for AI agents on any framework

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Abishek, Sebastian, Felicia & Vivek (Microsoft Foundry / Foundry Observability PM team)  
> **Duration:** ~35 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=a7FELS8hQAE)

## 🎯 TL;DR
Microsoft Foundry observability gives you an end-to-end **agent DevOps life cycle** built on four pillars — **tracing → evaluation → monitoring → optimization** — that works for *any* agent on *any* framework (LangChain, LangGraph, OpenAI SDK, Microsoft Agent Framework), not just Foundry-native agents. The session walks the full inner-loop/outer-loop journey through four live demos on a real "vendor history analyst" data-center agent: getting-started evaluation in the portal (with the new **rubric evaluator**), code-first observability via the **Foundry MCP server + Foundry skill** in VS Code, automated **AI Agent Optimize** that hill-climbs your system prompt / tools / model, and finally **Agent ROI** that proves business value by netting agent value against token + tool cost. Everything is grounded in **OpenTelemetry GenAI semantic conventions** (Microsoft is actively contributing, e.g. new memory semantics) and flows to **Azure Monitor** for full-stack visibility, then back into Foundry for centralized AI observability. The throughline: agents are non-deterministic, so you need observability to make them reliable, continuously improve them, and prove they're worth the spend.

## 🔑 Key Takeaways
- Foundry observability rests on **four pillars**: tracing (full end-to-end execution workflow), evaluation (quality/safety run *off the traces*), monitoring (run the same offline evals online to catch issues in real time), and optimization (continuously improve).
- Observability is part of Foundry's **control plane** that spans the agent service, models, IQ for knowledge, tools, and ML capabilities like fine-tuning.
- **Open ecosystem support** is the headline: you can trace and evaluate **non-Foundry agents built with any framework** — LangChain, LangGraph, OpenAI SDK, Microsoft Agent Framework — getting full execution visibility and eval signals from the traces.
- The **rubric evaluator** (public preview) auto-generates a **multi-dimensional** evaluator (the demo produced 8 weighted dimensions) from just your system prompt + agent, usable for both offline testing and online evaluation — even with **zero existing data**.
- Evals run continuously against **production traces pulled from Application Insights**; low-scoring traces are drillable down to the exact prompt/response to root-cause hallucinations.
- **Full-stack observability** comes from Foundry's partnership with **Azure Monitor**: Foundry observes apps/agents/AI-platform components, ships the data to Azure Monitor for a cross-resource view, then reads it back into Foundry for centralized AI observability.
- **Code-first observability**: the **Foundry MCP server + Foundry skill** ship in the **Foundry toolkit** (a VS Code extension) so you can fetch eval results, get grounded explanations, and take actions on Foundry from your IDE / GitHub Copilot Chat / CLI.
- A **skill** is an *opinionated flow* authored by the Foundry team — it knows which part of the observability loop you're in, grounds analysis in your **repo context + Foundry skill context** (more trustworthy than a generic LLM), and connects client-side vs server-side issues.
- **Multi-turn evaluation** (public preview): evaluate across an entire session, not just single turns — e.g. a session that succeeds but takes 20 min when 5 was expected is *not* a success.
- **User simulation** (public preview): auto-generate realistic conversations to bootstrap multi-turn evaluation when you lack real multi-turn data.
- **Traces → datasets with smart filtering** lets you feed production traces back into the inner loop to expand test coverage beyond your initial handful of cases (20 test cases won't cover production).
- The **evaluator catalog** spans quality, risk, safety, and agent evaluators; many are now multi-turn (groundedness, coherence, task completion, customer satisfaction, rubric). Use a mix — **code-based evaluators** (regex, DB lookups) are recommended for deterministic checks instead of an LLM-as-judge.
- **AI Agent Optimize** (private preview, public preview soon) automatically creates and deploys new agent versions, hill-climbs the system prompt / skills / tool descriptions / model against your dataset + rubrics, and keeps what works — demo got a **24% boost** and went **38/40 → 40/40** tasks, lifting score **0.577 → 0.7** in **25 minutes**.
- **Agent ROI** (private preview, public preview soon) proves business value: assign a dollar business value to an evaluator, auto-pull token cost, add tool cost, and track **net value per agent version** over time — revealing, e.g., that **tool calls cost more than the LLM** and surfacing low-ROI/failed invocations to drill into.
- Microsoft is **deeply invested in OpenTelemetry** as the standard underpinning both tracing and evaluation — engineers actively contribute to the open-source community (newly contributed **memory semantics** coming to Foundry soon).
- Customer proof point: **NTT Data** uses Foundry + Azure Monitor to turn AI into an enterprise-grade, production-ready system.

## 📚 Detailed Notes

### Why observability for agents — the non-determinism problem
Agents are **non-deterministic**, which creates new reliability and consistency challenges for both developers and operators. A traditional deterministic app behaves predictably; an agent may answer the same class of question differently, hallucinate, or take an unexpectedly long path to a correct answer. Observability is the discipline that lets you *see* what your agent actually did, *assess* whether it was good, *catch* regressions in production, and *improve* over time. The session frames this as the reason the whole agent DevOps life cycle has to evolve.

### The four pillars of Foundry observability
Foundry observability is structured as four pillars that build on each other:
1. **Tracing** — view the **full end-to-end execution workflow** of your agents (every step, tool call, model invocation).
2. **Evaluation** — assess **quality and safety**; crucially, evaluations are **run off of the traces**, so the same captured execution data feeds the scoring.
3. **Monitoring** — run the **same evaluations you ran offline, now in an online setting**, so you detect issues in **real time** in production.
4. **Optimization** — **continuously improve** your agents using the signals from the first three pillars.

The key architectural idea repeated throughout: **traces are the substrate**. Evals, monitoring, ROI, and optimization all read from traces rather than requiring separate instrumentation.

### Observability as part of the Foundry control plane
Foundry positions observability not as a bolt-on but as part of the **control plane** that spans every capability you need to build production agents: the **agent service**, **models**, **IQ for knowledge** (retrieval/grounding), **tools**, and **ML capabilities such as fine-tuning**. Observability cuts across all of them, giving a single lens over the agent platform rather than per-component silos.

### The agent DevOps life cycle: inner loop ↔ outer loop
The organizing metaphor is **traditional DevOps evolving for the age of AI agents**:
- **Getting started** — out-of-the-box observability with no setup.
- **Inner loop** — where developers **plan, code, test, and release**, all with observability **at their fingertips directly within the IDE**.
- **Outer loop** — the same observability capabilities used to **monitor** agents in production, **analyze results and get insights**, and **optimize**.
- **The feedback cycle** — outer-loop signals (production traces, eval results) feed **back into the inner loop** for continuous improvement. This bidirectional flow is the heart of the talk.

### The demo scenario: vendor history analyst agent
All demos build on the **data-center operations scenario** introduced in **BRK241** ("developing production agents"). The agent is a **vendor history analyst** for Microsoft's data center operations. Use case: a **vendor manager** oversees vendors that fix/address issues in data centers and wants data-driven insight before conversations with those vendors. The agent **summarizes vendor job history, surfaces insights, and highlights key learnings** so the manager can have an evidence-based conversation that drives outcomes. This concrete, relatable scenario anchors every feature shown.

### Demo 1 (Felicia) — getting-started evaluation in the portal
Felicia starts from an **existing hosted agent** (the vendor analyst), referencing earlier sessions by Jeff and Tina on how hosted agents are deployed. In the **portal playground** she sends a basic user-style query and the **logs stream in on the right** in real time, confirming the request reached the agent.

The core challenge she calls out: when you first play with agents it's **hard to assess whether they're trustworthy or healthy** — how do you actually *evaluate* an agent? Her answer: **evaluation** is the keyword, and the goal is to set the agent up so you can evaluate across **a wide range of question types** a user might ask, covering many cases rather than one happy path.

### The rubric evaluator (new in Foundry)
While the agent "thinks," Felicia introduces the **rubric evaluator** — a new Foundry feature that produces a **multi-dimensional evaluation score** rather than a single pass/fail. To create one with **no existing data**, she:
1. Names the rubric and selects the **rubric type**.
2. Pastes in the **system prompt the agent uses**.
3. Selects a **model**.
4. Sets the **target** to the hosted agent shown earlier.
5. Clicks **Generate the rubric**.

Foundry then auto-generates a rubric across **eight different dimensions, each with different weights**, derived from the prompt + agent. She notes you can also **upload additional context files from your code**, and that everything done in the portal can equally be done **in code**. The payoff: evaluation is dramatically simplified because you see quality **across a whole set of dimensions inside a single evaluator**.

### Reading traces and root-causing a low score
Back on the agent, the reply comes back **contradictory** — it's unsure whether the vendor needs management, but still issues a recommendation — exactly the kind of thing worth investigating. Felicia opens the **Traces** view, which shows traces from **other query types** too because **continuous evaluations and jobs** have been set up: it **pulls production traces from Application Insights** and runs the previously-created evaluator against them, scoring each trace as it populates. Scores **vary by the kind of question** asked.

She spots a **low score**, clicks the **trace ID**, and gets a **rich trace view** showing the evaluations against the agent invocation. The detailed view reveals **both task completion and the vendor-history rubric score are low**. Switching to the **user view** to see what actually happened: the user asked a **very specific question** and the agent **lacked the exact data it was supposed to provide** (data the user explicitly referenced). Conclusion: the agent is **hallucinating** — claiming the vendor is "performing well" without giving the correct, context-grounded response. This demonstrates the full loop: trace → eval score → drill into the offending prompt → diagnose the failure mode.

### Recap 1 — open ecosystem + Azure Monitor + rubric GA status
The team recaps three things from Demo 1:
- **Open ecosystem support** (the exciting announcement): the tracing experience and evals-off-traces work for **Foundry *and* non-Foundry agents on any framework** — **LangChain, LangGraph, OpenAI SDK, Microsoft Agent Framework** — giving complete visibility into the full agent execution workflow plus eval signals straight from the traces.
- **Full-stack observability via Azure Monitor partnership**: inside Foundry you observe your **apps, agents, and all AI platform components**; all that data goes to **Azure Monitor** for a **full-stack view across all Azure resources, data, and infrastructure**; then that data is **read back into Foundry** for **centralized observability of all AI workloads**.
- **Rubric evaluator is now in public preview** — out-of-the-box *and* context-specific observability, for both the no-data (new agent) and existing-traces cases, usable offline and online.

### Demo 2 (Felicia) — code-first observability with the Foundry MCP + skill
Felicia moves from the portal to her **editor (VS Code)** to show **code-first** observability. She uses the **Foundry MCP server** and the **Foundry skill** to understand, analyze, and even **take actions on behalf of Foundry** from the developer environment.

**How to get access:** the Foundry MCP and Foundry skill are both packaged under the **Foundry toolkit**, a **VS Code extension**. (Roadmap: support for other coding agents and editors is coming; today it's the VS Code extension.)

She prompts **Copilot Chat inside VS Code** to fetch the **eval result** she'd hooked up earlier in the portal and explain **why the 0.4 score (pulled from the traces) is low** and **what the opportunities for improvement are**.

### What a Foundry "skill" is and why it's trustworthy
A **skill** is an **opinionated flow** authored by the Foundry team that encodes "here's how you should observe, analyze, and optimize your agent — the recommended loop." Because the skill knows **which part of the observability loop you're in**, it can suggest next steps, and it distinguishes whether an issue is a **client-side** or **server-side** problem, connecting both layers to recommend improvements. Critically, its analysis is **grounded in your repo context + the Foundry skill context**, which makes it **more trustworthy and actionable than dropping the result into a generic LLM**. It also means you **don't have to manually wade through hundreds of traces and eval results**.

### Reading the analysis and drafting a fix
Felicia shows a **previous run** (since the live one takes a moment): the same query she sent hours earlier, where the Foundry MCP retrieved the **evaluator definition + last run** and produced a **last-8-hour evaluation analysis** with a full summary. Because the whole team was testing the agent, it shows **everyone's evaluation runs** — with a **per-dimension breakdown** that calls out the **weakest dimension** (she jokes her runs did worse than Vivek's).

The key value: monitoring telling you "something's off" isn't enough — you need to know **what to do about it**. The skill gives a **detailed explanation of what went wrong, the patterns, and recommended improvements**, grounded so it's actionable. It recommends a **system prompt change** (with reasons) and how to **change the harness and evaluator**. She asks it to **"draft the system prompt,"** and it produces a **new system prompt** that, notably, addresses the **exact trace issue (the hallucinated vendor detail) via a metric-definition block**.

### Doing it at scale: traces back into datasets for regression-proofing
To move beyond one-off fixes, Felicia highlights that because Foundry is **all-in-one**, you can **pull traces back into your dataset**. This lets you **regression-proof** changes: a developer in the inner loop can run **locally-staged agent changes against that dataset**, then push the code to production with confidence. This is the concrete mechanism of the inner-loop ↔ outer-loop feedback.

### Recap 2 — code-first capabilities, multi-turn eval, user simulation, traces→datasets
The team recaps the code-first capabilities and announces several **additional public preview** features:
- **Code-first observability for Foundry agents** with the **skill-based guided UX**: run evaluations, **analyze** results, do **comparisons**, look at **traces**, and seamlessly transition to **optimization** — all available in **VS Code, GitHub Copilot Chat, and CLI**.
- **Multi-turn evaluation** (public preview): previously everything was **single-turn**; now you evaluate **across an entire session**. The motivating example: an agent might succeed at the end of a session, but if that session took **20 minutes when 5 was expected**, it's **not a successful session**.
- **User simulation** (public preview): **automatically generate realistic conversations** so that if you lack multi-turn data, you can still run your first multi-turn evaluation.
- **Traces → datasets with smart filtering**: feed production traces back into the inner loop to **improve test coverage**. Initial coverage only goes so far — **20 test cases won't cover everything you see in production** — so select traces and add them to your datasets.

### The evaluator catalog
Foundry ships a **comprehensive evaluator catalog** with **built-in evaluators spanning quality, risk, safety, and agent** evaluation. Several are now **multi-turn**: **groundedness, coherence, task completion, customer satisfaction**, and the **rubric evaluators** are also multi-turn. You can create **custom LLM-as-a-judge**, **code-based**, and **rubric** evaluators and make them multi-turn. Guidance: use a **variety** of evaluators — rubric for multi-dimension, but **custom/code-based evaluators are highly recommended for non-deterministic scenarios**. Example: for a **regex check** or a **database lookup**, use a **code-based evaluator** — you **don't need an LLM-as-judge** for that.

### Demo 3 (Vivek) — AI Agent Optimize
Vivek (handed off with "Thanks, Abishek") recaps the setup: a **working hosted agent**, a **dataset** of representative tasks the agent should do, and **rubrics** that score how good it is. The question: how do you **improve** it and **fix specific gaps** so it does well **across all tasks**? Answer: **AI Agent Optimize**, a new feature, shown live.

It opens with a **warning**: *optimization will create new versions of your agent*. This is the key behavior — it doesn't just **recommend** your next system prompt, it **deploys those versions**, **tries them across the tasks**, **assesses on rubrics**, and **iterates**: the prompt/context that works it **doubles down on**; what doesn't, it **tries another strategy**. It is **real, live, and iterative**.

**What it needs to start** (`eval.yaml`): a **hosted agent**, a **dataset** (here a **40-query dataset**), and an **evaluator** (the rubrics Felicia built). What it can **iterate on**:
- the **instructions file / system prompt**,
- **skills** (not configured for this agent, so skipped),
- **tool descriptions and parameter descriptions** (these go into the agent's context and affect tool use),
- optionally a **list of models** — it can recommend the **best-performing model** for your tasks. Why that matters: new models ship constantly with **cost/latency tradeoffs**, and you'd otherwise re-run evaluations many times manually across tasks; this finds the **best combination of model + prompt + tool definition + skills together**.

A separate **optimization model** is selected — distinct from the agent model — used by the optimization job to **self-reflect, read traces, read evaluation rubrics, and decide what to change**. A **better reflection model helps even if your agent runs a smaller model**.

### Optimization results: hill-climbing the agent
The live job can take **minutes to tens of minutes** ("I can walk my dog and get coffee"), so Vivek opens a **prior completed run** on the same agent Felicia used. Results:
- A **24% boost** over the base system prompt + tool definitions, **with just context engineering** — and **without** a human reading prompts/traces or spending evaluation time.
- Completed in **25 minutes**.
- It created **four candidates**:
  - **Candidate 1** — a system-prompt change making **38/40 tasks** work.
  - **Candidate 2** — system prompt + tools.
  - **Candidate 3** — tools.
  - **Candidate 4** — works **40/40 (all the time)**, raising the baseline score from **0.577 → 0.7**.
It **keeps trying new things and adjusting**: figuring out the right thing to change, trying it, learning, iterating, then suggesting new changes.

The **change view** shows the **system prompt rewritten** (grounded more on the traces, data, and rubrics) **and tool definitions changed** (the tool *description* changed). Crucially, the earlier **hallucinated vendor detail** is exactly what the optimizer **addressed**. You can drill into **score details** and see **real evaluation results** for that agent iteration — per-task, with **rubric details** explaining why each task was scored and an analysis.

**Not set-and-done:** you optimized on 40 tasks, but the agent does many more. You must **keep looking at traces** (smart filtering helps pick the right ones) and **keep hill-climbing** as users' queries, domains, models, and tool definitions/implementations change. **Agent Optimizer is now in private preview, public preview soon.**

### Demo 4 (Abishek) — Agent ROI: proving business value
The final step: once the inner and outer loops are set up, **how do you prove the business value** of your agents? You have to **do math** to decide whether agents generate enough value to justify their cost. The new **Agent ROI** feature (private preview, public preview soon) does this by looking at **all agent invocations** based on settings you specify:
1. In **settings**, enable the feature, **select an evaluator**, and **assign a business value** to that evaluator. *You* must do the math — Foundry doesn't have that info. Example: every time the vendor analyst **successfully completes its task** and gives an analysis, it **saves $5** of time vs. running the query / looking it up elsewhere — that's the business value generated.
2. In **optional settings**, the feature **automatically pulls in the token cost** of your agents. You then specify the **tool cost** (Foundry can't provide it; you **average it across invocations**).

Once enabled, you **track the net value** the agent generates **over time**. The demo shows **three different agent versions** and, over time, the **difference between value, cost, and net value**. A standout insight: the **tool calls actually cost more than the LLM** — something you could then optimize. At the bottom you see **how ROI changes across versions**.

A forthcoming capability: **drill into low-ROI traces**. The clearest example — an **agent invocation that just doesn't succeed** is **all negative cost**, so you'll want to drill in and use the **code-first capabilities** to **root-cause** what happened. **Agent ROI is now in private preview**, with **public preview soon** as feedback is collected; interested customers can engage via their **sales team** to try it and give feedback.

### End-to-end recap of the journey
The team ties the whole arc together:
1. **Build reliable agents** — test in the **playground**, create a **context-specific rubric evaluator**, look at **traces** and **eval scores**.
2. **Go to the IDE** — **code-first** debugging with the **Foundry toolkit + Foundry skills**.
3. **Optimize** — with **AI Agent Optimize**.
4. **Prove value** — the broader view via **Agent ROI**.
Foundry observability broadly covers the **tracing, evaluation, monitoring, and optimization** you need to **ship agents with confidence**.

### OpenTelemetry, monitoring depth, and single-shot optimization
Key capability emphases in the wrap-up:
- **Tracing**: Foundry **continues to invest heavily in OpenTelemetry** as the standard underpinning **both tracing and evaluation**. Microsoft engineers are **heavily involved in the open-source community** and are **contributing new semantics** — notably **new memory semantics** just contributed and **coming soon to Foundry**. This is a stated open-source commitment.
- **Evaluation**: beyond the rubric evaluator and built-in catalog, Foundry offers **red-teaming agents** and **CI/CD integration**.
- **Monitoring**: in addition to running evaluations in production, you get access to **all the operational metrics** needed to understand how your AI apps/agents are performing.
- **Optimization**: beyond the agent optimizer, there's also **single-shot optimization** as another option.

### Customer proof, labs, and the broader platform story
**NTT Data** is cited as a customer already using these observability capabilities — **Foundry together with Azure Monitor** — to transform AI into an **enterprise-grade, production-ready system**. There's a **hands-on lab** (takeable with you; everything available online). The closing platform framing: Microsoft provides the **building blocks for the agent platform** — **start building in GitHub**, get all the run/evaluate/optimize/**governance** capabilities **within Foundry**, and **distribute agents to users via M365 Copilot, Teams, apps, and APIs**.

### What's next (follow-on sessions)
The speakers point to upcoming sessions: a **breakout on A365** covering how Foundry observability **aligns with A365**; a **demo session** with more detail on the **interoperability story** (the any-framework story); and a **lightning talk** on **how Azure Monitor fits into the picture**.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — the AI platform providing the building blocks (agent service, models, knowledge, tools, fine-tuning) and the observability control plane.
- **Foundry Observability** — the four-pillar (tracing/evaluation/monitoring/optimization) observability suite for agents.
- **Tracing** — full end-to-end agent execution workflow capture; the substrate evals/monitoring/ROI/optimization read from.
- **Evaluation** — quality/safety assessment run off traces (offline and online).
- **Monitoring** — running offline evals online to catch issues in real time, plus operational metrics.
- **Optimization** — continuous improvement of agents from observability signals.
- **Rubric evaluator** — auto-generates a multi-dimensional, weighted evaluator (8 dimensions in demo) from your system prompt + agent; offline + online; multi-turn capable.
- **Evaluator catalog** — built-in evaluators across quality, risk, safety, agent; many multi-turn (groundedness, coherence, task completion, customer satisfaction).
- **Custom / code-based evaluators** — LLM-as-judge or deterministic code (regex, DB lookups) evaluators; recommended for non-deterministic checks.
- **Multi-turn evaluation** — evaluate across a whole session, not just single turns.
- **User simulation** — auto-generates realistic conversations to bootstrap multi-turn eval.
- **Traces → datasets (smart filtering)** — feed production traces back into the inner loop to grow test coverage.
- **Application Insights** — source of the production traces pulled into Foundry evals.
- **Azure Monitor** — partner platform for full-stack observability; receives Foundry data and is read back into Foundry.
- **Foundry MCP server** — lets you fetch evals/definitions/runs and take Foundry actions from the IDE.
- **Foundry skill** — an opinionated, loop-aware analysis/optimization flow grounded in repo + Foundry context.
- **Foundry toolkit** — the **VS Code extension** packaging the Foundry MCP server + Foundry skill.
- **GitHub Copilot Chat / VS Code / CLI** — surfaces where code-first observability is available.
- **AI Agent Optimize (AGD AI Agent Optimize)** — creates/deploys new agent versions and hill-climbs prompt/skills/tools/model against dataset + rubrics.
- **Single-shot optimization** — an alternative one-pass optimization option.
- **Agent ROI** — nets agent business value against token + tool cost to track net value/ROI per version.
- **OpenTelemetry (GenAI semantic conventions)** — the open standard underpinning tracing + evaluation; Microsoft contributing new memory semantics.
- **Red-teaming agents** — evaluation capability for safety/adversarial testing.
- **CI/CD integration** — wiring evaluation into pipelines.
- **Agent frameworks supported** — LangChain, LangGraph, OpenAI SDK, Microsoft Agent Framework.
- **IQ for knowledge / fine-tuning / agent service / models** — Foundry control-plane components observability spans.
- **M365 Copilot, Teams, apps, APIs** — agent distribution channels.
- **GitHub** — starting point for building agents in the platform story.

## 🚀 Announcements / What's New
- **Open ecosystem support** — trace + evaluate **non-Foundry agents on any framework** (LangChain, LangGraph, OpenAI SDK, Microsoft Agent Framework). (Announced as the exciting new capability.)
- **Rubric evaluator** — **now in public preview**. Auto-generates a multi-dimensional evaluator; works with no data or existing traces; offline + online.
- **Multi-turn evaluation** — **public preview**. Evaluate across an entire session.
- **User simulation** — **public preview**. Auto-generate realistic conversations to bootstrap multi-turn eval.
- **Traces → datasets with smart filtering** — **public preview** capability to feed production traces back into the inner loop.
- **Code-first observability for Foundry agents** (Foundry toolkit + skills in VS Code / GitHub Copilot Chat / CLI) — highlighted as newly available preview capabilities.
- **AI Agent Optimize** — **private preview now, public preview soon**.
- **Agent ROI** — **private preview now, public preview soon** (customers can engage via sales to try it).
- **OpenTelemetry memory semantics** — newly contributed to the open-source spec, **coming soon to Foundry**.
- **Hands-on lab** — available at Build and takeable with you; resources available online.

## 💡 Demos
- **Demo 1 — Getting-started evaluation (Felicia, portal):** Ran a query against the hosted vendor analyst agent in the playground (logs streaming live), created a **rubric evaluator** from scratch (8 weighted dimensions auto-generated), then used **continuous evals on production traces from App Insights** to find a **low-scoring trace**, drilled into the trace ID, and root-caused a **hallucination** (agent claimed a vendor was performing well without the requested data). *Proved:* you can evaluate trustworthiness across many dimensions and trace a bad score to the exact prompt.
- **Demo 2 — Code-first observability (Felicia, VS Code):** Used the **Foundry MCP + Foundry skill** via Copilot Chat to fetch the eval result, get a grounded **last-8-hour analysis** with per-dimension breakdown (showing the whole team's runs + weakest dimension), then had it **draft a new system prompt** that fixed the exact hallucination via a metric-definition block, and pulled traces back into a dataset to **regression-proof** changes. *Proved:* skill-grounded, repo-aware analysis turns monitoring signals into concrete, trustworthy fixes without reading hundreds of traces.
- **Demo 3 — AI Agent Optimize (Vivek, VS Code):** Configured `eval.yaml` (hosted agent + 40-query dataset + rubric evaluator), chose what to optimize (system prompt, tool definitions, model) and a separate reflection model, then reviewed a completed run: **4 candidates**, **+24%** via context engineering, **38/40 → 40/40** tasks, score **0.577 → 0.7** in **25 min**, with prompt + tool-description changes addressing the earlier hallucination. *Proved:* automated, iterative hill-climbing finds the best prompt/tool/model combo without manual trial-and-error.
- **Demo 4 — Agent ROI (Abishek, portal):** Enabled ROI, picked an evaluator, assigned **$5** business value per successful task, auto-pulled token cost + added tool cost, then tracked **net value across 3 versions** — revealing **tool calls cost more than the LLM** and that failed invocations are pure negative cost to drill into. *Proved:* you can quantify whether an agent is worth its spend and where to optimize cost.

## 📊 Notable Stats / Quotes
- **Four pillars**: tracing → evaluation → monitoring → optimization (the organizing model).
- Rubric evaluator generated **8 weighted dimensions** automatically.
- A flagged trace scored **~0.4** (low), traced to a hallucination.
- **AI Agent Optimize**: **+24%** boost via context engineering; **4 candidates**; **38/40** then **40/40** tasks; score **0.577 → 0.7**; **25 minutes**.
- Optimization dataset = **40 queries**; the all-pass candidate solved **40/40**.
- **Agent ROI**: **$5** assumed business value per successful task; **3 agent versions** tracked; insight that **tool calls cost more than the LLM**.
- “Agents are non-deterministic, creating new reliability and consistency challenges for developers and operators.”
- “We continue to invest heavily in OpenTelemetry as the standard that underpins both tracing and evaluation… we just contributed new semantics for memory.”
- “If you have 20 test cases, that's not going to cover everything that you see in production.”
- “It's worth the cost that you're spending on your agent workloads… you have to do math.”
- Customer: **NTT Data** using Foundry + Azure Monitor for an enterprise-grade, production-ready AI system.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Enable Foundry tracing + rubric evaluator on a non-Foundry agent (LangGraph / OpenAI SDK) and confirm evals run off the OTel traces; wire continuous evals against App Insights traces; install the **Foundry toolkit** VS Code extension and drive the Foundry MCP/skill from Copilot Chat; pilot **AI Agent Optimize** on a small (~40-query) dataset + rubric; stand up **Agent ROI** with a real $-per-success value and compare token vs tool cost.
- [ ] Questions: Which OTel GenAI semantic conventions are covered today vs. coming (esp. the new **memory** semantics)? How does the Azure Monitor ↔ Foundry round-trip bill (data egress/ingestion)? What model families can the optimizer recommend across, and what are the private-preview access criteria for **Agent ROI** / **AI Agent Optimize**? How is tool cost averaged — manual only, or any assist?
- [ ] Relevant to: Any team running production agents who needs reliability + cost/quality proof; platform/observability owners standardizing on OpenTelemetry; FinOps for AI workloads; framework-agnostic agent teams (LangChain/LangGraph/OpenAI SDK/Microsoft Agent Framework).

## 🔗 Related
- [[BRK241 - Developing production agents]] — the companion session whose data-center vendor scenario this builds on
- [[ODSP933 - Agentic infrastructure needs agentic observability]] — sibling take on why agents demand purpose-built observability
- [[ODSP907 - Monitor GenAI applications beyond golden signals]] — deeper monitoring angle for GenAI apps
- [[Microsoft Foundry]] — the platform hosting agents, evaluation, optimization, and observability
- [[OpenTelemetry GenAI semantic conventions]] — the open standard underpinning Foundry tracing + evaluation
- [[Azure Monitor]] — full-stack observability partner that round-trips data with Foundry
- [[AI agent evaluation]] — rubric / multi-turn / code-based evaluators and the evaluator catalog
- [[Agent DevOps inner loop and outer loop]] — the lifecycle model this session is organized around
- Source list: [[2026 Build Session List]]


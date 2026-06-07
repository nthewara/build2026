---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai-foundry
  - topic/model-router
  - topic/cost-optimization
  - topic/evals
  - topic/fine-tuning
  - topic/ai
  - topic/models
source: https://www.youtube.com/watch?v=05naxQpKqaU
session_code: BRK230
event: Microsoft Build 2026
speakers: Yina (Product Lead, Microsoft Foundry), Naomi (Models, Microsoft Foundry)
duration_min: 46
aliases:
  - Build smarter AI systems in Foundry as models and costs evolve
---

# BRK230 — Build smarter AI systems in Foundry as models and costs evolve

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Yina (leads product for Microsoft Foundry) · Naomi (ships the models in Microsoft Foundry) · Demos built by Nthia (credited)  
> **Duration:** ~46 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=05naxQpKqaU)

## 🎯 TL;DR
A year ago, building an AI app was simple: pick a model, wire it up, ship. Now you're building long-running **agentic systems** that must continuously improve while the landscape — models, tools, context, costs — keeps shifting underneath you. This session argues that durability comes not from a better prompt or a newer model, but from **building a system** on a governed platform (Microsoft Foundry) that decouples your solution from any single model. The core mental shift: **stop QA-ing at the end — shift left to define your success criteria and evals first**, then "hill climb" toward your target. Using a worked **trip-planning app** demo, Yina and Naomi walk a baseline (single GPT-4.1 model = "a Ferrari for a grocery run", quality 0.59 vs target 0.8) through four optimization stages — **Select → Evaluate → Optimize → Scale/Operate** — applying decomposition, the **model router** (28 models, now with governance policies), custom & new **rubric-based evals**, **explicit prompt caching** (Azure context cache you own), and **distillation/fine-tuning** (GPT-4.1-nano fine-tune hit target quality at low cost). Key announcements: **Claude now runs on Azure on GB300s** (Opus 4.8 in catalog), **Microsoft first-party models live** (incl. image 2.5), **rubric-based evaluators**, **explicit prompt caching (private preview)**, **model-router governance policies**, **serverless RL fine-tuning API**, and **Fireworks GA** on Foundry. Catalog now exceeds **11,000+ models**. The throughline: it's not about model choice, it's about the **entire platform** — build smarter systems as models and costs keep evolving.

## 🔑 Key Takeaways
- **Build the system, not the prompt.** "Long gone are the days of just prompt engineering." Durable AI solutions decouple from the model, the tools, and the context — all of which keep evolving around you.
- **Shift left: evals first, not QA last.** The one thing to take from the session — define success criteria and evaluation *before* you build, so you can continuously improve. Evals become your product spec; as you hill-climb, your evals/data/criteria become your **IP**.
- **"Hill climbing"** is the operating loop: set a baseline → measure honestly → decide where the next gain comes from → repeat. Demo started at quality **0.59**, target **0.8**.
- **Don't use one frontier model for every task** — that's "a Ferrari for a grocery run." Decompose the workflow into jobs-to-be-done and pick the right model per task (microservices-architecture thinking for AI).
- **Model choice is by task, not by app** — an ongoing systems decision because the model lifecycle keeps accelerating.
- **Model router** auto-analyzes each prompt and routes to the best model: supports **28 models** (GPT-4.x, GPT-5.5 family, Claude, OSS), with **automatic failover** and **agentic support**; **NEW today: governance policies** to restrict which models the router may use. Roadmap: customizable/fine-tunable router + bring fine-tuned models.
- **DIY router alternative:** use a small model (e.g. **GPT-4.1-nano** or **Mistral Small**) with rules to route intent to job-specific models.
- **Benchmarks don't decide for you.** "Evaluate on your workload, not the beautiful benchmarks." The answer comes from your data/scenario.
- **Three model-selection questions:** (1) Capability — can it do the job at all? (2) Production bar — latency/cost good enough for prod? (3) Affordability — can you run it at scale?
- **NEW: rubric-based evaluators** — Foundry analyzes your agent definition + sample trajectories and auto-generates weighted rubric dimensions (demo produced **7 dimensions**); editable weights; plus cluster analysis of failures (hallucination, inadequate final answer).
- **Cost reduction rarely comes from a cheaper model — it comes from architecture.** Stack levers: routing by workload, batch inference, async jobs, structured outputs, caching, distillation. Gains **compound**.
- **NEW: explicit prompt caching (private preview)** via **Azure context cache** — *you* own the cache (not the inference provider); better privacy controls and operational availability for long-running tasks.
- **Latency is engineered, not hoped for:** route to faster models, reserve capacity (PTU), priority processing ("toll road"), prompt caching, predicted/structured outputs, tighter token budgets, streaming for perceived speed, API gateways for regional traffic.
- **Quality levers progress lightweight → heavyweight:** start with **prompt design** (cheapest/fastest), then grounding (retrieval/tools), then **fine-tuning/distillation**, then custom domain model training. Don't jump to the heaviest first.
- **Distillation + fine-tuning embedded the travel policy into the model:** a bigger teacher model taught a smaller student; a fine-tuned **GPT-4.1-nano (v1.2)** reached target quality while keeping cost low.
- **Foundry post-training spectrum:** managed fine-tuning (SFT / DPO / RL, easiest, highest success for non-ML folks) → **NEW serverless RL fine-tuning API** (control rewards/hyperparameters, produces LoRA weights, no cluster mgmt) → full-control RL (own code/algorithms/GPU clusters; frameworks like **slime**, **veRL**). Start simplest, move right as needed.
- **Operate with discipline = observability:** tracing (end-to-end prompt/tool visibility) + evaluation (quality/safety/agent behavior) + monitoring (Azure Monitor for real-time cost/latency). Copilot can suggest fixes in-portal (e.g. "how do I improve time-to-last-byte?").
- **Announcements:** Claude on Azure (GB300s, Opus 4.8), MS first-party models live (image 2.5), rubric evals, explicit prompt caching (private preview), router governance policies, serverless RL API, **Fireworks GA**, Aurora 1.5 (geospatial/weather), expanded Nvidia partnership (Nemotron, Cosmos, Earth-2).
- **Catalog scale: 11,000+ models**; the Foundry value prop spans Select → Scale → Optimize → Operate (security, compliance, rollback, CI/CD via GitHub) — "it's not about model choice, it's the entire platform."

## 📚 Detailed Notes

### The problem: the landscape keeps evolving under you
Yina opens by framing the shift every AI team faces: you build a system and the world around it keeps moving — the models, the tools, the surrounding capabilities. A year ago, building an AI app felt simpler: pick a model, wire it up, ship it. But teams are no longer building chat apps — they're building **full agentic systems**: long-running systems that have to continuously improve. Three pain points she sees in *every* developer:
1. **Picking the right model is hard.** Many models, more arriving daily; benchmarks look great on paper but don't tell you if a model is good for *your* scenario.
2. **Costs are hard to predict.** You can analyze during build, but the production bill is "painful."
3. **It never stops.** The moment you ship, the next model and next tool drop, and you must keep changing the system as the landscape moves.

What you want: a system that is **simpler, better, more cost-effective, and scalable** into production, giving the best outcome for *your* scenario.

### The thesis: build a system on a governed platform, not a better prompt
The fix is **not** a better prompt, a newer model, or the latest MCP tool. It's **a system that continuously improves over time** plus a platform that spans building → governing → managing at scale. Yina sketches the end-to-end Foundry stack:
- **Build** with GitHub Copilot CLI.
- **Ground** with your organization's knowledge: productivity data in **Work IQ**, structured data in **Fabric IQ**, agent context/knowledge via **Foundry IQ**, and the world's knowledge via **Web IQ**.
- **Run** in Foundry using **Foundry-hosted agents**.
- **Govern** with **H365** (Microsoft 365 / agent governance).
- **Improve over time** with Foundry's platform capabilities.

Foundry is positioned as the platform that brings together models, agent service, grounding, tools, and post-training capabilities — **fully governed for the entire agentic lifecycle**, not just inferencing or a single point solution. You build, deploy, operate at scale, and continuously improve.

### The core mental shift: shift left from QA to evals
**If there's one thing to take from the session:** evolve how you think about QA-ing solutions. Old model: "I'll build it, then think about QA at the end." New model: **shift left** — define your **success criteria and evaluation first**, so you can then continuously improve and build a resilient solution that **decouples from the model evolving, the tools changing, and the context evolving**. That's how you build something "ready for the test of time." Once evals are defined, they reveal the **set of levers** you can pull to optimize. The talk is structured around the optimization categories: **Selection → Evaluation → Optimization → Scaling**, organized around the model ecosystem (with other conference sessions going deeper on the agentic side and post-training).

### Select — Foundry models as your raw materials
Naomi takes Select. Lots and lots of models are available in Foundry — building on the morning keynote announcements. Every AI system "belongs with selecting models," but the framing is **model choice by task**, an **ongoing systems decision**, because the model lifecycle is continuously accelerating. Models are your **raw materials** — but what matters is whether it's the **right model for the job**, not the model itself. With Foundry models, developers can **access, explore, compare** across the catalog with a **consistent API** and built-in **enterprise curation**, enabling faster experimentation, faster path to production, and quick redeployment as requirements change.

Flagship/partner highlights on the slide:
- **OpenAI** and **Anthropic** flagship models.
- A special call-out to the **Hugging Face** partnership (shout-out to "Jeff" in the room) — they populate much of the catalog; "we love our OSS models."
- **Nvidia** mentioned from the morning keynote.

### Claude on Azure (GB300s) and Microsoft first-party models
- **Claude:** **Opus 4.8** launched last week into the Foundry catalog. **Announcement: Claude is finally running on Azure**, on **GB300s** (highest-end hardware), bringing the full Anthropic lifecycle and dev tools directly from Azure. (Crowd was warm — "one person at least was excited about Claude.")
- **Microsoft AI models:** Announced in the keynote with **Mustafa**, several first-party models went **live that morning** ("my team just pushed them"). Foundry isn't just the platform — Microsoft is also bringing **first-party models** running efficiently with strong **cost-optimization** scenarios. **image 2.5** called out as one of the latest — a full **multimodal application stack** spanning thinking, image, code, and audio models.

### Strategy: innovate across the full AI spectrum (11,000+ models)
Foundry strategy = innovate across the full spectrum:
- **Production-grade frontier models** — usable quickly inside apps under strict operational requirements.
- **Cutting-edge / experimentation** — research-grade exploration, e.g. **Foundry Labs**: a new set of capabilities primarily from **Microsoft Research**, the latest/greatest pieces, a place to build models with confidence and explore future frontiers.

Catalog scale: **11,000+ models**, with more coming.

### The shift to purpose-built models
It's not one reasoning/frontier model for all use cases — there's a shift toward **purpose-built, domain-specific models**. Not every problem warrants the same general-purpose model. Domains called out: **geospatial, robotics, biomedical, material science, code, search, media**. Developers should design the system to apply the right domain model per area. Specific call-out: **Aurora 1.5** (geospatial) — an "amazing weather modeling system" using satellite imagery + atmospheric data that scales where traditional models can't.

### Expanded Nvidia partnership — into physical AI
Foundry is expanding the **Nvidia** partnership with additional models: **Nemotron** reasoning models, **Cosmos** for physical AI, and new Nvidia **AI weather models like Earth-2**. These let developers build systems that **reason, act, and respond to real-world conditions** — going beyond software workloads into **physical AI**. A **pre-recorded session with a "very cool" physical-AI demo** is recommended. Together with Nvidia, Foundry enables a **unified platform** to build, run, and scale AI systems spanning into the physical world.

### The Foundry portal — leaderboards, comparison, save-as-agent
Yina gives a portal tour:
- See **all models and providers**; a **leaderboard** benchmarking across **quality, safety, throughput, and cost** dimensions, with **trade-off charts** to select by your priorities.
- **Compare models** across providers (open-source vs closed) across benchmarks, and run **side-by-side** on a given set of prompts to see latency and responses — great for prototyping.
- **Save as an agent:** unlocks new capabilities — add **tools, knowledge, memory, guardrails**, and set **metrics**. In the demo she set **task adherence, intent resolution, relevance** as out-of-the-box metrics; Foundry then **evaluates every time the agent is invoked**.
- Running a request produces a **trace** with **spans** (duration per turn), the **evaluation outputs**, **LLM-as-a-judge** pass/fail, and **verbatim** on what happened during the call.

### The running scenario: a trip-planning app
The session uses a **trip-planning app** as a typical enterprise scenario: understand intent → make decisions based on prompts → produce output for the user. The key takeaway repeated: **start with what success looks like** — success criteria across **correctness, compliance, user behavior**, and what you'll use in production. This introduces **hill climbing** (also shown in the keynote): with a clear success criteria you can continuously improve. The standard developer workflow: have a scenario → understand success → **prototype with the latest/greatest model** to establish a **baseline**. All demo code is in a GitHub repo (aka.ms link), built **with agents** so you can try it yourself; they show outputs rather than deep code. Gratitude to **Nthia**, the "mastermind behind all of the demos."

### Establishing the baseline — one model for everything (the anti-pattern)
Naomi runs the baseline: take **GPT-4.1** and apply it to **every task**. Start with a small seed dataset (**~20 seed rows**) — you're prototyping. The **scorecard** is honestly "not great": **quality** is well below target, **cost per task** is "pretty expensive," **latency** is "not bad." Quality here uses **out-of-the-box evaluators** (task adherence, task completion); domain-specific evals come later. The big problem: **one frontier-ish model for every job**, including cheap ones — **"a Ferrari for a grocery run."** Reality check on the hill climb: target **0.8**, baseline **0.59** — and that gap tells you where to go. The job is **not to guess** but to proceed **methodically**: baseline → measure honestly → decide the next gain.

### Decomposition — the first optimization move
An employee travel request looks simple but should be **decomposed into distinct tasks** (jobs-to-be-done). For each job, use the **right model** — don't overbuild each step. Choose the right **prompt, model, tool, and context** per job. Yina's framing: think **microservices architecture** — don't use a single model for everything; break it apart, and for each job optimize the model you use. **Smaller models = faster + cheaper**, more room for cost optimization.

### Routing — the model router vs DIY router
Two ways to route once decomposed:
1. **Model router** (simplest): automatically analyzes each prompt and routes to the best model. Foundry's router supports **28 models** (incl. **GPT-4.x**, **GPT-5.5 family**, **Claude**, **OSS** models), with **automatic failover** to improve customer experience and **agentic support**. **NEW today:** ability to **govern the policies** of which models the router may use — so from a governance standpoint you can auto-select only approved models. **Roadmap:** open up the ability to **customize/fine-tune the router itself** and **bring in fine-tuned models**.
2. **DIY router:** build it yourself with a **small intent-routing model** — e.g. **GPT-4.1-nano** or **Mistral Small** — given a set of rules describing scenarios/jobs, routing to job-specific models.

### Routing in action — synthetic data + improved scorecard
Demo of the **simple router**: it decomposes tasks, examines **intent**, and recommends a model **per task** (optimizing for quality here). Then **synthetic data generation** in Foundry scales the dataset: **20 seed rows → 170 synthetic rows**, of which **50** are sampled and run. Re-running the eval against the **multi-model router** vs the single GPT-4.1 baseline shows **cost per task significantly improved** (down to target range), with **latency** still an area to work on.

### Model selection — the three questions + "evaluate on your workload"
Model selection comes down to three questions:
1. **Capability** — can it even do the job at all?
2. **Production bar** — latency and cost good enough for production?
3. **Affordability** — can you afford to run it at scale?

Benchmarks **help** you understand direction but **shouldn't make the decision for you**. The decisive principle: **"Evaluate on your workload, not the beautiful benchmarks."** The answer comes from your scenario/data.

### Evaluate — evals are your product spec and your IP
Yina: benchmarks won't drive model selection — **how you evaluate on your data** should. Foundry ships an extensive **evaluation catalog**. Key reframes:
- In the improvement loop, **evaluations become your product spec**.
- As you hill-climb, the **evaluations become your IP** — your data, success criteria, and definition of "good" live here; they define which trade-offs matter and are the **measuring stick for every change** — whether a change you make *or* one you must react to (e.g. **model lifecycle**: a model is removed from the catalog, so you must continuously re-run evals as you swap components to confirm expected behavior).

For the trip planner, eval dimensions include **correctness**, **policy compliance** (companies have travel policies — max $/day, business class only if trip > 7 hours, etc.), **tool-call validity**, **escalation accuracy** (when to escalate to a human vs not), and **safety/privacy**.

### Evaluator types in Foundry — built-in, custom, and NEW rubric-based
- **Built-in evaluators:** **quality** (e.g. intent adherence), **risk & safety**, and **agentic** evaluators (whether the solution follows correctly across multiple turns).
- **Custom evaluators:** **prompt**, **code**, and — **announced today** — **rubric-based** evaluators.

**Rubric-based eval demo:** in the evaluation catalog, create an evaluator → choose **rubric / prompt / code**. With **rubric**, select an agent; Foundry **analyzes the agent definition + seed trajectories** (takes a moment) and **auto-generates rubric dimensions across multiple axes**. For the **concierge starter agent** (the travel agent), it generated **7 dimensions**. You can **edit weights** (e.g. bump policy compliance from weight 5 → 8) and re-run. Results show per-dimension successes/failures plus a **cluster analysis** across evaluators — revealing where the agent **hallucinated** or **didn't produce an adequate final answer** — so you can drill into system behavior. Everything in the UI is also available **in code**.

### Custom policy evaluator — why generic judges aren't enough
Demo of the **travel policy** (a **skill file** grounds the rubric). A **generic LLM judge** looks at **answer quality**, but the scenario needs a **five-axis rubric**. Re-running both agents with all three evaluators produces a scorecard: **policy adherence** improved with the multi-model router but **still missed target** — the generic LLM judge couldn't handle policy on its own. Important call-out (Yina): baseline evaluators said "about halfway there," but checking **policy adherence** specifically showed it wasn't following the travel policy — so they had to build a **custom evaluator specific to the travel policy**. The lesson: your **quality definition** is critical and **may shift over time** as you learn more about the scenario.

### Optimize — the biggest wins come from architecture, not cheaper models
Naomi opens Optimize: this is where the **biggest wins** live, across the whole application. Crucial: **cost reduction rarely comes from choosing a cheaper model** — "I see customers doing this all the time." It's about **architectural decisions**. Optimization is the **hill climb** across multiple dimensions (cost, quality, latency) — not just pushing on cost. It's **iterative**: start with **prompt improvements**, then **better context**, then **decomposition/routing** (as shown), then **deeper architectural latency levers**. The goal isn't a perfect endpoint — it's making the **system operate measurably faster and better with every choice**.

### The full stack of cost levers — gains compound
When teams talk AI cost (Naomi: ~three-quarters of the room thinks about cost; "the rest of you are obviously ballers"), the instinct is to ask for a cheaper model — but the biggest wins come from **system design**. Foundry's full stack of levers:
- **Routing by workload**
- **Batch inference** (can save a lot of money)
- **Async jobs**
- **Structured outputs** (avoid wasted tokens)
- **Caching** (avoid repeated work)
- **Distillation** (brings down cost)

The point: gains **compound** — there's no single magical fix; you need an **architecture** that lets you **stack** optimizations.

### Explicit prompt caching — Azure context cache that YOU own (private preview)
Caching has evolved from low-level **implicit caching** toward a richer set of caching capabilities. **Announcement: explicit prompt caching** — a new service treating caching as a **core system capability** of the AI platform: not just one lever, but understanding not just *where the request lands* but **delivering consistent, guaranteed performance** and the savings you need. The differentiator: **Azure context cache** — it is **not owned by us (the inference provider); it is owned by you**. It's *your data*; you can see your deployments and your savings. Benefits: **better privacy controls** and **better operational availability across long-running tasks**. **Available in private preview today.**

### Latency — engineered, not hoped for
Latency isn't about picking a faster model — it's about **designing a faster system**, improving responsiveness at multiple stages:
- **Route each task to a faster model** (as demoed).
- **Reserve capacity** with **PTU** for consistency under large workloads.
- **Priority processing** — a "toll road" for low-latency when you need it.
- **Prompt caching** to remove wasted work.
- **Predicted outputs**, **structured outputs**, and **tighter token budgets**.
- **Streaming** for perceived speed.
- **API gateways** to optimize traffic across regions.

The premise: **production latency is engineered for**, not something you hope and wish for.

### Quality levers — lightweight → heavyweight
When quality is the constraint, there's a **progression** of levers from lightweight to heavyweight:
1. **Prompt design** — always start here (fastest, cheapest).
2. **Grounding** — retrieval / tool use.
3. **Fine-tuning & distillation** — when you need to go stronger.
4. **Custom domain model training** — for highly specialized domains.

Key: **don't jump to the heaviest solution first** (tempting, but don't). Start with prompts, move along the spectrum as needed, and **incrementally stack** the benefits. (Yina notes a **full session on agent optimization** that shows automatically analyzing your agent, optimizing prompts, and optimizing tools — recommended.)

### Distillation + fine-tuning — embedding the travel policy into the model
To fix the **travel-policy adherence** gap, they deliberately start with the *heaviest* lever (the model): use **distillation + fine-tuning** to **embed the travel-policy knowledge into the model**. Approach: take a **bigger teacher model** and **teach a smaller student model**, preserving the cost optimization they want. In Foundry, **fine-tuning is simple** — supervised fine-tuning, **preference optimization (DPO)**, and **RL**, all as a **managed service** (a few clicks in the UI or a few lines of Python). Flow: select **endpoint** → select **dataset** → choose **base model** + **training model** → in **under ~100 lines of code**, the job is ready to submit.

**Result:** they ran the training, then deployed into a **developer tier** — a cheap way to try multiple fine-tuned models and test against your data. Versus prior runs, the fine-tuned **GPT-4.1-nano (v1.2)** got **all the way up to the target quality** for the scenario in a **single simple fine-tuning run**. The Foundry fine-tuning experience also shows the **loss curve** and **token accuracy**; you can **continuously fine-tune** as new trajectories arrive, with **checkpoints** you can inspect and bring in.

### Foundry post-training spectrum — managed → serverless RL → full-control RL
Foundry offers multiple ways to post-train models:
- **Managed fine-tuning** (what was demoed) — the **simplest**: bring your data, Foundry handles **data prep, training, monitoring, deployment**. **Highest likelihood of success** if you're not an ML professional/data scientist; very low effort; pick **SFT / DPO / reinforcement fine-tuning**.
- **Serverless API (NEW at Build)** — you control **rewards and hyperparameters**; Foundry handles infrastructure. Produces a set of **LoRA weights** overlaid on top of deployments; **no cluster management**.
- **Full-control RL** — full ownership of the **code, distributed strategies, algorithms, GPU clusters**; Foundry manages compute and orchestration. Use frameworks like **slime** or **veRL** for training.

Recommendation: **start at the simplest**, see what you get (you have the evals to judge), and **move right as your scenario demands**.

### Running customized & open models — Fireworks GA, managed compute, Hugging Face
Once you have a customized model, you bring it into Foundry and run it:
- **Open-source models:** use **Foundry managed compute**, or the **Fireworks** partnership (**announced GA today**) — or deploy on your own compute clusters.
- **Fireworks GA on Foundry** brings customers **zero-day access to optimized frontier models**, **best-in-class inferencing performance**, and **native Azure integration** for an enterprise foundation. Key differentiator vs Fireworks directly: deep integration across Azure's **enterprise stack**.
- **Managed compute in Microsoft Foundry** for teams standardizing on open models wanting broad selection — where the **Hugging Face** partnership shines (thousands of models from Hugging Face, Nvidia, Microsoft Research). Use optimized runtimes (**vLLM**, **SGLang**, **Nvidia NIM**); Foundry manages accelerators; bring your own capacity; **same API endpoints, same SDK**, no separate management.

### Operate — observability with discipline
Once **selection, evaluation, and optimization** are done, the next challenge is **operating with discipline**, which means **observability**. Taking something from prototype to production makes observability critical. Three pillars:
- **Tracing** — end-to-end visibility across prompts and tools.
- **Evaluation** — quality, safety, and agent behavior.
- **Monitoring** — via **Azure Monitor**, real-time signals for **cost** and **latency**.

Build observability into your loop **straight away**. Demo: in the Foundry portal you can inspect these directly — picking **time-to-last-byte** and asking **Copilot "how do I improve this?"** surfaces guidance **in-portal**.

### Take it home — the recap
Yina closes: across the end-to-end scenario, every step improved quality — the **hill-climbing** notion from the keynote. The recap:
- **Start with your evals** — the definition of success; Foundry helps with the new **rubric-based** capabilities (bring code, bring prompts, or let Foundry build the rubrics).
- **Build the system, not just the prompt** — "long gone are the days of just prompt engineering."
- **Pick the best model for the workload**; **decompose** scenarios (microservices-architecture thinking); **evaluate on your particular scenario**.
- Use the full set of **optimization levers** across **quality, latency, cost**; your scenario understanding becomes your **IP**.
- **Operate with control** — monitoring, versioning, governing, rollback, fully integrated into **CI/CD** (GitHub integration).
- **Continuously improve** so solutions not only meet the goal but **keep meeting it** as everything changes around you.

### The Foundry value proposition
Stepping back: the value prop is **Select → Scale → Optimize → take global / handle changing demand → iterate → keep control (security, compliance, operations)**. "It's **not about model choice** — it's about the **entire platform value** that Foundry delivers," giving a way to **build smarter systems as models and costs keep evolving**. Closing pointers: more sessions on **post-training**, **agentic solutions**, and **safety/responsible AI**; remember **ai.azure.com** ("AI.asher.com" in the captions); use the **session-code aka.ms link** for all the demo code; and join the **active Discord community**.

## 🛠️ Products / Features / Technologies Mentioned
- **Microsoft Foundry** — the governed platform for the entire agentic lifecycle (build, deploy, operate, continuously improve).
- **Foundry model catalog** — **11,000+ models**, consistent API, enterprise curation, leaderboard (quality/safety/throughput/cost), trade-off charts, side-by-side compare.
- **Model router** — auto-routes prompts to the best of **28 models**; automatic failover; agentic support; **NEW governance policies**; roadmap for customization/fine-tuning.
- **Foundry evaluation catalog** — built-in (quality, risk & safety, agentic), custom (prompt, code), and **NEW rubric-based** evaluators; cluster analysis of failures.
- **Save-as-agent** — add tools, knowledge, memory, guardrails, metrics; auto-eval on each invocation; traces with spans + LLM-as-a-judge + verbatim.
- **Synthetic data generation** — expand seed data (20 → 170 rows demo) for testing.
- **Explicit prompt caching** / **Azure context cache** — customer-owned cache (private preview).
- **Managed fine-tuning** — SFT, DPO, reinforcement fine-tuning; loss curve, token accuracy, checkpoints; **developer tier** for cheap testing.
- **Serverless RL fine-tuning API** (NEW) — control rewards/hyperparameters; LoRA weights; no cluster mgmt.
- **Full-control RL** — own code/algorithms/GPU clusters; frameworks **slime**, **veRL**.
- **Foundry managed compute** — run open models; runtimes **vLLM**, **SGLang**, **Nvidia NIM**; same API/SDK.
- **Observability** — tracing, evaluation, monitoring (**Azure Monitor**); Copilot in-portal assistance.
- **Grounding IQ stack** — **Work IQ**, **Fabric IQ**, **Foundry IQ**, **Web IQ**.
- **Foundry Labs** — cutting-edge capabilities from **Microsoft Research**.
- **Foundry-hosted agents**, **GitHub Copilot CLI**, **H365** governance, **PTU** reserved capacity, **priority processing**, **API gateways**, **CI/CD via GitHub**.
- **Models named:** GPT-4.1, GPT-4.1-nano, GPT-5.5 family, Claude **Opus 4.8**, **image 2.5**, **Mistral Small**, **Aurora 1.5** (geospatial/weather), Nvidia **Nemotron** / **Cosmos** / **Earth-2**.
- **Partners:** OpenAI, Anthropic, Hugging Face, Nvidia, **Fireworks** (GA).
- **Resources:** **ai.azure.com**, session-code **aka.ms** code repo, Discord community.

## 🚀 Announcements / What's New
- **Claude on Azure** — Anthropic Claude now **runs on Azure** on **GB300s** (highest-end hardware); **Opus 4.8** launched last week into the Foundry catalog. *(GA-style availability in catalog.)*
- **Microsoft first-party models live** — several models announced in the keynote with Mustafa went **live that morning**, including **image 2.5**; full multimodal stack (thinking/image/code/audio). *(Live/GA.)*
- **Rubric-based evaluators** — **announced today**; auto-generate weighted rubric dimensions from an agent definition + trajectories. *(New capability; appears available in portal — GA/preview status not explicitly stated.)*
- **Explicit prompt caching (Azure context cache)** — customer-owned cache; **private preview today**.
- **Model-router governance policies** — **starting today**, govern which models the router may use. *(New.)*
- **Serverless RL fine-tuning API** — **launching at Build**; control rewards/hyperparameters, LoRA weights, no cluster mgmt. *(New — launch status; preview/GA not explicitly stated.)*
- **Fireworks on Foundry — General Availability (GA)** — zero-day access to optimized frontier models, best-in-class inferencing, native Azure integration.
- **Aurora 1.5** — newest geospatial/weather modeling model (satellite imagery + atmospheric data).
- **Expanded Nvidia partnership** — additional models: **Nemotron** reasoning, **Cosmos** (physical AI), **Earth-2** AI weather. *(New/expanding.)*
- **Foundry Labs** — new set of cutting-edge capabilities from Microsoft Research. *(New.)*
- **Roadmap (not yet shipped):** customizable/fine-tunable **model router** + bringing fine-tuned models into the router.

## 💡 Demos
- **Foundry portal tour** — model catalog, leaderboard, trade-off charts, side-by-side model comparison on shared prompts; **save-as-agent** with task adherence/intent resolution/relevance metrics; live **trace** with spans, LLM-as-a-judge pass/fail, and verbatim.
- **Baseline (anti-pattern)** — single **GPT-4.1** applied to every task in the trip-planning app; ~20 seed rows; scorecard “not great”: quality below target (**0.59** vs **0.8**), cost-per-task expensive, latency okay. (“Ferrari for a grocery run.”)
- **Decomposition + simple router** — break the employee travel request into jobs-to-be-done; router examines intent and recommends a model per task; **synthetic data 20 → 170 rows**, sample **50**, re-run eval → **cost-per-task significantly improved**; latency remains to optimize.
- **Rubric-based evaluator** — on the **concierge starter agent**, Foundry analyzed the agent + trajectories and generated **7 rubric dimensions**; edited a weight (policy compliance 5 → 8) and re-ran; results + **cluster analysis** showing hallucinations / inadequate final answers.
- **Custom policy evaluator** — travel-policy **skill file** grounds a **five-axis rubric**; generic LLM judge alone insufficient; re-run shows policy adherence improved with the router but still under target.
- **Distillation + fine-tuning** — teacher → student; fine-tuned **GPT-4.1-nano (v1.2)** deployed to a **developer tier**; reached **target quality in one simple run**; Foundry shows **loss curve**, **token accuracy**, and **checkpoints**.
- **Observability** — Foundry portal metrics; pick **time-to-last-byte** and ask **Copilot “how do I improve this?”** for in-portal guidance.
- **Pre-recorded physical-AI demo (Nvidia)** — referenced/recommended (not shown live).

## 📊 Notable Stats / Quotes
- **11,000+ models** in the Foundry catalog.
- **Model router supports 28 models** with automatic failover.
- **Baseline quality 0.59 → target 0.8** (the hill-climb gap).
- **Synthetic data: 20 seed rows → 170 generated → 50 sampled.**
- **Rubric auto-generated 7 dimensions** for the concierge agent.
- **Fine-tune job ready in under ~100 lines of code.**
- Claude runs on **GB300s** (highest-end hardware).
- **~3/4 of the room** said they think about AI cost.
- > “We used a **Ferrari for a grocery run**.” — on using one frontier model for every task.
- > “**Evaluate on your workload, not the beautiful benchmarks.**”
- > “In the improvement loop the **evaluations become your product spec**… as you’re hill climbing the **evaluations become your IP**.”
- > “Build the **system, not just the prompt**. Long gone are the days of just prompt engineering.”
- > “Cost reduction in AI **rarely comes from just choosing a cheaper model** … it is about the **architectural decisions**.”
- > “The Azure context cache … is **not owned by us, the inference provider — it is owned by you**.”
- > “Production latency is **engineered for**. It is not something you just hope and wish for.”
- > “It’s **not about model choice** — it’s about the **entire platform value**.”

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Clone the session repo (session-code **aka.ms** link) and run the **trip-planning** hill-climb end-to-end on a real workload.
  - Stand up the **model router**, enable the **NEW governance policies** to restrict to approved models, and measure cost/quality vs a single-model baseline.
  - Build a **rubric-based evaluator** from one of our agents; compare auto-generated dimensions to our hand-written eval criteria.
  - Prototype a **DIY router** with **GPT-4.1-nano** or **Mistral Small** for intent routing and benchmark against the managed router.
  - Pilot **explicit prompt caching (Azure context cache)** on a long-running task and verify privacy/ownership + savings (private preview — check eligibility).
  - Try a **managed fine-tune (SFT/DPO)** of a small model to embed a policy/domain doc; deploy to the **developer tier** to test cheaply.
- [ ] Questions:
  - GA/preview status + pricing for **rubric evals**, **serverless RL API**, and **router governance policies**?
  - How to **request access** to explicit prompt caching private preview?
  - Which exact 28 models are in the router, and how does **failover** affect cost attribution?
  - For Claude-on-Azure (GB300s): data residency, regions, and rate limits vs Anthropic-direct?
- [ ] Relevant to:
  - Any team building **cost-aware agentic systems** on Azure AI Foundry.
  - Platform/eval-first teams adopting **hill-climbing** + evals-as-IP.
  - FinOps / cost-optimization initiatives (caching, batch, routing, distillation).
  - Lab work: routing + fine-tuning + observability reference architecture.

## 🔗 Related
- [[BRK231 - Deploy Observe Learn Reinforcement learning for production agents]] — deeper on the RL / reinforcement fine-tuning thread for production agents.
- [[BRK252 - From observability to ROI for AI agents on any framework]] — extends the observability → cost/ROI story across frameworks.
- [[DEM333 - How Foundry integrates with open-source frameworks and tools]] — the open/composable Foundry ecosystem these model strategies plug into.
- [[DEM322 - Smaller faster smarter Distilling models with fine-tuning]] — the distillation/fine-tuning technique used to build the GPT-4.1-nano student here.
- [[BRK246 - Foundry IQ Fuel agents with enterprise knowledge]] — grounding/knowledge step in the same Foundry build journey.
- [[Model router]] — the 28-model routing layer (with governance policies) central to this session's cost strategy.
- [[Prompt caching]] — Azure explicit/context cache (private preview) covered as a core cost lever.
- Source list: [[2026 Build Session List]]

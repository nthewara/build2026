---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/on-device
  - topic/snapdragon
  - topic/edge-ai
  - topic/ai
source: https://www.youtube.com/watch?v=c0fKfsZny3Y
session_code: BRKSP90
event: Microsoft Build 2026
speakers: Alberto Martinez (Qualcomm)
duration_min: 42
aliases:
  - Stop routing docstrings to 70B models on-device AI on Snapdragon
---

# BRKSP90 — Stop routing docstrings to 70B models with on-device AI on Snapdragon

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speaker:** Alberto Martinez — Software Strategy, Compute Business, Qualcomm (~40 years in the industry)  
> **Duration:** ~42 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=c0fKfsZny3Y)

## 🎯 TL;DR

AI coding workloads are blowing up token budgets and dollar bills — and agentic orchestration is about to multiply that cost 10–100x. Alberto Martinez (Qualcomm) argues that the majority of everyday AI coding tasks (docstrings, lint fixes, simple routes) are *trivial* and should never be routed to a 70B+ cloud model. His thesis: build a **three-tier routing architecture** (on-device laptop → on-prem workstation → cloud) governed by a small, fast **classifier** that scores prompt complexity and dispatches each sub-task to the cheapest model that can do the job correctly. With a Snapdragon X2 Elite (80 TOPS, up to 122 GB memory, ~225 GB/s bandwidth), research shows **~73% of workload is resolvable locally**, potentially saving **up to ~$24,000/day** of a $36k/day spend, processing **~1.6 billion tokens locally per day with zero quality loss**, and hitting **sub-200ms on-device response** times. The classifier is the key IP developers should build themselves — it's a competitive advantage, lives in the orchestrator, and needs a confidence-based fallback to the cloud when entropy spikes mid-execution.

## 🔑 Key Takeaways

- **"Stop routing your docstrings to a 7-billion-parameter model"** — the provocative thesis. Blindly sending *every* prompt to a very large model wastes tokens, money, power, and latency on tasks that don't need that horsepower.
- **The token economy is now an everyday-life problem, not just a backend one.** Martinez personally runs out of tokens in hours; the inflection point is that his non-technical wife (an attorney) now hits limits too — meaning it's hitting *consumers*, not just infrastructure providers.
- **Agentic orchestration multiplies token consumption 10x–100x** (per Qualcomm CEO Cristiano Amon at Computex). A $36k/day spend becomes $300k–$350k/day on an exponential curve.
- **Most AI coding work is low-complexity.** On a 1–7 complexity score using Claude Sonnet 4.6 data: ~34% of workload is simple/medium-low (~1,300 queries), another tranche is medium-high (~1,500 queries), leaving only ~20–30% that is genuinely complex and needs a big model.
- **Three-tier architecture is the minimum sensible design:** (1) personal laptop/desktop on-device, (2) on-prem headless workstation/server, (3) cloud. More tiers are possible.
- **The classifier is the crown-jewel IP.** It's a small model (<20ms, <50 tokens budget) that scores each prompt and routes it. Building your own classifier is a *competitive advantage*; using a shared/commodity one gives you none.
- **Classifier uses four signals (prongs) + a fifth fallback leg:** (1) token count, (2) abstract-syntax/decision-tree depth, (3) profile/context reference count, (4) security flags — plus (5) confidence fallback that aborts to cloud when runtime entropy grows too fast.
- **Snapdragon X2 Elite specs:** 80 TOPS NPU, 143% greater compute than prior gen, up to 122 GB memory, up to ~225 GB/s memory bandwidth (stream edition; ~152 GB/s elite edition as stated), supports your favorite data types.
- **Integer quantization is a major lever:** up to ~50% memory reduction vs floating point, with only ~5% quality/precision loss — acceptable for complexity scores 1–7. Above score 7, keep floating point because precision becomes critical (avoid "activation collapse").
- **Economics are staggering:** demo showed the cloud-only path cost ~21¢ vs ~5.1–5.5¢ hybrid — **4x cheaper**. At scale that's ~$14k/month vs ~$4k/month differential per recurring marketing/dev workflow.
- **Everything is code now.** PowerPoints, Excel reviews, data compilations — all generate Python/JS/HTML under the hood, so the savings apply far beyond "developers."
- **Research-backed local resolution: up to ~73%** of workload resolvable on-device today; even a conservative 50% gap "would make you super happy."
- **Hardware pays for itself absurdly fast:** a partner spending $35k/dev/month could save $15k+/dev/month — enough to **replace the hardware every month and still save money** (vs typical 3–4 year refresh cycles).
- **Call to action — "build it yourself":** audit last week's AI coding request logs, categorize by complexity, find your threshold, measure for two weeks (token cost + latency), optimize the classifier, rinse and repeat.
- **The classifier belongs in the orchestrator**, which owns routing logic, execution monitoring, and aggregation — because the orchestrator ships requests to agents, and agents are attached to models.

## 📚 Detailed Notes

### Framing: predict the future by creating it
Martinez opened by improvising the whole talk and framing it as a "who-done-it mystery" about uncovering where agentic AI and orchestration are heading. His guiding philosophy (a famous, oft-attributed quote): *"If you want to predict the future, you have to go and create it."* Wait for someone else to build it and you're a follower; build it yourself and you're the innovator. The session is about "peeling the onion" on the agentic/orchestration story to understand what developers need to do next.

### The problem: token economics is becoming everyone's problem
- Martinez feels **10x more productive** using AI daily — for research, development, and practice.
- But he constantly runs out of tokens. At the office you don't *see* tokens run out; instead the **CIO sees the dollar counter climbing** in the backend and eventually says "guys, you're cut off."
- The personal inflection point: his wife (an attorney, non-technical) recently hit token limits for the first time and was told to "wait until 8 p.m." to continue. That signals the cost pain has reached **consumers**, not just infrastructure/foundation-model providers.
- Per Qualcomm CEO **Cristiano Amon** (Computex this week): token consumption is multiplying **10x and 100x** because agents run at a far higher token rate than human prompting.
- **The red thread:** the solution is in our hands — not only for economics, but for **power conservation, energy consumption, and latency**.

### The broken math (token costs per task type)
Using Qualcomm's research (data derived from Claude Sonnet 4.6), processing typical tasks costs:
- **Docstring** in a prompt: ~**180 tokens**
- **Lint error fix**: ~**210 tokens**
- **Generating a route**: ~**460 tokens**
- **Security audit**: starts at ~**3,800 tokens** ("goes off the roof")
- **Cross-repo refactor** (similar complexity to a security audit): ~**3,900 tokens**

When you send any of these to the cloud, the *smallest* model you hit is **over 70 billion parameters** — overkill for a docstring. "Your mileage will vary based on your classifier," but the point stands: it all costs money, and those tokens add up.

### The dollar math and the agentic multiplier
- On the **low side**, organizations spend ~**$36,000** (per the curve's lower distribution; he cites ~50 developers context).
- Anecdotally, some vendors/partners spend **~$35,000 per developer per month**.
- Once you apply **agentic + orchestration**, these functions go **10x** — so $36k becomes **$300k–$350k** on an exponential growth curve.
- He name-drops **Peter Steinberger** (rendered "Standberger" in captions) as someone spending ~**$1 million/month** — "maybe he can do that; I cannot afford it personally."

### Workload distribution (the core insight)
Analyzing prompt complexity on a 1–7 (sometimes 1–4) score using Claude Sonnet 4.6:
- **~34%** of all workload is **simple** (score 1–4) — ~**1,300 queries**.
- A **medium-to-low / medium-to-high** band — ~**1,500 queries** plus another ~7%.
- These simple/medium queries can **run locally** on a Snapdragon X2 Elite given its compute and memory bandwidth.
- The **remaining ~20% (sometimes 30%)** is **complex** — too big for the X2 Elite — and must go to a **more capable on-prem device** or the **cloud**.
- This naturally produces **three tiers**: (1) your PC/desk computer, (2) an on-prem headless workstation, (3) the cloud.
- The savings are big enough that **you can justify almost any hardware in your office to your CIO**.

### Why Snapdragon (the hardware plug)
The new-generation **Snapdragon X2 Elite**:
- **80 TOPS** NPU capacity
- **143% greater compute** than the previous generation
- Up to **122 GB of memory**
- Up to **~225 GB/s memory bandwidth** (stated as "225 in the stream edition, 152 in the elite edition")
- Supports your favorite data types (with an important FP-vs-INT differential discussed below)

### Quantization: floating point vs integer
- Historically, **floating-point** code is easier to develop and gives **better precision**.
- **Integer formats** (especially for weights) yield up to **~50% memory reduction** over floating point (a saving *not even counted* in his other calculations). A 100 GB FP model can drop to ~50 GB in INT — and then it *fits*.
- **Bandwidth savings** follow: smaller weights = half or a quarter of the memory bandwidth used (e.g., INT4 vs higher).
- **Power** drops for many reasons.
- **Caveat:** in floating point / FP16, **activations preserve forward numerical precision** that is critical for instructions and **avoid activation collapse** — and Qualcomm supports this.
- **Rule of thumb:** if you're power- and memory-conscious, an integer (or reduced-integer) format can do the task with only a **~5% quality gap** — *acceptable for complexity scores 1–7*. For scores **>7**, **don't** quantize to integers — precision becomes too relevant.

### The numbers (dual-axis research chart)
On a dual-axis chart (requests/day vs tokens/request), across ~20–30 task types:
- The curve skews left (requests/day) and right (token complexity).
- **On-device:** up to **~3,100 requests** can run locally.
- A **more capable on-prem device:** another **~660 requests**.
- The **remaining high-complexity** requests go to big cloud models — and routing this way saves **~50% to ~70%** of computational/token spend.
- Using the same $36k/day baseline, you can **save up to ~$24,000/day** by dividing prompts into sub-tasks dispatched to independent models.
- That equals **~1.6 billion tokens processed locally per day** (as of "April 1") — **with zero quality loss for developers**.
- Crucially: *not* a server-class box on your desk, *not* a water-cooled rack — **a laptop or a more capable workstation you can buy today at Best Buy**.

### The demo (proof of concept)
- Origin story: Martinez built an **emulator using AI-generated code**; it gained popularity inside Qualcomm; CEO Cristiano demoed it at **Computex**, and Martinez brought a version to Build.
- **The prompt:** "Design a Snapdragon page with a link to qualcomm.com, with Taiwanese floating lanterns in the background."
- It looks simple but is a *collapsed* prompt. The hardest sub-task — the **floating lanterns** — needs a **physics model**, background planning, and complex code execution that genuinely requires a **70B+ parameter** model (they tested 3B → 30B → 70B → 120B; smaller models couldn't do the lanterns).
- **Two streams raced** (framed as an F1 race — there was an F1/AMG car parked out front):
  - **Cloud-only:** Claude 4.7 Opus end-to-end.
  - **Hybrid mode:** the **classifier** decomposed the prompt into **5 tasks** — 1 medium (needs up to a **32B** model), 3 easy (run on an **8B** model on the PC), and 1 hard (the lanterns, executed on **Claude 4.7 Opus** in the cloud).
- **Result:** Both produced the **same final picture** ("Thank you Taiwan," lanterns animating). The cloud-only stream actually ran *faster* (the hybrid pipeline isn't optimized yet — he expects that to improve as the software team optimizes it).
- **But cost differs dramatically:** cloud-only ≈ **21¢**; hybrid ≈ **5.1–5.5¢** → **~4x cheaper**, on top of the ≥50% reductions already discussed.
- **Generalization:** Everything we do is ultimately code — generating a PowerPoint, reviewing an Excel sheet, compiling datasets all produce Python/JS/HTML. So classify correctly and the savings extend to **marketing teams building web pages, product launches**, etc. Recurring, that's ~**$14k/month vs ~$4k/month**.
- Martinez's aside: in the old days you punch-carded everything to a central server (he learned on an IBM mainframe). The pendulum is swinging back toward distributed/local compute — "send what matters to the cloud," and you also "save some polar bear habitat and penguins."

### What it means for everyone (provider, developer, user)
- **≥65%** of cloud GPU cycles consumed can be reclaimed/avoided.
- Research shows **sub-200ms on-device response** turnaround (the demo couldn't show sub-millisecond, so he didn't claim it).
- **User cost reduction** is "tremendous value."
- For a partner paying **$35k/dev/month**, integrating this saves **$15k+/dev/month** — enough to **buy a lot of hardware** that lasts 3–4 years. The savings are so large you could **replace hardware every month and still save money**.

### The three-tier model (concrete thresholds)
- **Tier 1 — On-device (laptop/desktop):** models **~13B and below** for sure, up to **~34B** with soon-to-release architectures; complexity score **1–6** ("logic entropy") runs locally.
- **Tier 2 — On-prem workstation/server:** up to **~100B (slightly more, ~120B)** parameters; "a little box that sits under your desk" — *not* a water-cooled rack.
- **Tier 3 — Cloud:** anything bigger, e.g., **security audits, full code-repo work** — send it up.
- Routing is governed by an **entropy threshold** evaluated by the **classifier**.

### The classifier (the heart of the architecture)
The classifier is a **small model** that must react in **<20ms** and use **<50 tokens** (so it's "lost in the noise" of the request). Why 20ms? Because the target end-to-end is **<200ms**, and a rule-of-thumb 10% budget = 20ms. It scores prompts on **four prongs**:

1. **Token count** — analyze the prompt and count tokens first.
2. **Abstract-syntax / decision-tree depth** — how deep is the tree of decision logic? `if` clauses, conditional branches ("create page A, but if X not released, make page B…") increase depth and push the request up a tier.
3. **Profile / context reference count** — how many external references the prompt pulls in ("look at this email *and* that presentation, search the web, combine into a solution"). More references = higher tier.
4. **Security flags** — authorization requests, prompt-injection signatures, compliance terms. Any compliance/security match raises a **red flag** for careful handling.

All four are **tunable thresholds** — you can find your own optimal point and even make the classifier **recursive / adaptive / self-learning**.

### The fifth leg: confidence-based fallback
The four prongs make a **prediction**, and predictions have errors. So there's a **fifth leg — the fallback**:
- Martinez draws an analogy to **CPU prefetchers** (from his CPU-architecture career): a prefetcher predicts the next instruction and goes in a direction; because it's imperfect, you *must* have a fallback when it's wrong.
- The runtime success metric is **entropy**. If, *during execution*, the query's entropy grows **faster than expected**, **abort** and reshuffle to the cloud "before it goes deeper into the weeds."
- On abort you have (at least) two choices: (a) **reclassify** with the same parameters (learns nothing, same answer) or (b) **eat the bullet and send to cloud** for a proper, non-hallucinated answer.
- Over time, review what went wrong and correct the classifier.

### Research evidence (the "boring" references slide)
Martinez declined to read citations aloud but summarized the support: entropy calculations, quantization research, edge inference, and routing capabilities. Headline numbers:
- **Up to ~73%** of workload is resolvable locally today (a 50% target "would make you super happy," even 10% is real money).
- **68% of Stack Overflow developers (2024 survey)** use AI tools for **documentation and boilerplate** — that's **100% local-eligible** work.
- A **73% enterprise-codebase workload analytics study** (50-developer team, cross-maintained heavy codebase) found **50–60%** could use **lower/edge resolution** → small models running locally.
- Integer quantization costs only **~5% precision** while delivering huge memory, power, and bandwidth reductions on a power-efficient NPU.

### Call to action — "build it yourself"
1. **Look at your request logs.**
2. **Categorize last week's AI coding requests by complexity** (simple completions, boilerplate, LLM/lint fixes by complexity).
3. **Find your own threshold** — nobody hands it to you; it's easy but lazy to send everything to a big model ("like driving a gas-guzzler two blocks for groceries").
4. **Measure for two weeks** — track token cost and latency.
5. **Optimize your classifier and repeat.** Rinse and repeat. That's the solution space — saving money *and* the environment.

### Where the classifier lives (Q&A insight)
The classifier **belongs in the orchestrator**, not standalone — because the orchestrator ships requests to agents, and agents attach to models. The orchestrator owns the **routing logic, execution monitoring, and aggregation output**. A deeper open research problem: **"which model, when, and who"** — today routing is by *known* capability (we test, we know model X can do task Y, so we send Y→X); in the near future, model/orchestrator/device capabilities will need to be **known in a global, discoverable fashion**.

## 🛠️ Products / Features / Technologies Mentioned

- **Snapdragon X2 Elite** — Qualcomm's new-gen compute platform: 80 TOPS NPU, 143% more compute than prior gen, up to 122 GB memory, up to ~225 GB/s bandwidth (stream edition; ~152 GB/s elite edition as stated). Stream edition and Elite edition variants referenced.
- **Qualcomm NPU** — power-efficient neural processing unit central to the on-device inference argument.
- **Claude Sonnet 4.6** (Anthropic) — used to generate the research workload-distribution data and complexity scoring.
- **Claude 4.7 Opus** (Anthropic) — the cloud-only / big-model stream in the live demo (also used for the hard "lanterns" sub-task in hybrid mode).
- **The Classifier** (Qualcomm research IP, not yet generally available) — small <20ms / <50-token model scoring prompts on 4 prongs + fallback.
- **The Orchestrator** — owns the classifier, routing logic, execution monitoring, and aggregation; dispatches to agents/models.
- **Hybrid / on-device emulator** — AI-coded proof-of-concept demonstrating multi-tier task decomposition (shown by CEO Cristiano Amon at Computex).
- **Integer (INT) quantization** (e.g., INT4 / reduced-int) vs **floating point (FP16)** — the memory/bandwidth/power vs precision trade-off.
- **Cline ("Klene") and Claude** — coding agent tools referenced by an audience member (Nathan) as where automated task-splitting is rarely seen.
- **GNNs / "GNI"-style models** — noted in Q&A as behaving slightly differently from LLMs for entropy measurement and classification, but the approach applies similarly.

## 🚀 Announcements / What's New

- **No formal product announcement.** This was a forward-looking research/strategy talk, not a launch. The headline artifacts are research findings and an architectural proposal.
- **Snapdragon X2 Elite** was presented with detailed specs as the enabling hardware (new-generation positioning), but framed as available-to-buy today rather than newly announced here.
- **Qualcomm classifier research** was previewed as **work-in-progress**: classifiers are **not yet generally available**; Qualcomm is researching them and intends to **make a classifier available** while encouraging the ecosystem to build their own.
- **A research paper is forthcoming** — Martinez said he hasn't published it yet but promised to: *"You're getting a preview of the paper."*

## 💡 Demos

**The Lantern Race (recorded demo, from Computex).**
- **The prompt:** "Design a Snapdragon page with a link to qualcomm.com, with Taiwanese floating lanterns in the background" — a deceptively simple but *collapsed* prompt.
- **The hard part:** the floating lanterns require a physics model, background planning, and complex code that genuinely needs a **70B+ parameter** model (tested across 3B / 30B / 70B / 120B; only the largest succeeded on the lanterns).
- **Two racing streams** (framed as an F1 race, complete with an F1/AMG car parked outside):
  - **Cloud-only:** Claude 4.7 Opus, end-to-end.
  - **Hybrid:** the classifier split the prompt into **5 sub-tasks** — 1 medium (≤32B model), 3 easy (8B model on the PC), 1 hard (lanterns → Claude 4.7 Opus in the cloud).
- **Outcome:** identical final result ("Thank you Taiwan" page with animating lanterns). The cloud-only stream ran *faster* (hybrid pipeline not yet optimized), but the **hybrid cost ~4x less** (~5.1–5.5¢ vs ~21¢).
- **Takeaway shown live:** same visual quality, dramatically lower cost — proving complexity-aware routing works in practice. Martinez accelerated the playback so the audience didn't "watch the matrix fall" (Python code scrolling).
- *Note:* sub-millisecond / sub-200ms latency was **not** demonstrated because this particular recorded demo didn't capture it — only cost was shown.

## 📊 Notable Stats / Quotes

> **"Stop routing your docstrings to a 7-billion-parameter model."** — the talk's core provocation.

> **"If you want to predict the future, you have to go and create it."** — Martinez's guiding philosophy (famous, oft-attributed quote).

> **"1.6 billion tokens could be processed locally… and I'm not telling you a server class on your desk. I'm talking about your laptop… that you can go and buy today at Best Buy — with zero quality loss."**

> **"You can replace your hardware every month and you're still saving money. It's an incredibly powerful equation."**

> **"It's like moving a gas-guzzler car to go for groceries two blocks away. It's a waste of resources."** — on sending everything to a big model.

> **"We can not only save money but we can save some polar bear habitat and some penguins on the other side of the world."** — on the energy/environmental angle.

**Token costs per task (Claude Sonnet 4.6 research):**
- Docstring in prompt: **~180 tokens**
- Lint error fix: **~210 tokens**
- Route generation: **~460 tokens**
- Security audit: **~3,800 tokens**
- Cross-repo refactor: **~3,900 tokens**

**Economics:**
- Low-side spend: **~$36,000** (per lower distribution); anecdotal partner spend: **~$35,000/developer/month**.
- With agentic orchestration: **10x → ~$300k–$350k**.
- Peter Steinberger cited at **~$1 million/month**.
- Potential savings: **up to ~$24,000/day** of a $36k/day baseline; **$15k+/dev/month** savings for a $35k/dev partner.
- Demo cost: **~21¢ (cloud) vs ~5.1–5.5¢ (hybrid) = 4x cheaper**; recurring ≈ **$14k/mo vs $4k/mo**.

**Hardware (Snapdragon X2 Elite):** 80 TOPS · +143% compute vs prior gen · up to 122 GB memory · up to ~225 GB/s bandwidth (stream; ~152 GB/s elite).

**Workload / routing:**
- ~**3,100** requests/day on-device · ~**660** on-prem · remainder to cloud.
- **~50–70%** computational/token savings via routing.
- **~1.6 billion tokens/day** processable locally with **zero quality loss**.
- **≥65%** cloud GPU cycles reclaimable; **sub-200ms** on-device response.
- **Up to ~73%** of workload locally resolvable (per research max).

**Quantization:** up to **~50%** memory reduction (INT vs FP), **~5%** precision loss — fine for complexity ≤7, not advised >7.

**Classifier budget:** **<20ms** latency, **<50 tokens** (10% of a 200ms target).

**Adoption evidence:**
- **68%** of Stack Overflow developers (2024) use AI for documentation/boilerplate → 100% local-eligible.
- **73%** enterprise-codebase study (50-dev team): **50–60%** suitable for lower/edge resolution.

## 🧠 My Notes / Follow-ups

- [ ] **Things to try:**
  - Audit my own AI coding request logs for the last week and bucket prompts by complexity (1–7) to find where my personal on-device/cloud threshold sits.
  - Prototype a tiny prompt classifier (token count + decision-tree depth + reference count + security flags) and measure routing accuracy.
  - Benchmark an 8B and a 32B model locally (e.g., on a Snapdragon X-class or comparable NPU/box) against cloud-only for everyday tasks; track $/task and latency.
  - Experiment with INT4 vs FP16 quantization on a small coding model and measure the real precision gap on complexity ≤7 tasks.
  - Implement a runtime "entropy" abort/fallback heuristic so a local run can bail to cloud mid-execution.
- [ ] **Questions:**
  - What *exact* entropy metric does the research use for the runtime fallback signal? (Paper not yet published.)
  - How does the ~225 GB/s "stream" vs ~152 GB/s "elite" bandwidth labeling reconcile? (Caption may have swapped editions.)
  - Is the 8B/32B/70B/120B tiering model-family-specific, or a general capability map?
  - When Qualcomm releases its reference classifier, how customizable/self-learning will it be vs. roll-your-own?
  - How does this integrate with existing agent orchestrators (Cline, Claude Code, AutoGen, etc.) without bespoke plumbing?
- [ ] **Relevant to:**
  - On-device / edge AI strategy and cost-optimization for AI coding workloads.
  - Anyone managing a CIO-visible AI token/dollar budget or GPU spend.
  - Hybrid local+cloud orchestrator design and model-routing IP.
  - Snapdragon / NPU hardware evaluation for dev workstations.

## 🔗 Related
- [[Microsoft Build 2026]]
- [[On-device AI]]
- [[Edge AI inference]]
- [[Model routing & orchestration]]
- [[Quantization (INT vs FP)]]
- [[Snapdragon X2 Elite]]
- [[AI token economics]]

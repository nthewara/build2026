---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/foundry
  - topic/models
  - topic/production
  - topic/ai
  - topic/fine-tuning
source: https://www.youtube.com/watch?v=sOvtPvaog3M
session_code: BRKSP91
event: Microsoft Build 2026
speakers: Vivek Chauhan (Fireworks AI), Jeet (Fireworks AI), Nico Groupin (Harvey AI)
duration_min: 41
aliases:
  - Turn foundation models into production AI on Foundry
---

# BRKSP91 — Turn foundation models into production AI on Microsoft Foundry

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Vivek Chauhan (Fireworks AI), Jeet (Fireworks AI — Foundry integration), Nico Groupin (Head of Applied Research, Harvey AI)  
> **Duration:** ~41 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=sOvtPvaog3M)

## 🎯 TL;DR
A Fireworks AI partner session arguing that for most enterprise use cases the quality gap between open-weight and frontier closed models has collapsed, so companies can switch to fine-tuned open models to cut cost dramatically while holding the quality bar. Fireworks pitches a single platform spanning world-class **inference** (their own CUDA-kernel-up inference engine) and **training** (a training agent for app builders, a managed training UI for ML engineers, and a raw training API for researchers), all tied together by a continuous-improvement "flywheel" of train → deploy → monitor → retrain with one-click deploy and guaranteed numerical fidelity. The headline announcement: **Fireworks is now generally available in Microsoft Foundry** (announced at Satya's keynote the prior day), exposing Fireworks inference + custom-model deployment through Foundry's model catalog via three modes — serverless/pay-as-you-go, PTU/provisioned throughput, and bring-your-own-weights. Harvey AI's Nico Groupin closes with a real-world case study: using GLM 5.1 worker agents that route to heavier closed "advisor" models to navigate the quality/cost Pareto frontier, achieving up to **2.4× cheaper** while being ~**30% better** on their legal agent benchmark's all-pass metric.

## 🔑 Key Takeaways
- **The open-vs-closed gap has collapsed for most enterprise tasks.** Pointing Claude Opus 4.7 at something like email summarization is overkill; a smaller fine-tuned open-weight model can hit the same quality bar and save a ton of money.
- **True differentiation comes from your own data, not the base model.** If you use the same closed model as every competitor, there's no moat — fine-tuning your own data into the model is how you differentiate.
- **The real winners run a flywheel, not a one-off fine-tune.** Leading companies continuously train → deploy → monitor → pull traces → retrain on the same platform, spinning the loop faster and faster.
- **LLM inference is a brutal combinatorial problem** (~84,000–85,000 permutations per model across SKUs, parallelization, quantization, speculative decoding). Most companies shouldn't solve this in-house; Fireworks absorbs that complexity.
- **One platform, three training surfaces by skill level:** a no-code **training agent** (PMs/app builders), a **managed training** clickable UI (ML engineers), and a raw **training API** (advanced ML teams/researchers) — all with one-click deploy.
- **One-click deploy is the speed unlock.** No downloading weights, reformatting, re-uploading, or worrying about numerics between training and serving — train, eval, ship from the same place.
- **Guaranteed numerical fidelity:** what you trained (and the eval results you saw) matches production serving — critical for MoE/floating-point models where numerics can drift.
- **File/inference optimizer gives "custom shapes":** the same model on the same GPUs can be served minimal-shape vs full-precision, optimized for speed vs throughput, tuned to your traffic — plus autoscaling for peaks/troughs.
- **Fireworks is now GA in Microsoft Foundry** (announced at Satya's Build 2026 keynote): one endpoint, one contract, one platform. Inference + custom-model deployment are on Foundry; training stays on Fireworks (train there, download, deploy on Foundry).
- **Four reasons customers pick Fireworks on Foundry:** performance (CUDA-kernel-up optimization), model advantage (day-zero open-source releases), control/extensibility (custom models in the catalog), and economics (cheaper than closed at comparable quality, and you spend existing Azure credits).
- **Three Foundry integration modes:** serverless/pay-as-you-go (shared, per-token, rate-limited), PTU/provisioned throughput (reserve GPUs for production), and bring-your-own-weights (deploy your trained custom models on Azure credits).
- **Fireworks models in the Foundry catalog carry the `FW` prefix** and can be wired directly into Foundry **agents** alongside tools (web search, custom functions).
- **Harvey's hybrid "advisor agent" architecture works:** open-weight worker agents (GLM 5.1) calling heavier closed advisor models (Opus 4.7) via inference-time routing beat pure-closed on cost/latency *and* sometimes on quality — up to **2.4× cheaper, ~30% better** on all-pass.
- **"Jagged intelligence" (Karpathy's term) is why post-training matters in a vertical:** models are great at some tasks (e.g. corporate M&A) and fail at others (e.g. litigation/case-law research); post-training smooths these rough edges across all practice areas.
- **Security/governance is a first-class reason to use open weights:** in-VPC deployment plus access to the full reasoning trace enables interpretability, auditability, and compliance for high-stakes work — a key driver for regulated domains like legal.

## 📚 Detailed Notes

### Three fundamental truths about the AI landscape (Fireworks' thesis)
Vivek Chauhan opens by framing the whole session around three beliefs:
1. **The gap between open-weight and frontier closed models has collapsed** for all practical purposes across most enterprise use cases. Companies can switch to an open-weight model and keep the same quality bar while saving a lot of money. Concrete example: instead of pointing **Claude Opus 4.7** at an email-summarization task, use a smaller open-weight model and reach the same quality for far less cost.
2. **Differentiation comes only from embedding your own data into the AI.** If you run the same closed-weight model as all your competitors, you have no differentiation. Fine-tuning your own data in is the key to a genuinely differentiated AI stack.
3. **The leading companies go beyond one-off inference/fine-tuning** — they continuously improve their stack and have found a **flywheel** on Fireworks' platform that gives them a durable, differentiated "mode/moat." The session's goal is to show how you can build that same flywheel.

### About Fireworks AI (scale and customers)
- Processes **more than 30 trillion tokens per day** — positioned right behind frontier closed-weight labs (Claude/Anthropic, OpenAI).
- Serves **more than 10,000 enterprise customers** globally building production-grade applications on open-weight models.
- Named customers: **Cursor** (used Fireworks' RL rollout capabilities to build **Composer 2 / Composer 2.5** models), **Vercel**, **Jasper**, **Uber**, **DoorDash**, and many more. They lean on Fireworks for better quality (via fine-tuning/training) and better performance (speed, throughput, time-to-first-token) tuned to each application's needs.

### The inference engine (why in-house is a bad idea)
- LLM inference is described as a **very brutal combinatorial problem**: speculative decoding, quantization modes, different SKUs, different parallelization strategies → **more than ~84,000–85,000 permutations for a single model** you want to serve.
- For most companies it makes no sense to handle this complexity in-house; the space moves too fast. Fireworks keeps up with it all — **CUDA kernels, quantization, speculative decoding, adaptive caching**, and every new optimization trick — and bakes it into the stack so customers can focus on their application.
- They can hit application-specific SLAs on demand: e.g. "time to first token < 500 ms," "end-to-end latency < 2 s," specific throughput targets.
- **All of these inference-engine capabilities are now available on Foundry** (demoed live later in the session).

### "Own your AI stack" — meeting customers where they are
Vivek's "favorite slide": Fireworks wants every company to **own their AI stack**, and to meet teams wherever they are on their AI journey (different companies — and even different teams within one company — are at different stages). To do that, they offer three training surfaces ranging from high-level/no-code to low-level/raw control:

1. **Training agent** — targeted at **product managers and app builders**. You give it your data and business use case in plain English; it returns a fine-tuned model. (Live/recorded demo shown.)
2. **Managed training platform** — targeted at **ML engineers**. If you already know your training method and have a dataset, just port the dataset and kick off a job; Fireworks handles all back-end infrastructure orchestration.
3. **Training API** — targeted at **advanced ML teams and researchers**. Exposes the raw primitives: custom loss functions, reward functions, advanced algorithms, highest context window, full-parameter fine-tuning.

Crucially: **no matter which surface you use, you get one-click deploy** in the platform — essential for iteration speed. No training-here-serving-there, no downloading/reformatting. One-click deploy → run evals → ship to production.

### The flywheel (continuous improvement loop)
Leading companies on the platform run an accelerating loop: **train → deploy → monitor → pull traces → retrain.** Fireworks handles the hard parts that make this possible:
- **GPU orchestration** — no scavenging for GPUs, no worrying about elasticity, bad nodes, or CSP issues ("that's our headache").
- The mechanical core of the loop — **moving weights over, hot loading, checkpointing** — is handled for you.
- **Speed:** what might take many weeks DIY in-house, you could get **~10 iterations** done on Fireworks.
- **Numerical fidelity guarantee:** when training large models (especially **MoE** models using floating-point precision), numerics can drift, so "what you train on might not be what you serve on." Fireworks guarantees the eval results you got in training match production serving performance.
- **No vendor sprawl:** training + inference in one platform, one-click deploy.

### Demo 1 — The training agent (no-code fine-tuning)
Premise (after asking the room "how many of you love writing evals and reformatting data?" — nobody): the agent is for people who don't want to deal with the ML plumbing. You speak in plain English ("this is my dataset, this is my business goal, help me fine-tune a model"), and the agent:
- **Reformats your data** and **writes evals** for you.
- Helps with **model selection** (finds a model that may suit your use case).
- Does **hyperparameter search** for you (instead of manually grinding through permutations).
- Produces a **plan** outlining what it proposes — including an **upfront cost estimate** for the training iteration.

Workflow once you approve the plan:
1. Agent takes a **small cut** of your dataset and runs a **hyperparameter grid search** to narrow the sample space.
2. It comes back: "I tried ~10 iterations; these two are most promising, here's why + the eval results. Do a full-dataset run?"
3. On yes, it runs the **full training run on the full dataset**, gives a step-by-step view of what's happening under the hood, and a **comprehensive final report**.

Everything is also available **headless via a skill file** — drop the skill file into your own coding agent/harness (GitHub Copilot, Claude, Cursor, etc.), add your API keys, and train directly from there. It also suggests follow-on iterations. The agent covers **supervised fine-tuning, preference optimization, and classification-model** tasks out of the box.

### Demo 2 — Managed training (clickable workflow)
For users who already have a dataset and know their method/hyperparameters:
- Choose the workflow: **supervised fine-tuning, reinforcement fine-tuning, or preference optimization.**
- **Pick the model** — Fireworks is typically among the fastest (often "day zero") providers for open-weight inference, which also makes them one of the fastest to support **fine-tuning** on those open-weight models.
- **Upload the dataset directly**, or use **secure training** to stream data **BYOB** (bring-your-own-bucket) straight from your own cloud.
- Expose raw parameters — **epochs, learning rate, batch size** — with smart defaults out of the box, then kick off the job.
- **Reinforcement fine-tuning** adds one step: upload or connect a **grader** (e.g. via your GitHub repo) so the RFT job can reward the model. Exposes additional knobs (**top-K, top-P**, batch size, learning rate).
- **Weights & Biases** integration: plug in your API key for detailed telemetry/monitoring.
- **Preference optimization**: similar setup — upload data, choose configs, run as many times as you want.
- **Live monitoring:** while a job runs you watch the **loss/reward function in real time**; if it's misbehaving you can **pause** and redo the reward function/eval.
- **One-click deploy** at the end (no downloading/reformatting/re-uploading, no numerics worries).
- **Compound training:** chain methods — SFT → DPO on top → RL on top → as many passes as you want (this is the flywheel of continuous iteration).
> Note: the transcript renders "DPU" — in context this is almost certainly **DPO (Direct Preference Optimization)** layered on a supervised fine-tuned model.

### Inference & dedicated deployment (custom "shapes")
After training, you deploy:
- **On-demand deployment** of fine-tuned models; supports the **largest array of open-weight models**. You can run inference on a plain base model or on your fine-tuned model.
- **File/inference optimizer → custom shapes:** the *same* model on the *same* number of GPUs can deliver very different performance depending on how the whole GPU stack (CUDA kernels → spec decoding → everything around it) is orchestrated. The UI lets you pick a shape: **minimal-shape vs full-precision**, **optimized for speed vs optimized for throughput**, matched to your application's traffic — then one-click deploy that shape.
- **Autoscaling:** scales up/down automatically with your traffic peaks and troughs.

### The training API (raw power for advanced ML teams)
For advanced ML users who want the platform's raw primitives while Fireworks still handles infra:
- Write your **own custom loss functions**; use the **latest algorithms** (e.g. on-policy techniques — transcript mentions "on policy registration" and "Syspo," likely garbles of current RL post-training methods).
- **Full-parameter fine-tuning** supported.
- A publicly available **cookbook (GitHub repo)** with ready-made recipes — pick a recipe, change the knobs, no need to write from scratch.
- Killer capability: **train the model from within your own harness.** The argument: an AI must learn to do the job *from within your environment/harness*, knowing which tools it has and how to orchestrate them. (Harness + model co-training is revisited later via Harvey.)
- Scale claim: you can "**train a 1 trillion parameter model from your laptop**" because Fireworks handles all the infra.

### Announcement — Fireworks GA in Microsoft Foundry
Announced the prior day at **Satya Nadella's Build 2026 keynote**. Everything shown for **inference deployment** is available on **Foundry**; **training is not** on Foundry — you train on Fireworks, then download and move the model into a **custom model deployment** on Foundry. An announcement video (with a partner, "Lean," from the Microsoft Foundry side) frames it as: take all of Fireworks' greatness *and* all of Foundry's greatness in a simplified way — **one endpoint, one contract, one journey, one platform.**

### Why customers choose Fireworks on Foundry (four reasons — Jeet)
The second presenter (Jeet) takes over to explain the Foundry fit:
1. **Performance** — the inference engine optimizes from the **CUDA-kernel level up**, squeezing the most out of the GPU for the customer's specific use case.
2. **Model advantage** — most models release on Fireworks at **day zero** (examples cited: **DeepSeek V4**, **Kimi 2.6**), so you can plug state-of-the-art open-source models into agents as soon as they ship.
3. **Control & extensibility** — many **custom models** can now be deployed on Foundry via the Fireworks ↔ Azure Foundry catalog integration.
4. **Economics** — what customers care about most. Closed-source models get expensive fast at scale; Fireworks offers a cheaper alternative at comparable quality, and Foundry integration lets you **spend existing Azure credits**.

### Three Foundry integration / deployment modes
1. **Serverless (pay-as-you-go):** models already deployed on Foundry — no need to create a deployment; it's a **shared deployment** across users, **per-token billing**, with **rate limits** (shared infra). State-of-the-art OSS models available today in this mode include **GLM 5.1, Kimi 2.6, GPT 120B**, with more added as they release.
2. **PTU / provisioned throughput:** for a known production workload — **reserve GPUs** and deploy a model for your specific use case. PTU-gated; works very well for production.
3. **Bring your own weights (BYOW):** for customers who've **trained open-source models** to compete with closed-source on quality. Train/chain on Fireworks → download the weights → upload to Azure → deploy on Azure using your Azure credits. Best when you have trained proprietary models to use in your application.

### Customer proof points (Foundry + Fireworks)
- **UiPath** — wanted a faster, more cost-effective model, *and* an open-source model that beats the quality of a closed-source **Sonnet 4.6**; achieved using Fireworks models on Azure Foundry. (Transcript "Sonic 4.6" → Claude **Sonnet 4.6**.)
- **Bolt** (transcript: "Bolt New," i.e. **bolt.new**) — needed something that scales well on **throughput and latency** for production; solved via the Azure ecosystem + Fireworks model.
- **Motive** — needed models to run **repeatable tasks at high volume**; deployed on Azure Foundry, optimized with the Fireworks engine, to serve that repeatable high-volume workload.

### Demos 3–5 — Deploying on Foundry (serverless, custom, agents)
- **Serverless deploy:** In Azure Foundry → **Discover** → **Models** → model catalog. Fireworks-optimized models carry the **`FW` prefix**. Click a model → **Deploy** → optionally set **custom settings** (PTU / rate limits, since serverless is shared) → toggle rate limits → Deploy. You can then **chat with the model** in the UI or call the **API** to plug into agents/apps.
- **Custom-model deploy:** Go to the **Build** section → **Models** → **Custom model** section (not Deployments) → **Add** → name it and **choose the base architecture** (if the architecture isn't supported by default, contact Azure/Fireworks to enable it) → use the provided **command-line prompt to upload** your custom model to Azure → then just **click Deploy**. Because it's *your* deployment, **no rate limits**; you decide how many **PTUs / provisioned throughput** to allocate. Chat via UI or call the API.
- **Agents deploy:** In the **Build** page there's a step for **agents** on your Azure account. Name the agent → Deploy (a couple of minutes) → choose the model behind the agent (a Fireworks model already on Foundry **or** a custom model) → integrate **tools** (web search, your own defined tools/functions). The agent works well with those tools alongside the chosen Fireworks model.

### Customer spotlight — Harvey AI (Nico Groupin)
Nico Groupin, **Head of Applied Research at Harvey AI**, joins as special guest. Harvey is **the generative AI platform for legal and professional services**, used by **thousands of law firms** worldwide; mission is to make lawyers' work more efficient, higher quality, and reduce busy work. (Vivek notes Harvey is used by "hundreds of leading legal firms"; Nico says thousands.)

**LAB — the Legal Agent Benchmark** (launched ~2–3 weeks before the talk): a benchmark to measure **Long-Horizon agents on legal tasks**, addressing the central question of *quality* in a specific vertical as agents proliferate in the application layer. Four components:
1. **The agent's environment** = a **client matter** — the universe of documents, work, and intermediate work product a lawyer uses on a project. The agent is dropped into this environment.
2. **The instruction is partner-level**, not a detailed checklist — e.g. "here's a data room, write me an issues list," then circle back with the complete work product. The agent must rely on its **priors** for how legal work is done plus its **tools and harness skills**.
3. **It must produce real legal work product** — not just a chat answer, but real **Word docs, Excel spreadsheets, PowerPoints** (often 5–10 in a single task scope).
4. **Graded with expert rubrics** — each task has **~50+ rubric criteria** specifying the material points of good work product.

Scale of LAB: **24 legal practice areas**, **over 1,200 tasks total**, up to **~75,000 total rubric criteria.** The strict **all-pass** scoring is a high bar for whether the agent truly did the task a human would.

**Why Harvey invests in open models — four considerations (Nico):**
1. **Domain expertise (named first, surprisingly):** models exhibit **"jagged intelligence"** (term coined by **Andrej Karpathy**) — really good at some things, failing miserably at others, hard to reason about why. In legal, a model might be strong at **transactional work** (corporate M&A, financial due diligence) but weak at **litigation work** (case-law research, writing-intensive tasks). **Post-training smooths these rough edges** and brings the model up to speed across all practice areas.
2. **Cost and latency:** "you don't need to bring the Ferrari off the racetrack if you don't need to." A **bimodal distribution** of usage is emerging — pay a premium with frontier closed models for really high-stakes, complex work, but route a lot of simpler work to open-weight models that are perfectly well suited. **Routing between these two modes** becomes increasingly important.
3. **Security and governance:** for the highest-stakes work, customers ask for **secure deployment within their own VPC**, which open-weight models enable. You also get access to the **complete reasoning trace** of the model, enabling much greater **interpretability and auditability** of an agent's behavior — increasingly important for **compliance** over time.
4. **(Iteration velocity / the managed loop)** — see below; Harvey treats faster iteration as itself a key reason.

### Harvey + Fireworks — the advisor-agent architecture (the headline result)
The research track Nico is most excited about (published the morning of the talk): **advisor agents.** Harvey built a system where **worker agents driven by open-weight models (GLM 5.1)** call out to heavier **advisor models** — in many cases closed-source frontier models like **Opus 4.7**. This **inference-time routing** lets you navigate the **Pareto frontier of quality vs cost**:
- Pure closed frontier → top performance but significant cost + latency tradeoffs.
- Open-weight → much cheaper, much faster, greater security guarantees, but a performance tradeoff.
- **Hybrid system → maintains quality at lower cost and latency, and in many cases actually improves quality.**

**Quantified result (Vivek):** up to **2.4× cheaper** on a task where it's about **30% better on the all-task (all-pass) metric.** Vivek's framing: using a frontier closed model for *every* task is "like having an aircraft carrier to point at a bunker as well as to point at an ant" — you should exercise judgment on which model each task needs, and open models are genuinely very good.

Harvey is also pursuing **straightforward post-training (SFT) with Kimi models**, showing nice lift on LAB's all-pass criteria over the base model. LAB is treated not just as a benchmark but as a **foundation for research** into post-training of open-weight models, **harness optimizations** (baking domain specificity into the agent harness), **skills, tool use**, and frontier topics like **memory**.

### The iteration cycle & why Foundry (Harvey's perspective)
- **Managed inference = plug-and-play:** Harvey can start consuming open-source models very quickly with no iteration overhead.
- **Managed training infrastructure tightens the loop:** the iteration loop becomes much tighter, faster, more efficient — running many post-training experiments **in parallel** in a low-touch way for the research team. Harvey's mantra: **"all timelines are compressed"** — including research — so velocity is crucial. (Fireworks echoes: "all iteration cycles are compressed.")
- **Why Microsoft Foundry specifically:** Harvey has "always been an Azure customer." Legal is the **highest-stakes type of knowledge work**, demanding the highest grade of infrastructure, security, governance, and compliance — which is what Nico associates with Microsoft Foundry. The Fireworks ↔ Foundry partnership is a **"best of both worlds"**: keep the enterprise-grade Azure infrastructure they already use, then **layer on** managed inference for open-weight models, training infrastructure, and seamless deployment — **without handicapping their own infra teams.**
- **Historical context / advice:** when Nico joined Harvey (~3 years ago) it was 5–6 people in an Airbnb worrying about whether the Wi-Fi worked, before this AI infrastructure existed. His advice to founders building an AI stack for the first time — or enterprises rebuilding to be **agent-native** — is to **"ride the tailwinds"** of this managed infrastructure (Fireworks' work + its Microsoft partnership) so you don't have to figure it all out yourself and can move much faster.

### Closing call to action (Jeet)
If you're starting a new use case or reimagining an existing one and already use Azure, go check out **Fireworks models on Azure Foundry** — multiple deployment modes (serverless, PTU, BYOW) that you can integrate into agents, whether Azure agents or agents you built yourself. The session closes to Q&A for Nico, Vivek, and Jeet.

## 🛠️ Products / Features / Technologies Mentioned
- **Fireworks AI** — inference + training platform for open-weight models; ~30T tokens/day, 10,000+ enterprise customers.
- **Microsoft Foundry (Azure Foundry)** — Microsoft's enterprise AI platform; hosts the model catalog and agents; now hosts Fireworks (GA).
- **Fireworks inference engine** — proprietary inference stack optimizing from the CUDA-kernel level up across ~84k–85k permutations.
- **File / inference optimizer** — produces **custom model "shapes"** (minimal vs full-precision, speed- vs throughput-optimized) tuned to your traffic.
- **Training agent** — no-code, plain-English fine-tuning agent for PMs/app builders (data reformatting, eval writing, model selection, hyperparameter search, cost-estimated plan, full-run report). Also available **headless via a skill file**.
- **Managed training platform** — clickable UI for ML engineers (SFT, RFT, preference optimization).
- **Training API** — raw primitives for advanced ML teams (custom loss/reward functions, full-parameter fine-tuning, train-from-within-your-harness).
- **Fireworks cookbook** — public GitHub repo of training recipes.
- **Compound training** — chain SFT → DPO → RL across multiple passes (the flywheel).
- **Secure training (BYOB)** — stream training data directly from your own cloud bucket.
- **Weights & Biases** — optional telemetry integration for training runs.
- **Foundry integration modes** — serverless/pay-as-you-go, PTU/provisioned throughput, bring-your-own-weights.
- **Foundry model catalog** — Fireworks models carry the **`FW` prefix**; deploy via Discover → Models.
- **Foundry agents** — wire a Fireworks/custom model into an agent plus tools (web search, custom functions).
- **GLM 5.1** — open-weight model; used as Harvey's worker-agent model and available serverless on Foundry.
- **Kimi 2.6** — state-of-the-art open-source model; day-zero on Fireworks; available serverless on Foundry. (Also "Kimi models" used in Harvey's SFT work.)
- **GPT 120B** — open-weight model available serverless on Foundry.
- **DeepSeek V4** — cited as a day-zero open-source release on Fireworks.
- **Claude Opus 4.7** — frontier closed model; used as Harvey's heavier "advisor" model and as the "overkill for email summarization" example.
- **Claude Sonnet 4.6** — closed model UiPath's open-source model was tuned to beat (transcript: "Sonic 4.6").
- **Cursor / Composer 2 & 2.5** — customer that used Fireworks RL rollouts to build its Composer models.
- **Harvey AI** — generative AI platform for legal/professional services; thousands of law firms.
- **LAB (Legal Agent Benchmark)** — Harvey's benchmark for long-horizon legal agents.
- **Vercel, Jasper, Uber, DoorDash, UiPath, bolt.new, Motive** — named Fireworks/Foundry customers.

## 🚀 Announcements / What's New
- **General Availability of Fireworks AI in Microsoft Foundry** — announced at Satya Nadella's Build 2026 keynote (the day before this session). One endpoint, one contract, one platform. **Inference deployment + custom-model deployment** are available on Foundry; **training remains on Fireworks** (train on Fireworks → download → deploy on Foundry).
- Fireworks models live in the **Foundry model catalog** with the `FW` prefix, deployable **serverless (pay-as-you-go), via PTU, or bring-your-own-weights**, and integratable directly into **Foundry agents** with tools.
- **Harvey's advisor-agent research** published the morning of the talk (GLM 5.1 workers + closed advisor models; up to 2.4× cheaper / ~30% better on all-pass) — a publication/announcement rather than a Microsoft product GA.

## 💡 Demos
> All demos were recorded (Vivek noted "actually, recorded demo").
- **Training agent (no-code fine-tuning):** plain-English goal → agent reformats data, writes evals, selects a model, runs hyperparameter grid search on a data subset, proposes a cost-estimated plan, then (on approval) runs the full-dataset training with a step-by-step view and final report. Proves you can fine-tune without touching ML plumbing or writing evals/data formatting yourself.
- **Managed training UI:** pick SFT/RFT/preference optimization, select model, upload or BYOB stream the dataset, set epochs/learning rate/batch size (with smart defaults), connect a grader for RFT, optional W&B telemetry, live loss/reward monitoring with pause, then one-click deploy. Proves the clickable end-to-end training-to-deploy loop for ML engineers.
- **Dedicated inference deployment with custom shapes:** select a custom-tuned model and choose a serving shape (minimal vs full-precision, speed vs throughput) on the same GPUs, with autoscaling, then one-click deploy. Proves the same model/GPUs can be tuned to very different performance profiles per traffic need.
- **Foundry serverless deploy:** Discover → Models → `FW`-prefixed model → Deploy → set rate limits → chat in UI / call API. Proves pay-as-you-go Fireworks models are a few clicks away in Foundry.
- **Foundry custom-model deploy:** Build → Models → Custom model → Add → name + base architecture → CLI upload to Azure → Deploy (no rate limits, choose PTUs). Proves you can bring trained weights into Foundry easily on your own Azure credits.
- **Foundry agent deploy:** Build → Agents → name → Deploy → choose Fireworks/custom model behind the agent → add tools (web search/custom functions). Proves Fireworks models plug straight into Foundry agents with tooling.

## 📊 Notable Stats / Quotes
- **~30 trillion tokens/day** processed by Fireworks — "right behind frontier closed-weight labs."
- **10,000+ enterprise customers** on Fireworks.
- **~84,000–85,000 permutations** for serving a single model (SKUs × parallelization × quantization × spec decoding).
- SLA examples: **time to first token < 500 ms**, **end-to-end latency < 2 s**.
- DIY in-house might take **many weeks**; Fireworks gets you **~10 iterations** in that time.
- "You can **train a 1 trillion parameter model from your laptop**."
- Harvey **LAB**: **24 practice areas**, **1,200+ tasks**, **~75,000 rubric criteria**, **~50+ criteria per task**, agents produce **5–10** real documents per task.
- Harvey advisor-agent result: **up to 2.4× cheaper** while **~30% better on the all-task (all-pass) metric.**
- *"It's like having an aircraft carrier to point at a bunker as well as to point at an ant. You don't need that."* — Vivek, on using frontier closed models for every task.
- *"You don't need to bring the Ferrari off of the racetrack if you don't need to."* — paraphrasing the cost/latency argument.
- **"Jagged intelligence"** (Andrej Karpathy) — models great at some tasks, failing at others; the motivation for vertical post-training.
- *"All timelines are compressed."* — Harvey's mantra; Fireworks: *"all iteration cycles are compressed."*
- *"Ride the tailwinds."* — Nico's advice to founders/enterprises building or rebuilding an agent-native AI stack.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Browse the Foundry model catalog for `FW`-prefixed models and deploy one serverless (GLM 5.1 / Kimi 2.6 / GPT 120B) to compare cost vs a closed model on a real task.
  - Prototype the **advisor-agent / inference-time routing** pattern: open-weight worker + closed advisor, and measure the quality/cost Pareto on our own workload.
  - Test the Fireworks **training agent skill file** inside a coding harness (Copilot/Claude/Cursor) for a quick SFT iteration.
  - Walk the **BYOW** path: train on Fireworks → download weights → upload + deploy as a Foundry custom model on Azure credits.
- [ ] Questions:
  - Pricing specifics for serverless vs PTU on Foundry, and how Azure credit consumption is metered for Fireworks models.
  - What base architectures are supported by default for custom-model upload, and the turnaround to enable an unsupported one.
  - How strong is the "numerical fidelity" guarantee for MoE models in practice (any published validation)?
  - Which RL post-training methods are actually behind the garbled "on policy registration / Syspo" references?
- [ ] Relevant to:
  - Any team weighing open-weight fine-tuning vs frontier closed models for cost control.
  - Regulated/high-stakes domains (legal, finance, healthcare) needing in-VPC deployment + reasoning-trace auditability.
  - Platform/MLOps teams wanting a single train→deploy→monitor flywheel on Azure.

## 🔗 Related
- [[2026 Build Session List]]
- Microsoft Foundry / Azure AI Foundry notes
- Fine-tuning & post-training (SFT / DPO / RFT) notes
- Open-weight vs frontier closed model strategy
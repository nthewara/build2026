---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/nvidia
  - topic/nemotron
  - topic/agents
  - topic/foundry
source: https://www.youtube.com/watch?v=ELusMKrFJso
session_code: BRKSP94
event: Microsoft Build 2026
speakers: Joey (NVIDIA — Nemotron product), Stephen McCullough (NVIDIA — AI Solutions Architect)
duration_min: 38
aliases:
  - Orchestrate specialist agents with NVIDIA Nemotron on Foundry
  - Orchestrate special agents with NVIDIA Nemotron models on Foundry
  - BRKSP94
---

# BRKSP94 — Orchestrate specialist agents with NVIDIA Nemotron models on Foundry

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Joey (NVIDIA — Nemotron product/strategy) & Stephen McCullough (NVIDIA — AI Solutions Architect, works daily with Microsoft on HW/SW integration)  
> **Duration:** ~38 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=ELusMKrFJso)

> [!note] Naming note
> The official Build catalog title uses "special agents," but the talk is really about **specialist / specialized agents** — agents that hold a specific skill or body of knowledge. Caption garbles in the source have been corrected to the verified spellings: **Nemotron** (not "Neotron/Neimotron/Nematron/Matron/Emotron"), **Entra ID** (not "intra ID"), **Nous Research** (not "Noose Research"), and presenter **Stephen McCullough** (captioned "Steven McCulla").

## 🎯 TL;DR
NVIDIA (Joey + Stephen McCullough) walk through the journey from the ChatGPT moment → open reasoning models (DeepSeek) → today's agents, then introduce the **NVIDIA Nemotron** open model family and its newest, most capable member: **Nemotron 3 Ultra** (550B total / 55B active), a frontier open reasoning + orchestration model announced at Build, available on Foundry managed compute "this month" (Ultra specifically called out as available **Tuesday**). The core thesis: enterprises will run a **system of models** (different sizes, modalities, locations) powering **specialized agents** in a reason→act loop, with an emphasis on **efficiency** (moving the accuracy-vs-compute and accuracy-vs-cost frontier to the upper-left). Nemotron is fully open (weights, datasets, RL environments/skills via NeMo Gym, research) and is post-trained for agentic use. The second half is a live **Microsoft Foundry hosted agents** demo where a **Hermes agent (Nous Research) on Nemotron 3 Super** reads an email, makes code changes, opens a GitHub PR, learns a reusable **skill**, and gets governed end-to-end via **Microsoft Entra ID** and a single **Foundry managed toolbox** of MCP tools — then surfaced in **Microsoft Teams** with memory persisting across sessions.

## 🔑 Key Takeaways
- **Three-era framing:** ChatGPT moment (~3.5–4 yrs ago) → DeepSeek open reasoning models (~1.5 yrs ago, breakthrough for *open* reasoning) → **agents** (start of this year) where software does multi-step work, shifting focus from Q&A exchanges to **tasks and outcomes**.
- **Agent mental model:** prompt/request → agent loop of *context/knowledge → observe → plan → reason → act*, looping until the job is done; surrounded by **tools & skills**, **security & governance**, **memory** (short- and long-term), and **orchestration** across a *fleet* of agents.
- **Agents = harness + LLMs.** LLMs power the reason/act core; skills can run on CPU or GPU (via the **CUDA / CUDA-X** stack); memory and governance can live local or across the network.
- **Three NVIDIA pillars for long-running agentic systems:** (1) **systems of models** (more than one model — varied sizes/languages/modalities/locations), (2) **specialized agents** (Toy Jensen "different outfits" metaphor — post-trained skills + access), (3) **efficiency** (push pre-train/post-train/inference left on the compute axis: more intelligence, less compute).
- **Nemotron is a *family*** of checkpoints + data + tools, with pillars: **reasoning**, **vision**, **information retrieval** (embedding + reranking), **content moderation/safety**, and **speech** (STT + TTS) — all open models, open datasets, open training techniques, open customization software.
- **Three reasoning model sizes (by GPU footprint):** **Nano** (Dec) — small data-center GPU, MoE **30B / 3B active**; **Super** (March) — ~1–2× H100 80GB; **Ultra** — largest open model, ~2× **B200**, best capabilities. Ultra **available Tuesday**.
- **Nemotron 3 Ultra (announced Sunday at Build):** **550B total / 55B active**, *frontier reasoning + orchestration*, strong **task-completion times**, fast prefill + fast multi-turn agentic loops, **lower cost / more work in less time**, tuned to run well across agentic harnesses, and **1M-token context**.
- **Headline efficiency claim:** at frontier-level accuracy, Ultra delivers **~5× faster inference speed** vs the March (Nemotron 3 Super) release, per third-party **Artificial Analysis** — with expectation to push further over the coming weeks.
- **Training breakthrough:** **multi-teacher on-policy distillation** — multiple specialized Ultra "teacher" models distilled down into Nemotron 3 Ultra (vs prior SFT → RL progression).
- **Precision breakthrough:** **NVFP4** format optimized for **Blackwell** — reduces memory footprint *and* accelerates compute; **one checkpoint** now runs **NVFP4 on Blackwell** and **falls back to run well on Hopper**, eliminating per-architecture checkpoint sprawl (previously bf16/FP8 on Hopper, bf16 on Ampere, NVFP4 on Blackwell).
- **Architecture features (Ultra, shared with Super):** **hybrid (Mamba-Transformer MoE)** architecture (compute-efficient in the DC, memory-efficient for long context), **latent MoE** (reach more experts with less compute), **multi-token prediction** (predict multiple tokens per inference query → higher throughput), **1M context length**.
- **Open harness ecosystem:** Nemotron tuned to run across open harnesses incl. **OpenCode**, **Hermes agent**, **OpenClaw**, and **pi**.
- **Foundry hosted agents (Stephen's half):** **bring-your-own container/harness/env**, deploy into Foundry; agent gets an **agent identity** recognized across the environment (Entra ID); **isolated per-session** execution (security); **lifecycle, versioning, auditing, compliance** built in.
- **Single control plane:** the **Foundry managed toolbox** connects many services/MCP servers (Outlook, GitHub, Teams, MongoDB, Cosmos DB, + bring-your-own MCP) through one endpoint with granular allow/deny per function — plus **observability/traces** of every tool & step the agent took.
- **Govern agents like colleagues:** grant/revoke/audit agent access via **Entra ID** (e.g., add the agent as a *Reader* on a storage account in IAM); **OAuth pass-through** lets the agent inherit the user's identity (PR commits show as the user); publish the agent to **Microsoft 365 / Teams** with **skills + memory persisting across sessions and services**.

## 📚 Detailed Notes

### Speakers & structure
Two NVIDIA presenters. **Joey** opens with the journey, the Nemotron family, and the Nemotron 3 Ultra announcement (plus the Hermes "Collective Wisdom" demo video). He then hands off — "*with that I'll hand over to my colleague… Thank you Joey*" — to **Stephen McCullough**, an **AI Solutions Architect at NVIDIA** who works with Microsoft daily integrating NVIDIA hardware + software, who delivers the live **Foundry hosted agents** demo and the recap.

Agenda Joey set: (1) history of the journey of the last few years and where we are today; (2) new work from NVIDIA and the Nemotron open model family; (3) the ecosystem and how NVIDIA is contributing.

### The journey: three eras of capability
- **ChatGPT moment (~3.5–4 years ago):** the LLMs the field had worked on for years suddenly proved far more capable — an amazing interface where you could ask complex questions and get complex answers.
- **DeepSeek open reasoning (~1.5 years ago):** DeepSeek published **open models that could reason** — a breakthrough because, before this, reasoning wasn't common in the *open* community. This unlocked many more open models tackling math, coding, and scientific Q&A.
- **Agents (start of this year):** software where you interact with models *in the background* to get more work done, focusing on **tasks and outcomes** rather than simple question-answer exchanges — unlocking many more use cases. This is where the session spends most of its time.

### How NVIDIA thinks about an agent (the loop)
Starting from a **prompt** (a request, a job to do), the agent sits in a loop:
- **Context / background / knowledge** — what it needs to do, what it has access to, what its skills are.
- **Observe** — look at what's available and what it can do.
- **Plan** — create a plan for making progress.
- **Reason** — reason through that plan; identify tasks.
- **Act** — do the actual work; loop until the job is done.

Surrounding the loop:
- **Tools & skills** (top-right) — configurable; an enterprise/company may provide some.
- **Security & governance** — just as employees have scoped access today, agents need scoped access too.
- **Memory** (bottom) — short-term and long-term; tracks work done, work pending, and potentially broader knowledge of what *other* agents are doing.
- **Orchestration** (far left, under prompt) — one agent runs its loop, but can work with and **orchestrate workloads across a fleet of other agents**.

### Agents = harness + LLMs (where compute runs)
NVIDIA overlays where LLMs run on that diagram: LLMs power most of the **context/reason/act** core. **Skills** can run on CPU **or** GPU (via the **CUDA** software stack alongside the LLMs). **Security & governance** can mean access to network protocols or content across a company. **Memory** can live across the network, locally, on CPU or GPU, and there's also some memory **inside the LLM** itself.

### Three pillars for long-running agentic systems
1. **Systems of models.** To be most successful, enterprises will likely need **more than one model** — different languages, modalities, sizes, and run locations, all working together.
2. **Specialized agents.** Like people specialize, agents gain a specific skill/knowledge set. NVIDIA illustrates with **"Toy Jensen"** (their CEO as a toy) wearing different outfits = different skill sets; agents are **post-trained** and given knowledge/capabilities/system access to take on tasks.
3. **Efficiency.** Across **pre-training, post-training, and inference (runtime / test-time thinking)**, plotted against **compute** on the x-axis, NVIDIA constantly tries to **move the curve left** — improve intelligence while reducing the compute (and time) needed.

### The Nemotron family (what it actually is)
NVIDIA frames Nemotron as a **family of models = checkpoints + data + tools**, not a single model. Pillars across the family:
- **Reasoning** (the focus of this talk).
- **Vision** capabilities.
- **Information retrieval** — embedding and reranking.
- **Safety** — content moderation.
- **Speech** — speech-to-text and text-to-speech.

Everything is **open**: open models, open datasets, the training techniques used to create them, and software to **customize** them. Across the bottom of the family slide are the published content families (pre-training data, post-training data, RL environments/skills under **NeMo Gym**, and research).

### The three reasoning sizes (footprint, capability, speed)
- **Nano** — smallest; targets a **very small data-center GPU**; small MoE, **30B total / 3B active**; released **December**.
- **Super** — published **March**; think **~1–2× H100 80GB** data-center GPUs.
- **Ultra** — the **largest open model** NVIDIA has; think **~2× B200**; takes a few GPUs but delivers the best capabilities; **available Tuesday**.

All sizes ship with **open datasets** (pre-training + post-training data), **RL environments and skills under NeMo Gym**, and **published research**.

### Announcement: Nemotron 3 Ultra (made Sunday)
- **Largest + most capable** Nemotron to date: **frontier reasoning and orchestration**.
- **550 billion total / 55 billion active** parameters.
- Highlights: **great task-completion times** (heavy focus on output generation), **fast prefill** + **fast multi-turn** agentic runs, **lower costs** (more work in less time), tuned for **agentic harnesses in the ecosystem** (demo video to follow), and **everything open** so people can inspect it, gain confidence, and build a business on it.

### Nemotron 3 Ultra — the breakthroughs
1. **Multi-teacher on-policy distillation (training).** Evolution from **SFT** → (late last year) heavy **RL** → now **multi-teacher on-policy distillation**: multiple large **teacher** models — various Ultra models trained on **specific tasks** — are distilled down into Nemotron 3 Ultra, so Ultra learns well across all teachers and inherits their capabilities/skills.
2. **NVFP4 precision (Blackwell).** **NVFP4** is optimized to run on **Blackwell**, reducing memory footprint *and* accelerating compute. Crucially, instead of separate checkpoints per format/architecture (historically: bf16 / FP8 on Hopper, bf16 on Ampere, NVFP4 on Blackwell), Ultra fits **one checkpoint** (e.g., a single Hugging Face download) that runs in **NVFP4 on Blackwell** and **falls back to run well on Hopper** — fewer options, easier selection.
3. **Open harnesses in the ecosystem.** Time spent ensuring Nemotron runs well across **OpenCode**, **Hermes agent**, **OpenClaw**, and **pi**.
4. **Architecture & features (also in Nemotron 3 Super):**
   - **Hybrid architecture** — compute-efficient in the data center, memory-efficient for long context.
   - **Latent (MoE) architecture** — reach more experts with less compute.
   - **Multi-token prediction** — one inference query predicts **multiple** tokens instead of one → higher throughput.
   - **1M-token context length** — up to 1,000,000 input tokens the model can use and keep in memory while running agentic tasks.

### Benchmarks & how Ultra was evaluated
NVIDIA compared Nemotron 3 Ultra against strong open models — **GLM (5.x)**, **Kimi K2 (≈K2.6)**, and **Qwen 3.5** (caption spellings "GLM51 / Kim K26 / Quen 35") — and praised the open community's progress. This release leaned **more on agentic tasks** than past releases:
- **Agentic tool use / productivity** — a **τ-bench-style** ("Pinchbench" in captions) eval: can the agent call the **right tools**, get the work done, and do it **efficiently**?
- **Long-horizon planning** — using **ServiceNow's "Enterprise Ops Gym"**: complex tasks like a **password reset** that may touch many systems, record information, send responses, fail, and require iteration.
- **Coding** — increasingly common and popular.
- **Instruction following** — strictly adhering to given directions.
- **Knowledge work** — common-industry tasks (e.g., **manufacturing, healthcare**) plus professional work (e.g., **PhD-level** and **MBA-level** tasks).
- **1M context length** capability.

**Third-party validation (Artificial Analysis):** y-axis = an **accuracy index** (combination of the above tasks); x-axis = **output token speed** (how fast it thinks/answers). Goal = **upper-right** (frontier accuracy *and* high throughput). Reference point: Nemotron 3 (March release). Result: at that **frontier-level accuracy**, Ultra achieves **~5× faster inference speed** — with expectation to push further in the coming weeks.

**Cost-efficient frontier (new chart, first shown at the CEO's GTC keynote days earlier):** y-axis = **accuracy** = ability to **complete a coding task correctly**; x-axis = **cost to complete the task**. A query goes in; the model does real work (calls tools, modifies/edits files, runs a compiler) and returns the answer; NVIDIA measures the **tokens + time**, prices it using the **lowest** of **CoreWeave** and **Deep Infra** prices, and plots a **Pareto curve**. Different cost footprints (smaller vs larger budget) let you trade off accuracy/capability. Nemotron 3 Ultra moves toward the **upper-left** (more accuracy per dollar), and NVIDIA expects all models to trend that way over time.

### Demo 1 (video): Hermes "Collective Wisdom" — skills that compound across a company
**Scenario:** a small company doing a **product launch**; **four senior leads** across four functions, each with a **two-week window** to get launch content ready. Each box = a workflow a person owns.
- Each senior lead works alongside **Hermes agent on Nemotron 3 Ultra**, bringing **reasoning, writing, and judgment** to every task.
- When a person **corrects** Hermes, the correction is **saved as a reusable skill** the team can apply.
- The **Hermes curator** runs on **Nemotron 3 Super**, continuously processing skills — **merging, de-duping, rewriting, testing, and promoting only what's ready to share**.
- Anything shared goes through **enterprise review and approval**; **the method is shared, the launch data stays private**.
- Approved skills join **Hermes "Collective Wisdom"** — the company's growing library of proven methods.
- **Months later** the team moves faster — not from their own work alone, but from each other's; **every method captured by one lifts the rest**.
- Tagline: "*the power of Hermes from **Nous Research** on NVIDIA Nemotron 3 Ultra*."

**Joey's takeaway from the demo:** individuals create skills (ways for agents to get work done); agents then **generalize** those skills across the company; more people adopt them; skills come to represent **subject-matter experts**. Forward-looking idea: future job candidates might ask **"what agents/skills are available at this company?"** because better agents/skills make work easier. We're "just at the beginning of this journey."

### Foundry hosted agents (Stephen McCullough)
The bridge from "intelligence + agentic environment" to the **real world** is **Microsoft Foundry hosted agents**. Key features:
- **Bring your own container / harness / environment** and deploy it into Foundry hosted agents.
- **Agent identity** — give it access to resources just like a regular colleague; the identity is **recognized across your environment**.
- **Isolated sessions** — any code it writes or documents it produces can be **isolated to a single session**, improving security and confining work to a specific user/environment.
- **Lifecycle & compliance** — meet **auditing** and **versioning** requirements so deployed agents can be used to their fullest.

**Reference deployment shown:** **Hermes agent** running in Foundry hosted agents; **Nemotron Super + Nemotron Nano** running in **Foundry managed compute endpoints**; **Entra ID** granting the agent access to external data (GitHub, Teams, email). Pitch: tell your agent *"check my email and take care of this,"* or *"look at what my boss said in Teams yesterday and handle it."*

### Demo 2 (live): email → PR → learned skill, fully governed
1. **Session start / self-check.** Stephen starts a new session in **Foundry Agent Service**; asks the agent what it is. It reports running **Nemotron 3 Super** with the **Hermes agent harness**.
2. **Real task delegated.** Colleague **Alex** emailed about a feature request in **"LLM Perfbench"** (an internal LLM testing repo): add **chat-completions endpoint** support to the benchmarking tool. Stephen **delegates** the whole thing — *without pasting the email into the prompt/context*. Because the hosted Hermes agent is connected to **Outlook + GitHub** via Foundry, it **finds the email, makes the code changes, and opens a PR by itself**. The interaction is framed like talking to a colleague ("my manager sent me an email, go find it and do its thing").
3. **One toolbox, many services.** The workflow uses **Outlook (email)**, **GitHub**, and a **coding sandbox** for code testing. Rather than wiring each service/auth flow/MCP endpoint/permission model separately, Stephen connects them all through a **single Foundry managed toolbox**. The **Foundry catalog** has built-ins — **MongoDB, Teams, Cosmos DB**, many MCP servers — and you can **bring your own MCP tool/agent**. Admins **granularly allow/deny** functions (e.g., *read* from Teams but **no** sending messages/emails to the manager). This **single management plane** matters more as workloads and tool use grow.
4. **Result + observability.** The agent **successfully creates the PR**. Foundry shows **exactly what happened** — which **tools and MCP servers** were used, every step, and the path from original email → final PR. This **observability/audit trail** is critical for enterprise agents (debugging, workflow improvement, and proving how the agent acted **on behalf of a user**).
5. **Review + teach a skill.** The PR's code checks **pass**, but Stephen wants changes: **add Alex (the requester) as a reviewer** and **include docstrings** in functions — *and* wants the agent to **remember this for the future** whenever it works with this repo. This demonstrates Hermes' **self-learning skill mechanism**: instead of one-off requests, the agent turns feedback into **reusable behavior** (for **LLM Perfbench**: Alex is always the reviewer; docstrings always included). The agent **edits the PR** and **creates the skill**; the trace shows it called Hermes' internal **`skill manage`** function (create/delete/update skills).
6. **Verify + identity.** The updated PR shows **Alex added as reviewer** and a **commit adding docstrings**. Via **OAuth pass-through**, the agent **inherits Stephen's identity** — its **commits show as coming from Stephen**.

### Governance via Microsoft Entra ID
Foundry doesn't just give agents tools — it **governs** them through **Microsoft Entra ID**, managing an agent's access **the same way you'd manage access for a person**. From the Foundry UI you can find the agent's Entra ID and grant it access to, e.g., **blob storage**: go to the storage account → **IAM** → add the agent (by the **agent ID hash** Foundry generated) **as a Reader**, exactly as you would add a colleague like Alex. Useful when you want the agent to **read data** or **maintain a database** for you, with **granular** control over what it can and cannot do.

The key point: the agent now has an **identity that can be retrieved, managed, and governed across the company** — granted access, restricted access, **audited**, and governed with the **same controls enterprises already rely on**. This extends **far beyond Azure resources**: as agents become closer collaborators, NVIDIA + Microsoft are implementing agents **across the Microsoft 365 ecosystem**, with **built-in identity, authentication, and access management** at the core — increasingly essential as agents grow more complex and intelligent.

### Publishing to Microsoft 365 / Teams + cross-session memory
Foundry also makes it easy to **integrate agents into the tools themselves**. Once the agent is configured and working well, Stephen **publishes** it and makes it available to **Microsoft 365 apps**, including **Microsoft Teams**. In Teams he opens the **hosted Hermes agent** and chats with it directly in the Teams UI, asking whether it **still has the skill for the LLM Perfbench repo** — the skill it created only **~5–10 minutes earlier in a completely different session**. The agent **remembers the specific guidance**, proving it is **not confined to a single chat interaction**: the hosted agent **retains skills across interactions, sessions, and services**, so over time it becomes **more aligned to how you, your team, and your company collaborate** — managing long-running agentic tasks **from the same place you already collaborate with colleagues** (your "co-pilot / partner").

### Recap — why this combination matters
Stephen recaps that **Foundry hosted agents** solve key problems that typically slow agentic development. With hosted Hermes, the demo showed the agent **take a real task from an email**, **find that email**, **leverage Foundry's built-in tooling**, **create its own PR**, **expose its tools via observability**, and **learn a specific skill it remembers across sessions and services**. The value isn't just that the model can reason or write code — it's that **Foundry provides the infrastructure, tooling, and observability** to **customize the agent and turn the model into a useful enterprise asset**.

The three-part value stack for enterprises:
- **Nemotron** → highest **token efficiency**, **frontier intelligence**, **open** models + training data + research, **post-trained for agentic use**.
- **Hermes (agent wrapper, Nous Research)** → wraps Nemotron to add **multi-model orchestration** and **continuous learning/improvement**, making the agent more of an organizational **asset** over time.
- **Foundry** → the **infrastructure** to run/support/distribute it across the company: **agent identities via Entra ID** (treat the agent like a colleague — grant/revoke access; integrate into Teams), the **toolbox** (single control plane for all tools + MCP servers), and **secure session management** (no data leaving the session; every user/agent gets a **fresh, fully-controlled session**).

### Resources & call to action
Live demo running at the NVIDIA **booth in the 308 space** — come talk to the experts. Check out NVIDIA **models** and **NeMo skills**; tons of **free** online resources — not just open-source models but **all the research and information** about them. A **QR code / survey** was shared at the end. (Applause.)

## 🛠️ Products / Features / Technologies Mentioned
- **NVIDIA Nemotron** — open model family (checkpoints + data + tools); pillars: reasoning, vision, information retrieval (embedding + reranking), safety/content moderation, speech (STT/TTS).
- **Nemotron 3 Nano** — MoE **30B / 3B active**; small data-center GPU; released **December**.
- **Nemotron 3 Super** — released **March**; ~1–2× H100 80GB; hybrid MoE; powers the live demo + Hermes curator.
- **Nemotron 3 Ultra** — **550B / 55B active**; frontier reasoning + orchestration; ~2× B200; **announced Sunday**, **available Tuesday**.
- **Nemotron 3.5 ASR** — speech recognition (per NVIDIA Build materials accompanying this launch).
- **Nemotron 3.5 Content Safety** — content safety model (per accompanying materials).
- **NVFP4** — 4-bit precision format optimized for **Blackwell**; reduces memory + accelerates compute; single fallback-capable checkpoint.
- **NVIDIA Blackwell / B200**, **Hopper / H100**, **Ampere** — GPU architectures referenced for footprint + precision.
- **CUDA / CUDA-X** — software stack; skills/libraries usable as agent domain skills.
- **NeMo** — model customization/fine-tuning + lifecycle; **NeMo Gym** for RL environments + skills; **NeMo skills** resources.
- **Hermes agent (Nous Research)** — agentic harness/wrapper providing multi-model orchestration + self-learning skills; internal **`skill manage`** function; **Hermes curator** + **Collective Wisdom** skill library.
- **Open agentic harnesses** — **OpenCode**, **Hermes agent**, **OpenClaw**, **pi**.
- **Microsoft Foundry** — unified platform/control plane for models + agents + governance.
- **Foundry hosted agents** — BYO container/harness; agent identity; isolated sessions; lifecycle/versioning/auditing/compliance.
- **Foundry managed compute endpoints** — where Nemotron Super/Nano run in the reference deployment.
- **Foundry managed toolbox** — single control plane for tools + MCP servers (Outlook, GitHub, Teams, MongoDB, Cosmos DB, BYO MCP) with granular per-function permissions.
- **Foundry Agent Service** + **Foundry catalog** — session management + built-in service/MCP catalog.
- **Microsoft Entra ID** — agent identity, authentication, access management, audit/governance (e.g., IAM Reader on storage).
- **OAuth pass-through** — agent inherits the user's identity (PR commits attributed to the user).
- **Microsoft 365 / Microsoft Teams** — publish + interact with the agent; cross-session memory.
- **Evals/benchmarks referenced** — τ-bench-style agentic tool-use eval; **ServiceNow Enterprise Ops Gym** (long-horizon planning); coding; instruction following; knowledge work (PhD/MBA level); **Artificial Analysis** (3rd-party throughput/accuracy index).
- **Pricing sources referenced** — **CoreWeave**, **Deep Infra** (lowest-price selection for cost-efficient-frontier chart).
- **Comparison models** — GLM (5.x), Kimi K2(.6), Qwen 3.5 (named as strong open models).
- **Hugging Face** — distribution of open Nemotron checkpoints/datasets.

## 🚀 Announcements / What's New
- **NVIDIA Nemotron 3 Ultra** — largest + most capable Nemotron to date; **550B / 55B active**; frontier **reasoning + orchestration**; **1M-token context**. **Announced Sunday** (also debuted in the CEO's GTC keynote days earlier); **available Tuesday** on **Foundry managed compute** ("this month").
- **Multi-teacher on-policy distillation** — new training approach distilling multiple task-specialized teacher models into Ultra.
- **Single unified checkpoint** — one Ultra checkpoint runs **NVFP4 on Blackwell** and **falls back to Hopper**, replacing per-architecture checkpoint sprawl.
- **~5× faster inference** at frontier accuracy vs the March (Nemotron 3 Super) release (per Artificial Analysis), with more gains expected in the coming weeks.
- **Cost-efficient-frontier chart** — new framing (accuracy-per-cost on coding tasks) first shown at the GTC keynote, now extended to Ultra.
- **Companion model releases** (per NVIDIA's Build launch alongside this session): **Nemotron 3.5 ASR** (speech recognition) and **Nemotron 3.5 Content Safety**.
- **Ecosystem/partner work** — Nemotron tuned across open harnesses (OpenCode, Hermes, OpenClaw, pi); deep **Microsoft Foundry hosted agents** integration (toolbox, Entra ID identity, M365/Teams publishing) demonstrated live.

## 💡 Demos
**Demo 1 — Hermes "Collective Wisdom" (video).** A small company's product launch with **four senior leads** (two-week window). Each works with **Hermes agent on Nemotron 3 Ultra**; corrections become **reusable skills**; the **Hermes curator on Nemotron 3 Super** merges/de-dupes/rewrites/tests/promotes skills; approved methods (data stays private) join **Collective Wisdom**; months later the whole team is faster because **every captured method lifts everyone**. "*Hermes from Nous Research on NVIDIA Nemotron 3 Ultra.*"

**Demo 2 — Foundry hosted agent: email → PR → learned skill (live).**
1. New **Foundry Agent Service** session; agent self-reports **Nemotron 3 Super + Hermes harness**.
2. Delegated a real task from **Alex's email** (add chat-completions support to **LLM Perfbench**) **without pasting the email** — agent uses **Outlook + GitHub** (via Foundry) to find the email, make changes, and **open a PR** autonomously.
3. All services wired through **one Foundry managed toolbox** (Outlook, GitHub, coding sandbox; catalog incl. MongoDB/Teams/Cosmos DB + BYO MCP) with **granular allow/deny** (e.g., read Teams, no sending).
4. PR created; **full observability/trace** of tools, MCP servers, and steps (email → PR).
5. Feedback taught as a **reusable skill** (Alex = reviewer; docstrings required for LLM Perfbench) via Hermes' **`skill manage`** function.
6. PR verified (Alex added, docstrings committed); **OAuth pass-through** makes commits show as **Stephen**.
7. Agent **published to Microsoft 365 / Teams**; in Teams it **remembers the skill** created minutes earlier in a **different session** → memory persists **across sessions + services**.

## 📊 Notable Stats / Quotes
- **Nemotron 3 Ultra: 550B total / 55B active** parameters.
- **Nemotron 3 Nano: 30B total / 3B active** (MoE).
- **1,000,000-token context length** (Ultra and Super).
- **~5× faster inference speed** at frontier-level accuracy vs the March Nemotron 3 Super release (Artificial Analysis).
- **Footprints:** Nano → very small DC GPU; Super → ~1–2× H100 80GB; Ultra → ~2× B200.
- **Timeline:** Nano = December; Super = March; Ultra announced **Sunday**, available **Tuesday**.
- **Pricing inputs:** lowest of **CoreWeave** + **Deep Infra** for the cost-efficient-frontier (accuracy-per-dollar coding) chart.
- **Booth:** NVIDIA in the **308 space**, live Foundry + Hermes + Nemotron demo.
- Joey: "*the better the agents and the better the skills, the easier it will be to get your work done… we're just at the beginning of this journey.*"
- Joey (forward-looking): future candidates may ask "*what type of agents or skills are available at that company?*" when weighing job offers.
- Stephen: the value "*it's not just that your model can reason or that your model can write code. It's that Foundry gives you this infrastructure and this tooling and observability… to customize your agent and turn that model into a useful enterprise*" asset.
- Stephen (governance): you can grant/revoke/audit agent access "*using the same kind of controls that enterprises already rely on.*"

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Deploy a **Foundry hosted agent** (BYO container/harness) and wire **Outlook + GitHub** via a single **managed toolbox**; reproduce the email → PR flow.
  - Stand up **Nemotron 3 Super (or Nano)** on **Foundry managed compute** and benchmark prefill + multi-turn latency for an agentic loop.
  - Try **Nemotron 3 Ultra** when live (Foundry managed compute) for long-horizon/orchestration tasks; test the **1M context**.
  - Experiment with **Hermes' skill-learning** (`skill manage`) — teach a repo-specific skill (reviewer + docstrings) and verify persistence across sessions/Teams.
  - Grant an agent an **Entra ID** identity + **IAM Reader** on a storage account; validate **OAuth pass-through** attribution on GitHub commits.
  - Pull a single **NVFP4 Ultra checkpoint** from Hugging Face and confirm **Blackwell run + Hopper fallback**.
- [ ] Questions:
  - Exact GA/region availability + pricing for **Nemotron 3 Ultra** on Foundry managed compute (and quota/VM SKU requirements)?
  - Which **MCP servers** are GA in the **Foundry toolbox** today vs preview? Admin UX for per-function allow/deny at scale?
  - How does **Hermes curator** dedupe/merge/test skills technically, and what does enterprise **review/approval** for shared skills look like in practice?
  - τ-bench-style + **Enterprise Ops Gym** scores — exact numbers vs GLM/Kimi/Qwen? (slides referenced, not all read aloud).
  - Governance depth: audit log schema, session-isolation guarantees, data-residency for the cross-session memory store.
- [ ] Relevant to:
  - Anyone building **multi-agent / specialist-agent** systems on Azure/Foundry.
  - Enterprises wanting **open** frontier reasoning models with **agentic governance** (Entra ID, observability, isolated sessions).
  - Teams evaluating **cost-vs-accuracy** trade-offs across a **system of models** (frontier + Nemotron + local).
  - Platform/IT admins standardizing **agent identity + tool access** via a single control plane.

## 🔗 Related
- [[Build2026/]] — other Microsoft Build 2026 session notes
- NVIDIA Nemotron developer page · Hugging Face (open weights/datasets) · NeMo / NeMo Gym
- Nous Research — Hermes agent
- Microsoft Foundry — hosted agents, managed compute, toolbox, Agent Service
- Microsoft Entra ID — agent identities & governance
- Related Build sessions: "Post-Training and Deploying Open Source Reasoning Models in Foundry," "Turn foundation models into production AI on Microsoft Foundry"

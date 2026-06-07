---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/azure
  - topic/keynote
  - topic/foundry
  - topic/copilot
  - topic/agents
  - topic/windows
  - topic/quantum
  - topic/silicon
  - topic/security
source: https://www.youtube.com/watch?v=FFMm454fxNA
session_code: KEY01
event: Microsoft Build 2026
speakers: Satya Nadella (+ Jensen Huang, Mustafa Suleyman, Peter Steinberger, Stevie Bathiche, Cristiano Amon, Dr. Gianrico Farrugia, The Chainsmokers, + demo presenters)
duration_min: 143
aliases:
  - Satya Nadella Opening Keynote
  - Build 2026 Keynote
---

# KEY01 — Microsoft Build 2026 Opening Keynote (Satya Nadella)

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Satya Nadella + guests (Jensen Huang/NVIDIA, Mustafa Suleyman/Microsoft AI, Peter Steinberger/Open Claw, Stevie Bathiche, Cristiano Amon/Qualcomm, Dr. Gianrico Farrugia/Mayo Clinic, The Chainsmokers, plus demo presenters Kayla, Elijah, Cassidy, Amanda, Sarah, Tanaya, David)  
> **Duration:** ~143 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=FFMm454fxNA)

## 🎯 TL;DR
The 2026 Build keynote frames the entire conference around one question: how every developer can **participate fully in the frontier intelligence ecosystem** — not by consuming a single model or platform, but by compounding their own value on top of the stack. Satya walks the full AI stack bottom-up: **ubiquitous compute** (edge → cloud), a new **intelligence layer** (models + context + tools, branded as "IQ"), an **agent runtime** (Windows + Foundry), and the **tooling/security/governance** wrapping it all. Headline moves include on-device unmetered intelligence on Windows (new MAI Ion models, Surface RTX/DevBox dream machines, NVIDIA N1X SOC), Azure's Fairwater AI super-factory with NVIDIA Vera Rubin and Microsoft's own Maia/Cobalt silicon, **Project Solara** agent-first devices, the **Microsoft IQ** layer (Web IQ, Fabric IQ, Work IQ), **Foundry as a full agent application platform**, **Agent 365** governance, **Open Claw running natively on Windows** with new MXC isolation, and **seven new MAI models** plus a Mayo Clinic frontier health-model partnership. The throughline is "**humanist superintelligence**" and a "**hill-climbing machine**" / **frontier tuning** vision where each organization keeps and compounds its own tacit knowledge as a moat.

## 🔑 Key Takeaways
- The conference's single message: **participate in the frontier intelligence ecosystem** — value compounds on top of the platform, not in any one model/chip.
- The AI stack as framed: **ubiquitous compute fabric (edge+cloud) → models/context/tools layer → agent + app runtime → tooling + security/compliance/governance.**
- **Unmetered intelligence at the edge**: Windows ML/AI expanded to the full installed base of NPUs/GPUs/CPUs so every developer can build local on-device AI; new **MAI Ion Instruct** (reasoning) and **MAI Ion Plan** (planning) models run locally for a full agentic loop with no cloud round-trip.
- New hardware tier: **NVIDIA N1X** next-gen PC SOC (CPU+GPU+AI, unified memory, integrated DRTM); **Surface Ultra** (128 GB unified memory, ~2K display, all-day battery, this fall); **Surface RTX DevBox** "dream machine" (~1 petaflop AI, 20 CPU cores, 128 GB unified memory); Windows is coming to the **NVIDIA DGX (GB300) "desktop data center"** capable of running a ~1T-parameter model locally.
- The cloud driving equation is **tokens per dollar per watt**, optimized end-to-end "from electrons to tokens"; **community trust principles** (don't raise local electricity prices, responsible water use, local jobs/tax base, training & nonprofit investment) are the *first* design criteria before any tech.
- **Azure scale**: 500+ data center regions; more capacity added in the last 18 months than in the first decade; three dominant workloads now = **training, inference, agent runtime**.
- **Fairwater** = Microsoft's first AI "super-factory" (Georgia + Wisconsin), two-story dense-GPU architecture co-designed with NVIDIA; closed-loop liquid cooling → ~zero water consumption (yearly water ≈ one restaurant's usage); ~100 kW/rack power delivery rethought.
- **Silicon choice**: largest fleet of NVIDIA Grace Blackwell in the world; validating **NVIDIA Vera Rubin** (built for agents, low latency); **AMD MI** next-gen partnership; first-party **Maia 200** (~30% better tokens/$ vs leading GPU, will power M365 Copilot) and **Cobalt 200** CPU preview (~30% better than prior Cobalt; agent traces show ~33% lower latency, ~14% faster, ~23% higher throughput).
- **Project Solara**: a turnkey platform for **agent-first purpose-built devices** — "the next computer is all your devices working as one system." Three pillars: enterprise-ready (AOSP-based Microsoft Device Ecosystem Platform), agent-driven just-in-time UI, and bring-your-own-agent extensibility; unified by Azure. Two device categories previewed — a stationary desk device (MediaTek) and a portable **agent access badge** (Qualcomm).
- **Microsoft IQ** = the unified context layer: **Web IQ** (LLM/agent-native web grounding, MCP-native, model-agnostic, best-in-class quality/speed/cost), **Fabric IQ** (live operational ontology of the business), **Work IQ** (people + procedures grounded in M365/SharePoint, always current).
- **Foundry** becomes a **full application platform for the agent era**: Foundry-hosted long-running agents with IQ layers, durability/memory/state, fast sandboxes, auto-generated rubrics/evals, built-in self-improvement loop; 121k+ models in the catalog (largest), now including OpenAI realtime voice + Claude Opus 4.8, MAI models, plus new **Fireworks AI** open-weight partnership.
- **Agent 365** is the **agent control plane** — agents get their own identities/access controls; Defender extended for real-time agent defense, Purview for data protection/compliance; works across AWS/GCP and any framework; **Agent 365 SDK now GA** and extended to local Windows agents.
- **Open Claw now runs natively on Windows** using new **Microsoft eXecution Containers (MXC)** OS-native isolation; Peter Steinberger announced an **Open Claw Foundation** (nonprofit, any model/any OS), pluggable harness (Copilot/Codex/etc.), folder-level permissions, and "you can run it inside your company now."
- **Copilot becomes a super-app**: chat + Cowork + code unified by summer; new **Autopilots** ("enterprise-grade claws") — autonomous long-running agents with identity, personality, memory, running in your tenant; first autopilot is **Scout** (available now on Copilot Frontier).
- **Mustafa Suleyman / MAI** announced **seven new models** (image, voice, transcription, reasoning, coding) built toward **humanist superintelligence**; codesigned with Microsoft's own Maia silicon for a further ~1.4× perf/watt.
- **Frontier tuning** + **RLEs (reinforcement learning environments)** let every org build its own **"hill-climbing machine"** — private evals, traces, tools, rubrics, and even custom-trained models become *your moat*; only you keep the resulting model and benefits.
- **Mayo Clinic** partnership: co-creating a **frontier health model** to deploy in their hospitals and beyond, encoding decades of clinical practice (not just textbook knowledge), with patient-first, safe/secure/trustworthy framing.
- **Microsoft Discovery** went **GA** — an agentic scientific-discovery loop (models + HPC compute + scientific knowledge graphs + automated lab + simulation); demoed enzyme/protein design for true plastic recycling, sending real DNA sequences to an automated lab.
- **Quantum**: announced **Majorana 2** — topological qubits with ~20 seconds to ~1 minute coherence lifetime (~1000× Majorana 1), same tiny qubit form factor (~1/100th mm), digital control, path to ~1M qubits on a credit-card-sized chip; **Q North** quantum computer coming (Atom Computing neutral atoms + Microsoft stack).
- Satya's closing North Star: two possible stories about technology — concentrating power vs. unlocking opportunity for developers/scientists/enterprises/communities — "**Our job is to make the second story true.**"

## 📚 Detailed Notes

### Opening Vision — "Participate fully in the frontier intelligence ecosystem"
Satya opens back in San Francisco, framing developer conferences as the place to understand tech shifts, the new stack, and the new opportunity for developers, their companies, and the broader world. **The single key takeaway:** *How do you all participate fully in this frontier intelligence ecosystem?* It's explicitly **not** about any one piece of technology or even the platform itself — it's about the **value you can build, compound, and create on top of the platform.**

He lays out the **AI stack** the conference will unpack:
1. **Ubiquitous compute fabric** spanning the edge and the cloud.
2. The **emerging intelligence layer** — models + context + the tools models can access.
3. The **runtime** where you deploy the agents and applications you build on the content/model layer.
4. The **best tooling** to do all of this, wrapped in **security, compliance, and governance.**

He then walks the stack bottom-up, starting at the very edge: **Windows.**

### The Edge — Windows as the place to build local, unmetered AI
The amount of compute at the edge is "astounding" — every NPU, GPU, CPU, every PC. Microsoft is already delivering on-device AI: **Outlook Summarize** uses onboard local AI, **PowerPoint** all-text, **Teams super-resolution** — and it's not just Microsoft: **Adobe After Effects / Premiere** use **Windows ML** too. Microsoft is **expanding the scope of Windows ML and Windows AI** so developers can reach the **full installed base of GPUs** — build once for local onboard AI and run it across the entire install base.

Two new local models announced for Windows:
- **MAI Ion Instruct** — a strong reasoning model.
- **MAI Ion Plan** — a planning model.

Together they give a **full local agentic loop**: give the models tool access and build fully agentic applications **without a round-trip to the cloud.**

**Hardware ecosystem** pushing "unmetered intelligence":
- **Intel** — exciting new silicon.
- **Qualcomm** — two announcements: high-end **Snapdragon X** and a lower-end part for **sub-$500 PCs.**
- **NVIDIA N1X** — next-gen **SOC for PCs** bringing CPU + GPU + AI capabilities into a single SOC, with **unified memory architecture** and **integrated DRTM**.
- **Surface Ultra** — built on the NVIDIA platform, **128 GB unified memory**, beautiful ~**2,000 (2K) display**, **all-day battery life**; shipping this **fall**. Many OEM partners are building exciting machines on the new platform/SOC.

Pushing the architecture to its limit for developers → **Surface RTX DevBox** ("dream machine"): **1 petaflop of AI compute**, **20 CPU cores**, **128 GB unified memory access** (there's a wait list — Satya jokes he's on it). And going further: **Windows is coming to the NVIDIA DGX (GB300) station** — a "**desktop data center**" that can run a **1-trillion-parameter model locally**, "close to what we had when we built GPT-5 / one of the first supercomputers."

Extending developer endpoints to the cloud: **Windows 365** with a developer distribution optimized for developer productivity (Satya uses it daily). The goal: make Windows — laptop, desktop, or cloud — **the best place to build.**

**Windows developer experience updates:**
- A **distraction-free dev environment**.
- An **intelligent terminal** with built-in **GitHub Copilot** intelligence.
- Lots of **Linux love**: **70+ utilities** coming to Windows; **Homebrew on native**; first-class **container** support for local development.

### Demo — Kayla: Windows dev tooling on Surface RTX DevBox
Kayla shows the default experience on the **Surface RTX Spark DevBox** — calm, no news feed/widgets/notifications, dark mode. Highlights:
- **Vertical task bar** announced for Windows Insider build (popular demand), set via PowerToys-built run/command palette.
- DevBox ships with tools pre-installed (Python, Node); the **config file is published in a public repo** so anyone can reproduce the setup (applies Windows adjustments + installs tools).
- **PowerToys "Grab and Move"** — hold a key and move windows from anywhere; **End Task** to kill a process without Task Manager.
- **Dev Drive** with Defender running async for authorized performance; Git-aware shell (file status, branch name bottom-left).
- **Intelligent terminal** lets you pick your favorite agent (she uses GitHub Copilot); terminal pane on top, agent pane on bottom; the agent **detects errors and proposes fixes**.
- Building **Open Claw** using a **WSL container** — native container experience on Windows that can **leverage the GPU** and reference existing container files (e.g., the one in the Open Claw project); opened in **Microsoft Edit** with syntax highlighting.
- A **WSL profile** comfortable for zsh/csh/Homebrew users with favorite utilities (incl. **btop**), available in the repo.
- **Large local models for coding**: ran a **120-billion-parameter model** most machines can't load; **3.4 million tokens** used locally on-device.
- Kicking off agents using **Fleet**; **Copilot voice** feature (local model) to delegate: "find any `Console.WriteLine` calls and convert them to the standard logger." The **main agent delegates sub-agent tasks of appropriate complexity to the local model**, using the GPU and making it cost-efficient.
- **75+ command-line utilities** added to Windows (on top of curl, etc.) — `grep`, `head`, `tail`, `touch`, etc.
- **MAI Ion Instruct** continuously analyzing log files locally for instant diagnosis — no token-usage worries since it's all local.
- Machine resources: **~90 GB of RAM** utilized by the GPU using the full power of RTX Spark — multiple local models running simultaneously, unmetered, "without a hitch."

The point proved: **on-device unmetered intelligence** — models and agents working in parallel to you, locally, as a first-class Windows capability.

### The Cloud — "Electrons in, tokens out" and community trust first
Driving equation: **tokens per dollar per watt.** Microsoft thinks of the systems problem as **electrons coming in one end, tokens out the other**, optimizing end-to-end: data center design itself (core compute/storage/network), accelerators for each component, **DC-to-DC connectivity and networking**, and offload to the edge.

**Before** any tech, the most important design criterion is **earning permission from the communities** where data centers are built. Grounding principles:
- **Don't increase local electricity prices.**
- **Responsible water use.**
- **Create jobs for local residents.**
- **Add to the tax base.**
- **Strengthen communities** via local training investment and area nonprofits.

Only after living up to those principles does the hard innovation work happen.

**Azure footprint:** more than **500 data centers / regions** — the most expansive hyperscaler footprint. **More data center capacity added in the last 18 months than in the first decade.** Built for **heterogeneous workloads** across the enterprise, with **three dominant workloads**: **training, inference, and the agent runtime.**

**Fairwater** — Microsoft's first **AI super-factory**, spanning two regions (**Georgia + Wisconsin**), designed from the ground up for AI, co-designed closely with NVIDIA:
- **Two-story architecture** to densely pack GPUs with network access → higher performance networking, lower latency, more bandwidth across the cluster.
- **Power delivery rethought**: how to deliver **~100 kW/rack** with minimal conversion loss from grid to silicon.
- **Cooling/water**: closed-loop liquid cooling — the loop is filled once and the DC operates effectively with **zero water consumption**; daily water usage over a full year ≈ what a **single restaurant** uses.

**Silicon — lots of choice (first-party + partners):**
- First cloud to bring up NVIDIA; **largest deployment of NVIDIA Grace Blackwell in the world.**
- **AMD** partnership — working on next-gen **AMD MI** GPU.
- **Maia 200** — first-party accelerator, continuing to scale, live in Arizona, deploying internationally; **~30% better tokens/$** vs the leading GPU today; validated with **GPT-5.5**; will **power Microsoft 365 Copilot**.
- For running agents, **CPU is critical** — accelerator-to-CPU ratios may approach 1:1. Hence **Cobalt 200** CPU **preview** — next-gen, designed for cloud-native and agent workloads; **~30% better than Cobalt** on cloud-native; using **GitHub Copilot agentic traces**, agents show **~33% lower latency**, **~14% faster speed**, **~23% higher throughput** — a co-design of AI accelerator + CPU for agents.

**Networking:** rebuilt how traffic moves across Azure to support **synchronous data workloads spanning tens of thousands of GPUs** that must stay coherent — the next frontier of network scaling, both inside and across continent-spanning data centers, creating a **fungible compute fabric.**

### Guest — Jensen Huang (NVIDIA), live from Taipei
Satya brings on **Jensen Huang**, calling NVIDIA the best company and Jensen the best person to talk systems + AI. Key points:
- The collaboration started **~3 years ago** with a conversation about a new class of PCs incredible for designers/creators *and* AI — processing capability plus an integrated software stack. Three years later: a new chip + the new Windows software, with **autonomous agents running on the PC.**
- Over ~30–40 years (from inventing **DirectX** together to today), the **PC evolved from a tool to a tool used autonomously by an AI assistant** — "personal computer → personal AI." Jensen's vision: text your PC while traveling, it fires up the tools, makes the changes/design, and iterates with you while you're away.
- **RTX Spark**: ~**1 petaflop** of AI performance in **NVFP4** numerical format (a format the companies developed together), exploiting **128 GB memory** to fit a **couple hundred billion-parameter model** — state-of-the-art; "a really smart assistant running on the PC is here."
- **Data center journey**: **Hopper** (pretraining) → **Grace Blackwell** (post-training, RL, reasoning models / mixture-of-experts; the whole **NVL72 rack became one computer**) → **Vera Rubin** (built for the **agentic** era). Fairwater described as magnificent, liquid-cooled, closed-loop, near-zero water, environmentally friendly, increasing token generation rate and **reducing cost per token by ~an order of magnitude (~30× over Hopper).**
- **Vera (the CPU)** designed for **extremely low latency** — "in the past CPUs were designed for humans; agents want low latency." The whole disaggregated/distributed system: storage = long-term memory, working memory; **data encrypted in transit, at rest, and in use.**
- Both teams aligned **long before chips taped out** — Microsoft stood up Vera Rubin systems the moment they rolled off the line.
- On the broader opportunity: it's about creating opportunity for **every developer and organization** to build on the platforms. NVIDIA software/models will be in **Foundry**; NVIDIA software accelerates Microsoft workloads (data warehouse, etc.). **GitHub commits have gone "parabolic" — up ~3× in the last several months** — proof agentic systems are useful, productive, and profitable. NVIDIA + Microsoft are making **all agent tools fully GPU-accelerated** (Fabric, data processing, SQL, Spark, semantic/graph) because **"agents are impatient"** — faster iteration = more profitable, intelligent tokens.

### New Form Factors — Project Solara (agent-first devices)
Satya reflects on Jensen's weekend photo of all the desktops — "I'm back in the 90s" — the same beloved form factors with **unbelievable new function** thanks to onboard AI. That sets up the next question: if you can put new function into existing form factors, **can you purpose-build new form factors for the new function? Can you build a new platform for the agent era?** → **Project Solara.**

A cinematic video frames it: agent-first devices that come forward when you approach, understand your speech, surface what matters and let everything else fall away, keep going when you want, "light the path / clear the way."

**Stevie Bathiche** ("Stevie") presents the "why," referencing his **Build 2023** talk on outside-in AI infrastructure that moves within the application frame to operate globally, **maintaining context across workflows, devices, and timescales.** The big insight for Solara: **don't choose one form factor — create a system that extends your agent across a constellation of devices.** *"The next computer is all of the devices working together as one system, with agents closer to where and when you need them."*

Two challenges Solara solves:
1. Specialized form factors exist but rely on **custom one-off apps and fragmented stacks** — hard/expensive to build, deploy, maintain.
2. Organizations are already building **deeply specialized agents** whose impact is **constrained by where they can exist.**

**Solara's three pillars** (unified by **Azure** across cloud + device):
1. **Enterprise-ready** — built on the **AOSP-based Microsoft Device Ecosystem Platform.**
2. **Agent-driven interaction model** with **just-in-time UI** that adapts to the form factor.
3. **Extensibility** — **bring your own agents.**

**Two device categories previewed:**
- **Stationary (desk) device** — built on **MediaTek**; **Windows Hello for Business** signs you in by walking up, giving direct, frictionless-yet-protected access to **Microsoft 365 Copilot grounded in Work IQ**; surfaces "what matters next in your workday," lets you delegate tasks to your agent with a tap or voice. A dedicated **ambient device for work** that acts as a companion to your existing **Windows Copilot+ PC** or accesses **Windows 365** on a connected monitor. (Demoed by Nathan.)
- **Portable — an "agent access badge"** — re-imagining the access badge millions wear daily; built using **Qualcomm** silicon, lightweight, designed for **agents on the go**, adaptable across verticals/workflows. Demo: unlock with fingerprint → all your agents securely available → "gather content for a social media post," hit record, the badge's camera captures, the agent finds/cleans up the best shots and sends them to the team for review — fully agent-driven.

**Vertical examples & flexibility:** With small changes (different agent, shape, screen size, sensors, input methods), the *same foundation/software* adapts to **retail, industrial, hospitality, financial services, legal**, and more. **Healthcare** example: a small wearable where the right agent shapes the experience around role/workflow — check-ins, patient records, critical insights via enterprise-grade secure access; built-in mics enable hands-free voice documentation (incl. diarization/annotation); a side-facing camera captures vitals, scans medications, verifies workflows — bringing intelligence into the flow of patient care while the nurse stays present with the patient.

**Named early explorers:** **Accenture, Best Buy, Target**, and others are exploring how these devices can improve their workflows. The broader opportunity: *agents moving outside the app and taking shape in devices designed for a specific scenario, customer, and place* — "imagine where your agent should live, what form it should take, and what new work it can unlock."

### Guest — Cristiano Amon (Qualcomm)
A recorded device-lab conversation between Satya and Qualcomm CEO **Cristiano Amon** on the platform shift from building OSes/devices **for apps** to building **for agents**:
- **Agents change the nature of the device.** As AI understands the world the way we do, computing moves **closer to our senses** — eyes, mouth, ears — into things we **wear**; you need silicon geared toward **real-time context**, from silicon to cloud.
- Requires a **power-efficient CPU** and a **cloud-native experience** with many **sensors** for personalization — a fundamental change in the nature of devices; the wearable platform itself is changing.
- The key shift: today the **smartphone is the center** of digital life and other devices extend it, which pushed vertical (single-company) platforms. With agents, **the agent becomes the center** of the digital experience — and agents will want an **open, horizontal platform** that lets them interact with the **best possible device for each application.** The goal: make it possible for any agentic system to live across **many devices** carrying that intelligence — an **open ecosystem** built together. "That's just the beginning."

Satya's takeaway: new platforms mean **new platform rules** that don't hem in the form factors where agents live — "when new platforms come, you get to rewrite the rules of how platforms operate." Solara gives developers/enterprises the flexibility to imagine the form factors they want and make agents **ubiquitous.**

### The Intelligence Layer — models + context + tools
Moving up the stack to a **new intelligence layer** bringing together **models, context, and tools.** It starts with **model choice** — every customer/developer chooses the right model for the right task, eval mix, and agency/budget. **Foundry has 121k+ models** ("the largest model catalog out there") — from **OpenAI** to **Anthropic** to **MAI** models. Last week Microsoft brought **OpenAI realtime voice models** and **Claude Opus 4.8** to Foundry, continuing to bring frontier models.

**Context starts at the data tier.** Data has historically been built for user-facing applications; now it must be **rebuilt for agents** (different call patterns even at the data tier). Agents are continuously **storing, retrieving, reasoning, acting, and learning** — using **Cosmos DB** (as ChatGPT does), **Azure Search** retrieval of indices, **Fabric real-time intelligence** as the business-logic tier for agents.

New data services announced:
- **"Verizon DB"** *(caption-uncertain name — described as a fully managed PostgreSQL/SQL service on Azure; likely a garbled product name)* — ground-up managed Postgres service for **high availability and scale-out**, **automated failover**, **128 TB per cluster**, built for read-heavy workloads; internal testing shows **~3× throughput vs PostgreSQL.**
- **Data warehouse with GPU acceleration in Fabric** — for a world where agents constantly query data on the fly; **~7× performance gain** bringing AI acceleration to Fabric.

**Microsoft IQ** = the **IQ layer** that mixes model capability with data to deliver the **right context** and unlock intelligence. **Token efficiency** is framed as *the* key consideration: structure the context right and feed the models well, and you are by definition far more token-efficient.

**Web IQ** (announced): LLM/agent-native **web grounding** built on Microsoft's global infrastructure already serving **1B+ users**, but **fundamentally re-architected** for LLM/agentic workflows — **model-agnostic, MCP-native**, plugs into any agent runtime; covers **web, news, images, video** so agents ground responses in **fresh, verifiable** content. **Best-in-class on all three criteria: quality, speed, and cost.**

Beyond the web, Microsoft unifies **Foundry + Fabric + Microsoft 365** as a unified IQ layer — a continuously updated understanding of your organization. The three sub-layers:
- **Web IQ** — external, fresh web grounding.
- **Fabric IQ** — a **living operational ontology** of the business (the grid, the operation) coupled with **live telemetry**, reflecting real state minute-by-minute; extends models used by millions of customers into rich ontologies.
- **Work IQ** — **people + procedures** grounded in **M365/SharePoint** playbooks, **always current** (no re-uploads, no stale versions; when the procedure changes, the answer changes). *Critically: this is your knowledge — the assets you create stay with you regardless of which model/agent reasons over them.*

### Demo — Elijah: Microsoft IQ in a power-utility control center
Elijah ("agents are only as good as the context we give them") demos a fictional utility, **Brightline**, in a grid-operations control center:
- Kicks off a **long-running agent** to assess a grid incident and produce a brief, built in **Foundry** and wired to a **Foundry IQ knowledge base** (a single grounded source packaging documents, operational data, and people), then **published to Microsoft 365** for the whole team.
- In M365, asks about **current electricity prices in SF** — the agent pulls **Web IQ** to ground in fresh official sources.
- Asks about **at-risk substations** — the agent pulls **Fabric IQ**: Brightline's grid as an operational **ontology** + live telemetry, returning a table of most-exposed substations.
- Asks **"what are the steps to respond to a substation trip"** — the agent pulls **Work IQ**: Brightline's response procedure in **SharePoint**, answered from the same source the team maintains daily (not a stale snapshot).
- The **long-running agent** finishes: it used Web IQ (outside) → Fabric IQ via Foundry (state of operations) → Work IQ (people + procedures), and even **alerted Elijah directly in Teams** with a brief. With **Foundry routines** this can run on a **schedule** — turning a one-off response into **continuous, proactive execution.**

**Point proved:** *"When the crisis hits, teams don't chance an answer — they get an answer, all in one place they can trust."* The combination of external + internal context (Microsoft IQ) is what makes agents reliable.

### The Agent Runtime — Windows + Microsoft eXecution Containers (MXC)
Moving from context to **deploying agents** — you need a first-class **agent runtime**, shipping in both **Windows** and **Foundry/Azure**. Agents are a **new execution environment / paradigm**: they reason continuously, **generate and run code dynamically**, and act across files, devices, and the network — powerful, but it creates **new risk.**

**Microsoft eXecution Containers (MXC)** — a new **policy layer** that lets Windows apply **isolation and containment using OS-native primitives** (baked into the OS so containment is **policy-enforced**):
- **Process-level isolation** for lightweight agent actions.
- **Session-level isolation** for user separation across Windows and Linux machines (incl. **WSL**) for stronger boundaries.
- **Windows 365 for agents** — **maximum isolation** in a separate managed environment.
Pick the right containment option per workload; Windows enforces it **regardless of who builds the agent.** Partners are engaged; **NVIDIA is bringing Open Shell** *(caption-uncertain phrasing)* to Windows.

### Demo — Scott, Samantha & Peter Steinberger: Open Claw native on Windows
Microsoft announced **Open Claw running natively on Windows leveraging MXC.** Scott and Samantha demo a new **Open Claw Windows companion app** (alpha):
- Open Claw "came out in November of last year and took the world by storm"; people use it for health/blood-sugar tracking, triaging email & GitHub issues, buying movie tickets, even as a **triathlon coach** building a work-back plan from personal data.
- The companion app is a **native Windows app** with info about the gateway, other machines, sessions, usage; quick access to chat, Canvas, the main dashboard; **full chat support with tool calling**; sandbox configuration in the corner.
- **Sandbox uses MXC** (process isolation; newer Windows versions will add more containment options). One-click security settings plus **custom folder permissions** — granular control over files/folders Open Claw can access, plus features like clipboard access or internet access.
- **The "scary" test:** they give Open Claw read-only access to the desktop folder, then ask it to **delete all files on the desktop.** Even with **all of Open Claw's own safety layers turned off**, **MXC's read-only sandbox** (set by IT/Samantha) blocks every deletion attempt — the files stay safe ("Foiled again!"). The point: **OS-enforced containment** holds even when the agent tries hard and its own guardrails are disabled.
- The work was done on a calm Windows dev machine with WSL, containers, containment, and **GitHub Copilot with multi-model support**.

**Peter Steinberger** ("the claw father himself", creator of Open Claw) joins:
- He built Open Claw to have access to **everything** — files, machines, chats — always-on and **fully open source**; that power made companies nervous ("Peter, I love my claw — can I use this at work?").
- The last few months' work (with **Microsoft, GitHub, OpenAI, NVIDIA** among others): **observability, auto-mode for permissions**, changed how access works — **"not all or nothing anymore"** (pick read-only or hidden folders). **"You can run it inside your company now."**
- Made the **harness itself a plugin** — bring your own (**Copilot, Codex**, whatever you trust) and your rules come with it; plus **persistent memory, heartbeats**, and a claw inside **Slack or Teams.**
- Announced the **Open Claw Foundation** — a nonprofit; **any model, any operating system** — "a new era of building agents, more capability for people who don't code, more power for those who do… Come build with us."

This was the first time Open Claw ran on a **Surface Ultra**.

### Foundry as a Full Application Platform for the Agent Era
Moving from edge to cloud: **Foundry** is becoming a **full application platform** — the cloud stack for the agent era:
- **Foundry-hosted agents** as a runtime for **long-running agents**, with all the **IQ layers**, tools, **durability, memory, and state**, and a **super-fast sandbox** you can spin up.
- **Generate rubrics and evals**; full **safety/guardrails** around the agentic system.
- A **continuously improving / self-improvement loop** built in — agents that **keep getting better.**
- New partnership with **Fireworks AI** — bringing their **open-weight models** to Foundry plus a great inference stack, with Foundry's enterprise guardrails/governance.

### GitHub as the Agent Control Plane + the new GitHub Copilot app
GitHub is becoming **the control plane for all agents** (as Jensen noted). Nearly everything measured on GitHub — repo creation, PR activity, API usage, Actions — is **accelerating** because of agentic workflows; the new scale is **humans + agents collaborating**, exposing tooling across every form factor. **CLI** growth has been tremendous (approachable + natural language), but **hundreds of CLIs don't scale** — too much cognitive load with 100 sessions open.

So Microsoft built the **new GitHub Copilot app** — the speed/flexibility of a CLI, the capability of an IDE, and the ability to **scale to an infinite number of agent sessions** — "your home base for development and operations."

**Rayfin** — an **agent-first SDK** that connects agents to the **backend-as-a-service** (identities, storage, database schemas) — "code is easy to generate, but what about the backend?" Brought everywhere you build. Partnership with **Replit**: build an app in Replit while the app + data deploy into an **enterprise-managed Fabric tenant** via the Rayfin SDK; available now for any tool to use as a backend.

### Demo — Cassidy: GitHub Copilot app, Canvas & Rayfin
Cassidy demos the **GitHub Copilot app**:
- Home screen kicks off new agentic coding sessions (you can drag **Mona** around — there's a hidden game).
- Reviews release blockers and **kicks off a separate session for every issue** using **Git worktrees** (isolated environments) so agents work in parallel without stepping on each other.
- **Agent merge** — Copilot babysits a PR through CI checks, code review, and merge conflicts.
- A **Work** view shows all activity (projects, PRs); **Automation** has reusable sessions (local or cloud), including a real, "load-bearing" **issue-poetry** session (joke).
- **Sessions**: add any repo/open-source project, start a session anywhere; integrated **browser + chat**, light/dark toggle, a **"pick and polish"** button to refine UI ("add reordering to this list" → it just works).
- **All popular models via one GitHub Copilot subscription** (OpenAI, Anthropic, Google); model change is easy; **"rubber-duck review"** — a session using **GPT-5.5** can request a review from **Claude Opus 4.8** to catch each model's blind spots.
- **Canvas** — "working with AI in 2026 should be more than chat"; an agent can **build a custom UI** to communicate with you (e.g., a camera-driven canvas where you thumbs-up/down to approve PRs). "IDEs that have UI — come full circle."
- **Rayfin deploy**: a 100% agent-built, containerized signal-box app with a database backend deploys to enterprise via **`rayfin up`** — hosted on **Microsoft Fabric**, giving agents a complete enterprise backend. *"This app is not just another session manager — session managers make it easy to create work; this helps you finish it."*

### Agent 365 — the agent control plane (govern, observe, secure)
**Agent 365** is the **control plane** for agents at scale. Agents need their **own identities and access controls** even when working on your behalf (work-on-behalf identity enforced):
- **Defender** extended for **real-time agent defense.**
- **Purview** extended for **always-on data protection and compliance.**
- Agents can be **hosted everywhere** — **AWS, GCP**, not just Azure — and built with **any framework.**
- Announcements include **GA of the Agent 365 SDK**, expanded to **local agents running on Windows** and elsewhere (and the claws shown earlier).

### Demo — Amanda: Foundry from local to enterprise-ready
Amanda shows how **Foundry** makes integrating + governing agents easy:
- Built a **LangGraph agent** locally; **Foundry Tool Box** — add tools once, any agent consumes them through a **single MCP endpoint**; governance applied once (a **guardrail blocking PII leakage**) protects all agents.
- **Deploy with one block of code** → push → **GitHub Actions** takes over; then use the agent in the Foundry extension.
- Each session spins up a **dedicated microVM** with its **own persistent file system** (the agent literally writes to a file you can see in the Files tab); **server-side traces and evals** show exactly what happened on every run.
- **Rubric evaluators** (brand-new): one command, **Foundry reads the agent and generates evaluation criteria** (a personalized rubric with dimensions like governance, outcome correctness, prescribed source usage) **from production traces** — then scores the agent.
- **Agent optimizer** (brand-new): tunes four things — **model, instructions, tool descriptions, and scales** — generates improved **candidates**, scores each with the rubric, shows strategy/scores/exact changes, and deploys the best as a **new agent version.** Every run feeds the next eval — *agents get better the more they're used.*
- Published the agent to **Teams + M365 Copilot** as an **autopilot agent** (its own identity + productivity license, works across M365 on its own behalf), living in the team's Teams group chat to catch the user up on missed updates.
- **Governance first:** every autopilot agent requires **admin approval**; admins review, choose who can talk to it, monitor it, and block it at any time — every agent managed with the same rigor as users/apps. *"You build the agent; we handle the rest."*

### Defender Security Harness — "MDASH" (AI defending against AI)
Last month Microsoft announced a **multi-model agentic security system** — an **agent harness for security** (referred to as **"MDASH"**, caption-uncertain spelling) that brings together **~100 agents** across frontier + custom models to find **exploitable bugs** better than any single model. It debuted on top of the **CyberGym** *(caption-uncertain)* benchmark.

### Demo — Sarah: MDASH finding & fixing vulnerabilities
Sarah shows results of a scan run from the **GitHub Copilot app** on a local dev machine (the system also runs as a standalone CLI):
- Results broken down by **vulnerability, demands, and severity**; finds traditional issues (coding errors, hard-coded secrets) **plus AI-specific vulnerabilities.** Under the hood: **100+ specialized agents discover, debate, and prove exploitable vulnerabilities end-to-end.**
- Generates a **log + HTML report** for management; **`defender details`** to dig into each vuln (what/where/severity).
- **`defender fix`** — remediates directly in the local dev environment; review the diff (human-in-the-loop), or create a **PR** to push to the repo; output can upload to tools like **GitHub Advanced Security.**
- A real vulnerability found by Microsoft's security-research teams using MDASH: a bug spread across **three different parts** of the codebase — no single file looks wrong (even a developer comment claims "everything is fine," which fools normal scanners/single models). **MDASH wasn't fooled**: one agent team spotted the gap, another argued it, a third built a working crash example — joined-up reasoning that previously required significant manual research. **Coming soon to the CLI and Microsoft Defender portal.**

### Guests — The Chainsmokers (Alex Pall & Drew Taggart, Mantis VC)
A lighter interlude: **Alex Pall and Drew Taggart of The Chainsmokers**, now general partners at their VC firm **Mantis** (~7+ years; ~14 years as a duo). They met founders from the consumer/mobile/cloud-era startups, fell in love with early-stage investing, institutionalized in **2020**, and focus on **B2B SaaS.** On the opportunity: AI is moving **"from producing outputs to producing actions"** — reimagining the entire architecture of enterprise software (machines, not humans, producing outputs). Advice to founders mirrors making music: find your **authentic** "sound," stay connected to the product, and **iterate** relentlessly to lock in your fan base. They agreed to **play a set at 6 p.m.** for attendees.

### Copilot Ecosystem — discovery, super-app & Autopilots
For any builder (AI-native company, SaaS, or enterprise), **job one** is making your plugins/agents/AI apps **discovered through the Microsoft ecosystem** — Windows, Microsoft 365 Copilot, Teams, GitHub. Line-of-business apps/agents built with **Copilot Studio** are discoverable as part of the Copilot experience. **Teams** has become the destination for **multiplayer, human-to-agent** interaction.

**Copilot's evolution:** started as **chat** (best models + Work IQ) → **Cowork** (a new way of working: generate stunning artifacts, solve multi-step problems, assign multi-step tasks) → **GitHub/code** → by **summer**, **coding comes to all knowledge work in one Copilot "super-app"** (chat + Cowork + code in one Copilot).

**Autopilots** (brand-new) — think **"enterprise-grade claws"**: autonomous, long-running agents with **full enterprise compliance** running **in your tenant**, with a **name, personality, custom connectors, context, and memory** — to reduce toil. The **first autopilot is Scout** (joins group chats/Teams, handles threads in Outlook) — **available today on Copilot Frontier**; over coming months this builds out to a **complete digital team of autopilots** inside Copilot.

### "The Future of the Firm" — tacit knowledge & the hill-climbing machine
What makes any organization unique is its **tacit knowledge**, continuously compounding through operations. The key question in an AI age: **"What is the future of the firm?"** — how do you preserve and compound tacit knowledge when models can learn anything from the data/trajectories they see? The answer: every organization should build its own **"hill-climbing machine"** — a system that **continuously improves against your objectives and private evals, compounding *your* advantage over time — not someone else's.**

### Guest — Mustafa Suleyman (Microsoft AI): Humanist Superintelligence & 7 new MAI models
**Mustafa Suleyman** takes the stage to supercharge **frontier tuning** with innovation from Microsoft's **superintelligence lab (MAI)**:
- Since he started in AI, training compute for frontier models has increased **~1 trillion-fold** — **12 orders of magnitude in ~15 years** — and **~3 more orders of magnitude** are coming in the next few years. **Scaling laws are clearly holding**; "long, linear hill climbing is the norm."
- **Humanist superintelligence**: state-of-the-art AI **explicitly designed to serve people and organizations, not replace them** — placing **humanity first**, prioritizing human well-being and progress. As a platform company, the job is to keep developers building at the **absolute frontier.**

**Seven new MAI models** (image, voice, transcription, reasoning, coding):
1. **MAI Image 2.5** and **MAI Image 2.5 Flash** — a step change in quality, now **#2**, surpassing the core of **Nano Banana 2**; precise editing with control/consistency; Flash for efficient production, 2.5 for maximum fidelity. **Live in PowerPoint today**, rolling out to **OneDrive**, on **Foundry** at market-leading quality-per-dollar.
2. **MAI Transcribe 1.5** — "the best transcription model in the world," SOTA accuracy across **43 languages**, beating Gemini and OpenAI flagships, **~5× faster**; integrated in **GitHub, Copilot, Dynamics 365 Contact Center**, and **Foundry** (fastest, most efficient, most cost-effective transcription of any hyperscaler).
3. **MAI Voice 2** + **Voice 2 Flash** — latest speech generation; beautiful prosody, natural delivery, fine-grained control in **15 languages** (more coming); Flash for ultra-low-latency voice ("the biggest thing in 2026").
4. **MAI Thinking 1** — first **reasoning** model; **35B active-parameter MoE** ("medium weight class"); independent human raters on Surge **prefer it over Sonnet 4.6** in overall quality; **97% on AIME 2025**; **53% on SWE-bench Pro** (alongside Opus 4.6 on the toughest coding benchmark). Notably **climbed entirely "from the bottom"** — **no benchmark-specific targeting, zero distillation** — giving **clean, commercially licensed data lineage** for trustworthy production use.
5. **MAI Code 1 Flash** — inference-efficient coding model tuned for **VS Code and GitHub CLI**; **51%** on a coding benchmark despite only **~5B parameters** (close to Haiku in size but cheaper), rolling out **inside VS Code.**

**Distribution & openness:** alongside Foundry + 1P-product optimization, models are available on **OpenRouter, Fireworks, and Baseten** — for the first time you can **tune the weights directly yourself** in your ecosystem of choice.

**Safety & silicon codesign:** built-in from the start — voice models have **anti-cloning protection**, **everything watermarked**, reduced refusals, plus a **detailed technical report** for transparency. MAI models are **codesigned with Microsoft's own silicon**: **MAI Thinking 1 optimized on Maia 200**, benchmarked against the GB300, with a further **~1.4× performance-per-watt** gain running end-to-end on Maia. These faster/more-efficient MAI models are coming to the **N1X** Satya mentioned — best performance on Windows in a few months.

**RLEs (reinforcement learning environments)** — "unique training gyms for your AIs" that create company/task-specific agents adapted only to you, built on MAI models:
- Internally, MAI used RLEs to climb toward the **best agentic uses on Excel** — on par with **GPT-5.4** on public/private benchmarks while **~10× more cost-efficient.**
- Tuned on **McKinsey's** tasks, MAI delivered the **highest win rate**, outperforming **GPT-5.5** with **~10× greater cost efficiency.**
- Unlike shared-model-only approaches, **only you keep** the benefits from your workflows, know-how, and institutional data — **the RLEs and the models you build inside them become your moat.**

### Guest — Dr. Gianrico Farrugia (Mayo Clinic): a frontier health model
**Dr. Gianrico Farrugia** (physician, researcher, President & CEO of **Mayo Clinic**) joins to announce a partnership to build a **frontier health model** for deployment in Mayo's hospitals and beyond:
- Mayo is ranked the **#1 healthcare organization in the world**, but most people will never have access — so **7 years ago** they built the **Mayo Clinic Platform**, moving healthcare from a pipeline to a platform; it now spans **4 continents**, reaches **~100 million people**, and holds what they believe is the **largest longitudinal, multimodal (genomics) healthcare dataset** in the world.
- The collaboration encodes not just textbook knowledge (models already know the journals) but **decades of clinical practice and clinical expertise** — the model can act as a **real-time team member**, predict what's likely to happen next, **prevent harm**, and improve **patient safety.**
- Each side does what it does best: Mayo brings the **right data, the right people, and a patient-focused lens**; together they build a frontier model offering **safe, secure, trustworthy, effective** healthcare solutions for all — "**the needs of the patient come first.**"

### Demo — Tanaya: Frontier tuning in practice ("hill climbing as smooth as butter")
Tanaya shows how to build your own enterprise AI with **frontier tuning**:
- **MAI Thinking 1** is in **private preview** in the **Foundry model catalog** — deploy as-is, or click **fine-tune**: set up the job, add a **grader**, create the job; it runs through logs, scores them, and starts the **hill climb.**
- A **low-level training API** gives full control: configure **rollout strategy, hyperparameters**, and incorporate your **own RLM** by defining the tools the model interacts with.
- As an **M365 customer you never start from scratch** — hop into Copilot to **build environments based on your data and workflows.** Customer **Land O'Lakes** (one of the largest U.S. businesses) uses it to perfect butter-report generation — complex tasks needing many manual steps and high precision where ~80% accuracy isn't good enough.
- Microsoft **extends the industry definition of "skills" to include rubrics** of what good looks like; uses **M365 signals (Teams, Outlook, Word, Excel, PowerPoint)** to suggest skills/rubrics that define how you work; add organizational/branding knowledge from **OneDrive/SharePoint**; tools are **simulated** so the model learns **without impacting live business state.**
- The science: by **generalizing learnings into the main model + the embedding model**, they hill-climb to **>90% accuracy** for the Land O'Lakes class — estimated **~10× more efficient** than baseline. Output "doesn't feel generic — it feels undoubtedly Land O'Lakes," and the task **continuously retrospects and evaluates success.** *"Frontier tuning as smooth as butter."*

Satya's synthesis: a significant shift — **from consuming a frontier model to fully participating at the frontier.** With **private evals/outcomes, private RLEs/traces, and enterprise knowledge**, you create scaffolding for models to hill-climb. The **new operating point**: use a very **efficient reasoning + coding model** yet achieve frontier results because you did the hard work to build the **RLE / hill-climbing machine.** The future is **the ecosystem built around you (you in control)** vs. "a few models hungry for all data."

### Microsoft Discovery (GA) — the scientific discovery loop
Building the **scientific discovery loop** may have the biggest societal impact. Science today is too **"lenient"** (hypothesize → experiment → wait for lab results → repeat). **Microsoft Discovery** makes the scientific method **continuous and programmable**, bringing together models, **HPC compute**, **knowledge graphs of scientific knowledge**, an **automated lab**, and **simulation** into one **agentic discovery loop**. **GA announced.**

### Demo — David: Microsoft Discovery designing enzymes for true plastic recycling
David (Microsoft Discovery & Quantum team) shows the **Discovery Studio** (built on VS Code) tackling **true plastic recycling** — today recycling a bottle requires shredding/melting (down-cycling); the goal is using **proteins/enzymes** so plastic can be recycled again and again:
- Three scientist goals: **write a scientific paper**, **perform the actual discovery**, and **create a protocol to test results in a real lab.**
- Launches the **discovery engine** — specialized agents always running, following the scientific method (add more from a community of agents/models/tools, or create your own). Runs can take **hours or days** running simulations; files (incl. the research paper) appear as created. Uses an internal **knowledge graph** for complete provenance/visibility.
- No out-of-the-box agent for generating candidate proteins? **Create one on the fly** (YAML-defined). Candidate generation is compute-heavy — **integrated with HPC**: start with a seed protein, vary small segments, test if each helps, repeat **millions of times** exploring a huge tree → **80 proteins** sent to the lab.
- To make a protein, bacteria produce it; Discovery creates a file with **DNA sequences** that can be **submitted to a real automated lab** via a custom agent. David shows a **real automated lab** with a **Copilot interface** — the job is submitted live; a previous run shows all the (mostly automated, human-supervised) steps. *"Bringing together the physical and agents in a unified Discovery loop."* Industries are using it today.

### Quantum — Majorana 2
Last year Microsoft announced its **first QPU**, creating a **new state of matter** (theorized ~100 years ago, proven to exist) — a radically different approach to the barriers of **reliability, speed, and size.** Progress since, with academic + industry partners:
- **Q North**: a quantum computer powered by **Atom Computing neutral atoms** with Microsoft's stack (partners incl. algorithmic/Columbia/Zurich — caption-uncertain).
- Microsoft used the **Discovery agentic loop** to compress years of quantum research into the last year.
- **Majorana 2** (announced): qubits that are **reliable and maintain state much longer** — vs **microsecond** lifetimes for common approaches, Majorana 2 delivers **~20 seconds up to ~1 minute** (**~1000× Majorana 1**), enabling complex quantum computation in that lifetime. Same tiny **qubit form factor** (~**1/100th of a millimeter**) with **digital control** — making it possible to fit **~1 million qubits on a chip smaller than a credit card.** Reliability + speed + size make the **topological approach** unique: Majorana 1 proved the physics; **Majorana 2 begins the engineering scale.**

### Closing — The frontier ecosystem & the North Star
Satya closes: it's never **tech for tech's sake** — it's about tackling the pressing challenges of **people and planet.** The real question isn't whether you *can* build the next great model/platform/quantum machine — it's **how do we build the frontier ecosystem.** Two possible stories about technology:
1. Technology **concentrates power, reduces human agency**, and leaves society to absorb the consequences.
2. We use this next wave to **unlock opportunity** for developers, scientists, enterprises, and every community.

> **"Our job is to make the second story true. That's our North Star for the frontier ecosystem. Let's all go build together."**

A closing video reinforces the quantum vision (reliable + scalable quantum unlocking chemistry, life-sciences discovery, faster drugs-to-market) — "Quantum will change the world. This change is just beginning to happen."

## 🛠️ Products / Features / Technologies Mentioned
- **Windows ML / Windows AI** — expanded to the full installed base of NPUs/GPUs/CPUs for local on-device AI.
- **MAI Ion Instruct** — local reasoning model for Windows.
- **MAI Ion Plan** — local planning model for Windows (full local agentic loop).
- **NVIDIA N1X** — next-gen PC SOC (CPU+GPU+AI, unified memory, integrated DRTM).
- **Surface Ultra** — NVIDIA-based Surface; 128 GB unified memory, ~2K display, all-day battery (this fall).
- **Surface RTX DevBox** ("Spark") — dev "dream machine": ~1 petaflop AI, 20 CPU cores, 128 GB unified memory.
- **NVIDIA DGX / GB300 station** — "desktop data center" running a ~1T-parameter model locally; Windows coming to it.
- **Windows 365** — cloud developer distribution; also **Windows 365 for agents** (max isolation).
- **Intelligent terminal (Windows)** — built-in GitHub Copilot; pick your agent.
- **PowerToys** — vertical taskbar, command palette, "Grab and Move," End Task.
- **Dev Drive** — Git-aware, Defender async for performance.
- **WSL / containers on Windows** — native, GPU-leveraging; 75+ CLI utilities; Homebrew native; Microsoft Edit.
- **Fleet** — kick off agents on Windows.
- **Copilot voice (local model)** — delegate coding via voice on-device.
- **Maia 200** — first-party AI accelerator (~30% better tokens/$; powers M365 Copilot).
- **Cobalt 200** — first-party CPU (preview) for cloud-native + agent workloads.
- **NVIDIA Grace Blackwell / NVL72** — training/post-training racks (largest fleet at Microsoft).
- **NVIDIA Vera Rubin / Vera CPU** — next-gen, built for agents + ultra-low latency.
- **AMD MI (next-gen GPU)** — partner silicon.
- **Fairwater** — Microsoft's first AI super-factory (Georgia + Wisconsin), closed-loop cooling, ~zero water.
- **Project Solara** — turnkey platform for agent-first purpose-built devices.
- **Microsoft Device Ecosystem Platform (AOSP-based)** — enterprise-ready Solara foundation.
- **Solara stationary device (MediaTek)** — ambient desk device; Windows Hello for Business; M365 Copilot + Work IQ.
- **Solara agent access badge (Qualcomm)** — portable wearable for agents on the go.
- **Foundry** — 121k+ model catalog + full agent application platform (hosted agents, IQ knowledge base, routines, Tool Box, microVMs, rubric evaluators, agent optimizer).
- **Cosmos DB / Azure Search / Fabric real-time intelligence** — agent data tier.
- **"Verizon DB"** *(caption-uncertain)* — fully managed Postgres/SQL service; HA, scale-out, 128 TB/cluster, ~3× throughput vs PostgreSQL.
- **Fabric (GPU-accelerated data warehouse)** — ~7× performance gain.
- **Microsoft IQ** — unified context layer: **Web IQ**, **Fabric IQ**, **Work IQ** (+ **Foundry IQ** knowledge base).
- **Web IQ** — LLM/agent-native web grounding; MCP-native, model-agnostic.
- **Microsoft eXecution Containers (MXC)** — OS-native agent isolation policy layer.
- **Open Claw on Windows** — native companion app (alpha) using MXC; **Open Claw Foundation** (nonprofit).
- **Fireworks AI partnership** — open-weight models to Foundry.
- **GitHub Copilot app** — home base for dev/ops; Git worktrees, agent merge, Canvas, rubber-duck reviews, multi-model.
- **Canvas** — agent-built custom UI.
- **Rayfin** — agent-first backend-as-a-service SDK (`rayfin up`); deploys to Microsoft Fabric; **Replit** partnership.
- **Agent 365** — agent control plane; **Agent 365 SDK GA**; Defender + Purview extended; cross-cloud (AWS/GCP).
- **Foundry Tool Box** — tools once → single MCP endpoint + governance.
- **Microsoft Defender security harness ("MDASH")** — ~100-agent security system; `defender details` / `defender fix`.
- **Copilot Studio** — build discoverable line-of-business agents.
- **Microsoft 365 Copilot** — chat + Cowork + code super-app (by summer); **Cowork**, **Autopilots**, **Scout**.
- **Frontier tuning + RLEs (reinforcement learning environments)** — build your own hill-climbing machine.
- **MAI Image 2.5 / 2.5 Flash, MAI Transcribe 1.5, MAI Voice 2 / Voice 2 Flash, MAI Thinking 1, MAI Code 1 Flash** — seven new MAI models.
- **OpenRouter / Fireworks / Baseten** — distribution for self-tuning MAI weights.
- **Mayo Clinic Platform / frontier health model** — co-created clinical model.
- **Microsoft Discovery** — agentic scientific-discovery loop (GA); Discovery Studio, HPC, knowledge graph, automated lab.
- **Majorana 2 / Q North** — topological qubits; neutral-atom quantum computer (Atom Computing).

## 🚀 Announcements / What's New
1. **Windows ML/AI expanded** to the **full installed base** of NPUs/GPUs/CPUs for local on-device AI (build once, run across the install base).
2. **MAI Ion Instruct** (reasoning) + **MAI Ion Plan** (planning) — new **local** models on Windows for a full local agentic loop.
3. **NVIDIA N1X** next-gen PC SOC announced (CPU+GPU+AI, unified memory, integrated DRTM).
4. **Intel** new silicon; **Qualcomm** two parts — high-end **Snapdragon X** + a sub-$500 PC part.
5. **Surface Ultra** — 128 GB unified memory, ~2K display, all-day battery; **available this fall.**
6. **Surface RTX DevBox** developer "dream machine" — ~1 petaflop AI, 20 CPU cores, 128 GB unified memory (**wait list**).
7. **Windows coming to the NVIDIA DGX/GB300** — "desktop data center" running a ~1T-parameter model locally.
8. **Vertical taskbar** — available in the **Windows Insider** build.
9. **DevBox config file** published in a **public repo** to reproduce the setup.
10. **PowerToys** updates — "Grab and Move," End Task, command palette.
11. **75+ CLI utilities** added to Windows; **Homebrew native**; first-class **container** support; **Microsoft Edit** updates.
12. **Intelligent terminal** with built-in GitHub Copilot — pick-your-agent.
13. **Maia 200** scaling (live in Arizona, deploying internationally); ~30% better tokens/$; validated with GPT-5.5; will power M365 Copilot.
14. **Cobalt 200 CPU — preview**; cloud-native + agent workloads; ~30% better than Cobalt; agent traces ~33% lower latency / ~14% faster / ~23% higher throughput.
15. **AMD MI next-gen GPU** partnership.
16. **Fairwater** AI super-factory detailed (Georgia + Wisconsin; closed-loop, ~zero-water).
17. **NVIDIA Vera Rubin** being validated/stood up at Microsoft (built for agents).
18. **Project Solara** — agent-first device platform; two device categories previewed (stationary MediaTek desk device + portable Qualcomm agent badge). Early explorers: **Accenture, Best Buy, Target.**
19. **OpenAI realtime voice models** + **Claude Opus 4.8** brought to **Foundry** (last week).
20. **"Verizon DB"** *(caption-uncertain)* — fully managed Postgres/SQL service; HA, scale-out, 128 TB/cluster (~3× throughput vs PostgreSQL).
21. **GPU-accelerated data warehouse in Fabric** (~7× performance gain).
22. **Web IQ** announced — LLM/agent-native web grounding (MCP-native, model-agnostic; best-in-class quality/speed/cost).
23. **Microsoft IQ** unified layer (**Web IQ + Fabric IQ + Work IQ**, plus **Foundry IQ** knowledge base) across Foundry + Fabric + M365.
24. **Microsoft eXecution Containers (MXC)** — new OS-native agent isolation in Windows (process / session / Windows 365 for agents).
25. **Open Claw runs natively on Windows** via MXC; new **Open Claw Windows companion app** (alpha).
26. **Open Claw Foundation** announced (nonprofit; any model/any OS); pluggable harness, folder-level permissions, auto-mode, observability — "you can run it inside your company now."
27. **Foundry as a full application platform** — hosted long-running agents, fast sandbox, durability/memory/state, auto rubrics/evals, self-improvement loop.
28. **Fireworks AI partnership** — open-weight models to Foundry.
29. **New GitHub Copilot app** — CLI speed + IDE capability, infinite agent sessions; Git worktrees, agent merge, Canvas.
30. **Canvas** — agent-built custom UIs.
31. **Rayfin** — agent-first backend-as-a-service SDK; deploys to **Microsoft Fabric**; **Replit** partnership; available now.
32. **Agent 365** — agent control plane; **Agent 365 SDK GA**, extended to local Windows agents; Defender + Purview extended; cross-cloud.
33. **Foundry Tool Box, rubric evaluators, and agent optimizer** — brand-new Foundry capabilities.
34. **Microsoft Defender security harness ("MDASH")** — ~100-agent system; `defender fix`/`details`; **coming soon to CLI + Defender portal.**
35. **Copilot super-app** — chat + Cowork + code unified **by summer.**
36. **Autopilots** — enterprise-grade autonomous agents in your tenant; **first autopilot Scout available today on Copilot Frontier.**
37. **Frontier tuning** supercharged with MAI; **RLEs** to build your own hill-climbing machine.
38. **Seven new MAI models**: **Image 2.5 / 2.5 Flash** (live in PowerPoint today; rolling to OneDrive + Foundry), **Transcribe 1.5**, **Voice 2 / Voice 2 Flash**, **Thinking 1** (private preview in Foundry catalog), **Code 1 Flash** (rolling out in VS Code).
39. MAI models on **OpenRouter / Fireworks / Baseten** — self-tunable weights for the first time; MAI **technical report** published.
40. **MAI Thinking 1 optimized on Maia 200** (~1.4× perf/watt); MAI models coming to **N1X** in a few months.
41. **Mayo Clinic partnership** — co-creating a **frontier health model** for hospitals and beyond.
42. **Microsoft Discovery — GA** (agentic scientific-discovery loop; Discovery Studio + automated lab).
43. **Majorana 2** — topological qubits, ~20 s–1 min lifetime (~1000× Majorana 1); path to ~1M qubits on a credit-card-sized chip.
44. **Q North** — forthcoming quantum computer (Atom Computing neutral atoms + Microsoft stack).

## 💡 Demos
- **Kayla — Windows dev tooling (Surface RTX DevBox):** vertical taskbar, PowerToys, Dev Drive, intelligent terminal + Copilot, WSL containers w/ GPU, **120B-param local model (3.4M local tokens)**, Copilot voice delegation, 75+ CLI tools, local log analysis via MAI Ion Instruct, ~90 GB GPU RAM running multiple models at once. **Proves:** on-device unmetered intelligence as a first-class Windows capability.
- **Jensen Huang (NVIDIA, remote from Taipei):** personal-computer → personal-AI vision; RTX Spark (1 petaflop, NVFP4); Hopper→Grace Blackwell→Vera Rubin journey; Fairwater ~30× cost-per-token vs Hopper; GitHub commits ~3×; all agent tools GPU-accelerated. **Proves:** systems co-design powers the agent era.
- **Project Solara video + Stevie Bathiche + Nathan:** agent-first stationary device (MediaTek, Windows Hello) and portable agent badge (Qualcomm) capturing/cleaning social content. **Proves:** agents can live across a constellation of purpose-built devices.
- **Cristiano Amon (Qualcomm, recorded):** agents become the center of digital life → open horizontal device platform. **Proves:** the app→agent shift reshapes silicon + devices.
- **Elijah — Microsoft IQ (Brightline utility):** one agent answering grid questions via Web IQ → Fabric IQ → Work IQ, plus a long-running agent alerting via Teams. **Proves:** combining external + internal context makes agents trustworthy in a crisis.
- **Scott, Samantha & Peter Steinberger — Open Claw on Windows:** native companion app + MXC read-only sandbox blocking a deliberate "delete all desktop files" attempt even with Open Claw's own guardrails disabled. **Proves:** OS-enforced containment makes autonomous agents enterprise-safe.
- **Cassidy — GitHub Copilot app + Rayfin:** parallel issue sessions via Git worktrees, agent merge, multi-model rubber-duck review, Canvas (camera PR approval), `rayfin up` deploy to Microsoft Fabric. **Proves:** finish (not just create) agent work, with an enterprise backend.
- **Amanda — Foundry local→enterprise:** Tool Box + single MCP endpoint + PII guardrail, one-block deploy via GitHub Actions, per-session microVM w/ persistent FS, auto-generated rubric evaluators + agent optimizer, autopilot agent in a Teams group chat. **Proves:** "you build the agent; we handle the rest," governed at scale.
- **Sarah — Defender MDASH:** ~100-agent scan finding AI-specific + traditional vulns, `defender fix` remediation, and a real 3-part cross-file bug other scanners miss. **Proves:** multi-agent joined-up reasoning beats single models at security.
- **Tanaya — Frontier tuning (Land O'Lakes):** fine-tune MAI Thinking 1 in Foundry, skills-as-rubrics from M365 signals, simulated tools, hill-climb to >90% accuracy (~10× more efficient). **Proves:** every org can build its own hill-climbing machine / moat.
- **David — Microsoft Discovery:** agentic enzyme design for true plastic recycling — HPC-driven protein search (millions of variants → 80 candidates) and DNA sequences submitted to a real automated lab via Copilot. **Proves:** a continuous, programmable scientific-discovery loop.

## 📊 Notable Stats / Quotes
- **121,000+ models** in the Foundry catalog ("the largest model catalog out there").
- **500+ Azure data center regions**; more capacity added in the **last 18 months** than in the **first decade.**
- **Fairwater**: ~**100 kW/rack** power delivery; closed-loop cooling → **~zero water** (annual water ≈ one restaurant's usage).
- **Maia 200**: ~**30% better tokens/$** vs leading GPU; **Cobalt 200**: ~30% better cloud-native, **~33% lower latency / ~14% faster / ~23% higher throughput** on agent traces.
- **NVIDIA / Fairwater**: **~30×** cost-per-token improvement over Hopper (~order of magnitude).
- **GitHub commits up ~3×** in the last several months ("gone completely parabolic").
- **"Verizon DB"** *(caption-uncertain)*: **~3× throughput vs PostgreSQL**, **128 TB/cluster**.
- **GPU-accelerated Fabric data warehouse: ~7×** performance gain.
- **Web IQ** serves on infra already used by **1B+ users.**
- **DevBox**: ~**1 petaflop AI**, **20 CPU cores**, **128 GB unified memory**; demo ran a **120B-param model** and **3.4M tokens locally**, ~**90 GB GPU RAM** utilized.
- **Compute for frontier training up ~1 trillion-fold (12 orders of magnitude) in ~15 years**; **~3 more orders of magnitude** coming.
- **MAI Thinking 1**: **97% on AIME 2025**, **53% on SWE-bench Pro**, preferred over **Sonnet 4.6**; **35B active params**, **zero distillation.**
- **MAI Code 1 Flash**: **51%** on a coding benchmark at only **~5B params.**
- **MAI Transcribe 1.5**: SOTA across **43 languages**, **~5× faster** than rivals.
- **RLE results**: Excel agent on par with **GPT-5.4** at **~10×** lower cost; McKinsey tasks beat **GPT-5.5** with **~10×** efficiency.
- **MAI Thinking 1 on Maia 200**: **~1.4× perf/watt** end-to-end.
- **Mayo Clinic Platform**: **4 continents**, **~100M people**, largest longitudinal multimodal healthcare dataset.
- **Majorana 2**: qubit lifetime **~20 s up to ~1 min** (**~1000× Majorana 1**); **~1M qubits** on a chip smaller than a credit card; qubit ~**1/100th mm.**
- Quotes: *"Agents are impatient."* (Jensen) · *"In the past CPUs were designed for humans; agents want low latency."* (Jensen) · *"The next computer is all of the devices working together as one system."* (Stevie/Solara) · *"Agents become the center of your digital experience."* (Cristiano Amon) · *"Humanist superintelligence — designed to serve people and organizations, not replace them."* (Mustafa) · *"The RLEs and the models you build inside them become your moat."* (Mustafa) · *"What's the future of the firm?"* (Satya) · *"Our job is to make the second story true."* (Satya, closing).

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - [ ] Stand up an **Open Claw companion** on Windows once available; test **MXC** folder-level sandbox + auto-mode permissions.
  - [ ] Try **MAI Thinking 1** (private preview) in the **Foundry** catalog and run a **fine-tune / RLE** on a small internal workflow.
  - [ ] Pilot the **new GitHub Copilot app** (Git worktrees + agent merge + rubber-duck reviews) and **Rayfin** deploy to Fabric.
  - [ ] Evaluate **Web IQ** for agent grounding vs current web-search stack; test **Fabric IQ / Work IQ** for internal context.
  - [ ] Look at **Microsoft Discovery** (now GA) for any research/simulation use cases.
- [ ] Questions:
  - [ ] Confirm the real name of **"Verizon DB"** (caption-garbled — likely a managed Postgres service; verify against official Build announcements).
  - [ ] Verify the **"MDASH"** / **"CyberGym"** spellings and the **"Open Shell"** NVIDIA item.
  - [ ] Pricing / availability dates for **Surface Ultra**, **DevBox**, **Cobalt 200**, and **Agent 365 SDK** in **australiaeast**.
  - [ ] How **Autopilots** (Copilot) relate to **Foundry-hosted agents** and **Agent 365** governance — one control plane or several?
- [ ] Relevant to:
  - [ ] Azure platform/architecture decisions; agent governance (Agent 365 / Purview / Defender); dev tooling standardization on GitHub Copilot.

## 🔗 Related
- [[2026 Build Session List]]
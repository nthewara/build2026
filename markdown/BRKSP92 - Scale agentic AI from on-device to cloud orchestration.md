---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/agents
  - topic/edge
  - topic/on-device
  - topic/intel
source: https://www.youtube.com/watch?v=2O1pBbxk0ac
session_code: BRKSP92
event: Microsoft Build 2026
speakers: Eddie (Intel, host), Jayen (Intel — AI client demo), Colin (Intel — edge/distributed demo), Imran (Intel — cloud/data center demo)
duration_min: 29
aliases:
  - Scale agentic AI from on-device to cloud orchestration
---

# BRKSP92 — Scale agentic AI from on-device to cloud orchestration

> [!info] Session Info
> **Event:** Microsoft Build 2026 (Intel partner/sponsor session — "SP" code)  
> **Speakers:** Eddie (Intel engineer, host); Jayen (Intel — AI client demo); Colin (Intel — edge / pooled-resource demo); Imran (Intel — data center / cloud orchestration demo)  
> **Duration:** ~29 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=2O1pBbxk0ac)

## 🎯 TL;DR
An Intel-hosted partner session arguing that modern AI is no longer "one model in one place" — agentic systems now span **client → edge → cloud**, and Intel hardware can run real workloads at every tier to escape per-token cloud costs. Three live demos prove it: (1) a small LLM ("ion 1.0 instant", released the day before and name-checked by Satya in the keynote) running **entirely on the Intel Panther Lake NPU** of a Core Ultra Series 3 laptop with near-zero CPU/memory/thermal impact via OS-level APIs (OpenVINO + Windows ML); (2) **three Asus NUC Pro 16 mini-PCs pooled over Thunderbolt** using llama.cpp RPC to expose ~150 GB of VRAM and run up to ~180B-parameter models offline for "free tokens" at <$7,000 total; and (3) a **96-vCPU Azure Xeon 6 VM** running a Qwen3 MoE model on CPU (leveraging AMX) with OpenClaw as the agent harness on Kubernetes, doing real GitHub repo analysis with autoscaling. The recurring theme: **free/cheap tokens, data that never leaves the network, and the same agentic patterns scaling from a laptop NPU to a cloud VM.**

## 🔑 Key Takeaways
- AI apps are now **agentic systems distributed across cloud, edge, and client** — not a single model in a single place; the session walks one demo per tier.
- **Every cloud token has a round-trip, latency, and cost** — teams "max out the monthly AI budget" and can't ship features because "the math doesn't math." On-device/local inference removes that ceiling.
- **"ion 1.0 instant"** (as spoken — likely a Windows on-device small-LM, referenced by Satya in the keynote, "released yesterday") runs fully on the **Intel Panther Lake NPU** of the **Core Ultra Series 3** with **~50 TOPS** of throughput, using **<20% of NPU capacity** even on bigger prompts.
- On-device inference is achieved with **zero hand-written NPU code** — it's all **OS-level APIs**: OpenVINO at the bottom, Windows ML on top; scheduling onto the NPU is the platform's job, not the developer's.
- On-device runs with **negligible CPU/memory bump, no thermal throttling, no fans, no power cliff** — it coexists with whatever else the user is running, and works **offline** (hospital, airplane, air-gapped networks) and "runs for free."
- Panther Lake enables **aggressive quantization** so you no longer trade "faster vs. smaller" — you get a model that's both faster AND smarter on hardware users already own.
- **Edge/pooled demo:** three **Asus NUC Pro 16** units (Core Ultra Series 3 **X7**, big **Arc B390** integrated graphics, 64 GB RAM each) networked via **point-to-point Thunderbolt 4 / USB4 (20 Gbit/s links)** — no network backbone.
- The Intel graphics driver exposes a **"Shared GPU NPU override"** slider letting you assign up to **93% of system RAM as VRAM** (e.g. 51.3 GB VRAM on a 64 GB box); paired with very fast **LPDDR5X (9200+ MT/s)** memory Intel mandates from OEMs.
- Using **llama.cpp's RPC mode**, the three nodes pool into **~150 GB of VRAM**, loading up to a **~180B-parameter** model; the demo ran **Qwen3-Next 80B (A3B)** at **~16–18 tok/s** offline, whole stack **<$7,000**, each node drawing **~100 W**.
- **Microsoft MXC** (Microsoft eXecution Containers for agents — announced "yesterday") lets you **sandbox agent code**: control MCP-server access, file-system access, and network in/out, and crucially **enforce it via policy** (admin-set) — demoed through **Copilot CLI** pointed at the local model.
- **Copilot CLI** (the agent built into Visual Studio) can target **local models** by setting a few env vars (model name, endpoint IP, API key) instead of cloud — directly answering "my company gives me 5,000 tokens/month and I burn them in an hour."
- **Cloud/data-center demo:** a single **Azure Xeon 6 VM (96 vCPUs, ~200 GB RAM)** runs **Qwen3 ~35B (3B active) MoE** on **CPU**, exploiting **Intel AMX** for the matrix-multiply-heavy (>80% MATMUL) transformer ops; **MoE means only a fraction of params activate**, making CPU inference viable.
- That cloud demo uses **OpenClaw as the agent harness on Kubernetes** (`oc status`), wired to the local LLM (served via **SGLang**), with **GitHub CLI inside the harness** to list issues and find the "riskiest files" for an issue — at **~15–16 tok/s** (→ **~21 tok/s** with `torch.compile`; speculative decoding/draft models coming to SGLang).
- The harness is **swappable** (OpenClaw, pi-dev, Hermes, etc.) and the K8s pods **autoscale on CPU load**, enabling multi-agent / multi-persona (PM, reviewer) workflows and nightly agent-to-agent jobs to complete a PR/issue.

## 📚 Detailed Notes

### Framing — AI spans client → edge → cloud
Eddie (Intel engineer, host) opens the partner session by reframing AI: it's "no longer just a single model running in a single place." Developers now build **agentic systems that distribute across cloud, edge, and client**. The session structure mirrors that spectrum with three demos:
1. **Client** — lightweight agents running locally for fast, real-time interaction.
2. **Edge** — distributed systems where multiple machines come together to handle more context/complexity.
3. **Cloud** — multi-agent orchestration at enterprise scale on Azure.

The through-line across all three: escaping the cost/latency of always-cloud token generation by running capable models on Intel silicon at each tier.

### Demo 1 — AI on the Client: on-device LLM on the Intel NPU (Jayen)
**The pain:** Jayen opens with a show of hands — who's maxed out their monthly AI budget? (He has too, with side-eye from management.) The core problem: **every generated token has a round-trip, latency, and a cost line item.** Many features simply can't be built/shipped because "the math doesn't math."

**The pitch:** a model called **"ion 1.0 instant"** (auto-caption spelling; described as **"released yesterday"** and **mentioned by Satya in the keynote**). Context strongly suggests this is a **Windows on-device small language model** ("Windows instant on"). It runs **entirely on the device** — specifically on the **Intel Panther Lake NPU**, part of the **Core Ultra Series 3** (Jayen notes Panther Lake "just came out in January").

**The setup:** Left side of screen = a plain chat interface ("nothing special, something we can whip up in 30 minutes"). Right side = a **systems panel** showing **NPU neural activity, CPU, memory**. Jayen tells the audience to watch the right side — "that's where the real story is."

**What the demo showed:**
- Prompt: *"What is the color of the sky?"* → answer "blue," with a **very small NPU blip**. The Panther Lake NPU offers **~50 TOPS** of AI throughput; this used **<20%** of it.
- Bigger prompt: *"Why is the color of the sky blue?"* → returned **very fast**, with visible NPU throughput, and **memory barely moved**.
- Another prompt about a polluted sky (typed with a spelling error) still answered well — robustness to messy input.
- Throughout: **small/negligible CPU blip, no memory spike, no thermal throttle, no power cliff, no fans.** The inference **coexists** with everything else the user has running.

**Why it matters / the architecture point:**
- **No NPU code was written.** It's all **OS-level APIs**: he "got the AI model, put it on the NPU, and ran with it." Stack = **OpenVINO at the bottom, Windows ML on top**. **Scheduling onto the NPU is the platform's job, not the developer's** — "we build features, that's all we do."
- Division of labor: **Microsoft provides the model + API surface; Intel ensures it runs on-device/on-prem and is always available** even with no network. Code runs "clean, fast, and cool, on hardware users already own."
- **Aggressive quantization** on Panther Lake means you don't have to choose between a **faster** or a **smaller** model — you get **both faster and smarter**.
- **Offline/privacy:** runs "in a hospital, on an airplane, anywhere the data does not get out of the network," and "runs for free for the 10,000th time."

**Booth call-out:** a reasoning game ("put in words, get a relation between the two") running on the Intel NPU — showcased as evidence the NPU reasons well.

### Demo 2 — AI on the Edge: pooling mini-PCs over Thunderbolt (Colin)
**The hardware:** three **Asus NUC Pro 16** mini-PCs running **Intel Core Ultra Series 3** processors, specifically the **X7** SKU. The **"X"** denotes Intel's **big built-in graphics** (great for gaming — "a LAN-party stack" — but used here for AI). Each node:
- **Arc B390** integrated graphics (big iGPU built into the chip).
- **64 GB RAM**.
- Very fast **LPDDR5X** memory — Intel pushes OEMs to ship **9200 MT/s or faster**.
- Draws **~100 W** each; stays cool.

**The VRAM trick:** Intel's free graphics driver (from intel.com) exposes a **"Shared GPU NPU override"** slider. Because the memory is so fast, you can reassign system RAM as VRAM — up to **93%**. The demo had it at ~81%, yielding **51.3 GB of VRAM** on a single 64 GB box (visible in Task Manager; requires a reboot to change). That alone lets a **single** node run the latest **~28B Qwen** models well.

**Pooling for big models:** Colin took it further by using **llama.cpp's RPC functionality** to connect the three nodes over IP, **pooling their resources into ~150 GB of VRAM** — enough to load a very large model. He emphasized the platform's **flexibility**:
- A single system is already potent; cheap enough to "put one on every developer's desk" before they graduate to enterprise solutions.
- For a team of ~10, you could load a **28–35B** model on each box and **load-balance** across them.
- **Total stack cost < $7,000** (individual box ~$2,300–$2,500 at top spec); **low power, stays cool.**

**Fully offline networking:** no network backbone — the three nodes are linked with **point-to-point Thunderbolt 4 / USB4 cables**, giving **20 Gbit/s** links between each system. With llama.cpp he can load **up to ~180 billion parameters** across the stack. The live model was **Qwen3-Next 80B (A3B)** running at **~16–18 tok/s**.

**Copilot CLI → local models:** Colin shows **Copilot CLI** (the agent built into Visual Studio). Many don't realize you can **point it at local models**: set a few **environment variables** — model name, **endpoint IP address**, **API key** — and from then on Visual Studio uses (here) an **80B-parameter** model to check/work with your code. Payoff: **free tokens.** Directly addresses "my company gives me 5,000 tokens a month and I use them in an hour — this is your answer."

**Microsoft MXC (announced "yesterday"):** Colin enabled **MXC — Microsoft eXecution Containers for agents** — in Copilot CLI. Purpose: **encapsulate/sandbox the code** so the agent can't "run off and do things you don't want." You can configure:
- which **MCP servers** it may access,
- which **file systems** it may touch,
- **network in/out**.
The differentiator vs. other sandboxing tools: **MXC is part of the Microsoft platform, so these settings can be enforced via policy** (admins set them) — "developers may not be as happy, but it keeps them reined in and safe." Works with a **local OR cloud** model.

**The sandbox demo (with demo gremlins):** he asks the sandboxed agent to *"run a script that pauses 5 seconds."* The flow: the agent talks to the model, reasons ("I need PowerShell to run the script"), and because it's containerized a **small execution container pops up on screen** (an executable) then disappears when done. It ran slowly ("demo demons"), so he cancelled and instead showed the model's web interface, prompting *"why is the sky blue?"* to display **token processing speed** across the three nodes: **~12 tok/s, boosting to ~16** once warmed up (first run after bring-up is slower).

**Takeaway:** start thinking of small edge client PCs not just individually but **distributed** — low-cost, flexible, "free tokens" for experimentation and small-team development.

### Demo 3 — AI in the Cloud / Data Center: agentic orchestration on Azure Xeon (Imran)
**Framing — agentic vs. chat:** Imran notes the billboards all over town about "agentic AI." Agentic AI moves far beyond chat: instead of typing queries and reading an LLM's text reply, today's tools **move and execute commands on a private VM in a sandbox**, return tool output, etc. The common thread is **context size**. Chat historically started around **1,000–2,000 tokens**; **agentic systems start at a minimum of ~10,000 tokens.** Bigger contexts strain GPU memory, which becomes a bottleneck — so why not **reuse the private VMs you already have in your VPCs?**

**The setup:**
- A single **Azure VM** with **96 virtual CPUs** and **~200 GB RAM**.
- Hosting a local LLM: **Qwen3 ~35B with 3B active parameters** (a **Mixture-of-Experts** model), context window **200,000 tokens**.
- **Why CPU works:** in an MoE model, **only a fraction of parameters activate** per execution. **Xeon 6 CPUs have AMX** (Advanced Matrix Extensions) built in, which **accelerates matrix multiplication**. Since **>80% of transformer operations are MATMUL**, AMX directly improves **prefill time and time-per-token (TTFT)**.

**The agent harness:**
- LLM served by **SGLang** ("SG lang") on the VM (visible serving on the left).
- **OpenClaw** deployed as the **agent harness on a Kubernetes-based system**; status checked with **`oc status`** — up and running and mapped to the loaded Qwen3.6 35B / 200K-context model.
- **GitHub CLI** is installed **inside** the OpenClaw instance so it can run the commands the LLM decides to call.

**What the demo did:**
1. Asked OpenClaw to **list issues in a private GitHub repo.** Two-step process: (a) OpenClaw parses the command, sends it to the LLM to decide which tools to call; (b) the harness runs the **GitHub CLI** command, returns the result to the **SGLang** serving engine, which **summarizes** the output. Token rate **~15–16 tok/s**.
   - Throughput levers: **`torch.compile`** → ~**21 tok/s** on the 96 cores; **draft model + speculative decoding** coming soon to SGLang (already available in **vLLM** and other engines).
2. Asked OpenClaw to **create a list of the "riskiest files" for a specific issue** — same loop: translate instruction → run GitHub CLI to extract info → summarize. Result: only **one file** was changed in that issue (so it surfaced as the risky/relevant file).

**Why this architecture (the payoff):**
- The harness is **easily swappable** — OpenClaw could be replaced by **pi-dev, Hermes, or any other harness**.
- **Autoscaling on Kubernetes:** start with a couple of replicas (demo had ~2); as **CPU utilization rises, replicas auto-increase.**
- Enables **multi-agent / multi-persona** workflows: spin up agents acting as **PM, reviewer**, etc., all on a single box, to run an **end-to-end workflow** — or push a **nightly job** where agents communicate with each other to complete the coding for a given PR/issue.
- All on a **single Xeon-hosted Azure VM**, ideal where you have **spare CPU cycles** and want **private agentic AI** — "not heavy on the pocket."

### Q&A
- **Box cost?** ~**$2,500** individually at highest spec (~$2,300 typical); the **whole 3-node stack ≈ $7,000**.
- **How is the model/workload scheduled across the stack?** A **single llama.cpp endpoint**. Colin **sFards/shards the model into three** and pushes it out; the **biggest network usage is the initial load** (faster network = faster assembly). After that, each node runs an **RPC server** and **llama.cpp handles routing** layers/work to whichever machine has them. You then point any agents at the **OpenAI-compatible endpoint** llama.cpp exposes. llama.cpp breaks the model into layers across nodes ("all very off-the-shelf").
- **Compile note:** he compiles **llama.cpp** (2–3 terminal lines), enabling the **`--rpc`** flag and using the **Vulkan backend** (because he's driving the iGPU directly), which works well for this multi-node case.
- **Will OpenVINO get similar capability to what llama.cpp does here?** "It's coming." On **individual machines, OpenVINO beats most of this**; but for the **multi-node RPC** setup OpenVINO "needs a little work — it gets confused about the memory." On a **single machine, OpenVINO is a lot faster than Vulkan.**

## 🛠️ Products / Features / Technologies Mentioned
- **Intel Core Ultra Series 3** — Intel's client CPU line used across all demos (includes NPU + Arc iGPU).
- **Intel Panther Lake NPU** — the NPU in Core Ultra Series 3 (~50 TOPS); ran the on-device LLM; "came out in January."
- **"ion 1.0 instant" / Windows "instant on" small LM** — on-device small language model (auto-caption garbled name; said to be "released yesterday" and referenced by Satya in the keynote) running entirely on the Intel NPU.
- **OpenVINO** — Intel's inference runtime; the bottom layer enabling NPU execution (and faster single-machine inference).
- **Windows ML** — Microsoft's on-device ML API layer sitting on top of OpenVINO; gives developers the model + API surface without writing NPU code.
- **Intel Arc B390 (integrated graphics)** — the "big" iGPU in the Core Ultra Series 3 **X7** SKUs used in the NUCs; driven via Vulkan for AI.
- **Asus NUC Pro 16** — mini-PC used three-up for the pooled edge demo (64 GB RAM each, ~100 W).
- **"Shared GPU NPU override" (Intel graphics driver slider)** — lets you assign up to 93% of system RAM as VRAM (free driver from intel.com).
- **LPDDR5X memory (9200+ MT/s)** — the fast memory Intel requires OEMs to ship, enabling the large VRAM allocation.
- **llama.cpp** — local inference engine; its **RPC mode** + **Vulkan backend** pool the three NUCs into one ~150 GB-VRAM endpoint and expose an OpenAI-compatible API.
- **Thunderbolt 4 / USB4** — 20 Gbit/s point-to-point cabling used to network the three nodes with no switch/backbone.
- **Copilot CLI** — the agent built into Visual Studio; can be pointed at local models via env vars (model, endpoint IP, API key).
- **Microsoft MXC (Microsoft eXecution Containers)** — execution/sandbox containers for agents, controlling MCP-server/file-system/network access, enforceable via admin policy ("announced yesterday").
- **MCP servers** — accessible tools an agent can be granted (or denied) under MXC policy.
- **Azure VM (Xeon 6, 96 vCPU, ~200 GB RAM)** — the cloud host running the data-center demo.
- **Intel Xeon 6 + AMX (Advanced Matrix Extensions)** — server CPU + built-in matrix-multiply acceleration making CPU LLM inference viable (>80% of transformer ops are MATMUL).
- **Qwen3 models** — the open models used: ~**28B** (single NUC), **Qwen3-Next 80B (A3B)** (pooled NUCs, ~16–18 tok/s), and **Qwen3 ~35B / 3B-active MoE** with 200K context (Azure Xeon).
- **Mixture-of-Experts (MoE)** — model architecture where only a fraction of parameters activate per token — key to running large models on CPU.
- **SGLang** — LLM serving engine used in the cloud demo (torch.compile → ~21 tok/s; speculative decoding "coming soon").
- **vLLM** — referenced as already supporting draft-model speculative decoding.
- **OpenClaw** — the agent harness on Kubernetes in the cloud demo (`oc status`), wired to the local LLM + GitHub CLI.
- **GitHub CLI** — installed inside the OpenClaw harness to execute repo commands (list issues, find riskiest files).
- **pi-dev / Hermes** — alternative agent harnesses mentioned as drop-in replacements for OpenClaw in the cloud setup.
- **Kubernetes** — orchestrates the OpenClaw harness pods and provides CPU-load-based autoscaling for multi-agent workflows.
- **Satya Nadella keynote** — referenced as where the on-device model was announced "yesterday."

## 🚀 Announcements / What's New
- **"ion 1.0 instant" / Windows on-device small LM** — described as **released the day before** the session and **mentioned by Satya in the Build keynote**; runs entirely on the Intel Panther Lake NPU. *(Status: newly released; exact product name uncertain from auto-captions.)*
- **Microsoft MXC (Microsoft eXecution Containers for agents)** — **announced "yesterday"**; available to **start experimenting with today** via Copilot CLI. Sandboxes agents (MCP/file-system/network controls) with **policy enforcement** as the key differentiator. *(Status: newly announced, usable now.)*
- **Intel Panther Lake (Core Ultra Series 3)** — noted as **shipping since January**, enabling aggressive quantization on the NPU. *(Status: GA / shipping.)*
- **Copilot CLI → local model targeting** — highlighted as a capability (point the VS-built-in agent at local endpoints via env vars). *(Status: available now; not a new announcement per se.)*
- **SGLang speculative decoding / draft models** — **"coming soon"** to SGLang (already in vLLM and other engines). *(Status: roadmap.)*
- **OpenVINO multi-node RPC pooling** — parity with llama.cpp's RPC pooling is **"coming"** (currently has memory-handling issues across nodes). *(Status: roadmap.)*

## 💡 Demos
1. **On-device NPU chat (Jayen):** "ion 1.0 instant" running on the Intel Panther Lake NPU of a Core Ultra Series 3 laptop. Split screen: chat on the left, live systems panel (NPU/CPU/memory) on the right. Prompts about the sky's color showed **fast responses, <20% NPU usage (~50 TOPS total), negligible CPU/memory, no thermal/fan/power impact.** **Proved:** capable LLM inference can run fully on-device, offline, "for free," with zero NPU code (just OS-level OpenVINO + Windows ML APIs) — coexisting with the user's other workloads.
2. **Pooled mini-PC stack (Colin):** three Asus NUC Pro 16 (Core Ultra X7, Arc B390, 64 GB each) linked by point-to-point Thunderbolt 4 (20 Gbit/s), using the driver's "Shared GPU NPU override" to expose ~51 GB VRAM per box and **llama.cpp RPC to pool ~150 GB VRAM**, running **Qwen3-Next 80B at ~16–18 tok/s fully offline** for **<$7,000**. Also demoed **Copilot CLI pointed at the local 80B model** and **MXC sandboxing** (a containerized agent spinning up a visible execution container to run a PowerShell "pause 5s" script — hit demo gremlins, then showed ~12→16 tok/s via the model's web UI). **Proved:** cheap, low-power edge PCs can be pooled to run large models locally for "free tokens," with policy-enforceable agent sandboxing.
3. **Cloud Xeon agentic orchestration (Imran):** a single Azure Xeon 6 VM (96 vCPU, ~200 GB RAM) running **Qwen3 ~35B / 3B-active MoE (200K context)** on **CPU via AMX**, served by **SGLang**, with **OpenClaw on Kubernetes** as the agent harness + GitHub CLI. Live: listed issues in a private GitHub repo and identified the **"riskiest files" for an issue** (found 1 changed file) at **~15–16 tok/s** with **autoscaling replicas**. **Proved:** private, cost-effective agentic AI can run on spare CPU cloud capacity (no GPU), with swappable harnesses and multi-agent/multi-persona autoscaling.

## 📊 Notable Stats / Quotes
- **~50 TOPS** — Intel Panther Lake NPU AI throughput; on-device LLM used **<20%** of it.
- **~150 GB VRAM** — pooled across **3 NUCs** via llama.cpp RPC; supports up to a **~180B-parameter** model.
- **51.3 GB VRAM** allocated from a **64 GB** box via the driver's GPU/NPU override (up to **93%** of RAM assignable as VRAM).
- **LPDDR5X @ 9200+ MT/s** — the fast memory Intel mandates from OEMs.
- **Thunderbolt 4 / USB4 @ 20 Gbit/s** point-to-point links; **~100 W** per NUC.
- **< $7,000** total for the 3-node stack (~$2,300–$2,500 per box); **Qwen3-Next 80B at ~16–18 tok/s**.
- **96 vCPU + ~200 GB RAM** Azure Xeon 6 VM; **Qwen3 35B / 3B active**, **200K context**; **~15–16 tok/s** (→ **~21 tok/s** with `torch.compile`).
- Agentic context sizes start at **~10,000 tokens** vs. chat's **1,000–2,000**; **>80%** of transformer ops are **MATMUL** (why AMX helps).
- *"My company gives me 5,000 tokens a month and I use those in an hour. This is your answer."* — Colin, on local models as the fix for token budgets.
- *"You get a faster and a smarter model and you get both."* — Jayen, on Panther Lake quantization.
- *"It runs for free for the 10,000th time."* — Jayen, on on-device inference economics.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Verify the real name/SKU of "ion 1.0 instant" (likely a Windows on-device small LM announced in the Build keynote) and check Windows ML + OpenVINO NPU sample code.
  - Spin up **Copilot CLI → local model** via env vars (model / endpoint IP / API key) against a llama.cpp OpenAI-compatible endpoint.
  - Experiment with **MXC** agent sandboxing (MCP/file/network controls + policy) once docs are available.
  - Try **llama.cpp RPC pooling** across 2–3 machines over Thunderbolt/USB4; compile with `--rpc` + Vulkan backend.
  - Test **CPU LLM inference on Azure Xeon 6 (AMX)** with an MoE model (Qwen3 35B/3B-active) served by SGLang; measure tok/s with `torch.compile`.
- [ ] Questions:
  - Exact product name + availability of the on-device model; is it OS-bundled or a separate download?
  - MXC GA timeline and which Copilot surfaces support it beyond Copilot CLI?
  - OpenVINO multi-node RPC parity ETA vs. llama.cpp?
- [ ] Relevant to:
  - On-prem / air-gapped (hospital, regulated) AI deployments where data can't leave the network.
  - Cost control on AI token budgets for dev teams (local/edge inference for "free tokens").
  - Private agentic AI on existing Azure CPU capacity (cost-effective, no GPU).

## 🔗 Related
- [[2026 Build Session List]]
- Microsoft Build 2026 — Intel partner session (BRKSP92)

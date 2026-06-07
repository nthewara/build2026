---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/kubernetes
  - topic/aks
  - topic/agents
  - topic/ai
  - topic/cloud-native
source: https://www.youtube.com/watch?v=_SzOdHMVPnY
session_code: BRK222
event: Microsoft Build 2026
speakers: Lachlan Evenson (Microsoft)
duration_min: 50
aliases:
  - The honest practitioner's take on agentic AI on Kubernetes
---

# BRK222 — The honest practitioner's take on agentic AI on Kubernetes

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Lachlan Evenson (Microsoft — Kubernetes/AKS, 10+ yrs in Kubernetes); demo voiceovers by colleagues Ralph (AI Runway demo) and Bob (Anyscale/Ray demo)  
> **Duration:** ~50 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=_SzOdHMVPnY)

## 🎯 TL;DR
An unusually candid, practitioner-level walkthrough of running AI — and especially **agentic** — workloads on Kubernetes/AKS. Lachlan Evenson frames the core decision as a spectrum: **fully-managed AI platforms (PaaS, e.g. Microsoft Foundry) on the left** for speed and curation, versus **AKS/Kubernetes on the right** as a composable, "you-tuned", open substrate for teams that need extreme scale, tunable cost-per-token, data sovereignty, multi-cloud/on-prem/edge, or to *build* a platform rather than rent one. Neither end is "wrong" — it depends where your team sits. He argues Kubernetes is **necessary but not sufficient**: it provides declarative resource management, heterogeneous scheduling, namespace isolation, and a durable ecosystem, but AI needs more layered on top (gang scheduling, accelerator/topology awareness, GPU/token-based autoscaling, durable state). The session walks a **four-layer stack** — Kubernetes substrate → inference/serving (KAITO + AI Runway) → training/fine-tuning (Ray + Anyscale on Azure) → agentic orchestration (skills, MCP, OpenClaw, KARS) — with live demos, real customers (RBC, Wave), and a batch of AKS announcements (GA: AKS Automatic managed system node pools, Azure Container Linux; Preview: AKS on bare metal, Fleet for Arc-enabled clusters, Anyscale-on-Azure managed Ray). The honest message: agentic orchestration is the **least mature, fastest-changing** layer — but you can run it up *today* and start experimenting, with Kubernetes primitives (namespaces, service mesh, workload identity, Azure Linux sandboxes) supplying the security and observability guardrails.

## 🔑 Key Takeaways
- **It's a spectrum, not a binary.** Managed AI PaaS (Foundry) = fastest path, curated, standardized, vendor-tuned. AKS/Kubernetes = composable, open, *you-tuned*, deeper into the stack. Choose based on where your team sits, not hype.
- **Pick AKS/Kubernetes when** you need extreme scale, tight tunable cost control (cost per token/inference/tenant), data sovereignty, multi-cloud / on-prem / edge / sovereign portability, or you're an ISV building & shipping an AI platform yourself.
- **The AI "iron triangle":** quality, speed, cost — pick your trade-offs. Kubernetes gives four levers: **granular control** (scheduler, accelerators, isolation = quality), **open tooling** (no vendor lock-in, runs anywhere), **data sovereignty** (data/weights stay in your boundary), and **digital unit economics** (tunable cost per token). The price you pay at the bottom of the triangle is **operational complexity** — you buy flexibility with operational overhead.
- **Kubernetes is necessary but NOT sufficient for AI.** It ships declarative resource mgmt, heterogeneous scheduling, namespace isolation, and a durable primitive ecosystem — but the AI era demands more layered on top.
- **Four gaps Kubernetes must close for AI:** (1) **gang scheduling / advanced queuing** (start tens-of-thousands of pods together, not one at a time, don't use the default scheduler); (2) **heterogeneous-hardware / accelerator awareness** (GPU family awareness, topology, NUMA-aware placement as first-class signals); (3) **AI-aware autoscaling** (scale on tokens/sec, queue depth, GPU utilization — not just CPU/mem — and release accelerators when idle); (4) **durable state** (caching + storage so training and agentic workloads survive evictions, drains, topology changes, spot interruptions).
- **Three distinct AI workloads, three operational profiles:** **Inference** (ms–sec/request, GPU+CPU, often single-node, drop overflow, optimize latency & cost/token → KAITO, AI Runway); **Training** (throughput-bound, hours–weeks, checkpoint/resume, keep expensive GPUs saturated → Ray, Anyscale); **Agentic** (sessions/minutes-per-turn, multi-modal, resume-on-state mid-session, tool-call latency sensitive → skills, MCP, OpenClaw). They share GPUs but not operational assumptions.
- **Start your AI-on-K8s journey at inference/serving** — it's the logical entry point: take a model, get a reliable inference endpoint into dev/prod, let developers integrate it.
- **AI Runway = the platform layer:** Kubernetes-native inference platform with a web UI + unified model-deployment controller; "App Store for AI models" with a curated catalog (Qwen, Phi, DeepSeek, Llama) + Hugging Face gallery integration; supports vLLM, SGLang, TensorRT, llama.cpp; key feature is a **GPU-fit indicator** telling you instantly if a model fits your cluster (and triggers autoscaling if not). One-click deploy.
- **KAITO (Kubernetes AI Toolchain Operator) = the operation layer:** optimized presets for pipeline/data/tensor parallelism, KV-cache-aware routing via Kubernetes primitives (inference pool). AI Runway is the platform; KAITO is **one of its providers** alongside NVIDIA Dynamo, llm-d, and others. Both open-source, Kubernetes-native, run on any conformant cluster.
- **From browse-to-serve in a few clicks, on primitives you already operate:** browse catalog → check GPU fit → create model deployment → KAITO workspace estimates GPU + autoscaling → live endpoint → ship; Kubernetes does the rest (KEDA autoscaling, vLLM metrics, canary + rollback-aware deployments). "We're not giving you anything new — we're just shaping it for AI."
- **Ray fills the training/fine-tuning gap AKS doesn't cover natively:** distributed CPU+GPU scheduling in one job, **fractional GPU allocation** (keep GPUs ~100% utilized), multi-node training + reinforcement-learning orchestration (a CI/CD pipeline for models), autoscaling, and one **Python-native API** across data prep, training, tuning, and serving. AKS is the cluster; Ray is the workload.
- **Anyscale on Azure = managed Ray (public preview):** Azure-native integration; open-source Ray is the engine, Anyscale provides managed lifecycle, observability, and 24/7 support. Runs **in your subscription**, billed through your Azure agreement (no new vendor relationship). Two boundaries: **Anyscale control plane** (dev tools, observability, orchestration, monitoring) in Anyscale's managed Azure tenant; **your data + models** stay in your subscription/AKS cluster. Provisioned from the Azure portal, unified billing, Entra ID security (workload identity, RBAC, audit trails). Data/models never leave your environment.
- **Agentic orchestration is the frontier — and the least mature, fastest-changing layer.** You build agents on Kubernetes with **skills** (any script your platform team would run, registered in a catalog, callable by any permitted agent — turns checked-in repos into agent capabilities), **MCP** (protocol for agents↔tools/data/other agents; Microsoft exposes an **AKS MCP server** so you can provision/operate AKS in natural language with workload identity), and Kubernetes primitives filling the gaps (namespaces for isolation, service meshes for observe/filter/policy).
- **OpenClaw** = a reference implementation of a multi-channel, multi-tool personal AI assistant that bridges a chat platform into a multi-agent orchestrator with approval flows, tools, and memory — a base pattern you can build on. Microsoft has codified AKS support-engineer troubleshooting skills into agents for **day-2 operations**.
- **KARS (Agent Reference Stack for Kubernetes, `azure/kars`) released today:** a vertically integrated, **secure sandbox** for running agents on any Kubernetes cluster (even local) via a single `kars up` binary; applies workload-identity policies, sandboxes leveraging **Azure Linux**, a `kars-system` namespace for the machinery, a **Headlamp** plugin + mesh-topology view to introspect where agents run / what tools/policies/access they have. Keeps agents from "running wild."
- **Four reasons practitioners build the agent layer on Kubernetes:** session state, multi-state coordination built-in, tool-call observability, and a composable stack.
- **Real customers prove it in production:** **Royal Bank of Canada** runs KAITO for production model serving inside a strict compliance perimeter (Entra ID, Key Vault, private ACR, self-service GPU provisioning via CI/CD, secure-by-default). **Wave** rewrote the self-driving playbook with end-to-end deep learning on **AKS + Ray + Anyscale**, connecting thousands of GPUs into a flexible supercomputer — their AI driver demonstrated autonomous driving in Tokyo after only ~4 months. Microsoft itself runs **AKS Claw** (SRE subject-matter expertise encoded as an agent — each on-call engineer gets an isolated Claw instance, up and running in minutes).
- **The takeaway checklist:** start with Kubernetes (the substrate you likely already run) → build the agent layer with MCP + skills + reference stacks like OpenClaw/KARS → choose tooling matching your build-vs-buy (KAITO/AI Runway for inference, Ray/Anyscale for training, KARS for agentic runtime specialization) → **invest in Fleet early**, before your workloads outgrow a single cluster.

## 📚 Detailed Notes

### Framing: "the honest practitioner"
Lachlan Evenson opens with high energy (5pm slot, "the only thing between you and the Chainsmokers tonight") and sets the session's promise: this is for people **already running Kubernetes** who are trying to figure out **what AI workloads actually need on top of Kubernetes**. The arc is deliberately three-part: **what works today, what's harder than it looks, and where the ecosystem is going.** He repeatedly returns to being the *honest* practitioner — naming trade-offs and immature areas rather than selling hype. He promises a tangible payoff: demos, real customer cases, links to Kubernetes repos, and a **checklist you can take back to your team this week**.

### Why Kubernetes shows up as the AI substrate
The "why" comes before the "what" and "how." His blunt caveat: **"Kubernetes is a big hammer, and with a big hammer everything looks like a nail."** It isn't always the right fit — but where **scale** is involved (and AI + scale go hand-in-hand), Kubernetes is one of the right answers. The session is fundamentally about earning the right to choose Kubernetes consciously, not defaulting to it.

### The PaaS ↔ Kubernetes spectrum
He draws a left-to-right spectrum:
- **Left — fully-managed AI services (PaaS).** Microsoft Foundry is the cited example (the *preceding* Build session covered "Microsoft boundary"/Foundry). This is the **fastest path to a deployment model**: curated, standardized, vendor-tuned. Best for **common patterns, speed, and deployment**.
- **Right — AKS / Kubernetes.** A **deeper path into the stack**: composable, open, *you-tuned*. The **"open"** is the powerful part — multi-cloud, on-prem, sovereign environments all get a *very similar experience*. Best for **extreme scale, tunable tight cost control, data sovereignty, or building something a managed stack can't tune**.

**Neither end is wrong — it's a matter of where your team sits.** If you already run Kubernetes, AKS/Kubernetes may be the right place to chart your AI course.

### The AI iron triangle and four control levers
He loves the **iron triangle of project management** (fast / good / cheap — pick two). AI has its own version with **quality, speed, cost** at each apex. Kubernetes/AKS gives four levers to navigate it:
1. **Granular control → quality.** Choose your scheduler, accelerators, and isolation model to match what your customers need.
2. **Open tooling.** Leverage the *entire* AI open-source stack **without vendor lock-in**; run on-prem, in other data centers, or other clouds with a near-identical experience.
3. **Data sovereignty.** Workloads, data, and weights **stay where compliance demands** — inside your security boundary, never sent off-premises.
4. **Digital unit economics.** The "talk of the town" is **cost per token**; self-hosting lets you tune **cost per token / per inference / per tenant**.

**The trade-off at the bottom of the triangle: complexity.** "You're buying flexibility with operational overhead" — this platform gives ultimate flexibility but *you* operate it. (Foreshadow: agentic systems can help operate it — covered later.)

### Who wins by self-managing
Profiles where self-managed Kubernetes wins (Microsoft's observed customers):
- Teams running **AI at scale** with cost sensitivity or sensitivity to **where the data sits**.
- **ISVs / cloud-agnostic vendors** building and shipping AI platforms to **on-prem and edge**.
- **Platform owners** who want **composability rather than rent**.

For these, "composability isn't optional — it's required."

### Kubernetes primitives that do the work
What Kubernetes ships out of the box to manage the substrate:
- **Declarative resource management** — memory, GPUs, and quotas all defined as code; everything declarative.
- **Heterogeneous scheduling** — in a world of many accelerators, match the right workload to the right accelerator at the right time; compose clusters with different compute and networking accelerators.
- **Namespace isolation** — multi-tenant AI that doesn't cross the security boundary (so you don't have to rewrite your security tools).
- **A complete ecosystem of durable primitives** — abstractions stable enough that other platforms build on top of them. (He shouts out **Mark** in the audience, who works on **Dapr** — caption-garbled as "Dapper" — which sits *on top of* Kubernetes as an example.)

Kubernetes was *built for* this complexity, "not in spite of it."

### Three AI workloads — different conditions, lifetimes, compute
A pivotal slide: each AI workload has its **own operational environment**. They share GPUs but **not** the same operational assumptions.

**Inference (left, red):**
- Lifetime: **milliseconds to seconds per request.**
- Compute: **GPU + CPU** (heterogeneous); **often single-node.**
- Overflow behavior: just **drop the request.**
- Optimize for: **latency and cost per token.**
- Tools: **KAITO, AI Runway.**

**Training (middle):**
- **Throughput-bound**; lifetime **hours to weeks.**
- Data scientists "get really mad when training jobs break" — they must **resume from a checkpoint.** Hardware is extremely expensive, so **time is money**; keep GPUs **absolutely saturated/utilized.**
- Measure: **throughput / iteration time** (how long a training iteration takes).
- Tools: **Ray, Anyscale on Azure.**

**Agentic systems (right):**
- Lifetime: **sessions / minutes per turn.** Autonomous/autopilot agents act on our behalf, ingest data, make decisions.
- **Multi-modal** (images, text, voice, video streams); **resume on state mid-session** → need state awareness.
- **Tool-call latency** is very sensitive.
- Tools: **skills, MCP, OpenClaw.**

### Necessary but not sufficient: four gaps to close
"Kubernetes gives you the foundation, but the era of AI asks for more on top." Necessary, not sufficient. Four gaps (being actively worked on):
1. **Scheduling at AI scale.** Traditional Kubernetes schedules **one pod at a time**; AI wants **tens/hundreds of thousands of pods to start together** → use **gang scheduling and advanced queuing**, not the default scheduler (Kubernetes lets you clip in a custom one).
2. **Heterogeneous-hardware awareness.** Each new accelerator generation shouldn't force a platform rewrite — just use the new one alongside the trusted old. **GPU family awareness, accelerator topology, and NUMA-aware placement** must become **first-class signals.**
3. **AI-aware autoscaling.** Traditional Kubernetes scaled only on **CPU and memory** — not enough. Scale on **tokens/sec, queue depth, GPU utilization**, and **release accelerators when idle.**
4. **Durable state.** Kubernetes was designed for **stateless** services. AI needs **caching + storage** so long-running **training** jobs and **agentic** workloads survive **evictions, drains, topology changes, and spot interruptions.**

### The four-layer mental model
The rest of the session is structured bottom-up as a **four-layer stack**:
1. **Kubernetes / AKS** — the substrate (bottom).
2. **Inference & serving** — **KAITO + AI Runway** (where most customers start).
3. **Training & fine-tuning** — **Ray + Anyscale on Azure** (green layer).
4. **Agentic orchestration** — **skills, MCP, OpenClaw** (top; the layer he's most excited about).

Presentation order: **inference first**, then jump to the **top (agentic)**, and finish with the **substrate + announcements** at the bottom.

### Layer 2 — Inference & serving (KAITO + AI Runway)
**Why start here:** if you haven't begun your AI-on-Kubernetes journey, this is the logical entry point — you have a model, you want a reliable **inference endpoint** in dev and prod so developers can integrate it and you can *see the value* AI provides.

Two open-source tools, both on GitHub today, with one goal — **get a model serving reliably behind an inference endpoint**:
- **AI Runway = the platform layer.** A **Kubernetes-native inference platform** with a **web UI** and a **unified model-deployment controller**. Get a model up on Kubernetes in a few clicks. Supports all major serving engines — **vLLM, SGLang, TensorRT, llama.cpp** — so you can plug in your own engine (each has different trade-offs). One-click deploy, nice UI, runnable on any cluster this afternoon.
- **KAITO (Kubernetes AI Toolchain Operator) = the operation layer.** Handles the operational burden of running/serving a model in production: **optimized presets** for **pipeline, data, and tensor parallelism**, and **KV-cache-aware routing** using Kubernetes primitives like **inference pool**.

**Key relationship:** AI Runway is the **platform**; KAITO is **one of its providers**, alongside **NVIDIA Dynamo, Q Bright, and llm-d**. All open-source and Kubernetes-native → run on any conformant Kubernetes cluster, anywhere.

### The browse-to-serve flow (on primitives you already operate)
The promise: **from browsing a model to serving in production in just a few clicks**, on primitives you already run:
1. **Browse** — open AI Runway, pick a model from the **catalog** (integrates the **Hugging Face UI** for the latest open-weight models), and **check GPU fit** (it states whether the model fits, or triggers cluster autoscaling to make it fit), then create a model deployment.
2. **Create a KAITO workspace** — estimates required GPU utilization, the autoscaling/nodes needed, and where the workload runs, with **optimized presets**. Spins up a **live endpoint**.
3. **Ship it** — Kubernetes does the rest: **KEDA** for autoscaling, **vLLM metrics** integration (scale on many metrics), **canary deployments**, and **rollback-aware deployments**.

Every item on the right of the slide is **a Kubernetes primitive you already know how to operate** — "we're not giving you anything new, we're just shaping it for AI."

### Demo — AI Runway (voiced by Ralph)
Filmed by colleague **Ralph** ("a voice for radio — smooth and buttery"):
- **Model catalog** = "App Store for AI models": curated popular models (**Qwen, Phi, DeepSeek, Llama**), each card showing size, supported engines, and what it's good at (chat, text generation, multimodal).
- **GPU-fit indicator on every card** — instantly shows whether a model will run on *your* cluster. No guesswork, no trial-and-error.
- **Runtime tab** — shows the inference frameworks under the hood; **multiple runtimes, fully extensible, never locked in.**
- **Hugging Face gallery** — search **DeepSeek R1, 671B params**. Won't fit the single node (8× H100), so select **Dynamo** as runtime, deploy to default namespace. Because the model is huge, it **recommends 3 nodes = 24 GPUs total**; with the **cluster autoscaler enabled**, deploying eventually brings the extra nodes online.
- **Storage volumes** — attach a **persistent volume backed by Azure Managed Lustre** (high-performance shared FS). Model weights are **cached** so restarts/scale-out don't re-download hundreds of GB; it's **read-write-many** so all nodes access it simultaneously.
- **Live cost estimate** — per-hour and per-month on Azure, updating in real time (varies by cloud provider).
- **Autoscale + rollout** — cluster starts at 1× H100 node (8 GPUs); needs 24 across 3 nodes; on deploy, nodes come online, rollout completes across all three, status → running.
- **Use it** — deployment page shows storage, mounted disk, and the **gateway endpoint**. AI Runway integrates the **Gateway API Inference Extension** (using **Istio** here) for a **single stable endpoint** across all models, plus a ready-to-use **curl** command. It's a **standard OpenAI-compatible API** — any tool/SDK that speaks OpenAI talks to your models unmodified.

**The kicker:** Ralph did the whole thing in **3 minutes** — "what used to take me 3 weeks to get up and running" — all with open-source tools available on GitHub today.

### Layer 3 — Training & fine-tuning (Ray + Anyscale on Azure)
Next up the stack: you have a running model, now **fine-tune it with your own data** for your own workflow. Eventually all agents need a **fine-tuned model with your data behind it**, and **Ray** is the workload that powers that.

**What AKS provides natively:** pod scheduling, autoscaling, node lifecycle, networking, storage — the substrate, hardened for production at scale. **What production AI also needs that AKS doesn't provide natively, and Ray fills:**
- A **distributed computing / scheduling framework** that schedules **both CPUs and GPUs in a single job.**
- **Heterogeneous hardware** handling via **fractional GPU allocation** (critical for keeping GPUs at ~100% as long as possible).
- **Multi-node orchestration** for both **training and reinforcement learning** — effectively a **CI/CD pipeline for your models.**
- **Autoscaling** on your behalf.
- **One Python-native API** across **data prep, training, tuning, and serving** — hosted in their interface, deployable from it, running on an AKS cluster.

"AKS is the cluster, Ray is the workload."

### Announcement — Anyscale on Azure (managed Ray, public preview)
**Public preview of Anyscale on Azure** — **managed Ray**, an **Azure-native integration** built in collaboration with Anyscale. Open-source **Ray is the distributed compute engine**; **Anyscale provides the managed lifecycle, observability, and 24/7 support.** Crucially it **runs in your subscription** and is **billed through your Azure agreement** — no new vendor relationship; you pay Microsoft and Microsoft handles Anyscale.

**Architecture / two boundaries that matter (for sovereignty):**
- **Anyscale control plane (top, orange)** — runs in the **Anyscale-managed Azure tenant**: dev tools, observability, APIs, controllers, job orchestration, monitoring, etc.
- **Your subscription (bottom, blue)** — where **your data and models live.** The **Anyscale runtime runs a managed Ray operator on your AKS cluster** with your blob storage and your GPU/CPU nodes. Everything stays within your tenant.

**Three pillars:** (1) **Provisioning from the Azure portal** — one portal, same familiar workflow; (2) **unified billing**; (3) **enterprise security with Entra ID** — workload identity *plus* identity with your own credentials, RBAC, audit, and compliance trails. **Data and models never leave the environment.**

### Demo — Anyscale on Azure end-to-end (with Bob)
Colleague **Bob** helped; a **7-minute** end-to-end **training + fine-tuning** exercise for a **product-catalog search**:
- **All in the Azure portal** — search "Anyscale" → **Anyscale Cloud** (in preview) → create flow familiar to Azure users: pick subscription, resource group (e.g. "Bob's testing"), region (**South Central US**), cloud name (identifies the cloud talking to the Anyscale control plane), and provision a **new or existing AKS cluster** (link existing clusters).
- **Managed identity** — how all workloads on the Anyscale Cloud identify with Azure and the storage accounts holding **model checkpoints and weights**; **ACR** stores container images supporting the Ray/Anyscale operator.
- **Create** — runs validation ("tap blade"), submits, and provisions in seconds ("magic of video editing"). From **no Anyscale to a running Anyscale-on-Azure cluster in a few clicks, never leaving the portal.**
- **Launch the Anyscale UI** — **same Azure credentials** carry over ("one identity, multiple platforms"). Inside: dashboards, **workspaces** + **Jupyter notebooks** (where data scientists work), **jobs** (short-run to completion) and **services** (for inferencing endpoints).
- **Templates** — zero-to-running-pipeline in a minute via a **template library** (multimodal inferencing, LLMs, hero demos, etc.).
- **The fine-tune** — a pre-provisioned **CPU-only cluster** with a head node, running on an **8-node Kubernetes cluster**. Launch an **embedded VS Code instance** from the portal and run Python directly. The demo fine-tunes an **embedding model** on a **product catalog of images** so "shoe" → "sock", "headphones" → "speakers", etc. Click play to **clean data + run the fine-tune**; accuracy graphs update (note: the narrated numbers are caption-garbled — he describes accuracy *improving* via fine-tuning to give better recommendations).
- **Embedded vectors / relationships** — related items (laptop stands, smartwatches, portable SSDs, webcams) cluster together; before/after embedding clouds show scattered colors → aggregated, i.e. a **more accurate model** from the provided data.
- **Serving** — Anyscale on Azure **handles routing**: **3 endpoints** (HTTP ingress + two models: image-to-text and the fine-tuned recommendations). Ask about "wireless headphones" → relevant matched references.
- **Monitoring/observability** — integrated stack shows node/cluster utilization, what's running, and **dependencies** (something only the Anyscale-on-Ray platform surfaces) so you can troubleshoot and confirm full utilization.

**The kicker:** "In only 7 minutes — that took me **3 months** to do." Notebook-to-production in a few clicks, ideal for **fine-tuning and reinforcement learning**.

### Layer 4 — Agentic orchestration (skills, MCP, OpenClaw, KARS)
The layer he's most excited about — and openly the **"least mature part of the stack, changing very rapidly"** (name-checking emerging things like "open floor" and "Hermes" — caption-uncertain — with "I don't know where it's going"). The honest pitch: **you can run it up and start experimenting today.** The question this layer answers: *how do I serve inference + training up to my autonomous agents?*

**Building an agent on Kubernetes uses three things plus Kubernetes primitives:**
- **Skills** — a **discrete set of capabilities an agent can run**; essentially **any script your platform team would run.** "Everything I had checked into a repo has now become a skill, and I have agents running on my behalf." Register a skill in a **catalog**; any agent with the right permissions can call it. (Hold that in mind for **day-2 operations.**)
- **MCP** — a **protocol** letting agents talk to **tools, data, and other agents.** Microsoft **exposes the AKS MCP server today** — so in **VS Code** you can say "Provision me an AKS cluster" in natural language and the LLM makes the call and provisions the infrastructure. Open-source today, runs your tools under the hood, secured with **workload identity.**
- **Kubernetes primitives fill the gaps** — **namespaces** to isolate the agent and scope its privileges; **service meshes** to **observe, filter, and apply policy** to the calls. "Kubernetes has all the primitives we need under the hood to make this work."

This is "right out on the edge of the frontier."

### OpenClaw as the reference agent pattern
**OpenClaw** — a **reference implementation for a multi-channel, multi-tool personal AI assistant** (he jokes he uses it to book his Pilates lessons). It **bridges a chat platform into a multi-agent orchestrator** with **approval flows, tools, and memory** — a **base pattern** to build on. Microsoft has **codified the skills its AKS engineers use to troubleshoot environmental issues** into agents — effectively "creating agents out of our support engineers," giving them the **right tools at the right time** so they skip the monotony of pulling logs. Used **right now for day-2 operations** — a likely high-value starting point for teams experimenting with agents.

### Announcement — KARS: Agent Reference Stack for Kubernetes (`azure/kars`)
**Released today: KARS** (k-a-r-s) — a **vertically integrated, secure sandbox environment** for running agents, where you **apply workload-identity policies** and run **sandbox environments leveraging Azure Linux** under the hood, so you have the **right security primitives in place** and "don't let agents run wild" (security being a major concern).

### Demo — KARS + OpenClaw (live, unedited)
2-minute demo of the agent reference stack (`azure/kars`):
- **`kars up`** — ships as a **single binary**; run on **any Kubernetes cluster, even local**. It runs preflight checks and installs anything missing; here it runs against a real AKS cluster.
- **`kars-system` namespace** — where all the machinery runs on your AKS cluster.
- **Run up OpenClaw via a custom resource** — declaratively in Kubernetes: "Please OpenClaw, be a helpful agent. Here's the access you have, the tools you have, what you can call." Apply to the cluster → access the OpenClaw UI.
- **Headlamp** — an open-source **heads-up display for Kubernetes** with plugins; Microsoft built a **KARS plugin** so you can **introspect** where sandboxes/agents run, their **security capabilities, policies, and access**, plus a **mesh-topology graph** of where calls flow (agents → LLMs / elsewhere).
- **`kars operator` / `kars list`** — a **binary** view of the same info; list **sandboxes**, connect to one, and it **passes back the OpenClaw URL with an embedded token** to log in.
- **Live agent answer** — unedited, recorded "yesterday": ask the agent **"what announcements did Microsoft have with NVIDIA this week?"** — it goes to the **web**, consults media/press analysis, and returns a well-thought-out response, demonstrating a fresh/live agent giving real value **in a couple of minutes and a couple of clicks**, on top of AKS/Kubernetes.

### Why practitioners build the agent layer on Kubernetes
Four reasons summarized: **session state**, **multi-state coordination built-in**, **tool-call observability**, and a **composable stack** (pick up skills/MCP — cloud providers publish MCP skills constantly; interact with Azure via the **AKS MCP server** in natural language).

### Layer 1 — Substrate announcements (AKS)
Four AKS announcements spanning **single-cluster, multi-cluster, and fleet**:

1. **AKS Automatic + managed system node pools — GA.** AKS Automatic is "the easiest way to get started with Kubernetes/AKS." Now Microsoft **manages and scales the system node pools** (the pods running the Kubernetes components themselves). **Why it matters for AI:** you don't waste your **GPU nodes** running system components — milk every cycle for AI workloads.
2. **Azure Container Linux — GA.** "The best of Azure and the best of Linux." Benefits: **smaller attack surface** (curated package set, smaller CVEs, predictable/fast patching), **transparent supply chain** (packaged + distributed with **predictable signed artifacts** and upgrade paths for **regulated workloads**), and **consistency across hosts**. Runs in **containers, on VMs, or even WSL on Windows**. Philosophy: the **OS layer in AKS should be invisible, secure-by-default, consistent, and out of your way.**
3. **AKS on bare metal — public preview.** **Direct hardware access** from AKS to manage **physical nodes** — install AKS on physical hardware with **no hypervisor / no virtualization layer** for your workload. Important for **GPUs, NICs, and specialized accelerated hardware**. **Same AKS control plane, same operational model.** Matters for AI because you can **extend AI to on-prem and other clouds** while staying inside Azure and **not paying the virtualization tax** on-prem — scaling quickly.
4. **Fleet for Arc-enabled clusters — (preview/new).** Clusters "get really, really big, really quickly," so manage a **fleet of clusters**: **progressive rollouts across clusters**, **intelligent workload placement** across boundaries/environments (on-prem, edge), and **consistent policy enforcement** (push the same policies everywhere at once). **Arc-enabled** → has an Azure identity, same control plane. "All AI workloads outgrow a single cluster very quickly — this is how you stay ahead of that."

### Customer story — Royal Bank of Canada (KAITO in production)
**RBC** runs **KAITO in production**. Their **platform onboarding & deployment operator** wraps **GPU resource provisioning into a CI/CD workflow** that **developers run themselves** — self-service deployment, **secure by default**. KAITO powers the **production model-serving workspace**; AI models deploy as **pods** with images stored in the **bank's ACR** (Azure Container Registry). The critical piece is the **compliance perimeter**: Entra ID, Key Vault, private ACR — **all models and data stay inside their secure perimeter, subscription, and boundary.** A flagship example of banks running **KAITO on AKS** for model serving.

### Customer story — Wave (self-driving on AKS + Ray)
**Wave** is "rewriting the self-driving playbook with **end-to-end deep learning**," running on **AKS with Ray**. Their **AI driver demonstrated autonomous driving in Tokyo after only ~4 months** — in a brand-new **Nissan** vehicle, **learning on the go**. That generalization required **massive infrastructure**; they use **AKS + Anyscale on Azure** to connect **thousands of GPUs into a flexible supercomputer** for training and validation. The training layer is pushed to its limits — **the scale of the infrastructure directly determines how fast they can iterate and train.**

### Microsoft's own dogfooding — AKS Claw
**AKS Claw** = Microsoft's **SRE subject-matter expertise encoded as an agent.** Each dedicated/on-call engineer gets an **isolated instance of Claw**; once installed, **every new on-call engineer is up and running within minutes** with minimal training, getting the **right tools and environment access** to make decisions and get customers back online. One **natural-language interface** that **replicates consistent operational behavior** by encoding it into agents — a concrete agentic-day-2-operations pattern built on the same primitives.

### Closing — "so now what?"
The takeaway checklist for the audience:
- **Start with Kubernetes** — the substrate many already run today.
- **Build the agent layer** with **MCP + skills** and **reference stacks like OpenClaw** (and KARS).
- **Choose tooling that matches your build-vs-buy** — there's a tool for every layer: **KAITO + AI Runway** (inference/serving), **Ray + Anyscale on Azure** (training/fine-tuning), and the **runtime specialization for agentic AI** announced today (**KARS**). Mix and match.
- **Invest in Fleet early** — before workloads outgrow a single cluster.

He closes by inviting the audience to come build, share what they're building, and "next time you're on stage telling me what y'all built."

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Kubernetes Service (AKS)** — the managed Kubernetes substrate; central to every layer.
- **Kubernetes** — declarative resource mgmt, heterogeneous scheduling, namespace isolation, durable primitive ecosystem.
- **Microsoft Foundry** — cited as the fully-managed AI PaaS example on the "left" of the spectrum (covered in the preceding session).
- **KAITO (Kubernetes AI Toolchain Operator)** — inference operation layer; presets for pipeline/data/tensor parallelism, KV-cache-aware routing via inference pool. Open-source.
- **AI Runway** — Kubernetes-native inference *platform* (web UI + unified model-deployment controller); GPU-fit indicator; OpenAI-compatible endpoints. Open-source.
- **Inference serving engines:** vLLM, SGLang, TensorRT, llama.cpp.
- **AI Runway providers:** KAITO, NVIDIA Dynamo, Q Bright, llm-d (llmd).
- **Ray** — distributed compute/scheduling engine for training/RL; fractional GPU allocation; one Python-native API across data prep/training/tuning/serving. Open-source.
- **Anyscale on Azure** — managed Ray, Azure-native integration (public preview); runs in your subscription, Azure-billed.
- **KARS — Agent Reference Stack for Kubernetes (`azure/kars`)** — secure agent sandbox; single `kars up` binary; `kars-system` namespace; Azure Linux sandboxes; `kars operator`/`kars list`.
- **OpenClaw** — reference multi-channel/multi-tool personal AI assistant; chat → multi-agent orchestrator with approval flows, tools, memory.
- **MCP (Model Context Protocol)** + **AKS MCP server** — natural-language provisioning/operation of AKS (e.g. from VS Code), secured by workload identity.
- **Skills** — discrete agent capabilities (any script), registered in a catalog, callable by permitted agents.
- **Headlamp** (+ KARS plugin) — open-source Kubernetes heads-up display / introspection UI with mesh-topology view.
- **KEDA** — event-driven autoscaling for serving.
- **Gateway API Inference Extension** + **Istio** — single stable endpoint across models.
- **Azure Managed Lustre** — high-performance RWX shared file system for cached model weights.
- **Azure Container Linux** — hardened, minimal, signed-supply-chain OS for AKS nodes / VMs / WSL.
- **AKS Automatic** — easiest on-ramp; now with managed system node pools.
- **AKS on bare metal** — hypervisor-free AKS on physical nodes.
- **Fleet (for Arc-enabled clusters)** — multi-cluster progressive rollouts, workload placement, policy enforcement.
- **Azure Arc** — gives non-Azure clusters an Azure identity / common control plane.
- **Entra ID, Azure RBAC, Key Vault, ACR (Azure Container Registry)** — enterprise identity/security/compliance for workloads, weights, and images.
- **Workload identity** — used across MCP server, KARS, and managed Ray for secure auth.
- **Hugging Face** — model gallery integrated into AI Runway's catalog.
- **AKS Claw** — Microsoft's SRE expertise encoded as an isolated per-engineer agent.
- **Dapr** — mentioned (audience member "Mark"; caption-garbled "Dapper") as a durable abstraction built on top of Kubernetes.
- **Models referenced:** Qwen, Phi, DeepSeek (incl. DeepSeek R1 671B), Llama.
- **Hardware referenced:** NVIDIA H100 GPUs; NICs; heterogeneous accelerators.

## 🚀 Announcements / What's New
- **AKS Automatic — managed system node pools: GENERALLY AVAILABLE.** Microsoft manages/scales the Kubernetes system components so GPU nodes are reserved for AI workloads.
- **Azure Container Linux: GENERALLY AVAILABLE.** Hardened, minimal-CVE, signed-supply-chain OS; runs in containers, on VMs, and in WSL.
- **Anyscale on Azure (managed Ray): PUBLIC PREVIEW.** Azure-native managed Ray; control plane in Anyscale's managed Azure tenant, data/models in your subscription; provisioned via Azure portal, Azure-billed, Entra ID-secured.
- **AKS on bare metal: PUBLIC PREVIEW.** Hypervisor-free AKS on physical hardware for direct GPU/NIC access; same AKS control plane and operational model; extends AI to on-prem/other clouds without the virtualization tax.
- **Fleet for Arc-enabled clusters: NEW (multi-cluster/fleet).** Progressive cross-cluster rollouts, intelligent workload placement, and consistent policy enforcement across on-prem/edge, Arc-enabled with an Azure identity.
- **KARS — Agent Reference Stack for Kubernetes (`azure/kars`): RELEASED today.** Vertically integrated secure agent sandbox with workload-identity policies and Azure Linux sandboxes; runnable on any cluster (incl. local) via a single binary.
- **AKS MCP server: available (open-source).** Natural-language provisioning/operation of AKS via MCP, secured by workload identity. (Presented as available now rather than newly GA.)

## 💡 Demos
- **AI Runway (voiced by Ralph, ~3 min):** browse the model catalog (Qwen/Phi/DeepSeek/Llama) with per-card **GPU-fit indicator**; pick **DeepSeek R1 671B** from the Hugging Face gallery; select **NVIDIA Dynamo** runtime; it recommends **3 nodes / 24 GPUs**; **cluster autoscaler** brings nodes online; attach **Azure Managed Lustre** RWX persistent volume for cached weights; **live cost estimate**; rollout to running; consume via **Gateway API Inference Extension + Istio** single endpoint with an **OpenAI-compatible curl**. "3 minutes vs the 3 weeks it used to take."
- **Anyscale on Azure end-to-end (with Bob, ~7 min):** create an **Anyscale Cloud** entirely in the **Azure portal** (subscription/RG/region/cluster, managed identity, ACR); launch the **Anyscale UI with the same Azure credentials**; open an **embedded VS Code** notebook; **fine-tune an embedding model** on a product-catalog of images (better recommendations, accuracy graphs, before/after embedding clusters); **serve 3 endpoints** (HTTP ingress + image-to-text + recommendations); view **integrated monitoring/observability** with dependencies. "7 minutes vs the 3 months it used to take."
- **KARS + OpenClaw (live, unedited, ~2 min):** `kars up` on a real AKS cluster; **`kars-system` namespace**; declaratively run **OpenClaw** via a Kubernetes custom resource; introspect agents/sandboxes/policies in **Headlamp (KARS plugin)** + **mesh topology**; `kars list` → connect → token-embedded OpenClaw URL; ask the live agent **"what announcements did Microsoft have with NVIDIA this week?"** → it browses the web and returns a fresh analysis.

## 📊 Notable Stats / Quotes
- **"Kubernetes is a big hammer, and with a big hammer everything looks like a nail."** — the honest framing of when *not* to use it.
- **"Kubernetes is necessary, but it's not sufficient"** for AI — the session's thesis.
- **"We're not giving you anything new — we're just shaping it for AI."** (every serving primitive is one you already operate).
- **"AKS is the cluster, Ray is the workload."**
- **AI Runway demo: ~3 minutes** vs **"3 weeks"** the manual way.
- **Anyscale demo: 7 minutes** vs **"3 months"** the manual way.
- **DeepSeek R1 = 671B parameters**, requiring **24 GPUs across 3 nodes** (won't fit one 8×H100 node).
- **Agentic orchestration is "arguably the least mature part of the stack"** and "changing very rapidly."
- **Wave's AI driver: autonomous driving in Tokyo after only ~4 months**, using **thousands of GPUs** stitched into a flexible supercomputer (AKS + Anyscale/Ray).
- **AKS Claw:** every new on-call engineer **up and running within minutes** with minimal training.
- **Four announcements** spanning single-cluster, multi-cluster, and fleet.
- Speaker has **10+ years in Kubernetes**; likens agentic AI on Kubernetes to a "world of pure imagination" (Wonka) and his original Kubernetes "aha moment" scaling 1 → 100 containers.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Spin up **AI Runway + KAITO** on a test AKS cluster; deploy a small open-weight model (Phi/Qwen) and hit the OpenAI-compatible endpoint; watch the **GPU-fit indicator** + KEDA autoscaling.
  - Try **`azure/kars`** (`kars up`) against a local kind/minikube cluster, then run **OpenClaw** via the custom resource and introspect it in **Headlamp**.
  - Stand up the **AKS MCP server** in VS Code and provision/operate a throwaway cluster via natural language (with workload identity).
  - Evaluate **Anyscale on Azure (preview)** for a real fine-tuning/RL job — confirm the control-plane/data boundary split satisfies our sovereignty needs.
  - Codify a couple of our own **day-2 ops runbooks as "skills"** and expose them to an agent.
- [ ] Questions:
  - What's the production maturity / SLA story for **AKS on bare metal** GPU scheduling vs virtualized AKS?
  - How does **KARS** sandboxing (Azure Linux) compare to gVisor/Kata for agent isolation, and what's the blast-radius model?
  - Pricing/billing specifics for **Anyscale on Azure** managed Ray through the Azure agreement?
  - Is **KAITO**'s KV-cache-aware routing (inference pool) compatible with multi-tenant isolation at scale?
  - Roadmap for the named-but-uncertain agentic frameworks ("open floor"/"Hermes") — worth tracking?
- [ ] Relevant to:
  - Anyone running (or planning) **AKS** who is deciding **managed PaaS (Foundry) vs self-managed Kubernetes** for AI.
  - **Platform engineering / SRE** teams building internal AI platforms, day-2 agent ops, and cost-per-token controls.
  - **Regulated / sovereign** customers (banking, gov) needing data/weights to stay in-boundary (Entra ID, Key Vault, private ACR).
  - Teams scaling beyond one cluster → **Fleet** + Arc.

## 🔗 Related
- [[ODSP914 - Run AI at scale with Ray Kubernetes using Anyscale on Azure]]
- [[ODSP933 - Agentic infrastructure needs agentic observability]]
- [[DEM311 - Scale cloud-native workloads with Azure Linux]]
- [[OD827 - Build deploy and run Linux workloads on Azure]]
- [[OD870 - Azure Storage for AI workloads]]
- [[OD800 - Using autonomous SRE to move from alerts to action]]
- [[OD837 - Build and deploy AI at the edge for real-world impact]]
- [[BRK241 - From prototype to production build and run agents at scale]]
- Source list: [[2026 Build Session List]]

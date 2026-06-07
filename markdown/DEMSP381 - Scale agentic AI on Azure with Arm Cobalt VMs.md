---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ai
  - topic/azure
  - topic/arm
  - topic/cobalt
  - topic/infrastructure
source: https://www.youtube.com/watch?v=MGCfkPbRMzU
session_code: DEMSP381
event: Microsoft Build 2026
speakers: Samir Nori (Arm), Goa (Microsoft Azure Arm product team), demo presenter (Arm)
duration_min: 17
aliases:
  - Scale agentic AI on Azure with Arm Cobalt VMs
---

# DEMSP381 — Scale agentic AI cost-efficiently on Azure with Arm Cobalt VMs

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Samir Nori (Software & Ecosystem team, Arm) · "Goa" (Arm product team, Microsoft Azure) · Demo presenter (Arm)  
> **Duration:** ~17 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=MGCfkPbRMzU)

> [!note] Transcript caveat
> This is a short partner/sponsor demo session and the auto-captions garbled several speaker names and a few product terms. The second presenter is introduced as "Goa" (likely a phonetic spelling), and the demo presenter's name was inconsistently captioned ("Renee"/"Kren"). Product names were corrected to their plausible real forms (e.g. "five model" → **Phi model**, "onx" → **ONNX**, "R 64"/"64" → **Arm64 / Aarch64**, "coord/cobwalt" → **Cobalt**). Nothing was invented beyond these corrections.

## 🎯 TL;DR
Arm and Microsoft used this session to spotlight the newly previewed **Azure Cobalt 200 VMs** — Microsoft's second-generation in-house, custom-built Arm-based server processor — and position them as the cost-efficient compute platform for cloud-native and **agentic AI** workloads. The headline is **~50% better per-core price/performance over Cobalt 100** (which itself was ~50% better than the prior generation), built on **3nm** on the latest Arm architecture with **Azure Boost** built in. Microsoft's own first-party services (Teams, Defender) already run on Cobalt 100 in production, and the new lineup adds memory-optimized and storage-dense VM families aimed squarely at AI sandboxes and microservices. The closing live demo ran an agentic shopping-cart application **entirely on CPU, locally and privately** (no external LLM call), using a **Phi model + ONNX runtime** across a mixed Cobalt 100/200 cluster to prove agentic workloads scale cost-efficiently on Arm without GPUs.

## 🔑 Key Takeaways
- **Cobalt 200 VMs are in preview** (announced by Satya in the Build keynote), the second generation of Microsoft's custom-built, purpose-built-for-server Arm processor.
- **~50% better per-core performance vs Cobalt 100** — and Cobalt 100 was already ~50% better than the generation before it, so two consecutive ~50% per-core leaps.
- Built on **3nm process technology** on the **latest Arm architecture**, and the VMs come **innately supported with Azure Boost** (offloaded networking/storage).
- The processors are **in-house designed by Microsoft**, optimized first for Microsoft's own first-party workloads and a broad set of third-party workloads.
- **Production proof from first-party Microsoft services**: **Microsoft Teams** runs on Azure Cobalt 100, and **Microsoft Defender** uses Cobalt as its default processor for its workloads.
- **Expanded VM families** beyond Cobalt 100's D / Dp / E series: now also a **memory-optimized** family (~**16 GB memory per core**) and an **L-series dense local-storage** family targeted at agentic AI and cloud-native workloads.
- **Agentic AI is the strategic narrative** — Cobalt 200 is pitched as ideal for sandbox creation, full agent request loops, and packing many sandboxed agents densely into a single VM.
- **Preview is in 8 regions today**, with more regions planned at **GA**.
- **Arm scale/ecosystem credentials:** ~30 years old, ~**350 billion chips** shipped, ~**22 million** Arm developers, ~15 years building the server ecosystem, and **~95% of CNCF projects support Arm**.
- **Demo punchline:** an agentic shopping app ran **100% on CPU, fully local and private** (data never leaves the cluster, no third-party LLM) using a **Phi model via ONNX**, including context retention (table/KV-style cache) across prompts.
- Arm offers a **migration program** (resources, a "CP/Copilot-style" assistant, and engineering expertise) to help customers/partners port workloads to **Arm64**.
- Hands-on **labs** were offered (sign-up, sessions the next day) for attendees to try the demos themselves.

## 📚 Detailed Notes

### Framing: the Arm ↔ Microsoft partnership
Samir Nori (Arm Software & Ecosystem team) opened by setting context for the partnership and Arm's role. Arm has been around ~30 years and has shipped close to **350 billion chips**, positioning itself as "the computing platform for all devices — from cloud to edge." For this session the focus is specifically **data center and cloud**, and the collaboration with Microsoft/Azure.

He framed the Microsoft partnership as resting on **two pillars**:

1. **Silicon innovation** — Arm works with Microsoft's hardware and systems teams on designing, developing, and deploying the **Cobalt** chip. There are now **two generations**: the prior gen launched with ~**50% better price/performance** than what came before it, and **Cobalt 200 is now ~50% better again than Cobalt 100**.
2. **Software enablement** — making the broad software ecosystem run well on Arm. Arm cites ~**22 million developers**, ~**15 years** building this ecosystem, and **~95% of CNCF projects supporting Arm**. Support spans Linux, cloud-native (CNCF), AI/ML, and a wide range of SaaS/enterprise and ISV packages.

The takeaway of the intro: there is broad, mature software support on Arm, so moving workloads to Arm-based Azure VMs is low-friction.

### Cobalt 100 success story (the baseline)
The second presenter ("Goa," from the Arm product team at Microsoft) grounded the new announcement in Cobalt 100's track record. **Cobalt 100 launched in 2024** and the response has been "tremendous":

- Strong adoption across **both enterprise and cloud-native** customers, many already onboarded and seeing significant price/performance benefits.
- Crucially, **first-party Microsoft proof points**: **Microsoft Teams runs on Azure Cobalt 100**, and **Microsoft Defender** has made **Cobalt its default processor** for driving its workloads.
- The argument: these first-party deployments are a testament that the **price/performance is "immense and unmatched"** versus other offerings.

### Cobalt 200: what's new (the core announcement)
**"Yesterday's story was Cobalt 100; today Satya announced Cobalt 200 VMs."** Key technical points:

- **In-house, custom/purpose-built for the server space by Microsoft** — optimized for Microsoft's first-party workloads and a variety of third-party workloads. (Both Cobalt 100 and 200 are Microsoft-designed silicon.)
- **Azure Boost built in** — Cobalt 200 VMs come innately supported with Azure Boost (Azure's hardware offload for networking/storage performance).
- **~50% better per-core VM performance** vs the previous (Cobalt 100) generation.
- **3nm process technology** on the **latest Arm architecture** — the source of the per-core gains.

The framing emphasizes translating the per-core silicon gains into customer value via the VM offerings.

### Expanded VM families
Cobalt 100 shipped **D, Dp, and E** series. Cobalt 200 extends the lineup to fit essentially any workload:

- **D / Dp / E series** — general-purpose (carried forward).
- **Memory-optimized family** — roughly **16 GB of memory per core**, for memory-hungry workloads.
- **L-series, dense local-storage optimized** — explicitly targeted at **agentic AI and cloud-native workloads** (lots of fast local storage per VM).

Goal: with this breadth, any enterprise or cloud-native workload can find a fitting Cobalt 200 VM size.

### Benchmarks (the developer slide)
The presenter walked a benchmark slide aimed at developers:

- **Left side: industry-standard benchmarks** — notably **SPECrate** — compared against the previous generation on a **per-vCPU performance basis**.
- **Right side: Microsoft's own benchmarks and Microsoft products.**
- The claim: **industry benchmarks and Microsoft benchmarks tell the same story** — substantially higher performance than the previous generation, with Microsoft's own first-party products serving as additional real-world evidence (alongside third-party customer results).

(No specific benchmark numbers beyond the recurring "~50% per-core" improvement were stated verbally in the transcript.)

### Why Cobalt 200 + agentic AI
The forward-looking thesis: **"the future is about agentic AI."** Cobalt 200, being strong in the **cloud-native** space, is positioned to excel at agentic patterns:

- **Sandbox creation** for agents.
- Running the **full agent loop** (creating a request and executing the entire loop).
- **Density** — fitting as many sandboxed agents as possible into a single VM.

The promise across all of these is **unmatched price/performance**.

### Availability
- **Preview today in 8 regions.**
- **More regions to be added at GA.**
- The presenter offered to take questions afterward and handed off to the demo.

### Demo: agentic, CPU-only, local & private (the centerpiece)
The demo presenter (Arm) reframed the industry shift first: traditional cloud-native and classic apps had **fixed workflows** (get from point A to B, run a few tasks, done). The industry is now moving toward **AI-first / AI-native / agentic** applications, where existing apps gain agentic capabilities. Cobalt VMs support **both families** — fixed/traditional workflows on Cobalt 100 and the newer agentic-capable workloads on Cobalt 200 — and the point of distributed microservices is scaling an app across **hundreds of nodes**.

What the live demo showed (a "busy slide" with a three-tier architecture):

- **Tier 1 — microservices app:** a **polyglot microservices "shopping cart" application**, with its microservices running on **Cobalt 100** VMs.
- **Tier 2 — orchestration:** running on the newer **Cobalt 200** VMs, which are capable enough to execute **CPU inference** without needing any external accelerator/service.
- **Tier 3 — serving:** provisioning **multiple pods** to serve the intensive (inference) requests generated by the application.

**The critical property:** *everything runs on CPU, inside the cluster.* **Data never leaves** — no third-party LLM call — so it is **fully local and private**. The presenter added agentic agents that manage the workflow, all running locally within the cluster with no external dependency.

Live interaction shown via the app's web UI:
- The presenter prompted the agent with a **budget of ~$2,000** and asked it to add items; the agent tracked spend (e.g., **"~$700 left"** after some items), demonstrating a budget-aware scanning/selection service.
- Asked for **shoes**, the agent returned a single relevant suggestion (not a generic list), and critically **maintained conversational context across turns** — described as using a **table/KV-style cache** so prior context (the budget, prior items) carried over rather than re-querying from scratch.
- The agent added the selected items to the cart, all computed **on CPU and locally**.

**Implementation details called out:** the demo used a **Phi model** with the **ONNX runtime** to do the inference on CPU, inside the cluster. (Process counts were referenced for the different node tiers — e.g., the Cobalt 200 tier handling the heavier 200+ process load — though the exact figures were partly garbled in captions.)

The point proved: **agentic AI workloads — including model inference with context/memory — can run cost-efficiently on Arm-based Azure CPUs, entirely local and private, with no GPUs and no external LLM dependency.**

### Closing: labs + migration program
- **Hands-on labs** were offered — a lab the next day (sign-ups; times mentioned around **6:30 / 9:00**) for attendees to run the demos themselves and talk to the team.
- **Migration program:** Arm helps customers and partners on their journey to **Arm64**. Whether just starting or already underway and wanting **performance analysis on CPU**, customers can reach out to get a **migration resource/assistant** plus **engineering expertise** from Arm.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Cobalt 200 VMs** — Microsoft's 2nd-gen, in-house custom Arm-based server CPU; ~50% better per-core vs Cobalt 100; 3nm; latest Arm architecture; the session's focus. *(Preview.)*
- **Azure Cobalt 100 VMs** — 1st-gen Microsoft Arm server CPU (launched 2024); the production baseline running first-party workloads.
- **Azure Boost** — Azure's hardware offload (networking/storage acceleration) innately supported on Cobalt 200 VMs.
- **Cobalt VM families** — **D / Dp / E** (general purpose), a **memory-optimized** family (~16 GB/core), and an **L-series** dense local-storage family for agentic AI / cloud-native.
- **Arm / Arm64 (Aarch64)** — the underlying CPU architecture; the migration target.
- **Microsoft Teams** — first-party Microsoft service cited as running on Cobalt 100.
- **Microsoft Defender** — first-party Microsoft service using Cobalt as its default processor.
- **Phi model** — the small language model used in the demo to run inference on CPU. *(Caption said "five model"; corrected to Phi.)*
- **ONNX (ONNX Runtime)** — used to run/interface the Phi model for CPU inference. *(Caption said "onx".)*
- **SPECrate** — industry-standard benchmark used for per-vCPU performance comparisons.
- **CNCF projects / cloud-native ecosystem** — ~95% of CNCF projects support Arm; basis of the cloud-native readiness claim.
- **Polyglot microservices "shopping cart" app** — the demo application spanning the multi-tier Cobalt cluster.
- **Pods / cluster (Kubernetes-style)** — used to scale and serve inference requests inside the cluster.
- **Table/KV-style cache** — mechanism cited for retaining agent conversational context across prompts.
- **Arm migration program** — assistance (resources + assistant + engineering expertise) to port workloads to Arm64.

## 🚀 Announcements / What's New
- **Azure Cobalt 200 VMs — PREVIEW.** Announced by Satya in the Build 2026 keynote; this session expanded on it. ~50% better per-core performance than Cobalt 100, 3nm, latest Arm architecture, Azure Boost built in.
- **Preview footprint: 8 regions today**, with **more regions at GA** (GA date not stated).
- **New VM families on Cobalt 200:** memory-optimized (~16 GB/core) and L-series dense local-storage (for agentic AI / cloud-native) — in addition to D/Dp/E.
- (Context, not new) **Cobalt 100** general availability and production first-party adoption (Teams, Defender) referenced as the proven baseline.

## 💡 Demos
- **Agentic shopping-cart app, CPU-only and fully local/private.** A polyglot microservices shopping app ran across a mixed cluster — microservices on **Cobalt 100**, orchestration on **Cobalt 200** doing CPU inference, and pods serving intensive requests. Using a **Phi model via ONNX**, the agent handled a budget-aware shopping task (~$2,000 budget, tracked remaining spend, returned a targeted shoe suggestion) and **retained context across prompts** via a table/KV-style cache.  
  **Point proved:** agentic AI — including model inference *with* memory/context — runs cost-efficiently on Arm-based Azure CPUs, entirely inside the cluster with **no external LLM and no data leaving the environment** (private by design), and **no GPUs required**.

## 📊 Notable Stats / Quotes
- **~50% better per-core performance, Cobalt 200 vs Cobalt 100** — and Cobalt 100 was likewise **~50% better** than the generation before it.
- **3nm** process technology, **latest Arm architecture** (Cobalt 200).
- **~16 GB memory per core** on the memory-optimized Cobalt 200 family.
- **8 regions** in preview at launch; **more at GA**.
- **Cobalt 100 launched in 2024.**
- Arm scale: **~30 years**, **~350 billion chips shipped**, **~22 million developers**, **~15 years** building the server ecosystem, **~95% of CNCF projects support Arm**.
- Demo: **~$2,000 budget**, **~$700 remaining** after items — illustrating budget-aware agent behavior.
- **"Cobalt is their default processor"** — on Microsoft Defender's use of Cobalt.
- **"All of this is happening on a CPU and inside that cluster. So your data is not going outside. You're not talking to a third-party LLM and everything is local and private."** — demo presenter (paraphrased from captions).

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Spin up a **Cobalt 200** VM (preview, one of the 8 regions) and benchmark a representative .NET/Linux workload vs an equivalent x86 D-series; compare price/perf.
- [ ] Things to try: Reproduce the demo pattern — run a **Phi model via ONNX Runtime on Arm64 CPU** for a small agent loop; measure latency/throughput and whether CPU-only inference is viable for the use case.
- [ ] Things to try: Evaluate the **L-series (dense local storage)** and **memory-optimized (~16 GB/core)** families for agent-sandbox density.
- [ ] Questions: What are the **actual SPECrate numbers** and real-world price/perf deltas (the talk only said "~50% per-core")? Which **8 regions** are in preview, and is **australiaeast** among them?
- [ ] Questions: What model sizes/quantizations of **Phi** are practical CPU-only on Cobalt 200, and at what concurrency? How does the table/KV cache work in their agent stack?
- [ ] Questions: Migration program specifics — what is the "migration resource + assistant" they offer, and is there tooling to flag Arm64 incompatibilities?
- [ ] Relevant to: Cost-optimization of Azure compute; agentic/AI-native app architecture; private/local inference (data-residency-sensitive workloads); cloud-native/Kubernetes platform decisions; Arm64 migration planning.

## 🔗 Related
- [[Build2026]]
- Topic: Azure Cobalt 100 / Cobalt 200, Arm64 on Azure, Azure Boost
- Topic: Agentic AI, CPU inference, Phi models, ONNX Runtime
- Microsoft Build 2026 keynote (Satya — Cobalt 200 preview announcement)

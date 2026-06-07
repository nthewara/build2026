---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/ray
  - topic/kubernetes
  - topic/ai
  - topic/scaling
  - topic/anyscale
  - topic/aks
source: https://www.youtube.com/watch?v=nwR1NBm3Uug
session_code: ODSP914
event: Microsoft Build 2026
speakers: Katerina (Product Marketing Manager, Anyscale); Daniel Ariza (Field Engineer, Anyscale)
duration_min: 23
aliases:
  - Run AI at scale with Ray Kubernetes using Anyscale on Azure
---

# ODSP914 — Run AI at scale with Ray + Kubernetes using Anyscale on Azure

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Katerina — Product Marketing Manager, Anyscale; Daniel Ariza — Field Engineer, Anyscale  
> **Duration:** ~23 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=nwR1NBm3Uug)

## 🎯 TL;DR
Anyscale on Azure brings the managed Ray platform — built by the creators of Ray and powered by **Ray on AKS** — into your own Azure subscription. It targets teams who want to *own* (not just rent) their AI stack: deploying, fine-tuning, and serving open-source and custom models while keeping proprietary data and IP inside their existing Azure security and governance boundary. The session pairs a "why own your AI stack" business framing with a full end-to-end technical demo: provisioning an Anyscale Cloud from the Azure portal onto AKS, then using Ray (Ray Data, Ray Train, Ray Serve) to build a multimodal e-commerce recommendation engine — fine-tuning a PyTorch model, running batch embeddings, and serving multiple composed models behind a single endpoint, all with one-click GPU scaling, fault-tolerant checkpointing, built-in observability, and CLI "skills" that let AI coding assistants generate and optimize Ray workloads.

## 🔑 Key Takeaways
- **AI is a rent-vs-own spectrum.** Renting = calling someone else's model via API. Owning is *not binary* — it spans deploying open-source models → customizing them with your own data → training your own models. Most teams use a mix; the real question is *which workloads* justify ownership.
- **Ownership makes sense when three drivers apply:** (1) **Control** over models/operations (avoid model deprecations, rate limits, outages), (2) **Data & differentiation** (keep proprietary data inside your boundary), and (3) **Cost & latency** (better unit economics at scale, faster end-to-end response).
- **Scaling AI is getting harder** because both data and models are exploding: structured tabular → multimodal data; gigabytes → petabytes; single models → many models; parameter counts growing exponentially. Legacy tooling wasn't designed for this.
- **Ray is the convergence point.** The open-source distributed compute framework for Python/AI has **12M+ downloads/week** and is the most widely adopted AI compute framework across AI labs and enterprises (OpenAI, Uber, Tripadvisor, and more).
- **Anyscale on Azure = three pillars:** (1) accelerates dev→prod with a **unified runtime** for multimodal data curation, distributed training, and multimodal online serving; (2) runs reliably at scale via **fully managed Ray lifecycle on AKS**, a **priority-aware scheduler** that maximizes GPU utilization, and **24/7 Ray expert support**; (3) is **Azure-native** — runs on AKS in your own subscription, integrates with **Entra ID for RBAC**, available through the **Azure portal**.
- **Provisioning is portal-driven.** Create an "Anyscale Cloud" by picking a subscription, resource group, region, and AKS cluster. Bring your own Kubernetes cluster, or use a **one-liner** to create AKS for you — no infra expertise required, but deep Kubernetes integration is retained under the hood.
- **Three core console primitives:** **Workspaces** (interactive dev — write/run code, see metrics/logs/observability), **Jobs** (run code over a larger dataset/production, then auto-shut-down the cluster when done), and **Services** (always-on endpoints serving models).
- **One-click elastic scaling.** A workspace runs on a Ray cluster; adding worker nodes (e.g. A100 GPUs, scaling from 1 to 10/100/1,000) is a button click — minimal effort to scale up.
- **Dev/prod parity.** You can open the same cluster in **VS Code Desktop over SSH** or a web VS Code interface, install deps via pip or a dependencies UI, and **freeze everything into a container image** for fully reproducible dev→prod.
- **Ray wraps standard frameworks, doesn't replace them.** It keeps PyTorch (and other OSS libraries) intact and adds an orchestration layer for performance, stability, and scalability across many CPUs/GPUs.
- **Ray Train delivers fault tolerance cheaply.** Adding checkpointing is ~10% more code; on any failure it resumes from where it left off — **even mid-epoch** — so massive multi-thousand-GPU runs stay reliable.
- **Ray Data keeps GPUs fed.** It streams data to the GPU and auto-scales CPU nodes so the CPU never becomes the bottleneck — avoiding the wasteful 20–30% GPU utilization that's common when GPUs starve for data.
- **Ray Serve simplifies multi-model serving.** Compose multiple models (e.g. image-to-text → fine-tuned recommender) behind one endpoint with far less code than hand-stitched Kubernetes microservices; supports **zero-downtime version rollouts**, independent per-model scaling, and **prefix-aware caching**.
- **Anyscale "skills" + CLI supercharge AI coding assistants.** `anyscale skills` exposes packaged capabilities (set up infra/platform, create Ray Data/Train/Serve workloads, RL for post-training, more coming) usable inside your favorite AI code assistant — and the agents can read the platform's metrics/observability to write and *optimize* code automatically.

## 📚 Detailed Notes

### Why teams choose to own their AI stack
Every team building with AI is positioned somewhere on a spectrum between **renting intelligence** (calling someone else's model through an API) and **owning it**. Crucially, ownership is not a single switch — it's its own sub-spectrum that includes (a) deploying open-source models, (b) customizing open-source models with your own data, and (c) training your own models from scratch. In practice most teams blend renting and owning; the strategic question is identifying *which specific workloads* warrant ownership rather than going all-in on either side.

Ownership typically becomes the right call when one or more of three conditions hold:
- **Control over models and operations** — so you're not exposed to model deprecations, rate limits, or provider outages that you can't influence.
- **Data and differentiation** — when proprietary data must stay inside your own security/governance boundary, and when your data is the source of competitive advantage.
- **Cost and latency** — when you need better unit economics at scale and faster end-to-end response times than an external API gives you.

When several of these stack up, that's the inflection point where teams move toward owning.

### Why owning is hard: data and models are scaling fast
The difficulty of building AI is rising because *both* inputs are scaling simultaneously:
- **Data:** what used to be structured tabular data is now **multimodal** (text + images + more), and dataset sizes have jumped from **gigabytes to petabytes**.
- **Models:** single models have become **many models**, and **parameter counts are growing exponentially**.

This complexity surfaces across the entire AI lifecycle:
- **Building** requires *coordinated CPU and GPU compute* (you can't treat them in isolation).
- **Training** must be *distributed across nodes with fault tolerance built in* — at scale, hardware/process failures are expected, not exceptional.
- **Serving** requires *composing many models*, often on *different hardware* profiles.

These are precisely the problems legacy tools were never designed to handle, which is why teams keep hitting their limits.

### Why Ray
As AI workloads grow in scale and complexity, teams are converging on **Ray** — the open-source **distributed compute framework for Python and AI workloads**. Ray adoption has tracked this growth:
- **12M+ downloads per week.**
- The **most widely adopted AI compute framework** across both AI labs and enterprises.
- Used by teams such as **OpenAI, Uber, Tripadvisor**, and more.

Ray's design lets the same framework span the building, training, and serving stages that legacy tools struggle to unify.

### What Anyscale on Azure is — the three pillars
**Anyscale on Azure** comes "from the creators of Ray" and is **powered by Ray on AKS**. Three things to know:

1. **Accelerates dev → prod** with a **unified runtime** covering multimodal data curation, distributed training, and multimodal online serving — one platform across the lifecycle instead of separate stitched tools.
2. **Runs reliably at scale** via:
   - a **fully managed Ray lifecycle on AKS** (Anyscale operates Ray for you),
   - a **priority-aware scheduler** that maximizes GPU utilization, and
   - **24/7 Ray expert support**.
3. **Azure-native** by design:
   - runs on **AKS in your own subscription**,
   - integrates with **Entra ID for RBAC**, and
   - is available **through the Azure portal**.
   The net effect: your **data and IP stay inside your existing Azure security and governance boundaries**.

### Demo part 1 — Provisioning an Anyscale Cloud from the Azure portal
Daniel begins in the **Azure console** and creates an **Anyscale Cloud** (from "Anyscale Clouds" → **Create**). The provisioning wizard asks for:
- **Subscription** to launch into,
- **Resource group** (he uses one created earlier),
- **Cloud name** (e.g. "my cloud"),
- **Region**, and
- an **AKS cluster** selection.

Key flexibility point: **bring your own Kubernetes cluster** if you already have one — deploy straight into it. If you're "not a Kubernetes wiz," there's a **one-liner to create the Kubernetes cluster for you**, so you don't have to think about the infra side. Either way, Anyscale **integrates very deeply with Kubernetes**, retaining all the power of that rock-solid infrastructure.

Remaining wizard steps: pick a **storage account** and the **identity** used to connect to it, choose an **Azure Container Registry** (it can create new resources for you), then set **support plan** and **tags**, and hit **Create**. Provisioning takes some time, so Daniel uses a pre-created cloud for the rest of the demo.

### Demo part 2 — The Anyscale console: Workspaces, Jobs, Services
The left-hand nav exposes three primitives:
- **Workspaces** — *interactive development*: write code, run it, observe how it behaves, and inspect observability (metrics, logs, etc.). Most of the demo lives here.
- **Jobs** — once code is ready for a *larger dataset or production*, launch a Job. It runs in the background over time and **turns off the cluster when done** (cost-efficient).
- **Services** — an **always-on** endpoint, ready to listen for requests and **serve models**.

Workspaces also offer **many templates** (inference, training, building a RAG system, etc.) as starting points.

### Demo part 3 — Inside a workspace: cluster, scaling, and dev environment
Daniel opens a pre-created workspace. The right panel shows it's running on a **Ray cluster**: **8 CPUs / 32 GB on one node**, with a single CPU-based worker node for now. To scale, he clicks **add worker nodes** and can request **GPUs** (e.g. **A100s**) at **10, 100, or 1,000** nodes depending on availability and the job's needs — "not a lot to do in order to scale things up."

Development options:
- **Open in VS Code Desktop** → launches VS Code and **SSHes directly into the cluster**, so dev and prod environments are nearly identical (same hardware/environment type).
- Or use the **web VS Code interface** in-browser.

He keeps all code in a **notebook** but notes you can use many Python files. **Dependencies** install via **pip** or a dedicated **Dependencies** UI, and you can **freeze all dependencies into a container image** for a **fully reproducible** dev→prod path.

### Demo use case — A multimodal e-commerce recommendation engine
The end-to-end scenario: build an **e-commerce recommendation engine**. Daniel reasons through the options (echoing Katerina's framing):
- Use a hosted **AI model provider endpoint** → likely **very expensive** and you **lose control**.
- Use an **open-source model** → much **cheaper**, but **less effective** because it doesn't know your data and tends to be smaller.
- **Chosen path:** **fine-tune an open-source model** using Ray, which requires data processing, then run **batch embeddings** (inference over all his data with the fine-tuned model).

Scale considerations baked into the use case:
- A large store may have **~1M products** with **~10% changing week over week**, so the pipeline must **re-run constantly** — making it a **scheduled Job**, needing real scale to produce a good model.
- The data is **multimodal** — products have **text descriptions *and* images** — so the embedding space must process text and images **together**.
- **Serving needs multiple models** — e.g. an **image-to-text** model feeding the **fine-tuned** recommender — behind a single endpoint.

The goal is a **full end-to-end solution**: data pre-processing → fine-tuning → batch embeddings → serving.

### Demo — Fine-tuning with Ray Train (`TorchTrainer`)
After installing dependencies and sampling images from the product catalog, Daniel builds a **training dataset** from sampled records, then uses a **`TorchTrainer`** — i.e. real **PyTorch** code. The important Ray principle: **Ray doesn't take PyTorch away.** It **wraps the standard OSS frameworks** and adds an **orchestration layer** for better performance, stability, and scalability (scaling to many CPUs/GPUs).

The trainer config specifies **epochs, batch size, how much to scale (1 worker → 1,000 workers), GPU count**, and **checkpointing**. A standout **Ray Train** capability: on a **failure at any point**, it **resumes from where it left off — even mid-epoch** — so you get fewer fully-failed runs. This is what makes scaling to **thousands of GPUs** reliable instead of brittle.

In the **per-worker train loop**, the body is **standard PyTorch**; adding checkpointing is "**~10% more code than you'd normally have**," and Ray then handles reliability/checkpointing for you. Daniel ran a couple of epochs and confirmed **training loss went down**.

### Demo — Keeping GPUs fed with Ray Data
The data loader uses **Ray Data** to feed the Ray Train job. Ray Data **streams data to the GPU**, keeping it **always fed** so you achieve **full GPU utilization** — avoiding the common **20–30% GPU utilization** that wastes scarce, expensive GPU capacity (and caps how good the model can get). It manages this partly by **scaling up CPU nodes** so the **CPU is never the bottleneck**; you can spin up as many CPU nodes as needed to keep GPUs saturated.

### Demo — Batch embeddings + evaluating the fine-tuned model
With a fine-tuned model in hand, Daniel **loads it** and runs **batch embeddings** (inference over his data). The embedding step runs on a single CPU in the demo but can scale to **`num_gpus=1000`** with "very little code change."

Evaluating embedding quality via **product embedding similarity**: **speakers, laptops, and webcams** cluster as similar to each other, but **not** to **shoes or sweaters** — sensible. Comparing the **base open-source model** vs the **fine-tuned model**, the fine-tuned model shows **better-clustered** results (the base model's light-blue group wasn't well grouped), confirming the fine-tune improved results.

### Demo — Serving multiple models with Ray Serve
Finally, the **serving** code creates an **endpoint** that listens for **recommendation requests** and runs through multiple models: first an **image-to-text** model, then the **fine-tuned** recommender, returning a **JSON response**. Without Ray, you'd likely hand-build and deploy **many microservices in Kubernetes** and stitch them together — painful. With **Ray Serve**, the code is much simpler.

Demonstrated output: querying recommendations similar to "travel wireless headphones" returns other wireless headphones and related items. The serving stack: a recommendation **endpoint** takes an **image** → runs the **image-to-text** model → runs the **fine-tuned** model → returns JSON. The fine-tuned product recommender loads the model and runs an **embedding norm** (standard PyTorch).

Deployment story: **`anyscale service deploy`** gets the service "up and ready to go" as an **always-available** service. As new versions ship, it supports **zero-downtime** rollouts, **independent per-model scaling** (e.g. if one model gets more traffic than another), and **prefix-aware caching** built in.

### Demo — Anyscale "skills", CLI, and observability/agents
You don't have to write all this code by hand. From the terminal, the **Anyscale CLI** (`anyscale`) exposes **`anyscale skills`** — packaged capabilities usable in your favorite **AI code assistants**: setting up **infra**, setting up the **platform**, and creating **workloads** (Ray **Data**, **Serve**, **Train** serving, **RL for post-training**, with **more coming**). The CLI can also **create jobs and services**.

Critically, these **skills/agents can read the platform's metrics and observability**. The **Metrics** tab surfaces utilization, node counts, memory, and CPU. **Ray Workloads** lets you drill into the **different stages** to find **bottlenecks**. If you're not an expert, the **agent can grab this telemetry and both write and optimize code** for you. Daniel stresses observability matters for **day one** ("I wrote code and it kinda works") *and* **day two** (you scaled up, things regress, and you need to debug).

### Next steps (closing)
Katerina closes with three calls to action:
- **First QR code** → the Anyscale **Build conference webpage**: scheduled **table talks** (including **Daniel's session on building multimodal data pipelines**) and a way to **request a meeting** with the team.
- **Second QR code** → **get started on Anyscale on Azure** to try the demo hands-on.
- **In person at Build:** visit **booth G201**.

## 🛠️ Products / Features / Technologies Mentioned
- **Anyscale on Azure** — managed Ray platform, powered by Ray on AKS, deployed into your own Azure subscription.
- **Ray** — open-source distributed compute framework for Python/AI (12M+ downloads/week).
  - **Ray Train** (`TorchTrainer`) — distributed training with mid-epoch fault-tolerant checkpointing.
  - **Ray Data** — streaming data loader that keeps GPUs fed and auto-scales CPU nodes.
  - **Ray Serve** — multi-model composition, zero-downtime rollouts, independent scaling, prefix-aware caching.
- **Azure Kubernetes Service (AKS)** — the underlying compute substrate ("Ray on AKS").
- **Azure portal / Azure console** — where Anyscale Clouds are provisioned.
- **Microsoft Entra ID** — RBAC integration.
- **Azure Container Registry (ACR)** — for container images during provisioning.
- **Azure storage account + managed identity** — workspace storage and access.
- **PyTorch** — the deep-learning framework Ray wraps (kept intact).
- **Anyscale console primitives** — Workspaces, Jobs, Services, Templates.
- **Anyscale CLI** (`anyscale`) — `anyscale skills`, `anyscale service deploy`, job/service creation.
- **Anyscale Skills** — packaged capabilities for AI coding assistants (infra, platform, Ray Data/Serve/Train workloads, RL for post-training).
- **VS Code Desktop (SSH) / web VS Code** — dev interfaces into the Ray cluster.
- **A100 GPUs** — example GPU type for scaling worker nodes.
- **Priority-aware scheduler** — Anyscale scheduler that maximizes GPU utilization.

## 🚀 Announcements / What's New
None explicitly announced as new in this session. The session positions **Anyscale on Azure** (Ray-on-AKS, Azure-portal-provisioned, Entra-integrated) as the offering to try, and notes that additional **Anyscale Skills** (including **RL for post-training**) are present with "more coming," but no dated GA/preview announcement is made in the transcript.

## 💡 Demos
A single continuous end-to-end demo led by **Daniel Ariza**, structured as:
1. **Provisioning** — create an Anyscale Cloud from the Azure portal onto AKS (subscription/RG/region/AKS cluster, storage + identity, ACR, support plan, tags). Bring-your-own AKS or one-liner cluster creation.
2. **Console tour** — Workspaces vs Jobs vs Services; templates (inference, training, RAG).
3. **Workspace internals** — Ray cluster (8 CPU / 32 GB), one-click worker scaling (A100s up to 1,000), VS Code Desktop SSH vs web VS Code, pip/Dependencies UI, freeze-to-container-image.
4. **Use case** — multimodal e-commerce recommendation engine (~1M products, ~10% weekly churn; text + image data; multi-model serving).
5. **Ray Train** — `TorchTrainer` fine-tuning with config (epochs/batch size/scale/GPUs/checkpointing); ~10% extra code for mid-epoch-resumable checkpointing; training loss decreased.
6. **Ray Data** — streaming to keep GPUs fed; CPU-node autoscaling to avoid bottlenecks; avoids 20–30% GPU utilization.
7. **Batch embeddings + evaluation** — load fine-tuned model, embed products, scale to `num_gpus=1000`; similarity check (speakers/laptops/webcams cluster together, not shoes/sweaters); fine-tuned model clusters better than base.
8. **Ray Serve** — endpoint chaining image-to-text → fine-tuned recommender → JSON; `anyscale service deploy`; zero-downtime versions, independent scaling, prefix-aware caching; sample recommendations for "travel wireless headphones."
9. **CLI / skills / observability** — `anyscale skills` for AI code assistants; Metrics tab (utilization/nodes/memory/CPU); Ray Workloads stage-level bottleneck drill-down; agents that read telemetry to write and optimize code.

## 📊 Notable Stats / Quotes
- **12M+ downloads per week** — Ray's adoption rate.
- **Most widely adopted AI compute framework** across AI labs and enterprises (OpenAI, Uber, Tripadvisor, and more).
- **Gigabytes → petabytes** — the shift in dataset sizes driving the scaling challenge.
- **8 CPUs / 32 GB on one node** — the demo workspace's starting Ray cluster.
- **Scale from 1 to 10 / 100 / 1,000 nodes** (e.g. A100 GPUs) with a button click.
- **~10% more code** — what adding fault-tolerant checkpointing to a PyTorch loop costs with Ray Train.
- **Resumes mid-epoch** on failure — Ray Train's checkpointing recovers without restarting the whole run.
- **20–30% GPU utilization** — the wasteful baseline Ray Data avoids by keeping GPUs fed.
- **~1M products, ~10% changing week over week** — the e-commerce scale that forces a scheduled, re-running pipeline.
- **`num_gpus=1000`** — how far batch embeddings can scale with "very little code change."
- **Booth G201** — Anyscale's in-person location at Build.
- > "What is special about Ray is that it doesn't take that stuff away. All it does is it wraps a lot of the open-source regular frameworks that you use and creates an orchestration layer around all of it so that we have better performance and better stability and also great scalability." — Daniel Ariza
- > "You're not getting those 20–30% GPU utilization, which is such a shame because we have such little availability of GPUs." — Daniel Ariza
- > "Your data and IP stay inside your existing security and governance boundaries." — Katerina (on Azure-native deployment)

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Provision an Anyscale Cloud into the default `australiaeast` Azure subscription and try the **one-liner AKS creation** path vs bring-your-own-AKS.
  - Stand up a minimal **Ray Train + Ray Data** fine-tune to feel the mid-epoch checkpoint resume and the GPU-fed streaming behavior.
  - Test **Ray Serve** multi-model composition (image-to-text → fine-tuned model) and a **zero-downtime** version rollout.
  - Install the **Anyscale CLI** and explore `anyscale skills` inside an AI code assistant; see how the agent reads Metrics/Ray Workloads to optimize a workload.
- [ ] Questions:
  - How does the **priority-aware scheduler** interact with AKS node pools / autoscaler and Azure GPU quota in `australiaeast`?
  - What's the pricing model (Anyscale platform fee vs raw AKS/Azure compute) and how does the auto-shutdown Job behavior affect cost?
  - How deep is **Entra ID RBAC** integration — workspace/job/service-level permissions? Does it map to existing AKS RBAC?
  - What GPU SKUs are actually available for Anyscale-on-AKS in Australian Azure regions (A100/H100 availability)?
  - Is there a GA/preview status and SLA for Anyscale on Azure, and what does "24/7 Ray expert support" cover?
- [ ] Relevant to:
  - Azure lab work where customers want to **own/fine-tune open-source models** while keeping data in-subscription.
  - Any AKS + GPU scaling scenarios; demos showing Ray as the distributed compute layer on Azure.
  - Multimodal data pipeline / RAG / recommendation-engine reference architectures on Azure.

## 🔗 Related
- [[Microsoft Build 2026]]
- Daniel Ariza's table talk — **building multimodal data pipelines** (Build 2026 schedule)
- Ray docs — Ray Train, Ray Data, Ray Serve
- Azure Kubernetes Service (AKS) + GPU node pools
- Microsoft Entra ID — RBAC for Azure-native services

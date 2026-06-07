---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/azure
  - topic/storage
  - topic/ai
  - topic/inference
source: https://www.youtube.com/watch?v=0aBr_9Unpco
session_code: OD870
event: Microsoft Build 2026
speakers: Saurabh Sen Sharma, Saloni Sonpal, Vishnu Charan
duration_min: 32
aliases:
  - Azure Storage for AI workloads
---

# OD870 — Azure Storage for AI workloads

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Saurabh Sen Sharma (PM, Azure Storage — AI workloads), Saloni Sonpal (PM, Azure OpenAI / Microsoft Foundry), Vishnu Charan (PM, Azure Storage — AI workloads)  
> **Duration:** ~32 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=0aBr_9Unpco)

## 🎯 TL;DR
This session reframes Azure Storage as a first-class performance and security layer for **agentic AI inference** — not just durable bulk storage. The team distills the storage problem for inference into three pillars: (1) bring enterprise data to agents as governed knowledge, (2) distribute/load models fast enough to keep expensive GPUs busy, and (3) optimize infrastructure utilization to maximize tokens-per-watt-per-dollar. The centerpiece is a three-tier **prompt caching** strategy in Microsoft Foundry — implicit (GPU memory) → extended (local SSD) → explicit **Azure Context Cache** (durable Azure Blob in the customer's tenant) — delivering up to 90% inference cost savings and dramatic TTFT reductions by reusing the KV cache of repeated prompt context. Live demos showed KV-cache offload to Blob via NVIDIA NIXL + LMCache (52s → 8s cold start, ~6× faster) and fast model-weight loading via the Run:AI Model Streamer (3–6× faster) plus a new Azure Container Storage distributed cache for AKS (2.5× faster at fleet scale). It closes by showing how Azure Files → Azure AI Search, Foundry IQ, and the new **Storage Center** hub turn raw enterprise data into agent-ready knowledge.

## 🔑 Key Takeaways
- **Storage is now a critical lever across the entire AI lifecycle** — training, fine-tuning, and (today's focus) agentic inference — wherever speed, scale, and security must converge.
- Two framings of storage + AI: **"storage for AI"** (storage powering AI workloads — this talk) vs **"AI for storage"** (AI making storage itself smarter, e.g. classification/ops). The session covers the former.
- **Inference is the dominant AI workload today**, and agentic inference multiplies storage load on every turn of the agent loop (more retrievals, more test-time compute, exponential growth of logs/conversation state/tool outputs/traces).
- **The static, unchanged portion of a prompt is >60% of inference cost** in most production agents — the GPU re-reads the same system prompt, tool definitions, and prior turns on every turn, driving up TTFT and end-to-end latency.
- **Prompt caching** caches the KV (key-value) attention state of repeated context tokens and reuses it, cutting GPU compute per turn dramatically — **up to 90% inference cost savings** with significantly lower time-to-first-token (TTFT).
- Microsoft Foundry offers **three tiers of prompt caching**: implicit (GPU memory, KB–low MB, 5–10 min to ~1 hr TTL), extended (GPU node local SSD, hundreds of GB, up to 24 hr TTL), and explicit (Azure Context Cache on durable Blob, days/weeks/months TTL).
- **Implicit and extended caching are node-bound** — cache is lost if the request routes to a different node/cluster/region or the TTL expires, forcing full prefill recompute. **Explicit caching (Azure Context Cache) solves this** by being node-independent and working across sessions, deployments, and regions.
- **Azure Context Cache** is a first-class Azure resource built on Azure Blob, living in the customer's own tenant, with a split-endpoint design: a **provider-only** endpoint writes encrypted KV state (model IP never exposed in clear text) and a **customer-only** endpoint controls TTL, retention, invalidation, and metrics.
- For OSS/BYO stacks, Microsoft contributed a **first-class Azure Blob backend to NVIDIA NIXL** (the inference transfer library), so any NIXL-speaking framework (vLLM, Dynamo, TensorRT-LLM, Ray) can read/write KV blocks to Blob with zero custom adapter code; **LMCache** offloads KV blocks straight to Blob via a plugin.
- **Model loading is the other half of cold-start cost** — beyond KV cache, every cold start must load model weights from storage to GPU (minutes for large models). The **Run:AI Model Streamer** with an Azure Blob plugin gives **3–6× faster cold starts** by chunking, parallel reads, CPU staging, and overlapping concurrent GPU copies that saturate the NIC.
- **Azure Container Storage distributed cache** (in early access) solves AKS fleet-scale cold starts: every GPU node is both cache and client (local NVMe RAID + zero-copy sendfile), so the first pod warms the cache and the rest read from inside the cluster — **2.5× faster model loading**, hitting Blob exactly once instead of 100 pods pulling 14TB simultaneously.
- **Bring enterprise data to agents** via native integrations: BlobFuse (POSIX mount), ADLFS (fsspec for Dask/Pandas/Ray), PyTorch connector, LangChain Azure Blob loader (5–10× faster), plus Azure Files as a data source for Azure AI Search (Logic Apps connector + native indexer), and **Foundry IQ** as Microsoft's unified governed knowledge layer with Blob as a first-class source.
- **Storage Center** — a new centralized hub (limited preview) for file, block, and object storage giving a unified view + a launchpad into the storage-for-AI experiences.

## 📚 Detailed Notes

### Framing: Storage for AI vs AI for Storage
The session opens by framing the storage/AI relationship in two categories:
- **Storage for AI** — storage as a foundational element of every AI workload, from training and fine-tuning to agentic inference (the focus of this talk). This is where **speed, scale, and security** must come together.
- **AI for storage** — using AI to make storage itself smarter: better data management, classification, and day-to-day operations.

This talk is exclusively about the first category, and specifically about **inference**, described as "the dominant AI workload today." The promise is making **agentic inference faster, cheaper, and more secure**, including turning enterprise data into agent-ready knowledge. The content applies whether you build on **Microsoft Foundry**, **AKS**, or **directly on Azure IaaS**.

### How Azure Storage plugs into the AI stack
At the **infrastructure layer**, the AI workload stack looks familiar: physical infrastructure (GPUs, NICs, local NVMe), then virtualization (VMs and Kubernetes nodes). The **differences emerge in storage**, because AI workloads demand high throughput and low latency at massive distributed scale across **three patterns**:
1. **Data prep** (ingestion/processing)
2. **High-throughput checkpointing** during training
3. **Model and data retrieval** during inference

The foundation is **Azure Blob** as the durable backing store, accessed through **purpose-built storage clients**:
- **BlobFuse** — POSIX-like file access
- **ADLFS** — for fsspec workflows
- **PyTorch connector** — high-throughput data loading
- **Azure Managed Lustre (AMLFS)** with its POSIX client — for HPC-class throughput
- **Azure Container Storage** — presents local NVMe as persistent volumes for stateful Kubernetes workloads (with Azure Files, Disks, and Elastic SAN support on the roadmap)

All of this is orchestrated across **VMSS and AKS**. The clients are optimized to plug into the AI runtimes/orchestrators the developer community uses today: **Ray, PyTorch, TensorFlow, vLLM, SGLang, Triton, and ONNX**. This same foundation powers **Microsoft Foundry**, the **AKS Kubernetes AI Toolchain Operator (KAITO)**, and the broader Azure AI infrastructure.

### Three intentional paths to run AI workloads
Azure deliberately offers **three paths**, with storage critical across all of them ("freedom of choice"):
- **Managed (Microsoft Foundry)** — the managed AI platform with access to Microsoft, partner, and open models. Great for teams who want abstraction.
- **Managed Kubernetes (AKS)** — for teams who want more control: bring your own models, frameworks, and orchestration, still deeply integrated with Azure infra.
- **Direct IaaS** — VMs, storage, networking, and AI-optimized silicon directly. This is where **hyperscale and megascale** AI customers operate.

Across all three, storage delivers the same outcomes: bringing enterprise data into the agent stack and powering fast, cost-effective, governable inference.

### Agentic inference from a storage-centric view
Any agent that leverages enterprise data is built on a **data pipeline anchored in object storage (Azure Blob)**, with two stages:

**Stage one — bringing enterprise data to AI services/agents (the data preparation pipeline):** ingestion → cleaning → chunking → embedding → indexing into a **vector database**, so the agent can do grounded retrieval with the right context. The **intermediate representations** — embeddings, indexes, processed chunks — are stored on **Azure Blob** so they can be retrieved with **milliseconds latency at query time** without rerunning the entire pipeline.

**Stage two — retrieve, store, and manage AI data at runtime:** every turn of the agent loop multiplies load on storage — more retrievals from Blob and the vector index, more test-time compute, and an **exponential explosion of logs, conversation state, tool outputs, and agent traces** that must all be persisted for fast downstream retrieval. At scale, distributed inference also **swaps models in and out across GPUs**.

This yields **three critical storage requirements for agentic inference** (the spine of the whole talk):
1. **Bring enterprise data securely to agents** and convert it into agent-accessible knowledge.
2. **Distribute and load models** onto AI compute fast enough to keep expensive GPUs busy.
3. **Optimize infrastructure utilization** to drive up **tokens per watt per dollar**.

### Pillar: Optimizing inference with prompt caching
The biggest lever for optimizing inference right now is **prompt caching**, because the way prompt tokens flow through the GPU is becoming one of the largest drivers of inference cost and latency as enterprises move from single-turn chat to long multi-turn agentic workflows.

**Inference today without caching:** Modern agents run on long, static enterprise context — system instructions, tool definitions, retrieval context — invoked across millions of invocations. In most production agents the **static unchanged portion of the prompt is >60% of inference cost**. On every turn the GPU recomputes model attention over the entire prefix (static system prompt + tool definitions + all prior turns). Turn two adds more history; turn three adds even more. A few turns in, the GPU is "burning expensive cycles re-reading the same tokens it has already seen." That recompute drives up **TTFT (time to first token)** and end-to-end latency, making long-context agents expensive to operate.

**With prompt caching:** Instead of recomputing attention every turn, **cache the KV state** of the repeated context tokens and reuse it. On turn one the GPU still processes the full prefix once, but as it does, it **writes the attention state out as a context-cached object**. Turn two loads the cached state and only computes attention on the new tokens; every subsequent turn is the same. Result: **dramatic reduction in GPU compute per turn → up to 90% inference cost savings** plus significantly lower TTFT. This is so impactful that providers like **OpenAI already offer implicit prompt caching APIs out of the box** — a great starting point, but **implicit caching alone is not enough** for enterprise scenarios.

### The three tiers of prompt caching in Microsoft Foundry
Foundry treats prompt caching as an **evolution across three tiers**, each for a different workload scale:

**1. Implicit prompt caching — "fast by default."** The KV cache sits **directly in GPU memory** alongside the inference engine. Ideal for real-time agents, multi-turn conversations, and short-lived workloads. Supports **KB to low MB**, with **TTLs typically 5–10 minutes, up to ~1 hour**. Advantage: speed + simplicity — the **model provider owns the cache and API**; the customer benefits from improved performance with **zero application changes**. *Already supported in Foundry.*

**2. Extended prompt caching — the cost-efficient scale tier.** As workloads scale (longer conversations, richer media, larger datasets), GPU memory limits appear. Extended caching **moves the cache onto the GPU node's local SSD**, enabling **hundreds of GB** of capacity and **TTL up to 24 hours**. Still managed by the model provider, but lets customers retain context much longer. *Generally available in Foundry starting May 2026.* Customers can set the prompt cache retention option to 24 hours, or leverage it by default on **GPT-5.5 or newer** model deployments.

**The node-bound limitation:** Both implicit and extended caching are **node-bound**. If a request routes to a **different node, cluster, or region**, or if the **TTL expires**, the cache is lost and the **full prefill compute cost is incurred again**. This is a problem for long-running agents, global workloads, and scenarios where context must be reused across the enterprise.

**3. Explicit prompt caching — Azure Context Cache.** Foundry addresses the node-bound gap with **Azure Context Cache**, a first-class Azure resource purpose-built to store preprocessed context in **durable storage within the customer's own tenant**. Built on **Azure Blob Storage**, it removes size constraints, extends **TTL to days/weeks/months**, and **operates independently of nodes** — working seamlessly across sessions, deployments, and regions. The **API is owned by the inference layer**, making it portable across models and frameworks. The vision: "prompt caching as a core system capability of the AI platform, not tied to where your request lands," delivering consistent, guaranteed savings wherever reusable context exists.

### Inside Azure Context Cache (enterprise-ready design)
At its core, Azure Context Cache is **durable storage of model KV prompt objects inside the enterprise's own Azure tenant**, with three properties that make it enterprise-ready:
1. **Provider-only write endpoint** — writes the **encrypted KV state** into the cache. The model's IP (the attention representation) is **never exposed to the customer in clear text**.
2. **Customer/developer-only endpoint** — gives the enterprise full control over **TTL, retention, invalidation, and metrics**. As the AI developer, "you own the lifecycle of your own cache."
3. **Low-latency and highly performant** — milliseconds latency and **several tens of millions of tokens per minute** of throughput at global scale, with a **neutral API** that integrates cleanly with **Microsoft Foundry** today, and in future with **AKS** and **third-party frameworks**.

### Outcomes that matter (developer benefits of explicit caching)
Saloni summarized five outcomes:
1. **Cost & efficiency** — explicit prompt caching improves **cache hit rates** and delivers durable cost savings on the cached portion of the prompt; for **GPT-5 class models** this lets inference scale economically.
2. **Throughput** — supports **multi-million tokens-per-minute** throughput for GPT-5 class models, providing headroom for high-concurrency agent workloads without bottlenecks.
3. **Latency** — retrieving from context cache is **orders of magnitude faster** than recomputing full prefill → a **step-function reduction in TTFT**; in multi-turn scenarios it also improves observed end-to-end latency across concurrent users.
4. **Security & control** — a **bring-your-own-resource** model with purpose-built protection for model IP and secure access, all running in the customer's own Azure tenant, preserving enterprise-level access controls.
5. **Observability** — rich cache diagnostics and fine-grained TTL control to tune cache behavior per workload and understand its impact.

### OSS path: KV caching to Blob via NVIDIA NIXL + LMCache
For customers building agents with **their own open-source toolchains/models**, the reason explicit caching works is that **the cache no longer lives on the GPU node — it lives on durable Azure storage**, unlocking the full scale of Azure Blob behind the KV cache: effectively **unlimited capacity, configurable retention, multi-region reach**.

**NIXL (NVIDIA Inference Xfer Library)** is NVIDIA's unified API for moving model weights and KV blocks across memory tiers, with a **pluggable backend** underneath. Microsoft **contributed a first-class Azure Blob backend** into NIXL, so any NIXL-speaking framework — **vLLM, Dynamo, TensorRT-LLM, Ray** — can read/write KV blocks to Azure Blob with **zero custom adapter code**.

The most immediate payoff is **LMCache**, the open-source KV-cache layer widely used with vLLM. Through Microsoft's plugin, **LMCache offloads KV blocks straight to Blob**. So the picture is consistent across the stack:
- **Managed customers** land on **Azure Context Cache**.
- **OSS developers** land on **Azure Blob via NIXL + LMCache**.

Both paths put KV cache on **durable Azure storage that travels with the workload, not the node**.

### Pillar: Fast model loading and distribution
KV cache is only **half** of the cold-start story — every cold start must also **load the model weights** from storage onto the GPU. For small models that's seconds; for large ones it's **minutes**. Same problem, same fix: **saturate the NIC straight out of Blob**.

**Run:AI Model Streamer** is an open-source loader for large model weights that plugs straight into the engines people run in production (**vLLM and SGLang**). Drop it in, point it at a storage account, and it replaces the default loader. Cold starts are "the tax every GPU pays when it comes up" — auto-scaling out, recovering a failed node, rotating a model, or loading a fine-tune on demand. The default loader makes that tax **unpredictable and minutes long** on big models, so the bigger the fleet, the more capacity is burned waiting for weights.

**How the streamer differs:** it **splits the model file into chunks**, pulls them from object storage **in parallel**, stages them in CPU, and pushes chunks to GPU memory **concurrently**. The reads and copies **overlap**, so the NIC stays saturated and the GPU is fed as fast as the network allows. Microsoft built the **Azure Blob plugin for the Run:AI streamer** — weights flow straight out of Blob through CPU into the GPU; the Blob container is the source of truth and the NIC is the only bottleneck. Result: **3–6× faster cold starts than the default loader, consistently**.

### Pillar (AKS scale): Azure Container Storage distributed cache
Everything demoed up to this point was a single pod / single GPU box. But **production isn't one pod — it's a hundred**, and each must pull the model down before serving a token. Doing the math: a **70B model is ~140GB**; **100 pods coming up together = ~14TB out of Blob all at once** → throttling, NIC saturation, and **cold starts stretching to ~10 minutes** — every minute being GPU you pay for and get nothing back.

The fix: a **distributed cache inside the AKS cluster itself**, with **zero changes to the workflow on top** (Hugging Face loader, BlobFuse, Run:AI streamer all sit on top unchanged). Underneath, **every GPU node is both a cache and a client**: local **NVMe RAID** holds the hot data, served at NVMe speed with **zero-copy sendfile**; anything missing comes in over the network from a peer with **ingress acceleration** on the fabric inside. The **first pod warms the cache; the next 99 read from inside the cluster** → **2.5× faster model loading on AKS**, with **Blob hit exactly once**.

This is **Azure Container Storage's new distributed cache**, built for AI on AKS: NVMe-class latency, throughput to local network saturation, Kubernetes-native, minimum-to-zero changes on the customer side. **In early access** — sign up via the on-screen QR code.

### Pillar: Bringing enterprise data to AI inference (native ecosystem integrations)
None of the compute story runs without data — the model, the cache, the context windows, the retrieved documents all live in storage. For inference, the bottleneck isn't *whether* you have the data, it's **how fast you can feed it into the GPU**. The guiding principle: **"meet developers where they are"** with native integrations across the entire AI ecosystem so that whatever stack you're on (Python, Spark, Ray, PyTorch, or an agent framework) you reach Blob without friction.

Key integrations called out:
- **BlobFuse** — POSIX-like mount; treat object storage like a local file system, same experience across VMs, containers, and AKS.
- **AzCopy** — data movement.
- **ADLFS** — Python-native, fsspec-compatible interface; makes Blob instantly usable from **Dask, Pandas, and Ray**.
- **PyTorch connector** — plugs directly into dataset, dataloader, and checkpoint APIs; no custom code, **zero-config auth with Azure Identity**.
- **Run:AI Model Streamer** — cuts cold-start times, loading models from Blob **6× faster** (as demoed).
- **NVIDIA NeMo / NIXL** — drops into NVIDIA's data movement stack with **KV cache offload** and high-performance model transfers across Dynamo, vLLM, Ray, etc.
- **LangChain Azure Blob loader** — faster ingestion and lower memory footprint for large document corpora: **5–9× faster lazy load, 7–10× faster non-lazy load** vs the community loader.

The summary: Blob "isn't just scalable infrastructure underneath — it's deeply integrated into the AI developer ecosystem with high-performance, secure, seamless access across training, inference, and agent workflows."

### Closing the loop: enterprise data → agent-ready knowledge
Returning to the **knowledge** half of agentic inference (turning enterprise data into agent knowledge): in the past Microsoft has shown how Blob storage plugs directly into AI services like **Azure AI Search** and **Microsoft Foundry** to turn enterprise data into agent-ready knowledge with just a few API calls. But many customers have **unstructured enterprise data on Azure Files** too — file shares, SMB workloads, lift-and-shift estates — and need the same ease of getting that data into AI.

**Azure Files is now a data source for Azure AI Search**, with two ways in:
1. **Azure Files Logic Apps connector** — a low-code path to connect a file share and create a vector or hybrid index; it also handles **re-indexing** as data changes.
2. **Native Azure Files indexer in Azure AI Search** — for teams that want **finer control** over enrichment and indexing.

Either way, the path from a file share to a **RAG (retrieval-augmented generation)-ready index** is now only a few clicks or a few lines of code.

**Foundry IQ** takes this further: it's **Microsoft's unified knowledge layer for agents**. Instead of every agent reinventing its own retrieval stack, Foundry IQ gives a **single governed knowledge layer** that any agent in Microsoft Foundry can ground against. **Azure Blob is a first-class knowledge source** for Foundry IQ — just point it at a Blob container and enterprise data becomes agent-accessible knowledge with the **security, lineage, and governance** of Azure storage already in place and **no glue code**. Foundry IQ also supports **Azure AI Search indexes** built on Azure Blob or Azure Files data. This closes the loop between the **data plane** (Azure storage) and the **agent plane** (Microsoft Foundry) — from raw enterprise data to grounded, governed agents in a few steps.

### Storage Center — the unified entry point
To give AI developers and storage admins a single place to discover Azure Storage's AI capabilities and wire data into agent inference fast, the team introduced **Storage Center**: a **centralized hub for file, block, and object storage**, all in one place. It provides a **unified view** of the storage landscape (usage, performance, redundancy tiers) plus tools like **lifecycle management** and **Storage Mover** with rich visualizations. The message from customers/partners/developers was that this is the **best place for both admins and developers to land their data** (starting with Blob) and then connect it to AI. From Storage Center you can **launch into the storage-for-AI experiences** covered in the session. **Announced as a limited preview** — sign up via the on-screen QR code.

### Session recap
The talk opened with three storage requirements and showed how Azure storage delivers on all three:
1. **Bringing enterprise data to agents as knowledge** — Azure Files → Azure AI Search, Foundry IQ with Blob as a first-class source.
2. **Distributing and loading models fast enough to keep GPUs busy** — Run:AI Model Streamer + Azure Container Storage distributed cache.
3. **Optimizing infrastructure utilization for better tokens-per-watt-per-dollar** — Azure Context Cache for explicit prompt caching (Foundry) + the NIXL plugin for OSS runtimes.
And **Storage Center** as the unified entry point to leverage storage for AI applications.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Blob Storage** — the durable object-storage foundation underpinning every pattern (data, KV cache, model weights, knowledge sources).
- **Azure Context Cache** — first-class Azure resource for **explicit prompt caching**; stores encrypted model KV prompt objects on durable Blob in the customer's tenant, node-independent, days/weeks/months TTL.
- **Microsoft Foundry** — Microsoft's managed AI platform; host for the three-tier prompt caching strategy and Foundry IQ.
- **Azure OpenAI** — model provider side (Saloni's team); owns implicit/extended cache + API.
- **Implicit prompt caching** — KV cache in GPU memory; fast-by-default, KB–low MB, 5–10 min–~1 hr TTL; provider-owned, zero app changes.
- **Extended prompt caching** — KV cache on GPU node local SSD; hundreds of GB, up to 24 hr TTL; cost-efficient scale tier.
- **BlobFuse** — POSIX-like mount over Blob; same experience across VMs, containers, AKS.
- **ADLFS** — Python-native, fsspec-compatible interface to Blob (Dask/Pandas/Ray).
- **AzCopy** — high-performance data movement to/from Blob.
- **PyTorch connector** — plugs Blob into dataset/dataloader/checkpoint APIs; zero-config auth via Azure Identity.
- **Azure Managed Lustre (AMLFS)** — HPC-class throughput with a POSIX client.
- **Azure Container Storage** — presents local NVMe as persistent volumes for stateful K8s workloads; home of the new distributed cache (Azure Files/Disks/Elastic SAN on roadmap).
- **Azure Container Storage distributed cache** — in-cluster AKS cache; every GPU node is cache+client (NVMe RAID, zero-copy sendfile, peer fetch with ingress acceleration).
- **NVIDIA NIXL (NVIDIA Inference Xfer Library)** — unified API for moving model weights/KV blocks across memory tiers with pluggable backends; Microsoft contributed an Azure Blob backend.
- **LMCache** — open-source KV-cache layer widely used with vLLM; Microsoft plugin offloads KV blocks to Blob.
- **Run:AI Model Streamer** — open-source large-model-weight loader for vLLM/SGLang; Azure Blob plugin gives 3–6× faster cold starts via chunked parallel reads + overlapping GPU copies.
- **NVIDIA NeMo** — NVIDIA's data movement stack; integration brings KV cache offload + high-perf transfers across Dynamo/vLLM/Ray.
- **LangChain Azure Blob loader** — faster, lower-memory document ingestion for large corpora (5–10× faster than community loader).
- **Azure AI Search** — retrieval/index service; now supports Azure Files as a data source (Logic Apps connector + native indexer) for RAG-ready indexes.
- **Foundry IQ** — Microsoft's unified, governed knowledge layer for agents; Blob is a first-class knowledge source.
- **Storage Center** — centralized hub for file/block/object storage; unified view + launchpad into storage-for-AI experiences (includes Storage Mover, lifecycle management).
- **AI runtimes/orchestrators integrated:** Ray, PyTorch, TensorFlow, **vLLM, SGLang, Triton, ONNX**, Dynamo, TensorRT-LLM.
- **KAITO (Kubernetes AI Toolchain Operator)** — AKS AI toolchain operator powered by the same storage foundation.
- **VMSS / AKS** — orchestration substrate for the storage clients.
- **GPT-5 / GPT-5.5 class models** — referenced as the models benefiting from explicit caching and default extended caching.

## 🚀 Announcements / What's New
- **Azure Context Cache (explicit prompt caching)** — in **gated/limited preview** at Build 2026, integrated with Microsoft Foundry (future: AKS + third-party frameworks).
- **Extended prompt caching in Foundry** — **Generally Available starting May 2026**; settable to 24 hr retention, or **on by default for GPT-5.5+ deployments**.
- **Implicit prompt caching in Foundry** — **already supported** (GA-level, fast-by-default).
- **Azure Blob backend contributed to NVIDIA NIXL** — enables attaching Blob storage to OSS model runtimes (vLLM, Dynamo, TensorRT-LLM, Ray) for prompt caching with zero adapter code.
- **Azure Blob plugin for LMCache** — offloads KV blocks from vLLM straight to Blob.
- **Azure Blob plugin for Run:AI Model Streamer** — 3–6× faster model cold starts (IaaS).
- **Azure Container Storage distributed cache for AKS** — in **early access** (sign up via QR); 2.5× faster model loading at fleet scale.
- **Azure Files as a data source for Azure AI Search** — via Logic Apps connector + native Azure Files indexer.
- **Foundry IQ** — unified knowledge layer with Azure Blob as a first-class knowledge source.
- **Storage Center** — **limited preview** (sign up via QR) as the unified storage hub / entry point to storage-for-AI.
- **LangChain Azure Blob loader** — high-performance document loader for AI ingestion.

## 💡 Demos
1. **KV-cache offload to Blob via NIXL + LMCache (single VM, 4 GPUs).** An inference app on **vLLM serving Llama 3.3 70B**, tensor-parallel across all four GPUs on the VM, loading the model from a Blob container, with **LMCache** alongside building the KV cache. A simple Python client posted an OpenAI-compatible request with a **~100,000-token** context.
   - *Cold start, no NIXL:* **52 seconds to first token** (GPUs doing full prefill from scratch — the familiar long-context cold start).
   - *With NIXL wired in:* config set chunk size 256, local CPU tier off, NIXL storage on, backend = Azure Blob, **async puts** (writes never block inference). On the next run, NIXL wrote KV chunks to Blob in the background — the portal showed **~1,500 chunks, ~20MB each (~30GB total)** persisted durably.
   - *Genuine cold start (vLLM restarted, GPU+CPU memory wiped):* NIXL **streamed KV chunks directly from Blob into GPU memory**, nearly saturating the **80Gb NIC** — the bottleneck moved from GPU compute to network bandwidth. **~8 seconds to first token** — **~6× faster** (52s → 8s). *Point proved:* don't pay prefill twice; stream the KV out of Blob.
2. **Fast model-weight loading via Run:AI Model Streamer (single VM, 8× H100).** Same **ND96 H100** VM (eight H100s, 80Gb NIC). Model = **GPT-OSS-120B (~60GB of weights)** pre-staged as safetensor shards in a Blob container. Started the vLLM serve command with one switch — **load format = Run:AI streamer** (the entire integration). Streamer did chunked parallel reads from Blob, CPU staging, and concurrent overlapping CPU→GPU copies. The NIC hit **~86 Gbps on the 80Gb link (fully saturated)**, and **60GB of weights loaded into eight H100s in roughly the time it took to say the sentence** — all 8 GPUs loaded, app startup complete. *Point proved:* loading is bounded only by network speed, not the default loader's slow path.
3. **AKS-scale distributed cache (Azure Container Storage).** Live comparison loading **12GB of LLM weights** on a real cluster: **direct from Blob → ~1,500 MB/s, ~8 seconds**; **with the distributed cache → ~4,000 MB/s, ~3 seconds (2.5× faster)**. When **100 pods come up together, they all read from the cache and Blob gets hit exactly once**. *Point proved:* fleet cold starts collapse from a thundering-herd Blob hit to a single warm-once read.

## 📊 Notable Stats / Quotes
- **>60%** of inference cost in most production agents is the **static unchanged portion** of the prompt.
- **Up to 90%** inference cost savings from prompt caching (reusing KV state instead of recomputing attention).
- **Implicit cache:** KB–low MB, **5–10 min** (up to ~1 hr) TTL. **Extended cache:** hundreds of GB, **up to 24 hr** TTL. **Explicit (Context Cache):** **days/weeks/months** TTL.
- Azure Context Cache: **several tens of millions of tokens per minute** throughput at global scale, **milliseconds** latency.
- **Multi-million tokens-per-minute** throughput for GPT-5 class models.
- **NIXL demo:** 100k-token cold start **52s → 8s (~6× faster)**; ~1,500 KV chunks of ~20MB each persisted to Blob; 80Gb NIC near line rate.
- **Run:AI streamer:** **3–6× faster cold starts**; ~60GB (GPT-OSS-120B) into 8× H100 with NIC at **~86 Gbps**.
- **AKS scale math:** 70B model = **~140GB**; **100 pods = ~14TB** out of Blob at once → throttling + **~10-min** cold starts.
- **Distributed cache:** **~1,500 MB/s → ~4,000 MB/s**, **8s → 3s (2.5× faster)**; Blob hit **exactly once** for 100 pods.
- **LangChain Azure Blob loader:** **5–9× faster lazy load, 7–10× faster non-lazy load** vs community loader.
- > "By the time you're a few turns in, the GPU is burning expensive cycles re-reading the same tokens it has already seen before." — Saurabh, on uncached recompute.
- > "prompt caching as a core system capability of the AI platform, not tied to where your request lands." — Saloni, on the vision for explicit caching.
- > "Both paths put KV cache on durable Azure storage that travels with the workload, not the node." — Vishnu, on Context Cache vs NIXL+LMCache.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: stand up **Azure Context Cache** (gated preview) against a GPT-5.5 Foundry deployment and measure TTFT delta on a long multi-turn agent; benchmark the **Run:AI Model Streamer + Azure Blob plugin** vs default loader on a real model; sign up (QR) for **Azure Container Storage distributed cache** early access on AKS; try the **NIXL Azure Blob backend + LMCache** with vLLM for KV offload; wire **Azure Files → Azure AI Search** (Logic Apps connector) for a lift-and-shift file share; point **Foundry IQ** at a Blob container; sign up for the **Storage Center** limited preview.
- [ ] Questions: What are the exact **pricing/billing** semantics for the cached prompt portion with Azure Context Cache? Which **regions** are in the gated preview? How does Context Cache handle **cache invalidation** when underlying context changes? What's the **GA timeline** for Context Cache and the AKS distributed cache? Any model-family restrictions beyond GPT-5 class for explicit caching?
- [ ] Relevant to: cost optimization for long-context/agentic workloads; GPU utilization & cold-start reduction on AKS/IaaS; RAG/knowledge grounding from existing Azure Files + Blob estates; any Foundry-based agent platform work.

## 🔗 Related
- [[2026 Build Session List]]
- Topics: Azure Storage · Azure Blob · Microsoft Foundry · Foundry IQ · Azure AI Search · prompt caching / KV cache · AKS · vLLM · NVIDIA NIXL · agentic inference

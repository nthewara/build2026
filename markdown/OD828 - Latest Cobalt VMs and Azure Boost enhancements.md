---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/cobalt
  - topic/azure-boost
  - topic/infrastructure
  - topic/arm
  - topic/confidential-computing
source: https://www.youtube.com/watch?v=K5j58fPl2sE
session_code: OD828
event: Microsoft Build 2026
speakers: Amar Ham (PM, VM Sizes – Azure Compute), Nico Pambukus (Principal PM, Azure Boost), [Azure Compute PM – Intel/AMD VMs], Vikas Batya (Head of Product, Azure Compute Security & Confidential Computing)
duration_min: 40
aliases:
  - Latest Cobalt VMs and Azure Boost enhancements
---

# OD828 — Latest Cobalt VMs and Azure Boost enhancements

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Amar Ham (PM, VM Sizes team – Azure Compute), Nico Pambukus (Principal PM, Azure Boost team), an Azure Compute PM (Intel/AMD general-compute VMs), and Vikas Batya (Head of Product, Azure Compute Security & Confidential Computing)  
> **Duration:** ~40 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=K5j58fPl2sE)

## 🎯 TL;DR
This is a four-part Azure infrastructure deep dive covering the silicon and platform layer underneath your VMs. **Part 1 — Cobalt 200:** Azure's next-gen Arm-based CPU (successor to Cobalt 100) delivering up to **50% higher performance** than Cobalt 100, with brand-new VM families (high-memory MP series, dense-local-storage LP series) on top of the existing general-purpose and memory-optimized lines, all running on Azure Boost and tuned for cloud-native + agentic AI workloads. **Part 2 — Azure Boost:** Microsoft's hardware/software offload system (now GA with the Intel V7 VMs) that moves virtualization off the host onto dedicated hardware; the headline feature is **guest RDMA**, which bypasses the TCP/IP stack for direct memory-to-memory transfers — demoed live on distributed AI inference for up to **2.2× throughput and 3× faster time-to-first-token**. **Part 3 — Intel & AMD V7 VMs:** new Granite Rapids (Intel) and 5th-gen EPYC Turin (AMD) general-compute SKUs with big gen-over-gen gains. **Part 4 — Confidential computing & security:** AMD SEV-SNP / Intel TDX confidential VMs, confidential VM live migration, and GA of Azure Integrated HSM. The throughline: Azure's custom silicon and offload platform let developers do more work per core, at lower cost, with stronger isolation — using the exact same Azure control plane and tooling they already know.

## 🔑 Key Takeaways
- **Cobalt 200 is Azure's leading-performance Arm CPU**, delivering up to **50% higher performance over Cobalt 100** and becoming Azure's top-performing offering in market.
- **Cobalt 100 (GA 2024)** was Microsoft's first cloud-designed CPU: up to **2× the performance** of the prior Arm generation, up to **20% lower cost** than comparable Azure VMs, and up to **45% better real-world performance** for customers — letting them use **~35% fewer cores/VMs** for the same work.
- **Microsoft's own first-party services run on Cobalt 100** — Teams, Cosmos DB, Azure SQL, and Defender are standardized on it ("we run our own business on it before we ever ask a customer to").
- **Cobalt's sweet spot = cloud-native + agentic AI**: scale-out/web-tier services, microservices, containers, plus agent runtimes, sandboxes, vector search, retrieval pipelines, and model orchestration — and Windows 11 on Arm dev targets.
- **Modernizing the enterprise estate is "recompile and go"** for Java, Python, .NET, and Go; open-source databases, in-memory caches, and analytics engines port cleanly, aided by a deep ARM Holdings partnership (migration guides, dependency analyzers, runtime support).
- **Cobalt 200 adds two entirely new VM families** shaped by customer requests: **MP series** (high-memory, 16 GB/vCPU, ~1.3 TB) and **LP series** (dense local storage, up to ~23 TB NVMe local) — on top of refreshed general-purpose (DPLS/DPS) and memory-optimized (EPS) lines.
- **For agentic AI, the metric that matters is "time to interact"** — how fast you spin up an agent sandbox, how quickly it becomes responsive, and how many you can run concurrently per machine. Cobalt 200 improves all three (faster spawn, higher density, lower cost per agent).
- **Running an Arm VM on Azure is identical to running an x86 VM** — same control plane, portal, CLI, marketplace, scale sets, spot, monitor, backup, AKS. No new operational model to learn.
- **Azure Boost offloads hypervisor/host-OS work onto dedicated hardware**, improving isolation, servicing (background maintenance with no customer-visible impact), networking, and storage — now GA with the Intel V7 VMs.
- **Latest Azure Boost gen hits 400 Gbps networking, up to 20 GB/s remote storage throughput, and 1M remote-storage IOPS**, plus >25% greater confidential-device saturation vs Build 2025.
- **Guest RDMA bypasses the TCP/IP stack** — offloading packetization, reliability, flow/congestion control to the NIC — for dramatically lower latency/jitter and CPU overhead; up to **200 Gbps on a single connection**, and it works *inside* normal Azure virtual networks via the Microsoft Azure Network Adapter (RDMA network virtualization).
- **Guest RDMA preview starts June 2026** (limited preview via sign-up form).
- **Intel V7 VMs (DSV7/ESV7)** run on 6th-gen Xeon 6 Granite Rapids: up to 372 vCPUs, 2.88 TB RAM, 4.2 GHz turbo, and (via Boost) 400 Gbps networking and ~9.6M local-NVMe IOPS.
- **AMD V7 VMs (DA/EA/FASv7)** run on 5th-gen EPYC Turin: up to **35% CPU gains** gen-over-gen (and up to 130% on web apps), 160 vCPUs, 1.25 TB RAM, already live in 11 regions.
- **Confidential computing protects data *in use*** via TEEs — AMD SEV-SNP and Intel TDX V6 confidential VMs — and Microsoft moved Entra ID security-critical workloads entirely onto confidential compute.
- **Azure Integrated HSM (AIHSM) is GA** — a node-local, hardware-backed key store (FIPS 140-3 Level 3) so keys never sit in VM memory in cleartext, giving both stronger security *and* lower latency than remote HSM calls.

## 📚 Detailed Notes

### Session structure & speakers
This "OnDemand" (OD) session is a stitched set of **four short talks**, each from a different Azure Compute product owner, all centered on the infrastructure/silicon layer beneath Azure VMs:
1. **Amar Ham** — PM on the VM Sizes team in Azure Compute (owns the optimized + Cobalt VM portfolio): **Cobalt 100 momentum and the Cobalt 200 launch**.
2. **Nico Pambukus** — Principal PM on the Azure Boost team: **Azure Boost overview + guest RDMA deep dive + live distributed-inference demo**.
3. **An Azure Compute PM** (name not stated in the captions): **new Intel & AMD general-compute V7 VMs**.
4. **Vikas Batya** — Head of Product for Azure Compute Security & Confidential Computing: **confidential VMs, confidential live migration, and Azure Integrated HSM**.

The unifying theme: Microsoft's custom silicon (Cobalt) and offload platform (Azure Boost) plus partner silicon (Intel/AMD) all combine to raise per-core performance, lower cost, and strengthen isolation — while keeping the developer experience identical to the Azure they already use.

### Part 1 — Cobalt: what it is and why it exists
**Cobalt is Azure's own silicon, purpose-built for the cloud**, and the team frames its mission simply: get the customer "the right VM for the right workload at the right price." Cobalt is reshaping the **price/performance** conversation because Microsoft designs the chip specifically for cloud-native scale-out patterns rather than buying a general-purpose part.

**Cobalt 100 (GA in 2024)** was the first-ever Microsoft-designed CPU built for the cloud, setting a new bar for **Arm64 price/performance**. The measurable results:
- Up to **2× the [Arm] performance** of the prior generation.
- Up to **20% lower cost** than comparable Azure VMs.
- Real production workloads at scale see up to **45% better performance** on real-world workloads.
- Because of that uplift, customers need roughly **35% fewer cores and VMs** for the same work → lower bills, smaller fleets, smaller carbon footprint.

Demand "exceeded what we planned for." Every major modern-cloud workload segment is represented among adopters, and customers migrating production workloads consistently report meaningful price/performance gains — "the kind of gains that change the map on their roadmap."

**Microsoft eats its own dog food:** first-party services among the largest-scale workloads on the planet — **Teams, Cosmos DB, Azure SQL, and Defender** — are now standardized on Cobalt 100. The point: Microsoft proves it on its own business before asking customers to adopt.

### Part 1 — Where Cobalt VMs shine (workload fit)
**Two big buckets:**

**A) Digital / cloud-native (the heart of Cobalt deployments today):**
- Scale-out and web-tier services, microservices, containers — "the engine room of modern cloud applications."
- Developers building **Windows 11 on Arm** apps use Cobalt as a native cloud target that mirrors the client experience their users run on, keeping the dev→deploy loop tight.
- **Agentic AI lives squarely here**: agent runtimes, sandboxes, vector search, retrieval pipelines, model orchestration — all cloud-native by nature. Cobalt 200 specifically targets these with the per-core performance, density, and cost efficiency they demand. Key line: *"The same Cobalt VMs you build cloud-native services on today are the ones your agentic systems will run on tomorrow."*

**B) Modernizing the enterprise estate:**
- Customers with established workloads — most easily portable to Arm — move them onto Cobalt for a step change in performance and efficiency.
- If your workload is built on **Java, Python, .NET, or Go, it ports cleanly.** Open-source databases, in-memory caches, data processing, and analytics engines "run beautifully."
- For most teams this is a **recompile and go** — "the heavy lift you may be imagining is rarely there."
- Microsoft partnered deeply with **ARM Holdings** on migration tooling: via Azure's own porting frameworks plus the ARM partnership, you get **migration guides, dependency analyzers, and runtime support across the major languages — available today.**

### Part 1 — Cobalt 200: the headline
Cobalt 200 is the next step built directly on Cobalt 100 learnings and customer feedback. The headline: **up to 50% higher performance over Cobalt 100**, making it **Azure's leading performance offering in the market.** It brings:
- **A new architecture and refined design** — a real step change in performance, not just a clock bump.
- **Entirely new VM families** engineered for a wide variety of workloads (detailed below).
- Purpose-built for the workloads defining this era: **cloud-native services and agentic AI** — containerized microservices, distributed data pipelines, vector search, retrieval/model orchestration, and the agent runtimes on top. These workloads are **concurrent, memory-aware, IO-sensitive, and must be cheap to run at scale** — exactly Cobalt 200's design target.
- Portfolio expansion: from **DP / DPL / EP** families on Cobalt 100, Cobalt 200 adds **high-memory-optimized** and **dense-local-storage-optimized** VMs.
- **Cobalt 200 runs on Azure Boost** and is Azure's **most power-efficient compute offering yet** — tying Part 1 directly to Part 2's platform.

### Part 1 — Cobalt 200 per-core performance (the proof slide)
The presenter calls this "the slide that matters most to developers." Cobalt 200's **per-core performance is measured relative to Cobalt 100 across three lenses**, and the story is consistent across all of them:
1. **Industry-standard benchmarks** (left) — vendor-neutral, repeatable measurements engineering teams already trust. Cobalt 200 shows a meaningful generational leap.
2. **Microsoft's own benchmarks** (middle) — broader, more diverse workload coverage that mirrors real production. Same story: a clear, consistent step up.
3. **Microsoft's own products** (right) — first-party services at hyperscale on real customer traffic every day. "The strongest signal of all" — when those workloads see this uplift, it's not synthetic, it's real.

The guidance: **focus on the shape of the distribution, not any single bar.** Workloads differ and yours will land somewhere along the distribution, but *every* bar to the right of Cobalt 100 tells the same story — **Cobalt 200 raises the floor on per-core performance.** For developers: more work per core → fewer cores to provision → lower bills → real headroom to scale.

### Part 1 — Cobalt 200 for agentic AI (three takeaways)
This is where Cobalt 200 matters most for the next wave. Three points:
1. **Why it matters — a new performance mental model.** The industry is converging on a different way to think about agentic performance. It's **no longer just throughput on a single request.** It's: how fast can you **spin up an agent sandbox**, how quickly does that agent **become responsive**, and **how many can you run concurrently** on one machine? That's the metric translating per-core performance into real product/customer value, and it's the lens the benchmarks are built around.
2. **What they're seeing on Cobalt 200.** Internal agentic benchmarks for **"time to interact"** — from requesting an agent sandbox to it doing useful work — are **meaningfully faster** than on Cobalt 100. **Spawn rates are up.** The latency story is consistent with the per-core performance story; the platform is faster end-to-end and the developer experience reflects it.
3. **Density.** Because Cobalt 200 does more useful work per core, you can pack **more agent sandboxes per VM and more agents per fleet** → lower cost per agent, higher concurrency for end users, and real headroom as agentic workloads scale.

### Part 1 — Cobalt 200 VM lineup & specs
**Two foundational families (refreshed end-to-end on the new generation):**

*General purpose:*
- **DPLS / DLDDS series** — **2 GB memory/vCPU**, scaling **1→128 vCPUs**, up to **256 GB** memory. Purpose-built for **media encoding, gaming servers, microservices, small databases.**
- **DPS / DPDS series** — **4 GB memory/vCPU**, up to **128 vCPUs**, up to **512 GB** memory. The natural home for **application servers, web servers, small-to-medium databases.**

*Memory optimized:*
- **EPS / EPDS series** — **8 GB memory/vCPU**, up to **128 vCPUs**, up to **1 TB** memory. For **larger in-memory databases, caches, and analytics.**

*Platform leveled up across all of the above:*
- Up to **7 TB NVMe local storage**
- Up to **85 Gbps network bandwidth**
- Up to **70 Gbps remote storage throughput**
- Can attach **Standard, Premium SSD v2, and Ultra disks** (regional availability dependent)

Takeaway: the Cobalt VM families you already deploy keep the same shape, ergonomics, and workload fit — now with a meaningful performance step-up from Cobalt 200 underneath.

**Two entirely new VM types (built in direct response to customer requests — "not refreshes"):**
- **MP series (high memory)** — for workloads needing lots of memory per core: large in-memory databases, caches, big analytics, relational databases, **ERP**. Ratio set at **16 GB memory/vCPU**, scaling up to **84 vCPUs** and roughly **1.3 TB** memory in a single VM. "Customers have been asking for this profile for years" — Cobalt 200 makes it deliverable at family-level price/performance.
- **LP series (dense local storage)** — for **data prep/processing, storage caching, relational + NoSQL databases, big-data analytics, search/index engines.** **8 GB memory/vCPU**, up to **128 vCPUs**, **1 TB** memory, and up to **~23 TB NVMe local storage sitting right next to compute.** For storage-hungry, latency-sensitive workloads "where the math fundamentally changes."

Both new series are the clearest examples of Cobalt 200 being "shaped by customer feedback" — each fills a stated gap, enabled by the new silicon + new platform working together.

### Part 1 — Guest OS, feature parity, operations, regions
- **Guest OS:** broad support — **all major Linux families plus Windows 11 client** (for developer scenarios). "Whatever your team runs is almost certainly on the list." Advice: use the **latest patches, kernels, and libraries** to extract maximum Cobalt performance.
- **Feature parity:** Cobalt 200 supports the **full set of Azure capabilities** across management, security, core platform, and developer tooling, with support for new capabilities continuing to grow.
- **Operations — no new model to learn:** Arm-based VMs are built into Azure exactly like x86 VMs. Same **Azure control plane, tools, and workflows** — ARM (Resource Manager), portal, CLI, marketplace, scale sets, spot, monitor, backup, AKS — "it all just works." *If you can run a VM on Azure today, you already know how to run an Arm VM.*
- **Regions:** Cobalt 200 launches in **West US 3, East US 2, Central US, and Sweden Central**, expanding from there. The **Product Availability by Region** page is the source of truth — bookmark it.
- **Where to go next:** Cobalt 100 customer stories on the Azure blog; Cobalt 200 announcement blog (deeper technical narrative); full ARM migration overview via ARM learning paths; the **ARM software ecosystem dashboard** to confirm your stack's libraries/runtimes; and Azure Cobalt VM docs on Microsoft Learn.

### Part 2 — Azure Boost: what it is
**Azure Boost is a Microsoft-designed system that offloads virtualization tasks** traditionally handled by the **hypervisor and host OS** onto **specialized hardware and software.** It recently went **GA alongside the first VMs using it — the Intel-based V7 VMs.** What offloading buys you (multi-dimensional improvements):
- **Performance** optimization across varied workloads.
- **Increased host isolation** from customer VMs.
- **Improved servicing** — Microsoft can maintain the platform in the background with **no customer-visible impact.**
- **Better networking and storage access** (the basis for guest RDMA).
- **Bare-metal functionality** enablement.

**Latest-gen Boost numbers (vs Build 2025):** dramatic increases in storage throughput and IOPS, **confidential-device support saturation up >25%**, and **total networking bandwidth of 400 Gbps** — all advancing confidentiality across the fleet. Exposed via the **optimized V7 VM SKUs**:
- **3× networking bandwidth increase**
- **400,000 connections/second** across **2 million concurrent connections**
- Remote storage: up to **20 GB/s throughput** and **1 million IOPS** (capabilities future VMs will support)

### Part 2 — Guest RDMA deep dive
**The problem with TCP:** every data transfer is CPU-intensive — each packet traverses the full networking stack, paying protocol overhead, context switches, and per-layer processing delays. Result: TCP consumes significant CPU and adds hard-to-avoid latency.

**How guest RDMA changes it:** RDMA (Remote Direct Memory Access) **allows direct access to memory, bypassing the OS layers** and removing the intermediate networking-stack steps. Instead of moving through TCP/IP layers, data transfers **directly between application memory and the network interface** → significantly lower latency and dramatically reduced CPU overhead.

**Why it matters to network app developers:** RDMA offers an alternative, far-less-CPU-intensive path. Work you'd normally do in software — **message packetization/reassembly, reliability, flow control, congestion control** — is **offloaded to the NIC.** Applications bypass traditional networking overhead entirely, cutting both **latency and jitter** because the heavy lifting moves from software into hardware. Critical for workloads needing **high bandwidth + very consistent latency**: large-scale **AI training, distributed inference, and HPC** — "scenarios where every microsecond counts." RDMA can push **up to 200 Gbps on a single connection** while holding tight, predictable latency.

**Azure's twist — RDMA network virtualization:** RDMA traffic now works **seamlessly inside the cloud-native virtual-network constructs** you already use. You don't have to choose between RDMA performance and cloud-native VNet features — **you get both.** It's available **today on Azure Boost instances** via the **Microsoft Azure Network Adapter**, which combines high performance with full virtualization support in one place.

### Part 2 — Distributed inference (the demo workload explained)
The demo compares **TCP vs RDMA** transport for **distributed AI inference** by directly comparing resource utilization across the two paths. Setup:
- The inference pipeline is **disaggregated into two stages — prefill and decode** — so they run on separate resources and scale independently.
- Workload runs **across two VMs on the same Azure ND GB200 v6 cluster**, once over TCP and once over RDMA.
- Model: **Llama 3.1 70B Instruct**, driven by **vLLM benchmarking tools** (specifically `vllm bench serve`) with **synthetic prompt generation** for consistent, repeatable traffic.
- **VM1 (prefill):** processes the user's input prompts, building up context in memory for token generation — creating the **KV cache.** Focused on prompt processing.
- **VM2 (decoder):** the **memory-intensive** VM — takes the prefill's context and **generates tokens** (the actual chat response). The GPU drives the inferencing engine; results stream back to the client in real time.
- In this disaggregated architecture, **transport choice (TCP vs RDMA) really starts to matter.**

**Three key metrics tracked:**
1. **Throughput** — tokens generated per second.
2. **TTFT (Time To First Token)** — how quickly users see the very first response.
3. **TPOT (Time Per Output Token)** — how efficiently tokens are generated after the first one lands.

### Part 3 — New Intel & AMD general-compute VMs
The third speaker covers recently announced **Intel and AMD general-compute VMs** (GA and preview).

**Intel DSV7 / ESV7 (GA):** the VMs bringing latest-gen **Azure Boost** benefits to customers, based on **Intel 6th-gen Xeon 6 (Granite Rapids).**
- Up to **15% CPU improvement** over prior gen; very large configs up to **372 vCPUs** and **2.88 TB** memory; turbo up to **4.2 GHz.**
- Via Boost: up to **400 Gbps networking**, **800K IOPS** and **20 GB/s** throughput to Premium v2 / Ultra remote storage, and up to **9.6M IOPS** + **53 GB/s** to local NVMe temp.
- Gen-over-gen workload gains: CPU up to **13%**, in-memory cache up to **18%**, cryptography up to **20%**, AI pre-processing up to **18%**, video encoding up to **24%.**

**Intel network-optimized series:** purpose-built for high-performance **NVA (network virtual appliance)** workloads — up to **4 vNICs** at small (2 vCPU) sizes scaling to **15 vNICs** on larger ones; up to **400K connections/sec**; top-end **128 vCPU** sizes enable up to **200 Gbps** bandwidth. Ideal for **firewalls, gateways, packet-processing.**

**Intel EBSV6 series:** for remote-storage-intensive workloads (databases, analytics), on the **Intel Emerald Rapids** CPU. Key value is Azure Boost integration → remote storage throughput/IOPS far above general purpose: up to **14 GB/s** and **800,000 IOPS.**

**AMD DA / EA / FASv7 (general purpose / memory optimized / compute optimized):** options with and without local SSD, plus new **constrained-core sizes** for cost control. Powered by **5th-gen AMD EPYC Turin:** up to **35% CPU improvement** gen-over-gen, up to **160 vCPUs**, **1.25 TB** memory, boost up to **4.5 GHz**, already in **11 regions** (broader expansion in 2026). Gen-over-gen (V6→V7) benchmark gains vary by workload: CPU up to **35%**, Java up to **25%**, in-memory caching up to **65%**, crypto up to **80%**, **web applications up to 130%.**

**AMD LSV5 (local-storage-intensive):** for caching layers and search benefiting from local NVMe; 5th-gen EPYC Turin, up to **35% CPU gains**, increased local disk capacity/IOPS, consistent disk-to-vcore ratios with larger sizes for big-data processing. **LAOSV5** is the latest AMD **dense** local-storage VM with **3× the local-storage ratio of LSV5**, and big increases in max local disk capacity/IOPS vs the prior LAOSV4 gen.

### Part 4 — Compute security & confidential computing
The fourth speaker (Vikas Batya) frames **secure hardware system architecture as defense in depth** — not one layer, but security technologies at *every* layer, anchored in **hardware as the foundation.** Azure's security architecture rests on: **confidential computing, a silicon root of trust, Azure Boost (secure host hardware management), and Azure Integrated HSM (to meet FIPS 140-3 Level 3).**

**Two isolation goals:**
- **Tenants isolated from each other** — via trusted launch, disk encryption, key management offerings, verified boot chains, AKS controls, and just-in-time memory access.
- **The cloud provider (Azure) isolated from tenant workloads** — led by Azure Boost investments, plus Azure Integrated HSM, confidential computing, and the **Caliptra root of trust.**

**Confidential computing — the core idea:** industry has long had encryption *at rest* and *in transit*, but protecting data **in use (in memory)** wasn't solved at scale until now. Confidential computing protects data in memory while in use from outside a trusted boundary called the **TEE (Trusted Execution Environment)**, which assures **data + code integrity and data confidentiality.** Two takeaways: (1) it protects data in use from malicious actors/code; (2) data and code are protected across their **entire lifecycle** — from creation to destruction — with **a confidential key the customer owns.**

**AMD SEV-SNP V6 confidential VMs:** hardware-enforced memory encryption protecting data in use from the **host, hypervisor, and other tenants.** Strong isolation keeps both **memory and CPU state private** even from privileged infrastructure layers. Built-in **attestation** (via Microsoft Azure Attestation service or in-guest attestation) lets customers **verify VM integrity before releasing secrets.** Supports enterprise-scale workloads (high core counts/memory), integrates with **Kubernetes cloud-native tooling** for secure containerized workloads, and improved performance reduces the old security-vs-efficiency tradeoff. Notably, Microsoft moved **security-critical workloads such as Entra ID** to run **entirely on confidential computing.**

**Intel TDX V6 confidential VMs:** like SEV-SNP, extends confidential computing to a broader workload set with strong **VM-level isolation using TDs (Trusted Domains).** **OpenCL** [as spoken — likely the open paraverifier/firmware-visibility component] supports increased transparency/trust into the firmware stack. High-performance configs (large vCPU/memory) suit data-intensive enterprise workloads; new capabilities like **accelerated storage and infrastructure improvements** close the performance gaps (the "asterisks") of confidential VMs. Enables **lift-and-shift of sensitive workloads** into Azure without exposing data to the cloud operator.

**Confidential VM live migration:** **coming soon to Intel TDX.** Provides **near-zero downtime** for maintenance/upgrades — eliminating outages and operational disruption for mission-critical workloads, and improving reliability by transparently moving workloads away from failures and rebalancing capacity **without customer intervention.**

**Azure Integrated HSM (AIHSM) — GA:** Microsoft's first-party security ASIC acting as a **secure, hardware-backed, node-local key vault.** Customers offload keys typically stored in **Azure Key Vault, Azure Managed HSM, or an external key manager.** Keys are **never exposed in the clear** and remain inside the **AIHSM boundary while in use — with no performance penalty.** It carries **FIPS 140-3 Level 3 certification.** Mechanically: crypto operations are offloaded to a **local PCIe SR-IOV device on the node**; the VM uses a **local interface** to access keys securely, so keys never sit in VM memory as cleartext. This **changes the threat model** — even **crash dumps or memory inspection** won't expose sensitive material (it never leaves the HSM boundary) — while the local interface delivers **lower latency and higher throughput** than repeated remote HSM calls, making it viable for high-scale production without trading off security vs performance.

### Closing thread
The session's wrap-up: building **verifiable trust rooted in hardware** lets organizations develop new applications and migrate existing sensitive ones, keeping protected data safe at all times. Across all four parts, the consistent message is that Azure's silicon (Cobalt), partner silicon (Intel/AMD), offload platform (Azure Boost), and security stack (confidential computing + AIHSM) work together to deliver **more performance per core, lower cost, and stronger isolation — without changing how developers build and operate on Azure.**

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Cobalt 100** — Microsoft's first cloud-designed Arm64 CPU (GA 2024); foundation for Microsoft first-party services.
- **Azure Cobalt 200** — next-gen Arm CPU; up to 50% faster than Cobalt 100; Azure's leading-performance offering; runs on Azure Boost.
- **Cobalt 200 VM families** — DPLS/DLDDS & DPS/DPDS (general purpose), EPS/EPDS (memory optimized), **MP series** (high memory), **LP series** (dense local storage).
- **Azure Boost** — Microsoft's hardware/software offload system for virtualization tasks; GA with Intel V7 VMs; powers networking/storage/isolation gains.
- **Guest RDMA** — direct memory-to-memory transfers bypassing TCP/IP and the CPU/OS; up to 200 Gbps/connection.
- **Microsoft Azure Network Adapter** — delivers RDMA network virtualization (RDMA inside normal VNets) on Azure Boost instances.
- **Azure ND GB200 v6** — GPU cluster used for the distributed-inference demo.
- **vLLM / `vllm bench serve`** — LLM serving + benchmarking tooling used in the demo.
- **Llama 3.1 70B Instruct** — model used in the inference demo.
- **Intel DSV7 / ESV7 (V7)** — Granite Rapids (Xeon 6) general-compute VMs; GA; bring Azure Boost benefits.
- **Intel network-optimized series** — high-vNIC NVA VMs for firewalls/gateways/packet processing.
- **Intel EBSV6** — Emerald Rapids remote-storage-intensive VMs.
- **AMD DA / EA / FASv7** — 5th-gen EPYC Turin general/memory/compute-optimized VMs.
- **AMD LSV5 / LAOSV5** — EPYC Turin local-storage-intensive and dense-local-storage VMs.
- **Confidential computing / TEE** — protects data *in use* in memory.
- **AMD SEV-SNP** — hardware memory encryption for V6 confidential VMs; runs Entra ID.
- **Intel TDX** — Trusted Domains for V6 confidential VMs; live migration coming.
- **Microsoft Azure Attestation** — verifies confidential VM integrity before secret release.
- **Caliptra** — silicon root of trust for provider-from-tenant isolation.
- **Azure Integrated HSM (AIHSM)** — GA; node-local hardware key store, FIPS 140-3 Level 3, PCIe SR-IOV.
- **ARM Holdings partnership / ARM software ecosystem dashboard** — migration tooling, dependency analyzers, runtime/library support.
- **AKS, scale sets, spot, Azure Monitor, Backup, ARM/portal/CLI/marketplace** — standard Azure control-plane surfaces that work identically for Arm VMs.

## 🚀 Announcements / What's New
- **Azure Cobalt 200** — new Arm CPU generation announced: up to **50% higher performance** than Cobalt 100, Azure's leading-performance offering. Launch regions: **West US 3, East US 2, Central US, Sweden Central** (expanding).
- **New Cobalt 200 VM families — MP series (high memory, 16 GB/vCPU, ~1.3 TB) and LP series (dense local storage, ~23 TB NVMe local)** — net-new SKUs built from customer feedback.
- **Azure Boost (latest generation) is GA** — shipping with the first VMs to use it, the **Intel V7 VMs**; brings 400 Gbps networking, 20 GB/s remote storage, 1M IOPS.
- **Guest RDMA limited preview kicks off June 2026** — sign-up form to join; starting limited to harden the experience before broad rollout.
- **Intel DSV7 / ESV7 (V7) VMs — GA** (Granite Rapids / Xeon 6).
- **AMD DA / EA / FASv7 VMs** — announced (GA + preview mix), 5th-gen EPYC Turin, already in 11 regions, broader expansion in 2026.
- **AMD LSV5 and LAOSV5** local-storage VMs — latest AMD local/dense-local storage offerings.
- **Confidential VM live migration — coming soon to Intel TDX** (near-zero downtime for confidential VMs).
- **Azure Integrated HSM (AIHSM) — generally available** (node-local, FIPS 140-3 Level 3 hardware key store).
- Entra ID and other security-critical Microsoft workloads **now run entirely on confidential computing** (AMD SEV-SNP).

## 💡 Demos
- **Guest RDMA — distributed AI inference (TCP vs RDMA), live.** A disaggregated **prefill + decode** inference pipeline runs across two VMs on the same **Azure ND GB200 v6** cluster, serving **Llama 3.1 70B Instruct** via **vLLM (`vllm bench serve`)** with synthetic prompts. Demo screens: top-left = prefill VM, bottom-left = decoder VM; top-right = live benchmark results; bottom-right = **RDMA stats that light up/tick in real time** when traffic flows over the RDMA fabric (visual confirmation it's not TCP). The demo runs the **same workload twice — run 1 over TCP, run 2 over RDMA** — an apples-to-apples comparison (same model, prompts, VMs; only transport changes). **Result (RDMA vs TCP): up to 2.2× higher throughput, ~3× reduction in time-to-first-token, and ~20–25% faster token generation after the first token.** Proves RDMA delivers a meaningful step-change for distributed AI inference on Azure.
- **Confidential VM live migration, live.** Two servers shown — **left = source, right = destination.** A CVM on the source runs a basic script printing "hello" + the time. The demo shows **attestation and key exchange** occurring, then live migration progressing; key exchange completes, the **handoff occurs**, and the CVM moves from source to destination. The time-printing script **continues on the destination with just a short blackout**, demonstrating near-zero-downtime migration of a *confidential* VM.

## 📊 Notable Stats / Quotes
- **Cobalt 100:** up to **2×** prior-gen Arm performance; up to **20% lower cost** vs comparable Azure VMs; up to **45%** better real-world performance → **~35% fewer cores/VMs.**
- **Cobalt 200:** up to **50% higher performance** than Cobalt 100; **16 GB/vCPU** (MP) and **~23 TB** local NVMe (LP); platform up to **7 TB** local NVMe, **85 Gbps** network, **70 Gbps** remote storage.
- **Azure Boost (latest):** **400 Gbps** networking, **3×** bandwidth increase, **400K connections/sec** across **2M concurrent connections**, **20 GB/s** + **1M IOPS** remote storage, **>25%** greater confidential-device saturation vs Build 2025.
- **Guest RDMA:** up to **200 Gbps** on a single connection; demo gains **2.2× throughput / 3× TTFT reduction / 20–25% faster TPOT.**
- **Intel V7 (Granite Rapids):** up to **372 vCPUs**, **2.88 TB** RAM, **4.2 GHz**, **400 Gbps**, **9.6M** local-NVMe IOPS, **53 GB/s** local throughput; **+13%** CPU, **+18%** cache, **+20%** crypto, **+24%** video encode gen-over-gen.
- **AMD V7 (EPYC Turin):** up to **160 vCPUs**, **1.25 TB** RAM, **4.5 GHz**, **11 regions**; gen-over-gen up to **+35%** CPU, **+25%** Java, **+65%** caching, **+80%** crypto, **+130%** web apps.
- **Security:** **FIPS 140-3 Level 3** for AIHSM; **Entra ID** moved entirely to confidential computing.
- *"The same Cobalt VMs you build cloud-native services on today are the ones your agentic systems will run on tomorrow."* — Amar Ham
- *"We run our own business on it before we ever ask a customer to."* — on first-party Cobalt 100 adoption.
- *"If you know how to run a VM on Azure today, you already know how to run an Arm VM on Azure."*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Benchmark a current Cobalt 100 (DPS/EPS) workload, then re-test on Cobalt 200 once available in **East US 2** / **Sweden Central** to validate the per-core uplift on *your* workload shape.
  - Pilot an **Arm recompile** of a Java/.NET/Go/Python service using the **ARM software ecosystem dashboard** + dependency analyzers to confirm library coverage before committing.
  - Evaluate the **MP series** for an in-memory DB / ERP workload and **LP series** for a storage-hungry analytics/search workload.
  - Sign up for the **guest RDMA limited preview (June 2026)** if running distributed inference / AI training / HPC.
  - Prototype **disaggregated prefill/decode inference** with vLLM to measure TTFT/TPOT/throughput deltas in our environment.
  - Pilot **Azure Integrated HSM** to pull keys out of VM memory for a high-throughput crypto workload.
- [ ] Questions:
  - Cobalt 200 pricing vs Cobalt 100 — does the ~50% perf uplift hold the same price/perf advantage (or better)?
  - Exact GA timing for Cobalt 200 vs the four launch regions; when does **australiaeast** (our default) get it?
  - Which specific Azure Boost VM SKUs will eventually expose the 20 GB/s + 1M IOPS remote-storage ceilings?
  - Confidential VM live migration GA date for Intel TDX; is AMD SEV-SNP live migration also planned?
  - Does guest RDMA require app changes, or is it transparent via the Microsoft Azure Network Adapter for existing RDMA-aware apps?
- [ ] Relevant to:
  - Azure migration/modernization planning (Arm recompile candidates: Java/.NET/Go/Python services, OSS DBs, caches, analytics).
  - Agentic AI infra (sandbox spin-up density/cost), distributed inference cost optimization.
  - Security/compliance workloads needing data-in-use protection or FIPS 140-3 L3 key handling.

## 🔗 Related
- [[DEMSP381 - Scale agentic AI on Azure with Arm Cobalt VMs]] — companion demo session: running agentic AI on Arm Cobalt VMs.
- [[BRK226 - Inside Azure innovations with Mark Russinovich]] — broader Azure infrastructure/silicon innovation context.
- [[DEM311 - Scale cloud-native workloads with Azure Linux]] — cloud-native scale-out OS that pairs with Cobalt's target workloads.
- [[DEM314 - Majorana 2 Topological Quantum Computing]] — another Microsoft custom-silicon / infrastructure frontier.
- [[DEM364 - Cloud-native PostgreSQL in Azure HorizonDB]] — OSS database modernization, a prime Cobalt-port candidate.
- [[OD822 - Smarter PostgreSQL migrations to power modern intelligent apps]] — database migration motion complementary to Arm modernization.
- [[BRK247 - Scott and Mark learn how agents reshape software engineering]] — agentic-AI direction that Cobalt 200 is engineered to host.
- Source list: [[2026 Build Session List]]

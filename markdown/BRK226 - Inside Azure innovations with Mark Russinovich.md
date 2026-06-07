---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/azure
  - topic/infrastructure
  - topic/security
  - topic/ai
  - topic/networking
  - topic/confidential-computing
source: https://www.youtube.com/watch?v=p2lJFg9bSjM
session_code: BRK226
event: Microsoft Build 2026
speakers: Mark Russinovich
duration_min: 45
aliases:
  - Inside Azure innovations with Mark Russinovich
---

# BRK226 — Inside Azure innovations with Mark Russinovich

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Mark Russinovich (CTO & Deputy CISO, Azure); live guest appearance by "Katar/Qatar" — a researcher from Microsoft Research Cambridge (Project Mosaic demo)  
> **Duration:** ~45 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=p2lJFg9bSjM)

## 🎯 TL;DR
Russinovich's signature under-the-hood tour of Azure infrastructure, spanning data centers, networking, serverless, AI inference, and security — with the unifying theme of **co-designing AI data centers, core infra, and software together**. Highlights: the latest **Azure Boost** offload card (now 400 Gb networking, multi‑million IOPS) and bare-metal instances powering OpenAI in the Fairwater data centers; a new resilient training-network protocol called **MRC (Multipath Reliable Connection)** that packet-sprays across "planes" to survive switch failures with zero bandwidth loss; **VM-to-VM RDMA** over Azure Boost roughly doubling inference throughput. On the serverless side, **Azure Container Instances** is being re-platformed onto **direct (L1) virtualization**, gaining **container live migration** and the ability to host AI models (Manifold) with isolated CPU/GPU pods. New AI-inference features include **Azure Context Cache** (a pooled, storage-backed KV cache) and ultra-fast **container sandboxes** (10,000 launched in ~2s avg via memory snapshotting). Security closed the show with the **first-ever public confidential VM live migration**, the **Azure Integrated HSM** (an HSM in every server, FIPS 140‑3 L3) giving ~30× faster signing, and speculative MSR work — **Project Mosaic**, micro‑LED optical interconnect — demoed live from Cambridge.

## 🔑 Key Takeaways
- **Theme: innovation powering AI** via co-design of AI data centers + core infrastructure + the software on top. Caveat up front: some items shown are pre-release / may never ship as presented.
- **Fairwater** AI data centers (Wisconsin + new Atlanta site) use liquid cooling and enormous network cabling — *"enough cabling to wrap the Earth four times"* in one site; continuously under construction.
- **Azure Boost** offloads storage + networking data planes (and the host "agents") onto a dedicated card with **Arm cores + DPU + FPGA** SoC, leaving the workload in control of the server. Now in **>30% of the fleet**; goal is every server.
- Azure Boost gen-over-gen gains (vs last Build): **20 Gb/s remote storage (≈1.4× up), 1M remote-storage IOPS, 36 Gb/s + 6.6M IOPS local NVMe, 400 Gb networking (up from 200), 400k connections/sec**. Dual 200 Gb ports → two top-of-rack switches → sub-second servicing with sub-second workload impact.
- **Bare-metal instances** (management offloaded to Azure Boost) launched in limited access for **OpenAI** on Fairwater (GPU servers are bare metal); a **general-purpose offering is coming** soon. Demoed `ND144V6` with no virtualization running and 8 RDMA-capable Mellanox NICs on the back-end GPU network.
- Fairwater switched from **InfiniBand → Ethernet**, and from RoCE to a new protocol **MRC (Multipath Reliable Connection)**, co-developed with OpenAI + a growing partner consortium. MRC **sprays packets across independent "planes"** so a dropped link/switch rebalances automatically — critical when synchronizing **100,000 GPUs** (a failure otherwise forces a checkpoint restart). Now described as an **industry standard for large network topologies**.
- **VM-to-VM RDMA over Azure Boost** bypasses the TCP/MANA software path (memory copies + sync), used for split **prefill/decode** inference pools. Demo: throughput **~3,400 → 7,637 tokens** (≈2×) and **TTFT cut from ~123k → ~47k ms** when switching TCP/IP → RDMA (`mana0` device). Powers inference clusters behind **Foundry**.
- **The future is serverless** (a 10-year-running Russinovich thesis) — now arriving via **Azure Container Instances (ACI)**. Azure treats **only virtualization** (not process/user-mode isolation) as a security boundary, so ACI isolates containers with **Hyper-V**. Already underpins **GitHub Actions, Python in Excel, Horizon DB**.
- **Direct virtualization (L1)**: containers run as peers to the management VM (parent partition = L1 host; child VMs = L2 hosts for individual containers/pods) — removes nested-virtualization overhead while keeping strong hostile-multi-tenant isolation. Whole fleet migrating (a **1–2 year** effort).
- **Container live migration** shown publicly for the first time — a ticking container moved server→server with **no gap** (tick 695 preserved). Brings VM-style minimal-downtime servicing to containers.
- **Manifold** treats all Microsoft GPUs as **one pool** for priority-based, topology-aware scheduling across **ASICs / GPUs / FPGAs / CPUs**; supports complex models (embedding + vision LLM components). With direct virtualization, CPU and GPU model components run in **separate Hyper-V-isolated pods** with direct GPU passthrough. Demoed Llama 4 Maverick inference on a GPU pod beside an isolated 2-CPU/no-GPU pod.
- **Azure Context Cache** (preview): a **storage-account-backed, pooled KV cache** behind all servers, so a moved/re-routed conversation doesn't re-pay prefill. Demo lifted cache hit rate to **~96.2%** under concurrency where per-server caches dropped.
- **Container sandboxes** for agents start in ~instant time via **memory snapshotting** (snapshot once, map memory for subsequent launches, skipping init). Demo: **10,000 sandboxes** across 10 workers, **~2s average launch**. Agent sandboxing is landing on ACI.
- **Confidential computing** protects data *in use* (in a hardware enclave) + provides **attestation** (a hardware "quote" → relying party / KMS policy releases a key only to an approved enclave). Azure has built this for **a decade** (Intel SGX → AMD/Intel CVMs) and claims the **largest confidential-computing portfolio of any hyperscaler**.
- **First-ever public confidential VM live migration** — achieved "in the last few weeks," not yet in production. Uses a measured **migration TD (mig TD)** + sending/receiving policy to extend the confidential trust boundary between two servers (work done deeply with Intel).
- **Azure Integrated HSM** (internal name **ManaCore**; announced late last year) puts a **FIPS 140‑3 Level 3 HSM in every Azure server**; keys can be released *with policy* from Azure Managed HSM / Key Vault into it and used directly by the VM. Demo: AKV signing **~640 ops/s → ~18,800 ops/s** with no loss of security. Built on Microsoft's **Caliptra** root of trust (donated to Open Compute Project).
- **Project Mosaic** (MSR, experimental): replace high-power optical lasers with **many low-speed channels of standard micro-LEDs** over imaging fiber, read by **silicon camera sensor arrays** — riding commodity VR/camera supply chains. Live demo from **MSR Cambridge** rendered the letter "Z" by individually modulating micro-LEDs at gigabit speeds.

## 📚 Detailed Notes

### Framing & format
Mark Russinovich opens as **CTO and Deputy CISO for Azure**, noting this recurring "Inside Azure Innovations" talk spans the whole Azure infrastructure stack — **data centers → cybersecurity → systems under development**. Standard caveat: some content hasn't shipped, some just shipped, and some may never ship (or not in the form shown). The unifying thread is **innovation powering AI**, specifically the **co-design of AI data centers, the core infrastructure, and the software running on top**.

### 1. Infrastructure — Fairwater data centers
Russinovich recounts a **November visit to Fairwater in Atlanta** (companion sites in Wisconsin). The Atlanta site is "continuously under construction." A walkthrough video showed:
- **Network cabling trunks** connecting top-floor and bottom-floor servers — "enough cabling to wrap the Earth four times" per site.
- **Liquid-cooling cables** pre-laid so servers can be dropped into sleds and racked; InfiniBand + Ethernet cables on the rack backs.
- A **break-fix** of liquid cooling being plugged into a rack. (Aside: Mark plugged in a loose cable and minutes later Scott Guthrie got a text that "power cell three" had unexpectedly powered on.)

### 2. Azure Boost (server offload card)
**Purpose:** offload the **data planes** for storage + networking off the main server CPUs onto a dedicated card, and also move the host **management "agents"** off the server — leaving the customer workload in maximal control of the server.

**Hardware:** the latest-gen Azure Boost card carries **DRAM** around the edges and a central **SoC** containing **Arm cores, a DPU, and an FPGA**, where the data plane is processed and the agents run.

**Gen-over-gen stats (since last Build):**
| Capability | New value | Note |
|---|---|---|
| Remote storage throughput | **20 Gb/s** | ≈ **1.4×** increase |
| Remote storage IOPS | **1,000,000** | |
| Local NVMe throughput | **36 Gb/s** | local NVMe |
| Local NVMe IOPS | **6.6 million** | via Boost NVMe offload acceleration |
| Networking | **400 Gb** | up from 200 Gb |
| Connections/sec | **400,000** | |

The card has **two 200 Gb network ports**, each going to a different **top-of-rack switch**, so a switch failure doesn't sever the server, and **sub-second servicing** with sub-second workload impact becomes possible. Azure Boost has been deploying for several years; **>30% of the fleet** now has it, with the goal of **every server**. It also enables **guest VM RDMA** (memory-to-memory transfers bypassing the networking stack, with Boost as transport).

**Bare-metal instances:** because management is offloaded to Boost, Azure can offer **bare-metal instances**, currently in limited access for **OpenAI** (the Fairwater GPU servers are bare metal). A **general-purpose bare-metal offering is coming**. Demo of `ND144V6`: grab the IP, SSH in, confirm **no virtualization services running**, and `lspci` showing a PCI bridge plus **eight Ethernet controllers** wired to RDMA-capable **Mellanox** NICs for the back-end GPU-to-GPU network.

### 3. MRC — Multipath Reliable Connection (training-fabric networking)
Fairwater **switched from InfiniBand to Ethernet**, and instead of **RoCE** (RDMA over Converged Ethernet) uses a **new protocol, MRC (Multipath Reliable Connection)**, co-developed with **OpenAI** and a growing partner consortium.

**Why:** synchronizing **~100,000 GPUs** routes packets across a vast fabric; **any congestion or failure on a synchronous training job** forces a checkpoint rollback and restart — a huge loss. MRC is **resilient** by **spraying packets across independent network domains called "planes."** If a link drops, the spray **rebalances automatically** onto the remaining planes.

**Demo:** two servers exchanging **4 GB payloads** over four switches, packet-sprayed across **eight planes (~12 Gb/plane)** for an **aggregate ~95 Gb/s** target. One switch was killed mid-flight; traffic **rebalanced across the remaining three** (one switch went to 0, another jumped to ~36 Gb/s) with **no drop in aggregate bandwidth (~95 Gb/s held)**. MRC is described as having become an **industry standard for large network topologies**.

### 4. VM-to-VM RDMA over Azure Boost
For general-purpose workloads, Azure is bringing **RDMA into VMs**. Normally VM↔VM traffic traverses the app → **TCP** → **MANA driver** (Microsoft Accelerated Network Adapter / Azure Boost NIC driver) and back up, with heavy **memory copies and synchronization**. **RDMA bypasses all of it** — the app maps memory in the remote system and Boost transfers data straight into the remote memory, eliminating the copies and sync.

**Scenario — split inference (prefill/decode):** inference splits into **prefill** (consume the prompt, populate the KV cache) and **decode** (generate new tokens). It's now common to put these in **separate server pools** because their memory/compute constraints differ.

**Demo (vLLM benchmark):**
- **TCP/IP baseline:** RDMA send-requests stayed flat at **460**; **token throughput ~3,400**; **median TTFT ~123,000 ms**.
- **RDMA via MANA link (`mana0`):** send-requests jumped **460 → 506**; **throughput ~7,637** (≈2×); **mean TTFT dropped to ~47,000 ms**.

This is deployed in Azure's **inference clusters behind Foundry**, powered by Azure Boost.

### 5. The core — serverless via Azure Container Instances (ACI)
Russinovich reiterates his long-held thesis: **"the future is serverless,"** now arriving with **ACI**. Traditional containers use **process isolation** (OS primitives). But **Azure does not treat a process / user-mode kernel as a security boundary** — only **virtualization** (with a tight, small connection between host and server) qualifies. So **ACI isolates every container with Hyper-V**.

**Adoption is broad** — using these services means indirectly using ACI:
- **GitHub Actions** now runs on ACI.
- **Python in Excel** runs on ACI.
- **Horizon DB** runs on ACI.

The goal is to make ACI efficient and capable enough that **process isolation is never needed**.

### 6. Direct (L1) virtualization
To remove **nested-virtualization overhead**, **direct virtualization** places containers **directly on servers as peers to the management VM**:
- **Parent partition = Layer-1 virtualization host.**
- **Child VMs = Layer-2 hosts**, each running an **individual container or pod**.

This keeps **strong hostile-multi-tenant isolation** while improving performance/efficiency. ACI itself now runs on direct virtualization, and **the entire fleet is migrating** — expected to take **1–2 years**. Direct virtualization also lets a GPU be assigned to a VM, which can spawn an L2 sub-VM and **hand the GPU through** for **direct hardware access**.

### 7. Container live migration (first public demo)
A long-standing VM advantage is **live migration** — minimal downtime when a server must be serviced or is predicted to fail. Containers have lacked this. Russinovich showed the **first public demo of container live migration**: a container on "dev six" emitting a **tick per second** (reached tick **695**) was migrated to "dev one." Inspecting the destination showed the same `hello world` workload, already at tick **755**, with **tick 695 present and no gap** in the log.

### 8. Manifold — Microsoft's GPU fleet scheduler
**Manifold** powers all of Microsoft's own inference and training by treating the **entire GPU pool as one**, doing **priority-based, topology-aware deployment** to maximize utilization while **abstracting the hardware** (**ASICs, GPUs, FPGAs, CPUs**). Modern models increasingly mix **CPU and GPU portions** and embed sub-models (e.g., an **embedding model** or a **vision LLM** in a multimodal model), making topologies more complex.

With **direct virtualization**, Manifold can place **CPU model components and GPU model components in separate Hyper-V-isolated pods** that don't interfere yet get **direct hardware access**.

**Demo:** a cluster node with two pods — a **GPU-based llama server** and a **CPU-based metrics server**. The GPU pod showed visible GPUs (via `nvidia-smi`), large RAM, many processors; the adjacent CPU pod showed **~no memory, 2 processors, no GPUs**. A cat image was sent for inference to the GPU pod running **Llama 4 Maverick**, proving CPU/GPU pods are isolated yet directly attached to physical hardware.

### 9. Azure Context Cache (pooled KV cache) — preview
The **KV cache is effectively the LLM's state** — you can't decode efficiently without the KV representing all prior prompt tokens. Conversations proceed in **turns** (e.g., a system prompt, then a PR-diff interaction with Copilot extends the prompt). Frameworks often let you cache the **system prompt**, but ideally you'd cache **the whole thing** so that if inference **moves to another server**, you don't re-pay the prefill cost. That requires a **cache behind all servers**.

**Azure Context Cache** (preview) backs the KV state in a **storage account**, so regardless of which server a request hits, a missing KV can be **fetched from the shared cache** instead of re-decoded — saving time and money.

**Demo:**
- **Concurrency 1, same system prompt:** ~**81%** cache-hit (after the first request, subsequent ones reuse the cached system prompt).
- **Concurrency 10:** requests spread across servers, so per-server hit rate **drops** (a conversation can land where the system prompt isn't present; first query is always a miss).
- **With the remote prompt cache enabled:** hit rate climbed to **~96.2%**, because the KV is fetched from remote cache no matter which server is hit — effectively a **pooled cache** rather than per-server caches.

### 10. Container sandboxes for agents (memory snapshotting)
Unlike container layers/images or full VM images, **container sandboxes** are **bespoke, tiny, lightweight** images meant to start **near-instantly** — ideal for agents that "write a Python script and run it" or "spin up an HTML site and iterate." Normal container cold-start is **5–20s** depending on OS, but the goal is **thousands starting simultaneously, fast, off the same base image**.

**Technique — memory snapshotting:** start the container once, **snapshot its memory**, then for subsequent requests **map that memory** straight into a running container, **skipping initialization**.

**Demo:** 10 worker pods each launching **1,000 sandboxes** → **10,000 container sandboxes**, with an **average launch time of ~2 seconds** — speed *and* scale. **Agent sandboxing is landing on ACI.**

### 11. Security — confidential computing
**Confidential computing** completes the data-protection triad. Data is already protected **in transit** (TLS everywhere now, vs occasional SSL 20 years ago) and **at rest** (node-level → server-side encryption → **customer-managed keys** for double-layered at-rest encryption). The gap is **data in use**: once decrypted on a server, plaintext sits where the **hypervisor, admins, host software, or a hacker** could reach it — and you may even want to keep **your own operators** away, exposing data **only to the compute that needs it**.

Confidential computing puts data in a **hardware enclave** none of those actors can enter. Crucially, the hardware can **measure the enclave's contents** — an **attestation**. Code inside requests a **"quote"** (the attestation) and presents it to a **relying party** (typically a **key management service** with a policy: release this key *only* to an enclave of this **hardware type, security version number, and code configuration**). The key is then released **encrypted to the enclave**, decrypted inside, and used to process data in the clear — with everyone assured of hardware isolation.

Azure has built this for **over a decade**: **Intel SGX** servers first, now **AMD and Intel confidential VMs**, with the **largest confidential-computing portfolio of any hyperscaler** (services, **confidential containers on ACI**, and underlying hardware).

### 12. Confidential VM live migration (first-ever public demo)
**Live migration is a fundamental hyperscale requirement** (reduce fragmentation, move workloads off failing servers, reduce servicing impact) — but it's been **missing from confidential computing**. Working deeply with **Intel**, Azure built **confidential live migration**:
- The source CVM is paired with a **migration TD (mig TD)** — a **confidential partition** that is **measured as part of the VM's measurement**.
- **Sending and receiving sides enforce policy**: migrate only to a server with a **mig TD approved for this VM**, thereby **extending the confidential trust boundary** between servers under hardware-enforced policy.

**Demo:** Hyper-V Manager on two servers; a CVM on server one RDP-pinging every second. After starting migration (a multi-GB VM, sped up for the demo), **TD-info attestations** printed, then the **CVM moved** to the other server (the ping died because the IP was tied to server one). Russinovich stresses this is **the first confidential VM live migration shown anywhere**, achieved **in the last few weeks**, **not yet in production**.

### 13. Azure Integrated HSM (ManaCore) + Caliptra root of trust
Beyond a **root of trust** (Microsoft's **Caliptra**, donated to the **Open Compute Project**, deployed in every server), Azure's security-hardware architects identified a need for **key management inside the hardware of every server** — so keys stay **hardware-protected across their whole lifecycle** and **never leave the hardware trust boundary**.

This became **ManaCore** internally, announced publicly **late last year** as the **Azure Integrated HSM** — effectively an **HSM in every single Azure server**, now being deployed fleet-wide. A key can be **released with policy** from **Azure Managed HSM or Azure Key Vault** into the integrated HSM, which is **FIPS 140‑3 Level 3 certified** (same bar as the HSMs behind Managed HSM / Key Vault). So the key stays **within a FIPS 140‑3 Level 3 boundary** from the HSM all the way to the server, and can be used for operations **directly from the VM** (the hardware is mapped into the VM).

**Demo (sign 5,000 payloads over 32 threads with an AKV key):**
- **Key never leaves AKV's HSM** (every op sent to the HSM): **~640 signing ops/sec**.
- **Key released into the local Azure Integrated HSM** (ops performed directly on it): **~18,800 signing ops/sec** — with **no loss of security**.

Russinovich frames this as the future: confidential computing where **keys for everything** (including services agents talk to) are **hardware-protected for their entire lifecycle** and **can never be stolen**.

### 14. Project Mosaic — micro-LED optical interconnect (Microsoft Research, experimental)
Closing with speculative **Microsoft Research** work that may or may not be productized. **Intra-data-center networking has been copper** — cheap, light, reliable, but limited to **~2 m** without loss, which is too short as computing **disaggregates** (GPUs in one place, servers in another) and demands high-bandwidth interconnect. The industry is moving to **optics with lasers**, but lasers are **high-power, hot, and expensive**.

**Project Mosaic** instead uses **many low-speed channels with standard micro-LEDs** — the same **micro-LED tech being productized for next-gen VR glasses/goggles and cameras** — projecting LED light over **fibers inside a cable**, read by **standard silicon camera sensor arrays**. The appeal: **ride commodity supply chains** scaling for other reasons, while deploying the tech in data centers.

**Live demo from MSR Cambridge** (guest researcher "Katar/Qatar"): inside the cable is a small **PCB** with a **package** containing a tiny **array of micro-LEDs + photodetectors** over a **CMOS control chip**, tested on a larger evaluation board. Hundreds of micro-LEDs couple via an **optical coupler** into an **imaging fiber** (with **thousands of pores/cores**, each micro-LED coupling to more than one pore to ease alignment). After **tens of meters** of transmission, the receiver shows the fiber's output facet. In real operation all micro-LEDs flash **billions of times per second** (invisible to the eye). To prove it's live and individually controllable, Mark picked the letter **"Z"**, and the lab modulated the micro-LEDs (each "flower" = one micro-LED at gigabits/sec) to render it.

### Wrap-up
Russinovich recaps innovation **at every layer** — hardware, data centers, serverless, GPUs, prompt pre-fetching/inference, and a speculative look at future in-data-center networking — then points to his follow-on session with **Scott Guthrie** on the **future of software engineering**.

## 🛠️ Products / Features / Technologies Mentioned
- **Fairwater data centers** — Microsoft's AI data centers (Wisconsin, Atlanta) with liquid cooling and massive InfiniBand/Ethernet fabric.
- **Azure Boost** — server offload card (Arm cores + DPU + FPGA SoC) moving storage/networking data planes and host agents off the main CPU.
- **Bare-metal instances** — VM-free instances enabled by Boost offload; in limited access for OpenAI, GP offering coming (demoed `ND144V6`).
- **MRC (Multipath Reliable Connection)** — resilient Ethernet training protocol that packet-sprays across "planes"; replaces RoCE for large GPU fabrics.
- **InfiniBand → Ethernet** — Fairwater's back-end network transport switch.
- **MANA driver / `mana0`** — Microsoft Accelerated Network Adapter (Azure Boost NIC) driver; exposes the RDMA verbs device.
- **VM-to-VM RDMA (guest RDMA over Azure Boost)** — memory-to-memory transfers bypassing the TCP/software networking path.
- **Azure Container Instances (ACI)** — serverless containers, Hyper-V-isolated; underpins GitHub Actions, Python in Excel, Horizon DB.
- **Direct virtualization (L1)** — containers as peers to the management VM (L1 parent partition / L2 child VMs) to drop nested-virt overhead.
- **Container live migration** — minimal-downtime server-to-server container moves on ACI (first public demo).
- **Manifold** — Microsoft's fleet-wide GPU scheduler; one pool across ASIC/GPU/FPGA/CPU with topology-aware, priority-based placement.
- **Azure Context Cache** — preview; storage-backed pooled KV cache so moved inference doesn't re-pay prefill.
- **Container sandboxes** — ultra-fast (memory-snapshot) sandboxes for agent code execution on ACI.
- **Confidential computing** — hardware-enclave protection of data *in use* with attestation/quotes; SGX, AMD/Intel CVMs, confidential containers on ACI.
- **Confidential VM live migration** — CVM migration via a measured **migration TD (mig TD)** under hardware-enforced policy (first public demo, with Intel).
- **Azure Integrated HSM (internal: ManaCore)** — FIPS 140‑3 Level 3 HSM in every server; policy-released keys usable directly by the VM.
- **Caliptra** — Microsoft's hardware root of trust in every server, donated to the Open Compute Project.
- **Azure Managed HSM / Azure Key Vault (AKV)** — KMS that releases keys (with policy) into the Azure Integrated HSM.
- **Project Mosaic** — experimental MSR micro-LED optical interconnect over imaging fiber, read by silicon camera sensor arrays.
- **Azure AI Foundry** — platform whose inference clusters run the Boost-powered RDMA inference described.
- **vLLM** — inference engine used for the prefill/decode RDMA benchmark.
- **Llama 4 Maverick** — model run in the Manifold GPU-pod inference demo.
- **Horizon DB** — database service shown running on ACI.
- **Python in Excel** — feature shown running on ACI.
- **GitHub Actions** — CI/CD service shown running on ACI.

## 🚀 Announcements / What's New
- **Latest-gen Azure Boost** deployed: **400 Gb** networking (from 200), **20 Gb/s** remote storage / **1M IOPS**, **36 Gb/s** + **6.6M IOPS** local NVMe, **400k** conns/sec. **>30% of fleet** enabled. *(Shipping/rolling out.)*
- **Bare-metal instances** — **limited access today (OpenAI on Fairwater)**; **general-purpose offering coming** "in the near future." *(Limited → GP roadmap.)*
- **MRC** — in production for OpenAI training; positioned as an emerging **industry standard** for large topologies. *(In use.)*
- **VM-to-VM RDMA over Azure Boost** — deployed in **Foundry inference clusters**. *(In use.)*
- **Direct (L1) virtualization** — ACI now runs on it; **whole-fleet migration underway (1–2 years)**. *(Rolling out.)*
- **Container live migration on ACI** — **first public demo**; **still under development**. *(Preview/dev.)*
- **Azure Context Cache** — **coming out in preview now**. *(Preview.)*
- **Container sandboxes for agents** — agent sandboxing **landing on ACI**. *(Coming.)*
- **Confidential VM live migration** — **first-ever public demo**; **not yet in production** (built with Intel, achieved within weeks). *(Pre-production.)*
- **Azure Integrated HSM (ManaCore)** — announced **late last year**; **being deployed into every server** now. *(GA-track rollout, FIPS 140‑3 L3.)*
- **Project Mosaic** — **experimental Microsoft Research**; may or may not be productized. *(Research.)*

## 💡 Demos
1. **Fairwater Atlanta walkthrough video** — cabling trunks, liquid-cooling install, server-sled racking, a live break-fix — conveyed the scale and continuous build-out of an AI data center.
2. **Bare-metal `ND144V6`** — SSH in, confirm no virtualization running, `lspci` shows PCI bridge + 8 RDMA-capable Mellanox NICs — proved it's a true bare-metal GPU server.
3. **MRC resiliency** — 4 GB payloads sprayed over 8 planes / 4 switches at ~95 Gb/s; killed a switch, traffic rebalanced (one →0, another →36 Gb/s) with **no aggregate bandwidth drop** — proved failure resilience for 100k-GPU training.
4. **VM-to-VM RDMA (vLLM prefill/decode)** — TCP/IP ~3,400 tok & ~123k ms TTFT vs RDMA (`mana0`) ~7,637 tok & ~47k ms TTFT — proved ~2× inference gain by bypassing the software net stack.
5. **Container live migration** — ticking container moved dev6→dev1; tick 695 preserved, no gap — proved VM-class live migration for containers.
6. **Manifold isolated pods** — GPU pod (Llama 4 Maverick, GPUs/RAM/CPUs visible) beside an isolated CPU pod (2 procs, ~no RAM, no GPU); cat-image inference succeeded — proved CPU/GPU isolation with direct GPU passthrough via direct virtualization.
7. **Azure Context Cache** — hit rate ~81% (concurrency 1) dropping under concurrency 10, then **~96.2%** with the remote pooled cache — proved pooled KV cache beats per-server caches.
8. **10,000 container sandboxes** — 10 workers × 1,000 each launched with **~2s average** start — proved speed *and* scale via memory snapshotting.
9. **Confidential VM live migration** — CVM with mig TD migrated between Hyper-V hosts; TD-info attestations printed, ping died as IP moved — **first-ever public demo** of confidential live migration.
10. **Azure Integrated HSM signing** — AKV-only signing **~640 ops/s** vs key released into integrated HSM **~18,800 ops/s** — proved ~30× throughput with no security loss.
11. **Project Mosaic live link (MSR Cambridge)** — micro-LED-over-imaging-fiber transmission rendered the letter **"Z"** by individually modulating LEDs — proved live, individually addressable optical channels on commodity tech.

## 📊 Notable Stats / Quotes
- “Enough cabling to **wrap the Earth four times**” in one Fairwater site.
- Azure Boost: **400 Gb** net, **20 Gb/s**/**1M IOPS** remote storage, **36 Gb/s**/**6.6M IOPS** local NVMe, **400k** conns/sec; **>30% of fleet**.
- MRC demo: **~95 Gb/s** aggregate held through a switch failure; **8 planes × ~12 Gb/s**.
- RDMA inference: **~3,400 → ~7,637 tokens** throughput; **TTFT ~123,000 → ~47,000 ms**.
- Container cold-start **5–20s** normally; **10,000 sandboxes** at **~2s average** launch.
- Azure Context Cache hit rate up to **~96.2%** (pooled) vs ~81% / lower per-server.
- Copper link limit **~2 m**; micro-LEDs flash **billions of times/sec**; fiber has **>thousands of pores/cores**.
- Azure Integrated HSM signing: **~640 → ~18,800 ops/sec**; **FIPS 140‑3 Level 3**.
- “The **future is serverless**” — a thesis Russinovich says he's repeated for **10 years**.
- “**First time ever** this has been shown publicly” — on the confidential VM live migration.
- Connecting **~100,000 GPUs** is the scale driving MRC's design.
- Confidential computing built in Azure for **over a decade**; **largest hyperscaler portfolio**.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: provision a **bare-metal `ND`-series** instance once GP-available; test **VM-to-VM RDMA** for a split prefill/decode inference deployment; enable **Azure Context Cache** (preview) on a Foundry workload and measure hit-rate/cost; evaluate **Azure Integrated HSM** for high-throughput signing vs AKV/Managed HSM.
- [ ] Questions: When does the **GP bare-metal** offering GA, and which regions? Is **container live migration** / **Azure Context Cache** GA timeline public? Is **confidential VM live migration** AMD-bound too or Intel-TDX-only at first? What models/sizes does **Azure Context Cache** support, and storage-cost vs prefill-savings tradeoff?
- [ ] Relevant to: AI infra/platform planning, Foundry inference cost optimization, confidential-computing migration story for regulated workloads, key-management/HSM strategy, and ACI-based agent sandboxing.

## 🔗 Related
- [[2026 Build Session List]]
- 
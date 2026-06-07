---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/azure-linux
  - topic/linux
  - topic/containers
  - topic/aks
  - topic/azure
source: https://www.youtube.com/watch?v=z7KV4KwoU0s
session_code: OD827
event: Microsoft Build 2026
speakers: Purvi Naran, Flora Targin
duration_min: 22
aliases:
  - Build, deploy, and run Linux workloads on Azure
---

# OD827 — Build, deploy, and run Linux workloads on Azure

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Purvi Naran (Senior Product Manager, Azure Linux) · Flora Targin (Azure Linux team)  
> **Duration:** ~22 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=z7KV4KwoU0s)

## 🎯 TL;DR
Azure Linux is Microsoft's own purpose-built Linux distribution — "by Azure, for Azure" — that already powers over 80% of Microsoft's internal Linux usage (Office, LinkedIn, Xbox, Defender, Cloud Shell, AKS, App Services, core Azure infra). This session walks through Microsoft's long Linux journey, the three-layer Azure Linux architecture, and where it runs (AKS, VMs/VMSS, containers). The headline Build 2026 announcements are **Azure Linux 4.0 in preview for VMs and VMSS** (rebased on Fedora, SELinux + FirewallD enforcing by default, DNF5, 6.18 LTS kernel) and the **GA of Azure Container Linux (ACL)** — an immutable, Flatcar-architecture container host built on the Azure Linux supply chain for AKS. The core value props throughout are resiliency (release-blocking validation), security (Microsoft-owned supply chain, fewer packages = fewer CVEs, 5-day critical-CVE SLA), and performance (lean image → faster pod/node startup). Everything is open source on GitHub with a bi-monthly community call.

## 🔑 Key Takeaways
- **Azure Linux = Microsoft's purpose-built Linux distro for Azure**, formerly the internal CBL-Mariner project; it is now the standard OS for the bulk of Microsoft's own Linux footprint.
- **Over 80% of Microsoft's Linux usage runs on Azure Linux today** — adopting it means running the same OS that powers Microsoft's most critical workloads.
- Two big Build 2026 announcements: **Azure Linux 4.0 (preview) for VMs/VMSS**, and **Azure Container Linux (GA)** as an immutable OS for AKS nodes. Azure Linux container images also enter preview.
- **Azure Linux 4.0 is rebased on Fedora** (3.0 lineage was different) — packages derived from Fedora, optimized for Azure; familiar to anyone in the RHEL/Fedora ecosystem; eases ISV adoption.
- **Secure by default:** SELinux enforcing, FirewallD locked down, lean package set (smaller attack surface), 6.18 upstream LTS kernel, DNF5 package manager.
- **Azure Container Linux (ACL)** marries **Flatcar's** proven immutable design with Azure Linux's hardened, signed-RPM supply chain — read-only `/usr` backed by DM-Verity, SELinux enforcing, A/B update agent, trusted launch with a unified kernel image. Not binary-compatible with Flatcar (built on Azure Linux, not Gen2 sources).
- **Two AKS host options, not mutually exclusive:** Azure Linux (flexible, familiar, great for lift-and-shift) vs Azure Container Linux (opinionated, hardened, immutable). You can run both as separate node pools in one cluster and schedule workloads accordingly.
- **Four reasons Microsoft built its own distro:** security (own the end-to-end supply chain, every package built from source + signed), performance (Azure-optimized image), quality (failing tests block the release), support/compliance (one vendor, one channel).
- **Three-layer architecture:** Azure Linux kernel (upstream LTS, Hyper-V + Azure silicon drivers, hardened, x86-64 + arm64) → small-footprint core RPM packages → around-the-clock Microsoft protection (monthly servicing + on-demand critical patches).
- **Security SLAs:** critical CVEs remediated within **5 days**; kernel modules signed with Microsoft's trusted key; FIPS, CIS L1/L2, FedRAMP-ready, secure boot — all at no extra cost.
- **Performance wins are real:** MediaKind reported faster node setup; PlayFab saw quicker scaling under player influx; cluster create/upgrade benchmarks are on par or faster than other distros.
- **AKS GA since May 2023**, running millions of cores across thousands of customers in financial services, healthcare, video streaming, and data analytics.
- **Fully open source** — file issues / submit PRs on GitHub, contributions actively reviewed, plus a bi-monthly community call for roadmap, demos, and live feedback.

## 📚 Detailed Notes

### Microsoft's Linux journey (the "why we're credible here" timeline)
Purvi opens by framing Microsoft's Linux story as longer than most people realize:
- **2009** — Microsoft releases 20,000 lines of code into the Linux kernel. (The famous headline: "pigs do fly.")
- **2011** — Microsoft becomes one of the **top five contributors** to the Linux kernel, driven by Hyper-V and virtualization investment.
- **2015** — Ships **VS Code** and co-founds the **Node.js Foundation**.
- **2018** — Acquires **GitHub**; VS Code is the #1 developer tool; Azure trending toward **50% Linux workloads**.
- **2019** — Ships the **Linux kernel for WSL**, and quietly releases an internal project, **CBL-Mariner**, on GitHub — the seed that becomes Azure Linux.
- **2023** — **Azure Linux becomes GA as a container host on AKS**; .NET and Java container images built on it are released.
- **2026 (today, at Build)** — **Azure Linux 4.0 preview for VMs and VMSS** + **Azure Container Linux GA** as an immutable OS on AKS. Framed as "the next chapter."

### Why build your own Linux distribution? (four reasons)
1. **Security** — Microsoft owns the **end-to-end supply chain**. Every package is built from source and signed by Microsoft, so you never have to wonder where your binaries came from.
2. **Performance** — A highly performant image optimized specifically for Azure workloads across many environments.
3. **Quality** — A high quality bar to minimize outages and disruptions: **if tests fail, the release does not ship.**
4. **Support & compliance** — One vendor, one support channel; centralized support and compliance. "A distribution for Azure, by Azure."

This isn't theoretical: **over 80% of Microsoft's Linux usage runs on Azure Linux today** — Office, LinkedIn, Xbox, Defender, Cloud Shell, AKS, App Services, and core Azure infrastructure. Using it lets those teams spend less time on operational toil (compliance, OS upgrades, scanning/patching critical CVEs). "We trust it, and so can you."

### Architecture — a three-layer stack
1. **Azure Linux kernel (foundation)** — an upstream **LTS** Linux kernel optimized for **Hyper-V** across cloud and edge, with **Azure-specific silicon drivers** for better performance. Hardened with secure defaults; supports multiple architectures (**x86-64 and arm64**).
2. **Azure Linux core RPM packages** — a deliberately **small default footprint**: "you get what you need, nothing that you don't."
3. **Around-the-clock Microsoft protection** — every package built from scratch for supply-chain security; **critical CVE patches available quickly** for commercially supported images; **monthly servicing plus on-demand updates** for critical issues.

### Where Azure Linux runs
- **AKS** — GA since 2023, running **millions of cores** in mission-critical workloads across thousands of customers. New at Build: **Azure Container Linux GA** as an immutable OS for AKS nodes.
- **Virtual Machines** — Azure Linux entering **preview** for VMs: the same distribution but more **general-purpose**, supporting any VM or VMSS deployment.
- **Container images** — entering **preview**, pre-installed with all the tooling you need to work with Azure, ready to pull from the **Microsoft Container Registry (MCR)**.

### Azure Linux on VMs (general-purpose story)
- A **full general-purpose distribution** — supports any Linux workload you want to run.
- Packages are **derived from Fedora** and optimized for Azure; each undergoes rigorous **performance and quality testing** before release.
- **Day-one GA** support for Microsoft extensions and partner products → existing tooling works out of the box.
- Security/compliance: **SLAs for high and critical CVEs** (backed by thousands of security researchers + MSRC), plus **FIPS validation**, **CIS Level 1 and Level 2 benchmarks** at GA, and **secure boot** support.

### Azure Linux 4.0 — what's new (Fedora rebase)
Built on a robust open-source foundation (**Fedora**) and enhanced with Azure-specific innovations for a powerful, secure, developer-friendly environment:
- **Robust upstream support** — leverages Fedora's active community for rapid innovation.
- **Declarative deviations** — any changes from upstream are clearly documented → straightforward auditing and compliance.
- **Simplified ISV experience** — if partners already support the **RHEL/REL ecosystem**, Azure Linux feels familiar and easy to adopt.
- **Enhanced security** — Azure CVE SLAs inherited; compliance-ready out of the box with **FIPS, FedRAMP, CIS benchmarking, secure boot, and SELinux enforced by default**.
- **Operational excellence** — a **rolling release model**, **LTS + hardware-enablement (HWE) kernels**, and **single-vendor support** for streamlined management.

### Azure Linux 4.0 — native Azure integration
Ships with native support for the Azure services, dev tools, and security features workloads already depend on:
- **Security & observability** — **Defender for Cloud** (security management) and **Azure Monitor** (health/performance insights).
- **Custom image management** — **Azure Image Builder** and **Image Customizer** to build, customize, and deploy your own Azure Linux images.
- **Developer ecosystem** — full support for popular runtimes (**.NET, OpenJDK**) and seamless control via **Azure CLI**.

### Customer adoption (VMs / general)
Since GA in **May 2023**, thousands of customers across financial services, healthcare, video streaming, and data analytics have adopted Azure Linux:
- Streaming-service customers report **strong reliability** (fewer interruptions).
- Large retailers chose it for **best-in-class performance** on Azure.
- Regulated industries (healthcare, finance) adopted it for its **reduced attack surface** / strong security guarantees.
- Consistent feedback theme: **reliability, performance, security.**

### Azure Linux for AKS (Flora's segment)
Flora Targin takes over to cover the Kubernetes story:
- A **typical AKS node** runs a **purpose-built version of Azure Linux** including only the essential components needed to run Kubernetes workloads efficiently → a **lightweight OS** with a minimal footprint.
- Packages are **deliberately selected and rigorously tested on AKS infrastructure** for high confidence in stability.
- **Available everywhere you need it** — in the cloud with AKS, or at the edge via **AKS enabled by Azure Arc** → a consistent platform across environments.
- **Security built in by design** — strong **compute-level isolation**, and with options like an **immutable host configuration**, it reduces drift and minimizes attack surface over time.
- Net: a **minimal, well-tested, secure foundation** for running containerized workloads at scale.

### Azure Container Linux (ACL) — GA announcement
The marquee AKS announcement. **Azure Container Linux (ACL)** brings together:
- **Flatcar's** proven, **vendor-neutral, immutable** design, **+**
- The **hardened security and trusted supply chain of Azure Linux**.

Result: a secure, scalable container host purpose-built for production workloads.
- Based on **Flatcar's architecture**; delivers a minimal, immutable OS optimized for containers.
- **Not binary-compatible with Flatcar** — it's built on **Azure Linux rather than Gen2 sources** — but provides the **same core functionality and operational model** customers rely on today.

**Out-of-the-box security guarantees in ACL:**
1. **Immutability enforced at the kernel level** — critical system components like the **`/usr` directory** are locked down to prevent drift and unauthorized changes.
2. **Minimal, purpose-built package set** — reduces attack surface and lowers CVE exposure.
3. **Strong runtime protection via SELinux** — strict, least-privilege access controls across the system.
4. **Trusted launch with a unified kernel image** — ensures system integrity from the very first boot stage.
5. **Same secure end-to-end Microsoft supply chain** as Azure Linux — **signed RPMs you can trust**.

### Choosing between Azure Linux and Azure Container Linux on AKS
A decision slide differentiating the two Azure Linux–based container host options:
- **Azure Linux (left)** — the more **general-purpose, familiar** Linux node experience. Uses the **standard Kubernetes host stack**. Great for **lift-and-shift migrations** or anyone wanting a flexible, familiar host environment while still getting Microsoft's security posture for AKS.
- **Azure Container Linux (right)** — the more **opinionated, container-optimized** option. Builds on Azure Linux but adds stronger security/integrity guarantees by default: **read-only `/usr` backed by DM-Verity**, **SELinux enabled**, an **A/B update agent**, and other hardening. Designed for **cloud-native** customers wanting a minimal, immutable host model (similar to other container-optimized OSs in the ecosystem).

**Key practical point — they're not mutually exclusive:** in AKS you can run an **Azure Linux node pool alongside an Azure Container Linux node pool in the same cluster** and schedule workloads to the right host based on needs. Takeaway:
- Choose **Azure Linux** → familiar, flexible host experience.
- Choose **Azure Container Linux** → most hardened, minimal, immutable host by default.
- **Mixed requirements** → use **both side by side**, splitting workloads across node pools.

### Ecosystem & partner integration
- Azure customers depend on a diverse ecosystem of **Azure-native, third-party, and open-source tooling** across DevOps, observability, networking, and security.
- On AKS, Azure Linux enables **seamless integration** with leading partner solutions, with **full compatibility with Azure extensions**.
- **Azure Linux 4.0 for VMs and Azure Container Linux** deliver strong **day-one partner support** for a subset of partners, accelerating production readiness.
- Deeply integrated with the **open-source ecosystem** — builds on and contributes to the upstream kernel and Fedora, plus key community projects: **Kata Containers, containerd, and systemd**.

### Three core benefits (the closing framework)
**1. Resiliency**
- Customers worry about outages during OS/app upgrades; traditional distros bring frequent reboots, downtime, regressions.
- Azure Linux mitigates via **rigorous end-to-end validation across Azure scenarios before release** — **any failure blocks the release**.
- Core components (kernel, critical system packages) kept on **stable LTS versions with security patches backported**; changes introduced in a **controlled manner at release boundaries**, avoiding disruptive mid-cycle updates.

**2. Performance**
- Performance regressions hurt line-of-business apps, and customers often blame the OS.
- A **lightweight, Azure-optimized image** → **faster pod and node startup times** on AKS.
  - **MediaKind** reported faster node setup times.
  - **PlayFab** saw quicker scaling to handle player influx.
- Performance tests run alongside quality checks; **regressions block the release**.
- **Cluster create and cluster upgrade** benchmarks show Azure Linux **consistently on par or faster** than other distros.

**3. Security**
- Challenges: **CVE overload** and **supply chain threats**.
- **Fewer packages shipped → fewer CVEs to begin with** (reduced attack surface).
- **Strict remediation SLAs** — **critical CVEs addressed within 5 days**.
- **All kernel modules signed with Microsoft's trusted key** → only authorized code runs in kernel space.
- **Everything built from source on Microsoft-managed infrastructure** → full control and transparency.
- **Strong out-of-the-box compliance** — FIPS images, CIS benchmark alignment, secure boot — **at no additional cost**.

### Getting started / community
- **Everything is open source.** GitHub is where you can **file issues and submit PRs**; community contributions are actively reviewed ("we want more of them").
- Enterprise offerings reachable via documentation links on the slide.
- **Bi-monthly community call** — roadmap updates, new-feature demos, and live feedback. "This is a community effort and your feedback directly shapes what we build."
- Closing: Azure Linux end-to-end — modern, secure, purpose-built; a **unified foundation across VMs, AKS, and containers**, from **Azure Linux 4.0** to **Azure Container Linux**.

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Linux** — Microsoft's purpose-built Linux distribution for Azure (formerly CBL-Mariner); runs on AKS, VMs/VMSS, and as container images.
- **CBL-Mariner** — the original internal Microsoft Linux project (2019) that became Azure Linux.
- **Azure Linux 4.0** — new major version rebased on Fedora; preview for VMs/VMSS; SELinux + FirewallD enforcing, DNF5, 6.18 LTS kernel.
- **Azure Container Linux (ACL)** — immutable, Flatcar-architecture container host for AKS built on the Azure Linux supply chain; GA at Build 2026.
- **Azure Kubernetes Service (AKS)** — managed Kubernetes; primary home for Azure Linux as a container host since 2023.
- **AKS enabled by Azure Arc** — runs Azure Linux on AKS at the edge for a consistent cloud/edge platform.
- **Azure Linux container images** — preview; pre-loaded with Azure tooling, pullable from MCR.
- **Microsoft Container Registry (MCR)** — registry to pull Azure Linux container images from.
- **Flatcar Container Linux** — the proven, vendor-neutral, immutable OS whose architecture ACL is based on (not binary-compatible).
- **Fedora** — upstream foundation Azure Linux 4.0 packages are derived from.
- **Linux kernel (6.18, upstream LTS)** — the kernel Azure Linux 4.0 ships, hardened/tuned for Azure with Azure silicon drivers.
- **SELinux** — mandatory access control, **enforcing by default** in Azure Linux 4.0 and ACL.
- **FirewallD** — host firewall, **active and locked down by default** in 4.0 (only explicitly allowed services open).
- **DNF5** — fast modern package manager shipped in Azure Linux 4.0 (familiar from Fedora/RHEL).
- **DM-Verity** — block-layer cryptographic verification backing the read-only `/usr` in ACL.
- **Unified Kernel Image (UKI)** — kernel + initramfs + command line signed as a single bundle (trusted launch).
- **vTPM / secure boot attestation** — verifies the secure boot chain in ACL (`bootctl`).
- **A/B update agent** — atomic, rollback-friendly OS updates in ACL.
- **Defender for Cloud** — security posture management integrated with Azure Linux.
- **Azure Monitor** — health/performance observability for Azure Linux.
- **Azure Image Builder / Image Customizer** — build, customize, and deploy custom Azure Linux images.
- **Azure CLI (`az aks create` with `--os-sku`)** — provisions AKS clusters/nodes, including ACL via the OS SKU flag.
- **.NET / OpenJDK** — supported developer runtimes with images built on Azure Linux.
- **MSRC (Microsoft Security Response Center)** — backs the high/critical CVE SLAs.
- **FIPS / CIS L1 & L2 / FedRAMP / secure boot** — compliance certifications/benchmarks available out of the box.
- **Kata Containers, containerd, systemd** — key open-source community projects Azure Linux builds on and contributes to.

## 🚀 Announcements / What's New
- **Azure Linux 4.0 — PREVIEW for VMs and VMSS.** Rebased on Fedora; SELinux enforcing + FirewallD locked down by default; DNF5; 6.18 upstream LTS kernel; FIPS/CIS/secure boot compliance-ready; rolling release with LTS + HWE kernels.
- **Azure Container Linux (ACL) — GA on AKS.** Immutable, Flatcar-architecture container host built on Azure Linux's signed-RPM supply chain; read-only `/usr` via DM-Verity, SELinux enforcing, A/B update agent, trusted launch with UKI. Provisioned via `--os-sku` in `az aks create`.
- **Azure Linux container images — PREVIEW.** Pre-installed with Azure tooling, pullable from MCR.
- (Context, prior milestone) Azure Linux on AKS has been **GA since 2023 / May 2023**, now running millions of cores.

## 💡 Demos

### Demo 1 — Azure Linux 4.0 on a VM (Purvi)
Purvi SSHes into an Azure Linux 4.0 VM running in Azure and demonstrates the "secure by default, lightweight" posture:
- **Confirms the OS** — Azure Linux 4.0, Fedora foundation, optimized for Azure.
- **Kernel** — the **6.18** upstream LTS kernel, hardened/tuned for Azure.
- **SELinux is enforcing by default** — no extra configuration; mandatory access control out of the box.
- **Lean image** — a small set of packages → fewer packages to patch, fewer CVEs, smaller attack surface.
- **Package management** — ships with **DNF5** (fast, modern, familiar from Fedora/RHEL); installing a package is "exactly what you'd expect."
- **Firewall** — **FirewallD active and locked down by default**; only explicitly allowed services are open. To open a custom port (e.g. **8080**) you add it explicitly — "nothing is open unless you say so."
- **Point proven:** secure by default (SELinux + FirewallD), lightweight (minimal package set), built on a modern Azure-optimized kernel.

### Demo 2 — Azure Container Linux on AKS (Flora)
Flora demos provisioning and inspecting an ACL node to prove the immutable, defense-in-depth model:
- **Create the cluster** — `az aks create` where the **only** extra thing needed is **`--os-sku AzureContainerLinux`** ("it's really that simple").
- **Grab credentials** and list nodes — the **OS image column confirms** the node is running Azure Container Linux.
- **OS identity** — ACL built on the **Azure Linux package pipeline** with the **same immutable OS architecture as Flatcar Container Linux**.
- **Kernel** — runs the **Azure Linux kernel**.
- **`bootctl`** — shows the **secure boot chain**: secure boot enabled with **vTPM attestation**, and a **unified kernel image** (kernel + initramfs + command line all signed as a single bundle).
- **DM-Verity on `/usr`** — cryptographically verifies every block read from disk.
- **Immutability proof** — trying to write to `/usr` directly, **even as root, is denied**; the filesystem is read-only enforced at the **block layer**.
- **SELinux in enforcing mode.**
- **Summary / point proven:** ACL gives **defense in depth at the node level** — an immutable OS image verified by DM-Verity plus mandatory access controls via SELinux. **Even if an attacker gets root inside a container, the host stays protected.**

## 📊 Notable Stats / Quotes
- **"Over 80% of Microsoft's Linux usage runs on Azure Linux today."** — the central credibility stat.
- **2009:** Microsoft released **20,000 lines of code** into the Linux kernel; headline: **"pigs do fly."**
- **2011:** one of the **top five contributors** to the Linux kernel.
- **2018:** Azure trending toward **50% Linux workloads**; VS Code the **#1 developer tool**.
- **AKS GA since 2023 (May 2023)** — running **millions of cores** across **thousands of customers**.
- **Critical CVEs remediated within 5 days** (security SLA).
- **Monthly servicing + on-demand critical updates.**
- Kernel: **6.18 upstream LTS**.
- Customer proof points: **MediaKind** (faster node setup times), **PlayFab** (quicker scaling under player influx).
- **"If tests fail, the release does not ship"** / **"any failure blocks the release"** — the quality-gate philosophy, repeated for resiliency and performance.
- **"This is a distribution for Azure, by Azure."**
- **"We trust it, and so can you."**
- **"Nothing is open unless you say so."** (FirewallD secure-by-default demo)
- Compliance out of the box **"at no additional cost"**: FIPS, CIS, secure boot.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Spin up an **Azure Linux 4.0 preview VM** and verify the secure-by-default posture (SELinux enforcing, FirewallD locked, DNF5, 6.18 kernel) hands-on.
  - Create an AKS cluster with **`az aks create --os-sku AzureContainerLinux`** and inspect the node (`bootctl`, DM-Verity on `/usr`, SELinux enforcing, attempt a root write to `/usr`).
  - Test the **mixed node-pool model**: one Azure Linux pool + one ACL pool in the same cluster, scheduling workloads to each.
  - Pull an **Azure Linux container image** from MCR and check the pre-installed Azure tooling.
  - Try **Azure Image Builder / Image Customizer** to produce a custom Azure Linux 4.0 image.
- [ ] Questions:
  - Migration path / compatibility from **Azure Linux 3.0** (different lineage) to **4.0 (Fedora-based)** for existing AKS node pools and images?
  - Exact **GA timeline** for Azure Linux 4.0 on VMs/VMSS and for the container-image preview?
  - Since ACL is **not binary-compatible with Flatcar**, what's the practical migration story for existing Flatcar users on AKS?
  - Which specific **partner/ISV products** get day-one support on 4.0 + ACL (the slide listed a subset)?
  - How does the **A/B update agent** in ACL handle rollback and surface update status operationally?
- [ ] Relevant to:
  - AKS platform/security hardening work and any lift-and-shift Linux migrations to Azure.
  - Regulated-industry workloads needing FIPS/CIS/secure boot + reduced attack surface.
  - Cost/ops reduction via fewer CVEs to patch and release-blocking quality gates.

## 🔗 Related
- [[Azure Kubernetes Service (AKS)]]
- [[Azure Linux]]
- [[Azure Container Linux]]
- [[Linux on Azure]]
- [[Container security]]
- [[Azure compliance (FIPS, CIS, FedRAMP)]]
- Source list: [[2026 Build Session List]]

---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/azure-linux
  - topic/containers
  - topic/aks
  - topic/cloud-native
  - topic/linux
  - topic/security
source: https://www.youtube.com/watch?v=mkeb8FbATG8
session_code: DEM311
event: Microsoft Build 2026
speakers: Jim Perrin, Porvi Narang
duration_min: 26
aliases:
  - Scale cloud-native workloads with Azure Linux
---

# DEM311 — Scale cloud-native workloads with Azure Linux

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Jim Perrin (PM, Azure Linux team) & Porvi Narang (PM, Azure Linux team)  
> **Duration:** ~26 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=mkeb8FbATG8)

## 🎯 TL;DR
Azure Linux is Microsoft's own Linux distribution, now in its 4.0 generation, built on Fedora as its upstream and re-architected around a "one OS everywhere" story: the same binaries, kernel, and libraries run across WSL, Azure VMs, containers, and AKS. The team's core philosophy is **security out of the box** (SELinux enforcing, firewalld, FIPS/FedRamp targeting) plus **declarative deviations** — intentionally stripping the desktop/graphical stack and other non-cloud packages to produce a lean image with a minimal attack surface and fewer CVEs, all tracked publicly in GitHub. The live demo proved the consistency claim by running the same Python app simultaneously on WSL, an Azure Linux 4.0 VM, and an AKS cluster. The headline announcements: **Azure Linux 4.0 VM image entered public preview** (WSL preview as a fast follow), and **Azure Container Linux went generally available** at Build — a hardened, immutable variant derived from CNCF's Flatcar Container Linux, currently shipping as 3.0 until 4.0 GA brings everything into alignment.

## 🔑 Key Takeaways
- **Azure Linux uses Fedora as its upstream** (the same innovation distro Red Hat builds RHEL from), giving Microsoft access to existing ISV support, CVE discovery/remediation partnership, and upstream open-source speed.
- **Microsoft's added value is programmatic reliability**: predictable release cadence, consistent CVE fixes (Patch-Tuesday-style cadence), FIPS compliance, FedRamp compliance — the enterprise dependability Azure customers expect layered onto fast upstream innovation.
- **All source code for the distribution is public on GitHub**, with a clear, declarative set of differences from Fedora so customers can see exactly where and why Microsoft deviates.
- **"One OS everywhere"** is the central value prop: Azure Linux and Azure Container Linux are built from the *exact same sources and binaries* and are fully compatible across WSL, VM, and Kubernetes/container scenarios.
- **Security out of the box** is the #1 principle: SELinux **enabled by default in enforcing mode**, firewalld on by default (only SSH open out of the box), no configuration required to be secure.
- **Declarative deviations = a leaner image**: the graphical/desktop stack is removed (no need for cloud workloads), reducing package bloat, attack surface, and CVE complexity.
- **Azure Linux 4.0 ships kernel 6.18** (latest upstream at the time), maintained for the lifetime of the distribution; a hardware-enabled kernel offers both LTS stability and faster iteration for customers who want rapid turnover.
- **DNF5** is the package manager; the demo installed Azure CLI in well under a minute.
- **Azure Container Linux is immutable and hardened**, derived from **Flatcar Container Linux** (contributed by Microsoft to the CNCF as an incubating project) — it adds Secure Boot, DM-Verity (read-only, verified-on-boot filesystem), and SELinux by default.
- **Azure Container Linux ≠ Flatcar deprecation.** Flatcar continues upstream, fully supported; ACL is a productized, consistency-focused variant. It consolidates the two immutable images previously in AKS into one usable product.
- **The AppArmor → SELinux conversion** is the one migration friction point the team expects for AKS customers used to AppArmor.
- **Version skew during preview is intentional and temporary**: Azure Container Linux is 3.0 (kernel 6.6) while Azure Linux 4.0 (kernel 6.18) is in preview; at 4.0 GA everything aligns to 4.0 across the board.
- **Developer workflow simplicity**: validate an app on one surface (e.g. WSL on a laptop) and trust it across all of them — same Python, same kernel, same internal libraries from local → GitHub → cloud → AI workloads.

## 📚 Detailed Notes

### What is Azure Linux — and the Fedora upstream choice
Azure Linux is Microsoft's first-party Linux distribution, presented here by the two PMs on the team (Jim Perrin and Porvi Narang). The agenda: explain what Azure Linux is, cover the Azure Container Linux story for the container/Kubernetes audience, demo it, and take Q&A.

For people from the broader Linux ecosystem, the anchor is familiar: Red Hat Enterprise Linux is built on **Fedora**, Fedora being the upstream innovation distribution Red Hat uses. **Azure Linux now uses Fedora the same way** — as its upstream. Microsoft is partnering closely with the Fedora community on Linux innovation, performance tweaks, and "Azure flavoring," and wants the Microsoft Linux community's changes visible to the broader Fedora world.

Why Fedora as upstream:
- **Existing ISV support** in the ecosystem comes along for free.
- Microsoft can **add its own work and contribute it back** to Fedora where it makes sense.
- It enables **partnership on CVE discovery and CVE remediation**.

### Microsoft's added value: programmatic reliability
Beyond consuming the upstream, Microsoft layers on the program-management value enterprises want:
- **FIPS compliance** and **FedRamp compliance**.
- **Clear, determined release timing** — explicitly likened to Microsoft's famous "Patch Tuesday" cadence.
- The result: you get upstream open-source innovation *and* speed, but with **programmatic reliability** — consistent release times, consistent CVE fixes, and consistency across the different application families.

A key transparency commitment: **all distribution source code is public on GitHub**, and Microsoft maintains a **clear declarative set of differences** from Fedora and other distros so customers can see exactly where Azure Linux deviates and why.

### One OS everywhere — Azure Linux + Azure Container Linux from the same source
A foundational point: **Azure Container Linux and Azure Linux are derived from the exact same sources.** The same binaries exist in both; they're completely compatible across the board. What the team is delivering spans three surfaces:
- **Containers**
- **The VM space**
- **A hardened set of images** for customers who want an **immutable build system** (covered later as Azure Container Linux).

Much of the engineering value is in **kernel tuning specifically for Azure** — for performance and reliability. A **hardware-enabled kernel** delivers both the **LTS stability** some customers want *and* the ability to **iterate quickly** for customers who want rapid transition/turnover. Layered on top is **streamlined management**: all the Azure tooling customers already use — e.g. **Azure Update Manager** — works as-is, preserving consistency across Azure.

### Demo setup — the "three columns" consistency demo
Porvi drives the technical demo to show the strategy in action. The premise: run **one simple Python application** across three different platforms — **WSL**, an **Azure Linux VM**, and **AKS** (with Azure Container Linux) — and show identical behavior to prove "one OS everywhere." The app is a small Python app that continuously refreshes CPU usage, memory, and uptime. The demo UI lights up a column per platform as each one comes online (WSL first, then VM, then AKS).

### WSL on Azure Linux 4.0
Porvi is already inside WSL running **Azure Linux 4.0** and verifies the version live. The Python app is started in WSL — lighting up the first "column" of the demo. This establishes the local-developer entry point of the one-OS story.

### Azure Linux 4.0 on an Azure VM — a deep dive
The same app is then deployed on an **Azure Linux 4.0 VM**, live. Porvi SSHes into a pre-created VM to confirm it's running Azure Linux 4.0, then walks through what the VM actually contains:

- **Kernel 6.18** — the latest upstream kernel, which they will **maintain for the lifetime of the distribution**.
- **Security: SELinux enabled by default in enforcing mode** — "security out of the box," no extra configuration needed. (Jim notes this will delight the SELinux-loving MVP in the audience and is a strong selling point for how seriously they take security.)
- **Declarative deviations in practice**: the image is **very lean** — deliberately optimized for Azure and cloud-native workloads. Image size is much smaller because Microsoft **intentionally defers** packages and only includes what Azure customers need.
  - Jim elaborates: **most of the graphical/desktop stack has been pulled out.** Fedora targets desktop users; that's irrelevant for cloud. Removing the graphical stack removes **package bloat** and **CVE complication**. Everything not required for cloud use has been stripped.
  - Result: a **very minimal attack surface and fewer CVEs.**
- **DNF5** as the package manager. To demonstrate, Porvi installs **Azure CLI** via DNF5 — it resolves dependencies and pulls from the repo in seconds (the live install completed quickly), then she verifies the correct/latest Azure CLI from their repository landed in the image.
- **firewalld enabled out of the box** — preconfigured, nothing to do. By default the **only thing the firewall allows is SSH** (for management/configuration). No additional services run beyond SSH.
  - Jim's important caveat on the one extra open port: the **DHCPv6 client** port exists only because the **IPv6 protocol has an ICMP requirement** to obtain an address — that's its sole purpose.
  - Porvi then **manually opens a port** to show that, while secure by default, ports are easy to open and remain **under explicit administrator control** — "you have to manually allow anything to be enabled."
- The Python app is then started on the VM via SSH (lighting the second column), constantly refreshing CPU/memory/uptime like the WSL instance.

### AKS with Azure Container Linux
The final surface is **Azure Kubernetes Service** using **Azure Container Linux** (ACL) — "another thing we are making generally available at Build." It's described as the **hardened Azure Linux image**. The demo deploys the same app to an AKS cluster, lighting the **third and final column**. With all three (WSL, VM, AKS) running on Azure Linux, the consistency claim is visually complete — same OS everywhere.

> Note on versions during preview: the AKS column shows **Azure Container Linux 3.0**, because **Azure Linux 4.0 is still in preview**. When 4.0 GAs, Azure Container Linux will move to 4.0 to match. The 3.0 label is purely a preview-period artifact; everything becomes 4.0 and consistent at GA.

### Why the consistency matters (the developer story)
Jim summarizes the core benefit: no matter how you consume Azure Linux — WSL, VM, container, or Azure Container Linux — you're using the **same Python version, the same kernel, and the same internal libraries**. So if you **validate your application on one surface, you can be confident it works across all of them.** The intended developer flow: **WSL on a local laptop → local deployment → production deployment → AI space**, made as frictionless as possible from local laptop into GitHub, into the cloud, into AI workloads.

**Status recap from the demo:** the Azure Linux 4.0 **VM image is in public preview** — available to use, test, validate, and give feedback on.

### Azure Container Linux deep dive — immutability & the Flatcar relationship
Jim takes the ACL portion in depth. Key technical and strategic points:

- ACL is an **immutable distribution**, **derived from Flatcar Container Linux** — the distribution Microsoft **contributed to the CNCF** (landed as an **incubating project**, he believes the prior year).
- Microsoft is **partnering with the Flatcar team and the CNCF** to make a **productized version** based on the same libraries, for **consistency in the use case**.
- ACL **deviates from Flatcar slightly in terms of where the binaries come from**, purely for **application consistency** (so it matches the rest of Azure Linux).
- **Flatcar is NOT being deprecated.** Jim explicitly debunks the rumor: Microsoft **continues to support Flatcar upstream**, stays heavily engaged with its developer team for new features, and wants it to keep growing. Flatcar and ACL **serve different purposes**. ACL gives customers **product-ready consistency** without disrupting existing Flatcar users' expectations or workflows.
- Practically, ACL **consolidates the two immutable images that were previously in AKS** into a single, usable product customers can interact with.

### Azure Container Linux — the ACL demo (recorded)
A short ACL demo (assembled by **Flora**, with a shout-out; likely to be at KubeCon) repeats the earlier live flow of creating an AKS cluster using Azure Container Linux. It mirrors a standard **Azure CLI cluster create from the command line**: provisions a node, gets credentials, shows status. Highlights shown:
- The node **identifies as Flatcar** — Microsoft is "telling customers exactly what's going on."
- **Kernel 6.6** here (vs 6.18 on Azure Linux 4.0) — again, a preview-period difference; everything aligns at 4.0 GA.
- **Secure Boot** set up and enabled.
- **DM-Verity** configured so images are **verified on boot**; testing confirms a **read-only filesystem**.
- **SELinux enabled by default** — called out as a **key differentiator**. Many in the AKS space currently use **AppArmor**; with Flatcar/ACL it's **SELinux**, so the **AppArmor → SELinux conversion** is the one area the team expects to be **tricky for some customers**.

### Status summary (as stated)
- **Azure Linux 4.0 on WSL** — entering preview (WSL is a **fast follow** for preview after VMs).
- **Azure Linux 4.0 on VMs** — **public preview**.
- **Azure Container Linux** — **now generally available**; it's the **immutable variant of Azure Linux 3.0** for now, moving to 4.0 when 4.0 GAs.

### Q&A — firewalld rules
**Question (from Hayden in the audience):** How are firewall rules handled when packages ship their own?
**Answer (Jim):** Some packages are designed to install their own firewalld rules by default to simplify life for administrators. Some packages in the Azure Linux distribution **will** do that; some **will not**. Wherever Microsoft takes an opinion on this, it will be documented in **two places**: the **product documentation** and the **declarative change state in GitHub**. So for any package taken from upstream, you can see exactly what it was, what select changes Microsoft made, and what the firewall setup includes. (Jim called it a good question.)

### Wrap-up & how to engage
The team is excited to bring a Microsoft Linux distribution out for everyone to use. Ways to engage:
- **Reach out on GitHub** to learn more, get the image, or become a **software-validated partner** on Azure Linux (they'll guide partners through validation, including for Red Hat).
- There's a **community call** and **other resources** to check out.
(A final short ACL video had no audio and was cut for time.)

## 🛠️ Products / Features / Technologies Mentioned
- **Azure Linux** — Microsoft's first-party Linux distribution; the umbrella product (VM + WSL + container surfaces) built on a Fedora upstream.
- **Azure Linux 4.0** — the current generation; kernel 6.18, leaner image, SELinux enforcing by default; VM image in public preview.
- **Azure Container Linux (ACL)** — hardened, immutable variant for containers/AKS; derived from Flatcar; GA at Build (3.0 now, 4.0 at GA).
- **Fedora Linux** — the upstream innovation distribution Azure Linux is built on (same role Fedora plays for RHEL).
- **Red Hat Enterprise Linux (RHEL)** — referenced as the familiar Fedora-derived enterprise distro analogy.
- **Flatcar Container Linux** — immutable container OS contributed by Microsoft to the CNCF (incubating); the upstream basis for ACL; continues to be supported independently.
- **CNCF (Cloud Native Computing Foundation)** — where Flatcar lives as an incubating project.
- **WSL (Windows Subsystem for Linux)** — local developer surface running Azure Linux 4.0; preview is a fast follow.
- **Azure Kubernetes Service (AKS)** — the Kubernetes platform where Azure Container Linux runs as node OS.
- **Azure VMs** — the virtual-machine surface for Azure Linux 4.0 (public preview).
- **Linux kernel 6.18** — latest upstream kernel shipped in Azure Linux 4.0, maintained for the distro's lifetime.
- **Linux kernel 6.6** — the kernel in Azure Container Linux 3.0 during preview (aligns to 6.18 at 4.0 GA).
- **SELinux** — mandatory access control; enabled by default in enforcing mode (key security differentiator vs AppArmor).
- **firewalld** — host firewall enabled out of the box; only SSH open by default.
- **DNF5** — the latest package manager used in Azure Linux 4.0.
- **Azure CLI** — installed via DNF5 in the demo to show speed and repo freshness.
- **Azure Update Manager** — existing Azure management tooling that works with Azure Linux unchanged.
- **Secure Boot** — enabled in Azure Container Linux for boot integrity.
- **DM-Verity** — verifies/validates images on boot; enforces a read-only filesystem in ACL.
- **AppArmor** — the MAC system many AKS users come from; the AppArmor→SELinux conversion is the expected migration friction.
- **DHCPv6 client** — the only reason an extra port (beyond SSH) is open by default, due to IPv6's ICMP address requirement.
- **SSH** — the sole service/port open by default for management.
- **Python** — the language of the demo app; same version across all three surfaces reinforces consistency.
- **GitHub** — where all distribution source and the declarative deviation set live; primary engagement/contact channel.
- **FIPS compliance / FedRamp compliance** — government/security compliance Microsoft layers onto the Fedora base.

## 🚀 Announcements / What's New
- **Azure Container Linux — Generally Available (GA) at Build 2026.** Hardened, immutable Azure Linux image for containers/AKS; derived from Flatcar; currently shipping as **3.0** (kernel 6.6) and will move to **4.0** when Azure Linux 4.0 GAs.
- **Azure Linux 4.0 VM image — Public Preview.** Available to use, test, validate, and provide feedback on; kernel 6.18, SELinux enforcing, DNF5, lean image.
- **Azure Linux 4.0 on WSL — Preview (fast follow).** WSL preview follows the VM preview.
- **Roadmap / consistency commitment:** at **Azure Linux 4.0 GA**, all surfaces (VM, WSL, container/ACL) converge to **4.0** with a consistent kernel (6.18) and binaries across the board.
- **Ongoing Flatcar support (clarification, not a deprecation):** Microsoft continues to support and develop Flatcar Container Linux upstream within the CNCF; ACL is additive, not a replacement.

## 💡 Demos
- **"One OS everywhere" consistency demo (live):** the same Python app (live CPU/memory/uptime refresh) was deployed across **WSL**, an **Azure Linux 4.0 VM**, and an **AKS cluster (Azure Container Linux)**, lighting three columns. **Point proved:** identical app/runtime behavior across all surfaces because they share the same kernel, libraries, and Python — validate once, trust everywhere.
- **Azure Linux 4.0 VM walkthrough (live):** SSH into the VM; verified Azure Linux 4.0, kernel 6.18, SELinux enforcing by default, lean image (declarative deviations / desktop removed), DNF5 installing Azure CLI in seconds, firewalld on with only SSH open, then manually opening a port. **Point proved:** security out of the box + explicit admin control + a minimal, fast, cloud-optimized image.
- **Azure Container Linux / AKS demo (recorded, assembled by Flora):** `az`-style AKS cluster create — provision node, get credentials, show status; node reports as Flatcar, kernel 6.6, Secure Boot enabled, DM-Verity verifying a read-only filesystem on boot, SELinux by default. **Point proved:** ACL is genuinely immutable and hardened with verified boot, and is transparent about its Flatcar lineage.

## 📊 Notable Stats / Quotes
- **Kernel 6.18** in Azure Linux 4.0 (latest upstream), **maintained for the lifetime of the distribution**; **kernel 6.6** in Azure Container Linux 3.0 during preview.
- **DNF5 installed Azure CLI in seconds** during the live demo ("Pretend that was like 2 seconds, not 12.").
- **Only one service open by default: SSH** — "out of the box there are no additional services running beyond SSH."
- *"You can use the same OS everywhere — that's the consistency that Azure Linux brings to you."*
- *"If you validate your application on one, you can have confidence that it will work across all of them."*
- *"That is not true… Flatcar will continue to grow. It continues to exist upstream. We continue to support it upstream."* — Jim, debunking the Flatcar-deprecation rumor.
- *"Security out of the box… I'm repeating it again because it's one of our primary principles with Azure Linux 4.0."* — Porvi.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: Deploy the Azure Linux 4.0 VM image from public preview; install Azure CLI via DNF5; confirm SELinux enforcing + firewalld defaults out of the box. Spin up an AKS cluster on Azure Container Linux (now GA) and inspect Secure Boot / DM-Verity / read-only FS. Run the same containerized app across WSL + VM + AKS to feel the "one OS everywhere" story firsthand.
- [ ] Questions: What's the concrete migration path for existing AKS workloads from AppArmor profiles to SELinux policies? When is Azure Linux 4.0 GA expected (and the 3.0→4.0 / kernel 6.6→6.18 cutover for ACL)? How does the declarative-deviation GitHub manifest map to specific CVE reductions vs stock Fedora? What's the support lifecycle/LTS commitment per 4.x release?
- [ ] Relevant to: AKS node OS standardization; container image hardening & supply-chain (immutable + verified boot); FedRamp/FIPS workloads; dev-to-prod parity using WSL → Azure; any Flatcar users evaluating a productized path.

## 🔗 Related
- [[2026 Build Session List]]
- Topics: #topic/azure-linux #topic/containers #topic/aks #topic/cloud-native #topic/security
- External: [Azure Linux on GitHub](https://github.com/microsoft/azurelinux) · [Flatcar Container Linux (CNCF)](https://www.flatcar.org/) · [AKS documentation](https://learn.microsoft.com/azure/aks/)

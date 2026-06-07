---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/wsl
  - topic/containers
  - topic/windows
  - topic/devtools
source: https://www.youtube.com/watch?v=i0M13ZvL04M
session_code: DEM346
event: Microsoft Build 2026
speakers: Pooja Trivedi, Craig
duration_min: 23
aliases:
  - WSL improvements and the new Containers CLI and APIs
---

# DEM346 — WSL improvements and the new Containers CLI and APIs

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Pooja Trivedi (Architect, developer experiences in AI for Linux on Windows) · Craig (Product Manager, Windows Subsystem for Linux & AI tools on Windows)  
> **Duration:** ~23 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=i0M13ZvL04M)

## 🎯 TL;DR
Microsoft is shipping **WSL containers** — the ability to run Linux containers locally on Windows, delivered as a built-in part of the Windows Subsystem for Linux (no third-party tools, no daemons to start). It exposes two front doors over the same engine: a **`WSLc` command-line tool** (also aliased to `container`) whose syntax closely mirrors standard Linux container CLIs, and a **.NET API** shipped as a **NuGet package** that lets Windows applications create and manage Linux containers transparently. Containers can map ports to `localhost`, mount Windows volumes, and tap the host **GPU** for AI workloads. Under the hood, every app (and the CLI) gets its own isolated lightweight utility VM with a hypervisor security boundary, running the **Moby** runtime, communicating via **HV sockets** and sharing files over **VirtIOFS** (~2× faster than the older Plan 9 protocol). It's built to be **enterprise-ready** (Intune, MDE work against it), fully **open source**, and targets **public preview by end of June**.

## 🔑 Key Takeaways
- **WSL containers** lets you run **Linux containers locally on Windows**, both via a CLI and via an API embedded in Windows apps.
- It ships **as part of WSL** — you get it via a simple `wsl --update`; **no new install, no third-party tools, no daemons** ("no fasting rituals").
- The CLI tool is **`WSLc`**, internally **aliased to `container`**; its subcommands, options and switches **track closely to standard Linux container tooling** (familiar to Docker/Podman users).
- Common flows demoed: `run -it` an interactive Debian container, detach with **Ctrl-P Ctrl-Q**, list with `ps -a` / `container list`, `attach`, `build` custom images from a **container file**, `images`, and **port mapping** with `-p`.
- Containers can **expose services to the Windows host** — e.g. a web server on port 5000 reached via `127.0.0.1`/localhost.
- Containers can **mount Windows directories** as volumes (`-v`) and **access the host GPU** (`--gpus all`) for AI / graphical / compute scenarios.
- The **API** is a **NuGet package**; container build is integrated into the **`.csproj`** (item group) for a single **F5 / one-build** experience — the container file lives alongside app source.
- Both CLI and API are **"two doors for the same engine"**, all powered by the same **WSL VM** technology that powers WSL distributions.
- **Architecture:** each Windows app (and the CLI flow) gets its **own dedicated lightweight utility VM** → **hypervisor boundary per app**, with isolated names, volumes, networks, storage (per-app **VHD**) — no conflicts.
- Inside each VM runs the **Moby** container runtime (the open-source engine that powers Docker). **WSL service** (the same service that manages distros today) was augmented to manage containers and relay info to the host via an **HV socket** (a specialized point-to-point WinSock extension, not a network socket).
- **Storage** (`/var/lib/...` container metadata/scratch) is mapped to a **per-app VHD** on Windows; volume mounts use **VirtIOFS** (a newer VM↔host file-sharing protocol, **~2× faster than Plan 9** used by WSL today).
- **Enterprise-ready:** industry-standard tools like **MDE and Intune just work**; admins get strong VM isolation without an opaque "black box" they can't inspect or secure.
- Three target audiences: **container developers**, **app builders / ISVs** (embed Linux code in Windows apps), and **enterprise IT admins**.
- Microsoft built its **own** Linux container CLI (rather than reusing Docker/Podman/Rancher) to be **opinionated** and make the CLI + API work together — but **those other tools still work great** and benefit from the same underlying improvements.
- It's **fully open source on WSL**; underlying VM improvements (e.g. **cross-OS file performance**) **accrue to Docker Desktop, Rancher Desktop, Podman Desktop** too.
- Separately announced: **Azure Linux 4.0 is now generally available** (the same distro that runs AKS / powers Azure); WSL distro version **coming soon**.
- **Timeline: public preview by the end of June**; progress is open at **microsoft.com/wsl** and announcements will post on the **CLI blog**.

## 📚 Detailed Notes

### What WSL containers is (the three core points)
Craig framed the whole talk around three takeaways:
1. **Run Linux containers locally on Windows** — either directly via a CLI, or via an API used from within Windows applications.
2. **It's part of the Windows Subsystem for Linux** — a new feature you get directly as part of WSL. No need to install anything new; it's part of an existing package users likely already have.
3. **Enterprise-ready** — industry-standard tooling (MDE, Intune, and more) "just works" with WSL containers, so it's safe/secure to use inside enterprise environments.

Delivery is via a simple **WSL update** — no third-party tools to download, no daemons to start ("no fasting rituals").

### The CLI: `WSLc` (aka `container`)
- The command-line tool is **`WSLc`**, and Microsoft has **internally aliased it to `container`**, so users comfortable with a `container` binary can use that name instead.
- Pooja showed the **command reference**: subcommands, options and switches **track very closely to standard Linux container tools**, so it feels immediately familiar.
- **Simple interactive flow (Debian):**
  - `WSLc run -it debian` → the `-it` switch gives an **interactive shell** into a Debian Linux container. Normally the image is **auto-downloaded from a public registry** if not present locally (in the demo it was pre-downloaded due to venue internet issues).
  - **Detach** from a running container with the standard **Ctrl-P Ctrl-Q** sequence.
  - `WSLc ps -a` (or `WSLc container list`) lists containers and their state (e.g. "started about 40 seconds ago").
  - `WSLc attach <id|name>` re-attaches to the running container.
  - `exit` terminates the container; `WSLc ps -a` then shows it as **"exited"**.

### Building custom images
- Use case: **bring cloud/production workloads onto your primary Windows dev box** to iterate, test, and debug locally. Because the workload is packaged as a container, you get the **same environment as production**, avoiding "works in dev, doesn't work in prod."
- A **container file** holds all the "ingredients and the recipe" — environment, dependencies, application logic, and run instructions — used to build a container image.
- Demo container file (a "Linux spy" forensics utility that runs Linux inspection commands on any file dropped to it):
  - Starts **`FROM` a lightweight Python 3.12 base image**.
  - Installs dependencies needed for the container/app.
  - **Copies** application logic into the container.
  - It's a **web server listening on port 5000**, so the file **exposes** that port to map onto the Windows host.
  - Final line is the **start/run instruction** for the app.
- Build: `WSLc build` → named **`my-linux-spy`**, using the container file.
- `WSLc images` lists images. (Aside: you **can `grep` in PowerShell** because Microsoft imported **~168 core Linux utils into Windows**, fully integrated — "shameless plug.") Image showed "9 hours ago" because **base-layer caching** was reused.
- Run with **port mapping**: `WSLc run ... -p 5000:5000` maps the container's port 5000 to the Windows host; the web server is then reachable at **`127.0.0.1` / localhost**.

### GPU access for AI / graphical workloads
- Containers can **tap the GPU present on the Windows host** for AI scenarios, graphical apps, etc.
- Demo "AI container" (pre-built and pre-warmed to save time): a **Jupyter notebook web server** on **port 8888** (exposed via port mapping). It:
  - Pulls down a **GPT-2 model**.
  - **Fine-tunes it on the host GPU**.
  - **`torch.compile`s** it to generate **fused Triton kernels** (optimized kernels that make the model run much faster on the GPU).
  - Runs a **head-to-head race** between the compiled model and its **uncompiled eager-mode** counterpart to show the speedup.
- The launch command combined three switches:
  - **`run -it`** (interactive),
  - **`-p`** (port mapping),
  - **`-v`** to **mount a volume** — mounting the host's **Hugging Face (HF) cache** directory into the container,
  - **`--gpus all`** to grant the Linux container access to the **host GPU**.

### Two ways to interact: CLI vs API
- **CLI** — perfect for **direct container access, building, and running** (what Pooja demoed).
- **API** — shipped as a **NuGet package** Windows apps can reference to create/manage containers programmatically.
- "**Two different doors for the same engine**" — both powered by the **same WSL VM** that powers WSL distributions.

### Why Microsoft built this (three customer profiles)
1. **Container developers** — make it easier to get started with and use containers, running seamlessly on Windows. Microsoft wanted to be **opinionated**: because they're building **both an API and a CLI** that should work together (with some custom commands), they built **their own Linux container CLI** rather than reusing Docker, Podman, or Rancher Desktop. Those tools **still work great** and remain valid choices — this is just another approach.
2. **App builders / ISVs** — take existing Linux code (local or in the cloud) and run it **directly and locally as part of a Windows application** using standard, powerful APIs.
3. **Enterprise IT admins** — run containerized Linux apps (e.g. "run OpenClaw in a containerized Linux environment") while **managing them with familiar Windows tools (Intune, MDE)**. The goal is **powerful isolation** without admins fearing an **opaque "black box" VM** their security tools can't inspect or break into.

### Open source & shared benefit
- The work is **fully open source on WSL**. Improvements to the **underlying VM technology accrue to other container tech** too.
- Example: improving **cross-OS file performance** benefits **Docker Desktop, Rancher Desktop, Podman Desktop** — as well as the Linux container CLI inside WSL.

### Architecture (how it works)
- **Per-app isolation:** every Windows app intending to create Linux containers gets a **dedicated lightweight utility VM** created in the background. All of that app's Linux containers are **co-located on its VM**. The **CLI flow also gets its own VM**.
  - This yields a **hypervisor boundary per app**, **resource separation**, and **no conflicts** — each app's container names, volumes, and networks are **isolated on a per-VM basis**.
- **Two entry points** into the WSL containers world:
  - The **API**, exposed by a library published as a **NuGet package** that Windows apps include.
  - The **`WSLc` / `container` executable** (the CLI demoed earlier).
- Both **talk to WSL service via inter-process communication (IPC)**. **WSL service already exists today**; its job is managing WSL distros, the **lifecycle of the WSL VM**, and host↔VM communication. It was **augmented to also manage the containers** inside these VMs and relay information between containers and Windows-host users.
- Inside each Linux VM runs a **container runtime — Moby** (the open-source engine that powers Docker today).
- **WSL service uses an HV socket** to communicate user intent to the container runtime. An HV socket is **not a network socket** — it's a **specialized WinSock API extension**, a **point-to-point per-VM channel to the hypervisor**, giving each VM an **isolated communication channel**.
- When a user issues a create command, the **container runtime creates the containers** and WSL service relays information back and forth.

### Storage & file sharing
- The container runtime in each VM uses a **central directory** (e.g. `/var/lib/...`) for **container metadata, scratch space, etc.**
- That location is **mapped onto a virtual disk (VHD) on the Windows host**, and **every app (and the CLI flow) gets its own VHD** → **per-app storage separation**.
- **Volume mount flow example:** `run -it -v C:\data:/data debian:latest`
  - Maps the Windows **`C:\data`** directory onto the container's **`/data`** mount and creates a **`debian:latest`** container.
  - Under the hood the `/data` volume is mapped to `C:\data` using **VirtIOFS** — a **relatively new file-sharing protocol** for VM↔hypervisor file sharing.
  - Added complexity: **translating filesystem semantics between two different OSes** (Windows ↔ Linux).
  - **VirtIOFS is ~2× faster** than **Plan 9** (the protocol WSL uses today); Microsoft is investing further and evaluating alternatives to make it faster still.

### What else is new for WSL: Azure Linux 4.0
- **Azure Linux 4.0 is now generally available** for general use.
- It's the **same distro that runs AKS today** and **powers Azure** → a **consistent, battle-tested, proven** environment.
- **Microsoft provides the entire stack** (single vendor) with **full supply-chain attestation from build to deployment** — clear support ownership.
- **Available today for VMs**; the **WSL distro version is coming soon**. It is **container-optimized and lightweight** — Microsoft asks users to try it as a WSL distro and give feedback.

### Wrap-up / availability
- Microsoft will **post on the CLI blog** when WSL containers goes live and asks users to **try real-world scenarios and give feedback**.
- **Public preview targeted by the end of June.**
- It's **open source** — progress visible at **microsoft.com/wsl**.
- The **MoonRay dev lead** was also available for questions at the session.

## 🛠️ Products / Features / Technologies Mentioned
- **WSL (Windows Subsystem for Linux)** — host platform; WSL containers ship as part of it via `wsl --update`.
- **WSL containers** — the new feature for running Linux containers locally on Windows.
- **`WSLc` CLI** (aliased to **`container`**) — the new Linux container command-line tool.
- **WSL containers API** — a **.NET / NuGet package** for embedding container management into Windows apps.
- **WSL service** — existing host service, augmented to manage container lifecycle and host↔VM relay.
- **Moby** — open-source container runtime (powers Docker) run inside each VM.
- **HV socket** — specialized point-to-point WinSock extension for VM↔hypervisor comms (not a network socket).
- **VirtIOFS** — newer VM↔host file-sharing protocol (~2× faster than Plan 9).
- **Plan 9 (9P)** — the file-sharing protocol WSL uses today (being superseded by VirtIOFS for containers).
- **VHD (virtual hard disk)** — per-app/per-CLI storage backing for container data.
- **Windows core utils** — ~168 Linux utilities (e.g. `grep`) integrated into Windows.
- **Debian, Python 3.12** — base images used in demos.
- **GPU passthrough** (`--gpus all`), **port mapping** (`-p`), **volume mount** (`-v`).
- **PyTorch `torch.compile`, Triton (fused kernels), GPT-2, Jupyter notebook, Hugging Face cache** — AI demo stack.
- **`.csproj` integration** — container build wired into MSBuild item group for an F5 experience.
- **Azure Linux 4.0** — Microsoft's Linux distro, now GA; same distro that runs AKS.
- **AKS (Azure Kubernetes Service)** — referenced as running on Azure Linux.
- **MoonRay** — open-source rendering engine (DreamWorks) used in the API demo.
- **Intune, Microsoft Defender for Endpoint (MDE)** — enterprise management/security tooling that works with WSL containers.
- Comparison tools (still supported): **Docker / Docker Desktop, Podman / Podman Desktop, Rancher Desktop**.

## 🚀 Announcements / What's New
- **WSL containers** — new feature to run Linux containers locally on Windows, delivered as part of WSL (CLI + API). **Status: public preview targeted by the end of June** (not GA at session time).
- **`WSLc` CLI** (aliased `container`) — new first-party Linux container CLI for WSL. **Preview (with WSL containers).**
- **WSL containers API** — new **NuGet package** for embedding Linux container management in Windows apps, with **`.csproj`-integrated build / F5 experience**. **Preview (with WSL containers).**
- **VirtIOFS adopted** for container volume sharing — **~2× faster than Plan 9**, with further perf work planned. Cross-OS file-performance gains also flow to Docker/Rancher/Podman Desktop.
- **Azure Linux 4.0 — Generally Available** (the distro that runs AKS / powers Azure). **Available today for VMs; WSL distro version coming soon.**
- **Fully open source** — code and progress at **microsoft.com/wsl**; announcements via the **CLI blog**.

## 💡 Demos
1. **Basic CLI flow (Debian):** `run -it` into an interactive Debian shell, detach with Ctrl-P Ctrl-Q, `ps -a` / `container list`, `attach <id|name>`, then `exit`/terminate (shown as "exited").
2. **Build & run a custom image ("Linux spy" forensics web app):** authored a container file (`FROM python:3.12`, install deps, copy app, expose port 5000, run instruction); `WSLc build` → `my-linux-spy`; `WSLc images` (with `grep` in PowerShell); `run -p 5000:5000`; interacted with the web server at `127.0.0.1`.
3. **GPU-accelerated AI container:** Jupyter notebook server on port 8888; pulls GPT-2, fine-tunes on the host GPU, `torch.compile` → fused Triton kernels, then a compiled-vs-eager speed race. Launched with `run -it -p ... -v <HF cache>:... --gpus all`.
4. **API demo #1 — MoonRay rendering as a "Windows app":** ran `moonray.exe` (a Linux rendering engine) on Windows with backslash paths, fed `.rdl`/render input files, output a **JPEG** (an orange coffee maker via ray tracing). Task Manager showed the render running on CPU inside a transient MoonRay VM that **spun up and released back to Windows** seamlessly — looked like a native Windows app; user would be "none the wiser" Linux was involved.
5. **API demo #2 — embedded container in a .NET app ("Herbert" stock-trading agent):** NuGet `containers` package + `.csproj` item group pointing at the container file (co-located with source); single F5 builds + runs the container. A whimsical AI agent ("Herbert") makes fake stock trades on a container-provided desktop (visualized via an exposed port). It also **randomly deletes files** — but file access was **scoped to `C:\temp\Herbert`**, demonstrating **deep but bounded Windows↔container integration** (explicit ports + restricted file access → minimized blast radius).

## 📊 Notable Stats / Quotes
- **~168** Linux core utilities now integrated into Windows.
- **VirtIOFS ≈ 2×** the speed of Plan 9 in this environment today.
- **One VM per app + per CLI flow** → **hypervisor boundary per app**; per-app isolation of names, volumes, networks, **and storage (per-app VHD)**.
- Ports used in demos: **5000** (Linux spy web server), **8888** (Jupyter), volume mount example `C:\data → /data`.
- **"Two different doors for the same engine."** — Craig, on CLI vs API.
- **"No need to download any third-party tools, no starting of daemons, no fasting rituals."** — Pooja, on the zero-install update.
- **"It works in dev, doesn't work in prod"** — the production-parity gotcha WSL containers aims to eliminate.
- **"Public preview by the end of June."** — Craig, on availability.
- MoonRay powers films like **The Bad Guys 2** and **The Wild Robot**.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - `wsl --update`, then `WSLc run -it debian` and the `ps -a` / `attach` / `exit` loop once preview lands.
  - Build a custom image from a container file (`WSLc build`) and port-map a local web service to `localhost`.
  - Test **GPU passthrough** (`--gpus all`) + Hugging Face cache volume for a local AI fine-tune.
  - Add the **containers NuGet package** to a `.csproj`, wire the container build item group, and try the **F5** experience.
  - Try **Azure Linux 4.0** on a VM now; watch for the WSL distro drop.
- [ ] Questions:
  - Confirm exact NuGet package name and CLI binary name at preview (transcript captions garbled the library name).
  - How does per-app VM creation affect cold-start latency and memory footprint at scale (many apps)?
  - Image registry/auth story for enterprise (private registries, signing, supply-chain) with `WSLc`?
  - Networking model between containers in the same VM vs across app VMs (isolation vs intentional comms)?
  - How do Intune/MDE policies actually attach to these per-app utility VMs in practice?
  - Will image build caching/layers be shared across app VMs, or duplicated per-VHD?
- [ ] Relevant to:
  - Local dev of Linux/cloud workloads on Windows boxes (prod-parity, no Docker Desktop dependency).
  - Windows apps/ISVs wanting to embed Linux engines (rendering, AI, services) transparently.
  - Enterprise IT evaluating containerized Linux on Windows under existing Intune/MDE governance.
  - Local AI experimentation needing GPU + Hugging Face cache inside isolated containers.

## 🔗 Related
- [[BRK261 - Build and ship faster with a developer-optimized experience on Windows]]
- [[WSL (Windows Subsystem for Linux)]]
- [[Containers]]
- [[Azure Linux]]
- [[Docker]]
- [[Azure Kubernetes Service (AKS)]]
- [[Microsoft Build 2026]]
- Source list: [[2026 Build Session List]]

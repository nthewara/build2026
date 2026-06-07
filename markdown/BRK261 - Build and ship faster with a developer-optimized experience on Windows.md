---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/windows
  - topic/developer-experience
  - topic/devtools
  - topic/wsl
  - topic/performance
source: https://www.youtube.com/watch?v=V6mdr7Lw1TA
session_code: BRK261
event: Microsoft Build 2026
speakers: Kayla Cinnamon, Craig (WSL PM), Gier (Windows Performance) [caption-uncertain], Clint
duration_min: 42
aliases:
  - Build and ship faster with a developer-optimized experience on Windows
---

# BRK261 — Build and ship faster with a developer-optimized experience on Windows

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Kayla Cinnamon (PM, Windows developer utilities — Terminal, PowerToys, winget, WSL); Craig (PM, Windows Subsystem for Linux & AI tools on Windows); Gier (Windows performance) *[name caption-uncertain — also called "Gin"/"Gingier" in captions]*; Clint (4th speaker, assisting/timing demos)  
> **Duration:** ~42 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=V6mdr7Lw1TA)

## 🎯 TL;DR
The Windows developer-tools team (Terminal, PowerToys, winget, WSL) walks through a fast, minimal-slides tour of everything that makes Windows a better place to build and ship apps in 2026, split into **building *on* Windows** (your dev environment) and **building *for* Windows** (shipping WinUI apps). On the environment side they ship a one-command **Windows developer config** (a winget configuration file that installs WSL + Ubuntu + git/gh/Copilot CLI/VS Code idempotently), a **movable/vertical taskbar**, a **new Run dialog** built on the open-source **PowerToys Command Palette** architecture, an experimental **Intelligent Terminal** agent companion pane, brand-new **WSL containers** via the `wslc`/`container` CLI, GNU **core utils** ported natively to Windows (165 tools), and a pre-configured **comfort shell** Ubuntu flavour. For shipping apps they introduce the **WinApp CLI** (one tool for SDKs, packaging, identity, manifests, certs), the **winddev skills** agent plugin for building WinUI 3 / Windows App SDK apps with up-to-date context, a new **WSL Containers API** (NuGet package, runs Linux containers inside a Windows app's own WSL VM), and **Sample-based Profile Guided Optimization (SPGO)** which delivered up to **20% real-workflow gains for Adobe Photoshop** and ~33% in the demo — all friction-free using hardware counters instead of instrumented builds. The unifying theme: nearly everything (except Windows itself) is open source, with 16,000+ contributors thanked.

## 🔑 Key Takeaways
- **Windows developer config** is a public, idempotent **winget configuration file** (repo: `Windows developer config`, made public the morning of the talk) that bootstraps a dev box: installs WSL + Ubuntu plus git, GitHub CLI, Copilot CLI, VS Code and more — re-running won't reinstall tools you already have.
- **Movable/vertical taskbar is back** — pin the taskbar left, top, or bottom; a long-requested feature, currently in the **Windows Insider** program and shipping.
- The **new Run dialog** is rebuilt on the **PowerToys Command Palette** architecture (the successor to PowerToys Run), so community code contributed to Command Palette now ships inside Windows itself.
- **Intelligent Terminal** (experimental, open source, published the morning of the talk) gives you an **agent companion pane** in the terminal — the agent helps alongside your prompt instead of taking over the whole terminal like a full CLI agent does.
- Intelligent Terminal is **agent-agnostic**: it auto-detects whichever agents you have installed (GitHub Copilot, Claude, Codex, open code, etc.) and lets you pick your preferred model.
- **WSL containers** are brand new (announced that morning): a new `wslc` binary (aliased as `container`) runs Linux containers natively as part of WSL — pull/run distros (Ubuntu, Debian), build images from container files, port-forward into Windows, all from the terminal.
- WSL containers ship **both a CLI and an API** — Microsoft built their own opinionated CLI (e.g. a `system session` command that doesn't exist in Docker/Podman) specifically so the CLI and API stay aligned.
- WSL container improvements flow **upstream for free** to Docker Desktop, Podman Desktop and Rancher Desktop because the underlying VM tech is shared and open source — including a **2× cross-OS file performance** improvement for accessing Windows files from Linux.
- **Core utils**: ~165 GNU core utilities (the repo highlights ~75) are now available **natively on Windows** (`grep`, `tail`, `test`, `env`, `wc`, etc. as `.exe`), so you can pipe Linux-style commands directly in your Windows shell.
- **Comfort shell** (bundled in the Windows developer config) is a pre-configured Ubuntu setup script that ships Homebrew, zsh, Starship, **btop** and other favourites pre-installed, plugging straight into your Ubuntu distro.
- **WinApp CLI** (open source, on winget) is a **single CLI** for managing Windows SDKs, packaging, generating app identity, manifests, certificates and build tools — it handles the hard parts like publishing and unlocking **package identity** (native notifications, Explorer/taskbar/share-sheet integration).
- **winddev skills** is an **agent plugin** (bundle of skills + MCP servers + custom agents) for building **WinUI 3 / Windows App SDK** apps — ships skills for build/run workflow, WinUI design, code review, testing, packaging, WPF migration, and setup.
- The winddev plugin gives agents **up-to-date WinUI knowledge directly**, so the agent doesn't waste tokens on stale web searches — a real token-efficiency win.
- The **WSL Containers API** (a WSL containers NuGet package) lets a **C#/.NET app embed Linux containers**: defined in the `.csproj`, the container builds automatically as part of `dotnet build`/`dotnet run` — each Windows app gets **its own WSL VM** and can run many containers inside it.
- A WSL-container-backed app **looks and behaves like a native Windows app** — cold-start container init benchmarked at **~2.5 seconds**, with full resource cleanup (VM disappears) when the app closes; supports volume mounts (specific Windows folders) and **GPU access**.
- **SPGO (Sample-based Profile Guided Optimization)** removes the friction of classic PGO: instead of instrumented builds, it uses **lightweight hardware counters** on a normal **release build** captured via `xperf`/ETL traces — same perf wins, no extra build fork, no slow instrumented run.
- SPGO is **real and shipping value**: **Adobe Photoshop saw up to 20%** improvement on real CPU-bound workflows (releasing the optimized build to the public "in the coming days"); the live Fibonacci VM demo went **3s → 2s (~33%)**; ISVs report **5–15%** typical gains.
- SPGO is meant to be **iterative, not one-shot** — re-capture profiles as your code or your users' usage patterns change, and fold it into your existing **build pipeline** (it's non-intrusive — no instrumented fork).
- **Everything but Windows itself is open source** — the team thanked **16,000+ open-source contributors** across Terminal, WSL, WinUI and PowerToys (a contributors file 16,000 lines long).
- Bonus PowerToys utility shown: **grab-and-move** — hold **Alt** and click anywhere to drag a window, even when the title bar is hidden behind a wall of browser tabs.

## 📚 Detailed Notes

### Framing: two halves — building *on* Windows vs building *for* Windows
The team that owns a big chunk of Windows developer utilities (Windows itself, **PowerToys**, **Windows Terminal**, **winget** the Windows package manager, and **WSL** the Windows Subsystem for Linux) ran a deliberately minimal-slides, demo-heavy session ("that's our jam"). They split the talk into two parts:
- **Building *on* Windows** — improvements to Windows itself that make it a better machine to *do your development on* (environment setup, terminal, taskbar, WSL containers, core utils, comfort shell).
- **Building *for* Windows** — everything they've created to make *shipping Windows apps* (WinUI / Windows App SDK apps) more seamless (WinApp CLI, winddev skills agent plugin, SPGO performance optimization, WSL Containers API).

Most of what's shown was also in the Build 2026 keynote that morning; this session goes deeper. A recurring meta-point: almost everything except Windows itself is **open source on GitHub**.

### Developer setup pain → the Windows developer config (winget config file)
The problem: setting up a fresh Windows dev box is slow — you have to go grab Python, Node, all your packages and favourite tooling one at a time. The team's answer is a **winget configuration file** that automates this. It installs:
- **Ubuntu** along with **WSL** (Windows Subsystem for Linux)
- core tooling: **git**, **GitHub CLI (`gh`)**, **Copilot CLI**, **VS Code**, and more.

Key property: winget configuration files are **idempotent**. If you already have git (as most do), it won't reinstall — it just verifies git is present and moves on to the next item. You can download the config first to see exactly what it will install, then run it.

**Repo:** `Windows developer config` — published and made **public the morning of the talk**. Several other things shown in the session (comfort shell, etc.) also live in this repo. A final slide collects all the links.

### Movable / vertical taskbar (Insider)
A long-requested, popular feature is **back**: you can move the Windows taskbar to the **left**, **top**, or keep it on the **bottom** (where it's always been). Currently available in the **Windows Insider** program and shipping. (Kayla noted she keeps hers on the bottom out of habit so she doesn't "lose her icons.")

### The new Run dialog (built on PowerToys Command Palette)
The classic **Run** dialog gets a refreshed, **more streamlined UI**. The interesting part is *how* it's built: it leverages the architecture of **PowerToys Command Palette**. The lineage shown on screen:
1. **PowerToys Run** — the original launcher.
2. **Command Palette** — the evolution: more extensibility (you can install things into it), more capability, a redesigned UI based on feedback.
3. **New Run** — now uses the **Command Palette architecture** inside Windows itself; you can search for tooling and it looks much like Command Palette (just inverted).

The open-source payoff: because Command Palette is open source in PowerToys, **if you contributed to Command Palette, there's a good chance your code now ships inside Windows.**

### Intelligent Terminal — an agentic *companion pane* (experimental, open source)
Motivation: when you launch a full CLI agent (e.g. Copilot CLI), it **takes over your whole terminal**. It would be nicer to have a **companion** working alongside you so you can **stay in your own prompt** while an agent helps in parallel.

**Intelligent Terminal** is that experiment — an **agentic pane** in the terminal. Demo walkthrough:
- The presenter had an agent write a **regex** ("regex" — captions said "reax") for password verification, and deliberately asked it to make the regex *not work*.
- The agent **detected** that the regex doesn't work and started reasoning about how to fix it.
- Crucially, it **doesn't just hand back a command**, because it doesn't know the desired outcome (check for an uppercase letter? a unique character?). You **collaborate with the agent** to converge on a better regex — **without leaving the terminal**.

Setup behaviour: on first run, Intelligent Terminal asks **which agent you want to work with**. It's **agent-agnostic** — the presenter only had GitHub Copilot installed, but you can add **Claude, Codex, open code**, etc. Once installed on your machine, an agent is **auto-detected**; you can also pick your **preferred model**.

Status: **available today**, **open source on GitHub**, published the morning of the talk. The team explicitly wants feedback on how the agentic pane *feels* to work with and what to add.

### WSL containers — native Linux containers in WSL via the `wslc` / `container` CLI
Craig took over to show **WSL containers**, also **freshly announced that morning**. His stated goal: convince anyone who's never used containers *why* they'd want to, and show how to do it with WSL containers.

- A new binary, **`wslc`**, was added to WSL. It runs lots of standard Linux container commands. (`container` is a built-in **alias** — use whichever you prefer.)
- A Linux container is "a very nice little package" to run arbitrary Linux binaries or distributions. Running `wslc` pulled and ran the **latest Ubuntu**; asking for **Debian** pulled it down (even though it wasn't downloaded) and ran it — **directly inside the terminal**.
- The power: build **powerful Linux environments** you can **share to the cloud or run locally**, all working **directly as part of WSL**.

**Building an image from a container file:** Craig had a `container` folder with container files and **built an image** for a *service* directly in the terminal (cached from a prior run). He opened the container file with **`edit`** — the new command-line editor — praising that it **works with the mouse**. The container file grabbed **Python 3.13** and ran a series of Linux commands to set up a specific environment.

**Listing + piping with core utils:** He ran `wslc image ls` and piped it through `grep` and rendered markdown. The piping works because of the newly released **core utils** (see below). Piping the list to `wc` (word count) showed **165 tools** available; examples named: `test.exe`, `tail.exe`, and `env.exe` (he was "personally really excited" about `env.exe` since he only knew how to print env vars in bash). The point: Windows and Linux worlds can **coexist nicely**.

**Running the service + port forwarding:** He started the **markdown service** container he'd built, using **`-p`** to forward **port 8000** from the container onto Windows. Opening **`localhost:8000`** in Edge showed the container's web app: a small app that takes **any file** (PDF, `.docx`, etc.), converts it to **markdown**, and shows source on the left and markdown on the right. "That could be my full website, contained right there."

**Fun + the real reason for a custom CLI:** Containers can do silly things too — e.g. "light your whole terminal on fire" with a single command someone built. That raised the question: *why build a Linux container CLI when Podman Desktop, Docker Desktop and Rancher Desktop exist?* The answer: those are great tools, but Microsoft also built an **API** for this (shown in part two), and wanted to be **opinionated** about how the CLI and API work together. Example: they added a **`system session`** command that **doesn't exist in Docker or Podman**, to keep the API and CLI aligned. That deliberate decision is why they made their own CLI.

**Open source + upstream benefits:** It's **all open source**, with many improvements coming to the **underlying virtual machine technology**. Those improvements flow **to Docker, Podman and Rancher for free** — e.g. **cross-OS file performance improved by 2×** when accessing **Windows files from Linux**.

### Core utils — GNU core utilities running natively on Windows
While Craig spoke, Kayla pulled up the **core utils** repo: ~**75** command utilities (165 tools total counted in Craig's demo) available **natively on Windows** as `.exe` (e.g. `grep`, `tail`, `test`, `env`, `wc`). Grab them from the repo to get all those utilities immediately — it lets you pipe Linux-style command chains directly in your Windows shell.

### Comfort shell — a pre-configured Ubuntu flavour (in the developer config)
Also bundled in the **Windows developer config** is the **comfort shell** — described as a customized **implementation/setup script** for Ubuntu. It comes with familiar tools **pre-installed**: **Homebrew**, **zsh**, **Starship**, and more, plugging straight into your Ubuntu distro. Kayla's favourite demo of it (also shown at the keynote): **btop** baked in.

### Recap of "building *on* Windows"
Kayla recapped the first half:
1. **Optimize your setup** with the **config file** (GitHub repo) — fan-favourite tooling, idempotent.
2. **Intelligent Terminal** — experimental agent companion in the terminal.
3. **Windows improvements** — **new Run** (PowerToys Command Palette architecture) + **vertical taskbar**.
4. **Core utils** — Linux core utilities native on Windows.
5. **WSL containers** — native container solution that works with your existing container files.
6. **Comfort shell** — pre-configured Ubuntu with btop and friends.

### WinApp CLI — one CLI to build & ship WinUI apps
Moving to **building *for* Windows** (shipping WinUI / Windows App SDK apps), the team introduced the **WinApp CLI** (open source, on winget). It's a **single command-line interface** for managing:
- **Windows SDKs**
- **packaging**
- generating **app identity**, **manifests**, **certificates**
- **build tools**

Use it to jump-start building Windows apps and cover the hard parts like **publishing**. A highlighted benefit: it makes it easy to give your app **package identity**, which unlocks **interactive native notifications**, plus integration with **Explorer**, the **taskbar**, and the **share sheet**. It ships with getting-started instructions and (of course) installs via **winget** in a one-line install ("everything we make goes on winget").

### winddev skills — an agent plugin for WinUI 3 / Windows App SDK
Leveraging WinApp CLI, the team shipped **winddev skills** — an **agent plugin**. A plugin here is just a **bundle** of the things agents already understand: **skills**, **MCP servers**, and **custom agents**, packaged into one installer. winddev skills is for building **WinUI 3** and **Windows App SDK** apps and includes skills for:
- build & run **workflow**
- **WinUI design**
- **WinUI code review**
- **testing**
- **packaging**
- **migrating from WPF** (session report)
- **WinUI setup**

Key value (Craig's point): the plugin gives the agent **up-to-date WinUI information directly**, so it **doesn't waste tokens on web searches** and doesn't rely on stale training data. Providing that context up front is far more **token-efficient** than asking an agent to research WinUI 3 from scratch. Install was done by pasting a **long prompt** into Copilot (you can also do it by hand).

### Live demo: building a WinUI 3 markdown app with Copilot CLI + winddev
Kayla attempted a live build of a WinUI 3 version of Craig's "Mark It Down" app:
1. In **Copilot CLI**, with the winddev plugin already installed (via the long prompt), she **set the custom agent to `WinUI dev`** — this routes requests to the WinUI / Windows App SDK skills. Seeing `WinUI dev` as the active custom agent confirms you're "in the right place."
2. She used Copilot CLI's **voice feature** to dictate the prompt on stage: *build a native WinUI 3 app that takes any file and converts it to markdown, with a side-by-side view showing both files, "make it look prettier than Craig's,"* then **do UI testing and run it**.
3. She switched to **autopilot mode** (via **Shift+Tab** — modes are *plan*, *autopilot*, *regular*) and enabled all permissions to kick it off.

The plugin's bundled **UI testing** skill means the agent knows how to **build, deploy, then UI-test** the app automatically (mouse bouncing around, clicking buttons, checking text boxes). She'd done a similar build beforehand with a slightly different prompt and it **worked on the first try**, producing a genuine WinUI 3 app with modern WinUI 3 components — text box, a "browse file" button, etc. Later in the session she confirmed the live app **did build, ran all the UI testing, and finished**.

### Bonus: PowerToys grab-and-move
Kayla "shoehorned in" a new **PowerToys** utility she loves: **grab-and-move**. With dozens of browser tabs open you often can't reach the **taskbar or title bar** to drag a window. Grab-and-move lets you **hold Alt and click anywhere** to drag the whole window around — a small but handy quality-of-life win.

### SPGO — Sample-based Profile Guided Optimization (Gier)
Gier (Windows performance) presented **SPGO**, framed as a rethink of classic **Profile Guided Optimization (PGO)**.

**What PGO is:** collect data on the actual executable running — sampling which code paths/branches get executed — and feed that into the **compiler**, so it does a better job optimizing when emitting the final binary. PGO delivers **real** wins (reported **5–10%**), *but* its costs hinder ISV adoption:
1. It requires **instrumentation** — extra code injected into your app.
2. It adds an **extra fork in your build pipeline** — not everyone wants extra steps mucking with their build.
3. The **instrumented build runs very slowly**, so it **doesn't mimic** what the end user actually experiences — making the **quality of the collected profile questionable**.

**How SPGO fixes it:** instead of code instrumentation, SPGO uses **hardware counters** — very lightweight. You can run your normal **release build** and use **hardware counters to collect the profile**, getting the **same performance benefit without the friction**. Real impact: working with the **Adobe Photoshop** team, they saw **up to 20%** improvement on real, CPU-bound workflows.

**End-to-end SPGO walkthrough (live demo):** Gier used a sample **stack-based virtual machine computing the Fibonacci series** (full sample code to be published in the repo). He drew attention to the VM's **switch on the opcode** — it jumps based on each operator; in a stack VM a lot of branching is **highly predictable** while some branches are rarely used, which is exactly where PGO/SPGO excels at optimizing.

The steps (Clint timed the runs):
1. **Baseline build** — plain compiler optimizations, **no SPGO**. Baseline runtime: **3 seconds**.
2. **Compile with SPGO flag on** — identical to the baseline command except adding the SPGO flag. This doesn't optimize anything yet (no samples), but tells the compiler "I'm going to apply SPGO" and **prepares the executable + PDB** so the profile (`.spd`) can be consumed later. Running it warns the **`.spd` is not found** (nothing fed yet).
3. **Capture with `xperf`** — the traditional `xperf`-start / `xperf`-stop flow to capture **ETL traces** containing the **hardware counters** used for PGO. Critically, this runs the **release build — no instrumentation, nothing fancy** — exactly how the end user would run it. (A tutorial at the end explains the details.)
4. **Extract → `.spd`** in **two sub-steps**: first abstract the info out of the ETL traces, then **convert** that into the **`.spd`** file fed to the compiler. *Why two steps?* Big software has **many important workflows** (benchmarks, user interactions) you want to optimize together. Splitting capture means **one workflow → one ETL → one `.spd`**, done **several times in parallel**, then **combined** into a single profile — better, broader signal.
5. **Rebuild with the profile data** — identical to before except now you **feed the profile data to the compiler**, producing the optimized executable.

**Result:** optimized runtime **2 seconds** vs **3-second** baseline — **≈33% improvement** "without bringing up the calculator." Caveat: mileage varies with app code, **sample quality**, hardware, etc.; ISVs report **5–15%** typical gains.

**Why Adobe loved it (beyond the number):** more **responsive**, out-of-the-way Photoshop for users; and a **rethink of optimization** — instead of endless low-level hand-tuning, SPGO is a **scalable, sustainable procedure** that integrates **naturally into the product build pipeline** because it's **not intrusive** (no instrumented fork). Adobe planned to **ship the SPGO-optimized version to the public in the coming days**.

**SPGO is iterative, not one-shot (Adobe's tip):** product code keeps evolving, and even with unchanged code, **customers' usage patterns change**. So treat SPGO as a loop: when code or usage shifts, **go back to the capture step**, run the new scenario, **refresh the profile**, and feed it back to the optimizer — continuously, as part of the build pipeline. Gier's closing pitch: "this is not just a demo — it's reshaping how you think about optimization," and something you can apply to your product tonight. Kayla's one-line summary: you **built the app, trained a profile on it, then rebuilt with that profile** — that's where the **33%** boost came from ("everything in 10 seconds").

### WSL Containers API — embed Linux containers inside a Windows app (Craig)
Craig returned to show the **WSL Containers API** he'd teased. His goal: reuse all that **Linux container code** inside a **native Windows app** **without rewriting** it.
- On the left of his screen: the same **container file** with all his Linux code, now part of a **C# project**.
- In the **`.csproj`** he added a **WSL containers NuGet package**, then **defined the same container** he'd run in the CLI — what to call it, where to find it, where to output it.
- As part of **`dotnet build`** / **`dotnet run`**, it **automatically builds that container**; editing the container file just **re-triggers the build** — "it truly is part of my source code."

He ran `dotnet run` to build and launch the same **markdown app**, this time **fully in WinUI** — "nice and modern." The big takeaway: it **looks exactly like a Windows app**; if he hadn't said Linux was running in the back end, **you wouldn't know**. That's the point — many customers want the **power of Linux without knowing about it** ("my mom and dad don't need to know"). Feeding the same receipt PDF produced the same markdown rendering.

**Architecture:** a **log** showed startup/shutdown speed — **~2.5 seconds** cold start (initialize session → start container → run Linux code). **Task Manager** showed a new **`markdown service`** process running in **its own WSL VM** — the **same VM technology that powers WSL distros**, now applied to Linux containers running as part of a Windows app. **Each Windows app gets its own WSL VM**, and you can run **as many containers as you want** inside it.

**The API in code (C#):** short and simple — start a **new session** (starts the VM with given **CPU and memory** counts), **pull a specific image** (run locally), and **configure exactly the options you need**:
- map only the ports you need (here **port 8000** to expose the API),
- **volume mounting** to grant access to **specific Windows folders** only,
- even **GPU access**.
When closed, **all resources are cleaned up** and the **VM goes away** — it works just like any other app.

**Ecosystem improvements:** aiming for a comprehensive end-to-end container dev story (API *or* CLI):
- **`lazywslc`** — a community project giving a nice **TUI dashboard** for all your containers.
- **Dev Containers** support — WSL containers work with `attach to running container`, `reopen in container`, and in **VS Code**.

**Partner spotlight — Moonray:** Craig highlighted the **Moonray** team, who build a powerful **Linux-based rendering engine** used to render movies like **The Bad Guys 2** and **The Wild Robot**. Their code is **fully open source** and Linux-based; they wanted to bring it to Windows users in a **production-ready** way — bridged via **WSL containers**. Demo: a `wslc moonray` folder built into **`moonray.exe`** (a Windows executable) taking **Windows file inputs** (note the backslashes; `.rdla` render inputs) and rendering out a **JPEG**. The run showed the machine starting, the render **maxing out CPU** (as expected), then a clean shutdown/VM cleanup — producing an image of an **orange coffee maker**. Everything user-facing was **Windows** (`.exe`, Windows inputs/outputs, opened a Windows file), but **all the back-end code was fully Linux** apart from the API integration glue. Craig is excited about the range this unlocks — **AI containerization, cloud, and local**.

### Closing — 16,000+ open-source contributors
Wrapping up (running out of time), Kayla returned to the open-source theme. Clint had the idea to export the list of **everyone who's contributed** to **Terminal, WSL, WinUI and PowerToys** — the file is **16,000 lines long**, i.e. **over 16,000 open-source contributors**. The team thanked all of them (the products "would not be where they are today without y'all"), with a special shout-out to **Nora**, a standout PowerToys contributor (they did a `grep` in her honour using core utils). A final slide collected all the repo links: the **config file** + **comfort shell** (same repo), **SPGO** (with a how-to for your own projects), **Intelligent Terminal**, **WinApp CLI** and **winddev skills** (their own repos), and **PowerToys**. The session closed into **Q&A**.

## 🛠️ Products / Features / Technologies Mentioned
- **Windows** — the OS itself; the only thing in the talk that isn't open source.
- **WSL (Windows Subsystem for Linux)** — runs Linux on Windows; the foundation for WSL containers and the containers API.
- **winget** — the Windows package manager; delivery channel for the dev config, WinApp CLI, etc. ("everything we make goes on winget").
- **winget configuration file / Windows developer config** — idempotent setup file installing WSL+Ubuntu+git/gh/Copilot CLI/VS Code; public repo `Windows developer config`.
- **Windows Terminal** — the team's terminal; host for Intelligent Terminal and the container CLI demos.
- **PowerToys** — utility suite; source of Command Palette, grab-and-move, and (historically) PowerToys Run.
- **PowerToys Command Palette** — extensible launcher; its architecture now powers the new Windows **Run** dialog.
- **PowerToys Run** — the original launcher that evolved into Command Palette.
- **New Run dialog** — refreshed Windows Run built on the Command Palette architecture.
- **Movable / vertical taskbar** — pin taskbar left/top/bottom; in Windows Insider.
- **Intelligent Terminal** — experimental, open-source agentic companion pane in the terminal; agent-agnostic.
- **GitHub Copilot CLI** — CLI coding agent; used in Intelligent Terminal and the WinUI build demo (incl. voice + autopilot modes).
- **Other supported agents** — Claude, Codex, open code (auto-detected by Intelligent Terminal once installed).
- **`wslc` (WSL containers CLI)** — new WSL binary to pull/run/build Linux containers; aliased as **`container`**.
- **`container` alias** — built-in alias for `wslc`.
- **`system session` command** — opinionated `wslc` command (not in Docker/Podman) keeping CLI and API aligned.
- **`edit`** — new command-line editor; mouse-friendly.
- **Core utils** — GNU core utilities native on Windows (`grep`, `tail`, `test`, `env`, `wc`, … as `.exe`); ~75 in repo, 165 tools counted in demo.
- **Comfort shell** — pre-configured Ubuntu setup (Homebrew, zsh, Starship, btop) bundled in the dev config.
- **btop** — terminal resource monitor, baked into comfort shell.
- **Docker Desktop / Podman Desktop / Rancher Desktop** — existing container tools that benefit free from WSL's shared VM improvements.
- **WinApp CLI** — single open-source CLI for Windows SDKs, packaging, app identity, manifests, certificates, build tools.
- **Package identity** — app capability unlocked by WinApp CLI (native notifications; Explorer/taskbar/share-sheet integration).
- **winddev skills** — agent plugin (skills + MCP servers + custom agents) for building WinUI 3 / Windows App SDK apps.
- **WinUI 3 / Windows App SDK** — modern Windows UI framework / app platform targeted by winddev skills.
- **`WinUI dev` custom agent** — the custom agent set in Copilot CLI that routes to the WinUI skills.
- **WPF** — legacy UI framework; winddev includes a WPF→WinUI migration skill.
- **PowerToys grab-and-move** — Alt+click-anywhere window dragging.
- **SPGO (Sample-based Profile Guided Optimization)** — hardware-counter-based PGO with no instrumentation/build fork.
- **PGO (Profile Guided Optimization)** — classic profile-driven compiler optimization SPGO improves on.
- **`xperf` / ETL traces** — capture tool/format for the hardware counters SPGO consumes.
- **`.spd` / `.spt` profile files** — profile data converted from ETL traces and fed to the compiler.
- **WSL Containers API / WSL containers NuGet package** — .NET API to embed Linux containers in a Windows app via the `.csproj`.
- **`.NET` (`dotnet build` / `dotnet run`)** — build system that auto-builds the embedded container.
- **`lazywslc`** — community TUI dashboard for WSL containers.
- **Dev Containers** — supported with WSL containers (attach/reopen-in-container, VS Code).
- **VS Code** — editor; installed by the dev config and supports WSL containers via Dev Containers.
- **Moonray** — partner's open-source Linux rendering engine (The Bad Guys 2, The Wild Robot) brought to Windows via WSL containers.

## 🚀 Announcements / What's New
- **WSL containers** — **announced the morning of the talk**; new `wslc`/`container` CLI shipping as part of WSL. *(Preview/experimental, newly released; exact GA status not stated.)*
- **WSL Containers API** — new **WSL containers NuGet package** to embed Linux containers in Windows/.NET apps. *(Newly introduced; status not explicitly stated as GA.)*
- **Windows developer config** repo — **made public the morning of the talk**; idempotent winget config bootstrapping a dev box.
- **Intelligent Terminal** — **available today**, **open source**, published the morning of the talk; explicitly **experimental**, feedback wanted.
- **Core utils** — newly released; GNU core utilities running natively on Windows, downloadable from the repo today.
- **New Run dialog** — rebuilt on PowerToys Command Palette architecture (shown as shipping/insider-track).
- **Movable / vertical taskbar** — in the **Windows Insider** program and **shipping**.
- **PowerToys grab-and-move** — newly added PowerToys utility.
- **WinApp CLI** — introduced; open source and on winget.
- **winddev skills** — introduced; agent plugin for WinUI 3 / Windows App SDK on winget.
- **SPGO (Sample-based PGO)** — introduced with a tutorial/repo for applying it to your own projects; **Adobe Photoshop's SPGO-optimized build to ship to the public "in the coming days."**
- **2× cross-OS file performance** — improvement to the shared WSL VM tech (Windows files accessed from Linux), flowing upstream to Docker/Podman/Rancher.
- **Comfort shell** — bundled in the dev config repo.

## 💡 Demos
- **Intelligent Terminal regex repair** — an agent wrote a deliberately-broken password-verification regex, detected the failure, and reasoned toward a fix collaboratively without leaving the terminal. *Proved:* an agentic companion pane can assist in-context while you keep your own prompt.
- **`wslc` pull/run distros** — ran latest Ubuntu, then pulled+ran Debian on demand. *Proved:* native, frictionless Linux containers directly in WSL/terminal.
- **Build + run the markdown service container** — built an image from a container file (Python 3.13), listed images piped through `grep`/`wc` (165 tools), then ran it with `-p 8000` and opened `localhost:8000` to a file→markdown web app. *Proved:* end-to-end container build + port-forward into Windows, powered by core utils.
- **Terminal "on fire"** — a one-command novelty container. *Proved:* the breadth/fun of arbitrary containers.
- **WinUI 3 markdown app build (Copilot CLI + winddev)** — voice-dictated prompt, `WinUI dev` custom agent, autopilot mode; agent built, deployed, UI-tested and ran a modern WinUI 3 app. *Proved:* agent + winddev skills can ship a real WinUI app (worked first try in rehearsal; live build also completed).
- **PowerToys grab-and-move** — Alt+click-drag a window hidden behind many tabs. *Proved:* QoL window management.
- **SPGO end-to-end on a Fibonacci stack-VM** — baseline 3s → SPGO-optimized 2s via compile-with-flag → `xperf` capture → `.spt`→`.spd` → rebuild with profile. *Proved:* friction-free ~33% speedup from a release-build profile, no instrumentation.
- **WSL Containers API WinUI markdown app** — same Linux container embedded in a C#/.NET WinUI app via NuGet + `.csproj`, ~2.5s cold start, own WSL VM in Task Manager, clean teardown. *Proved:* Linux containers can power a native-feeling Windows app invisibly.
- **Moonray render** — `moonray.exe` (Windows `.exe`, Windows `.rdla` inputs) rendered a JPEG (orange coffee maker) with Linux code in the back end, maxing CPU then cleaning up. *Proved:* production Linux rendering engine shipped as a Windows app via WSL containers.

## 📊 Notable Stats / Quotes
- **Up to 20%** — real-workflow performance improvement Adobe Photoshop saw from SPGO on CPU-bound workflows.
- **~33%** — SPGO demo speedup (**3 seconds → 2 seconds**) on the Fibonacci stack-VM.
- **5–15%** — typical SPGO performance gains reported by ISVs (vs **5–10%** for classic PGO).
- **2×** — cross-OS file performance improvement (Windows files from Linux) in the shared WSL VM tech.
- **165 tools** — core utilities counted via `wslc image ls | … | wc` (repo highlights ~75).
- **~2.5 seconds** — benchmarked cold-start container init for a WSL-container-backed Windows app.
- **Port 8000** — the port forwarded from container to Windows in the markdown-service demos.
- **Python 3.13** — base used in the demo container file.
- **16,000+** — open-source contributors across Terminal, WSL, WinUI and PowerToys (a 16,000-line contributors file).
- *"If I didn't tell you that this was running Linux in the back end, you would not know."* — Craig, on the WSL Containers API WinUI app.
- *"My mom and dad don't need to know that they're doing some great Linux stuff in the background — they just need to run powerful apps."* — Craig.
- *"This is not just a demo — it's reshaping how you think about optimization."* — Gier, on SPGO.
- *"If you contributed to Command Palette … there's a good chance that your code is now in Windows."* — Kayla.

## 🧠 My Notes / Follow-ups
- [ ] Things to try: run the **Windows developer config** winget file on a fresh box; install **core utils** + **comfort shell** (zsh/Starship/btop); kick the tyres on **`wslc`** (build a container file, `-p` port-forward); enable **Intelligent Terminal** and wire up Copilot; build a WinUI 3 app via **Copilot CLI + winddev skills** (`WinUI dev` agent, autopilot); embed a container in a .NET app with the **WSL containers NuGet package**; apply **SPGO** end-to-end (`xperf` → `.spd` → rebuild) to a sample project.
- [ ] Questions: What's the exact **GA vs preview** status of `wslc`/the WSL Containers API and which Windows builds ship them? How does the WSL Containers API handle **secrets/identity** for embedded containers? Does **GPU passthrough** work across all GPU vendors? How does SPGO interact with existing PGO/LTCG pipelines, and is the `xperf` capture supported in CI? Which model/agent providers does Intelligent Terminal officially support beyond Copilot?
- [ ] Relevant to: anyone setting up or standardizing **Windows dev environments**; teams shipping **WinUI 3 / Windows App SDK** apps; **container/Linux-on-Windows** workflows (incl. AI containerization); **performance-sensitive ISVs** wanting low-friction compiler gains; agentic/AI-assisted dev tooling on Windows.

## 🔗 Related
- [[DEM346 - WSL improvements and the new Containers CLI and APIs]]
- [[DEM345 - From prompt to app build AI powered apps on Windows]]
- [[2026 Build Keynote]]
- [[BRK260 - What's new in Windows for developers]]
- [[BRK200 - The future of agentic development with GitHub Copilot]]
- [[DEM340 - Supercharge your terminal with PowerToys and Windows Terminal]]
- [[BRK265 - Optimizing app performance on Windows]]
- Source list: [[2026 Build Session List]]

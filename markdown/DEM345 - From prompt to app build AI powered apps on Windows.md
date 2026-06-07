---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/windows
  - topic/windows-ai
  - topic/on-device-ai
  - topic/copilot-pc
  - topic/winui
  - topic/agents
source: https://www.youtube.com/watch?v=wMSRtYCL_HU
session_code: DEM345
event: Microsoft Build 2026
speakers: Windows AI Platforms PM + WinUI/Skills & Agents Developer (Microsoft)
duration_min: 22
aliases:
  - From prompt to app, build AI powered apps on Windows
---

# DEM345 — From prompt to app, build AI powered apps on Windows

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Two Microsoft presenters — a developer working on WinUI **skills & agents tooling** (drives the demos) and a PM on **Windows AI platforms** (the AI/model side). Exact names not stated in captions; they joke "that's me, that's him" without naming themselves.  
> **Duration:** ~22 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=wMSRtYCL_HU)

## 🎯 TL;DR
A deck-free, terminal-only, demo-heavy session showing how to **build real WinUI apps on Windows entirely through GitHub Copilot agents** and how to **run AI models on-device** using the Windows AI stack. The hook: a fully offline media-processing app (transcripts, summaries, burned-in captions, video search) built ~100% by Copilot in roughly a day — the presenters say they never looked at the code. The core thesis is **"everything a human needs to build an app, an agent needs too"**: file→new templates, a way to run packaged apps from the CLI, API/control lookup, app UI inspection/automation, and a model tool chain. They ship a WinUI Copilot plugin (via **awesome-copilot**) plus CLI tools (`dotnet new winui`, `dotnet run`, **WinApp**, **WinApp search**, **WinAppD** API search, **WinApp UI** inspect/invoke) that cut agent token usage by **over 70%**. The headline announcement is the **WinML CLI** (announced that day) — a streamlined model tool chain (`winml export/analyze/optimize/perf/build`) that takes a Hugging Face PyTorch model → ONNX → analyzed → optimized → perf-tested, ready to run on CPU/GPU/**NPU** of a Copilot+ PC. They demo it on a **CLIP vision transformer** to add a "find frames" feature that semantically searches a 2-hour video on the NPU (~3 ms/inference, 300+ fps).

## 🔑 Key Takeaways
- **Agents need the same tools humans do.** The session's central argument: if a human uses file→new, looks up APIs, reads stack traces, and optimizes models, then agents must be able to do all of that via CLI tooling too.
- **You can build production WinUI apps without touching code.** The demo app was built ~100% with GitHub Copilot in about a day's work; the team "has not looked at the code for this application at all" and threw out the UI ~4 times while experimenting.
- **The whole talk is terminal-first, no PowerPoint.** Even the closing "deck" is a custom terminal presentation app the presenter built with Copilot (markdown-driven), because they "refuse to go to PowerPoint."
- **Windows AI stack = bring-your-own-model or built-in primitives.** Whether you bring your own model, pull from Hugging Face, or use Windows SDK AI primitives (Phi Silica, etc.), the goal is to make running AI models on Windows easy.
- **WinUI Copilot plugin** is installable in seconds: `plugin install WinUI@awesome-copilot`. **awesome-copilot** is a repository of plugins/skills for Copilot.
- **Skills are just markdown.** "Anybody can build a skill." The WinUI plugin ships skills for design, dev workflow, packaging, code review, test/report setup — everything an agent needs to build WinUI apps.
- **New `dotnet new winui` templates** (released a few weeks before Build) let agents scaffold manifests/XAML/CS files correctly instead of guessing.
- **`dotnet run` now launches a fully *packaged* WinUI app from the command line** — previously impossible (you needed Visual Studio's F5). Achieved via the new **WinApp** CLI.
- **WinApp CLI** (installable via WinGet) gives apps **package identity** so they can call identity-gated APIs: notifications, AI APIs like **Phi Silica**, and shell integrations.
- **Context-window hygiene via lookup tools.** Instead of dumping all API/control docs into skills (poisoning context), agents call CLI tools on demand: **WinApp search** (samples from WinUI Gallery / AI Dev Gallery / Community Toolkit Gallery) and **WinAppD** (API/namespace search).
- **These tools save over 70% of token usage** for agents building WinUI apps — a direct cost saving.
- **Agents can drive the finished app.** **WinApp UI** can launch apps, inspect the live visual tree, list interactive elements, click/invoke buttons, and take screenshots — enabling end-to-end build-and-verify loops.
- **WinML CLI (announced today)** streamlines the fragmented model-prep pipeline (convert PyTorch→ONNX, optimize, quantize, compile-to-hardware) into one tool chain with both a one-shot `build` command and step-by-step subcommands.
- **Model analysis finds fusion opportunities.** `winml analyze` walks the ONNX graph operator-by-operator, emits an optimization recipe (e.g. fuse MatMul+Add into a Gemm), which `winml optimize` then applies to reduce compute nodes.
- **Hardware-aware by default on Copilot+ PCs.** Execution providers shown: **OpenVINO EP** (Intel CPU/GPU/NPU) and **TRT/RTX EP** (NVIDIA GPU). Optimized ONNX stays platform-agnostic/portable unless you choose to compile to a specific hardware graph.
- **NPU is the smart default.** `winml perf` defaulted to the **NPU** on the Copilot+ device, leaving the GPU free for heavy video processing — different models on different chips, running simultaneously without contention. Result: ~3 ms average inference, 300+ frames/sec.
- **Real outcome:** the "find frames" feature (built by Copilot from the CLI + model in ~20-25 min) semantically searched a 2-hour video and surfaced Jensen Huang's leather jacket as the top match — all on the NPU.

## 📚 Detailed Notes

### Session framing: build *with* AI, run AI *in* your app — no slides
The two presenters open casually (long Build day, "ready for dinner"). They scope the talk to two intertwined ideas: (1) **building Windows applications with Copilot / agents** (using the WinUI skills + tooling), and (2) **using AI inside your Windows apps** via Windows platform APIs to "make your applications real." One presenter is a **developer** on skills & agents; the other is a **PM** on **Windows AI platforms** ("how to use AI as well as build *with* AI"). They commit to staying out of PowerPoint and doing **mostly live demos in the terminal**.

### The demo app: a fully offline media processor built ~100% by Copilot
The first demo is a **sample WinUI app** built with GitHub Copilot + the team's skills. Scenario: you're a **YouTuber** who wants to process a media file before upload — **generate transcripts**, **generate a summary**, **burn captions into the video**, apply effects/processes — and do it **fully offline**.

Stack used in the app:
- **Whisper** for transcription (runs completely offline).
- **Foundry Local** running **Qwen 3 14B** (14-billion-parameter model) — the PM clarifies the "name drops": **Project Local** and **Microsoft Foundry on Windows** are names for parts of the **Windows AI stack**.
- Hardware: a **Razer Blade** device with a strong GPU (≈ RTX **5080**), capable of running the 14B model and generating output entirely offline.

Build story: started ~a month ago, but effectively **~one full day** of work, **100% through Copilot**, and **"we have not looked at the code for this application at all."** They iterated heavily — **threw out the UI ~4 times** ("let's try a Jupiter-type look"), just experimenting. This sets up the rest of the session: show the *tooling Copilot uses* so the audience can do the same.

### Installing the WinUI plugin from awesome-copilot
In GitHub Copilot, the presenter has a **WinUI plugin** installed. `plugin list` shows it. Install it yourself with:

```
plugin install WinUI@awesome-copilot
```

**awesome-copilot** = a repository of plugins, skills, and things you can do for Copilot (download many different ones). The plugin ships **skills** — `skills list` shows WinUI skills for **design, dev workflow, packaging, code review, test/report setup** — i.e. "all the things an agent needs to know to build WinUI applications." The PM is "so happy to see packaging there" (the part humans get stuck on most). Key point: **skills are just markdown files; anybody can build one.**

### Tooling that lets agents actually build WinUI apps
Beyond markdown skills, the team **shipped CLI tools** bundled with the skills so agents can *do* the work, not just read about it.

**1) New WinUI templates** (released a few weeks earlier):
```
dotnet new winui
```
Lets agents scaffold a WinUI app quickly without guessing how to create manifest, XAML, and CS files — equivalent to starting a new template in Visual Studio, but **CLI-first because agents prefer CLI tooling over the Visual Studio GUI.**

**2) Run a *packaged* app from the CLI** (newly possible):
```
dotnet run   # on a WinUI app → runs fully packaged on the machine
```
Analogous to hitting **F5** in Visual Studio, but **previously there was no way to run a *packaged* app from the command line.**

### WinApp CLI — package identity + Windows app dev commands
The mechanism behind `dotnet run` working for packaged apps is a new CLI called **WinApp**, installable via **WinGet** ("or whatever"). It exposes many commands for Windows application development. A key capability: **giving applications package identity** so they can call APIs that **require identity**, including:
- **Notifications**
- **AI APIs** like **Phi Silica** (captioned as "my Silica")
- **Shell integrations**

(The PM jokes it "knows how to look out for dogs" — a playful nod to shell/identity integration.)

### Lookup tools instead of context-window poisoning
A recurring design principle: **don't stuff everything an agent might need into the skills/context** — that bloats and "poisons" the context window. Instead, give agents **CLI tools they call on demand** to fetch exactly what they need (which control to use, which API to use). This keeps the agent **actively aware of what it's building and how**.

**WinApp search** — finds samples and returns their code:
```
WinApp search tab      # e.g. search "tab"
```
It surfaces matching samples from the **WinUI Gallery**, the **AI Dev Gallery**, and the **Community Toolkit Gallery**. The agent can then **pull the code** for a sample (e.g. a `TabView`) — the **XAML** and the **.NET** code — plus extra guidance so it knows exactly how to use the control. The presenters note agents often **get stuck on random things and burn time**, so they packed in plenty of "how to handle certain situations" info.

**Token savings:** by giving agents these lookup tools, they measured **over 70% reduction in token usage** when building apps — so adopting the skills/tools both builds the app *and* lowers your token bill.

**WinAppD** — searches **APIs/namespaces** (vs. `WinApp search` for samples/controls). Building an AI-powered app, they search for AI APIs:
```
WinAppD ... use ml models
```
It returns relevant namespaces such as the **Machine Learning** namespace, the **ONNX Runtime** namespace, and the **Phi Silica** namespace (for AI text) — and the team's **language model** shows up there too. The agent then drills in to get the code, how to use it, and *when* to use it. Net effect: **"instead of shipping everything an agent needs to know, the agent looks it up whenever it needs it."**

### WinApp UI — agents launch, inspect, and drive the finished app
After building, an agent should **test and verify** the app works. **WinApp UI** lets an agent:
- **Launch** applications
- **Inspect** them (read the **live visual tree**)
- List **interactive elements**
- **Click / invoke** buttons
- Take **screenshots**

Live demo on the terminal itself:
```
WinApp UI inspect       # inspect the terminal → live visual tree + interactive elements (e.g. "new tab" button)
WinApp UI invoke <button>  # invoke the new-tab button → a new terminal tab opens
```
This closes the loop: agents can **interact with real apps end-to-end (100%)**, confirm features functionally work, and self-verify without a human.

### WinML CLI — the model tool chain (announced today)
The **headline announcement**: **WinML**, a new CLI **announced that day**. It solves the problem that **finding a model on Hugging Face ≠ having a model you can run on Windows**.

Motivating example: the app needed **per-frame captions** so you can **search video content / grab highlights** — a capability **not yet** in the built-in Windows AI APIs. The PM contrasts this with built-in **primitives** (language models like **Phi Silica**, plus video/audio processing) that Windows bakes in as **turnkey API-level solutions**. For non-primitive capabilities, you go to **Hugging Face** and find a model — here, a **CLIP** **vision transformer** model.

Why it's normally hard (the fragmented steps WinML streamlines):
- Most published models are **PyTorch** → must be made **Windows-friendly**.
- **Convert to ONNX** so they run with **ONNX Runtime**.
- **Optimize** and possibly **quantize** (model often too big).
- Optionally **compile** for a **specific hardware configuration**.

WinML offers **two top-level approaches**:
1. **One-shot `build`** — `winml build` with a build configuration exports the model locally, analyzes its graph, then optimizes (and optionally quantizes) in a streamlined run. *(Pizza analogy: order online and it's "ready when it's ready.")*
2. **Step-by-step subcommands** — to understand "how the pizza is made." They demo this path.

**Step 1 — Export (PyTorch → ONNX):**
```
winml export -m <hugging-face-model-id> -o clip.onnx
```
Grab the **model ID** from Hugging Face, pass `-m` for the model name and `-o` for the output `.onnx`. On the demo network they **don't wait for the cloud download** — they use a **pre-downloaded** CLIP ViT model already converted to ONNX on disk.

**Step 2 — Analyze (graph + optimization recipe):**
```
winml analyze -m clip.onnx --optim-config optim.json
```
*(Captioned as "ONNX analyze"; it's the WinML analyze step.)* It checks **which operators can leverage the target hardware** and **which have optimization opportunity**, walking the **entire model graph operator-by-operator** to find operators that can be **fused**. Execution providers observed in the analysis output:
- **OpenVINO EP** → Intel **CPU**, **GPU**, and **NPU** providers.
- **TRT / RTX EP** → the device's **NVIDIA GPU**.

The emitted JSON is tiny but important: it flags that a **MatMul** (matrix multiply) followed by an **Add** can be **fused into a single operator** (a **Gemm**) — a recipe to feed the next step.

**Step 3 — Optimize (apply the recipe):**
```
winml optimize -m clip.onnx -c optim.json
```
Applies the fusion recipe → **fewer compute nodes** → better performance. Important detail: **after optimization the model is still platform-agnostic** and portable to other devices. You *may* optionally **compile to the hardware graph layer** for a specific config (pre-compiled, ready to go) — **not done in this demo** to preserve portability.

**Step 4 — Perf test:**
```
winml perf -m clip.onnx
```
By default runs **100 iterations** of prepared test cases across popular Hugging Face model categories, giving a quick read on real-device performance. With **no device target specified on a Copilot+ PC, it defaults to the NPU** — which is exactly what they want, **leaving the GPU free for heavy video processing**. Result: **~3 ms average inference**, **300+ frames/sec**. Takeaway: **different models can run on different chips simultaneously** (NPU vs GPU) without hurting each other's performance.

### Recap: parity between humans and agents, and "inception" tooling
The closing message: a lot of what was once a **Visual Studio-only** experience is now **available in the terminal**, so **both humans and agents** can do it:
- Humans **look up APIs** → agents can too (WinAppD).
- Humans read **stack traces** to debug crashes → "industry" (the agent tooling) has the same.
- Humans **optimize models** → agents have the exact same tools (WinML).

Framing used throughout: **"If I ask you to build me a house, you won't *manifest* a house — you need the tools."** Same for agents. **"Everything a human requires to learn, there is a matching agent skill."** And by making it easier for agents, **you make it easier for humans** too. The presenter underscores how **cheap and fast** building apps has become — even the **terminal presentation app** used to deliver this "deck" was built with Copilot in markdown, and (because they hated editing markdown) they had Copilot build them **a whole new PowerPoint-style editor app** — "I feel like I'm in inception."

## 🛠️ Products / Features / Technologies Mentioned
- **GitHub Copilot** — the agent used to build the entire app and tooling (plugins/skills, chat-driven dev).
- **WinUI** — the UI framework for the demo app; subject of the Copilot plugin and skills.
- **WinUI Copilot plugin** — `plugin install WinUI@awesome-copilot`; ships skills + CLI tools.
- **awesome-copilot** — community repository of Copilot plugins/skills.
- **Windows AI stack / Windows AI APIs** — umbrella for on-device AI on Windows.
- **Microsoft Foundry on Windows / Foundry Local ("Project Local")** — runs local models (e.g. Qwen 3 14B) offline.
- **Phi Silica** — built-in local **language model** primitive, integrated as a turnkey Windows AI API (identity-gated).
- **Whisper** — offline speech-to-text used for transcription in the app.
- **Qwen 3 14B** — 14B-parameter model run locally via Foundry Local.
- **CLIP vision transformer (ViT)** — Hugging Face model used for image/text embeddings ("find frames").
- **Hugging Face** — source for the CLIP model.
- **ONNX / ONNX Runtime** — target model format and runtime on Windows.
- **`dotnet new winui`** — new WinUI project templates for agents/humans.
- **`dotnet run` (packaged)** — runs a fully packaged WinUI app from the CLI.
- **WinApp CLI** — Windows app dev commands; grants **package identity** (installable via WinGet).
- **WinApp search** — finds samples (WinUI Gallery, AI Dev Gallery, Community Toolkit Gallery) and returns code.
- **WinAppD** — API/namespace search (Machine Learning, ONNX Runtime, Phi Silica namespaces).
- **WinApp UI** — launch/inspect/click/invoke/screenshot apps for agent verification.
- **WinML CLI** — new model tool chain: `winml build/export/analyze/optimize/perf`.
- **Execution Providers:** **OpenVINO EP** (Intel CPU/GPU/**NPU**), **TRT/RTX EP** (NVIDIA GPU).
- **Galleries:** WinUI Gallery, AI Dev Gallery, Community Toolkit Gallery.
- **WinGet** — used to install the WinApp CLI.
- **Copilot+ PC / NPU** — target hardware; NPU is the default inference device.
- **Razer Blade (RTX 5080-class GPU)** — demo device running the 14B model offline.

## 🚀 Announcements / What's New
- **WinML CLI — announced *today*** at the session: a streamlined model tool chain (export PyTorch→ONNX, analyze graph, optimize/quantize, optional hardware compile, perf test) for getting Hugging Face models running on Windows CPU/GPU/NPU. *(Explicitly called "a tool that we just announced today.")*
- **`dotnet new winui` templates** — released **a few weeks before Build**; lets agents scaffold WinUI apps (manifests/XAML/CS) without guessing. *(Recent, not GA status stated.)*
- **`dotnet run` for packaged WinUI apps** — newly possible ("something you couldn't do before"); run a fully packaged app from the CLI via WinApp.
- **WinApp / WinApp search / WinAppD / WinApp UI tooling** — presented as new agent-facing CLI tooling shipped with the WinUI skills (package identity, sample search, API search, UI automation).
- **WinUI Copilot plugin on awesome-copilot** — publicly installable with skills for design, dev workflow, packaging, code review, test/report.

> **GA vs preview note:** The presenters did **not** state formal GA/preview/public-preview labels for these. WinML is explicitly a same-day **announcement**; `dotnet new winui` is described as released “a few weeks ago.” Treat exact channel/availability as **unspecified in this session**.

## 💡 Demos
- **Offline media-processing WinUI app** — take a media file and generate transcripts (Whisper), summaries (Qwen 3 14B via Foundry Local), burn in captions, apply effects — all **fully offline** on a Razer Blade. Built ~100% by Copilot in ~a day; UI reworked ~4 times.
- **Plugin/skills tour in Copilot** — `plugin list` (WinUI plugin present), `skills list` (design, dev workflow, packaging, code review, test/report).
- **Templates + run** — `dotnet new winui` to scaffold, then `dotnet run` to launch a **packaged** app from the CLI.
- **Sample lookup** — `WinApp search tab` returns `TabView` samples + XAML/.NET code from the galleries.
- **API lookup** — `WinAppD ... use ml models` surfaces Machine Learning / ONNX Runtime / Phi Silica namespaces.
- **Agent UI automation** — `WinApp UI inspect` on the terminal shows the live visual tree + the “new tab” button; `WinApp UI invoke` opens a new terminal tab.
- **WinML step-by-step pipeline** — `export` (HF model → ONNX), `analyze` (graph + `--optim-config` JSON; spots MatMul+Add → Gemm fusion; shows OpenVINO + RTX EPs), `optimize` (apply recipe), `perf` (100 iterations, defaults to **NPU**, **~3 ms** avg, **300+ fps**).
- **“Find frames” feature** — built by Copilot in ~20-25 min from the CLI + CLIP model; samples key frames from a **2-hour** Build keynote video, embeds them, compares against a query (“a person … leather jacket”), returns **top 5** — #1 is **Jensen Huang** in his leather jacket; ran **entirely on the NPU**.
- **Terminal “deck”** — the closing recap is a custom terminal presentation app (`presents`) built with Copilot in markdown; plus a Copilot-built markdown editor app for authoring slides (“inception”).

## 📊 Notable Stats / Quotes
- **Over 70% token savings** for agents building WinUI apps when using these lookup tools/skills.
- **~3 ms average inference** on the NPU for the optimized CLIP model → **300+ frames/sec**.
- **`winml perf` defaults to 100 iterations** across popular Hugging Face model categories.
- **~1 day** of effective work to build the full offline app, **~100% via Copilot**, **“we have not looked at the code … at all.”**
- **UI thrown out ~4 times** during experimentation (incl. a “Jupiter-type look”).
- **~20-25 minutes** for Copilot to build the entire “find frames” feature.
- **2-hour video** searched on-device for the leather-jacket demo.
- **Qwen 3 14B** (14-billion-parameter model) running offline on a **Razer Blade / ~RTX 5080**.
- > *“Everything a human requires to learn, there is a matching agent skill.”*
- > *“If I ask you to build me a house, you're not going to manifest a house — you're going to need the tools to build the house. Same thing with agents.”*
- > *“It's so cheap now to build applications. It's crazy.”*
- > *“I refuse to go to PowerPoint because I'm a developer.”*
- > *“Anybody can build a skill. It's just markdown files.”*

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install the WinUI Copilot plugin: `plugin install WinUI@awesome-copilot`, then `skills list`.
  - Scaffold + run a packaged app: `dotnet new winui` → `dotnet run`; install **WinApp** via WinGet and test package identity.
  - Run the WinML pipeline on a small Hugging Face model end-to-end: `winml export → analyze --optim-config → optimize → perf`; compare NPU vs GPU vs CPU.
  - Reproduce a CLIP “find frames” style semantic video search on a Copilot+ PC NPU.
  - Try `WinApp UI inspect`/`invoke` to let an agent self-verify a built app.
- [ ] Questions:
  - What are the official **GA/preview** channels for WinML CLI, WinApp CLI, and the WinUI templates? Any licensing/telemetry notes?
  - How does WinML's `analyze`/`optimize` compare to existing **Olive** / ONNX Runtime tooling — is WinML a wrapper or distinct?
  - Which NPUs are supported beyond Intel (OpenVINO) and NVIDIA (TRT/RTX) — Qualcomm/Snapdragon EP coverage?
  - Is **awesome-copilot** first-party/Microsoft-curated or community? Trust/quality model for installed skills?
  - Confirm exact speaker names + the language model that “shows up” in WinAppD (Phi Silica vs another).
- [ ] Relevant to:
  - On-device / edge AI app development on Copilot+ PCs and Windows AI Foundry.
  - Agent-driven app development workflows (Copilot + skills/CLI tooling) and token-cost optimization.
  - Anyone shipping WinUI apps that embed local models (transcription, summarization, vision search).

## 🔗 Related
- WinUI + AI-assisted workflows: [[OD854 - Building WinUI Apps with C# First Patterns and AI Assisted Workflows]]
- On-device AI / NPU routing: [[BRKSP90 - Stop routing docstrings to 70B models on-device AI on Snapdragon]]
- On-device → cloud orchestration: [[BRKSP92 - Scale agentic AI from on-device to cloud orchestration]]
- Hugging Face models → production: [[DEM320 - Hugging Face open-source models to production on Foundry]]
- AI building blocks for .NET apps: [[OD805 - AI Building Blocks for NET Add intelligence to your C sharp apps]]
- AI at the edge: [[OD837 - Build and deploy AI at the edge for real-world impact]]
- AI to the edge with .NET MAUI: [[OD803 - Taking your AI to the edge with NET MAUI]]
- Source list: [[2026 Build Session List]]

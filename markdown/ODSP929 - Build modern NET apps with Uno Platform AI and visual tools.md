---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/uno-platform
  - topic/dotnet
  - topic/cross-platform
  - topic/ai
source: https://www.youtube.com/watch?v=t_cKjNtB2aU
session_code: ODSP929
event: Microsoft Build 2026
speakers: Sam Basu (Developer Advocate, Uno Platform)
duration_min: 20
aliases:
  - Build modern NET apps with Uno Platform AI and visual tools
---

# ODSP929 — Build modern .NET apps with Uno Platform, AI, and visual tools

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Sam Basu — Developer Advocate, Uno Platform  
> **Duration:** ~20 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=t_cKjNtB2aU)

## 🎯 TL;DR
A whirlwind partner tour of **Uno Platform** — an open-source stack for building modern cross-platform .NET apps from a single shared C# + XAML codebase that runs on iOS, Android, WebAssembly (web), and Windows/macOS/Linux desktop (plus embedded). On top of the foundational platform sits **Uno Platform Studio**, a suite of AI and design tools: **Hot Design** (a runtime visual designer for a *live, running* app), **Hot Reload** (keeps running app, design surface, and IDE code in sync), and a built-in **AI agent** for generating UI. The headline theme is grounding AI agents in reality via two out-of-the-box **MCP servers** — an **Uno MCP** (feeds the agent live Uno docs/best practices) and an **Uno App MCP** ("eyes and hands" — essentially *Playwright for cross-platform .NET apps* that lets the agent screenshot, click, read the visual tree, and validate generated UI). Sam demos Visual Studio scaffolding, the Uno Chefs showcase app with Hot Design, and an AI-built enterprise sales dashboard driven by GitHub Copilot + the MCPs. Closes by teasing a bigger theater session with partner **Kahua** that hints at "a very big announcement and a surprise."

## 🔑 Key Takeaways
- **Single shared C# + XAML codebase → everywhere.** One Uno Platform project targets iOS & Android (mobile), web via WebAssembly, and Windows/macOS/Linux desktop + embedded systems.
- **OS/IDE/CLI-agnostic.** Start from any OS, any IDE (Visual Studio, VS Code), any command line, or any agentic workflow. A Visual Studio **Uno Platform extension** smooths the experience.
- **`uno-check`** is the terminal command/tool that installs all required dependencies and SDKs so you can get up and running on first use.
- **Uno Platform Studio** = the AI + design layer on top of the base platform, built to supercharge productivity.
- **Hot Design** is a *runtime* visual designer — you tweak the UI of an app **while it's actually running**, on a real design canvas with a toolbox, visual tree, and live property editing.
- **Hot Reload** keeps the running app, the design surface, and the IDE code all in sync — no separate design-time vs runtime; it's all real data, all together.
- **Two MCP servers ship out of the box** when Uno detects an Uno Platform project, wired via an `mcp.json` file: **Uno MCP** (docs grounding) and **Uno App MCP** (UI validation / "eyes and hands").
- **Uno MCP** grounds the agent in the latest Uno docs — it can search, fetch multiple pages, summarize, and initialize itself with best practices, so the agent "falls into success."
- **Uno App MCP is "Playwright for cross-platform .NET apps"** — the agent can launch the app, take screenshots, read the visual tree, click, paste text, press keys, and **validate** the UI it generated instead of guessing.
- **Agent-agnostic AI.** Works with GitHub Copilot, Claude Code ("Cloud Code"), Codex, Gemini, Cursor — from Visual Studio, VS Code, *or* a terminal-based agent. Same MCP tools everywhere.
- **You never need to leave the IDE/terminal.** Doc lookups, builds, launches, UI validation, and design pattern guidance (e.g. MVVM vs MVU/MVUX) all happen in-context.
- **Real enterprise proof:** partner **Kahua** runs mission-critical, enterprise-scale cross-platform .NET apps on Uno Platform, using its AI + design tools and embedding AI into the UX.
- **AI gallery** on the Uno site showcases UI (Matrix digital rain, a Winamp-classic player, etc.) built with AI that would take "weeks and weeks" by hand — inspiration that the MCP-grounded workflow is real.
- **Call to action:** start at **platform.uno**, and catch the live Uno + Kahua theater session at Build, which teases "a very big announcement and a surprise."

## 📚 Detailed Notes

### The problem Uno Platform solves
Modern .NET is great — until you realize you have to take your .NET apps to *all the places*. That cross-platform reach is where you need a **foundational platform** that keeps you productive. Uno Platform positions itself as exactly that: a **flexible, open-source stack** for building modern cross-platform .NET apps.

The core promise is a **single shared codebase of C# and XAML** that produces an app running everywhere:
- **Mobile:** iOS and Android
- **Web:** browsers via **WebAssembly**
- **Desktop & embedded:** Windows, macOS, Linux (and embedded systems)

On top of that, the developer gets **choice of UI rendering stack**, plus **themes, extensions, toolkits, and lots of prebuilt UI** to accelerate app building.

### Whole-lifecycle thinking
Uno explicitly designs for the **entire lifecycle** of building a cross-platform .NET app:
- **Start anywhere** — any OS, any IDE (Visual Studio or VS Code), any CLI, any agentic flow.
- **Simple setup** with lots of tools/utilities to build efficiently.
- **Run & deploy guidance** to ship to any platform and any device.

The recommended starting point is **platform.uno** (the website), which links into the **docs** — good for getting situated and getting started — including a **setup guide**. Uno is "fairly agnostic" about environment. If you choose an IDE like Visual Studio, the **Uno Platform extension** makes life easier.

### Uno Platform Studio (the AI + design layer)
Layered on the foundational base is **Uno Platform Studio** — a collection of **AI and design tools** meant to supercharge productivity. Its key pillars:
- **Hot Design** — a **runtime visual designer** for cross-platform .NET apps. While the app is running, you get a **design canvas** to tweak the UI.
- **Custom AI agent** — built into the design experience to generate or modify UI for you.
- **Hot Reload** — keeps everything in sync between the **running app**, the **design surface**, and the **code in the IDE**.

### Grounding AI: the MCP story (the heart of the talk)
For developers using **agentic workflows** between terminal and IDE, Uno brings "the context that AI desperately needs" via **MCP (Model Context Protocol)** tools. Two MCP services ship **out of the box**, auto-wired when Uno detects an Uno Platform project (configured through an **`mcp.json`** file that the AI agent harness reads):

1. **Uno MCP — documentation grounding.** Brings the context of all the latest Uno docs to the AI agent. The agent can **search the documentation, fetch multiple pages, summarize**, and **initialize itself with best practices** for building Uno Platform apps. The effect: the agent is "falling into a bit of success" because it's grounded in factual, current docs — **no hallucinations**.

2. **Uno App MCP — "eyes and hands."** This gives the AI agent the ability to *not guess anymore* about the UI it builds. Sam frames it as **"Playwright for cross-platform .NET apps."** The agent can:
   - take a **screenshot** of the running app,
   - **click** on things in the app,
   - look at the **visual tree structure**,
   - read the (PR/default) action,
   - **paste text**,
   - perform a **key press**.
   In short, anything a human tester can do, the AI agent can now do too — which lets it **validate** the UI it generated and gives you far more confidence in whichever agent you use.

### Demo flow 1 — Visual Studio: scaffold a fresh cross-platform app
On a Windows machine in Visual Studio:
- First-time users run **`uno-check`** (terminal tool) to install all dependencies and SDKs.
- With the **Uno extension** installed, creating a new app (e.g. named "test") launches a **wizard** that steps through everything you might add to a cross-platform .NET app:
  - **app runtime**, **target platforms** (iOS, Android, WebAssembly, desktops), **presentation layer**, **markup of choice**, **theme**, **extensions**, **app features**, all the way down to a **CI/CD pipeline**.
  - All of this is tweakable later; Sam just accepts the defaults and hits create.
- This **scaffolds a true cross-platform .NET project**, Uno-Platform all the way, cross-platform from the get-go.
- In the loaded solution, the various **platforms show up as folders**, so platform-specific code is possible where needed, but it's a **single shared codebase**.
- Running on **desktop** (a fresh build pulls down NuGet dependencies) produces a **super simple starter app** with an **empty shell** to navigate between page one and page two — and it has **Hot Reload and Hot Design wired up from the start**. The same project can run on iOS, Android, WebAssembly, and all desktop targets.

### Demo flow 2 — VS Code on Mac: Uno Chefs + Hot Design deep dive
Switching to the Mac in **VS Code** with a more advanced **showcase app, "Uno Chefs"** (open source, in the Uno sample gallery, a recipe app):
- Deployable to desktop, iOS, Android, or WebAssembly; Sam runs it on desktop.
- **Hot Reload and Hot Design** are wired up up front. Entering **Hot Design** (the runtime visual designer, app still running) exposes several modes:
  - **AI agent panel** — ask it to tweak existing UI or build new UI while the app runs.
  - **Design mode** — full UI design tweaking. Includes a **canvas**, a **toolbox** of drag-and-drop UI, and a **visual design tree** of all UI elements so you can drill down into exactly what to change. Sam drills from a **feed view → value template → item template**, demonstrating **data binding** against **real (not fake) data** — emphasizing there's **no separate design-time vs runtime; it's all together**.
  - Toggling the **Hot Design button** exits design mode while the **app keeps running** — a key UX win.
  - **Interactive mode** — use the app exactly as a real user would (tap, navigate). Sam navigates into a **nutrition** page, then re-enters design to **highlight a specific chart view** several layers down; its UI **properties appear on the right**, including **brushes** painting the colors.
  - Live edit: changing a brush color to **aqua** updates **immediately**. After fully closing and reopening the app to the recipe details page, the **protein brush is now aqua** — confirming the change persisted via the Hot Design + Hot Reload loop between IDE code and running app.

### Demo flow 3 — AI-built enterprise sales dashboard (Copilot + MCPs)
Sam opens a different app: an **enterprise dashboard** (the kind of Salesforce/ERP-style dashboard developers are often asked to build). It's still an Uno Platform app (runs everywhere); he runs it on desktop.
- Crucially, **he did not hand-code the UI** — **AI agents** did much of the work.
- He uses **GitHub Copilot** in the inner AI chat, but stresses agent-agnosticism: this works from **Visual Studio or VS Code**, and equally with **Claude Code ("Cloud Code"), Codex, Gemini, or Cursor**.
- The configuration the agent harness reads is the **`mcp.json`** file, which already wires up the **two Uno MCP services** (Uno MCP + Uno App MCP) because the project was detected as Uno Platform.
- **Starting point options:** he began from a **nice dashboard design**. If you use **design systems**, you can bring assets from **Figma or Penpot ("Pencil")** and have Uno's MCPs talk to those MCPs — or just **start from a screenshot**. The MCP tools then help ensure the UI **looks and behaves** exactly as intended.

**Live AI interaction A — read app state:**
- Fresh chat prompt: **"launch the app on desktop and tell me the total lead count."**
- The agent reasons through it: it's a .NET project → reads the **.csproj** → figures out it needs a **build** → how to **launch** → how to **interact**.
- Tool invocations are **pre-approved** in a couple of workspace spots, so it doesn't prompt before every tool call. **Build is green** → it **launches the Uno app server** → the app runs.
- The agent takes a **visual tree snapshot** to read the total lead count, gets a **screenshot** (Sam approves it on the workspace), and reads values.
- Even though **AI built it**, the dashboard still has **Hot Reload + Hot Design** wired in, so Sam can tweak the design as he goes.
- The dashboard is also **responsive** — running on desktop, but as he **shrinks the UI area** it reflows into a **mobile-suitable form factor** (and can run on web).
- The agent reports back **"$2,847 is your total income,"** which Sam confirms is **accurate** — proof of MCP-grounded, validated output.

**Live AI interaction B — grounded docs lookup:**
- Prompt: **"tell me about the MVUX design pattern in Uno Platform apps."**
- Context: **MVVM** is the common pattern with C# + XAML codebases, but Uno also supports **MVU**, extended as the **MVUX** pattern (shorter dev loop, cleaner approach).
- The agent does **repeated documentation search + fetch** (about **three different pages**) via the Uno MCP, then **summarizes** how to do MVUX with C# and XAML for Uno Platform apps — returning the **core idea, why it's recommended, the building blocks, and state management**, with an MVUX-vs-MVVM rundown.
- Sam enables **"bypass all approvals" / "Yolo mode"** to let it run freely (still may need to approve one at a time in spots). The recurring point: **the developer never needs to leave the IDE** — it's all right there, grounded in docs.

**Live AI interaction C — terminal-based agent parity:**
- Closing the app, Sam runs **GitHub Copilot in the terminal**. It loads up **skills and MCP servers**; inspecting the MCP config shows the **exact same MCP tools** as in Visual Studio / VS Code.
- Bottom line: your AI agents are **always grounded in factual docs (no hallucinations)**, with **more context** so agents can **test interactive features while the app runs** and **validate the UI** — regardless of IDE or terminal.

### The AI gallery (proof + inspiration)
Under **Resources** on the Uno site is a whole **AI gallery** — "amazing UI" with incredible, interactive, beautiful UX built **with AI**. Examples called out: a **Matrix digital rain** effect and a **Winamp classic player**. These would take **weeks and weeks** of hand-coding. The message: with the right **specs / requirements document**, plus the ability to **test the UI via MCPs**, "the world is your oyster" — AI agents become a **sidekick** that generates lots of code *and* validates it.

### Enterprise validation — Kahua
Uno's partner **Kahua** is the marquee enterprise success story: cross-platform .NET apps built with Uno Platform, **deployed at enterprise scale** with many **mission-critical apps**. Kahua uses Uno's **AI and design tools** to build modern .NET apps and **includes AI in the user experience** — a model for how to **modernize a .NET codebase** and deploy it cross-platform with AI + design help.

### Closing call to action
Back at Build, Sam issues an open invitation:
- Search the **Build session catalog** for **.NET / Enterprise .NET** — Uno has a session **on stage live with partner Kahua**, promising "a lot more" than this preview, plus a tease of **"a very big announcement and a surprise."**
- Visit the **booth** in the expo area to talk latest tech / all things AI (and grab swag).
- **Get started today at platform.uno.**

## 🛠️ Products / Features / Technologies Mentioned
- **Uno Platform** — flexible, open-source stack for building modern cross-platform .NET apps from one shared C# + XAML codebase.
- **C# + XAML** — the single shared language/markup combo for Uno apps.
- **WebAssembly** — how Uno apps run in the web browser.
- **Uno Platform Studio** — the suite of AI + design tools layered on the base platform.
- **Hot Design** — runtime visual designer; tweak UI on a canvas while the app is running (toolbox, visual tree, live property/brush editing, interactive mode).
- **Hot Reload** — keeps running app, design surface, and IDE code in sync (no design-time/runtime split).
- **Uno Platform extension (Visual Studio)** — IDE extension that eases the Uno dev experience (new-app wizard, etc.).
- **`uno-check`** — terminal tool that installs all Uno dependencies and SDKs for first-time setup.
- **MCP (Model Context Protocol)** — the protocol Uno uses to ground AI agents; configured via an **`mcp.json`** file.
- **Uno MCP** — out-of-the-box MCP server that feeds the agent the latest Uno docs (search, fetch, summarize, best-practice init).
- **Uno App MCP** — out-of-the-box MCP server giving the agent "eyes and hands" (screenshot, click, read visual tree, paste text, key press) — "Playwright for cross-platform .NET apps."
- **GitHub Copilot** — AI coding agent used in the demos (IDE inner chat *and* terminal).
- **Claude Code ("Cloud Code"), Codex, Gemini, Cursor** — other supported AI agents (Uno is agent-agnostic).
- **Visual Studio / VS Code** — supported IDEs demonstrated.
- **Uno Chefs** — open-source recipe showcase app from the Uno sample gallery (used to demo Hot Design).
- **AI Gallery** — Uno site resource showcasing AI-built UI (Matrix digital rain, Winamp classic player, etc.).
- **MVVM** — common design pattern for C# + XAML codebases.
- **MVU / MVUX** — Model-View-Update and Uno's extended MVUX pattern (shorter dev loop, cleaner state management).
- **Figma / Penpot ("Pencil")** — design-system tools whose MCPs Uno's MCPs can talk to (bring designs over).
- **NuGet** — dependency source pulled on first build.
- **Kahua** — enterprise partner running mission-critical cross-platform .NET apps on Uno Platform.

## 🚀 Announcements / What's New
None explicitly announced in this session. Sam **teases** a "very big announcement and a surprise" reserved for the **live Uno + Kahua theater session** at Build, but no details are revealed here — this is presented as a preview/invitation, not the announcement itself.

## 💡 Demos
- **Visual Studio scaffolding (Windows):** Created a new Uno app ("test") via the extension wizard (runtime, platforms, presentation layer, markup, theme, extensions, features, CI/CD), accepted defaults, and ran a fresh build on desktop — yielding a starter app with an empty navigation shell and Hot Reload/Hot Design pre-wired. *Proved:* one wizard scaffolds a true cross-platform .NET project ready to run on iOS/Android/Wasm/desktop.
- **Uno Chefs + Hot Design (VS Code, Mac):** Ran the open-source recipe showcase on desktop; entered Hot Design's AI/design/interactive modes; drilled the visual tree (feed view → value template → item template) showing real data binding; used interactive mode to navigate to a chart and changed a **brush to aqua live**, persisting after an app restart. *Proved:* runtime visual design + Hot Reload edit a *running* app against real data with no design-time/runtime split.
- **AI-built enterprise sales dashboard (GitHub Copilot + MCPs):** Agent launched the app and reported the total lead count and **"$2,847 total income" (confirmed accurate)** by reading the visual tree/screenshot; dashboard shown to be **responsive** (reflows to mobile form factor). *Proved:* AI agents grounded by the two MCPs can build *and validate* real UI.
- **Grounded MVUX explainer:** Agent fetched ~3 doc pages via Uno MCP and summarized MVUX (core idea, rationale, building blocks, state management; MVUX vs MVVM). *Proved:* doc-grounded answers without leaving the IDE — "no hallucinations."
- **Terminal-agent parity:** Ran GitHub Copilot in the terminal; it loaded the *same* MCP servers/tools as the IDE. *Proved:* the grounded experience is identical across IDE and terminal, and agent-agnostic.
- **AI Gallery walkthrough:** Showed AI-built UI (Matrix digital rain, Winamp classic player) on the Uno site. *Proved:* with good specs + MCP-based UI validation, AI can produce UI that would otherwise take weeks by hand.

## 📊 Notable Stats / Quotes
- **"$2,847 is your total income, which is accurate."** — the agent's MCP-validated readout from the AI-built sales dashboard (Sam confirms accuracy as proof the grounding works).
- **"This is Playwright for cross-platform .NET apps."** — Sam's framing of the **Uno App MCP** ("eyes and hands" for the agent).
- **"No hallucinations."** — repeated claim that agents stay grounded in factual Uno docs via the Uno MCP.
- **Targets one codebase → ~6+ platforms:** iOS, Android, WebAssembly/web, Windows, macOS, Linux desktop (plus embedded), from a single shared C# + XAML codebase.
- **~3 doc pages fetched** for a single MVUX query, illustrating how the Uno MCP grounds even simple questions.
- AI Gallery apps "would take **weeks and weeks** of coding" by hand (e.g. Matrix digital rain, Winamp classic player).
- Tease: **"a very big announcement and a surprise"** waiting at the live Uno + Kahua session at Build.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Run `uno-check` and scaffold a new Uno Platform app via the Visual Studio extension wizard; run it on desktop + WebAssembly from the one project.
  - Clone/run the **Uno Chefs** showcase app and exercise **Hot Design** (interactive mode → tweak a brush live → confirm Hot Reload persistence).
  - Wire up the two MCP servers (`mcp.json` with **Uno MCP** + **Uno App MCP**) and have GitHub Copilot build a small dashboard, then let the **Uno App MCP** screenshot/validate the UI.
  - Try the same MCP flow from a **terminal agent** (Copilot/Claude Code/Codex) to confirm IDE↔terminal parity.
  - Browse the **AI Gallery** on platform.uno for prompt/spec inspiration.
- [ ] Questions:
  - Which model/plan modes give the best results with the Uno App MCP's visual-tree validation loop?
  - How well do the Figma/Penpot → Uno MCP handoffs preserve fidelity for real design systems?
  - What is the licensing/pricing model for **Uno Platform Studio** (Hot Design + the MCP tooling) vs the open-source base?
  - When should I reach for **MVUX** over MVVM in a real Uno app, and what are the migration costs?
  - What was the teased "very big announcement" at the Uno + Kahua theater session? (Follow up post-Build.)
- [ ] Relevant to:
  - Cross-platform .NET app strategy (single C#/XAML codebase → mobile + web + desktop).
  - Agentic/AI-assisted UI development with grounded, validated output (MCP patterns).
  - Modernizing legacy .NET codebases for enterprise cross-platform deployment (cf. Kahua).

## 🔗 Related
- [[Microsoft Build 2026]]
- Uno Platform — https://platform.uno
- MCP (Model Context Protocol) — grounding AI agents in docs + UI validation
- Cross-platform .NET / XAML
- Kahua — enterprise Uno Platform partner

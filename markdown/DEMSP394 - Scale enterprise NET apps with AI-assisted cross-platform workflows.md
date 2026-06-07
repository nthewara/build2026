---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/dotnet
  - topic/cross-platform
  - topic/ai
  - topic/csharp
source: https://www.youtube.com/watch?v=djj1Cu46Ipk
session_code: DEMSP394
event: Microsoft Build 2026
speakers: Sam Basu, Colin Whitlock
duration_min: 24
aliases:
  - Scale enterprise .NET apps with AI-assisted cross-platform workflows
---

# DEMSP394 — Scale enterprise .NET apps with AI-assisted cross-platform workflows

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Sam Basu (Developer Advocate, Uno Platform) · Colin Whitlock (CTO, Kahua)  
> **Duration:** ~24 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=djj1Cu46Ipk)

## 🎯 TL;DR
Uno Platform and its largest enterprise customer, Kahua, jointly unveil **Uno Platform Studio 3.0** — an evolution of Uno's cross-platform .NET tooling into an agentic, AI-assisted developer workflow. The headline capability is a browser-based **"Uno Platform from Studio" app** that spins up a full, real, cross-platform .NET app (iOS, Android, Web/WebAssembly, Windows, macOS, Linux) from a single prompt — with **nothing to install** — then lets you export to GitHub or local and continue in your IDE/CLI. Studio 3.0 ships a **specialized Uno agent backed by 60+ skills**, **MCP tools** for docs grounding and app interactivity (a "Playwright for .NET apps" giving AI eyes and hands), **component previews**, **snippets**, and **plugins** usable from GitHub Copilot, Codex, or Claude Code. Kahua's CTO reports going from 100% hand-written code six months ago to **zero human-written code today** — developers are now "orchestrators" — while stressing that fundamentals, human-in-the-loop verification, and the same C#/XAML artifacts still matter. Core message: humans and AI work in a verification **loop**, and Uno's vertically integrated stack keeps you productive anywhere on the "code-centric ↔ AI-forward" spectrum.

## 🔑 Key Takeaways
- **Uno Platform Studio 3.0** is the major announcement — a re-architecture of Uno's tooling for the "agentic future" with skills, plugins, and integrated AI + design tools.
- A new **browser-based app builder** ("Uno Platform from Studio") spins up a **full cross-platform .NET app from a single prompt** directly in the browser — no SDK install required.
- **Zero install barrier:** the Studio app runs seamlessly on desktop, web, and mobile, removing the painful iOS/Android/Windows/Mac SDK setup that normally gates cross-platform .NET.
- **Build once, run everywhere:** a single shared C# codebase targets iOS, Android, Web (WebAssembly), Windows, macOS, and Linux — no duplicating code per platform.
- **Specialized Uno agent + 60+ skills** (released today) ground AI agents in Uno best practices for navigation, search, Material toolkit, theming, and more, so agents "fall into a pit of success."
- **MCP tools give AI "eyes and hands"** — essentially **Playwright for .NET apps**: agents take screenshots, read the visual tree, click, and type to validate UI in an autonomous loop (great for UI/integration testing).
- **MCP docs grounding** keeps both human and agent anchored in the latest Uno documentation via live search and fetch.
- **Hot Design + Hot Reload everywhere:** pause a running app, edit the live UI on a design surface, and changes sync bidirectionally to code instantly — across console *and* GUI, desktop and mobile.
- **Component Previews** let you build/validate UI elements in isolation across responsive breakpoints, states, themes, and with/without data binding.
- **Snippets** are reusable, drag-and-drop UI building blocks for rapid iteration (mentioned, not demoed).
- **Model-agnostic & MCP-extensible:** demo ran on **GPT-5 Mini**; you pick your model and can wire in your own/external MCP servers — Colin warns against "token maxing" given rising costs.
- **Agent-of-choice:** skills and plugins work from **GitHub Copilot, Codex, and Claude Code** — the same MCP tools surface identically across IDE chat and CLI.
- **Export path is real, not throwaway:** what you build exports to **GitHub or local** and continues as standard C#/XAML — same artifacts, foundations of CS unchanged.
- **Kahua's transformation:** 100+ developers went from fully traditional dev six months ago to **zero human-written code today**, now operating as orchestrators — yet keep strict **human-in-the-loop** approval (PRs, approve/decline/reject).
- **Multi-session collaboration (future):** multiple people on web/mobile can edit the same app's UI simultaneously and push tweaks via hot reload to all live sessions in real time.
- **Fundamentals matter more than ever:** AI multiplies speed, but the **context of how you build and verify** is what prevents "vaporware" — the human↔AI verification loop is the core philosophy.

## 📚 Detailed Notes

### Framing — the build-software spectrum
Sam Basu opens by framing how teams build software as a **spectrum**, not a binary. On the left is **traditional code-centric** development: living in the IDE all day, manually writing and testing code. Moving right you get **visual tooling** — drag-and-drop designers and Hot Reload that let you iterate on UI faster. Further right, **AI is dramatically changing how we build**, but the fundamentals still matter. Uno's thesis: bring enough **context** so that AI agents (and the developer) "fall into a pit of success." As you move left→right, tooling and developer productivity improve markedly with agentic workflows. Survey data (Uno's own) shows the **majority are adopting AI, mostly cautiously** — some hesitant, a growing cohort of "AI-forward" innovators doing **multi-agent orchestration, MCP tools, and skills**. The design goal: **no matter where you sit on the spectrum, tooling should be ready to make you productive.**

### Why fundamentals matter — the Uno Platform foundation
No matter how good AI tooling is, "otherwise it's vaporware." Uno's fundamental is a **foundational open-source stack — Uno Platform** — that has been around a long time. From a **single shared codebase** you build a .NET app that runs on **iOS, Android, Web (via WebAssembly in browsers), Windows, macOS, and Linux** — "all the things" — with a large set of tools to be productive.

### Uno Platform Studio (today's baseline) — AI + design tools
**Uno Platform Studio** is described as a collection of AI and design tools that augment productivity. Components called out:
- **Hot Design** — a **runtime visual designer**. While the app is running you get a **pause button** and a design surface to tweak the live UI; **Hot Reload** syncs changes back to the IDE and code.
- **Design import pipeline** — bring designs from **Figma** or **Pencil** (and similar tools) into actual functional code for your apps.
- **MCP tools for context** — "context is everything." MCP brings **grounding/docs** (latest documentation) so AI does the right thing.
- **Playwright-for-.NET (app interactivity)** — gives AI **"eyes and hands"**: agents can look at the app, interact, click, and type, providing a full way to **validate what the AI is building**.

Sam frames it as a **vertically integrated stack**: start wherever you are (any OS, any IDE), get set up easily with MCP tools, and have everything you need through to **CI/CD and deployment**. Colin (Kahua) confirms they use this heavily for enterprise apps.

### Kahua's context and entry points (Colin Whitlock)
Colin is **CTO of Kahua**, a long-time Uno partner and Uno's **biggest customer**, running an **enterprise platform with many apps under one umbrella**. Key points:
- The company has **100+ developers**.
- **Six months ago** they were still doing **traditional, hand-written development**; **today they write zero code by humans — it's all AI-driven**, and developers are **"orchestrators."** Colin frames this as "the big thing for everyone to learn."
- They **love AI and design tools** (mentions Copilot, "Cloud Design," and Figma) — but what's being shown is the **full stack**: "real live running code," not a mock-up you "polish off later."
- **Many entry points:** you don't have to be AI-first to start. You can do **database-first, rapid prototyping, any model — even waterfall.** Colin stresses the workflow is less linear/vertical and more "**a very big circle**" — you can jump in at any aspect and get started.

### The big reveal — Uno Platform Studio 3.0
After "several months" of work, Sam introduces **Uno Platform Studio 3.0** as the **evolution into the agentic future** with skills, plugins, and all the AI + design tools needed to be productive. Core building blocks:
- **A specialized agent** that knows exactly how to build Uno Platform apps well, **backed by 60+ skills** so agentic loops run efficiently.
- **MCP tools** so agents can read docs and **validate the UI** they build.
- **Zero barrier to entry / nothing to install** — the key innovation. Cross-platform .NET normally depends on **iOS, Android, Windows, and Mac SDKs** (real setup pain). Studio 3.0 removes this by launching the **"Uno Platform from Studio" app**, which runs seamlessly on **desktop, web, and mobile**.
- **Browser-first flow:** go to a browser, **spin up a full .NET app**, watch it being built visually, **tweak the UI**, and when happy, **export and drop into your IDE or CLI**.

Colin reiterates the Uno promise: **build it once, runs everywhere (desktop, web, mobile)** — no duplicating code on a new platform. What follows is "kind of the inverse": **running and building a full .NET app straight from the browser.**

### Demo 1 — Building a weather app from a prompt (platform.uno)
Sam navigates to **platform.uno** (Uno's website), which now has a front-and-center text box: **"Tell us what you want to build."** Unlike tools like **Lovable or Bolt**, this spins up a **full .NET cross-platform app in the browser** with an agent that's "very comfortable." He types a prompt to **build a weather app**; because it's AI, it's **non-deterministic** and enters **planning mode** while it builds (it runs in the background and finishes later — see Demo 4).

### Demo 2 — Pre-built gallery apps (coffee app, CRM app) + Hot Design in browser
While the weather app builds, Sam switches to a **gallery** of already-built apps (you can start from a prompt *or* a gallery template):
- **Coffee app:** out of the gate you can view it in **light and dark mode**, and across **mobile, tablet, and larger form factors** — full visualization of the app.
- The **agent is always present** to tweak app UI on request.
- **Design mode = Hot Design:** select any element, see the **actual visual tree**, drag-and-drop UI, and change properties — **live in the browser**.
- **Previews:** individual UI elements shown in isolation across **responsive breakpoints, states, and with/without data binding**; some system design UI included.
- Back in app mode you can **try the app fully interactively in the browser**.
- **CRM app** (also from a simple prompt): in **interactive mode** it behaves like a real, fully loaded app via **WebAssembly** — with **live charts/data visualization** and **custom mapping solutions** — i.e., **full-on enterprise apps**.
- When ready, hit **Export** → drops into **GitHub or local**.
- **Future tease (not shown live):** **multiple simultaneous sessions** — one person on web, another on mobile — making UI tweaks pushed via **Hot Reload** to all sessions, each loading the app live in real time.

### Demo 3 — Dropping into Visual Studio Code (the "chef's"/recipes app)
Sam moves to **VS Code** to show the dev-environment experience using the **same tools as the web**:
- Several **MCP servers are auto-wired** because the project is recognized as an Uno Platform app.
- A **new plugin** brings in the **60+ skills** with modular guidance/instructions so the agent does the right thing.
- He runs a **recipes app** ("chef's app"). VS Code recognizes all the targets; he runs it on **desktop**, which triggers a build on **.NET 10** (the desktop runtime), producing the **desktop application**.
- The app is **data-driven** with many views/view models. **Hot Reload and Hot Design are wired up** on desktop **and** mobile.
- **Design mode** lets him zoom into individual items, drill into a **CollectionView → template → individual bound data items** showing **live production data**.
- **Interactive mode** handles complex enterprise flows (wizards, multi-step), letting him tap through the app like a real user on desktop/mobile.
- **Round-trip edit:** prompted by a (joking) "CTO calls, wants a small change," Sam highlights a **chart**, changes a **brush color**, and Hot Design **immediately repaints**. Back in the IDE, the change appears in the **recipe pages detail page**, on the **chart control** — the **protein brush color** updated — proving design-surface edits flow straight back to code.

### Demo 3b — Agent grounding inside the IDE (GitHub Copilot / Claude Code)
Sam opens **GitHub Copilot** (notes you could use **Claude Code** or any agent). Because it's recognized as an Uno Platform project, MCP wires up:
- **Best-practice grounding** for how to initialize and build an Uno app.
- **Documentation search and fetch.**
- **App interactivity controls** — **click**, **screenshot**, etc. — "how AI keeps working in a loop until it gets it right."
- He demonstrates asking about a **reactive pattern (MVUX)** — noting Uno supports **MVVM or MVUX** in C#/XAML — and the agent **searches and fetches docs** to summarize what to expect, so **both human and agent stay grounded in the docs.**

### Demo 4 — Headless CLI + GitHub Copilot, 60+ skills, autonomous app launch
Sam closes the GUI to work fully **headless via terminal/command line** ("super super fast") on the same app, then pulls up **GitHub Copilot** chat (the same experience as in Visual Studio/VS Code/Rider, resumable across them):
- The **same MCP tools** appear as in the IDE — docs grounding + app interactivity.
- Asking for available skills surfaces **60+ skills released today** as a **big push for Studio 3.0** (navigation, search, Material toolkit, theming, and more).
- Test command: **"launch the app on desktop."** The agent is **non-deterministic**, recognizes a **.NET project**, reads the **.csproj**, and figures out how to launch with **no hints given** (working over "slow Wi-Fi").
- Meanwhile the **weather app from Demo 1 finishes** — took **~4 minutes** (times are shrinking) — a **fully immersive weather app built entirely in the browser**, exportable to Visual Studio, with light/dark mode and responsive form factors; he can drop into **design** and **previews** to tweak.
- Back on the CLI, **Copilot figures it out**, gets the runtime, and **invokes "app start"** (an **MCP tool**) to launch the **same app** programmatically.

### Demo 4b — Autonomous UI interaction ("click on avocado toast")
With minimal instruction, Sam tells the agent to **"click on avocado toast."** The agent must figure out **what the element is** (button? feed item? clickable?), **traverses the visual tree** via repeated **screenshots**, and clicks the right thing. Sam frames this directly at **testing scenarios — UI testing and integration testing — fully automatable with the right MCP tools.** Colin adds two points:
- It's **powered by MCP**, so you can use **your own or external MCP servers**.
- The demo uses **GPT-5 Mini** — **pick whichever model you like**; nothing is locked to one. He coins "**token maxing**" and warns against it given **rising costs** — "it doesn't need a whole lot to get started."
- Colin's analogy: for teenagers the worst crime is taking away their internet; for developers it's **taking away Hot Design and Hot Reload** — but here every change, **console or GUI**, reflects **immediately**.

### Recap — Studio 3.0 building blocks
Sam recaps Uno Platform Studio 3.0's key building blocks:
1. **Specialized agent** with **skills + MCP tools** so AI does the right thing.
2. **Previews** (shipping) — build/preview/validate UI components **in isolation**, across **responsive boundaries, data context, states, and themes**.
3. **Snippets** (mentioned, not demoed) — building blocks for app UI; drag-and-drop and customize for fast iteration.
4. **Skills and plugins** usable from **GitHub Copilot, Codex, Claude Code** — any agent.
The repeated theme: **start anywhere; barriers to entry removed.**

### Kahua deep dive — LiDAR, 3D mesh, 360° capture (construction)
Colin elaborates on what Kahua builds on Uno (Uno **powers all of Kahua's rendering and display**), and their broader ecosystem includes their own **canvas creator** (he invites attendees to their booth in another building):
- **LiDAR** is a favorite — not just a demo trick but genuinely powerful. You can start with a web-built app, **transition the component into VS Code using Uno components**, and immediately use **iPhone 16 / iPhone Pro and iPad Pro** for **3D mesh modeling**.
- Used internally for **building inspections** — **scan rooms and look for safety violations**.
- **360° photo capture** — important in **construction** (a large part of Kahua's business). For **30–40-year projects**, owners want to see sites **from the beginning through construction**, walking around over time.
- (Caption garble) Colin references a long-standing technology — "even though it's been out for about 20 years" — "powering everything you see here," with "a ton of visuals." *(The captions render this as "Ski"/"Unity platform," but in context this is Uno's own rendering technology; treat the specific name as a caption artifact.)*

### The core philosophy — human + AI in a verification loop
Sam closes with the central thesis: **humans and AI must work in a loop**, with neither holding the other back. Flow:
1. **Human** starts — a **prompt** or a **detailed spec file** — then **hands off to AI**.
2. **AI** must have the **right tools** to **gather, plan, generate code, and verify** — the **verification loop is critical** (this is where **MCPs and previews** come in).
3. The agent loops **until it thinks it's right**, with results streaming **live into the environment via Hot Reload** — keep the browser open and watch the agent fill in work.
4. If needed, jump into **Hot Design**, tweak, and "let it fly again," then move on while **AI builds the rest of the app**.

Returning to the spectrum framing: **no single company or developer does exclusively one thing** — Sam is "in code a lot but also using agents a lot." Uno's pitch: **one tech stack with tooling for every point on the spectrum.**

### Kahua's closing reinforcement — same artifacts, human-in-the-loop
Colin reinforces that Kahua constantly seeks to **reduce overhead** (bootstrapping, getting started — now "just go to a webpage"). Crucially, the **deliverables are the same artifacts**: you're still **building C#**, "not doing anything different" — the **foundations of computer science are exactly the same**; AI and the tooling (MCP servers, instant access, no separate UI-control interface) just **remove friction**. **Human-in-the-loop is a very big thing for Kahua** — "everything needs to be perfect." Although not demoed, **GitHub integration is there**: you can **approve/decline/reject pull requests** every day.

### Final word and CTAs
Sam's takeaway: **fundamentals matter more than ever** — AI increases speed, but **context about how you build and verify** absolutely matters. The promise is a **no-friction way to start cross-platform .NET** with Uno — start in **web, desktop, or mobile**, iterate on design together across multiple stacks. **CTA:** visit the Uno booth (up in the cross/other pavilion, all day for two days). Colin's lighter CTA: fans of **classic arcade games** can see a **Hawaiian-themed arcade game** at the booth.

## 🛠️ Products / Features / Technologies Mentioned
- **Uno Platform** — foundational open-source cross-platform .NET stack (single codebase → iOS, Android, Web/WebAssembly, Windows, macOS, Linux).
- **Uno Platform Studio** — collection of AI + design tools (Hot Design, design import, MCP tools, app interactivity).
- **Uno Platform Studio 3.0** — the new agentic release: specialized agent, 60+ skills, MCP tools, previews, snippets, plugins.
- **"Uno Platform from Studio" app** — install-free app running on desktop/web/mobile that builds full .NET apps from a prompt in the browser (accessed via **platform.uno**).
- **Hot Design** — runtime visual designer (pause running app, edit live UI, view visual tree, drag-and-drop, edit properties).
- **Hot Reload** — bidirectional code↔UI sync, reflected immediately across console and GUI.
- **Component Previews** — UI components in isolation across responsive breakpoints, states, themes, and data-binding.
- **Snippets** — reusable, customizable UI building blocks.
- **MCP tools / MCP servers** — docs grounding (search + fetch) and app interactivity (**click, screenshot, type, app start**); "Playwright for .NET apps"; supports your own/external MCP servers.
- **Skills (60+)** — modular guidance for the agent (navigation, search, Material toolkit, theming, etc.), released today.
- **Plugins** — bring skills/MCP into agents.
- **.NET 10** — desktop runtime used in the VS Code demo.
- **C# / XAML** — output language; supports **MVVM** and **MVUX** patterns.
- **WebAssembly (WASM)** — runs full enterprise apps in the browser.
- **GPT-5 Mini** — model used in the live demo (model-agnostic; user-selectable).
- **Agents / IDEs:** GitHub Copilot, Codex, Claude Code ("Cloud Code"), Visual Studio, VS Code, Rider.
- **Design tools (referenced):** Figma, Pencil, "Cloud Design."
- **Comparison tools (referenced):** Lovable, Bolt.
- **LiDAR / 3D mesh modeling** — via iPhone 16 / iPhone Pro and iPad Pro (Kahua building inspections, safety-violation scanning).
- **360° photo capture** — Kahua construction use case (long-lifecycle project documentation).
- **Kahua canvas creator** — Kahua's own component/build ecosystem layered on Uno.

## 🚀 Announcements / What's New
- **Uno Platform Studio 3.0** — the flagship announcement: Uno's tooling re-architected for the "agentic future," bundling a specialized agent, 60+ skills, MCP tools, previews, snippets, and plugins.
- **"Uno Platform from Studio" app (browser-based app builder)** — spin up a **full cross-platform .NET app from a single prompt** directly in the browser, with **nothing to install** (no iOS/Android/Windows/Mac SDK setup). Runs on desktop, web, and mobile; accessed via **platform.uno**.
- **60+ Uno skills — released today** — modular agent guidance (navigation, search, Material toolkit, theming, etc.) for GitHub Copilot, Codex, and Claude Code.
- **Component Previews (shipping)** — build/preview/validate UI components in isolation across responsive boundaries, data context, states, and themes.
- **Snippets** — drag-and-drop reusable UI building blocks (announced; not demoed).
- **Plugins** — deliver Uno skills + MCP tools into the agent of your choice.
- **Model-agnostic agent** — demoed on **GPT-5 Mini**; bring your own model and your own/external MCP servers.
- **Multi-session collaborative editing (previewed as "the future," not shown live)** — simultaneous web/mobile sessions editing the same app, pushed live via Hot Reload.

## 💡 Demos
- **Weather app from a prompt (platform.uno):** typed "build a weather app" into the front-page text box; agent entered planning mode and built a **full, immersive cross-platform .NET app in the browser in ~4 minutes**, exportable to Visual Studio, with light/dark mode and responsive form factors. *(Contrasted with Lovable/Bolt, which don't produce a real .NET app.)*
- **Gallery — coffee app:** viewed in light/dark mode and across mobile/tablet/larger form factors; entered **Hot Design** to select elements, inspect the **visual tree**, drag-and-drop UI, and edit properties live in the browser; browsed **Previews** of isolated UI elements across breakpoints/states/data-binding.
- **Gallery — CRM app (from a prompt):** fully interactive via **WebAssembly** with **live charts/data visualization** and **custom mapping** — a real enterprise app in the browser; **Export → GitHub or local**.
- **VS Code — recipes/"chef's" app:** auto-wired MCP servers + new plugin (60+ skills); ran on **desktop via .NET 10**; drilled CollectionView → template → live bound data; **changed a chart's protein brush color in Hot Design** and saw it repaint instantly **and** reflect back in the IDE code (recipe detail page / chart control).
- **IDE agent grounding (GitHub Copilot / Claude Code):** docs **search + fetch**, app interactivity (**click, screenshot**), and an **MVUX vs MVVM** documentation lookup keeping human + agent grounded.
- **Headless CLI + GitHub Copilot:** showed the **same MCP tools** as the IDE; listed **60+ skills**; asked the agent to **"launch the app on desktop"** — with no hints it read the **.csproj**, found the runtime, and invoked the **app start** MCP tool to launch programmatically.
- **Autonomous UI interaction ("click on avocado toast"):** agent traversed the **visual tree** via repeated **screenshots** to identify and click the element — framed as automatable **UI/integration testing**.

## 📊 Notable Stats / Quotes
- **"We've gone from writing code by hand 6 months ago … we now [have] zero code written by humans. It's all AI driven. We're orchestrators."** — Colin Whitlock (Kahua).
- **100+ developers** at Kahua operating in this AI-orchestrated model.
- **Weather app built in the browser in ~4 minutes** end-to-end ("making this shorter and shorter").
- **60+ skills** shipped with Uno Platform Studio 3.0 (released the day of the talk).
- **"There is literally nothing to install"** — the core promise of the browser-based Studio app (no iOS/Android/Windows/Mac SDK setup).
- **"AI has eyes and hands"** — MCP app-interactivity tools as "Playwright for .NET apps."
- **"Context is everything"** / agents should "fall into a pit of success." — Sam Basu.
- **"Token maxing"** — Colin's coined term; warns against over-spending on tokens given rising costs ("it doesn't need a whole lot to get started").
- **"The worst technical crime you could commit is taking away [teenagers'] internet … and for developers [it's] taking away their Hot Design and Hot Reload."** — Colin Whitlock.
- **"Fundamentals matter … more than it ever has … AI increases our speed, but the context about how you build and verify … absolutely matters."** — Sam Basu.
- Kahua use cases: **30–40-year construction projects** documented via 360° capture; **building inspections / safety-violation scanning** via LiDAR 3D mesh on iPhone/iPad Pro.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Go to **platform.uno**, type a prompt, and watch a full cross-platform .NET app build in the browser; then **Export to GitHub/local** and open in VS Code.
  - Install the **Uno Platform Studio 3.0** plugin + MCP servers; list the **60+ skills** from GitHub Copilot / Codex / Claude Code.
  - Wire up the **app-interactivity MCP tools** (click/screenshot/app start) and prototype an **automated UI/integration test** loop ("Playwright for .NET apps").
  - Experiment with **Hot Design ↔ Hot Reload** round-tripping (e.g., change a brush color and confirm it lands in code).
  - Try **GPT-5 Mini** (and a couple of other models) to gauge cost vs quality — avoid "token maxing."
  - Explore **Component Previews** across responsive breakpoints, states, themes, and with/without data binding; try **MVUX vs MVVM**.
- [ ] Questions:
  - What's the **licensing / pricing** for Uno Platform Studio 3.0 and the browser builder vs the open-source core?
  - Which **models/providers** are officially supported beyond GPT-5 Mini, and how is the model selected per project?
  - How robust is the **autonomous UI-interaction testing** for complex enterprise flows (wizards, multi-step) at scale?
  - What are the **export fidelity** and ongoing sync guarantees between the browser builder and a hand-maintained repo?
  - Status/availability of **multi-session collaborative editing** (shown as "the future")?
  - How does **GitHub PR approve/decline/reject** integrate into the agentic loop in practice?
- [ ] Relevant to:
  - Teams building **cross-platform .NET** apps (mobile + web + desktop) from a single C#/XAML codebase.
  - Enterprises wanting **AI-orchestrated development** while keeping **human-in-the-loop** governance and standard artifacts.
  - **UI/integration test automation** for .NET apps via MCP-driven agents.
  - **AEC/construction tech** (LiDAR 3D capture, 360° documentation, inspections) — cf. Kahua.

## 🔗 Related
- [[ODSP929 - Build modern NET apps with Uno Platform AI and visual tools]]
- [[Uno Platform]]
- [[Uno Platform Studio 3.0]]
- [[Model Context Protocol (MCP)]]
- [[Hot Reload and Hot Design]]
- [[AI-assisted development workflows]]
- [[Cross-platform .NET]]
- Source list: [[2026 Build Session List]]
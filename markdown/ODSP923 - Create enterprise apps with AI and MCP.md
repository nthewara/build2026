---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/mcp
  - topic/ai
  - topic/enterprise-apps
  - topic/agents
  - topic/blazor
  - topic/dotnet
  - topic/low-code
source: https://www.youtube.com/watch?v=hGbAbsaaHEI
session_code: ODSP923
event: Microsoft Build 2026
speakers: Jason Barris (Infragistics)
duration_min: 19
aliases:
  - Create enterprise apps with AI and MCP
---

# ODSP923 — Create enterprise apps with AI and MCP

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Jason Barris — Infragistics (jasonb@infragistics.com)  
> **Duration:** ~19 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=hGbAbsaaHEI)

## 🎯 TL;DR
A vendor session from Infragistics showing how to build enterprise applications fast by combining **AI/agents, MCP servers, and an installable "skills" system** with a battle-tested UI component library (**Ignite UI** for web, **WinUI/WPF/Windows Forms/MAUI** for desktop & cross-platform). The core thesis: pairing a coding agent (GitHub Copilot / Claude Code) with **Infragistics' MCP servers + skills + CLIs** gives the agent precise, approved knowledge of how to build with Ignite UI — so you get **pixel-perfect, production-ready, hallucination-free** code instead of thousands of unapproved `<div>`s. Jason demos the **App Builder** low-code WYSIWYG/conversational platform (Figma-to-app, sample CRM, publish to GitHub), then drives a coding agent in VS Code to add a data-bound grid and even generate a dashboard app *from a stock image* — all grounded by the MCP servers and skills. The headline announcement is the **brand-new WinUI component suite, launching at Build 2026**, mirroring the WPF experience.

## 🔑 Key Takeaways
- **Build less, ship more with AI + components:** the pitch is "a little low code, not a lot of coding" — AI does a lot with very little effort *when it's grounded by a real component library and skills*.
- **Infragistics ships the same components on every platform** with the **same APIs and feature set** — Blazor, Angular, React, Web Components on the web; WPF, WinUI, Windows Forms, MAUI on desktop/cross-platform. You're not locked into one framework to get a given component.
- **Data grids are the centre of gravity** for enterprise/SaaS apps; Infragistics' grids ship dozens of rich interactions (row actions, export, toolbar, column move/pin/resize/hide, Excel-style filtering, Outlook-style Group By).
- **NEW at Build 2026: the Infragistics WinUI component suite**, mirroring the WPF experience (data grids, data charts, geospatial maps, inputs, dashboard tile, more). **MAUI** with the same components follows shortly after.
- **App Builder = low-code WYSIWYG + conversational AI** — drag-and-drop *or* talk to it; start from empty templates, **Figma**, sample apps, or "create with AI."
- **App Builder generates real, production-ready code** (C#/HTML/Blazor or React) — "no black box, no garbage code" — and lets you **publish to GitHub, Azure DevOps, or download a zip**, even to GitHub Pages.
- **Three pillars ground the agent:** (1) **MCP servers** (Ignite UI CLI MCP + theming MCP), (2) **skills** (per-framework, installed via the Ignite UI CLI from GitHub), (3) the **CLIs** themselves. Together they "inform the agents on how to best build applications with Ignite UI."
- **`igniteui ... ai config`** scaffolds the `.vscode` MCP server config (`mcp.json`) for you; skills are installed with **`github skill install`** picking your framework (e.g. `Ignite UI/Ignite UI-Blazor`) and target agents (GitHub Copilot, Claude Code).
- **Skills are framework-specific:** working in Blazor installs Blazor skills (component skill, generate-from-image, grids, theming); Angular/React install their own equivalents.
- **50 Ignite UI components are open-source MIT** — you can build the majority of an app "literally free."
- **Six built-in themes** (Fluent, Bootstrap, Material, Indigo families) with one-click theming and the ability to build custom themes; demo uses **Fluent Light**.
- **AI grounded by components beats raw generation:** "no drift, no hallucination," fewer tokens, and certainty in outcomes because the agent uses an *approved design system* instead of inventing one.
- **Image-to-app works:** drag a stock screenshot into chat → agent uses Ignite UI MCP + skills → analyses image → emits "pixel-perfect, enterprise-ready" Blazor (cards, charts, gauge) in ~2 minutes — work that "otherwise would have taken days."
- **Cross-product API consistency** is the through-line: the **`XamCategoryChart`** in WinUI/WPF has the same APIs/properties as the Blazor/Angular/React chart — learn it once, use it everywhere.

## 📚 Detailed Notes

### Framing: AI + MCP + low code, minimal hand-coding
Jason opens by setting the thesis for the whole talk: build **enterprise apps with AI and MCP**, with *a little* low code and *not a lot* of hand-coding, because "with AI we can do a lot with very little effort nowadays." The session is deliberately **demo-heavy** — a bit of AI via Copilot, some low-code via Infragistics' **App Builder**, and some command-line tooling — ending with next steps. The implicit argument that recurs throughout: AI alone over-generates and drifts; **AI + a real component library + MCP + skills** produces approved, production-grade results.

### Who Infragistics is, and the "any platform" claim
Infragistics has shipped UI components "for over 35 years" — from the late '80s/'90s through the 2000s toward 2030 — across **desktop, mobile, WPF, WinUI, MAUI, Windows Forms**, and **modern web with Blazor, Angular, React, and Web Components**. The recurring promise: **the same components, with the same APIs and the same feature set, on every platform.** If you trial their React components and later switch to Blazor, the same things are available — you don't pick a framework to unlock a specific component.

### Why data grids matter for enterprise apps
Most enterprise web and SaaS apps have the usual navigation, calendaring, and charting — but **data grids are "a very big part"** of them and have been Infragistics' "claim to fame for decades." For Blazor or Windows Forms you need **dozens of rich interactions** in the grid. The component set also ships polished themes/styles applied uniformly across components (previewed via screenshots, then shown live).

### The desktop is not left behind — and the WinUI launch
Infragistics still does "a lot of work" on **Windows Forms and WPF**, and at **Build 2026 announces a brand-new WinUI component suite**. It **mirrors the WPF experience**: rich **data grids, data charts, geospatial maps, inputs, and more**. **MAUI** with those same components follows "shortly after," enabling **Android, iPad, and desktop** apps from one component set. The message: components on **any platform** to build **any type of experience**.

### Product tour: Ignite UI, Reveal, Slingshot
Starting at **infragistics.com**, Jason highlights three product lines:
- **Ignite UI** — the modern web component toolset (Angular, Blazor, React, Web Components).
- **Reveal** — an **embedded analytics SDK**.
- **Slingshot** — an **"AI-native, AI-first" GTM / work-management** platform (described as a growth/GTM tool).

On the Ignite UI homepage he reiterates the cross-framework parity: **each platform has the exact same components, APIs, and features.** "We ship everything you need to build high-performance web apps on your platform of choice."

### App Builder — low-code WYSIWYG + conversational AI
The "easiest way to get started" is **App Builder**, a **low-code WYSIWYG development platform** into which Infragistics has **injected AI over the last 18 months** — so you can build with a **conversational AI interface** *or* **drag-and-drop WYSIWYG**. It's not exclusive: you can still use the **CLI**, **VS Code / Visual Studio**, **Cursor**, **WinSurf**, etc. Sign-in is via **Office 365 login**, landing in the **App Builder workbench**. New apps can start from: **empty templates**, **Figma → app**, a **sample app**, or **create with AI**.

### Inside the App Builder IDE (CRM sample)
Jason grabs the **CRM sample app** and lands in a **single-page-application WYSIWYG IDE** with a familiar layout:
- **Views** on the left; **properties** on the right that change based on the selected element.
- Drag/move elements; **click and right-click** to **edit with AI**.
- **Grid feature toggles:** for a selected grid you can one-click enable **row actions, exporting, the grid toolbar, column moving, pinning, resizing, hiding, Outlook Group By**, then customise via the element/property panel.
- **Toolbox** of UI components on the left. Key fact: **50 Ignite UI components are open-source MIT** — start "literally free" with the majority of them.
- Bind to **any type of data**; configure **routing, navigation, variables, custom theming**.
- **Six default themes** across **Fluent, Bootstrap, Material, Indigo**; one-click apply or build your own. Plus **digital assets** and the **conversational AI helper**.

He switches the theme to **Fluent Light** and runs the app: dashboard, built-in navigation, the **Kanban view**, and the data grid with the enabled features — **Excel-style filter, Outlook Group By, toolbar with export options**.

### Generated code is real and multi-framework
A standout point: on the right of App Builder you can **see the generated code for the current screen**. For the Customers view it shows the **C# code** plus the **HTML and the Infragistics Blazor components** being generated. Switching the same screen to **React** shows the identical app rendered as React — proving the "any platform" claim live. App Builder is positioned as "an amazing WYSIWYG drag-and-drop AI app development" experience, but the generated output is the real asset.

### Publishing the app (GitHub) and inspecting the output
Jason leaves a `tasks` view intentionally empty, switches the target to a **Blazor Server app**, names it **"CRM app / build 2026"**, and **publishes**. Publish targets: **GitHub, Azure DevOps, or download a zip**; there's also a feature to publish as an actual app to **GitHub Pages**. He creates a **public GitHub repo**; App Builder provisions "the application in the cloud, all of the code that's necessary." Drilling into the repo, all the designed pages are present. Opening `customers.razor`, he stresses it's **"production-ready, amazing C# HTML code — no black box, no garbage code."**

### Bringing it into VS Code and wiring up MCP
He **clones** the repo and opens it in **VS Code** — identical to what was in GitHub. The first real "AI engineering" step:
1. **No `mcp.json` exists yet.** Using the **Ignite UI CLI** (already installed), he runs an **"AI config"** command which **adds the MCP servers into the `.vscode` folder** — specifically the **Ignite UI CLI** MCP and **Ignite UI theming** MCP. He **starts** them so they're "up and running."
2. **Install skills.** Ignite UI has a **CLI**, a **theming CLI**, and **skills** — "all of these together inform the agents on how to best build applications with Ignite UI." He runs **`github skill install`**, chooses **`Ignite UI/Ignite UI-Blazor`** (would be Angular or React if working in those), selects **all skills**, targets **GitHub Copilot and Claude Code**, scoped to this project. Installed skills include: **Ignite UI Blazor component skill, Blazor generate-from-image design, Blazor grids, Blazor theming**.
3. **Verify the agent is grounded.** He asks Copilot, *"Do you have the Ignite UI theming CLI, MCP servers, and skills available?"* — it confirms it has everything needed to build the **Ignite UI for Blazor** app.

### Running the cloned app
A `dotnet run` launches the app in an external browser — the same beautiful app seen in App Builder, with all grid capabilities (the empty **tasks** page already shows Outlook Group By, filtering, column moving/pinning, **export to Excel**, column hiding) — **none of which required hand-written code**; it all came from App Builder.

### Agent task #1 — add a data-bound grid by instruction
Jason now uses the agent to extend the app. He has **customer data with addresses in the cloud** plus a **logo from RoboHash**. He stops the app and gives the agent a precise instruction to add a grid to the **tasks** page, binding the cloud JSON data, with a specific feature list:

> *"On the task page, add a new Ignite UI data grid with this data bound. Add a nice margin around the page to match the other pages. Add these grid features: Outlook Group By, Excel-style filtering, column moving, export to Excel, and put the address information in a multi-row collapsible header. Make sure to inspect the schema of the JSON file to get the field names, and make sure the image for the logo column is rendered correctly."*

On enter, the agent uses the **MCP servers** — doing a **list/search of the Ignite UI CLI MCP servers** and **engaging the skills** — to update the app. After `dotnet run` and a browser refresh, the new grid is present with: an **Outlook Group By** already applied, the **logo rendered** in the left column, a **multi-column header with a collapsible address area**, an **Excel-style filter**, and **toolbar options including export to Excel**. Crucially, because he asked for *export to Excel* specifically (not PDF/CSV), the agent produced **only the Excel export** — evidence the skills + MCP give **precise, instruction-faithful output**.

### Agent task #2 — image-to-app (stock screenshot → Blazor)
Next, a different workflow: he has a **stock dashboard screenshot from Adobe Stock** (`image2.png`) — left nav, cards with data visualizations. He **drags the image into chat** and instructs:

> *"Use Ignite UI Blazor MCP servers and skills, build an app that looks exactly like the attached image. Make sure to match the colors, fonts, etc."*

The agent detects the MCP servers + skills, **analyses the image**, and goes "right from an image to pixel-perfect, enterprise-ready code with Ignite UI Blazor." Here Jason makes his central argument explicitly: by using **components + frameworks + AI together**, you avoid **drift and hallucination**, you don't **burn thousands of tokens** generating screens full of `<div>`s on an **unapproved design system**, and you get **certainty in outcomes** in the **most optimized, efficient manner** (with .NET + Blazor/React/Angular). The result loads on localhost: a **blue-themed app** with **cards across the top**, an **Ignite UI category chart**, and a **gauge**. Comparing to the source image it's "pretty darn close" — a **donut chart** top-right, the category chart, and the **correct values in the cards** — though it **didn't add the data grid** from the image. Next steps would be to keep working with the agent to **bind live data, add screens, and tweak**. His takeaway: ~**2 minutes** for something that "otherwise would have potentially taken days," starting from a stock image with **no designer**.

### WinUI deep-dive — the new product
Closing the demos, Jason showcases the **new WinUI product launching at Build 2026** (more demos downloadable at infragistics.com / YouTube): **beautiful charts, a data grid**, and other components. He highlights the **Dashboard Tile** — a component that gives **end users runtime customization**: swap between **data and chart** views, configure the chart's features, and even **change the chart type at runtime** (optionally hiding the configuration). Switching to code, he shows the **`Infragistics XamCategoryChart`** in **XAML** and stresses **API parity**: WPF users know it as the **XamCategoryChart**, and the Blazor/Angular/React charts share **the same capabilities, APIs, and property settings** — the same holds for other components across WPF/WinUI and Angular/React/Blazor. He's also using **GitHub Copilot Chat to customize the WinUI experience**, reinforcing: build with Infragistics components via **Copilot, by hand — your choice**.

### Wrap-up and call to action
The closing pitch: build beautiful experiences on **any platform** with Infragistics. Start today with **Ignite UI + MCP servers + skills** (any IDE), **App Builder** for low-code + conversational AI, and the **new WinUI** product (plus continued WPF/Windows Forms support). "Learn more at infragistics.com and have a great rest of Build 2026."

## 🛠️ Products / Features / Technologies Mentioned
- **Infragistics** — UI component vendor (35+ years) for desktop, mobile, and web.
- **Ignite UI** — modern web component suite (Blazor, Angular, React, Web Components); same components/APIs/features across frameworks; **50 components open-source MIT**.
- **App Builder** — low-code WYSIWYG + conversational-AI app development platform (AI added over the last 18 months); start from empty templates, **Figma**, sample apps, or "create with AI"; generates real C#/HTML/Blazor/React code; publish to **GitHub / Azure DevOps / zip / GitHub Pages**.
- **WinUI component suite** — **NEW at Build 2026**; mirrors WPF; data grids, data charts, geospatial maps, inputs, **Dashboard Tile**, more.
- **WPF / Windows Forms** — long-standing Infragistics desktop component sets (still actively supported).
- **MAUI** — cross-platform components (Android, iPad, desktop) with the same component set; arriving **shortly after** WinUI.
- **Reveal** — Infragistics **embedded analytics SDK**.
- **Slingshot** — Infragistics **AI-native / AI-first GTM & work-management** platform.
- **Ignite UI CLI** — command-line tool; provides the **`ai config`** command that scaffolds MCP server config and exposes an **MCP server**.
- **Ignite UI theming CLI / theming MCP server** — theming command line + MCP.
- **Ignite UI skills** — installable, framework-specific agent skills (e.g. Blazor component skill, generate-from-image, grids, theming) installed via **`github skill install`** (`Ignite UI/Ignite UI-Blazor`, etc.).
- **MCP (Model Context Protocol) servers** — Ignite UI CLI MCP + theming MCP that let coding agents query/use Infragistics tooling (configured in `.vscode/mcp.json`).
- **GitHub Copilot / GitHub Copilot Chat** — coding agent used to build & customize apps (Blazor and WinUI).
- **Claude Code** — supported coding agent target for skill installation.
- **Cursor, WinSurf, Visual Studio, VS Code** — supported IDEs/editors.
- **.NET / Blazor (Server) / `dotnet run`** — runtime/framework for the generated apps.
- **Data grid features** — row actions, export (Excel), grid toolbar, column moving/pinning/resizing/hiding, Excel-style filtering, Outlook Group By, **multi-row collapsible headers**.
- **Themes** — six defaults across **Fluent (Light), Bootstrap, Material, Indigo**; custom themes supported.
- **`XamCategoryChart`** — Infragistics chart in WPF/WinUI XAML with API parity to the Blazor/Angular/React charts; plus **gauge**, **category/donut charts**.
- **RoboHash** — source of the demo logo image.
- **Figma** — design source App Builder can turn into an app.
- **Adobe Stock** — source of the dashboard screenshot used for image-to-app.

## 🚀 Announcements / What's New
- **Brand-new Infragistics WinUI component suite — launching at Build 2026** (data grids, data charts, geospatial maps, inputs, Dashboard Tile, more), mirroring the WPF component experience. Demos available to download at infragistics.com / on YouTube.
- **MAUI cross-platform components** (same component set; Android, iPad, desktop) — **coming shortly after** the WinUI launch.
- **Ignite UI MCP servers + skills + CLIs** positioned as the supported way to ground coding agents (GitHub Copilot / Claude Code) for building Ignite UI apps — emphasized as current/available tooling.
- **AI in App Builder** — conversational AI interface added over the **last 18 months** (context: ongoing investment, not a brand-new Build 2026 reveal).

## 💡 Demos
- **App Builder CRM sample:** opened a sample CRM in the WYSIWYG IDE; one-click-enabled grid features (export, toolbar, column move/pin/resize/hide, Outlook Group By, Excel filter); applied **Fluent Light** theme; ran the app (dashboard, nav, Kanban view, feature-rich grid). **Proved:** rich enterprise UI assembled with zero hand-coding.
- **Generated-code inspection + framework swap:** viewed the C#/HTML/Blazor code for a screen, then switched the same Customers screen to **React**. **Proved:** real production code is generated and components are framework-agnostic.
- **Publish to GitHub:** set target to **Blazor Server**, named "CRM app build 2026," created a public GitHub repo with all pages and production-ready C#/Razor. **Proved:** App Builder output is real, no black box, deployable.
- **MCP + skills setup in VS Code:** cloned the repo; ran Ignite UI CLI **`ai config`** to scaffold `.vscode` MCP servers; started them; ran **`github skill install`** for **Ignite UI-Blazor** (all skills → GitHub Copilot + Claude Code); confirmed via Copilot that CLIs/MCP/skills were available. **Proved:** how to ground a coding agent for Ignite UI.
- **Agent adds a data-bound grid (task #1):** single natural-language instruction → agent used MCP servers + Blazor skills to add a grid bound to cloud JSON, with margins, Outlook Group By, Excel filtering, column moving, **export to Excel only**, multi-row collapsible address header, rendered RoboHash logo. **Proved:** precise, instruction-faithful, skill-driven generation (only Excel export because only Excel was asked for).
- **Image-to-app (task #2):** dragged an Adobe Stock dashboard screenshot (`image2.png`) into chat and asked for an app that matches its colors/fonts; agent detected MCP + skills, analysed the image, and produced a blue-themed Blazor app (cards, **Ignite UI category chart**, **gauge**, **donut chart**, correct card values) in ~2 minutes — "pretty darn close," though it omitted the data grid. **Proved:** image-to-pixel-perfect enterprise code with an approved design system, no drift/hallucination, minimal tokens.
- **WinUI showcase:** demoed the new WinUI charts/data grid and the **Dashboard Tile** (end users swap data↔chart, configure features, change chart type at runtime); inspected the **`XamCategoryChart`** in XAML and customized WinUI via **GitHub Copilot Chat**. **Proved:** new WinUI suite + cross-platform API parity (same XamCategoryChart APIs as WPF/Blazor/Angular/React).

## 📊 Notable Stats / Quotes
- **35+ years** building UI components ("from the late '80s to the '90s to the 2000s all the way through almost now to 2030").
- **50 Ignite UI components shipped as open-source MIT** — "you can get started for literally free with the majority of our components."
- **AI added to App Builder over the last 18 months.**
- **6 default themes** (Fluent, Bootstrap, Material, Indigo families).
- Image-to-app delivered a working dashboard in **~2 minutes** — work that "otherwise would have potentially taken days."
- > "This is all production-ready, amazing C# HTML code. No black box here. No garbage code."
- > "There is no drift. There is no hallucination. I'm not going crazy with tokens because I'm generating screens with thousands and thousands of lines of divs using a design system my company didn't approve... you'll get certainty in those outcomes in the most optimized, efficient manner."
- > "All of these together inform the agents on how to best build applications with Ignite UI." (on CLIs + MCP servers + skills)
- > "We give you components on any platform to build any type of experience that you need to deliver."

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Spin up the **Ignite UI CLI**, run `ai config` to scaffold `.vscode/mcp.json`, and `github skill install` the **Blazor** (or React/Angular) skills against GitHub Copilot — see how much grounding improves agent output vs raw generation.
  - Test the **image-to-app** flow with a real internal design/screenshot and measure how close the Blazor/React output gets (colors, fonts, charts) and how many tweak iterations it needs.
  - Evaluate **App Builder**'s Figma-to-app + publish-to-GitHub round-trip for a small internal SaaS-style CRM.
  - Download and trial the **new WinUI** suite (Dashboard Tile runtime customization, XamCategoryChart) for any desktop scenarios.
- [ ] Questions:
  - Are the Ignite UI MCP servers/skills usable with **any** MCP-capable agent (beyond Copilot/Claude Code), and how do they handle non-.NET stacks?
  - Licensing model: which 50 components are MIT vs commercial, and what's gated behind a paid Infragistics license?
  - How does the "no hallucination / fewer tokens" claim hold up on larger, multi-screen apps vs the small demos shown?
  - WinUI/MAUI GA timelines and feature parity gaps vs WPF at launch?
- [ ] Relevant to:
  - Teams building **enterprise/SaaS web apps** in Blazor/React/Angular who want agent-assisted, design-system-consistent UI.
  - Anyone evaluating **MCP + skills** as a pattern for grounding coding agents in a vendor toolkit (transferable idea beyond Infragistics).
  - Internal tooling / dashboard / data-grid-heavy app projects.

## 🔗 Related
- [[Model Context Protocol (MCP)]] — the protocol underpinning the Ignite UI CLI/theming MCP servers that ground the agent.
- [[GitHub Copilot]] — the primary coding agent driven in the demos (also Claude Code as a target).
- [[Blazor]] — the main framework used for the generated CRM and image-to-app demos.
- [[Agent skills]] — installable, framework-specific skills (`github skill install`) that teach agents how to build with a library.
- [[WinUI]] — the new Infragistics desktop component suite launched at Build 2026.
- [[Low-code platforms]] — App Builder as a WYSIWYG + conversational-AI low-code dev tool.
- [[Image-to-code with AI]] — generating UI directly from a screenshot/design via agent + skills.
- Source list: [[2026 Build Session List]]
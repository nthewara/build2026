---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/dotnet
  - topic/dotnet11
  - topic/aspnet-core
  - topic/blazor
  - topic/agentic-web
  - topic/aspire
  - topic/ai
source: https://www.youtube.com/watch?v=z2ppHjPRTjQ
session_code: OD802
event: Microsoft Build 2026
speakers: Daniel Roth
duration_min: 44
aliases:
  - Building for the agentic web with NET 11
---

# OD802 — Building for the agentic web with .NET 11

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Daniel Roth (Principal Product Manager, ASP.NET Core & Blazor, .NET team)  
> **Duration:** ~44 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=z2ppHjPRTjQ)

## 🎯 TL;DR
A tour of what's coming for ASP.NET Core and Blazor in **.NET 11**, organised around six roadmap themes: address top feedback, strengthen the foundation (perf/security/observability), invest in the modern stack (minimal APIs, SignalR, Blazor), simplify distributed apps with Aspire, enable agentic web apps, and improve Copilot-assisted .NET development. The headline message: most foundational gains (faster Kestrel, native OpenTelemetry, hardened security) come **just by upgrading — no code changes**. Blazor gets a big push toward **static server-side rendering (SSR) parity with MVC** (temp data, async + client validation without interactivity, new form components), plus a **WebAssembly runtime move from mono to CoreCLR** (preview in .NET 11, stable in .NET 12) and a new **Blazor WebWorker** template. Aspire integration gains a new **Blazor Gateway** for production-grade WASM hosting with service discovery + end-to-end telemetry. For the agentic web, ASP.NET Core hosts agents via the **Microsoft Agent Framework**, supports protocols like **OpenAI responses, A2A, AGUI, and MCP (C# SDK)**, and previews **Blazor AI components**. Finally, Microsoft is making coding agents smarter about .NET via the **.NET Skills repo/marketplace**, custom agents, tools, and eval suites.

## 🔑 Key Takeaways
- **.NET 11 ASP.NET Core roadmap** is on GitHub (`aka.ms/aspnet/roadmap`) and is structured around **six themes**; everything in the talk maps to one of them.
- **Upgrade-only wins:** faster TLS handshakes in Kestrel, efficient malformed-request shedding, **Zstandard compression** (Brotli-level ratios at much lower CPU), and **runtime async** all land with no code changes.
- **Observability is now native:** ASP.NET Core emits **OpenTelemetry semantic-convention tags out of the box** — every request is traced without adding the OTel ASP.NET Core instrumentation package.
- **Security modernisation:** hardened Kestrel, AI-model-driven security scanning of the codebase, **fetch-metadata-header-based CSRF** (Fetch-Site / Fetch-Mode), and **automatic auth token refresh** for long-lived SignalR/Blazor Server connections.
- **Modern stack is the innovation focus** (minimal APIs, SignalR, Blazor); MVC / Razor Pages / API Controllers remain supported and benefit from foundational improvements but aren't where new features go.
- **Async validation** is coming to minimal APIs and Blazor (validate against a DB/external service without blocking); **OpenAPI 3.2** support added with proper binary file responses.
- **Blazor static SSR parity with MVC** is a marquee theme: temp data, session-state binding, output caching, `EnvironmentBoundary`, `Label`/`DisplayName` components, **client-side validation with no interactivity required**, and **localized data-annotation validation messages**.
- **Blazor Server scalability:** new **pause/resume** for idle circuits to free held resources, plus Aspire-assisted scaling.
- **Blazor WebAssembly runtime consolidation:** moving from **mono → CoreCLR** (preview in .NET 11, stable in .NET 12) so WASM 3.0 features (multi-threading, 64-bit memory) are built once on the shared runtime.
- **Blazor WebWorker** template ships now: run CPU-intensive .NET work off the UI thread today (message-passing, not shared-memory — loads a second WASM runtime, so use judiciously).
- **C# unions** are finally coming and are being lit up across the ASP.NET Core stack for richer API contracts, more expressive component parameters, and better type safety.
- **New Blazor Gateway (Aspire):** a production-grade replacement for the long-standing Blazor dev server — serves standalone WASM via `MapStaticAssets`, proxies API calls (no CORS), flows service-discovery config, and collects browser OpenTelemetry into the Aspire dashboard.
- **Agentic web support:** host agents inside ASP.NET Core with the **Microsoft Agent Framework**; built-in hosting for **OpenAI responses, A2A, AGUI** protocols; act as an **MCP server or client** via the MCP C# SDK; all integrated with DI, auth, middleware, observability.
- **AGUI (Agent–User Interaction protocol):** open, event-driven wire format between agents and UIs enabling streaming, tool-execution display, state sharing, front-end tool calls, and human-in-the-loop; **preview** in Microsoft Agent Framework, with **prototype Blazor AI components** in progress.
- **AI-assisted .NET dev** invests in four areas — **agentic skills, custom agents, tools (C# LSP, .NET Inspect CLI), and eval test suites** — distributed via the **.NET Skills repo/marketplace** (`dotnet/skills`).
- **Try it today:** `get.net 11` (SDK/previews), `dot.net/ai` (Extensions AI / Agent Framework / MCP C# SDK), `aspire.dev`, and the `dotnet/skills` repo.

## 📚 Detailed Notes

### Framing: the demands on modern web apps
Daniel Roth (Principal PM for ASP.NET Core & Blazor) opens by noting the rising bar for modern web apps: users want more **performance, airtight security, and full observability** in production; apps must be **modern and interactive**, are mostly **cloud-native and distributed**, and increasingly need **agentic capabilities** — apps that *reason, use tools, and collaborate with people in real time*. Developers want to build more, faster, with **AI as a partner**, and the platform underneath must continuously improve. .NET 11 is positioned to address the needs of the most demanding modern web apps.

### The six .NET 11 ASP.NET Core themes
The roadmap (published earlier this year on GitHub, `aka.ms/aspnet/roadmap`) is organised around six themes, and the whole talk is a walk through them:
1. **Address top feedback & pain points** — issues, comments, and 👍 reactions directly drive the backlog; they aim to close as many top-voted issues as possible.
2. **Strengthen the foundation** — performance, security, observability; the things that make .NET trustworthy.
3. **Invest in the modern stack** — minimal APIs, SignalR, Blazor: where active innovation happens.
4. **Simplify building distributed web apps** — deep collaboration with the **Aspire** team.
5. **Enable building agentic web apps** — **Microsoft Agent Framework**, **MCP C# SDK**, new AI-driven UI patterns.
6. **Copilot-assisted web development** — make AI coding assistants love .NET via agent skills, custom agents, tools, and eval suites.

### Theme 2 — Strengthening the foundation
Foundations get attention every release because they're what you can count on, and **you get them just by upgrading**. .NET runs some of the world's biggest services at Microsoft — **Entra, Bing, Teams, Xbox, and most of Azure** — and those workloads push the bar up for everyone.

**Performance:**
- **Reduced TLS handshake overhead in Kestrel** → faster short-lived connections.
- **Optimised handling of malformed requests** → shed bad traffic efficiently and free capacity for real users.
- **Zstandard (zstd) compression support** → Brotli-level compression ratios at much lower CPU cost.
- **Runtime async** — a more efficient async implementation (worked on with the runtime team) that works great across the platform, including web.

**Security:**
- **Hardening Kestrel**, the cross-platform high-performance web server.
- **Running security scans on the codebase using the latest AI models** to keep the platform secure and trustworthy.
- **Modernised CSRF protection** using **fetch metadata headers** (e.g. `Fetch-Site`, `Fetch-Mode`) based on the latest OWASP/OAuth recommendations.
- **Automatic auth token refresh** for long-lived connections (SignalR, Blazor Server) — a long-standing request closing a real usability gap.

**Observability:**
- ASP.NET Core now **emits OpenTelemetry semantic-convention tags natively** — every request is automatically traced using OTel conventions without external instrumentation.
- **Full OpenTelemetry support for Blazor WebAssembly** is in progress so **component-level metrics and traces from the browser** show up in the same dashboards as server telemetry.

Net result: upgrade to .NET 11 and apps run **faster, safer, more observable — no code changes required**.

### Theme 3 — Investing in the modern stack
Investment is focused on the **modern stack: minimal APIs, SignalR, Blazor**. Other parts (MVC, Razor Pages, API Controllers) remain fully supported and benefit from the foundational improvements, but aren't where new innovation lands.

**Minimal APIs (and Blazor):**
- **Async validation** — validation logic can do long-running work (DB/external service checks) without blocking.
- **OpenAPI 3.2** support with proper **binary file responses**.
- Fixed a long-standing **testing pain point**: using `WebApplicationFactory` with minimal APIs and setting up **custom configuration**.

**SignalR:**
- **Auth token refresh** for long-lived connections (as above).
- **Correlation ID support** for distributed tracing.

**Blazor** (a lot happening — the session's biggest area):
- **Filling out static server-side rendering (SSR)** so you can use static SSR "without compromise": **temp data, binding to session state, output caching, client validation without interactivity, async validation, and much more.**
- **Server scalability via pause/resume** — free up resources held by **idle circuits**.
- **WebAssembly runtime consolidation:** transition the .NET WASM runtime from **mono → CoreCLR**; **preview in .NET 11, stable in .NET 12**. New capabilities (multi-threading, 64-bit memory, other **WASM 3.0** features) land on the CoreCLR base runtime so they don't have to be built twice.
- **Blazor WebWorker** project template (available now) to move CPU-intensive work off the UI thread today.
- **C# unions** — union support is finally coming to C#, lit up across the ASP.NET Core stack for richer API contracts, more expressive component parameters, and better type safety.

### Demo block 1 — Minimal APIs: OpenAPI 3.2 + native OTel
In a minimal API project, **OpenAPI 3.2** is wired up and configured. Opening the OpenAPI document in the browser confirms 3.2. What 3.2 adds: **structured tags, better support for streaming responses** (e.g. server-sent events), and **better representation of different auth flows**. The console output shows **out-of-the-box OpenTelemetry semantic conventions** for the HTTP request, response, and route — with **no additional instrumentation**. In code, all that's needed is adding the **trace source for `Microsoft.AspNetCore`**; you no longer have to add the OTel ASP.NET Core instrumentation package (though you may still want it for the extra niceties). Native support just makes it more efficient.

### Demo block 2 — Blazor static SSR feature parity
A major Blazor focus in .NET 11 is giving you **SSR feature parity with MVC** for things that weren't available in Blazor yet. Demoed side-by-side with Visual Studio:
- **`EnvironmentBoundary` component** — conditionally render content based on the current ASP.NET Core environment (e.g. only in Development, or Development+Staging; or *exclude* content in Production). It's the Blazor equivalent of MVC's **environment tag helper**.
- **`Label` component** — easily set up labels for Blazor forms using a normal C# expression pointing at a model property; generates a label with a friendly display name correctly associated with its input element. Also works in a **wrapping pattern** (wrap the input).
- **`DisplayName` component** — produces the friendly name for a property; demoed generating friendly column headings in a **QuickGrid** data grid, and also usable to generate a label (effectively what the `Label` component does for you).
- **QuickGrid `OnRowClick`** — a new component parameter to wire up an event handler when a user clicks a row; hands you the **model instance** used to render that row (demoed selecting a person and displaying it).
- **Temp data** (`[SupplyParameterFromTempData]`) — like MVC temp data: save a small piece of data to be read after a subsequent navigation (classic **POST → redirect → GET** pattern). Demo: clicking a button does a POST that saves the **server time** into a status-message property; the `[SupplyParameterFromTempData]` attribute marks that property to be saved into and read back out of temp data when the page loads. This was a **full-page navigation, not interactive**. Refreshing clears it (temp data is transient, usually stored in a **cookie**, though other providers are supported).
- **Virtualization enhancements** — the `Virtualize` component renders a huge list (demoed with **10,000 items**) but only renders currently-visible parts. Previously you had to specify a **fixed item size/height**; now it handles **variable item heights** automatically while staying fast.

### Demo block 3 — Validation without interactivity, localization, async
- **Client-side validation with no interactivity:** a static SSR form validates as you type/tab off, yet **no Blazor Server WebSocket and no WebAssembly** is loaded (DevTools confirms the only socket is VS's browser-refresh). Blazor now ships **built-in client-side validation logic** via a **lightweight JavaScript validation library** (no jQuery dependency) so you don't "fall off the cliff" from static SSR into having to enable interactivity just for form validation. It uses the **same data-validation attributes** as MVC/Razor Pages.
- **Localized validation messages:** switching the form language English → Spanish renders **localized validation error messages** — **data-annotation-based validation messages now get localization**, a long-standing pain point addressed in .NET 11.
- **Async validation:** a form requiring a **unique username** — trying `admin` shows a "checking the database…" UI experience and then a "taken" error; this is an **asynchronous, long-running** check (not synchronous), with UI feedback during the check. In code, the **`EditContext`** now exposes APIs for *is validating / is validation faulted / are validation messages available*, plus a **`ValidateAsync`** method on `EditContext`. Microsoft is also adding **async validation support to `System.ComponentModel.DataAnnotations`** in the core libraries (still coming) so you'll be able to annotate types with async validation attributes that plug into this experience.

### Demo block 4 — Blazor WebWorker (CPU-intensive work off the UI thread)
A **Blazor WebWorker** runs .NET code on WASM in the browser but **not on the UI thread** — in a separate web worker. There's a **new project template** (search "WebWorker"). It provides a **WebWorker client class** to create clients (which spin up JavaScript to set up the .NET runtime in a worker) and an **`InvokeAsync`** method to call code on the worker thread. Demo: a `DataWorker.AnalyzeSalesData` method marked **`[JSExport]`** crunches a large set of sales records. Running ~**a quarter-million records on the UI thread freezes a "health" counter**; running the same on the **web worker keeps the counter chugging** and the UI navigable.

**Caveats (stated explicitly):** this is **not true multi-threading** — **no shared memory** between worker and UI thread; think of it like a **separate process with message passing**. It **loads a second .NET WASM runtime** in the worker, so it can be **memory-heavy** — be judicious. Still a "very cool" way to offload CPU-intensive work with the existing runtime today.

### Theme 4 — Distributed & cloud-ready apps with Aspire
Modern web apps are distributed: front end, back-end APIs, AI services, databases, caches — lots of moving parts. **Aspire** provides **orchestration, observability, and configuration management** for distributed apps, with a great local-dev experience and a clean deployment story. In the .NET 11 timeframe they're **deepening Blazor + Aspire integration**:
- Make **Blazor WebAssembly work properly with Aspire** — configuration, **service discovery**, OpenTelemetry, and simplified debugging from the browser through to the back end.
- **Simplify Blazor Server scaling** via Aspire.

To enable this there's a **new Blazor-specific Aspire host integration package** and a new **Blazor Gateway service** that sits between the browser and the back end. The Gateway:
- **Serves standalone Blazor WASM apps via `MapStaticAssets`** (gets all the optimisations).
- **Proxies API calls** to back-end services → **no CORS needed**.
- **Flows configuration / service-discovery data** to the client.
- **Collects OpenTelemetry** from the client to populate the Aspire dashboard.
- Handles **session affinity**.
- **Replaces the long-standing Blazor dev server** with something **production-grade** — good for local dev *and* deployable as a production service to host standalone WASM with the right optimisations.

### Demo block 5 — Standalone Blazor WASM fully integrated with Aspire
Solution layout: a **standalone Blazor WASM** project (no server component), a **back-end minimal API** (weather), the **Aspire AppHost** (orchestrates front end + back end), the **ServiceDefaults** project (health checks, resiliency, etc.), and a **new `ClientServiceDefaults` project** for browser-specific concerns (analogous to the new ServiceDefaults template **MAUI** has for native mobile). There's a **new "Blazor WebAssembly service defaults" template** to set this up.

In `AppHost.cs` (referencing the **new Blazor Aspire hosting integration package**): the API project is set up normally; a new **`AddBlazorWasmProject`-style** entry for the WASM app references the API (so Aspire knows the front end calls it and gives it a real endpoint); and a **`WithBlazorClientApp`** call wires up the **Blazor Gateway** to host the WASM app, expose the API endpoints it needs, and collect client OpenTelemetry for end-to-end visibility.

Running the AppHost brings up the **Aspire dashboard** showing the **Gateway** (with the WASM app nested under it) and the **API**. Browsing the Blazor app, the counter and weather page work — the weather page calls the API successfully. In code, the WASM app's `HttpClient` uses the **Aspire service-discovery convention** ("talk to the weather API; Aspire, resolve the URL"), and the Gateway flows that service-discovery config into the WASM app so the URL resolves correctly. **Structured logs** show the request being proxied through the Gateway to the back end and succeeding; **traces** show the full end-to-end flow (browser → server → Gateway uses service discovery → proxy to API → weather data returned). **Metrics** from the WASM app (e.g. number of page navigations, which pages were browsed) surface in the dashboard because it's **exporting OpenTelemetry from the browser**. A **dashboard-launched debugging experience** (attach the debugger from the dashboard) is also planned/coming.

### Theme 5 — Making web apps agentic
Modern web apps increasingly include **AI agents that reason, plan, use tools, and interact with the user in real time** — a new set of web-framework requirements. Microsoft wants ASP.NET Core and Blazor to be the best place to build these. Working closely with the **Microsoft Agent Framework** team, you can **host agents directly inside ASP.NET Core apps** and tap into AI services like **Microsoft Foundry**. Built-in hosting support covers multiple agentic protocols:
- **OpenAI responses protocol** — chat completions and function calling.
- **A2A (Agent-to-Agent)** — multi-agent orchestration.
- **AGUI** — real-time agent-to-human / user-interface interactions.
- **MCP (Model Context Protocol)** — expose your app's functionality as an **MCP server** to other agentic apps, or act as an **MCP client** consuming tools/resources from other servers, via the **MCP C# SDK**.

All of this integrates naturally with ASP.NET Core **middleware, dependency injection, authentication, and observability**.

**Building agentic UIs** has its own challenges: streaming messages, showing tool execution and reasoning in progress, **synchronizing state** between agent and UI (so the agent knows what the user is looking at), **multimodal inputs** (speech, images, video), and **human-in-the-loop** workflows where the human stays in control.

**AGUI (Agent–User Interaction protocol)** is an **open, event-driven protocol that standardizes the wire format between agents and UIs**, letting you focus on the UI instead of plumbing. **AGUI support in Microsoft Agent Framework is currently in preview.** Microsoft is also building a set of **Blazor AI components** to make agentic UIs straightforward. (Learn more at the AGUI spec site, `agui.com`.)

### Demo block 6 — AGUI Dojo, in React and then in Blazor
The **AGUI Dojo** sample app showcases many AGUI scenarios across different agent-framework backends (including the Microsoft Agent Framework). The reference front end is **JavaScript + React** using components from **Copilot Kit** (usable with a .NET back end). Daniel then shows a **.NET + Blazor implementation of the AGUI Dojo**:
- **Server side (Microsoft Agent Framework):** to create an AGUI endpoint you just call **`MapAGUI`** and point it at the agent to host; multiple agents are wired up this way. Agent Framework is built on **Microsoft.Extensions.AI** abstractions, so you can wire up **tools** (e.g. an agent with a **`GetWeather`** tool to fetch current weather from the server).
- **Client side:** an **AGUI chat client** implementation is provided that is itself an implementation of the **`IChatClient`** interface from Microsoft.Extensions.AI — so it plugs seamlessly into that infrastructure while adding UI-specific affordances based on the AGUI protocol. One affordance is **front-end tools** — tools available not just from the server but from the **client** (e.g. a tool that lets the agent call down into the client to **change the background color** of the UI).

Running the Blazor AGUI Dojo, the demo shows:
- **Streaming chat** — ask it to generate a sonnet and get streaming text back.
- **Front-end tool call** — "please change the background color on the front end" gets plumbed back to the agent, which calls back into the client to execute the tool.
- **Back-end tool call with custom widgets** — invoking a back-end weather tool renders a **custom weather widget** (AGUI has affordances for rendering custom widgets on tool invocation).
- **Human-in-the-loop** — collaborate on a plan: a custom component renders where you select which parts of the plan you like, then **confirm** or **reject** (rolling it back) — true human↔agent interaction with the human in control.
- **Long-running / generative flows** — ask the agent to execute a plan (e.g. "a plan for going to Mars") and get **streamed progress updates** into the UI via specific AGUI events.
- **Full state sharing** between the UI state and the agent, so the agent can be a **full collaborator** in the UI experience.

The sample also shows **prototype Blazor AI components**: an **`AgentBoundary`** component for the chat interface (point it at the agent to drive it), a **messages** component, and **agent loading indicator** components. Daniel stresses the **names are still prototype** ("don't get too attached") but they show the direction.

### Theme 6 — Improving AI-assisted .NET web development
AI coding assistants (e.g. Copilot) are great partners *when they understand your frameworks*, but they struggle with unfamiliar features — picking the wrong pattern, missing a new feature, or generating code that compiles but isn't idiomatic. Microsoft is investing in **four areas** to make AI assistance genuinely smarter about .NET:
1. **Agentic skills** — a variety of ASP.NET Core and Blazor AI skills giving coding agents new capabilities/expertise; found and installed from curated **.NET plugins** in the **.NET Skills repo/marketplace** (`dotnet/skills`).
2. **Custom agents** — specialized personas for .NET work (back-end ASP.NET Core dev, front-end Blazor dev, tester, doc writer, architect), each with deep framework knowledge and a focused skill set; they're exploring which personas matter most.
3. **Tools** — command-line tools/executables that give agents new capabilities: e.g. the **C# LSP** (rich semantic engine for navigating/editing code), the **.NET Inspect** CLI (query .NET APIs across NuGet packages and local projects), and other MCP servers (e.g. **Playwright** integration). They're exploring which CLI/MCP tools to include for .NET.
4. **Eval test suites** — evaluation tests for real .NET coding tasks to **measure** whether skills/custom agents/tools actually move the needle. "If we can't measure it, we don't really know if it works."

### Demo block 7 — Blazor "Plan UI change" skill (Kanban refactor)
Visiting **`dotnet/skills`** shows the repo/marketplace with plugins for many .NET scenarios, including **ASP.NET Core** and **Blazor**. The Blazor plugin includes brand-new skills for authoring components, handling user inputs, configuring auth, coordinating components, and more. A notable one is **"Plan UI change,"** which helps the agent break a UI into composite parts — agents tend to create **big monolithic components** instead of decomposing into subcomponents, and this skill instructs the agent to do better.

Demo: asking an agent to build a **Kanban board** Blazor app **without** the skill produced a working board but a ~**300–400-line** single `Board.razor` file (poor factoring). Adding the Blazor plugin and asking again produced a **refactored version with proper subcomponents and component parameters** flowing data through the app — more idiomatic, equally functional (styling slightly different since it was a different agent run). Skills are added on a **need-only basis** so they don't contaminate the context window, and they're **heavily tested with eval suites** for real-world benefit.

### Recap — the big picture for .NET 11 web
- **Strengthen the foundation:** more performance, security, observability — often driven by the largest .NET services in the world, flowing straight into your apps on upgrade.
- **Invest in the modern stack:** minimal APIs, SignalR, Blazor — C# unions, async validation, OpenAPI improvements, and more.
- **Blazor specifically:** static SSR feature parity with MVC, server scalability, and the new **CoreCLR-based WASM runtime**.
- **Distributed apps with Aspire:** better Blazor WASM support, service discovery, end-to-end observability, and a production-grade **Blazor Gateway** hosting story.
- **Position .NET for the agentic web** with the Microsoft Agent Framework, **AGUI** support, and **Blazor AI components**.
- **Make AI smarter about .NET** with agentic skills, custom agents, tools, and eval suites.
- Throughout, keep addressing **top feedback and pain points**.

### How to get involved today
- **`get.net 11`** — install the .NET 11 preview SDK, try new templates, kick the tires, give feedback.
- **`dot.net/ai`** — Microsoft.Extensions.AI, Microsoft Agent Framework, MCP C# SDK for building agentic apps.
- **`aspire.dev`** — "aspirify" your .NET apps.
- **`dotnet/skills`** — install the new .NET skills.
- Build something cool and share your experience to help improve the platform.

## 🛠️ Products / Features / Technologies Mentioned
- **.NET 11** — the release this session is about (in preview at Build 2026).
- **ASP.NET Core** — the web framework; foundational + modern-stack improvements throughout.
- **Blazor** — Microsoft's web UI framework; the session's largest focus (SSR parity, WASM, agentic UIs).
- **ASP.NET Core .NET 11 roadmap** — published on GitHub at `aka.ms/aspnet/roadmap`; six themes.
- **Kestrel** — cross-platform high-performance web server; hardened + faster TLS handshakes in .NET 11.
- **Zstandard (zstd) compression** — new compression giving Brotli-level ratios at lower CPU cost.
- **Runtime async** — more efficient async implementation worked on with the runtime team.
- **OpenTelemetry (OTel)** — semantic-convention tags now emitted natively by ASP.NET Core; WASM telemetry coming.
- **Fetch metadata headers (Fetch-Site / Fetch-Mode)** — basis for modernised CSRF protection.
- **Minimal APIs** — modern-stack pillar; async validation, OpenAPI 3.2, testing fixes.
- **SignalR** — real-time pillar; auth token refresh + correlation ID for distributed tracing.
- **OpenAPI 3.2** — latest OpenAPI version supported: structured tags, streaming (SSE) responses, better auth-flow representation, binary file responses.
- **`WebApplicationFactory`** — test host; custom-configuration pain point with minimal APIs fixed.
- **MVC / Razor Pages / API Controllers** — still supported; benefit from foundational improvements but not the innovation focus.
- **`EnvironmentBoundary`** — new Blazor component: conditionally render by ASP.NET Core environment (MVC environment-tag-helper equivalent).
- **`Label` component** — new Blazor form-label component (expression-based or wrapping pattern).
- **`DisplayName` component** — new Blazor component producing a property's friendly name (grid headings, labels).
- **QuickGrid** — Blazor data grid; gains `OnRowClick` (returns the row's model instance) and `DisplayName`-driven headings.
- **Temp data / `[SupplyParameterFromTempData]`** — MVC-style temp data in Blazor (POST→redirect→GET), usually cookie-backed.
- **`Virtualize` component** — now supports **variable item heights** (previously fixed-size only); demoed with 10,000 items.
- **Client-side validation library** — lightweight JS validation (no jQuery) for static SSR forms without interactivity; uses MVC/Razor-Pages data-validation attributes.
- **Localized data-annotation validation messages** — validation errors now localizable (demoed EN→ES).
- **`EditContext` async APIs / `ValidateAsync`** — new APIs for validating-state, faulted-state, messages, and async validation.
- **`System.ComponentModel.DataAnnotations`** — gaining async validation attribute support (still coming).
- **Blazor Server pause/resume** — free resources held by idle circuits for better scalability.
- **CoreCLR WASM runtime** — Blazor WebAssembly moving mono→CoreCLR (preview .NET 11, stable .NET 12); WASM 3.0 features (multi-threading, 64-bit memory) on the shared runtime.
- **Blazor WebWorker** — new project template + WebWorker client class + `InvokeAsync` to run CPU-intensive .NET code off the UI thread (message-passing; loads a 2nd WASM runtime).
- **`[JSExport]`** — marks a .NET method callable from JS / the web worker (demoed on `AnalyzeSalesData`).
- **C# unions** — coming to C#, lit up across ASP.NET Core for richer contracts, expressive params, type safety.
- **.NET Aspire** — orchestration, observability, and configuration for distributed apps; deeper Blazor integration in .NET 11.
- **Blazor Gateway** — new production-grade service hosting standalone WASM (`MapStaticAssets`), proxying APIs (no CORS), flowing service discovery, collecting client OTel, session affinity; replaces the old Blazor dev server.
- **Blazor Aspire hosting integration package** — referenced in AppHost; `WithBlazorClientApp` wires up the Gateway.
- **ClientServiceDefaults project + "Blazor WASM service defaults" template** — browser-specific service defaults (analogous to MAUI's native-mobile ServiceDefaults).
- **Service discovery (Aspire convention)** — WASM `HttpClient` resolves API URLs via Aspire; Gateway flows the config.
- **Aspire dashboard** — shows resources, structured logs, traces, and metrics (including browser/WASM telemetry).
- **Microsoft Agent Framework** — host agents inside ASP.NET Core; built on Microsoft.Extensions.AI; supports AGUI/A2A/OpenAI-responses; provides `MapAGUI`.
- **Microsoft Foundry** — AI services that hosted agents can tap into.
- **OpenAI responses protocol** — supported agentic protocol for chat completions + function calling.
- **A2A (Agent-to-Agent) protocol** — supported protocol for multi-agent orchestration.
- **AGUI (Agent–User Interaction protocol)** — open, event-driven UI↔agent wire format; preview in Agent Framework (spec at `agui.com`).
- **MCP (Model Context Protocol) + MCP C# SDK** — expose your app as an MCP server or act as an MCP client.
- **Microsoft.Extensions.AI / `IChatClient`** — abstractions the Agent Framework and the AGUI chat client build on.
- **`MapAGUI`** — endpoint helper to host an Agent Framework agent over AGUI.
- **AGUI Dojo** — sample app showcasing AGUI scenarios across backends; React/Copilot-Kit version + new Blazor version.
- **Copilot Kit** — provides the React components for the reference AGUI Dojo front end.
- **Blazor AI components (prototype)** — `AgentBoundary`, messages, agent-loading-indicator components for agentic UIs.
- **.NET Skills repo/marketplace (`dotnet/skills`)** — curated .NET plugins/skills for coding agents (ASP.NET Core, Blazor).
- **Custom agents** — proposed .NET personas (back-end dev, front-end dev, tester, doc writer, architect).
- **C# LSP** — semantic engine giving agents rich code navigation/editing.
- **.NET Inspect (CLI)** — lets an agent query .NET APIs across NuGet packages and local projects.
- **Playwright (MCP)** — example MCP server adding capabilities to agents.
- **Eval test suites** — measure real-world coding-agent effectiveness for skills/agents/tools.
- **MAUI ServiceDefaults template** — referenced as the native-mobile analogue to the new Blazor client defaults.

## 🚀 Announcements / What's New
All of the following are **.NET 11** work; many are already shipping in the **.NET 11 previews**, with some items explicitly forward-looking:
- **Foundational upgrade-only improvements** (shipping/in-preview): faster Kestrel TLS handshakes, malformed-request shedding, **Zstandard compression**, runtime async, fetch-metadata CSRF, auto auth-token refresh for SignalR/Blazor Server, **native OpenTelemetry semantic conventions**.
- **Full OpenTelemetry for Blazor WebAssembly** — in progress (component-level browser metrics/traces in the same dashboards).
- **OpenAPI 3.2 support** in minimal APIs — available in previews.
- **Async validation** for minimal APIs and Blazor — available in previews; **async data-annotation attribute support in the core libraries is still coming**.
- **Blazor static SSR parity features** (in previews): `EnvironmentBoundary`, `Label`, `DisplayName`, QuickGrid `OnRowClick`, temp data, variable-height virtualization, client-side validation without interactivity, **localized data-annotation validation messages**.
- **Blazor Server pause/resume** for idle circuits.
- **Blazor WebAssembly runtime move to CoreCLR** — **preview in .NET 11, stable in .NET 12.**
- **Blazor WebWorker project template** — available now in previews.
- **C# unions** — coming to C# and being lit up across ASP.NET Core.
- **Blazor Gateway + Blazor Aspire hosting integration package + Blazor WASM service-defaults template** — new for .NET 11; **dashboard-launched debugging is planned/"coming."**
- **Agentic hosting in ASP.NET Core** via Microsoft Agent Framework (OpenAI responses, A2A, AGUI, MCP via the MCP C# SDK).
- **AGUI support in Microsoft Agent Framework** — **currently in preview**; **Blazor AI components are prototype** (names not final).
- **.NET Skills repo/marketplace (`dotnet/skills`)** — new Blazor/ASP.NET Core skills "just landed recently," with **custom agents, tools, and eval suites** being explored/built.

## 💡 Demos
1. **Minimal API — OpenAPI 3.2 + native OTel:** browsed the OpenAPI doc (confirmed 3.2) and the console showing out-of-the-box OpenTelemetry semantic conventions for HTTP request/response/route; code only adds the `Microsoft.AspNetCore` trace source. *Proved:* OpenAPI 3.2 and zero-instrumentation tracing on upgrade.
2. **Blazor static SSR components:** `EnvironmentBoundary`, `Label`, `DisplayName` (incl. QuickGrid headings), QuickGrid `OnRowClick` (selects/displays a person), temp data via `[SupplyParameterFromTempData]` (POST→redirect→GET server-time message), and variable-height virtualization with 10,000 items. *Proved:* MVC-grade SSR features now exist in Blazor.
3. **Validation:** client-side validation on a non-interactive static SSR page (DevTools shows no Blazor WebSocket / no WASM), EN→ES **localized** validation messages, and **async** unique-username check (`admin` taken) with in-flight UI and `EditContext.ValidateAsync`. *Proved:* rich validation without falling off the interactivity cliff, localized, and async-capable.
4. **Blazor WebWorker:** crunching ~250k sales records — UI-thread run freezes a health counter; web-worker run (`[JSExport]` `AnalyzeSalesData`) keeps the counter and UI responsive. *Proved:* offload CPU-intensive work off the UI thread today (with the message-passing/2nd-runtime caveats).
5. **Standalone Blazor WASM + Aspire:** AppHost wiring the API, WASM project, and **Blazor Gateway**; Aspire dashboard shows Gateway (WASM nested) + API; weather page works via Aspire **service discovery**; structured logs + traces show end-to-end proxying through the Gateway; **browser-exported metrics** (page navigations) appear in the dashboard. *Proved:* production-grade WASM hosting with full config/service-discovery/observability.
6. **AGUI Dojo (React → Blazor):** React/Copilot-Kit reference app, then a Blazor implementation — `MapAGUI` server endpoints with a `GetWeather` tool, an `IChatClient`-based AGUI chat client, **front-end tool call** (change background color), **back-end tool call** with a custom weather widget, **human-in-the-loop** plan confirm/reject, **streaming long-running** plan ("going to Mars"), and full UI↔agent state sharing; plus prototype `AgentBoundary`/messages/loading components. *Proved:* you can build rich agentic UIs in Blazor with AGUI.
7. **Blazor "Plan UI change" skill:** a Kanban app built **without** the skill (~300–400-line monolithic `Board.razor`) vs **with** the skill (cleanly factored subcomponents + component parameters), both functional. *Proved:* .NET Skills make coding agents produce more idiomatic, better-factored Blazor.

## 📊 Notable Stats / Quotes
- **.NET 11 ASP.NET Core roadmap = 6 themes** (feedback, foundation, modern stack, distributed/Aspire, agentic, Copilot-assisted dev).
- **4 investment areas** for AI-assisted .NET dev: agentic skills, custom agents, tools, eval suites.
- **Zstandard ≈ Brotli-level compression ratios at much lower CPU cost.**
- **CoreCLR WASM runtime:** preview in **.NET 11**, stable in **.NET 12**.
- **Virtualization demo:** ~**10,000 items** rendered efficiently with variable heights.
- **WebWorker demo:** ~**a quarter-million (250k)** sales records — froze the UI thread, smooth on a worker.
- **Kanban-skill demo:** monolithic board file ≈ **300–400 lines** before the skill vs cleanly factored subcomponents after.
- .NET runs some of the **biggest services in the world at Microsoft — Entra, Bing, Teams, Xbox, and most of Azure** — and those workloads push the bar for everyone.
- *"When you upgrade to .NET 11, your apps run faster, safer, and are more observable. No code changes required."*
- *"If we can't measure it, we don't really know if it works. The eval suite helps keep us honest."*
- *"We want AI coding assistants to love working with .NET as much as you do."*
- *"Don't get too attached to the specific names here"* — re: prototype Blazor AI component names.
- Speaker: **Daniel Roth**, Principal Product Manager for ASP.NET Core and Blazor.

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Install the **.NET 11 preview SDK** (`get.net 11`) and scaffold a **Blazor WebWorker** project; benchmark a real CPU-bound task on/off the UI thread.
  - Stand up the **standalone Blazor WASM + Aspire + Blazor Gateway** sample; confirm service discovery + browser OTel land in the Aspire dashboard.
  - Build a minimal **AGUI** endpoint with `MapAGUI` + a server tool, and try a **front-end tool** (e.g. change UI state) using the Blazor AGUI chat client.
  - Install the **Blazor** and **ASP.NET Core** plugins from `dotnet/skills`; rerun a UI task (Kanban-style) with/without the **"Plan UI change"** skill to compare factoring.
  - Turn on **OpenAPI 3.2** + verify native **OpenTelemetry** tags appear without the OTel instrumentation package.
- [ ] Questions:
  - When does the **CoreCLR WASM** preview ship in a .NET 11 preview, and what's the perf/size delta vs mono?
  - What's the **memory overhead** of a Blazor WebWorker (second WASM runtime) in practice for typical workloads?
  - Timeline for **async data-annotation attributes** in `System.ComponentModel.DataAnnotations` (the core-library half of async validation)?
  - Will the **Blazor AI component** names/APIs stabilize before .NET 11 GA, and where to track them?
  - Does the **Blazor Gateway** fully replace reverse-proxy/CORS setups in production, and how does session affinity behave at scale?
- [ ] Relevant to:
  - Any .NET web modernization (upgrade-only perf/security/observability wins).
  - Teams building **Blazor static SSR** apps wanting MVC-parity (forms, validation, temp data).
  - **Aspire** adopters hosting standalone Blazor WASM with end-to-end telemetry.
  - Teams building **agentic web apps / agentic UIs** on .NET (Agent Framework, AGUI, MCP).
  - Improving **Copilot/coding-agent** effectiveness on .NET codebases via the .NET Skills.

## 🔗 Related
- [[2026 Build Session List]]
- Microsoft Agent Framework / Microsoft.Extensions.AI sessions
- .NET
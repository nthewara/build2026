---
created_by_me: true
tags:
  - zone/areas
  - zone/areas/literature_notes
  - type/literature_note
  - event/msbuild2026
  - topic/dotnet-maui
  - topic/edge-ai
  - topic/mobile
  - topic/ai
  - topic/dotnet
source: https://www.youtube.com/watch?v=YSr1W-d4GVw
session_code: OD803
event: Microsoft Build 2026
speakers: Gerald Versluis (Microsoft, .NET MAUI team)
duration_min: 46
aliases:
  - Taking your AI to the edge with NET MAUI
---

# OD803 — Taking your AI to the edge with .NET MAUI

> [!info] Session Info
> **Event:** Microsoft Build 2026  
> **Speakers:** Gerald Versluis — Senior Software Engineer, Microsoft (.NET / .NET MAUI team)  
> **Duration:** ~46 min  
> **Watch:** [YouTube](https://www.youtube.com/watch?v=YSr1W-d4GVw)

## 🎯 TL;DR
A state-of-the-union for .NET MAUI covering three threads: (1) what shipped in **.NET MAUI 10** (Nov 2025) under the banners *stable, fast, simple, modern* — big XAML investments, safe-area APIs, Android Material 3, and steady monthly service releases; (2) how the MAUI team re-tooled its **entire engineering pipeline around GitHub Copilot / agentic engineering**, taking Copilot-authored merged PRs from **7% to 62% in under a year**; and (3) where MAUI is going with **.NET 11** (Nov 2026) — CoreCLR as the default runtime, `dotnet run`/`dotnet watch` CLI support, map improvements, and a heavy **on-device AI** push. The AI story centers on **Maui Labs** experiments: **Essentials.AI** (unified on-device AI across Apple Intelligence, Gemini Nano, Windows Copilot Runtime/Phi Silica), **AI Extensions** (intent-driven navigation), **DevFlow** (lets Copilot see/drive a running app for autonomous testing), and **Maui Sherpa** (a MAUI-built dev tool). Recurring message: ship native AI apps everywhere, build them with agents, and lean on CLI-first tooling because it's "agent-friendly."

## 🔑 Key Takeaways
- **.NET MAUI** = .NET Multi-platform App UI: single project / single C# codebase targeting **iOS, Android, Windows, macOS**, mapping to **native controls and native styling** with built-in device APIs (geolocation, flashlight, file system, etc.).
- Three UI strategies coexist: **fully native MAUI**, **Blazor Hybrid** (wrap an existing Blazor app/control in a WebView and ship to stores), and the **HybridWebView** for React Native / Angular / other JS apps — mix-and-match seamlessly within one app.
- The MAUI team went **fully agentic end-to-end**: Copilot now does repro, testing (smart selection of relevant UI tests), fixing, **MAUI-aware code review**, post-merge learning, and even auto-drafting docs/blog PRs.
- **Copilot-authored merged PRs jumped from 7% → 62% in under a year** (inflection point ~November); transparency dashboard at **agenticengineers.net**.
- **.NET MAUI 10** (released **Nov 2025**) focused on **quality, performance, simplicity, modern APIs**; subsequent **monthly service releases** add fixes/features non-breakingly (SR6 = 242 commits, the biggest yet; SR7 continued the momentum).
- **XAML overhaul:** global XMLNS/implicit namespaces to kill boilerplate, plus **XAML Source Generation** (Roslyn → readable, debuggable C#) — opt-in in .NET 10, **default in .NET 11**.
- **XAML Source Gen perf claims:** ~**1,000% faster inflation**, **99% less debug memory**, faster release, smaller app memory; eliminates debug-vs-release trimming surprises so release == debug behavior.
- New **unified Safe Area Edges API** (`SafeAreaEdges`, e.g. `None`/`SoftInput`) settable per page/layout to handle notches, Dynamic Island, camera holes, and bottom gesture areas on iOS + Android (works nicely with iOS *liquid glass*).
- **Android Material 3** is rolling in via service releases (opt-in `UseMaterial3`); full experience lands in **.NET 11**.
- **.NET 11 headline:** **CoreCLR becomes the default runtime** on iOS/Android/Mac Catalyst (replacing **Mono**), unifying the runtime with ASP.NET/Azure and unlocking **.NET Trace / .NET Counters** profiling; opt-out is a one-liner; small app-size increase expected.
- **CLI-first tooling:** `dotnet run` (with interactive target/device picker) and `dotnet watch` (terminal hot reload) for MAUI — explicitly designed to be **agent-friendly** (easy for Copilot to invoke and parse).
- **Maps control** gains **pin clustering, custom pins via ImageSource, richer interactions** (long-press, tappable map elements/polylines/clusters), visibility/Z-index control, and Android style JSON.
- **On-device AI via Essentials.AI** (`Microsoft.Maui.Essentials.AI`, built on `Microsoft.Extensions.AI`): one API over **Apple Intelligence, Gemini Nano, Windows Copilot Runtime (Phi Silica)**, plus local (ONNX) and cloud (Azure OpenAI / Foundry) — swap providers with no code change.
- **AI Extensions** enable **intent-driven** apps: tag a C# method as an AI tool (e.g. `LogShot`) and the LLM routes user intent to the right action instead of manual button navigation.
- **DevFlow** injects a debug-time HTTP/agent server into the running MAUI app so Copilot can read the visual tree, screenshot, read sensors, and interact with controls to **test apps autonomously** (wrapped in an **MCP server** powering the MAUI VS Code extension).
- **Maui Sherpa** is a new all-in-one MAUI dev tool (visual tree inspector, live property inspector, network/profiling/logs, iOS certificate/device setup management) — itself **built with .NET MAUI** using the experimental macOS AppKit + Linux backends ("Maui everywhere").
- Strong **partner ecosystem momentum:** Syncfusion (free MAUI Toolkit, 30+ controls), Uno (SkiaSharp investment), Avalonia (embeds MAUI to reach **Linux and browser**).

## 📚 Detailed Notes

### What .NET MAUI is (refresher)
.NET MAUI = **.NET Multi-platform App UI**, Microsoft's offering for building cross-platform, native-looking apps on **iOS, Android, Windows, and macOS** from **C# and .NET**. The value proposition:
- **Single project, single codebase** launches all four platforms.
- Everything **maps to native controls and native styling**, so the app looks and feels correct for the OS/device it runs on.
- A **unified C#/.NET device-API layer** exposes geolocation, flashlight, file system, and many more capabilities, plus a large set of built-in controls.

### The choice spectrum: native, Blazor Hybrid, HybridWebView
The .NET ecosystem deliberately offers a range so any developer/audience is covered:
- **Fully native MAUI** — maximum native power on real devices.
- **Blazor Hybrid** — take an existing Blazor app (or even a single Blazor control) and host it in a Blazor Hybrid WebView, package it as a mobile app, and put it in the stores. You can make the **whole** app a Blazor Hybrid app *or* embed just a small Blazor part inside an otherwise-native app — the integration is seamless and indistinguishable.
- **HybridWebView** — for existing **React Native, Angular, or other JavaScript** apps, reuse them via the hybrid web view.
- Rule of thumb: **for reach → Blazor (web)**; **for full native power → MAUI**; and the **Blazor + MAUI combination** sits powerfully in between, reusing existing web-dev experience.

A highlighted customer story: **Motime** (UK) makes **pediatric physiotherapy devices** with a **.NET MAUI companion app** — cited as the kind of real-world, medical-space use of MAUI the speaker loves (full customer stories on the MAUI website).

### Agentic engineering: how the MAUI team re-tooled itself
The biggest narrative shift: over the past months the .NET / .NET MAUI team **incorporated Copilot and AI fully end-to-end** in their SDLC. It is **not just code generation**. Across the open-source MAUI repo, Copilot is used for:
- **Reproduction** — ask Copilot to try to reproduce a customer-reported GitHub issue (repro is often the hard part).
- **Testing** — the repo has **thousands of UI tests** that take a long time to run. Copilot is told to figure out which UI tests are **relevant** to a given PR/bug and run only those, returning results — saving the human the triage/wait.
- **Fixing** — assign a bug to Copilot ("assign to Copilot") and it goes off and produces fixes.
- **MAUI-aware code review** — MAUI is a **very complex codebase** (lots of non-.NET-native iOS/Android APIs), so the team built a **custom MAUI-aware reviewer** baked into their pipelines. It carries MAUI-specific expertise beyond the vanilla GitHub Copilot reviewer and flags "look out for this/that." Humans remain in the loop, but it's been a big help.
- **Verification & learning** — when something good or bad happens to a PR, a **custom Copilot agent** is pointed at it to answer "what can we learn from this PR?", and that learning is carried into future PRs to prevent recurrence.
- **Post-merge automation** — on merge, an **agentic workflow** decides whether the change needs a **docs update** or a **blog post**, and if so it **opens an issue and even drafts the PR** for the doc/blog change.

**Transparency & numbers:** As an open-source project they publish this openly at **agenticengineers.net**, showing per-PR whether code was Copilot-generated, the PR was Copilot-authored, and whether the Copilot reviewer was used — across the MAUI repos plus supporting products (Android, iOS) and tooling. Momentum picked up in **November**, climbing through Dec–April (**April** the high point so far): **7% → 62% Copilot-authored merged PRs in under a year.** This velocity lets the team ship bug fixes and previously-deprioritized functionality much faster.

### Community
MAUI is positioned as community-driven. Key threads:
- **Contributors** thanked for issues, PRs, samples, docs, and feedback (online + in-person). Team members out at conferences: the speaker (Gerald), **David Ortinau**, **Stefan**, and now **Jacob**.
- **Community Stand-up** — first Thursday of every month on YouTube (the .NET channel), usually with a guest / community highlights / new things the team built.
- **Maui Days** — dedicated community-run MAUI events (a continuation of the old Xamarin days). Held in Cologne, two in London, with **Krakow, Poland** coming up and more; the team will help bring one to your area.
- **MauiVerse** (mauiverse.net) — a community hub with a **Discord server** to talk to the team and community, sharing tools, samples, libraries, blog posts, and projects.
- **Partners / component vendors** build controls and ecosystems on top of MAUI (check them out for pre-built UI).

### Partner collaborations announced
- **Syncfusion** — working directly on the MAUI codebase (code fixes, testing across the suite). They created a **.NET MAUI Toolkit**, now **v1.0.10 with 30+ UI controls** (some previously from the paid Syncfusion suite) now **free**, built for performance, customization, and accessibility. Syncfusion also published numbers on their own Copilot/AI velocity gains: **50–70% time reduction** on repro/fix work, **2–3× more issues handled per week**, more PRs and a higher first-time fix rate.
- **Uno Platform** — partnered on **SkiaSharp** (maintained at Microsoft); Uno stepped up and invested in taking it to the next major version.
- **Avalonia** — proposed **embedding .NET MAUI apps in an Avalonia backend**, which brings **MAUI to Linux and the browser**; they published a getting-started blog post.

### .NET MAUI 10 (released November 2025): stable, fast, simple, modern
The four investment areas:
- **Quality** — upgrades must not break you; fixing more bugs than ever.
- **Performance** — mobile end-users are the most critical (slow startup / sluggishness gets noticed instantly), so perf is always top of mind.
- **Simplicity** — APIs should be simple to use so new features are easy to implement.
- **Modern** — keep up with new Android/iOS versions so modern platform behavior shows up in MAUI apps automatically.

#### XAML investments
XAML is "here to stay" and got major improvements:
- **Global namespaces (global XMLNS)** — reduce or completely eliminate XML namespace declarations, making even small XAML docs far less verbose by removing boilerplate.
- **Implicit namespaces** — in **preview in .NET 10**; the editor/language-service support promised at .NET Conf (November) is now available, so it can be tried with editor support today.
- **XAML Source Generation** — all XAML is taken through **Roslyn** and source-generated into **actual, readable, debuggable C#** (vs the current XamlC path that compiles to intermediate language). Big perf benefits and easier to build further tooling on. **Opt-in in .NET 10, default in .NET 11** — the team urges testing now and sending feedback so it's rock-solid by .NET 11.
  - **Enable it:** set `MauiXamlInflator` to `SourceGen` (one MSBuild property). Optionally set `EmitCompilerGeneratedFiles=true` to inspect the generated C# in your IDE (e.g. VS Code) and debug through it.
  - **Claimed gains (described as conservative/old numbers):** ~**1,000% faster inflation**, **99% less debug memory**, faster on release, less app memory — **biggest gain in debug builds** (which tend to be jittery, e.g. Android CollectionView scrolling).
  - **Bonus:** removes debug-vs-release **trimming differences** — release builds behave the same as debug, so nothing "suddenly breaks at runtime" because an API got trimmed out during optimization.
  - A comparison shown on a **Pixel 5 / Android 14**: XamlC takes noticeably longer than Source Gen across the same navigation operations.

#### Safe Areas (unified API)
The cross-platform problem: iOS introduced the **notch / Dynamic Island** and bottom **swipe-gesture** areas; Android has **camera holes / islands**. These zones are hard to use well — white/black boxes look bad, and you shouldn't place tappable buttons behind a Dynamic Island.
- New **unified Safe Area Edges API**: set `SafeAreaEdges` to values like **`None`** or **`SoftInput`** to control whether content draws under these regions or reserves space. Settable **per ContentPage or per layout** (Grid, ScrollView, etc.).
- Works on **Android and iOS** (the platforms with these form factors); other platforms get implementations if/when needed.
- Examples shown: setting `SafeAreaEdges="None"` lets content draw under the iOS region and pair nicely with **liquid glass**; on Android it draws under the top status-bar area while **preserving reachable navigation-bar buttons** at the bottom.

#### Android Material 3
Work is underway to implement **Material 3** on Android. The **first controls** already shipped in .NET MAUI 10 via service releases. Opt in with one line (`UseMaterial3`) in the `.csproj` and Android controls update to Material 3 where available. Bigger layout changes are still coming; the **full Material 3 experience lands in .NET 11**. Strong encouragement to try it today and send feedback.

#### Service releases
After the initial .NET MAUI 10 GA in November, **roughly monthly service releases** add fixes/features non-breakingly:
- **SR6** — biggest yet at **242 commits**.
- **SR7** — kept the momentum.
- Content across releases: **quality** (CollectionView/CarouselView handler fixes, Shell polish, accessibility test coverage), **modern APIs** (the **MediaPicker** modernized for new iOS/Android image/video-picking APIs), **safe areas** and **Material 3** enablement, **hybrid** improvements (JavaScript interop / message-passing over the JS↔C# bridge), and **tooling** (Android `dotnet run` support, design-time build speedups, better VS / VS Code loops).
- Reminder to try the **live property inspector** and **live XAML preview** in Visual Studio — launch via hot reload / XAML live preview and see changes in real time without stopping the app.

### .NET 11: the next wave (GA November 2026)

#### CoreCLR becomes the default runtime
The headline (and "not very glamorous but very visible") change: until now iOS/Android/macOS still ran on **Mono**. In .NET 11, **CoreCLR becomes the default runtime** on **iOS, Android, and Mac Catalyst** for MAUI (and the other platforms used directly), giving **one runtime** shared with ASP.NET, Azure services, and other .NET workloads.
- Automatically inherits .NET's performance upgrades.
- Unlocks diagnostics tooling: **.NET Trace** and **.NET Counters** now (great time to start profiling); more tools under consideration.
- **Opt-out** is a one-liner if anything goes wrong, but a smooth transition is expected with mostly upside.
- Tradeoff noted (still in preview): **app size increases a little**, balanced by the other gains; the team will keep optimizing.

#### CLI-first tooling (agent-friendly)
- **`dotnet run` support** — replaces verbose `dotnet build -t:run -f net10.0-android …`. Just `dotnet run`; if no target framework is specified it shows an **interactive prompt** to pick Android/iOS and the specific **emulator/simulator/device**, then launches.
- **`dotnet watch` support** — **terminal hot reload**: `dotnet watch` starts on the Android/iOS emulator and live-applies code changes to the running debug session.
- Rationale: CLI tools are **easy for Copilot to invoke and to parse output from** — "very agent-friendly" — while also pleasing terminal fans and human pilots. Expect more CLI tooling across .NET generally.

#### Maps control improvements ("more pins on the map")
The MAUI `Map` control (Google Maps on Android, Apple Maps on iOS) gains:
- **Pin clustering** — group nearby pins (e.g. a "7" cluster = Copilot Lab + six more) that expand on zoom-in; steerable grouping (group by name, etc.).
- **Custom pins** — just specify an **ImageSource** (no custom handlers needed), with callouts (e.g. "Microsoft Commons").
- **Richer interactions** — map long-press, tappable **map elements** (polylines, circles, shapes) that run code on click, and tappable clusters.
- **More control** — toggle element visibility, set **Z-index/order**, and on **Android** customize styling via **style JSON**.

#### Other .NET 11 previews (try now)
Less XAML ceremony (resource generation by default, implicit namespaces by default), **better compiled-bindings diagnostics**, **C# in XAML / code-in-XAML support** (long-requested), built-in **long-press gesture recognizer**, **badges on Shell tabs and ToolbarItems** (like app-icon notification badges), **Android themed (monochrome) icons**, more permissions, **trimmable CSS** (smaller app size), and more.

### Putting the AI in MAUI — Maui Labs
"MAUI has always been 50% AI — the letters are right there." To move faster, the team created **Maui Labs**: a vehicle to ship **experiments** quickly (most may stick, some may not), with the community welcome to try, suggest ideas, or collaborate. Key Maui Labs items:

#### Essentials.AI
`Microsoft.Maui.Essentials.AI`, built on top of **`Microsoft.Extensions.AI`** (the unified library/API to work with any AI model, local or remote, with no code change). Essentials.AI adds **on-device / platform-native** providers:
- **Apple Intelligence** (iOS/macOS)
- **Gemini Nano** (Android)
- **Windows Copilot Runtime via Phi Silica** (Windows)
- Plus **local models (ONNX)** and **cloud** (Azure OpenAI / Foundry).
- Same paradigm as MAUI: use the abstractions (`IChatClient`, embedding generator, etc.) and **swap between cloud / local / platform-native with zero code change**, "zero config, OS-managed, tight integration."
- A platform-support matrix was shown: **Apple** supports nearly everything (single-turn chat, multi-turn conversation, system prompts, …); **Android** and **Windows** each miss one or two features for now — a normal cross-platform reality to plan around.

#### AI Extensions (intent-driven apps)
Today's apps are **reactive** (you click to act). With LLMs, apps can be **intent-driven**: the user states what they want and the app figures out how to get there — no manual menu/button hunting.
- Mechanism: put an **attribute on a C# method** declaring it an **AI tool** (example: `LogShot`). The LLM can then route a spoken/typed intent ("log this coffee shot") to that exact C# method and invoke the code — the model determines the path inside your app.

#### More backends (via Copilot capacity)
With Copilot freeing up time, the team added **new backends**:
- **Linux** (natively where **GTK4** runs)
- **macOS via AppKit** (a true macOS backend, distinct from Mac Catalyst)
- **WPF**, with possibly more to come.

#### DevFlow
`aka.ms/mauidevflow` — a companion that lets Copilot **see and drive a running app** to verify itself. Built on the new **.NET MAUI CLI**:
- The CLI can **check your environment** (emulators present, Android SDK set up, Xcode installed correctly).
- It can **steer DevFlow** by connecting to a small **agent app injected into your MAUI app at debug time only** (a debug-time **HTTP server** inside the app — never shipped to production).
- Through that, you (or Copilot) can read the **visual tree** of the current screen, take a **screenshot**, read **sensor values**, and **interact with elements/buttons** to programmatically walk the app. This makes autonomous testing possible: tell Copilot to build an app, derive edge cases/test scenarios, and "run through this autonomously" — and it does.
- It is also **wrapped in an MCP server**, which in turn powers the **.NET MAUI VS Code extension**, combining these tools with built-in ones to deliver a "best-in-class" agentic engineering experience for MAUI apps.

#### Maui Sherpa
A new tool that brings much of this together for the **best MAUI dev experience**. Shown against the Barista Notes app, it offers:
- **Visual-tree inspector** (like browser dev tools)
- **Live property inspector** (edit properties and see them live-update in the running app)
- **Network traffic inspection, profiling, and logs** — all in one place
- **iOS certificate managers** and broader **device/developer-setup inspection** for releasing.
- Likely works beyond MAUI for some of this. Notably, **Maui Sherpa is itself built with .NET MAUI**, using the **experimental backends** — a beautiful **macOS AppKit** UI that also runs on **Linux** via the new Maui Labs Linux backends. "Full circle… Maui everywhere: with Maui, by Maui, through Maui."

### Release schedule reminder
.NET MAUI's support lifecycle differs from .NET generally (because it depends on third-party tools/SDKs): **each major .NET MAUI version is supported for 18 months**. New major versions ship **12 months apart**, so when a new major releases there are **6 months** of overlap before the previous major goes out of support. **.NET 11 ships November 2026** with everything shown in this session.

### Closing message
"Build with agents, ship AI on device, native apps everywhere with .NET MAUI."

## 🛠️ Products / Features / Technologies Mentioned
- **.NET MAUI** — .NET Multi-platform App UI; cross-platform native apps (iOS/Android/Windows/macOS) from one C# codebase.
- **Blazor Hybrid** — host an existing Blazor app/control in a WebView and ship as a native/store app; mix with native MAUI.
- **HybridWebView** — embed existing JS apps (React Native, Angular, etc.) inside a MAUI app.
- **GitHub Copilot** — used end-to-end for repro, testing, fixing, review, learning, and docs/blog automation in the MAUI pipeline.
- **MAUI-aware code reviewer** — a custom Copilot reviewer in the team's pipelines with MAUI-specific expertise.
- **agenticengineers.net** — public dashboard showing per-PR Copilot generation/authoring/review across MAUI repos and tooling.
- **Global XMLNS / implicit namespaces** — XAML features to reduce/eliminate namespace boilerplate (implicit ns in preview).
- **XAML Source Generation** — Roslyn-based generation of readable, debuggable C# from XAML (`MauiXamlInflator=SourceGen`); opt-in .NET 10, default .NET 11.
- **Safe Area Edges API** (`SafeAreaEdges`, e.g. `None`/`SoftInput`) — unified handling of notch/Dynamic Island/camera holes/gesture areas, per page/layout.
- **Android Material 3** — opt-in (`UseMaterial3`) Material 3 styling for Android controls; full experience in .NET 11.
- **MediaPicker** — modernized image/video picking APIs for iOS/Android.
- **CoreCLR** — becomes the default MAUI runtime on iOS/Android/Mac Catalyst in .NET 11 (replacing **Mono**).
- **.NET Trace / .NET Counters** — diagnostics/profiling tools usable with the CoreCLR move.
- **`dotnet run` / `dotnet watch`** — CLI run (with interactive device picker) and terminal hot reload for MAUI; agent-friendly.
- **Maps control** — native maps (Google Maps/Apple Maps) with new pin clustering, custom pins, richer interactions, Android style JSON.
- **Live property inspector / live XAML preview** — real-time inspection/preview in Visual Studio via hot reload.
- **Maui Labs** — initiative for fast-shipping experimental MAUI features (DevFlow, Essentials.AI, AI Extensions, new backends).
- **`Microsoft.Extensions.AI`** — unified .NET AI abstraction (`IChatClient`, embedding generators) across providers.
- **Essentials.AI** (`Microsoft.Maui.Essentials.AI`) — on-device AI over Apple Intelligence, Gemini Nano, Windows Copilot Runtime (Phi Silica), plus ONNX local and Azure OpenAI/Foundry cloud.
- **Apple Intelligence / Gemini Nano / Windows Copilot Runtime (Phi Silica)** — platform-native on-device AI providers.
- **ONNX (Onyx)** — local on-device model runtime option.
- **Azure OpenAI / Azure AI Foundry** — cloud AI model providers behind the same abstraction.
- **AI Extensions** — attribute-based exposure of C# methods as AI tools for intent-driven app navigation.
- **New backends** — Linux (GTK4), macOS AppKit (distinct from Mac Catalyst), WPF (experimental, via Maui Labs).
- **DevFlow** (`aka.ms/mauidevflow`) — new .NET MAUI CLI + debug-time in-app agent (HTTP server) + MCP server letting Copilot see/drive a running app; powers the MAUI VS Code extension.
- **.NET MAUI VS Code extension** — consumes DevFlow/MCP tools for agentic MAUI development.
- **Maui Sherpa** — all-in-one MAUI dev tool (visual tree, live properties, network/profiling/logs, iOS certs/device setup); built with MAUI on AppKit + Linux backends.
- **Syncfusion .NET MAUI Toolkit** — free, v1.0.10, 30+ UI controls (some ex-paid), perf/customization/accessibility-focused.
- **Uno Platform** — partnered on **SkiaSharp** (next major version investment).
- **SkiaSharp** — Microsoft-maintained 2D graphics library; advanced by Uno.
- **Avalonia** — embeds MAUI apps in its backend to reach **Linux and browser**.
- **MauiVerse** (mauiverse.net) — community hub + Discord.
- **Motime** — UK customer: pediatric physiotherapy devices with a .NET MAUI companion app.

## 🚀 Announcements / What's New
- **.NET MAUI 10** GA in **November 2025** (stable/fast/simple/modern), with monthly **service releases** (SR6 = 242 commits, SR7 momentum).
- **XAML Source Generation** — opt-in in .NET 10, **becomes default in .NET 11**.
- **Implicit namespaces** — **preview** in .NET 10 with new editor/language-service support now available.
- **Unified Safe Area Edges API** — shipped for Android + iOS.
- **Android Material 3** — first controls shipped via .NET 10 service releases (opt-in); full experience targeted for **.NET 11**.
- **CoreCLR as default runtime** on iOS/Android/Mac Catalyst — **coming in .NET 11** (currently in previews; opt-out one-liner; small app-size increase).
- **`dotnet run` and `dotnet watch`** support for MAUI (Android `dotnet run` already in .NET 10 service releases).
- **Maps control** enhancements (pin clustering, custom pins, richer interactions, Android style JSON) — for **.NET MAUI 11**, **first previews out now**.
- **.NET 11 preview features** (try now): resource generation by default, implicit namespaces by default, better compiled-bindings diagnostics, C#-in-XAML, built-in long-press gesture recognizer, Shell tab + ToolbarItem badges, Android themed/monochrome icons, more permissions, trimmable CSS.
- **Maui Labs** initiative launched, including **Essentials.AI**, **AI Extensions**, **DevFlow**, and new **Linux / macOS AppKit / WPF backends** (experimental/preview).
- **Maui Sherpa** tool announced (download via session link).
- **Partner announcements:** Syncfusion free **MAUI Toolkit v1.0.10** (30+ controls); **Uno** SkiaSharp investment; **Avalonia** MAUI-embedding for Linux/browser.
- **.NET 11 GA targeted for November 2026.**

## 💡 Demos
- **XAML Source Gen vs XamlC comparison** — side-by-side on a **Pixel 5 / Android 14** showing Source Gen completing the same navigation operations much faster than XamlC.
- **Safe Area Edges** — before/after screenshots on iOS (content drawing under the region with liquid glass) and Android (drawing under the top bar while preserving tappable nav-bar buttons) via `SafeAreaEdges="None"`.
- **`dotnet run` interactive picker** — menu to choose target framework and emulator/simulator/device, then launch.
- **Autonomous app build + test (Copilot CLI + DevFlow)** — a (sped-up) **Copilot CLI** session building a to-do app (a **Blazor Hybrid** app) and **autonomously driving the iOS simulator**: deciding where to click, what to test, and verifying results, with several tests passing — the mouse moves but Copilot, not a human, is interacting.
- **Barista Notes app (David Ortinau)** — tracks espresso shots and gives AI-powered advice using `Microsoft.Extensions.AI` + Essentials.AI. Voice intent demo: asked "How many cups of coffee do I need to make for the people in this room?", the app auto-opens the **camera**, takes a picture, counts the people, and answers (**18** for the shown photo). Also shows the **`LogShot` AI tool** attribute routing a "log this coffee shot" intent to a C# method.
- **Maui Sherpa** — live demo against Barista Notes: visual-tree inspection, live property editing that updates the running app, network/profiling/logs, and iOS certificate/device setup.

## 📊 Notable Stats / Quotes
- **7% → 62%** Copilot-authored merged PRs **in under a year** (inflection ~November).
- **XAML Source Gen:** ~**1,000% faster inflation**, **99% less debug memory**, faster release, less app memory ("these numbers are not inflated — pun intended").
- **Service Release 6 = 242 commits** (biggest service release yet).
- **Syncfusion:** **50–70% time reduction** on repro/fix work; **2–3× more issues** handled per week with AI/Copilot.
- **Syncfusion .NET MAUI Toolkit:** **v1.0.10**, **30+ UI controls**, free.
- **Maps:** a single cluster shown representing **7 pins** (Copilot Lab + 6 more); Barista demo counted **18 people**.
- **Support lifecycle:** **18-month** support per major MAUI version; new majors **12 months** apart with **6 months** overlap.
- **"MAUI has always been 50% AI — the letters are right there."**
- **"Build with agents, ship AI on device, native apps everywhere with .NET MAUI."**

## 🧠 My Notes / Follow-ups
- [ ] Things to try:
  - Flip `MauiXamlInflator=SourceGen` (+ `EmitCompilerGeneratedFiles=true`) on a real MAUI project and measure debug startup/scroll perf before .NET 11 makes it default.
  - Apply the new `SafeAreaEdges` API (e.g. `None`) to clean up notch/status-bar/gesture-area layouts on iOS + Android.
  - Opt into Android **Material 3** (`UseMaterial3`) and report rough edges.
  - Test the **CoreCLR** preview on iOS/Android/Mac Catalyst; wire up **.NET Trace / .NET Counters** profiling and note app-size delta.
  - Use `dotnet run` / `dotnet watch` for the MAUI inner loop (and from a Copilot/agent workflow).
  - Prototype **Essentials.AI** with a provider swap (Azure OpenAI ↔ ONNX local ↔ Apple Intelligence/Gemini Nano/Phi Silica) and confirm zero code change.
  - Try **AI Extensions** intent navigation: tag a C# method as an AI tool and drive it by voice/text.
  - Install **Maui Sherpa** and **DevFlow** (`aka.ms/mauidevflow`); have Copilot autonomously test a sample app via the MCP server + VS Code extension.
  - Evaluate the free **Syncfusion .NET MAUI Toolkit** controls in a project.
- [ ] Questions:
  - What's the concrete app-size increase from CoreCLR in practice, and does it net out after trimming/optimization?
  - Which Essentials.AI features are still missing on Android vs Windows (the matrix showed gaps) and what's the timeline?
  - Is DevFlow's in-app debug agent fully isolated from release builds, and what's the security model for the injected HTTP server?
  - Does Maui Sherpa support non-MAUI (other .NET UI) projects, as hinted?
- [ ] Relevant to:
  - On-device / edge AI mobile apps (privacy-sensitive, offline, low-latency inference).
  - Cross-platform .NET app teams modernizing XAML and upgrading to .NET 11.
  - Anyone standardizing an **agentic engineering** pipeline (Copilot for repro/test/review/docs) on an OSS or internal repo.

## 🔗 Related
- [[Microsoft Build 2026]]
- `Microsoft.Extensions.AI` / on-device AI (Apple Intelligence, Gemini Nano, Phi Silica, ONNX)
- agenticengineers.net — agentic engineering metrics
- mauiverse.net — MAUI community hub
